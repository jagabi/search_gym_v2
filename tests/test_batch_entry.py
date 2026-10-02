"""Offline batch entry protocol: one plan, bounded reads, closed return, main resumes."""
import json
import unittest
from unittest.mock import patch

from searchgym.agent import AgentConfig, SearchAgent, RunResult, _FetchSession
from searchgym.explorer import Document
from searchgym.llm import Reply
from searchgym.serving import profile_for
from searchgym.research_state import ResearchState
from test_reader_integrity import FakeLLM, MemoryTrace, note, fetch_call
from test_fetch_session import EntryTools, URLS
from test_relational_reading import config, batch_fetch
from test_tool_availability import call


class BatchEntryTests(unittest.IsolatedAsyncioTestCase):
    def make(self, replies, **overrides):
        llm = FakeLLM(replies)
        with patch('searchgym.agent.LLM', return_value=llm):
            agent = SearchAgent(profile_for('gpt-oss'), AgentConfig(
                **dict(dict(depthsearch_control=True, relational_reading=True, max_searches=1), **overrides)),
                'depthsearch', config(), 'Read evidence.')
        return agent, llm

    def assert_closed_calls(self, messages):
        self.assertEqual([m['role'] for m in messages], ['system','user'])
        self.assertNotIn('Select the useful roots', messages[0]['content'])
        payload=json.loads(messages[1]['content'])
        self.assertNotIn('selectable', payload)
        self.assertTrue(payload['readings'])

    async def test_array_shape_errors_recover_without_executing_or_inventing_urls(self):
        for args in [{'urls':'S1'},{'urls':[]},{'url':'S1'},{'urls':{'id':'S1'}}]:
            agent,llm=self.make([call('web_fetch',args),batch_fetch('S1')])
            state=ResearchState();sid=state.register(URLS[0],snippet='record',search_entry=True)
            result=RunResult(research_state=state);session=_FetchSession();trace=MemoryTrace()
            self.assertIsNone(await agent._control('Q',result,trace,[sid],select=True,session=session,batch=True))
            self.assertEqual(session.decision,'invalid_tool_call')
            self.assertEqual(await agent._control('Q',result,trace,[sid],select=True,session=session,batch=True),sid)
            self.assertIn('urls array',str(llm.requests[1][0]))

    async def test_mixed_array_keeps_valid_sources_in_model_order(self):
        agent,llm=self.make([call('web_fetch',{'urls':['S2',None,{'url':'S3'},'S1','S2']})])
        state=ResearchState()
        ids=[state.register(u,snippet='record',search_entry=True) for u in URLS]
        result=RunResult(research_state=state);session=_FetchSession()
        await agent._control('Q',result,MemoryTrace(),ids,select=True,session=session,batch=True)
        self.assertEqual([sid for sid,_ in session.selections],['S2','S1'])
        self.assertEqual(len({cid for _,cid in session.selections}),1)
        self.assertEqual(result.research_state.metrics['batch_unexecuted_urls'],3)

    async def test_valid_subset_survives_invalid_and_duplicate_calls_without_replanning(self):
        plan=batch_fetch('S1','https://invented.example','S1',URLS[1])
        agent,llm=self.make([call('web_search',{'query':'record'}),plan,
            note('ONE\n**Expand:** no'),note('TWO\n**Expand:** no'),
            Reply(text='Both records read.'),Reply(text='Answer')])
        tools,trace=EntryTools(),MemoryTrace()
        result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched,URLS[:2])
        self.assertEqual(result.research_state.metrics['batch_unexecuted_urls'],2)
        req=[e for k,e in trace.events if k=='control.request']
        self.assertEqual([e['mode'] for e in req],['select','batch_return'])
        self.assert_closed_calls(req[-1]['messages'])
        self.assertIn('ONE',str(llm.requests[-1][0]))
        self.assertIn('TWO',str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_all_invalid_plan_recovers_before_any_reading(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('https://invalid.example'),
            batch_fetch('S1','S2'),note('ONE\n**Expand:** no'),note('TWO\n**Expand:** no'),
            Reply(text='Reading complete'),Reply(text='Answer')])
        tools,trace=EntryTools(),MemoryTrace()
        result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.research_state.metrics['selector_recoveries'],1)
        self.assertEqual(tools.fetched,URLS[:2])
        requests=[e for k,e in trace.events if k=='control.request']
        self.assertEqual([e['mode'] for e in requests],['select','select','batch_return'])
        self.assertFalse(llm.replies)

    async def test_closed_return_never_executes_more_fetches_and_main_gets_notes(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1'),
            note('Saved fact\n**Expand:** no'),fetch_call(URLS[1]),fetch_call(URLS[2]),Reply(text='Answer')])
        tools,trace=EntryTools(),MemoryTrace()
        result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer,'Answer')
        self.assertEqual(tools.fetched,URLS[:1])
        returns=[e for k,e in trace.events if k=='control.request' and e['mode']=='batch_return']
        self.assertEqual(len(returns),2)
        self.assertTrue(all(e['tools'] is None and e['tool_choice']=='none' for e in returns))
        self.assertIn('Saved fact',str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_preselected_root_reached_by_recursion_is_not_fetched_twice(self):
        class Linked(EntryTools):
            async def fetch(self,url):
                self.fetched.append(url)
                return Document(url,f'[record]({URLS[1]})' if url==URLS[0] else 'CHILD FACT')
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1','S2'),
            note(f'ROOT\n**Next links:**\n{URLS[1]} | missing relation\n**Expand:** yes'),
            note('CHILD FACT\n**Expand:** no'),Reply(text='DONE'),
            Reply(text='Relationship established'),Reply(text='Answer')])
        tools,trace=Linked(),MemoryTrace()
        result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched,URLS[:2])
        self.assertEqual((result.auto_fetches,result.expansion_nodes),(1,1))
        self.assertTrue(any(k=='search.batch_root_skipped' and e['reason']=='already_processed' for k,e in trace.events))
        returned=next(e for k,e in trace.events if k=='control.request' and e['mode']=='batch_return')
        self.assert_closed_calls(returned['messages'])
        self.assertIn('CHILD FACT',str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_existing_root_allowance_is_a_ceiling_not_a_target(self):
        urls=[f'https://source.example/page{i}' for i in range(8)]
        class Many(EntryTools):
            async def search(self,query):
                from types import SimpleNamespace
                self.searched.append(query)
                data={'organic':[{'link':u,'title':u,'snippet':'record'} for u in urls]}
                return data,SimpleNamespace(is_error=False,duration_ms=1,text=json.dumps(data))
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch(*urls),
            *[note(f'FACT{i}\n**Expand:** no') for i in range(6)],Reply(text='Reading done'),Reply(text='Answer')])
        tools,trace=Many(),MemoryTrace()
        result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched,urls[:6])
        self.assertEqual(result.expansion_nodes,0)
        self.assertEqual(result.research_state.metrics['batch_unexecuted_urls'],2)
        self.assertFalse(llm.replies)

    async def test_explicit_fetch_budget_applies_to_batch(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1','S2','S3'),
            note('FACT\n**Expand:** no'),Reply(text='Reading done'),Reply(text='Answer')],max_fetches=1)
        tools=EntryTools();result=await agent.run('Q','Research',tools,MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched,URLS[:1])
        self.assertFalse(llm.replies)

    async def test_batch_return_failure_preserves_notes_for_main(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1'),
            note('FACT\n**Expand:** no'),RuntimeError('closure failed'),Reply(text='Answer')])
        result=await agent.run('Q','Research',EntryTools(),MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(result.answer,'Answer')
        self.assertIn('FACT',str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)
