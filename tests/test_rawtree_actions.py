"""Offline regressions for a single inspection gate and joint evidence/link reading."""
import asyncio
import json
import unittest

from searchgym.explorer import Document
from searchgym.rawtree import LocalDecisionError, RawTree
from test_rawtree import Capture
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config


class JointInspectionTests(unittest.IsolatedAsyncioTestCase):
    async def test_ten_roots_leave_four_child_visits_through_depth_three(self):
        roots = tuple(f'root{i}' for i in range(10))
        bodies = {name: f'{name} [A]({BASE}a) [B]({BASE}b)' for name in roots}
        bodies.update(a=f'A [C]({BASE}c) [D]({BASE}d)',
                      b=f'B [C]({BASE}c) [D]({BASE}d)', c='C final fact.', d='D final fact.')
        _, _, trace, fetched, (_, _, stats) = await self.run_graph(
            bodies, roots=roots, score=lambda *args:.9,
            jev_entries=10, jev_fetch_budget=14, jev_depth=3)
        self.assertEqual(fetched[:10], list(roots))
        self.assertEqual(set(fetched[10:]), {'a','b','c','d'})
        self.assertEqual(len(fetched), 14)
        self.assertEqual((stats['entries'],stats['nodes'],stats['max_depth']), (10,14,3))
        selections = [e for e in trace.events if e['event']=='rawtree.inspection_selection']
        self.assertEqual([(e['depth'],len(e['selected'])) for e in selections], [(1,2),(2,2),(3,2)])

    async def run_graph(self, bodies, *, roots=('root',), score=None, decision=None, **options):
        def default(state, key, ctx):
            if key == 'inspect_value':
                return .9
            if key.startswith('link_'):
                return .9
            return .95 if 'FINAL_FACT' in state['page_text'] else .01
        decision = decision or Decision(score or default)
        trace, fetched = Capture(), []
        async def fetch(url, *, engine):
            fetched.append(url.removeprefix(BASE))
            return Document(url, bodies[url.removeprefix(BASE)], title='Reader '+url.removeprefix(BASE))
        settings = dict(jev_traversal='beam', jev_entries=len(roots), jev_frontier_width=2,
                        jev_depth=3, jev_fetch_budget=10, jev_reads=2, jev_branch=2,
                        jev_direct_reads=1, jev_query_reads=1, jev_page_tokens=4096,
                        jev_bundle_tokens=4096, jev_read_dedup=True, jev_link_floor=.1)
        settings.update(options)
        tree = RawTree(decision, config(**settings), fetch)
        output = await tree.run_search('missing relation',
            [{'link': BASE+r, 'title': 'Search '+r} for r in roots],
            question='original question', trace=trace, usage=None,
            main_reasoning='PRIVATE_REASONING_MUST_NOT_BE_FORWARDED')
        return tree, decision, trace, fetched, output

    async def test_single_gate_and_title_sources_with_only_two_state_fields(self):
        _, decision, _, fetched, _ = await self.run_graph({
            'root': '[Record]('+BASE+'leaf)', 'leaf': 'FINAL_FACT original source.'})
        self.assertEqual(fetched, ['root', 'leaf'])
        previews = [(s,q,c) for s,q,c in decision.calls if c['phase']=='preview']
        self.assertEqual([s['page_title'] for s,_,_ in previews], ['Search root', 'Reader leaf'])
        self.assertTrue(all(set(q)=={'inspect_value'} for _,q,_ in previews))
        for state, questions, ctx in decision.calls:
            fields = {'page_title','page_text'}
            if ctx['phase'] == 'preview' and state['page_title'] == 'Search root':
                fields.add('search_snippet')
            self.assertEqual(set(state), fields)
            self.assertNotIn('PRIVATE_REASONING', str(state)+str(questions))
            self.assertLessEqual(decision.chunker.count(json.dumps(state,ensure_ascii=False)),4096)
        self.assertFalse(any(c['phase'] in ('links','link_region','node_action','read_selection')
                             for _,_,c in decision.calls))

    async def test_low_inspection_value_stops_before_bundle_or_link_scoring(self):
        _, decision, _, fetched, (_,_,stats) = await self.run_graph(
            {'root':'[Record]('+BASE+'leaf)'}, score=lambda *args: .01)
        self.assertEqual(fetched,['root'])
        self.assertEqual(stats['reads'],0)
        self.assertEqual([c['phase'] for _,_,c in decision.calls],['preview'])

    async def test_bridge_links_survive_low_evidence_and_final_source_quota_one(self):
        _, decision, _, fetched, (_,text,stats) = await self.run_graph({
            'root':'[Bridge]('+BASE+'bridge)',
            'bridge':'[Back]('+BASE+'root) [Appendix]('+BASE+'leaf)',
            'leaf':'FINAL_FACT requested source fact.'},
            jev_reads=1,jev_direct_reads=1,jev_query_reads=0)
        self.assertEqual(fetched,['root','bridge','leaf'])
        self.assertIn('FINAL_FACT',text)
        self.assertEqual((stats['max_depth'],stats['inspected_pages'],stats['evidence_pages']),(3,3,1))
        joint=[q for s,q,c in decision.calls if c['phase']=='bundle']
        self.assertEqual([len(q) for q in joint],[3,3,2])

    async def test_low_link_score_does_not_expand_even_with_good_evidence(self):
        def score(state,key,ctx):
            return .01 if key.startswith('link_') else .9
        _,_,_,fetched,(_,text,_) = await self.run_graph(
            {'root':'FINAL_FACT [Other]('+BASE+'other)'},score=score)
        self.assertEqual(fetched,['root'])
        self.assertIn('FINAL_FACT',text)

    async def test_only_highest_inspection_candidates_enter_full_reading(self):
        def score(state,key,ctx):
            if key=='inspect_value':
                return {'Search a':.4,'Search b':.9,'Search c':.8}[state['page_title']]
            return .9
        _,decision,trace,fetched,(_,_,stats) = await self.run_graph(
            {k:'FINAL_FACT '+k for k in 'abc'},roots=('a','b','c'),score=score)
        self.assertEqual(set(fetched),set('abc'))
        self.assertEqual({s['page_title'] for s,_,c in decision.calls if c['phase']=='bundle'},
                         {'Search b','Search c'})
        self.assertEqual(stats['inspected_pages'],2)
        self.assertEqual(stats['evidence_pages'],2)

    async def test_inspection_state_includes_title_and_json_in_token_limit(self):
        body='ordinary '*5000
        _,decision,_,_,_ = await self.run_graph({'root':body},score=lambda *args:.01)
        state=decision.calls[0][0]
        self.assertLessEqual(decision.chunker.count(json.dumps(state,ensure_ascii=False)),4096)
        self.assertLess(len(state['page_text']),len(body))

    async def test_identical_source_backfills_inspection_slot_with_distinct_body(self):
        _,decision,_,_,(_,_,stats)=await self.run_graph(
            {'a':'FINAL_FACT identical source.','b':'FINAL_FACT identical source.',
             'c':'FINAL_FACT additional source.'}, roots=('a','b','c'))
        self.assertEqual({s['page_title'] for s,_,c in decision.calls if c['phase']=='bundle'},
                         {'Search a','Search c'})
        self.assertEqual(stats['duplicate_reads_avoided'],1)

    async def test_depth_limit_omits_all_link_questions(self):
        _,decision,_,fetched,_=await self.run_graph(
            {'root':'FINAL_FACT [Other]('+BASE+'other)'},jev_depth=1)
        self.assertEqual(fetched,['root'])
        self.assertTrue(all(not k.startswith('link_') for _,q,c in decision.calls
                            if c['phase']=='bundle' for k in q))

    async def test_fetch_barrier_precedes_joint_reading(self):
        _,_,trace,_,_=await self.run_graph(
            {'a':'FINAL_FACT a','b':'FINAL_FACT b'},roots=('a','b'))
        # Both preview results must exist before inspection selection and full reading.
        names=[e['event'] for e in trace.events]
        last_preview=max(i for i,n in enumerate(names) if n=='rawtree.preview')
        first_inspection=names.index('rawtree.inspection_selection')
        self.assertLess(last_preview,first_inspection)

    async def test_partial_evidence_failure_preserves_valid_link_and_reaches_child(self):
        class Partial(Decision):
            async def noul(self,state,questions,trace,*,usage,context):
                result=await super().noul(state,questions,trace,usage=usage,context=context)
                if context['phase']=='bundle' and 'link_0' in result:
                    result.pop('query_answer')
                    raise LocalDecisionError('synthetic missing evidence key',partial_scores=result)
                return result
        decision=Partial(lambda state,key,ctx: .9)
        _,_,_,fetched,(_,_,stats)=await self.run_graph(
            {'root':'[Record]('+BASE+'leaf)','leaf':'FINAL_FACT original source.'},decision=decision)
        self.assertEqual(fetched,['root','leaf'])
        self.assertEqual(stats['bundle_eval_failures'],1)
