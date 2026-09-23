"""Offline policy regressions: entry breadth, local relations, source-only extraction."""
import json
import unittest
from unittest.mock import patch, AsyncMock

from searchgym.agent import AgentConfig, SearchAgent, RunResult, _FetchSession
from searchgym.explorer import Explorer, ExplorerConfig, Document, Budget, _link_goals, _norm
from searchgym.llm import Reply, Usage
from searchgym.research_state import ResearchState
from searchgym.serving import profile_for
from test_reader_integrity import FakeLLM, MemoryTrace, note, fetch_call
from test_fetch_session import EntryTools, URLS
from test_tool_availability import call


def config(**overrides):
    return ExplorerConfig(**dict(dict(max_depth=3, max_expansion_nodes=12, max_subtree_children=2,
        max_root_nodes=6, max_turns=6, extract_before_expand=True,
        isolate_extraction_context=True, prune_unhelpful_branches=True), **overrides))


class RelationalReadingTests(unittest.IsolatedAsyncioTestCase):
    def make(self, replies, **overrides):
        llm = FakeLLM(replies)
        with patch('searchgym.agent.LLM', return_value=llm):
            agent = SearchAgent(profile_for('gpt-oss'), AgentConfig(
                depthsearch_control=True, relational_reading=True, **overrides),
                'depthsearch', config(), 'Read supplied source evidence.')
        return agent, llm

    async def test_three_siblings_before_main_no_state_update_and_final_search_read(self):
        replies = [call('web_search', {'query': 'candidate record'})]
        for i in range(3):
            replies += [fetch_call(f'S{i+1}'), note(f'Evidence {i}\n**Connections:** A -> B{i}\n**Missing:** date\n**Expand:** no')]
        replies += [Reply(text='Three source connections established; date remains unknown.'), Reply(text='Answer')]
        agent,llm=self.make(replies,max_searches=1)
        tools,trace=EntryTools(),MemoryTrace()
        result=await agent.run('Question','Research',tools,trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer,'Answer')
        self.assertEqual(tools.fetched,URLS[:3])
        self.assertEqual((result.searches,result.auto_fetches,result.expansion_nodes),(1,3,0))
        requests=[e for k,e in trace.events if k=='control.request']
        self.assertTrue(all(e['mode']=='select' for e in requests))
        self.assertEqual(len(requests),4)
        self.assertEqual(result.usage.calls,9)  # main search + 4 entry turns + 3 extracts + final.
        self.assertNotIn('working_state',json.loads(requests[0]['messages'][1]['content']))
        self.assertIn('Evidence 0',str(llm.requests[-1][0]))
        self.assertIn('Three source connections established',str(llm.requests[-1][0]))
        self.assertEqual(llm.tool_choices[-1],'none')
        self.assertFalse(llm.replies)

    async def test_child_relation_is_navigation_only_and_leaf_returns_to_parent(self):
        child,leaf='https://source.example/book','https://source.example/edition'
        pages={URLS[0]:f'Author profile [Book]({child})',child:f'Book record [Edition]({leaf})',leaf:'Original title: Baby'}
        class Linked(EntryTools):
            async def fetch(self,url):
                self.fetched.append(url); return Document(url,pages[url])
        agent,llm=self.make([
            call('web_search',{'query':'QUERY_YEAR_2015'}),fetch_call(URLS[0]),
            note(f'PARENT_FACT_ONLY\n**Next links:**\n{child} | verify FIRST_BOOK_RELATION\n**Expand:** yes'),
            fetch_call(child),
            note(f'CHILD_FACT_ONLY\n**Next links:**\n{leaf} | verify ORIGINAL_TITLE_RELATION\n**Expand:** yes'),
            fetch_call(leaf),note('Original title: Baby\n**Connections:** Book -> original title Baby\n**Expand:** no'),
            Reply(text='DONE'),Reply(text='DONE'),Reply(text='Book relation complete'),Reply(text='Baby')])
        trace,tools=MemoryTrace(),Linked()
        result=await agent.run('Find the author and original title.','Research',tools,trace)
        self.assertIsNone(result.error)
        self.assertEqual((result.expansion_nodes,result.max_depth_reached),(2,3))
        extraction=[e for k,e in trace.events if k=='explorer.extract_input']
        for e in extraction:
            self.assertNotIn('QUERY_YEAR_2015',str(e['messages']))
            self.assertNotIn('FIRST_BOOK_RELATION',str(e['messages']))
            self.assertNotIn('ORIGINAL_TITLE_RELATION',str(e['messages']))
        self.assertNotIn('PARENT_FACT_ONLY',str(extraction[1]['messages']))
        navigation=[e for k,e in trace.events if k=='explorer.input']
        self.assertIn('FIRST_BOOK_RELATION',str(navigation[1]['messages']))
        self.assertIn('ORIGINAL_TITLE_RELATION',str(navigation[2]['messages']))
        self.assertNotIn('FIRST_BOOK_RELATION',str(navigation[2]['messages']))
        self.assertIn('Book -> original title Baby',str(llm.requests[-1][0]))
        self.assertTrue(all(e['mode']=='select' for k,e in trace.events if k=='control.request'))
        self.assertFalse(llm.replies)

    async def test_identical_root_content_skips_extraction_and_marks_alias_read(self):
        class Mirrors(EntryTools):
            async def fetch(self,url):
                self.fetched.append(url)
                return Document(url,f'Title: Record\nURL Source: {url}\nMarkdown Content:\nIdentical exact record')
        agent,llm=self.make([call('web_search',{'query':'record'}),fetch_call(URLS[0]),
            note('Fact retained\n**Expand:** no'),fetch_call(URLS[1]),Reply(text='DONE'),Reply(text='Answer')])
        trace=MemoryTrace(); result=await agent.run('Q','Research',Mirrors(),trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.explorer_calls,1)
        self.assertEqual(result.research_state.source(URLS[1])['status'],'read')
        reused=[e for k,e in trace.events if k=='explorer.reused_content']
        self.assertEqual(reused[0]['original_sources'],URLS[:1])
        self.assertIn('not independent corroboration',result.steps[0].tool_calls[0].result)
        self.assertFalse(llm.replies)

    async def test_entry_context_is_scoped_and_invalid_call_can_recover(self):
        agent,llm=self.make([fetch_call('https://invented.example'),fetch_call('S2')])
        state=ResearchState()
        state.register('https://old.example',snippet='OLD_UNRELATED_CONTEXT',search_entry=True)
        sid=state.register(URLS[0],snippet='current record',search_entry=True)
        result=RunResult(research_state=state);session=_FetchSession();trace=MemoryTrace()
        first=await agent._control('Q',result,trace,[sid],select=True,session=session,query='query')
        second=await agent._control('Q',result,trace,[sid],select=True,session=session,query='query')
        self.assertIsNone(first);self.assertEqual(second,sid)
        self.assertNotIn('OLD_UNRELATED_CONTEXT',str(llm.requests))
        self.assertIn('No page was fetched',str(llm.requests[1][0]))

    async def test_no_useful_entries_returns_to_main_and_new_search(self):
        agent,llm=self.make([call('web_search',{'query':'first'}),Reply(text='No useful route'),
            call('web_search',{'query':'different relation'}),fetch_call(URLS[0]),
            note('Useful fact\n**Expand:** no'),Reply(text='DONE'),Reply(text='Answer')])
        tools=EntryTools();result=await agent.run('Q','Research',tools,MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.searched,['first','different relation'])
        self.assertFalse(llm.replies)

    async def test_same_content_child_refunds_node_and_keeps_original_source(self):
        url='https://source.example/original'; alias='https://source.example/mirror'
        llm=FakeLLM([note('Exact fact\n**Expand:** no')]);budget=Budget(3);trace=MemoryTrace()
        fetch=AsyncMock(return_value=Document(alias,'Identical body'))
        explorer=Explorer(llm,config(),'Read',fetch,relational_reading=True)
        await explorer.explore(question='Q',reasoning='',query='',documents=[Document(url,'Identical body')],
            budget=budget,trace=trace,usage=Usage())
        _,child=await explorer._open(call=fetch_call(alias).tool_calls[0],question='Q',reasoning='',
            reasoning_now='',query='',budget=budget,trace=trace,usage=Usage(),depth=1,turn=1,
            allowed=2,openable={_norm(alias):alias},link_goals={_norm(alias):'verify fact'})
        self.assertTrue(child.reused);self.assertEqual(budget.used,0)
        self.assertEqual(budget.nodes_by_depth,{})
        self.assertEqual(child.sources,[url]);self.assertEqual(len(llm.requests),1)

    async def test_extraction_failure_is_not_cached(self):
        llm=FakeLLM([Reply(text=''),Reply(text=''),note('Recovered evidence\n**Expand:** no')])
        explorer=Explorer(llm,config(max_depth=1),'Read',AsyncMock(),relational_reading=True)
        budget=Budget(0)
        for i in range(2):
            result=await explorer.explore(question='Q',reasoning='',query='',documents=[Document(URLS[i],'Same body')],
                budget=budget,trace=MemoryTrace(),usage=Usage())
        self.assertFalse(result.reused)
        self.assertIn('Recovered evidence',result.information)
        self.assertEqual(len(llm.requests),3)

    def test_next_link_purpose_matches_url_not_neighbor_or_coverage(self):
        text=f'**Coverage:** year 2015\n**Next links:**\n| URL | Missing relation |\n| {URLS[0]} | first book |\n| [record]({URLS[1]}) | original title |\n**Missing:** OTHER_SENTINEL'
        goals=_link_goals(text)
        self.assertIn('first book',goals[_norm(URLS[0])])
        self.assertIn('original title',goals[_norm(URLS[1])])
        self.assertNotIn('OTHER_SENTINEL',str(goals))
        self.assertEqual(_link_goals('No formatted next links'),{})
