"""Offline behavior tests for bounded, resumable reading and grounded state."""
import asyncio
import copy
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from searchgym.agent import SearchAgent
from searchgym.explorer import Document
from searchgym.llm import Reply
from searchgym.raw_progressive import ProgressiveRawTree
from searchgym.raw_research import RawResearchState
from searchgym.research_state import ResearchState
from searchgym.serving import profile_for
from test_rawtree import Capture
from test_rawtree_policy import GraphDecision, config, BASE
from test_depthsearch_core import call
from test_reader_integrity import FakeLLM
from offline import FakeTools


class ProgressiveTests(unittest.IsolatedAsyncioTestCase):
    async def setup_tree(self, graph=None, **changes):
        graph = graph or {'a': [('child', .9), ('other', .8)], 'child': [('deep', .9)]}
        cfg = config(jev_traversal='progressive', jev_direct_reads=1, jev_query_reads=1,
                     **changes)
        decision = GraphDecision(graph)
        fetched, trace, state = [], Capture(), RawResearchState()

        async def fetch(url, *, engine):
            self.assertEqual(engine, 'browser')
            fetched.append(url)
            name = url.removeprefix(BASE)
            return Document(url, f'# Title {name}\n\nFACT_{name}\n\n' + '\n'.join(
                f'[{dest}]({BASE}{dest})' for dest, _ in graph.get(name, [])), title=f'Title {name}')

        tree = ProgressiveRawTree(decision, cfg, fetch, state)
        log, text, stats = await tree.run_search('first goal', [{'link': BASE+'a'}, {'link': BASE+'b'}],
            question='original question with constraints', trace=trace, usage=None)
        return tree, decision, fetched, trace, state, log, text, stats

    async def test_initial_read_precedes_any_link_evaluation_then_continuation_is_bounded(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree()
        self.assertEqual(fetched, [BASE+'a', BASE+'b'])
        self.assertIn('FACT_a', text)
        self.assertIn('Source ID: S1', text)
        self.assertIn('Title: Title a', text)
        self.assertFalse(any(c['phase']=='link' for _, _, c in decision.contexts))
        self.assertEqual(stats['links_scored'], 0)
        self.assertTrue(state.evidence)
        _, text, stats = await tree.continue_search(log['search_id'], 'first goal', ['S1'], trace=trace)
        self.assertEqual(stats['page_visits'], 2)
        self.assertEqual(fetched[2:], [BASE+'child', BASE+'other'])
        self.assertNotIn(BASE+'deep', fetched)
        self.assertIn('FACT_child', text)

    async def test_full_budget_never_scores_outgoing_links(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree(jev_fetch_budget=2)
        before = len(decision.contexts)
        _, _, stats = await tree.continue_search(log['search_id'], 'first goal', ['S1'], trace=trace)
        self.assertEqual(len(decision.contexts), before)
        self.assertEqual(stats['page_visits'], 0)
        self.assertFalse(tree.can_continue(tree.sessions[log['search_id']]))

    async def test_reread_other_goal_reuses_body_and_chunks_without_polluting_frontier_goal(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree()
        before = len(decision.contexts)
        _, text, stats = await tree.read_source('S1', 'publication date', trace=trace)
        self.assertEqual(len(fetched), 2)
        self.assertEqual(stats['chunk_cache_hits'], 1)
        self.assertEqual(stats['page_visits'], 0)
        self.assertEqual(tree.sessions[log['search_id']].goal, 'first goal')
        self.assertTrue(any('publication date' in str(q) for _, q, _ in decision.contexts[before:]))
        before = len(decision.contexts)
        await tree.read_source('S1', 'publication date', trace=trace)
        self.assertEqual(len(decision.contexts), before)

    async def test_goal_change_discards_old_pending_ranking(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree(jev_expand_batch=1)
        await tree.continue_search(log['search_id'], 'first goal', ['S1'], trace=trace)
        session = tree.sessions[log['search_id']]
        self.assertTrue(session.pending)
        tree._set_goal(session, 'new missing condition')
        self.assertFalse(session.pending)
        self.assertFalse(session.rows)
        self.assertFalse(session.expanded)
        self.assertEqual(session.goal_version, 2)

    async def test_same_source_in_two_sessions_remains_valid_parent_in_both(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree()
        await tree.run_search('other search', [{'link': BASE+'a'}], question='original question with constraints',
                              trace=trace, usage=None)
        await tree.continue_search(log['search_id'], 'first goal', ['S1'], trace=trace)
        self.assertIn(BASE+'child', fetched)
        self.assertEqual(fetched.count(BASE+'a'), 1)

    async def test_repeated_search_returns_new_metadata_without_duplicate_excerpts(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree()
        _, text, stats = await tree.run_search('another goal', [{'link': BASE+'a'}],
            question='original question with constraints', trace=trace, usage=None)
        self.assertNotIn('FACT_a', text)
        self.assertIn('No new source excerpts', text)
        self.assertEqual(stats['chunks_returned'], 0)
        _, text, stats = await tree.read_source('S1', 'another goal', trace=trace)
        self.assertIn('FACT_a', text)

    async def test_output_budget_includes_navigation_metadata(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree(jev_output_tokens=500)
        self.assertLessEqual(decision.chunker.count(text), 500)

    async def test_unobserved_source_is_rejected_without_network(self):
        tree, decision, fetched, trace, state, log, text, stats = await self.setup_tree()
        before = list(fetched)
        with self.assertRaises(ValueError):
            await tree.read_source('S999', 'guess', trace=trace)
        self.assertEqual(fetched, before)

    async def test_cancelled_initial_fetch_does_not_leave_background_jobs(self):
        cfg = config(jev_traversal='progressive')
        started, active = asyncio.Event(), set()
        async def fetch(url, *, engine):
            active.add(url)
            started.set()
            try:
                await asyncio.Event().wait()
            finally:
                active.remove(url)
        tree = ProgressiveRawTree(GraphDecision({}), cfg, fetch, RawResearchState())
        job = asyncio.create_task(tree.run_search('q', [{'link': BASE+'a'}, {'link': BASE+'b'}],
                                 question='question', trace=Capture(), usage=None))
        await asyncio.wait_for(started.wait(), 3)
        job.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await job
        self.assertFalse(active)


class StateTests(unittest.TestCase):
    def test_contradiction_survives_invalid_update_and_can_be_revised_with_evidence(self):
        state = RawResearchState()
        sid = state.register(BASE+'a')
        state.add_chunks(sid, 'hash', {'0': 'First book: 1981', '1': 'Correction: first book 1972'})
        def update(status, refs):
            state.update({'candidates': [{'name': 'Candidate', 'conditions': [
                {'condition': 'first book 1971-1974', 'status': status, 'evidence': refs}]}]})
        update('contradicted', ['S1:0'])
        update('supported', ['S999:0'])
        self.assertEqual(state.candidates['Candidate']['conditions']['first book 1971-1974']['status'], 'contradicted')
        update('supported', ['S1:1'])
        self.assertEqual(state.candidates['Candidate']['conditions']['first book 1971-1974']['status'], 'supported')
        restored = ResearchState.from_snapshot(json.loads(json.dumps(state.snapshot())))
        self.assertEqual(restored.render(), state.render())


class AgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_search_reread_state_final_review_and_exhausted_search_tool(self):
        decision = GraphDecision({})
        cfg = config(jev_traversal='progressive', jev_direct_reads=1, jev_query_reads=0,
                     jev_entries=1, max_searches=1)
        update = {'candidates': [{'name': 'Author', 'conditions': [
            {'condition': 'first book', 'status': 'supported', 'evidence': ['S1:0']}]}]}
        llm = FakeLLM([call('web_search', {'query': 'author first book'}),
            call('read_source', {'source_id': 'S1', 'goal': 'verify publication date', 'research': update}),
            Reply(text='Unreviewed answer'), Reply(text='Supported final answer')])
        tools = FakeTools()
        async def search(query):
            payload = {'organic': [{'link': BASE+'a', 'title': 'Author record'}]}
            return payload, SimpleNamespace(is_error=False, duration_ms=1, text=json.dumps(payload))
        async def fetch(url, *, engine):
            tools.fetched.append(url)
            return Document(url, '# Author record\n\nFirst book: Baby, 1972.', title='Author record')
        tools.search, tools.fetch = search, fetch
        with patch('searchgym.agent.LLM', return_value=llm), patch('searchgym.rawtree.LocalDecision', return_value=decision):
            agent = SearchAgent(profile_for('gpt-oss'), cfg, method='jevtree')
        result = await agent.run('Find the original book title.', 'Research.', tools, Capture())
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, 'Supported final answer')
        self.assertEqual(result.searches, 1)
        self.assertEqual(len(tools.fetched), 1)
        self.assertEqual(len(llm.requests), 4)
        self.assertNotIn('web_search', [s['function']['name'] for s in llm.requests[1][1]])
        self.assertIn('read_source', [s['function']['name'] for s in llm.requests[1][1]])
        final_messages, final_tools = llm.requests[-1]
        self.assertFalse(final_tools)
        self.assertIn('First book: Baby, 1972', str(final_messages))
        self.assertIn('supported', str(final_messages))
        self.assertNotIn('Unreviewed answer', str(final_messages))
        self.assertFalse(any(c['phase']=='link' for _, _, c in decision.contexts))
