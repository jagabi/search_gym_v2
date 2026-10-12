import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from searchgym.explorer import Document
from searchgym.jevtree import JevTree
from searchgym.llm import Usage
from searchgym.trace import Trace


class LDSTests(unittest.IsolatedAsyncioTestCase):
    async def test_shared_jina_session_caps_fifty_inflight_requests(self):
        from searchgym.tools import WebTools
        active=peak=0
        async def call_tool(*args):
            nonlocal active,peak
            active+=1;peak=max(peak,active)
            await asyncio.sleep(.01)
            active-=1
            return SimpleNamespace(content=[],isError=False)
        with patch.dict('os.environ',{'JINA_MAX_CONCURRENT':'50'}):
            tools=WebTools()
        tools._session=SimpleNamespace(call_tool=call_tool)
        await asyncio.gather(*(tools.call('web_fetch',{'url':f'https://x.test/{i}'}) for i in range(55)))
        self.assertEqual(peak,50)

    async def exercise(self, budget=12, delay_reverse=False):
        tmp=tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        trace=Trace(Path(tmp.name)/'trace.jsonl','test')
        active=peak=0; fetched=[]
        class Jev:
            async def noul(self,state,questions,trace,usage,context):
                usage.calls+=1
                # Even very low roots are mandatory; scores do not prune LDS.
                return {key:.01 for key in questions}
        async def fetch(url):
            nonlocal active,peak
            fetched.append(url);active+=1;peak=max(peak,active)
            await asyncio.sleep(.004 if ('a.test' in url)==delay_reverse else .001)
            active-=1
            return Document(url=url,content=url)
        tree=JevTree(jev=Jev(),llm=SimpleNamespace(),fetch=fetch,reader_prompt='',reader_max_tokens=10,
                     entries=2,branch=2,depth=3,reads=0,floor=.15,jev_page_tokens=100,visited=set(),
                     strategy='lds',fetch_budget=budget)
        async def score(node,*args,**kwargs):
            node.identification=node.query_answer=.01
            node.link_scores=[(.08,node.url+'/1','first'),(.07,node.url+'/2','second')] if node.depth<3 else []
        tree._score=score
        log,_,stats=await tree.run_search('q',[{'link':'https://a.test'},{'link':'https://b.test'}],
                                        question='q',main_reasoning='',trace=trace,usage=Usage())
        return log,stats,fetched,peak

    async def test_order_parallelism_budget_depth_and_causal_replay(self):
        log,stats,fetched,peak=await self.exercise(budget=10)
        self.assertEqual(stats['fetched'],10)
        self.assertEqual(peak,2)
        self.assertEqual(fetched[:6],['https://a.test','https://b.test',
            'https://a.test/1','https://b.test/1','https://a.test/1/1','https://b.test/1/1'])
        self.assertEqual(fetched[6:8],['https://a.test/2','https://b.test/2'])
        lds=log['lds']; known={}
        for action in lds['actions']:
            for n in action['updates']:
                if n['parent_id']:
                    self.assertIn(n['parent_id'],known)
                    self.assertIn(known[n['parent_id']]['status'],('scored','ready'))
                known[n['id']]=n
        self.assertEqual(known,{n['id']:n for n in lds['nodes']})
        self.assertTrue(all(n['depth']<=3 for n in known.values()))
        self.assertTrue(all(n['discrepancy']==0 for n in known.values() if not n['parent_id']))

    async def test_completion_order_does_not_change_choices(self):
        a=await self.exercise(delay_reverse=False)
        b=await self.exercise(delay_reverse=True)
        self.assertEqual(a[2],b[2])

    async def test_failure_duplicate_and_previsited_do_not_escape_budget(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        trace=Trace(Path(tmp.name)/'trace.jsonl','test')
        class Jev:
            async def noul(self,state,questions,trace,usage,context):
                return {k:.9 for k in questions}
        async def fetch(url):
            return Document(url=url,content='failure' if url.endswith('/bad') else 'identical content',is_error=url.endswith('/bad'))
        tree=JevTree(jev=Jev(),llm=None,fetch=fetch,reader_prompt='',reader_max_tokens=10,
                     entries=2,branch=2,depth=2,reads=0,floor=.15,jev_page_tokens=100,
                     visited={'https://x.test/old'},strategy='lds',fetch_budget=3)
        async def score(*args,**kwargs): pass
        tree._score=score
        _,_,stats=await tree.run_search('q',[{'link':'https://x.test/'+s} for s in ['old','bad','ok','same']],
             question='q',main_reasoning='',trace=trace,usage=Usage())
        self.assertEqual(stats['fetched'],3)
        self.assertEqual(stats['fetch_failed'],1)
        self.assertEqual(stats['duplicates'],1)

class ReaderTransportTests(unittest.TestCase):
    def test_local_http_no_pacing_no_hosted_key(self):
        from searchgym.tools import server
        with patch.object(server,'JINA_BASE_URL','http://127.0.0.1:3001'), \
             patch.dict('os.environ',{'JINA_RPM':'0','JINA_API_KEY':'not-for-local'}), \
             patch.object(server,'_request',return_value='markdown') as request:
            self.assertEqual(server.fetch('https://example.org/a'),'markdown')
            args,kw=request.call_args
            self.assertEqual(args[:3],('127.0.0.1:3001','GET','/https://example.org/a'))
            self.assertNotIn('Authorization',args[3])
            self.assertEqual(kw['scheme'],'http')
            self.assertIsNone(kw['pacer'])

    def test_default_public_pacing_preserved(self):
        from searchgym.tools import server
        with patch.object(server,'JINA_BASE_URL','https://r.jina.ai'), \
             patch.object(server,'_pacer',None),patch.dict('os.environ',{'JINA_RPM':'','JINA_API_KEY':''}):
            self.assertAlmostEqual(server._jina_pacer().interval,60/18)

