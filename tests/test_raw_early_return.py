"""Early return commits source facts before cancelling and draining parallel work."""
import asyncio
import json
import re
import unittest

import httpx
from searchgym.explorer import Document
from searchgym.rawtree import LocalDecision, LocalDecisionError, RawTree
from searchgym.config import load_test
from test_rawtree import Capture, chunker
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config
import test_rawtree_actions as actions


class EarlyReturnTests(unittest.IsolatedAsyncioTestCase):
    run_graph = actions.JointInspectionTests.run_graph

    def decision(self, return_score, score=None):
        return Decision(score or (lambda state,key,ctx: .9), return_score=return_score)

    async def test_returns_root_evidence_before_opening_high_scoring_child(self):
        decision=self.decision(lambda state,ctx:.95)
        _,_,trace,fetched,(_,text,stats)=await self.run_graph(
            {'root':'FINAL_FACT answer [Record]('+BASE+'leaf)'},decision=decision)
        self.assertEqual(fetched,['root'])
        self.assertIn('FINAL_FACT',text)
        self.assertEqual((stats['early_returns'],stats['return_now_signals']),(1,1))
        end=next(e for e in trace.events if e['event']=='rawtree.traversal_end')
        self.assertEqual(end['reason'],'return_now')
        self.assertTrue(any(e['event']=='rawtree.early_return_drained' for e in trace.events))

    async def test_cancels_slow_sibling_after_committing_winning_source(self):
        started,cancelled=asyncio.Event(),asyncio.Event()
        class Parallel(Decision):
            async def noul(self,state,questions,trace,*,usage,context):
                if context['phase']=='bundle':
                    if state['page_title']=='Search b':
                        started.set()
                        try: await asyncio.Event().wait()
                        finally: cancelled.set()
                    else:
                        await started.wait()
                return await super().noul(state,questions,trace,usage=usage,context=context)
        decision=Parallel(lambda *args:.9,return_score=lambda *args:.95)
        _,_,_,fetched,(_,text,stats)=await asyncio.wait_for(self.run_graph(
            {'a':'WINNING_FACT complete answer.','b':'SLOW_SOURCE unfinished.'},
            roots=('a','b'),decision=decision),10)
        self.assertTrue(cancelled.is_set())
        self.assertIn('WINNING_FACT',text)
        self.assertNotIn('SLOW_SOURCE',text)
        self.assertEqual(stats['early_returns'],1)

    async def test_first_packet_can_stop_before_remaining_link_packet_returns(self):
        later_started,later_cancelled=asyncio.Event(),asyncio.Event()
        posted=[]
        async def respond(request):
            body=json.loads(request.content);posted.append(body)
            questions=body['questions']
            if 'inspect_value' in questions:
                return httpx.Response(200,json={'answers':{'inspect_value':{'noul':.9}}})
            if 'return_now' in questions:
                await later_started.wait()
                return httpx.Response(200,json={'answers':{k:{'noul':.95} for k in questions}})
            later_started.set()
            try: await asyncio.Event().wait()
            finally: later_cancelled.set()
        cfg=config(jev_traversal='beam',jev_entries=1,jev_frontier_width=2,jev_depth=3,
                   jev_fetch_budget=10,jev_reads=1,jev_direct_reads=1,jev_query_reads=0,
                   jev_bundle_tokens=4096,jev_page_tokens=4096,jev_output_tokens=16000)
        client=LocalDecision(cfg);await client.http.aclose()
        client.http=httpx.AsyncClient(transport=httpx.MockTransport(respond));client.chunker=chunker(64)
        self.addAsyncCleanup(client.aclose)
        fetched=[]
        body='COMPLETE_ANSWER '+ ' '.join(f'[Record {i}]({BASE}r{i})' for i in range(120))
        async def fetch(url,*,engine):
            fetched.append(url);return Document(url,body,title='Original')
        tree=RawTree(client,cfg,fetch)
        _,text,stats=await asyncio.wait_for(tree.run_search('target',[{'link':BASE+'root','title':'Search'}],
            question='original',trace=Capture(),usage=None),10)
        self.assertTrue(later_cancelled.is_set())
        self.assertEqual(fetched,[BASE+'root'])
        self.assertIn('COMPLETE_ANSWER',text)
        self.assertEqual(stats['early_returns'],1)
        self.assertEqual(client.inflight_questions,0)
        self.assertFalse(client.question_waiters)
        self.assertFalse(client.active_decisions)
        self.assertEqual([len(b['questions']) for b in posted],[1,64,59])
        self.assertTrue(all(set(b['state'])=={'page_title','page_text'} for b in posted))

    async def test_true_without_eligible_facts_does_not_stop_navigation(self):
        def score(state,key,ctx):
            if key=='inspect_value' or key.startswith('link_'):return .9
            return .95 if 'FINAL_FACT' in state['page_text'] else .01
        decision=self.decision(lambda state,ctx:.95 if 'BRIDGE' in state['page_text'] else 0,score)
        _,_,_,fetched,(_,text,stats)=await self.run_graph(
            {'root':'BRIDGE [Record]('+BASE+'leaf)','leaf':'FINAL_FACT explicit answer.'},decision=decision)
        self.assertEqual(fetched,['root','leaf'])
        self.assertIn('FINAL_FACT',text)
        self.assertEqual(stats['early_returns'],0)

    async def test_tie_continues_and_small_output_budget_cannot_trigger_empty_return(self):
        for probability,budget in ((.5,3000),(.99,40)):
            with self.subTest(probability=probability):
                decision=self.decision(lambda *args:probability)
                _,_,_,fetched,(_,_,stats)=await self.run_graph(
                    {'root':'Observed facts '+('ordinary '*50)+' [Record]('+BASE+'leaf)',
                     'leaf':'Observed final source.'},decision=decision,jev_output_tokens=budget)
                self.assertEqual(fetched,['root','leaf'])
                self.assertEqual(stats['early_returns'],0)

    async def test_return_signal_resets_for_the_next_search_on_same_tree(self):
        decision=self.decision(lambda state,ctx:.95)
        tree,_,_,fetched,_=await self.run_graph(
            {'root':'FINAL_FACT [Record]('+BASE+'leaf)','leaf':'FINAL_FACT final.'},decision=decision)
        self.assertEqual(fetched,['root'])
        decision.return_score=lambda *args:0
        _,text,stats=await tree.run_search('different target',[{'link':BASE+'root','title':'Search root'}],
            question='original question',trace=Capture(),usage=None)
        self.assertEqual(fetched,['root','leaf'])
        self.assertEqual(stats['early_returns'],0)
        self.assertIn('FINAL_FACT',text)

    async def test_multiple_completed_return_signals_are_safe(self):
        decision=self.decision(lambda *args:.95)
        _,_,trace,_,(_,text,stats)=await self.run_graph(
            {'a':'FACT_A complete.','b':'FACT_B complete.'},roots=('a','b'),decision=decision)
        self.assertGreaterEqual(stats['return_now_signals'],1)
        self.assertLessEqual(stats['return_now_signals'],2)
        self.assertTrue('FACT_A' in text or 'FACT_B' in text)
        returned=next(e['returned'] for e in trace.events if e['event']=='rawtree.return')
        ids=[(r['node_id'],i) for r in returned for i in r['chunk_ids']]
        self.assertEqual(len(ids),len(set(ids)))

    async def test_returning_bundle_is_not_displaced_by_a_higher_relevance_sibling(self):
        other_done=asyncio.Event()
        class Ordered(Decision):
            async def noul(self,state,questions,trace,*,usage,context):
                if context['phase']=='bundle' and state['page_title']=='Search a':
                    await other_done.wait()
                result=await super().noul(state,questions,trace,usage=usage,context=context)
                if context['phase']=='bundle' and state['page_title']=='Search b':
                    other_done.set()
                return result
        decision=Ordered(lambda state,key,ctx: .3 if state['page_title']=='Search a' else .99,
                         return_score=lambda state,ctx:.95 if state['page_title']=='Search a' else 0)
        _,_,_,_,(_,text,stats)=await self.run_graph(
            {'a':'DECISIVE_FACT sufficient.','b':'HIGH_RELEVANCE incomplete.'},roots=('a','b'),
            decision=decision,jev_reads=1,jev_direct_reads=1,jev_query_reads=0)
        self.assertIn('DECISIVE_FACT',text)
        self.assertNotIn('HIGH_RELEVANCE',text)
        self.assertEqual(stats['evidence_pages'],1)

    async def test_draining_one_search_does_not_cancel_another_search(self):
        started={k:asyncio.Event() for k in ('a','b')}
        release=asyncio.Event()
        async def respond(request):
            body=json.loads(request.content)
            name=body['state']['page_text']
            started[name].set()
            await release.wait()
            return httpx.Response(200,json={'answers':{'gain':{'noul':.8}}})
        client=LocalDecision(config())
        await client.http.aclose()
        client.http=httpx.AsyncClient(transport=httpx.MockTransport(respond));client.chunker=chunker()
        self.addAsyncCleanup(client.aclose)
        trace=Capture()
        from searchgym.jevtree import JevUsage
        jobs=[asyncio.create_task(client.noul({'page_text':name},
            {'gain':{'type':'noul','instructions':'Useful?'}},trace,usage=JevUsage(),
            context={'search_id':name,'phase':'bundle'})) for name in ('a','b')]
        try:
            await asyncio.wait_for(asyncio.gather(*(e.wait() for e in started.values())),5)
            jobs[0].cancel()
            await asyncio.gather(jobs[0],return_exceptions=True)
            await asyncio.wait_for(client.drain_search('a'),5)
            self.assertFalse(jobs[1].done())
            release.set()
            self.assertEqual(await asyncio.wait_for(jobs[1],5),{'gain':.8})
            await client.drain_search('b')
            self.assertEqual(client.inflight_questions,0)
        finally:
            release.set()
            for job in jobs:job.cancel()
            await asyncio.gather(*jobs,return_exceptions=True)

    def test_model_instructions_are_english_and_return_is_only_on_full_bundle(self):
        import ast
        from pathlib import Path
        # Docstrings/comments may be Korean; actual configured model instructions are English.
        cfg=load_test(method='jevtree')
        self.assertIsNone(re.search('[가-힣]',cfg.system_prompt))
        for file in ('searchgym/agent.py','searchgym/rawtree.py','searchgym/raw_research.py'):
            module=ast.parse(Path(file).read_text(encoding='utf-8'))
            for statement in module.body:
                if isinstance(statement,(ast.Assign,ast.AnnAssign)):
                    for item in ast.walk(statement):
                        if isinstance(item,ast.Constant) and isinstance(item.value,str):
                            self.assertIsNone(re.search('[가-힣]',item.value),(file,item.lineno))
