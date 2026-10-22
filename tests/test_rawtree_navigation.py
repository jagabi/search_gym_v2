"""Offline navigation regressions; source selection belongs exclusively to d3."""
import unittest
import json
from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import patch

from searchgym.config import load_test, _validate
from searchgym.explorer import Document
from searchgym.jevtree import JevUsage, TreeNode
from searchgym.raw_chunks import Chunk
from searchgym.raw_navigation import partitions, region_preview
from searchgym.raw_policy import raw_policy
from searchgym.rawtree import LocalDecisionError, RawTree, decision_question
from searchgym.runner import _agent_fingerprint
from test_rawtree import Capture, chunker
from test_rawtree_policy import BASE, config


class Decision:
    def __init__(self, score=None, return_score=None):
        self.return_score = return_score
        self.chunker = chunker(64)
        self.calls = []
        self.score = score or (lambda state, key, ctx: .8)

    async def prepare(self):
        pass

    async def noul(self, state, questions, trace, *, usage, context):
        self.calls.append((state, questions, context))
        usage.calls += 1
        results = {}
        for key in questions:
            if key == 'return_now':
                results[key] = self.return_score(state, context) if self.return_score else 0.0
                continue
            if context.get('phase') == 'region' and key.startswith('region_'):
                region, objective = key.split('__', 1)
                i = int(region.removeprefix('region_'))
                start, stop = context['region_spans'][i]
                text = state['page_text'].split(region + ' / bundles ', 1)[1]
                text = text.split('\n\nregion_', 1)[0]
                results[key] = self.score({**state, 'page_text': text}, objective,
                                         {**context, 'bundle_start': start, 'bundle_stop': stop})
            else:
                results[key] = self.score(state, key, context)
        return results


class NavigationTests(unittest.IsolatedAsyncioTestCase):
    async def test_live_agent_contract_with_default_config_requires_only_search_queries(self):
        from searchgym.agent import SearchAgent
        from searchgym.llm import Reply
        from searchgym.serving import profile_for
        from test_depthsearch_core import call
        from test_reader_integrity import FakeLLM
        from offline import FakeTools

        cfg = load_test(method='jevtree').agent
        llm = FakeLLM([call('web_search', {'query': f'missing fact {i}'}) for i in range(10)]
                      + [Reply(text='Evidence remains insufficient.')])
        tools, queries = FakeTools(), []

        async def search(query):
            queries.append(query)
            return {'organic': []}, SimpleNamespace(is_error=False, duration_ms=1, text='{}')

        tools.search = search
        with patch('searchgym.agent.LLM', return_value=llm), \
                patch('searchgym.rawtree.LocalDecision', return_value=Decision()):
            agent = SearchAgent(profile_for('gpt-oss'), cfg, method='jevtree')
        result = await agent.run('Question', 'Research using source evidence.', tools, Capture())
        self.assertEqual(result.searches, 10)
        self.assertEqual(result.invalid_tool_calls, 0)
        self.assertEqual(len(queries), 10)
        for _, specs in llm.requests[:10]:
            self.assertEqual([s['function']['name'] for s in specs], ['web_search'])
            self.assertNotIn('research', specs[0]['function']['parameters']['properties'])
        self.assertTrue(all(s['function']['name'] == 'web_search'
                            for s in (llm.requests[-1][1] or [])))
        self.assertIsNone(result.research_state)

    async def run_search(self, results, bodies, *, score=None, **options):
        # These source/chunk-selection regressions also cover the retained
        # traversal-then-read mode. Node action scheduling has its own tests.
        options.setdefault('jev_traversal', 'best_first')
        cfg = config(**options)
        decision, trace, fetched = Decision(score), Capture(), []

        async def fetch(url, *, engine):
            self.assertEqual(engine, 'browser')
            fetched.append(url)
            body = bodies.get(url, 'Ordinary source facts.')
            return Document(url, body if body is not None else 'HTTP 422 unavailable',
                            is_error=body is None)

        tree = RawTree(decision, cfg, fetch)
        result = await tree.run_search('missing relation', results, question='original question',
                                       trace=trace, usage=None)
        return tree, decision, trace, fetched, result

    async def test_d3_can_admit_rank_seven_with_search_lead_in_preview(self):
        results = [{'link': BASE+str(i), 'title': f'Record {i}', 'snippet': f'Source clue {i}'}
                   for i in range(1, 11)]

        def score(state, key, ctx):
            return .99 if state['page_url'] == BASE+'7' else .1

        _, decision, _, fetched, (_, _, stats) = await self.run_search(
            results, {}, score=score, jev_entries=6, jev_fetch_budget=10,
            jev_rank_entries=True, jev_entry_candidates=10)
        self.assertIn(BASE+'7', fetched)
        self.assertEqual(len(fetched), 6)
        self.assertEqual(stats['entries'], 6)
        entries = [s for s, _, c in decision.calls if c['phase'] == 'entry']
        self.assertEqual(len(entries), 10)
        self.assertTrue(all(len(s['search_results']) == 10 for s in entries))
        preview = next(s for s, _, c in decision.calls
                       if c['phase'] == 'preview' and s['page_url'] == BASE+'7')
        self.assertEqual(preview['search_lead']['snippet'], 'Source clue 7')

    async def test_unknown_entry_score_falls_back_to_search_order(self):
        def score(state, key, ctx):
            if ctx['phase'] == 'entry' and state['page_url'] == BASE+'a':
                raise LocalDecisionError('unavailable')
            return .99

        _, _, trace, fetched, (_, _, stats) = await self.run_search(
            [{'link': BASE+x} for x in 'abc'], {}, score=score,
            jev_rank_entries=True, jev_entries=2)
        self.assertEqual(fetched, [BASE+'a', BASE+'b'])
        self.assertEqual(stats['entry_eval_failures'], 1)
        self.assertTrue(next(e for e in trace.events if e['event'] == 'rawtree.entries')['fallback'])

    async def test_beam_downloads_all_ten_before_any_entry_judgment(self):
        def score(state, key, ctx):
            self.assertNotIn(ctx['phase'], ('entry', 'entry_diversity'))
            return .01
        results = [{'link': BASE+str(i), 'title': f'Search {i}', 'snippet': f'Clue {i}'}
                   for i in range(1, 11)]
        _, decision, trace, fetched, (_, _, stats) = await self.run_search(
            results, {}, score=score, jev_traversal='beam', jev_entries=10,
            jev_fetch_budget=14, jev_rank_entries=True, jev_frontier_width=2)
        self.assertEqual(fetched, [BASE+str(i) for i in range(1, 11)])
        self.assertEqual(stats['entries'], 10)
        previews = [(s,q) for s,q,c in decision.calls if c['phase']=='preview']
        self.assertEqual(len(previews), 10)
        self.assertTrue(all(set(q)=={'inspect_value'} for _,q in previews))
        self.assertEqual(previews[6][0]['page_title'], 'Search 7')
        self.assertEqual(previews[6][0]['search_snippet'], 'Clue 7')
        self.assertFalse(any(e['event']=='rawtree.entry_diversity' for e in trace.events))

    async def test_entry_metadata_is_complete_inside_total_preview_budget(self):
        title = ' '.join(f'title{i}' for i in range(150))
        snippet = ' '.join(f'snippet{i}' for i in range(240))
        body = ' '.join(f'source{i}' for i in range(6000))
        _, decision, _, _, _ = await self.run_search(
            [{'link': BASE+'root', 'title': title, 'snippet': snippet}], {BASE+'root': body},
            score=lambda *args:.01, jev_traversal='beam', jev_entries=10,
            jev_fetch_budget=14, jev_page_tokens=4096)
        state = next(s for s,_,c in decision.calls if c['phase']=='preview')
        self.assertEqual(state['page_title'], title)
        self.assertEqual(state['search_snippet'], snippet)
        self.assertTrue(body.startswith(state['page_text']))
        self.assertNotIn('source5999', state['page_text'])
        self.assertLessEqual(decision.chunker.count(json.dumps(state,ensure_ascii=False)),4096)

    async def test_complementary_read_beats_second_copy_of_known_entity(self):
        def score(state, key, ctx):
            name = state['page_url'].removeprefix(BASE)
            if ctx['phase'] == 'read_selection':
                self.assertEqual(state['selected_sources'][0]['url'], BASE+'known')
                return .01 if name == 'similar' else .95
            if ctx['phase'] == 'preview':
                return {'known': .99, 'similar': .9, 'roles': .4}[name]
            return .9

        _, _, trace, _, (_, text, stats) = await self.run_search(
            [{'link': BASE+x} for x in ('known', 'similar', 'roles')],
            {BASE+'roles': 'Performer Mira played the archivist.'}, score=score,
            jev_entries=3, jev_reads=2, jev_direct_reads=1, jev_query_reads=1,
            jev_diverse_reads=True, jev_frontier_width=2)
        pages = next(e['pages'] for e in trace.events if e['event'] == 'rawtree.pages_selected')
        self.assertEqual([p['id'] for p in pages], ['n0', 'n2'])
        self.assertIn('Performer Mira played the archivist.', text)
        self.assertEqual(stats['reads'], 2)

    async def test_read_selection_retains_relation_after_navigation_heavy_opening(self):
        # Both the candidate list and selected source carry identifying facts
        # beyond 600 tokens. Titles/snippets deliberately provide no shortcut.
        opening = 'Site navigation entry. ' * 300
        bodies = {
            BASE+'known': opening + '\n\nAster held the office in 1910.',
            BASE+'registry': opening + '\n\n| Candidate | Birthplace |\n|---|---|\n'
                             '| Aster | Northport |\n| Rowan | Northport |\n',
            BASE+'other': 'Beryl held an unrelated office in Southport.',
        }

        def score(state, key, ctx):
            name = state['page_url'].removeprefix(BASE)
            if ctx['phase'] == 'read_selection':
                self.assertIn('Aster held the office in 1910.',
                              state['selected_sources'][0]['source_preview'])
                preview = state['candidate']['source_preview']
                return .95 if '| Rowan | Northport |' in preview else .05
            if ctx['phase'] == 'preview':
                return {'known': .99, 'registry': .4, 'other': .8}[name]
            if ctx['phase'] == 'bundle':
                return .99 if any(t in state['page_text'] for t in
                                  ('Aster held the office', '| Rowan | Northport |')) else .01
            return .9

        tree, decision, trace, _, (_, _, stats) = await self.run_search(
            [{'link': BASE+x, 'title': 'Source record', 'snippet': ''}
             for x in ('known', 'registry', 'other')], bodies, score=score,
            jev_entries=3, jev_reads=2, jev_direct_reads=1, jev_query_reads=1,
            jev_page_tokens=2000, jev_diverse_reads=True, jev_frontier_width=2)
        self.assertNotIn('Rowan', tree.jev.chunker.prefix(bodies[BASE+'registry'], 600))
        pages = next(e['pages'] for e in trace.events if e['event'] == 'rawtree.pages_selected')
        self.assertEqual([r['id'] for r in pages], ['n0', 'n1'])
        self.assertEqual(stats['reads'], 2)
        self.assertEqual(len([e for e in trace.events if e['event'] == 'rawtree.chunks']), 2)
        self.assertTrue(all(c['coverage'].startswith('Selected original')
                            for s, _, ctx in decision.calls if ctx['phase'] == 'read_selection'
                            for c in s['selected_sources']))
        cards = [s['candidate'] for s, _, ctx in decision.calls if ctx['phase'] == 'read_selection']
        self.assertTrue(all(tree.jev.chunker.count(c['source_preview']) <= 2000 for c in cards))
        self.assertTrue(all('reasoning' not in s and 'main_reasoning' not in s
                            for s, _, _ in decision.calls))

    async def test_weak_relevance_is_not_overridden_by_novelty_alone(self):
        def score(state, key, ctx):
            name = state['page_url'].removeprefix(BASE)
            if ctx['phase'] == 'read_selection':
                return {'alternative': .9, 'introduction': .4}[name]
            if ctx['phase'] == 'preview':
                return {'known': .99, 'alternative': .25, 'introduction': .9}[name]
            return .9

        _, _, trace, _, (_, _, stats) = await self.run_search(
            [{'link': BASE+x} for x in ('known', 'alternative', 'introduction')],
            {BASE+'known': 'Aster is one candidate.',
             BASE+'alternative': 'Rowan satisfies the missing birthplace relation.',
             BASE+'introduction': 'Another introduction to Aster.'}, score=score,
            jev_entries=3, jev_reads=2, jev_direct_reads=1, jev_query_reads=1,
            jev_diverse_reads=True)
        pages = next(e['pages'] for e in trace.events if e['event'] == 'rawtree.pages_selected')
        self.assertEqual([r['id'] for r in pages], ['n0', 'n2'])
        self.assertEqual(stats['reads'], 2)

    async def test_identical_body_dedup_backfills_distinct_source(self):
        _, _, trace, _, (_, text, stats) = await self.run_search(
            [{'link': BASE+x} for x in 'abc'],
            {BASE+'a': 'Identical article.', BASE+'b': 'Identical article.',
             BASE+'c': 'Additional original record.'},
            jev_entries=3, jev_reads=2, jev_direct_reads=1, jev_query_reads=1,
            jev_read_dedup=True)
        pages = next(e['pages'] for e in trace.events if e['event'] == 'rawtree.pages_selected')
        self.assertEqual([p['id'] for p in pages], ['n0', 'n2'])
        self.assertEqual(stats['duplicate_reads_avoided'], 1)
        self.assertEqual(stats['reads'], 2)
        self.assertIn('Additional original record.', text)

    async def test_satisfied_page_does_not_launch_link_judgments(self):
        def score(state, key, ctx):
            if key == 'return_now':
                return .99
            if key.startswith('link_'):
                return .05
            return .9

        _, decision, trace, fetched, (_, _, stats) = await self.run_search(
            [{'link': BASE+'record'}],
            {BASE+'record': 'The requested relation is stated here. [Menu](https://example.org/menu)'},
            score=score, jev_entries=1, jev_depth=2, jev_traversal='beam', jev_link_floor=.1)
        self.assertEqual(fetched, [BASE+'record'])
        self.assertFalse(any(ctx['phase'] == 'links' for _, _, ctx in decision.calls))
        self.assertEqual(stats['links_scored'], 1)
        self.assertEqual(stats['links_pruned'], 1)

    async def test_parent_beam_narrows_before_per_link_work(self):
        roots = ['a', 'b', 'c', 'd', 'e', 'f']

        def score(state, key, ctx):
            if key == 'inspect_value':
                return .99 if 'Record a.' in state['page_text'] else .9 if 'Record b.' in state['page_text'] else .1
            return .9 if key.startswith('link_') else .001

        _, decision, decision_trace, fetched, (_, _, stats) = await self.run_search(
            [{'link': BASE+x} for x in roots],
            {BASE+x: f'Record {x}. [Detail]({BASE}{x}1)' for x in roots},
            score=score, jev_entries=6, jev_fetch_budget=8, jev_frontier_width=2, jev_depth=2,
            jev_traversal='beam')
        self.assertEqual(fetched[:6], [BASE+x for x in roots])
        self.assertEqual(set(fetched[6:]), {BASE+'a1', BASE+'b1'})
        self.assertEqual(len([q for _, q, ctx in decision.calls if ctx['phase'] == 'bundle'
                              and any(k.startswith('link_') for k in q)]), 2)
        self.assertEqual(stats['links_scored'], 2)
        selection = next(e for e in decision_trace.events if e['event']=='rawtree.inspection_selection')
        self.assertEqual(len(selection['selected']), 2)

    async def test_failed_source_keeps_exact_title_and_url_as_unverified_lead(self):
        tree, _, _, _, (_, text, stats) = await self.run_search(
            [{'link': BASE+'paper', 'title': 'Regional Atlas by R. Chen',
              'snippet': 'Funding and acknowledgements in Appendix B'}],
            {BASE+'paper': None}, jev_notice_tokens=600)
        for value in ('Regional Atlas by R. Chen', BASE+'paper', 'access_failed',
                      'unverified navigation', 'Appendix B', 'web_search'):
            self.assertIn(value, text)
        self.assertNotIn('read_source', text)
        self.assertEqual(stats['fetch_failed'], 1)
        self.assertLessEqual(tree.jev.chunker.count(text), tree.cfg.jev_output_tokens)

    async def test_exact_judgment_reuse_invalidates_on_query_and_source_changes(self):
        decision = Decision()
        tree = RawTree(decision, config(jev_read_dedup=True), None)
        meter, trace = JevUsage(), Capture()
        state = {'page_url': BASE+'a', 'page_text': 'Original fact'}
        questions = {'query_answer': decision_question('query A', query=True)}
        for current_state, current_questions in (
            (state, questions), (dict(state), dict(questions)),
            (state, {'query_answer': decision_question('query B', query=True)}),
            ({**state, 'page_text': 'Revised source fact'}, questions),
        ):
            await tree._noul(current_state, current_questions, trace, usage=meter, context={})
        self.assertEqual(len(decision.calls), 3)
        self.assertEqual(tree.score_cache_hits, 1)

    async def test_partial_judgments_are_not_cached(self):
        class Partial(Decision):
            async def noul(self, *args, **kwargs):
                self.calls.append(None)
                return {'direct_answer': .7}

        decision = Partial()
        tree = RawTree(decision, config(jev_read_dedup=True), None)
        for _ in range(2):
            await tree._noul({}, {'direct_answer': {}, 'query_answer': {}}, Capture(),
                             usage=JevUsage(), context={})
        self.assertEqual(len(decision.calls), 2)
        self.assertFalse(tree.score_cache)

    async def test_document_beam_preserves_two_goals_and_bounds_leaf_work(self):
        chunks = [Chunk(i, f'Original source passage {i}.', 5, []) for i in range(256)]
        chunks[0].headings = ['TARGET_A original record']
        chunks[-1].headings = ['TARGET_B final appendix']
        chunks[0].text = 'TARGET_A original record\n' + chunks[0].text
        chunks[-1].text = 'TARGET_B final appendix\n' + chunks[-1].text
        bundles = [{'id': i, 'chunk_ids': [i], 'text': c.text} for i, c in enumerate(chunks)]

        def score(state, key, ctx):
            marker = 'TARGET_A' if key == 'direct_answer' else 'TARGET_B'
            return .99 if marker in state['page_text'] else .01

        cfg = config(jev_document_tree=True, jev_region_tokens=600, jev_bundle_tokens=4096)
        decision, trace, stats = Decision(score), Capture(), {}
        tree = RawTree(decision, cfg, None)

        async def evaluate(coro, *args):
            return await coro

        selected = await tree._document_regions(TreeNode(url=BASE+'collection', depth=1),
            chunks, bundles, 'original', 'query', 'search', trace, JevUsage(), stats, evaluate)
        self.assertEqual(len(selected), 4)
        self.assertTrue({0, 255}.issubset({b['id'] for b in selected}))
        self.assertEqual(stats['region_evaluations'], 24)
        self.assertEqual(stats['region_cards'], 5)
        self.assertEqual(stats.get('bundles_scored', 0), 0)
        events = [e for e in trace.events if e['event'] == 'rawtree.regions']
        self.assertTrue(all(len(e['selected']) <= 2 for e in events[:-1]))
        self.assertTrue(all(decision.chunker.count(json.dumps(s, ensure_ascii=False)) <= cfg.jev_bundle_tokens
                            for s, _, _ in decision.calls))

    async def test_failed_region_retains_an_uncertain_route(self):
        chunks = [Chunk(i, f'Passage {i}', 2, []) for i in range(32)]
        bundles = [{'id': i, 'chunk_ids': [i], 'text': c.text} for i, c in enumerate(chunks)]

        class PartialRegion(Decision):
            async def noul(self, state, questions, trace, *, usage, context):
                result = await super().noul(state, questions, trace, usage=usage, context=context)
                if context['phase'] == 'region':
                    i = len(context['region_spans'])-1
                    result.pop(f'region_{i}__query_answer')
                return result
        decision, trace = PartialRegion(lambda state, key, ctx:
            .99 if ctx['phase'] == 'bundle' and ctx['bundle_id'] == 31 else .5), Capture()
        tree = RawTree(decision, config(jev_document_tree=True, jev_bundle_tokens=4096), None)

        async def evaluate(coro, *args):
            try:
                return await coro
            except LocalDecisionError:
                return {}

        selected = await tree._document_regions(TreeNode(url=BASE+'doc', depth=1), chunks,
            bundles, 'original', 'query', 'search', trace, JevUsage(), {}, evaluate)
        self.assertIn(31, [b['id'] for b in selected])
        self.assertLessEqual(len(selected), 4)
        root = next(e for e in trace.events if e['event'] == 'rawtree.regions')
        self.assertIn((28, 32), root['selected'])

    async def test_long_document_reaches_tail_through_real_chunker_despite_low_prefix_score(self):
        body = '\n\n'.join(f'## Registry section {i}\n\n' + f'Record {i} ordinary facts. '*350
                           for i in range(100))
        body += '\n\n## TARGET_FINAL appendix\n\nTARGET_FINAL named Mira as the archivist.'

        def score(state, key, ctx):
            if ctx['phase'] == 'preview':
                self.assertNotIn('TARGET_FINAL', state['page_text'])
                return .001
            text = state.get('target_chunk', state.get('page_text', ''))
            return .99 if 'TARGET_FINAL' in text else .001

        _, _, trace, _, (_, text, stats) = await self.run_search(
            [{'link': BASE+'registry', 'title': 'Registry archive',
              'snippet': 'Mira, archivist, final appendix'}], {BASE+'registry': body}, score=score,
            jev_entries=1, jev_reads=1, jev_direct_reads=1, jev_query_reads=0,
            jev_page_tokens=64, jev_bundle_tokens=4096, jev_output_tokens=10000,
            jev_document_tree=True, jev_diverse_reads=True,
            jev_read_dedup=True, jev_notice_tokens=400)
        timing = next(e for e in trace.events if e['event'] == 'rawtree.chunk_timing')
        self.assertGreater(timing['bundle_count'], 16)
        self.assertLessEqual(stats['bundles_scored'], 16)
        self.assertGreater(stats['region_evaluations'], 0)
        self.assertIn('TARGET_FINAL named Mira as the archivist.', text)
        returned = next(e['returned'] for e in trace.events if e['event'] == 'rawtree.return')
        saved_chunks = next(e['chunks'] for e in trace.events if e['event'] == 'rawtree.chunks')
        self.assertTrue(all(t == saved_chunks[int(i)]['text']
                            for r in returned for i, t in r['texts'].items()))


class NavigationConfigTests(unittest.TestCase):
    def test_default_retains_search_only_contract_and_wave_four(self):
        cfg = load_test(method='jevtree')
        policy = raw_policy(cfg.agent, cfg.method)
        self.assertEqual(policy['tools'], ['web_search'])
        self.assertFalse(policy['research_state'])
        self.assertEqual(policy['traversal'], 'beam')
        self.assertEqual(policy['max_searches'], 10)
        self.assertEqual(policy['http_wave'], {'requests': 4, 'questions_per_request': 64,
                                             'question_budget': 256, 'wait_for_all': True})
        self.assertEqual(policy['entry_candidates'], 10)
        self.assertEqual(policy['initial_pages'], 10)
        self.assertEqual(policy['visits_per_search_limit'], 14)
        self.assertEqual(policy['entry_selection'], 'fetch_all_then_source_prefix')
        self.assertEqual(policy['entry_complement_slots'], 0)
        self.assertEqual(policy['document_routing']['leaf_bundles'], 4)
        self.assertEqual(policy['document_routing']['selector'], 'd3')
        self.assertFalse(policy['complementary_reads'])
        self.assertEqual(policy['branch_control']['selection'], 'single_inspect_value')

    def test_navigation_parameters_validate_and_change_run_fingerprint(self):
        cfg = load_test(method='jevtree')
        original = cfg.agent
        for field, bad in (('jev_region_branch', 1), ('jev_region_beam', 0),
                           ('jev_leaf_bundles', 0), ('jev_region_tokens', 0),
                           ('jev_entry_candidates', 0), ('jev_notice_tokens', -1)):
            cfg.agent = replace(original, **{field: bad})
            with self.subTest(field=field), self.assertRaises(ValueError):
                _validate(cfg)
        for change in ({'jev_document_tree': False}, {'jev_rank_entries': True},
                       {'jev_region_beam': 3}, {'jev_read_dedup': False}):
            self.assertNotEqual(_agent_fingerprint(original),
                                _agent_fingerprint(replace(original, **change)))

    def test_balanced_partitions_and_bounded_source_preview_include_tail(self):
        spans = partitions(0, 29, 4)
        self.assertEqual([i for a, b in spans for i in range(a, b)], list(range(29)))
        self.assertLessEqual(max(b-a for a, b in spans)-min(b-a for a, b in spans), 1)
        self.assertEqual(partitions(0, 0, 4), [])
        c = chunker(64)
        chunks = c.chunks('# Introduction\n\n' + 'Ordinary text. '*100 +
                          '\n\n## Final registry\n\nLAST_SOURCE_RECORD')
        bundles = c.bundles(chunks, 160, 2)
        preview = region_preview(chunks, bundles, 0, len(bundles), c, 600)
        self.assertIn('Final registry', preview)
        self.assertIn('LAST_SOURCE_RECORD', preview)
        self.assertLessEqual(c.count(preview), 600)


if __name__ == '__main__':
    unittest.main()
