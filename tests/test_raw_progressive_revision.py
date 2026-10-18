"""Regression checks for the observed run failures and revised workload policy."""
import json
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from searchgym.agent import SearchAgent
from searchgym.config import load_test
from searchgym.explorer import Document
from searchgym.jevtree import JevUsage
from searchgym.llm import Reply
from searchgym.raw_policy import raw_policy
from searchgym.raw_research import RawResearchState, raw_specs
from searchgym.serving import profile_for
import test_rawtree_progressive as progressive_fixture
from test_rawtree_policy import config, GraphDecision, BASE
from test_rawtree import Capture
from test_depthsearch_core import call
from test_reader_integrity import FakeLLM
from offline import FakeTools


class RevisionTests(unittest.IsolatedAsyncioTestCase):
    setup_tree = progressive_fixture.ProgressiveTests.setup_tree
    async def test_parent_count_is_independent_of_page_batch(self):
        tree, decision, fetched, trace, _, log, *_ = await self.setup_tree(jev_expand_batch=4)
        before = len(decision.contexts)
        with self.assertRaisesRegex(ValueError, 'at most 1'):
            await tree.continue_search(log['search_id'], 'first goal', ['S1', 'S2'], trace=trace)
        self.assertEqual(len(decision.contexts), before)
        self.assertEqual(len(fetched), 2)

    async def test_non_initial_search_hit_can_be_read_without_another_search(self):
        tree, _, fetched, trace, _, _, text, _ = await self.setup_tree(jev_entries=1)
        self.assertEqual(fetched, [BASE+'a'])
        self.assertIn('S2', text)
        _, text, stats = await tree.read_source('S2', 'read the alternative', trace=trace)
        self.assertEqual(fetched, [BASE+'a', BASE+'b'])
        self.assertIn('FACT_b', text)
        self.assertEqual(stats['page_visits'], 1)
        self.assertEqual(stats['links_scored'], 0)

    async def test_existing_frontier_is_consumed_without_rescoring_another_parent(self):
        graph = {'a': [(f'c{i}', .9-i*.01) for i in range(4)]}
        tree, decision, _, trace, _, log, *_ = await self.setup_tree(graph, jev_fetch_budget=10)
        await tree.continue_search(log['search_id'], 'first goal', ['S1'], trace=trace)
        before = sum(c['phase'] == 'link' for _, _, c in decision.contexts)
        _, _, stats = await tree.continue_search(log['search_id'], 'first goal', [], trace=trace)
        self.assertEqual(sum(c['phase'] == 'link' for _, _, c in decision.contexts), before)
        self.assertEqual(stats['parent_expansions'], 0)
        self.assertEqual(stats['page_visits'], 2)

    async def test_new_query_reuses_original_question_judgment(self):
        tree, decision, _, trace, *_ = await self.setup_tree()
        state = {'page_url': BASE+'a', 'page_text': 'unchanged document'}
        original = {'type': 'noul', 'instructions': 'original question'}
        for goal in ['first query', 'new query']:
            await tree._noul(state, {'direct_answer': original,
                'query_answer': {'type': 'noul', 'instructions': goal}}, trace,
                usage=JevUsage(), context={'phase': 'probe'})
        calls = [questions for _, questions, ctx in decision.contexts if ctx['phase']=='probe']
        self.assertEqual(set(calls[0]), {'direct_answer', 'query_answer'})
        self.assertEqual(set(calls[1]), {'query_answer'})

    async def test_refresh_replaces_cached_body_without_rewriting_old_evidence(self):
        tree, _, fetched, trace, state, *_ = await self.setup_tree()
        old = dict(state.evidence['S1:0'])
        state.update({'candidates': [{'name': 'Candidate', 'conditions': [
            {'condition': 'fact', 'status': 'supported', 'evidence': ['S1:0']}]}],
            'source_access': [{'source_id': 'S1', 'status': 'unavailable', 'reason': 'body is not the requested paper'}]})
        with self.assertRaisesRegex(ValueError, 'refresh=true'):
            await tree.read_source('S1', 'find the paper', trace=trace)
        async def replacement(url, *, engine):
            fetched.append(url)
            return Document(url, '# Paper\n\nNEW_ORIGINAL_FACT', title='Paper')
        tree.fetch = replacement
        _, text, stats = await tree.read_source('S1', 'find the paper', trace=trace, refresh=True)
        self.assertIn('NEW_ORIGINAL_FACT', text)
        self.assertEqual(state.evidence['S1:0'], old)
        self.assertEqual(state.sources['S1']['status'], 'superseded')
        self.assertEqual(state.candidates['Candidate']['conditions']['fact']['status'], 'unknown')
        self.assertEqual(stats['refreshes'], 1)
        self.assertEqual(stats['browser_fetches'], 1)
        with self.assertRaisesRegex(ValueError, 'already refreshed'):
            await tree.read_source(state.sources['S1']['superseded_by'], 'retry', trace=trace, refresh=True)

    async def test_workload_targets_do_not_stop_searches(self):
        tree, _, _, trace, state, *_ = await self.setup_tree(
            jev_target_visits=1, jev_target_reads=1, jev_target_expansions=1)
        for i in range(9):
            await tree.run_search(f'new relation {i}', [{'link': BASE+f's{i}'}],
                                  question='question', trace=trace, usage=None)
        self.assertEqual(len(tree.sessions), 10)
        self.assertGreater(state.workload['actual']['visits'], state.workload['targets']['visits'])

    async def test_failed_refresh_does_not_revoke_previous_source_evidence(self):
        tree, _, _, trace, state, *_ = await self.setup_tree()
        old = dict(state.evidence['S1:0'])
        state.update({'candidates': [{'name': 'Candidate', 'conditions': [
            {'condition': 'fact', 'status': 'supported', 'evidence': ['S1:0']}]}]})
        async def failed(url, *, engine):
            return Document(url, 'Reader HTTP failure', is_error=True)
        tree.fetch = failed
        _, _, stats = await tree.read_source('S1', 'check source', trace=trace, refresh=True)
        self.assertEqual(stats['fetch_failed'], 1)
        self.assertEqual(state.evidence['S1:0'], old)
        self.assertNotIn('superseded_by', state.sources['S1'])
        self.assertEqual(state.candidates['Candidate']['conditions']['fact']['status'], 'supported')


class ContractTests(unittest.TestCase):
    def test_policy_mismatch_fails_before_calls_and_default_is_progressive(self):
        cfg = load_test('conf.yaml', method='jevtree', expected_raw_traversal='progressive')
        policy = raw_policy(cfg.agent, cfg.method)
        self.assertEqual(policy['max_searches'], 10)
        self.assertEqual(policy['initial_pages'], 4)
        self.assertTrue(policy['final_evidence_review'])
        self.assertEqual(policy['parents_per_action_limit'], 1)
        with self.assertRaisesRegex(ValueError, 'Expected raw traversal'):
            load_test('conf.yaml', method='jevtree', raw_traversal='best_first', expected_raw_traversal='progressive')
        with self.assertRaisesRegex(ValueError, 'Expected raw traversal'):
            load_test('conf.yaml', method='jevtree', raw_traversal='best_first')
        legacy = load_test('conf.yaml', method='jevtree', raw_traversal='best_first', expected_raw_traversal='best_first')
        self.assertEqual(legacy.agent.jev_traversal, 'best_first')

    def test_schema_requires_state_and_bounds_parents(self):
        for spec in raw_specs([]):
            params = spec['function']['parameters']
            self.assertIn('research', params['required'])
            if spec['function']['name']=='continue_search':
                self.assertEqual(params['properties']['source_ids']['maxItems'], 1)
        state = RawResearchState()
        with self.assertRaises(ValueError):
            state.validate_action_update(None)
        state.validate_action_update({'candidates': [], 'next_gap': 'identify the requested person'})

    def test_alternative_and_contradiction_survive_snapshot(self):
        state = RawResearchState()
        state.register('https://example.org/first')
        state.register('https://example.org/second')
        state.add_chunks('S1', 'a', {'0': 'The first candidate died before the subject was born.'})
        state.add_chunks('S2', 'b', {'0': 'The alternative was born in the stated place and served in the requested office.'})
        state.update({'candidates': [
            {'name': 'First', 'conditions': [{'condition': 'chronology', 'status': 'contradicted', 'evidence': ['S1:0']}]},
            {'name': 'Alternative', 'conditions': [{'condition': 'place and office', 'status': 'supported', 'evidence': ['S2:0']}]}],
            'next_gap': 'identify the person who worked for the alternative candidate'})
        restored = RawResearchState.from_snapshot(state.snapshot())
        self.assertIn('contradicted', restored.render())
        self.assertIn('Alternative', restored.render())
        self.assertIn('stated place', restored.render())


class AgentContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_all_ten_searches_are_available_before_finalization(self):
        replies = [call('web_search', {'query': f'unverified relation {i}', 'research': {
            'candidates': [], 'next_gap': f'condition {i}'}}) for i in range(10)]
        llm = FakeLLM(replies + [Reply(text='No supported answer was found.')])
        tools, queries = FakeTools(), []
        async def search(query):
            queries.append(query)
            return {'organic': []}, SimpleNamespace(is_error=False, duration_ms=1, text='{}')
        tools.search = search
        cfg = config(jev_traversal='progressive', max_searches=10, max_turns=24, jev_target_visits=1)
        with patch('searchgym.agent.LLM', return_value=llm), patch('searchgym.rawtree.LocalDecision', return_value=GraphDecision({})):
            agent = SearchAgent(profile_for('gpt-oss'), cfg, method='jevtree')
        result = await agent.run('Question', 'Research', tools, Capture())
        self.assertEqual(len(queries), 10)
        self.assertEqual(result.searches, 10)
        self.assertEqual(result.invalid_tool_calls, 0)
        self.assertEqual(result.answer, 'No supported answer was found.')
        self.assertFalse(llm.requests[-1][1])

    async def test_missing_state_is_visible_and_does_not_spend_search_budget(self):
        llm = FakeLLM([call('web_search', {'query': 'missing state'}),
            call('web_search', {'query': 'corrected request', 'research': {
                'candidates': [], 'next_gap': 'find the requested source'}}),
            Reply(text='Draft'), Reply(text='Evidence insufficient.')])
        tools, trace = FakeTools(), Capture()
        async def search(query):
            return {'organic': []}, SimpleNamespace(is_error=False, duration_ms=1, text='{}')
        tools.search = search
        cfg = config(jev_traversal='progressive', max_searches=10)
        with patch('searchgym.agent.LLM', return_value=llm), patch('searchgym.rawtree.LocalDecision', return_value=GraphDecision({})):
            agent = SearchAgent(profile_for('gpt-oss'), cfg, method='jevtree')
        result = await agent.run('Question', 'Research', tools, trace)
        self.assertEqual(result.searches, 1)
        self.assertEqual(result.invalid_tool_calls, 1)
        self.assertEqual(result.answer, 'Evidence insufficient.')
        self.assertIn('No search or fetch was performed', str(llm.requests[1]))
