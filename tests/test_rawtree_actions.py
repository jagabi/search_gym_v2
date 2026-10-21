"""Server-side regressions for depth barriers and local d3 branch actions."""
import asyncio
import unittest

from searchgym.explorer import Document
from searchgym.rawtree import RawTree
from test_rawtree import Capture
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config


class BranchActionTests(unittest.IsolatedAsyncioTestCase):
    async def run_graph(self, graph, roots, score, **options):
        values = dict(jev_traversal='beam', jev_entries=len(roots), jev_reads=2,
                      jev_direct_reads=1, jev_query_reads=1, jev_depth=3,
                      jev_fetch_budget=10, jev_frontier_width=2,
                      jev_read_dedup=True)
        values.update(options)
        decision, trace, fetched = Decision(score), Capture(), []

        async def fetch(url, *, engine):
            name = url.removeprefix(BASE)
            # One sibling finishes later; no child or read may bypass it.
            if name == 'b':
                await asyncio.sleep(.01)
            fetched.append(name)
            trace.event('test.fetch_complete', name=name)
            body = f'VERIFIED_{name} original source record.\n\n'
            body += '\n'.join(f'[Record]({BASE}{child})' for child in graph.get(name, []))
            return Document(url, body)

        tree = RawTree(decision, config(**values), fetch)
        output = await tree.run_search('missing relation', [{'link': BASE+n} for n in roots],
                                       question='original question', trace=trace, usage=None,
                                       main_reasoning='PRIVATE_REASONING_MUST_NOT_BE_FORWARDED')
        self.assertTrue(all('PRIVATE_REASONING' not in str(state)
                            for state, _, _ in decision.calls))
        return decision, trace, fetched, output

    async def test_read_then_return_stops_before_links_without_filling_second_slot(self):
        def score(state, key, ctx):
            if key in ('direct_answer', 'query_answer') or ctx['phase'] in ('bundle', 'chunk'):
                return .9
            observed = bool(state.get('selected_sources'))
            return {'return_now': .99 if observed else .01,
                    'read_now': .95 if state['page_url'] == BASE+'a' else .2,
                    'expand_now': .8}[key]

        decision, trace, fetched, (_, text, stats) = await self.run_graph(
            {'a': ['a1'], 'b': ['b1']}, ['a', 'b'], score)
        self.assertEqual(fetched, ['a', 'b'])
        self.assertEqual(stats['reads'], 1)
        self.assertEqual(stats.get('zero_read_selections', 0), 0)
        self.assertIn('VERIFIED_a', text)
        self.assertFalse(any(ctx['phase'] == 'links' for _, _, ctx in decision.calls))
        events = trace.events
        chunk_at = next(i for i, e in enumerate(events) if e['event'] == 'rawtree.chunks')
        self.assertTrue(all(i < chunk_at for i, e in enumerate(events)
                            if e['event'] == 'test.fetch_complete'))
        previews = [i for i, e in enumerate(events) if e['event'] == 'rawtree.preview']
        self.assertEqual(len(previews), 2)
        self.assertTrue(all(i < chunk_at for i in previews))
        actions = [e for e in events if e['event'] == 'rawtree.node_action']
        self.assertEqual(sum(e['action'] == 'return_now' for e in actions), 2)
        self.assertTrue(any(s['selected_sources'][0]['evidence_available']
                            for s, _, c in decision.calls if c['phase'] == 'node_action'))

    async def test_multiple_local_returns_do_not_stop_expanding_sibling(self):
        def score(state, key, ctx):
            name = state['page_url'].removeprefix(BASE)
            if ctx['phase'] in ('bundle', 'chunk', 'links'):
                return .9
            if key in ('direct_answer', 'query_answer'):
                return .9 if name == 'b1' else .05
            if name in ('a', 'c') or state.get('selected_sources'):
                return .99 if key == 'return_now' else .01
            if name == 'b':
                return .99 if key == 'expand_now' else .01
            return .99 if key == 'read_now' else .01

        _, trace, fetched, (_, text, stats) = await self.run_graph(
            {'a': ['forbidden_a'], 'b': ['b1'], 'c': ['forbidden_c']}, ['a', 'b', 'c'], score)
        self.assertEqual(set(fetched[:3]), {'a', 'b', 'c'})
        self.assertEqual(fetched[3:], ['b1'])
        self.assertIn('VERIFIED_b1', text)
        self.assertEqual(stats['max_depth'], 2)
        closed_roots = [e for e in trace.events if e['event'] == 'rawtree.node_action'
                        and e['action'] == 'return_now' and e['depth'] == 1]
        self.assertEqual(len(closed_roots), 2)

    async def test_first_read_leaves_second_slot_for_depth_three(self):
        def score(state, key, ctx):
            name = state['page_url'].removeprefix(BASE)
            if ctx['phase'] in ('bundle', 'chunk', 'links'):
                return .9
            if key in ('direct_answer', 'query_answer'):
                return .1 if name in ('b', 'b1') else .9
            observed = state.get('selected_sources', [])
            if observed:
                self.assertIn('VERIFIED_a', observed[0]['source_preview'])
            if name == 'a':
                winner = 'return_now' if observed else 'read_now'
            elif name in ('b', 'b1'):
                winner = 'expand_now'
            else:
                winner = 'return_now' if state.get('document_already_read') else 'read_now'
            return .99 if key == winner else .01

        _, trace, fetched, (_, text, stats) = await self.run_graph(
            {'a': ['forbidden'], 'b': ['b1'], 'b1': ['b2']}, ['a', 'b'], score)
        self.assertEqual(fetched, ['a', 'b', 'b1', 'b2'])
        self.assertEqual((stats['reads'], stats['direct_reads'], stats['query_reads']), (2, 1, 1))
        self.assertEqual(stats['max_depth'], 3)
        self.assertIn('VERIFIED_a', text)
        self.assertIn('VERIFIED_b2', text)
        self.assertEqual(next(e for e in trace.events if e['event'] == 'rawtree.traversal_end')['reason'],
                         'read_budget')

    async def test_tied_actions_close_branch_without_threshold(self):
        _, trace, fetched, (_, _, stats) = await self.run_graph(
            {'a': ['child']}, ['a'], lambda state, key, ctx: .23)
        self.assertEqual(fetched, ['a'])
        self.assertEqual(stats['reads'], 1)
        self.assertEqual(stats['zero_read_selections'], 1)
        self.assertEqual(stats['branch_returns'], 1)
        self.assertFalse(any(e['event'] == 'rawtree.links' for e in trace.events))

    async def test_read_budget_prevents_opening_children_after_second_read(self):
        def score(state, key, ctx):
            if key in ('direct_answer', 'query_answer') or ctx['phase'] in ('bundle', 'chunk'):
                return .9
            return {'read_now': .99, 'expand_now': .8, 'return_now': .01}[key]

        decision, trace, fetched, (_, _, stats) = await self.run_graph(
            {'a': ['a1'], 'b': ['b1']}, ['a', 'b'], score)
        self.assertEqual(fetched, ['a', 'b'])
        self.assertEqual(stats['reads'], 2)
        self.assertFalse(any(c['phase'] == 'links' for _, _, c in decision.calls))
        self.assertEqual(next(e for e in trace.events if e['event'] == 'rawtree.traversal_end')['reason'],
                         'read_budget')

    async def test_partial_action_scores_are_unknown_not_a_successful_return(self):
        class Partial(Decision):
            async def noul(self, state, questions, trace, *, usage, context):
                return {key: .9 for key in questions if key != 'return_now'}

        async def fetch(url, **kwargs):
            return Document(url, 'Original record.')

        trace = Capture()
        tree = RawTree(Partial(), config(jev_traversal='beam', jev_entries=1,
            jev_reads=1, jev_direct_reads=1, jev_query_reads=0), fetch)
        _, _, stats = await tree.run_search('query', [{'link': BASE+'a'}],
                                            question='question', trace=trace, usage=None)
        actions = [e for e in trace.events if e['event'] == 'rawtree.node_action']
        self.assertEqual([e['action'] for e in actions], ['unavailable', 'read_now'])
        self.assertEqual(actions[-1]['reason'], 'zero_read_search')
        self.assertEqual(stats.get('branch_returns', 0), 0)
        self.assertEqual(stats['reads'], 1)
        self.assertEqual(stats['zero_read_selections'], 1)

    async def test_all_returns_read_best_source_once_without_reopening_branch(self):
        def score(state, key, ctx):
            if ctx['phase'] in ('bundle', 'chunk'):
                return .9
            if key in ('direct_answer', 'query_answer'):
                return .82 if state['page_url'] == BASE+'b' else .1
            return .99 if key == 'return_now' else .01

        decision, trace, fetched, (_, text, stats) = await self.run_graph(
            {'a': ['forbidden_a'], 'b': ['forbidden_b']}, ['a', 'b'], score)
        self.assertEqual(fetched, ['a', 'b'])
        self.assertEqual(stats['reads'], 1)
        self.assertEqual(stats['zero_read_selections'], 1)
        self.assertIn('VERIFIED_b', text)
        self.assertNotIn('VERIFIED_a', text)
        self.assertFalse(any(c['phase'] == 'links' for _, _, c in decision.calls))
        selected = next(e for e in trace.events if e['event'] == 'rawtree.read_selection')
        self.assertEqual(selected['selected'], 'n1')
        self.assertEqual(selected['reason'], 'zero_read_search')

    async def test_closed_source_can_win_read_requested_by_sibling(self):
        def score(state, key, ctx):
            if ctx['phase'] in ('bundle', 'chunk'):
                return .9
            name = state['page_url'].removeprefix(BASE)
            if key in ('direct_answer', 'query_answer'):
                return .9 if name == 'a' else .7
            if state.get('selected_sources') or name == 'a':
                return .99 if key == 'return_now' else .01
            return .01

        _, trace, fetched, (_, text, stats) = await self.run_graph(
            {'a': ['forbidden_a'], 'b': ['forbidden_b']}, ['a', 'b'], score)
        self.assertEqual(fetched, ['a', 'b'])
        self.assertEqual(stats['reads'], 1)
        self.assertEqual(stats.get('zero_read_selections', 0), 0)
        self.assertIn('VERIFIED_a', text)
        actions = [e for e in trace.events if e['event'] == 'rawtree.node_action']
        selected = next(e for e in actions if e['action'] == 'read_now')
        self.assertEqual(selected['node_id'], 'n0')
        self.assertEqual(selected['requested_by'], ['n1'])
        self.assertTrue(any(e['action'] == 'return_now' and e['node_id'] == 'n0' for e in actions))

    async def test_closed_source_marginal_score_refreshes_after_new_evidence(self):
        def score(state, key, ctx):
            if ctx['phase'] in ('bundle', 'chunk'):
                return .9
            name = state['page_url'].removeprefix(BASE)
            observed = bool(state.get('selected_sources'))
            if key in ('direct_answer', 'query_answer'):
                return ({'a': .98, 'b': .1, 'c': .8} if observed else
                        {'a': .98, 'b': .95, 'c': .9})[name]
            return .99 if key == 'return_now' and (name == 'b' or observed and name == 'a') else .01

        decision, _, _, (_, text, stats) = await self.run_graph({}, ['a', 'b', 'c'], score)
        self.assertEqual(stats['reads'], 2)
        self.assertIn('VERIFIED_a', text)
        self.assertIn('VERIFIED_c', text)
        self.assertNotIn('VERIFIED_b', text)
        refreshes = [s for s, _, c in decision.calls if c['phase'] == 'read_selection'
                     and s['page_url'] == BASE+'b']
        self.assertEqual(len(refreshes), 1)
        self.assertIn('VERIFIED_a', refreshes[0]['selected_sources'][0]['source_preview'])

    async def test_zero_read_policy_respects_explicit_zero_read_quota(self):
        _, _, _, (_, _, stats) = await self.run_graph({}, ['a'], lambda *args: .3,
            jev_reads=0, jev_direct_reads=0, jev_query_reads=0)
        self.assertEqual(stats['reads'], 0)
        self.assertEqual(stats.get('zero_read_selections', 0), 0)

    async def test_failed_fetch_does_not_trigger_minimum_read(self):
        async def fetch(url, **kwargs):
            return Document(url, 'access failed', is_error=True)

        trace = Capture()
        tree = RawTree(Decision(), config(jev_traversal='beam', jev_entries=1,
            jev_reads=2, jev_direct_reads=1, jev_query_reads=1), fetch)
        _, _, stats = await tree.run_search('query', [{'link': BASE+'a'}],
                                            question='question', trace=trace, usage=None)
        self.assertEqual(stats['reads'], 0)
        self.assertEqual(stats['fetch_failed'], 1)
        self.assertEqual(stats.get('zero_read_selections', 0), 0)

    async def test_useful_query_fact_beats_return_without_separate_read_action_call(self):
        def score(state, key, ctx):
            if ctx['phase'] in ('bundle', 'chunk'):
                return .9
            if key == 'direct_answer':
                return .03
            if key == 'query_answer':
                return .82
            return {'return_now': .75, 'read_now': .1, 'expand_now': .2}[key]

        decision, trace, _, (_, text, stats) = await self.run_graph(
            {'a': ['unneeded']}, ['a'], score, jev_notice_tokens=400)
        self.assertEqual(stats['reads'], 1)
        self.assertIn('VERIFIED_a', text)
        self.assertTrue(all('read_now' not in questions for _, questions, _ in decision.calls))
        action = next(e for e in trace.events if e['event'] == 'rawtree.node_action')
        self.assertEqual(action['action'], 'read_now')
        self.assertEqual(action['scores']['read_now'], .82)
        self.assertLess(text.index('Retrieved source excerpts'), text.index('Source access and discovery'))


if __name__ == '__main__':
    unittest.main()
