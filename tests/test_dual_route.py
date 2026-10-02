import unittest
from unittest.mock import patch

from searchgym.agent import AgentConfig, SearchAgent
from searchgym.explorer import ExplorerConfig
from searchgym.llm import Reply
from searchgym.serving import profile_for
from test_reader_integrity import FakeLLM, MemoryTrace, note
from test_relational_reading import batch_fetch
from test_fetch_session import EntryTools
from test_tool_availability import call


class DualRouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_isolated_planning_shared_total_budget_and_combined_final_evidence(self):
        llm = FakeLLM([
            call('web_search', {'query': 'first relation'}), batch_fetch('S1'),
            note('ROUTE_A_ONLY evidence\n**Expand:** no'), Reply(text='A relation observed.'),
            call('web_search', {'query': 'second relation'}), batch_fetch('S2'),
            note('ROUTE_B_ONLY evidence\n**Expand:** no'), Reply(text='B relation observed.'),
            Reply(text='Combined answer')])
        with patch('searchgym.agent.LLM', return_value=llm):
            agent = SearchAgent(profile_for('gpt-oss'), AgentConfig(max_searches=2,
                depthsearch_control=True, relational_reading=True, dual_route=True),
                'depthsearch', ExplorerConfig(max_depth=1, max_turns=6), 'Extract evidence.')
        tools, trace = EntryTools(), MemoryTrace()
        result = await agent.run('Original question', 'Research', tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, 'Combined answer')
        self.assertEqual(result.searches, 2)
        self.assertEqual(tools.searched, ['first relation', 'second relation'])
        self.assertNotIn('ROUTE_A_ONLY', str(llm.requests[4][0]))
        self.assertNotIn('ROUTE_A_ONLY', str(llm.requests[5][0]))
        self.assertIn('ROUTE_A_ONLY', str(llm.requests[-1][0]))
        self.assertIn('ROUTE_B_ONLY', str(llm.requests[-1][0]))
        self.assertEqual(llm.tool_choices[-1], 'none')
        self.assertEqual(sum(k == 'research.route_switch' for k, _ in trace.events), 1)
        self.assertEqual(result.research_state.metrics['batch_return_calls'], 2)
        self.assertFalse(llm.replies)


if __name__ == '__main__':
    unittest.main()
