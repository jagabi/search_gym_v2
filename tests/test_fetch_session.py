"""Offline checks for adaptive entry reading; no model or network calls."""
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from searchgym.agent import AgentConfig, RunResult, SearchAgent
from searchgym.explorer import Document, ExplorerConfig
from searchgym.llm import Reply
from searchgym.research_state import ResearchState, SELECT_FETCH_TOOL
from searchgym.serving import profile_for
from test_reader_integrity import FakeLLM, MemoryTrace, fetch_call, note
from test_tool_availability import call
from offline import FakeTools


URLS = [f"https://source.example/Record{i}" for i in range(4)]


class EntryTools(FakeTools):
    async def search(self, query):
        self.searched.append(query)
        data = {"organic": [{"link": u, "title": f"Record {i}", "snippet": f"Clue {i}"}
                            for i, u in enumerate(URLS)]}
        return data, SimpleNamespace(is_error=False, duration_ms=1, text=json.dumps(data))

    async def fetch(self, url):
        self.fetched.append(url)
        return Document(url, f"Evidence from {url}")


class FetchSessionTests(unittest.IsolatedAsyncioTestCase):
    def make(self, replies, **kwargs):
        llm = FakeLLM(replies)
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(depthsearch_control=True, **kwargs),
                                method="depthsearch", explorer_config=ExplorerConfig(
                                    max_depth=3, max_expansion_nodes=0, max_subtree_children=2,
                                    max_turns=6, extract_before_expand=True))
        return agent, llm

    def reading(self, index):
        return [fetch_call(URLS[index]), note(f"Evidence {index}\n**Expand:** no"),
                Reply(text='{"candidates":[]}')]

    async def test_three_roots_ignore_child_cap_and_exhausted_nodes_then_return_to_main(self):
        agent, llm = self.make([call("web_search", {"query": "specific relation"}),
            *self.reading(0), *self.reading(1), *self.reading(2), Reply(text="Enough evidence."),
            Reply(text="Answer")])
        tools, trace = EntryTools(), MemoryTrace()
        result = await agent.run("Question", "Research", tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, "Answer")
        self.assertEqual(tools.fetched, URLS[:3])
        self.assertEqual((result.searches, result.auto_fetches, result.expansion_nodes), (1, 3, 0))
        self.assertEqual(result.max_depth_reached, 1)
        requests = [e for k, e in trace.events if k == "control.request" and e["mode"] == "select"]
        self.assertEqual(len(requests), 4)
        third = requests[2]["messages"]
        self.assertEqual([m["role"] for m in third], ["system", "user", "assistant", "tool", "assistant", "tool"])
        self.assertIn("Evidence 0", third[3]["content"])
        self.assertIn("Evidence 1", third[5]["content"])
        payload = json.loads(third[1]["content"])
        self.assertEqual(payload["current_query"], "specific relation")
        self.assertNotIn("sources", payload["working_state"])
        enum = requests[2]["tools"][0]["function"]["parameters"]["properties"]["url"]["enum"]
        self.assertEqual(enum, URLS[2:])
        self.assertNotIn("enum", SELECT_FETCH_TOOL["function"]["parameters"]["properties"]["url"])
        self.assertIn("Evidence 2", result.steps[0].tool_calls[0].result)
        self.assertFalse(llm.replies)

    async def test_invalid_selection_gets_tool_feedback_and_can_recover(self):
        agent, llm = self.make([call("web_search", {"query": "clue"}),
            fetch_call("https://google.com/search?q=clue"), *self.reading(0),
            Reply(text="Return to planner."), Reply(text="Answer")], max_tool_recoveries=2)
        tools, trace = EntryTools(), MemoryTrace()
        result = await agent.run("Q", "Research", tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, URLS[:1])
        self.assertEqual(result.searches, 1)
        self.assertEqual(result.research_state.metrics["selector_recoveries"], 1)
        self.assertEqual(llm.requests[2][0][-1]["role"], "tool")
        self.assertIn("No page was fetched", llm.requests[2][0][-1]["content"])
        self.assertFalse(llm.replies)

    async def test_invalid_retry_is_bounded_and_retains_search_results(self):
        agent, llm = self.make([call("web_search", {"query": "clue"}),
            *[fetch_call("https://unlisted.example") for _ in range(3)], Reply(text="Answer")],
            max_tool_recoveries=2)
        tools = EntryTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [])
        self.assertEqual(result.research_state.metrics["controller_invalid"], 3)
        self.assertIn("Clue 0", result.steps[0].tool_calls[0].result)
        self.assertFalse(llm.replies)

    async def test_failed_page_is_removed_and_next_entry_can_be_read(self):
        class FailingTools(EntryTools):
            async def fetch(self, url):
                if url == URLS[0]:
                    self.fetched.append(url)
                    return Document(url, "HTTP 404", is_error=True)
                return await super().fetch(url)
        agent, llm = self.make([call("web_search", {"query": "clue"}), fetch_call(URLS[0]),
            *self.reading(1), Reply(text="Done"), Reply(text="Answer")])
        tools = FailingTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(result.research_state.source(URLS[0])["status"], "failed")
        self.assertNotIn(URLS[0], llm.requests[2][1][0]["function"]["parameters"]["properties"]["url"]["enum"])
        self.assertEqual(tools.fetched, URLS[:2])
        self.assertFalse(llm.replies)

    async def test_fetch_cap_stops_loop_and_last_search_calls_answer_phase(self):
        agent, llm = self.make([call("web_search", {"query": "clue"}), *self.reading(0),
                               Reply(text="Answer")], max_fetches=1, max_searches=1)
        result = await agent.run("Q", "Research", EntryTools(), MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(result.auto_fetches, 1)
        self.assertEqual(llm.tool_choices[-1], "none")
        self.assertIsNone(llm.requests[-1][1])
        self.assertEqual(result.answer, "Answer")
        self.assertFalse(llm.replies)

    async def test_entry_session_preserves_recursion_and_can_read_next_root_after_node_exhaustion(self):
        child = "https://source.example/child"
        class LinkedTools(EntryTools):
            async def fetch(self, url):
                self.fetched.append(url)
                return Document(url, "Parent evidence " + f"[child]({child})" if url == URLS[0] else "Other evidence")
        agent, llm = self.make([call("web_search", {"query": "clue"}), fetch_call(URLS[0]),
            note(f"Parent evidence\n**Next links:** {child}\n**Expand:** yes"), fetch_call(child),
            note("Child evidence"), Reply(text='{"candidates":[]}'), *self.reading(1),
            Reply(text="Done"), Reply(text="Answer")])
        agent.explorer_config.max_expansion_nodes = 1
        tools = LinkedTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [URLS[0], child, URLS[1]])
        self.assertEqual((result.auto_fetches, result.expansion_nodes, result.max_depth_reached), (2, 1, 2))
        self.assertIn("Child evidence", result.steps[0].tool_calls[0].result)
        self.assertFalse(llm.replies)

    async def test_turn_limit_keeps_last_read_and_returns_to_main(self):
        agent, llm = self.make([call("web_search", {"query": "clue"}), *self.reading(0),
            *self.reading(1), Reply(text="Answer")])
        agent.explorer_config.max_turns = 2
        trace = MemoryTrace()
        result = await agent.run("Q", "Research", EntryTools(), trace)
        self.assertEqual(result.answer, "Answer")
        self.assertIn("Evidence 1", result.steps[0].tool_calls[0].result)
        self.assertIn(("search.entry_session_end", {"turn": 1, "reason": "turn_limit", "recoveries": 0}), trace.events)
        self.assertFalse(llm.replies)

    async def test_previous_unread_menu_keeps_snippet_and_page_links_cannot_be_free_roots(self):
        state = ResearchState()
        old = state.register(URLS[0], snippet="DUPLICATE_OBSERVATION_SENTINEL", search_entry=True)
        state.register(URLS[0], snippet="RECENT_SNIPPET_SENTINEL", search_entry=True)
        fresh = state.register(URLS[1], snippet="Fresh clue", search_entry=True)
        link = state.register(URLS[2], title="Page-only link")
        state.register(URLS[3], search_entry=True)
        state.mark_failed(URLS[3], "404")
        agent, llm = self.make([Reply(text="Done")])
        await agent._control("Q", RunResult(research_state=state), MemoryTrace(), [fresh], select=True)
        payload = json.loads(llm.requests[0][0][1]["content"])
        self.assertEqual(payload["selectable"], [old, fresh])
        self.assertEqual([s["id"] for s in payload["previous_sources"]], [old])
        self.assertIn("RECENT_SNIPPET_SENTINEL", payload["previous_sources"][0]["evidence"])
        self.assertNotIn("DUPLICATE_OBSERVATION_SENTINEL", str(llm.requests))
        self.assertIn("Fresh clue", payload["sources"][0]["evidence"])
        self.assertNotIn(link, payload["selectable"])
        # A page link becomes a legitimate root only if a real search later returns it.
        state.register(URLS[2], search_entry=True)
        self.assertIn(link, state.selectable())
