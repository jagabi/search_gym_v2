"""Offline regressions for Reader validity, browser->curl fallback and near-tie beams."""
import re
import unittest

import httpx

from searchgym.explorer import Document
from searchgym.rawtree import RawTree, near_tie_take
from searchgym.urls import reader_failure
from test_rawtree import Capture
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config


class ReaderValidityTests(unittest.IsolatedAsyncioTestCase):
    def test_separate_title_and_thin_body_are_failures(self):
        self.assertIn('Access challenge', reader_failure(
            'Enable JavaScript and cookies to continue', title='Just a moment...'))
        self.assertIn('Too little readable text', reader_failure('Are you over 18? Enter', min_chars=200))
        self.assertEqual(reader_failure('word ' * 100, title='Article', min_chars=200), '')
        # Markdown Reader output keeps its inline title and no length floor.
        self.assertEqual(reader_failure('Title: Short note\n\nBrief.'), '')

    async def test_browser_reader_challenge_page_is_an_error(self):
        from searchgym.tools import WebTools

        def respond(request):
            return httpx.Response(200, json={'code': 200, 'data': {
                'title': 'Just a moment...', 'content': 'Enable JavaScript and cookies to continue'}})

        tools = WebTools()
        tools.reader_status = {'jina_base_url': 'http://127.0.0.1:3001'}
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            tools._reader_http = client
            doc = await tools.fetch('https://example.org/cgi/viewcontent.cgi?article=1', engine='browser')
        self.assertTrue(doc.is_error)
        self.assertEqual(doc.reader_metadata['failure_stage'], 'reader_content')


class FallbackTests(unittest.IsolatedAsyncioTestCase):
    async def search(self, browser_doc):
        calls = []

        async def fetch(url, *, engine):
            calls.append(engine)
            if engine == 'browser':
                return browser_doc(url)
            return Document(url, 'FINAL_FACT read over plain HTTP.', title='Plain', retrieval='jina_curl')

        decision = Decision(lambda state, key, ctx: .9 if 'FINAL_FACT' in state['page_text'] or key == 'inspect_value' else .01)
        trace = Capture()
        tree = RawTree(decision, config(jev_traversal='beam', jev_entries=1, jev_frontier_width=2,
                                        jev_fetch_budget=4, jev_bundle_tokens=4096, jev_page_tokens=4096), fetch)
        _, text, stats = await tree.run_search('q', [{'link': BASE+'root', 'title': 'Root'}],
                                               question='original', trace=trace, usage=None)
        return calls, text, stats, trace

    async def test_reader_failure_retries_once_with_curl(self):
        calls, text, stats, trace = await self.search(lambda url: Document(
            url, f'Could not read {url}: 422', is_error=True, retrieval='jina_browser',
            reader_metadata={'failure_stage': 'reader_http'}))
        self.assertEqual(calls, ['browser', 'curl'])
        self.assertIn('FINAL_FACT', text)
        self.assertEqual((stats['curl_fallbacks'], stats['curl_fetches'], stats['fetch_failed']), (1, 1, 0))
        event = next(e for e in trace.events if e['event'] == 'rawtree.fetch_fallback')
        self.assertTrue(event['recovered'])

    async def test_policy_blocks_are_not_retried(self):
        calls, _, stats, _ = await self.search(lambda url: Document(
            url, 'BLOCKED: evaluation material', is_error=True, retrieval='jina_browser'))
        self.assertEqual(calls, ['browser'])
        self.assertEqual((stats['curl_fallbacks'], stats['fetch_failed']), (0, 1))


class SearchResultsBlockTests(unittest.IsolatedAsyncioTestCase):
    async def test_all_snippets_lead_the_output_outside_its_budget(self):
        async def fetch(url, *, engine):
            if url.endswith('blocked'):
                return Document(url, 'BLOCKED: evaluation material', is_error=True, retrieval='jina_browser')
            if url.endswith('gated'):
                return Document(url, 'Are you 18?', is_error=True, retrieval='jina_browser',
                                retrieval_note='Too little readable text (9 characters)')
            return Document(url, 'FINAL_FACT body. [Child](' + BASE + 'child)', title='Body')

        results = [{'link': BASE+name, 'title': 'Title '+name, 'snippet': 'Snippet about '+name}
                   for name in ('body', 'gated', 'blocked')]
        decision = Decision(lambda state, key, ctx: .9 if 'FINAL_FACT' in state['page_text'] or key == 'inspect_value' else .01)
        tree = RawTree(decision, config(jev_traversal='beam', jev_entries=3, jev_frontier_width=2,
                       jev_depth=2, jev_fetch_budget=6, jev_bundle_tokens=4096, jev_page_tokens=4096,
                       jev_link_floor=.1, jev_output_tokens=3000, jev_notice_tokens=500,
                       jev_search_results=True), fetch)
        _, text, stats = await tree.run_search('q', results, question='original', trace=Capture(), usage=None)
        self.__class__.sample = text
        block, _, rest = text.partition('\n\nExcerpts from the pages read')
        self.assertTrue(block.startswith('Search results for "q"'))
        self.assertIn('[1] Title body\n' + BASE + 'body\nPage: read; its relevant passages are in the '
                      'excerpts below.\nSnippet about body', block)
        self.assertIn('Page: could not be opened: only a consent, age or bot-check screen came back.\n'
                      'Snippet about gated', block)
        self.assertNotIn('blocked', block)
        self.assertNotIn('NOT answer evidence', text)
        self.assertIn('FINAL_FACT', rest)
        notice = rest.partition('Pages reached through links:')[2]
        self.assertIn('- ' + BASE + 'child (link "Child" on ' + BASE + 'body, link score 0.90): read', notice)
        self.assertNotIn('Snippet about', notice)      # search results are not repeated there
        self.assertGreater(stats['search_results_tokens'], 0)
        self.assertLessEqual(stats['body_output_tokens'] + stats['notice_output_tokens'], 3000)


class NearTieTests(unittest.IsolatedAsyncioTestCase):
    def test_take_widens_only_within_margin_and_cap(self):
        take = lambda rows, margin, cap=4: near_tie_take(rows, lambda v: v, 2, margin, cap)
        self.assertEqual(take([.99, .98, .95, .90], .05), [.99, .98, .95])
        self.assertEqual(take([.99, .98, .97, .96, .96], .05), [.99, .98, .97, .96])
        self.assertEqual(take([.99, .98, .95], 0), [.99, .98])
        self.assertEqual(near_tie_take([1, 2, 3], lambda v: 1, 2, .1, 4, accept=lambda v: v != 2), [1, 3])

    async def children(self, **options):
        scores = {'Film A': .987, 'Film B': .985, 'Film C': .953, 'Other': .5}
        body = 'Director biography. ' + ' '.join(f'[{a}]({BASE}{a[-1]})' for a in scores)

        def score(state, key, ctx):
            if key.startswith('link_'):
                label = re.search(r'\[([^\]]+)\]\(' + key + r'\)', state['page_text'])
                return scores[label.group(1)]
            return .9

        fetched = []

        async def fetch(url, *, engine):
            fetched.append(url.removeprefix(BASE))
            return Document(url, body if url.endswith('root') else 'Film page.', title='T')
        tree = RawTree(Decision(score), config(jev_traversal='beam', jev_entries=1, jev_branch=2,
                       jev_frontier_width=2, jev_depth=2, jev_fetch_budget=10, jev_link_floor=.1,
                       jev_bundle_tokens=4096, jev_page_tokens=4096, **options), fetch)
        await tree.run_search('q', [{'link': BASE+'root', 'title': 'Root'}],
                              question='original', trace=Capture(), usage=None)
        return fetched[1:]

    async def test_near_tied_link_is_not_split_by_branch_or_frontier(self):
        self.assertEqual(await self.children(), ['A', 'B'])
        self.assertEqual(await self.children(jev_tie_margin=.05, jev_tie_width=4), ['A', 'B', 'C'])


if __name__ == '__main__':
    unittest.main()
