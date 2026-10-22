"""Offline regressions for links evaluated together with observed source bundles."""
import asyncio
import json
import unittest
from collections import defaultdict
from unittest.mock import AsyncMock

import httpx
from searchgym.explorer import Document
from searchgym.jevtree import JevUsage, TreeNode
from searchgym.raw_chunks import Chunk
from searchgym.rawtree import LocalDecision, RawTree
from test_rawtree import Capture, chunker
import test_rawtree_actions as actions
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config


class JointLinkTests(unittest.IsolatedAsyncioTestCase):
    run_graph = actions.JointInspectionTests.run_graph

    async def test_same_bundle_has_evidence_keys_and_multiple_link_keys(self):
        _,decision,_,fetched,(_,text,stats)=await self.run_graph({
            'root':'Original record: [First]('+BASE+'a) and [Second]('+BASE+'b).',
            'a':'FINAL_FACT first source.','b':'FINAL_FACT second source.'})
        root_calls=[(s,q,c) for s,q,c in decision.calls if c['phase']=='bundle'
                    and s['page_title']=='Search root']
        self.assertEqual(len(root_calls),1)
        state,questions,_=root_calls[0]
        self.assertEqual(set(questions),{'direct_answer','query_answer','link_0','link_1'})
        self.assertIn('(link_0)',state['page_text'])
        self.assertIn('(link_1)',state['page_text'])
        self.assertEqual(set(state),{'page_title','page_text'})
        self.assertNotIn(BASE+'a',str(questions))
        self.assertEqual(set(fetched),{'root','a','b'})
        self.assertIn('FINAL_FACT',text)

    async def test_120_links_share_state_across_two_real_transport_packets(self):
        posted=[]
        async def respond(request):
            body=json.loads(request.content);posted.append(body)
            return httpx.Response(200,json={'answers':{k:{'noul':.8} for k in body['questions']}})
        cfg=config(jev_traversal='beam',jev_bundle_tokens=4096,jev_page_tokens=4096)
        client=LocalDecision(cfg)
        await client.http.aclose()
        client.http=httpx.AsyncClient(transport=httpx.MockTransport(respond))
        client.chunker=chunker(64)
        self.addAsyncCleanup(client.aclose)
        tree=RawTree(client,cfg,None)
        text=' '.join(f'[Record {i}]({BASE}record{i})' for i in range(120))
        node=TreeNode(url=BASE+'root',depth=1,anchor='Source')
        state,questions,links=tree._joint_input(node,text,'original','query',{BASE+'root'})
        result=await client.noul(state,questions,Capture(),usage=JevUsage(),
                                 context={'phase':'bundle','search_id':'s'})
        self.assertEqual(len(links),120)
        self.assertEqual([len(b['questions']) for b in posted],[64,58])
        self.assertEqual(len(result),122)
        self.assertTrue(all(b['state']==state for b in posted))
        self.assertLessEqual(client.chunker.count(json.dumps(state,ensure_ascii=False)),4096)

    def test_visited_self_and_duplicate_destinations_are_filtered_before_keys(self):
        decision=Decision()
        tree=RawTree(decision,config(jev_traversal='beam'),None)
        node=TreeNode(url=BASE+'parent',depth=2,document=Document(BASE+'parent','',title='Reader'))
        text='[Self]('+BASE+'parent) [Back]('+BASE+'root) [New]('+BASE+'leaf) [Again]('+BASE+'leaf)'
        _,questions,links=tree._joint_input(node,text,'Q','q',{BASE+'root',BASE+'parent'})
        self.assertEqual([url for url,_ in links],[BASE+'leaf'])
        self.assertEqual(set(questions),{'direct_answer','query_answer','link_0'})

    async def test_routing_can_reach_link_only_tail_without_answer_evidence(self):
        def score(state,key,ctx):
            if ctx['phase']=='region':
                return .95 if 'USEFUL_ROUTE' in state['page_text'] else .01
            return .95 if key.startswith('link_') else .01
        decision,trace,stats=Decision(score),Capture(),defaultdict(int)
        cfg=config(jev_traversal='beam',jev_document_tree=True,jev_bundle_tokens=4096)
        tree=RawTree(decision,cfg,None)
        chunks=[Chunk(i,('USEFUL_ROUTE [Record]('+BASE+'leaf)' if i==63 else f'Ordinary {i}'),5,[])
                for i in range(64)]
        bundles=[{'id':i,'chunk_ids':[i],'text':c.text} for i,c in enumerate(chunks)]
        tree._chunks=AsyncMock(return_value=(chunks,bundles,False))
        node=TreeNode(url=BASE+'root',depth=1,node_id='n',anchor='Index',
                      document=Document(BASE+'root','source'))
        async def evaluate(coro,*args,**kwargs):return await coro
        async def unexpected(*args,**kwargs):self.fail('joint scorer must replace standalone scorer')
        text,_,returned,_=await tree._read_rows([{'id':'n','node':node,'objective':'direct_answer'}],
            question='Q',query='q',search_id='s',trace=trace,meter=JevUsage(),stats=stats,
            failures=[],scores=unexpected,evaluate=evaluate,visited={BASE+'root'})
        self.assertEqual([u for _,u,_ in node.link_scores],[BASE+'leaf'])
        self.assertEqual(returned,[])
        self.assertTrue(any('concrete outgoing links' in str(q) for _,q,c in decision.calls
                            if c['phase']=='region'))

    async def test_returned_source_keeps_original_urls_and_does_not_include_markers(self):
        def score(state,key,ctx):
            return .01 if key.startswith('link_') else .9
        _,_,_,_,(_,text,_)=await self.run_graph(
            {'root':'FINAL_FACT source [Record]('+BASE+'leaf)'},score=score)
        self.assertIn(BASE+'leaf',text)
        self.assertNotIn('(link_0)',text)

    async def test_rebundling_keeps_complete_state_within_budget(self):
        body='\n\n'.join('Original paragraph '+str(i)+' '+('facts '*45) for i in range(25))
        _,decision,_,_,_=await self.run_graph({'root':body},
            score=lambda *args:.9,jev_bundle_tokens=512,jev_chunk_tokens=64,
            jev_document_tree=False)
        calls=[s for s,_,c in decision.calls if c['phase']=='bundle']
        self.assertGreater(len(calls),1)
        self.assertTrue(all(decision.chunker.count(json.dumps(s,ensure_ascii=False))<=512 for s in calls))

    async def test_page_link_cap_is_shared_across_all_observed_bundles(self):
        body='\n\n'.join(f'Original record {i}: [Record {i}]({BASE}record{i})' for i in range(360))
        def score(state,key,ctx):return .01 if key.startswith('link_') else .9
        _,decision,trace,fetched,(_,_,stats)=await self.run_graph({'root':body},score=score,
            jev_bundle_tokens=1024,jev_chunk_tokens=64,jev_document_tree=False)
        self.assertEqual(fetched,['root'])
        calls=[q for _,q,c in decision.calls if c['phase']=='bundle']
        self.assertEqual(sum(k.startswith('link_') for q in calls for k in q),300)
        self.assertEqual(stats['links_scored'],300)
        self.assertGreater(stats['link_budget_skips'],0)
        self.assertTrue(any(r['skip_reason']=='page_link_budget' for e in trace.events
                            if e['event']=='rawtree.links' for r in e['links']))
