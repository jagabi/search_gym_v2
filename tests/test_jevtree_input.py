import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from searchgym.explorer import Document
from searchgym.jevtree import JevTree, TreeNode, JevUsage, candidate_links
from searchgym.jevtree_input import complete_prefix, numbered_page, page_requests


class PrefixInputTests(unittest.TestCase):
    def test_markdown_url_crossing_cut_is_not_a_candidate(self):
        source = '[Good](https://example.org/good) then [Tail](https://example.org/long-tail) end'
        prefix = complete_prefix(source, source[:source.index('long-tail') + 3])
        links = candidate_links(prefix, 'https://example.org/root', set())
        self.assertEqual(links, [('https://example.org/good', 'Good')])
        self.assertNotIn('[Tail]', prefix)

    def test_bare_url_crossing_cut_is_removed(self):
        source = 'Read https://example.org/complete-path for details'
        prefix = complete_prefix(source, source[:source.index('complete-path') + 4])
        self.assertEqual(prefix, 'Read ')
        self.assertEqual(candidate_links(prefix, 'https://example.org/root', set()), [])

    def test_numbering_preserves_labels_location_and_escaped_urls(self):
        page = 'Before [Film](https://example.org/Film\\_(2020)) after. More: https://example.org/team'
        links = candidate_links(page, 'https://example.org/root', set())
        numbered = numbered_page(page, links)
        self.assertIn('Before [Film](link_0) after.', numbered)
        self.assertIn('https://example.org/team [link_1]', numbered)
        self.assertEqual(links[0][0], 'https://example.org/Film_(2020)')

    def test_requests_have_only_original_question_page_and_short_questions(self):
        page = '[One](https://example.org/one)\n[Two](https://example.org/two)'
        links = candidate_links(page, 'https://example.org/root', set())
        packets = page_requests(question='Q', page_url='https://example.org/root', page=page,
            links=links, page_questions={'direct_answer': {'type': 'noul'},
                                         'answer_likelihood': {'type': 'noul'}}, links_per_request=1)
        self.assertEqual(len(packets), 2)
        for state, questions in packets:
            self.assertEqual(set(state), {'question', 'page_url', 'page_text'})
            self.assertEqual(state['question'], 'Q')
            self.assertIn('[Two](link_1)', state['page_text'])
        self.assertEqual(set(packets[0][1]), {'direct_answer', 'answer_likelihood', 'link_0'})
        self.assertEqual(set(packets[1][1]), {'link_1'})


class PrefixPipelineTests(unittest.IsolatedAsyncioTestCase):
    async def test_only_capped_prefix_links_are_scored_without_changing_reader_source(self):
        url = 'https://example.org/root'
        head = 'Facts [Keep](https://example.org/keep).\n'
        source = head + 'Other text.\n' * 100 + '[Outside](https://example.org/outside)'
        async def cap(text, limit):
            self.assertEqual(limit, 5000)
            return text[:len(head)], True
        jev = SimpleNamespace(noul=AsyncMock(return_value={
            'direct_answer': .8, 'answer_likelihood': .7, 'link_0': .9}))
        llm = SimpleNamespace(cap=cap, chat=AsyncMock(side_effect=AssertionError('No preparation call')))
        tree = JevTree(jev=jev, llm=llm, fetch=AsyncMock(), reader_prompt='unchanged',
            reader_max_tokens=8192, entries=3, branch=3, depth=3, reads=6, floor=.15,
            jev_page_tokens=5000, visited=set())
        node = TreeNode(url, 1, document=Document(url, source))
        await tree._score(node, 'Which person?', SimpleNamespace(event=lambda *a, **k: None),
                          {'links_scored': 0}, JevUsage(), 'search')
        state, questions = jev.noul.call_args.args[:2]
        self.assertEqual(set(questions), {'direct_answer', 'answer_likelihood', 'link_0'})
        self.assertNotIn('Outside', state['page_text'])
        self.assertIn('[Keep](link_0)', state['page_text'])
        self.assertEqual(node.link_scores, [(.9, 'https://example.org/keep', 'Keep')])
        self.assertEqual((node.identification, node.verification), (.8, .7))
        self.assertEqual(node.document.content, source)
        llm.chat.assert_not_called()


if __name__ == '__main__':
    unittest.main()
