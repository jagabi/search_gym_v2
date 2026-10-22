"""Offline regressions for unified evidence ranking and main-model token budgets."""
import json
import unittest
from collections import defaultdict

import httpx
from searchgym.config import load_test
from searchgym.explorer import Document
from searchgym.jevtree import TreeNode
from searchgym.llm import LLM
from searchgym.raw_chunks import Chunk
from searchgym.rawtree import RawTree, evidence_question
from test_rawtree import Capture
from test_rawtree_navigation import Decision
from test_rawtree_policy import config, BASE


class UnifiedOutputTests(unittest.IsolatedAsyncioTestCase):
    async def render_sources(self, values, *, budget=100000, counter=None):
        cfg=config(jev_traversal='beam',jev_direct_chunks=0,jev_query_chunks=0)
        tree=RawTree(Decision(),cfg,None,count_output_tokens=counter)
        cache={};pages=[]
        for i,value in enumerate(values):
            node=TreeNode(url=BASE+str(i),node_id=f'n{i}',depth=1,
                          document=Document(BASE+str(i),f'UNIQUE_{i}'))
            c=Chunk(0,f'UNIQUE_{i}',1,[])
            unit={'id':f'n{i}:bundle:0','node':node,'chunk_ids':[0],'chunk_id':0,
                  'bundle_id':0,'evaluation_unit':'bundle','evidence_value':value}
            cache[node.node_id]=([c],[unit]);pages.append({'id':node.node_id,'node':node})
        trace=Capture()
        result=await tree._read_rows(pages,question='Q',query='q',search_id='s',trace=trace,
            meter=None,stats=defaultdict(int),failures=[],scores=None,evaluate=None,
            output_budget=budget,scored_pages=cache,record_notes=False,visited=set())
        return tree,trace,result

    async def test_all_sources_rank_by_one_score_without_legacy_count_quota(self):
        _,_,(text,picked,returned,_)=await self.render_sources([.2,.9,.6]+[.3]*12)
        self.assertEqual([r['evidence_value'] for r in picked],sorted([.2,.9,.6]+[.3]*12,reverse=True))
        self.assertEqual(len(returned),15)
        self.assertTrue(all(r['objective']=='evidence_value' for r in picked))
        self.assertIn('UNIQUE_0',text)

    async def test_main_counter_controls_admission_instead_of_decision_tokenizer(self):
        counted=[]
        async def counter(text):
            counted.append(text)
            return 10+1000*text.count('UNIQUE_')
        tree,trace,(text,picked,_,_)=await self.render_sources([.2,.9,.6],budget=1200,counter=counter)
        self.assertEqual([r['id'] for r in picked],['n1:bundle:0'])
        self.assertEqual(await tree._count_output_tokens(text),1010)
        self.assertTrue(any(t.count('UNIQUE_')==2 for t in counted))
        self.assertEqual(sum(e['event']=='rawtree.output_budget' for e in trace.events),2)

    def test_compact_question_and_default_budget_contract(self):
        q=evidence_question('ORIGINAL_QUESTION','SEARCH_QUERY')
        self.assertEqual(q['type'],'noul')
        self.assertIn('Original question: ORIGINAL_QUESTION',q['instructions'])
        self.assertIn('Search query: SEARCH_QUERY',q['instructions'])
        self.assertLess(len(q['instructions'].split()),65)
        cfg=load_test(method='jevtree').agent
        self.assertEqual((cfg.jev_output_tokens-cfg.jev_notice_tokens,cfg.jev_notice_tokens),(14336,2048))

    async def test_notice_counts_main_model_tokens_and_preserves_whole_rows(self):
        async def counter(text):return len(text)
        tree=RawTree(Decision(),config(),None,count_output_tokens=counter)
        leads=[{'url':BASE+'small','title':'small','snippet':'ok'},
               {'url':BASE+'large','title':'large','snippet':'x'*2000}]
        notice=await tree._navigation_notice(leads,[],[],tree.jev.chunker,500)
        self.assertLessEqual(await counter('\n\n'+notice),500)
        rows=notice.split('\n')[1:]
        self.assertEqual(len(rows),1)
        self.assertEqual(json.loads(rows[0])['url'],BASE+'small')

    async def test_output_tokenizer_uses_served_model_and_never_estimates_on_error(self):
        async def response(request):
            body=json.loads(request.content)
            self.assertEqual(body,{'model':'served-gpt-oss','prompt':'source text'})
            return httpx.Response(200,json={'count':321})
        llm=LLM.__new__(LLM)
        llm.base_url='http://offline/v1';llm.model_name='served-gpt-oss';llm.api_key='EMPTY'
        llm._http=httpx.AsyncClient(transport=httpx.MockTransport(response))
        self.addAsyncCleanup(llm.aclose)
        self.assertEqual(await llm.count_output_tokens('source text'),321)
        await llm._http.aclose()
        llm._http=httpx.AsyncClient(transport=httpx.MockTransport(lambda req:httpx.Response(500)))
        with self.assertRaisesRegex(RuntimeError,'output tokenizer unavailable'):
            await llm.count_output_tokens('source text')


if __name__=='__main__':unittest.main()
