"""Search-o1 repository settings for the ragent/search-o1 baselines; fake model and tools."""
import unittest
from unittest.mock import patch

from searchgym.agent import (SearchAgent, RunResult, Step, REPEATED_QUERY, _final_information,
                             _snippet_context_like_search_o1, _strip_urls_like_search_o1,
                             _truncated_reasoning_like_search_o1)
from searchgym.config import load_test
from searchgym.llm import Reply
from searchgym.serving import profile_for
from searchgym.trace import ToolCall
from test_depthsearch_core import call
from test_reader_integrity import FakeLLM
from test_rawtree import Capture
from offline import FakeTools


class RepositoryHelperTests(unittest.TestCase):
    def test_url_removal_and_compaction(self):
        text = 'See [the page](https://a.example/x) and [https://b.example] now   ---   done'
        self.assertEqual(_strip_urls_like_search_o1(text), 'See [the page] and  now - done')

    def test_snippet_window_and_fallback(self):
        body = 'Intro sentence here. ' * 50 + 'The treaty was signed in 1842 by both parties. ' + 'Tail text. ' * 50
        ok, context = _snippet_context_like_search_o1(body, 'treaty signed 1842 parties', 40)
        self.assertTrue(ok)
        self.assertIn('The treaty was signed in 1842 by both parties.', context)
        self.assertLessEqual(len(context), len('The treaty was signed in 1842 by both parties.') + 80)
        ok, context = _snippet_context_like_search_o1(body, 'nothing alike at all', 40)
        self.assertFalse(ok)
        self.assertEqual(context, body[:80])

    def test_final_information_extraction(self):
        self.assertEqual(_final_information('notes\n**Final Information**\n\nSigned\nin 1842.'), 'Signedin 1842.')
        self.assertEqual(_final_information('no marker'), 'No helpful information found.')

    def test_previous_reasoning_keeps_first_last_four_and_search_steps(self):
        result = RunResult()
        first = Step(turn=1, reasoning='\n'.join(f'line {i}' for i in range(1, 9)))
        first.tool_calls.append(ToolCall(name='web_search', arguments={'query': 'old query'}, result='FOUND'))
        result.steps.append(first)
        result.steps.append(Step(turn=2, reasoning='\n'.join(f'later {i}' for i in range(1, 7))))
        text = _truncated_reasoning_like_search_o1(result, 'new query')
        self.assertTrue(text.startswith('Step 1: line 1'))
        self.assertIn('<|begin_search_query|>old query<|end_search_query|>', text)
        self.assertIn('<|begin_search_result|>FOUND<|end_search_result|>', text)
        self.assertTrue(text.endswith('<|begin_search_query|>new query<|end_search_query|>'))
        self.assertIn('...', text)
        self.assertNotIn('line 5', text)


class SearchO1RunTests(unittest.IsolatedAsyncioTestCase):
    async def run_case(self, method, replies):
        cfg = load_test(method=method)
        llm, trace, tools = FakeLLM(replies), Capture(), FakeTools()
        with patch('searchgym.agent.LLM', return_value=llm):
            agent = SearchAgent(profile_for('gpt-oss'), cfg.agent, method=method,
                                explorer_config=cfg.explorer, explorer_prompt=cfg.explorer_prompt)
        result = await agent.run('When was the treaty signed?', cfg.system_prompt, tools, trace)
        return result, llm, trace, tools

    async def test_one_reason_in_documents_call_reads_all_pages(self):
        result, llm, trace, tools = await self.run_case('search-o1', [
            call('web_search', {'query': 'treaty date'}),
            Reply(text='Analysis.\n**Final Information**\n\nThe treaty was signed in 1842.'),
            call('web_search', {'query': 'treaty date'}),
            Reply(text='The treaty was signed in 1842.')])
        self.assertEqual(result.answer, 'The treaty was signed in 1842.')
        self.assertEqual(len(tools.fetched), 6)                   # every top-k result, one RiD call
        rid = llm.requests[1][0][-1]['content']
        self.assertIn('**Current Search Query:**', rid)
        self.assertEqual(rid.count('**Web Page '), 6)
        self.assertNotIn('ref-1)', rid)                          # URLs stripped from page text
        self.assertNotIn('1840', rid.split('**Searched Web Pages:**')[0])
        event = next(e for e in trace.events if e['event'] == 'search.reason_in_documents')
        self.assertEqual(event['extracted'], 'The treaty was signed in 1842.')
        main_view = llm.requests[2][0][-1]['content']
        self.assertIn('The treaty was signed in 1842.', main_view)
        self.assertNotIn('answer_box', main_view)                # organic results only
        self.assertEqual(result.searches, 1)                     # repeated query not counted
        self.assertTrue(any(e['event'] == 'tool.repeated_query' for e in trace.events))
        self.assertIn(REPEATED_QUERY, str(llm.requests[3][0]))

    async def test_ragent_pages_are_url_free_and_cut_to_8000_chars(self):
        result, llm, _, tools = await self.run_case('ragent', [
            call('web_search', {'query': 'treaty'}),
            call('web_fetch', {'url': 'https://en.wikipedia.org/wiki/Treaty'}),
            Reply(text='1840s.')])
        search_view = llm.requests[1][0][-1]['content']
        self.assertNotIn('answer_box', search_view)
        page = llm.requests[2][0][-1]['content']
        self.assertNotIn('ref-1)', page)
        self.assertLessEqual(len(page), 8000 + 2000)            # page text plus tool framing
        self.assertEqual(result.answer, '1840s.')


class RawSearchViewTests(unittest.IsolatedAsyncioTestCase):
    async def test_search_results_block_is_the_only_copy_of_organic_results(self):
        from test_rawtree_navigation import Decision

        class Tools(FakeTools):
            async def fetch(self, url, engine=None):
                return await super().fetch(url)

        cfg = load_test(method='search-o1-decision')
        llm, trace, tools = FakeLLM([call('web_search', {'query': 'treaty'}), Reply(text='1840s.')]), Capture(), Tools()
        with patch('searchgym.agent.LLM', return_value=llm), \
                patch('searchgym.rawtree.LocalDecision', return_value=Decision()):
            agent = SearchAgent(profile_for('gpt-oss'), cfg.agent, method='search-o1-decision',
                                explorer_config=cfg.explorer, explorer_prompt=cfg.explorer_prompt)
            await agent.run('When was the treaty signed?', cfg.system_prompt, tools, trace)
        view = llm.requests[1][0][-1]['content']
        self.assertEqual(view.count('Scanned records of the signing'), 1)   # snippet shown once
        self.assertTrue(view.startswith('Search results for'))
        self.assertIn('Other search engine output:', view)                  # answer box kept
        self.assertIn('1840', view.split('Other search engine output:')[1])
        self.assertNotIn('Next action:', view)                          # no follow-up notice


class DecisionEndingTests(unittest.IsolatedAsyncioTestCase):
    async def test_exhausted_search_keeps_conversation_like_the_baselines(self):
        from test_rawtree_navigation import Decision

        class Tools(FakeTools):
            async def fetch(self, url, engine=None):
                return await super().fetch(url)

        cfg = load_test(method='search-o1-decision')
        cfg.agent.max_searches = 1
        llm, trace = FakeLLM([call('web_search', {'query': 'treaty'}),
                              call('web_search', {'query': 'treaty again'}),
                              Reply(reasoning='KEEP_THIS_THOUGHT', text='Signed in the 1840s.')]), Capture()
        with patch('searchgym.agent.LLM', return_value=llm),                 patch('searchgym.rawtree.LocalDecision', return_value=Decision()):
            agent = SearchAgent(profile_for('gpt-oss'), cfg.agent, method='search-o1-decision',
                                explorer_config=cfg.explorer, explorer_prompt=cfg.explorer_prompt)
            result = await agent.run('When was the treaty signed?', cfg.system_prompt, Tools(), trace)
        self.assertEqual((result.answer, result.stop_reason, result.searches), ('Signed in the 1840s.', 'answered', 1))
        self.assertFalse(any(e['event'] == 'run.finalizing' for e in trace.events))
        self.assertIn('web_search limit reached', str(llm.requests[2][0]))      # notice, same conversation
        self.assertEqual(llm.requests[2][0][0]['content'].count('You are a reasoning assistant'), 1)
        description = llm.requests[0][1][0]['function']['description']
        self.assertNotIn('links followed', description)                       # no jevtree tool note


if __name__ == '__main__':
    unittest.main()
