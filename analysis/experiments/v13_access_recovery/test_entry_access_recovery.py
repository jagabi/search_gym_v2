"""A failed root may use one alternate selection within the existing allowances."""
import json
import unittest

from searchgym.explorer import Document
from searchgym.llm import Reply
import test_batch_entry as batch_support
from test_fetch_session import EntryTools, URLS
from test_reader_integrity import MemoryTrace, note
from test_relational_reading import batch_fetch
from test_tool_availability import call


class FailedRoots(EntryTools):
    def __init__(self, failures):
        super().__init__(); self.failures=set(failures)

    async def fetch(self,url):
        self.fetched.append(url)
        if url in self.failures:
            return Document(url,'403 Forbidden',is_error=True)
        return Document(url,'Verified page content')


class AccessRecoveryTests(unittest.IsolatedAsyncioTestCase):
    make = batch_support.BatchEntryTests.make

    async def test_failed_root_gets_alternate_without_another_search(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1'),batch_fetch('S2'),
                            note('FACT\n**Expand:** no'),Reply(text='Alternate supplied the fact.'),Reply(text='Answer')])
        trace=MemoryTrace();tools=FailedRoots(URLS[:1]);result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error);self.assertEqual(result.searches,1)
        self.assertEqual(tools.fetched,URLS[:2]);self.assertEqual(result.auto_fetches,2)
        self.assertEqual(result.research_state.metrics['entry_access_recoveries'],1)
        requests=[e for k,e in trace.events if k=='control.request']
        self.assertEqual([r['mode'] for r in requests],['select','select','batch_return'])
        payload=json.loads(requests[1]['messages'][1]['content'])
        self.assertNotIn('S1',payload['selectable']);self.assertIn('S2',payload['selectable'])
        self.assertEqual(payload['max_root_reads'],5)
        self.assertIn('FACT',str(llm.requests[-1][0]));self.assertIn('Access failure',str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_one_successful_page_suppresses_access_recovery_even_if_irrelevant(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1','S2'),
                            note('Unrelated page\n**Expand:** no',status='not_found'),
                            Reply(text='No useful facts.'),Reply(text='Unknown')])
        result=await agent.run('Q','Research',FailedRoots(URLS[:1]),MemoryTrace())
        self.assertIsNone(result.error)
        self.assertNotIn('entry_access_recoveries',result.research_state.metrics)
        self.assertFalse(llm.replies)

    async def test_no_third_selection_when_both_access_rounds_fail(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1'),batch_fetch('S2'),
                            Reply(text='Both sources inaccessible.'),Reply(text='Unknown')])
        tools=FailedRoots(URLS);trace=MemoryTrace();result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error);self.assertEqual(tools.fetched,URLS[:2])
        self.assertEqual(sum(k=='search.entry_access_recovery' for k,e in trace.events),1)
        self.assertFalse(llm.replies)

    async def test_recovery_cannot_bypass_explicit_fetch_cap(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1'),
                            Reply(text='Unavailable.'),Reply(text='Unknown')],max_fetches=1)
        tools=FailedRoots(URLS);result=await agent.run('Q','Research',tools,MemoryTrace())
        self.assertEqual(tools.fetched,URLS[:1])
        self.assertNotIn('entry_access_recoveries',result.research_state.metrics)
        self.assertFalse(llm.replies)

    async def test_invalid_recovery_does_not_replay_the_old_selection(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1'),
            batch_fetch('S1'),batch_fetch('unknown'),batch_fetch('unknown'),
            Reply(text='No alternative could be opened.'),Reply(text='Unknown')])
        tools=FailedRoots(URLS);result=await agent.run('Q','Research',tools,MemoryTrace())
        self.assertIsNone(result.error);self.assertEqual(tools.fetched,URLS[:1])
        self.assertLessEqual(result.research_state.metrics['selector_recoveries'],2)
        self.assertLessEqual(result.research_state.metrics['controller_calls'],6)
        self.assertFalse(llm.replies)

    async def test_root_allowance_is_shared_across_selection_rounds(self):
        agent,llm=self.make([call('web_search',{'query':'record'}),batch_fetch('S1','S2'),
            batch_fetch('S3','S4'),note('FACT\n**Expand:** no'),Reply(text='Answer')])
        agent.explorer_config.max_turns=3
        tools=FailedRoots(URLS[:2]);trace=MemoryTrace()
        result=await agent.run('Q','Research',tools,trace)
        self.assertIsNone(result.error);self.assertEqual(tools.fetched,URLS[:3])
        requests=[e for k,e in trace.events if k=='control.request']
        self.assertEqual(json.loads(requests[1]['messages'][1]['content'])['max_root_reads'],1)
        self.assertLessEqual(result.research_state.metrics['controller_calls'],3)
