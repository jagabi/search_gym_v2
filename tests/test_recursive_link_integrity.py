"""Source URL integrity for DS recursion, with baseline parsing left unchanged."""
import unittest
from unittest.mock import AsyncMock

from searchgym.explorer import (Budget, Document, Explorer, _page_links, _link_menu,
                               _strip_visited_links, _link_goals)
from searchgym.llm import Reply, Usage
from test_reader_integrity import FakeLLM, MemoryTrace, note
from test_relational_reading import config


class LinkIntegrityTests(unittest.IsolatedAsyncioTestCase):
    def test_parentheses_survive_markdown_bare_angle_and_nested_forms(self):
        for url in ['https://example.org/Film_(1994)', 'https://example.org/A_(B_(C))',
                    'https://example.org/Film_(1994)?edition=2#cast']:
            for text in [url, f'[Record]({url})', f'[Record]({url}),next', f'[Record](<{url}> "Title")',
                         f'See ({url}).', f'`{url}`']:
                links=_page_links(text,balanced=True)
                self.assertEqual(list(links.values()),[url],text)

    def test_menu_and_note_route_share_the_exact_url(self):
        url='https://example.org/Record_(book)'
        menu=_link_menu(f'[Record]({url})',Budget(12),'Record','book',30,balanced=True)
        self.assertEqual(menu,[('Record',url)])
        self.assertEqual(_link_goals(f'**Next links:**\n{url} | verify publication'),{url:'verify publication'})

    def test_visited_link_removal_keeps_anchor_and_surrounding_text(self):
        url='https://example.org/Record_(book)';budget=Budget(12);budget.visit(url)
        text=f'Before [Record]({url}) after [Other](https://example.org/Other_(book)).'
        out,count=_strip_visited_links(text,budget,balanced=True)
        self.assertEqual(count,1)
        self.assertEqual(out,'Before Record after [Other](https://example.org/Other_(book)).')

    def test_legacy_parser_is_unchanged(self):
        url='https://example.org/Record_(book)'
        self.assertEqual(list(_page_links(url).values()),[url[:-1]])

    async def test_first_note_route_fetches_the_supplied_destination_without_damage(self):
        root='https://example.org/index';child='https://other.example/Record_(book)'
        llm=FakeLLM([note(f'INDEX\n**Next links:**\n{child} | publication\n**Expand:** yes'),
                     note('Exact publication\n**Expand:** no'),Reply(text='DONE')])
        fetch=AsyncMock(return_value=Document(child,'Publication record'))
        reader=Explorer(llm,config(),'Read',fetch,relational_reading=True)
        trace=MemoryTrace();result=await reader.explore(question='Publication?',reasoning='',query='',
            documents=[Document(root,f'[Record]({child})')],budget=Budget(12),trace=trace,usage=Usage())
        self.assertIsNone(result.error)
        fetch.assert_awaited_once_with(child)
        self.assertIn('Exact publication',result.information)
        self.assertTrue(any(k=='expand.from_note' and e['url']==child for k,e in trace.events))
