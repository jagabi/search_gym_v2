"""Raw finalization contract; fake model, fake search, no external services."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from searchgym.agent import SearchAgent, FINAL_SYSTEM
from searchgym.config import load_test
from searchgym.llm import Reply
from searchgym.serving import profile_for
from test_depthsearch_core import call
from test_reader_integrity import FakeLLM
from test_rawtree import Capture
from test_rawtree_navigation import Decision
from offline import FakeTools


class RawFinalAnswerTests(unittest.IsolatedAsyncioTestCase):
    async def run_case(self, replies):
        cfg = load_test(method='jevtree').agent
        cfg.max_searches = 1
        llm, trace, tools = FakeLLM(replies), Capture(), FakeTools()
        searches = []

        async def search(query):
            searches.append(query)
            return {'organic': []}, SimpleNamespace(is_error=False, duration_ms=1, text='{}')

        tools.search = search
        with patch('searchgym.agent.LLM', return_value=llm), \
                patch('searchgym.rawtree.LocalDecision', return_value=Decision()):
            agent = SearchAgent(profile_for('gpt-oss'), cfg, method='jevtree')
        result = await agent.run('Which record?', 'Research using web_search.', tools, trace)
        return result, llm, trace, searches

    async def test_exhaustion_goes_directly_to_answer_only(self):
        result, llm, trace, searches = await self.run_case([
            call('web_search', {'query': 'record'}), Reply(text='The best-supported answer is A.')])
        self.assertEqual(result.answer, 'The best-supported answer is A.')
        self.assertEqual(result.stop_reason, 'finalized')
        self.assertEqual(searches, ['record'])
        self.assertEqual(len(llm.requests), 2)
        messages, tools = llm.requests[-1]
        self.assertIsNone(tools)
        self.assertEqual(llm.tool_choices[-1], 'none')
        self.assertIn(FINAL_SYSTEM, messages[0]['content'])
        self.assertNotIn('Research using web_search.', messages[0]['content'])
        self.assertTrue(any(e['event'] == 'run.finalizing' and e['reason'] == 'search_exhausted'
                            for e in trace.events))

    async def test_reasoning_only_retry_yields_final_answer_without_more_search(self):
        result, llm, _, searches = await self.run_case([
            call('web_search', {'query': 'record'}),
            Reply(reasoning='PRIVATE_PLAN: search again.'), Reply(text='A, with uncertain dating.')])
        self.assertEqual(result.answer, 'A, with uncertain dating.')
        self.assertEqual(searches, ['record'])
        self.assertEqual(len(llm.requests), 3)
        self.assertNotIn('PRIVATE_PLAN', str(llm.requests[-1]))
        self.assertTrue(all(choice == 'none' for choice in llm.tool_choices[1:]))

    async def test_two_empty_finals_leave_explicit_failure_not_empty_answer(self):
        result, llm, trace, searches = await self.run_case([
            call('web_search', {'query': 'record'}), Reply(reasoning='Search again.'), Reply()])
        self.assertTrue(result.answer.strip())
        self.assertEqual(result.stop_reason, 'final_output_failed')
        self.assertIn('FinalOutputError', result.error)
        self.assertEqual(len(llm.requests), 3)
        self.assertEqual(searches, ['record'])
        self.assertTrue(any(e['event'] == 'run.final_output_failed' and
                            e['origin'] == 'system_failure_notice' for e in trace.events))

    async def test_final_service_error_is_not_presented_as_success(self):
        result, _, trace, _ = await self.run_case([
            call('web_search', {'query': 'record'}), RuntimeError('fake model outage')])
        self.assertTrue(result.answer)
        self.assertTrue(result.error)
        self.assertEqual(result.stop_reason, 'final_output_failed')
        self.assertTrue(any(e['event'] == 'run.salvage_failed' and 'outage' in e['error']
                            for e in trace.events))

    async def test_honest_insufficient_evidence_response_is_preserved(self):
        answer = 'I could not verify the requested award from the retrieved sources.'
        result, _, _, _ = await self.run_case([
            call('web_search', {'query': 'record'}), Reply(text=answer)])
        self.assertEqual(result.answer, answer)
        self.assertIsNone(result.error)
        self.assertEqual(result.stop_reason, 'finalized')

    async def test_research_plan_cannot_replace_exhausted_final_answer(self):
        result, llm, _, searches = await self.run_case([
            call('web_search', {'query': 'record'}),
            Reply(text='Need to verify the funding source.'), Reply(text='A is the strongest candidate.')])
        self.assertEqual(result.answer, 'A is the strongest candidate.')
        self.assertEqual(len(llm.requests), 3)
        self.assertEqual(searches, ['record'])

