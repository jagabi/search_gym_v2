import unittest
from unittest.mock import patch

from searchgym.agent import AgentConfig, SearchAgent
from searchgym.explorer import ExplorerConfig
from searchgym.llm import Reply
from searchgym.serving import profile_for
from test_reader_integrity import FakeLLM, MemoryTrace, note
from test_relational_reading import batch_fetch
from test_fetch_session import EntryTools, URLS
from test_tool_availability import call


class AdaptiveEntryTests(unittest.IsolatedAsyncioTestCase):
    def agent(self, replies, turns=6):
        llm = FakeLLM(replies)
        with patch('searchgym.agent.LLM', return_value=llm):
            agent = SearchAgent(profile_for('gpt-oss'), AgentConfig(max_searches=1,
                depthsearch_control=True, relational_reading=True, adaptive_entry=True),
                'depthsearch', ExplorerConfig(max_depth=1, max_turns=turns), 'Extract evidence.')
        return agent, llm

    async def test_returned_evidence_informs_second_batch_then_main_continues(self):
        agent, llm = self.agent([call('web_search', {'query': 'record'}), batch_fetch('S1'),
            note('First source identifies the second record.'), batch_fetch('S2'),
            note('Second source gives the date 1840.'), Reply(text='Two records establish the date.'),
            Reply(text='1840')])
        tools, trace = EntryTools(), MemoryTrace()
        result = await agent.run('Find the date.', 'Research', tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, '1840')
        self.assertEqual(tools.fetched, URLS[:2])
        self.assertEqual(result.searches, 1)
        self.assertIn('First source identifies', str(llm.requests[3][0]))
        choices = llm.requests[3][1][0]['function']['parameters']['properties']['urls']
        self.assertNotIn('S1', choices['items']['enum'])
        self.assertEqual(choices['maxItems'], 5)
        self.assertEqual(llm.tool_choices[-1], 'none')
        self.assertIn('Second source gives', str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_cumulative_root_and_entry_call_limits_force_tool_free_closure(self):
        agent, llm = self.agent([call('web_search', {'query': 'record'}), batch_fetch('S1', 'S2'),
            note('Evidence one'), note('Evidence two'), batch_fetch('S3', 'S4'),
            note('Evidence three'), Reply(text='Three sources checked.'), Reply(text='Answer')], turns=3)
        tools, trace = EntryTools(), MemoryTrace()
        result = await agent.run('Question', 'Research', tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, URLS[:3])
        self.assertEqual(result.auto_fetches, 3)
        self.assertEqual(llm.requests[4][1][0]['function']['parameters']['properties']['urls']['maxItems'], 1)
        self.assertIsNone(llm.requests[6][1])
        self.assertEqual(llm.tool_choices[6], 'none')
        entry = [e for k,e in trace.events if k=='control.request']
        self.assertEqual(len(entry), 3)
        self.assertEqual(result.answer, 'Answer')
        self.assertFalse(llm.replies)


if __name__ == '__main__':
    unittest.main()
