"""Offline policy regressions: entry breadth, local relations, source-only extraction."""
import json
import unittest
from unittest.mock import patch, AsyncMock

from searchgym.agent import AgentConfig, SearchAgent, RunResult, _FetchSession
from searchgym.explorer import (Explorer, ExplorerConfig, Document, Budget, _link_goals, _norm,
                                _access_only_documents, _first_note_route)
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
            note(f'CHILD_FACT_ONLY\n**Next links:**\n{leaf} | verify ORIGINAL_TITLE_RELATION\n**Expand:** yes'),
            note('Original title: Baby\n**Connections:** Book -> original title Baby\n**Expand:** no'),
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
        self.assertEqual(sum(k=='expand.from_note' for k,e in trace.events),2)
        self.assertEqual(sum(e.get('phase')=='recover' for k,e in trace.events if k=='explorer.response'),0)
        self.assertEqual(result.usage.calls,9)  # 3 extracts, 2 parent decisions, 2 entry, main + final.
        self.assertFalse(llm.replies)

    async def test_failed_document_metadata_survives_menu_refresh_and_returns_to_planner(self):
        class Failed(EntryTools):
            async def fetch(self,url):
                self.fetched.append(url)
                return Document(url,'403 Forbidden',is_error=True)
        agent,llm=self.make([call('web_search',{'query':'identified thesis'}),fetch_call('S1'),
            Reply(text='Identified document inaccessible; seek another copy.'),Reply(text='Answer')],max_searches=1)
        trace=MemoryTrace(); result=await agent.run('Q','Research',Failed(),trace)
        self.assertIsNone(result.error)
        requests=[e for k,e in trace.events if k=='control.request']
        payload=json.loads(requests[1]['messages'][1]['content'])
        failed=next(s for s in payload['sources'] if s['id']=='S1')
        self.assertEqual(failed['status'],'failed')
        self.assertTrue(failed['title'])
        self.assertTrue(failed['evidence'])
        self.assertIn('403',failed['access_error'])
        self.assertNotIn('S1',payload['selectable'])
        self.assertNotIn(URLS[0],requests[1]['tools'][0]['function']['parameters']['properties']['url']['enum'])
        self.assertIn('Document lead retained',str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_planner_and_entry_context_reach_navigation_but_not_extraction(self):
        search=call('web_search',{'query':'QUERY_UNVERIFIED_YEAR'})
        search.reasoning='PLANNER_CANDIDATE needs a release date; previous year was a guess.'
        fetch=fetch_call('S1');fetch.reasoning='ENTRY_PURPOSE verify candidate release date'
        agent,llm=self.make([search,fetch,note('Exact supplied fact\n**Expand:** yes'),
            Reply(text='DONE'),Reply(text='Local check done'),Reply(text='Answer')],max_searches=1)
        trace=MemoryTrace();result=await agent.run('Find a release date.','Research',EntryTools(),trace)
        self.assertIsNone(result.error)
        payload=json.loads(next(e for k,e in trace.events if k=='control.request')['messages'][1]['content'])
        self.assertIn('PLANNER_CANDIDATE',payload['planner_context_hypothesis'])
        extraction=next(e for k,e in trace.events if k=='explorer.extract_input')
        self.assertNotIn('PLANNER_CANDIDATE',str(extraction['messages']))
        self.assertNotIn('ENTRY_PURPOSE',str(extraction['messages']))
        navigation=next(e for k,e in trace.events if k=='explorer.input')
        self.assertIn('PLANNER_CANDIDATE',str(navigation['messages']))
        self.assertIn('ENTRY_PURPOSE',str(navigation['messages']))
        self.assertFalse(llm.replies)

    async def test_fused_first_link_then_parent_selects_second_child_with_purpose_fallback(self):
        root='https://site.example/root';one='https://site.example/one';two='https://site.example/two'
        second=fetch_call(two);second.reasoning='CHECK_SECOND_CONDITION'
        llm=FakeLLM([note(f'ROOT_FACT\n**Next links:**\n{one} | CHECK_FIRST_CONDITION\n**Expand:** yes'),
            note('FIRST_FACT\n**Expand:** no'),second,note('SECOND_FACT\n**Expand:** no')])
        pages={one:'First field',two:'Second field'}
        fetch=AsyncMock(side_effect=lambda url:Document(url,pages[url]))
        explorer=Explorer(llm,config(),'Read',fetch,relational_reading=True)
        trace=MemoryTrace();usage=Usage();budget=Budget(12)
        raw='Introduction\n\nDO_NOT_REREAD_RAW_BODY\n\nFirst field link\n[one]('+one+')\n\n[second]('+two+')'
        result=await explorer.explore(question='Q',reasoning='',reading_goal='LOCAL_PARENT_TASK',query='',
            documents=[Document(root,raw)],budget=budget,trace=trace,usage=usage)
        self.assertIsNone(result.error)
        self.assertEqual(fetch.await_count,2)
        self.assertEqual(result.nodes,2)
        self.assertEqual(usage.calls,4)  # Three extracts and one parent continuation.
        nav=[req for req,tools in llm.requests if tools]
        self.assertEqual(len(nav),1)
        self.assertIn('FIRST_FACT',str(nav[0]))
        self.assertNotIn('DO_NOT_REREAD_RAW_BODY',str(nav[0]))
        self.assertIn(two,str(nav[0]))
        self.assertIn('ROOT_FACT',result.information)
        self.assertIn('SECOND_FACT',result.information)
        tasks=[e for k,e in trace.events if k=='expand.relation_task']
        self.assertEqual(tasks[1]['fallback'],'parent_decision')
        self.assertEqual(tasks[1]['goal'],'CHECK_SECOND_CONDITION')
        extracts=[e for k,e in trace.events if k=='explorer.extract_input']
        self.assertNotIn('CHECK_SECOND_CONDITION',str(extracts[-1]['messages']))
        self.assertFalse(llm.replies)

    async def test_leaf_or_exhausted_budget_does_not_execute_note_route(self):
        for depth,limit in [(3,12),(1,0)]:
            llm=FakeLLM([note('FACT\n**Next links:**\nhttps://site.example/child | check date\n**Expand:** yes')])
            fetch=AsyncMock();trace=MemoryTrace()
            explorer=Explorer(llm,config(),'Read',fetch,relational_reading=True)
            result=await explorer.explore(question='Q',reasoning='',query='',depth=depth,
                documents=[Document('https://site.example/root','[child](https://site.example/child)')],
                budget=Budget(limit),trace=trace,usage=Usage())
            self.assertIsNone(result.error)
            fetch.assert_not_awaited()
            self.assertFalse(any(k=='expand.from_note' for k,e in trace.events))

    async def test_failed_note_route_refunds_budget_and_returns_control_with_saved_evidence(self):
        url='https://site.example/missing'
        llm=FakeLLM([note(f'FACT_BEFORE_FAILURE\n**Next links:**\n{url} | verify record\n**Expand:** yes'),
                     Reply(text='DONE')])
        fetch=AsyncMock(return_value=Document(url,'403 Forbidden',is_error=True))
        explorer=Explorer(llm,config(),'Read',fetch,relational_reading=True)
        budget=Budget(12);trace=MemoryTrace()
        result=await explorer.explore(question='Q',reasoning='',query='',
            documents=[Document('https://site.example/root',f'[record]({url})')],
            budget=budget,trace=trace,usage=Usage())
        self.assertIsNone(result.error)
        self.assertEqual(budget.used,0)
        self.assertIn('FACT_BEFORE_FAILURE',result.information)
        self.assertIn('403 Forbidden',result.information)
        self.assertIn('403 Forbidden',str(llm.requests[-1][0]))
        self.assertEqual(len(llm.requests),2)
        self.assertFalse(llm.replies)

    async def test_unmatched_note_link_uses_ordinary_navigation(self):
        llm=FakeLLM([note('FACT\n**Next links:**\nhttps://unobserved.example/record | date\n**Expand:** yes'),
                     Reply(text='DONE')])
        fetch=AsyncMock();trace=MemoryTrace()
        explorer=Explorer(llm,config(),'Read',fetch,relational_reading=True)
        result=await explorer.explore(question='Q',reasoning='',query='',
            documents=[Document(URLS[0],'Fact on current page')],budget=Budget(12),trace=trace,usage=Usage())
        self.assertIsNone(result.error)
        fetch.assert_not_awaited()
        self.assertTrue(llm.requests[-1][1])
        self.assertFalse(any(k=='expand.from_note' for k,e in trace.events))
        self.assertFalse(llm.replies)

    async def test_recognized_access_screen_skips_model_and_recursion(self):
        page='Title: 18+ Access\nMarkdown Content:\n18+ ONLY\nContinue to Access\nPlease confirm you are over 18 years old.\nCONTINUE 18+ VERIFIED\n[Leave](https://google.com/)\nLoading'
        llm=FakeLLM([]);fetch=AsyncMock();trace=MemoryTrace();usage=Usage()
        explorer=Explorer(llm,config(),'Read',fetch,relational_reading=True)
        result=await explorer.explore(question='Q',reasoning='',query='',
            documents=[Document(URLS[0],page)],budget=Budget(12),trace=trace,usage=usage)
        self.assertIsNone(result.error)
        self.assertEqual(result.status,'not_found')
        self.assertEqual(usage.calls,0)
        fetch.assert_not_awaited()
        self.assertTrue(any(k=='explorer.access_only' for k,e in trace.events))

    def test_access_screen_detection_never_discards_article_or_unknown_body(self):
        for page in ['Title: Article\nMarkdown Content:\n18+ Access is a website title.',
                     'Title: 18+ Access\nMarkdown Content:\nLoading\nAuthor: Real Person',
                     'Title: 18+ Access\nMarkdown Content:\n[Real record](https://site.example/record)']:
            self.assertFalse(_access_only_documents([Document(URLS[0],page)]))

    def test_ambiguous_or_unobserved_first_route_requires_navigation(self):
        budget=Budget(12);budget.visit('https://site.example/root')
        for note_text in ['**Next links:**\nhttps://other.example/a | check date',
                          '**Next links:**\nhttps://site.example/a and https://site.example/b | dates',
                          '**Next links:**\nhttps://site.example/a']:
            self.assertIsNone(_first_note_route(note_text,{},budget))

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
