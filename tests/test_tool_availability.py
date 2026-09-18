"""Offline tests of DepthSearch tool withdrawal; no external calls."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from offline import FakeTools
from test_reader_integrity import FakeLLM, MemoryTrace, note, fetch_call
from test_depthsearch_core import call
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.explorer import Budget, Document, Explorer, ExplorerConfig
from searchgym.llm import LLM, Reply, Usage
from searchgym.serving import profile_for


class AvailabilityTests(unittest.IsolatedAsyncioTestCase):
    async def test_search_exhaustion_keeps_fetch_then_final_has_no_tools(self):
        url = "https://a.example/source"
        llm = FakeLLM([call("web_search", {"query": "source"}), fetch_call(url),
                       note("A"), Reply(text="A"), Reply(text="A")])
        tools = FakeTools()
        tools.fetch = AsyncMock(return_value=Document(url, "A"))
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(
                max_searches=1, max_fetches=1, finalize_answer=True), method="depthsearch",
                explorer_config=ExplorerConfig(max_depth=1, max_expansion_nodes=0))
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertEqual((result.searches, result.fetches, result.answer), (1, 1, "A"))
        self.assertEqual([s["function"]["name"] for s in llm.requests[1][1]], ["web_fetch"])
        self.assertIn("web_search is exhausted", llm.requests[1][0][-1]["content"])
        self.assertIn("main fetch can still read", llm.requests[1][0][-1]["content"])
        # Extraction, no-tools main turn, and final synthesis all explicitly disable tools.
        self.assertEqual(llm.tool_choices[2:], ["none", "none", "none"])
        self.assertTrue(all(tools is None for _, tools in llm.requests[2:]))
        self.assertIsNone(result.error)
        self.assertFalse(llm.replies)

    async def test_fetch_exhaustion_keeps_search(self):
        url = "https://a.example/source"
        llm = FakeLLM([fetch_call(url), note("A"), call("web_search", {"query": "more"}), Reply(text="A")])
        tools = FakeTools()
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(max_fetches=1), method="depthsearch",
                                explorer_config=ExplorerConfig(max_depth=1))
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertEqual([s["function"]["name"] for s in llm.requests[2][1]], ["web_search"])
        self.assertEqual(result.searches, 1)
        self.assertIsNone(result.error)

    async def test_stale_and_batched_search_calls_cannot_exceed_limit(self):
        batch = call("web_search", {"query": "first"})
        batch.tool_calls += call("web_search", {"query": "extra"}).tool_calls
        llm = FakeLLM([batch, call("web_search", {"query": "stale"}), Reply(text="A")])
        tools, trace = FakeTools(), MemoryTrace()
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(max_searches=1), method="depthsearch")
        result = await agent.run("Q", "Research", tools, trace)
        self.assertEqual(tools.searched, ["first"])
        self.assertEqual(result.searches, 1)
        self.assertEqual(sum(k == "tool.unavailable" for k, _ in trace.events), 2)
        self.assertFalse(any(k == "budget.search_exhausted" for k, _ in trace.events))
        self.assertIsNone(result.error)

    async def test_expansion_exhaustion_returns_notes_without_another_navigation_call(self):
        child = "https://a.example/child"
        llm = FakeLLM([note("ROOT"), fetch_call(child), note("CHILD")])
        fetch = AsyncMock(return_value=Document(child, "CHILD"))
        result = await Explorer(llm, ExplorerConfig(max_depth=3, max_subtree_children=1),
                                "Read", fetch, enforce_tool_availability=True).explore(
            question="Q", reasoning="", query="Q", documents=[Document(
                "https://a.example/root", f"ROOT [child]({child})")],
            budget=Budget(1), trace=MemoryTrace(), usage=Usage())
        self.assertIn("ROOT", result.information)
        self.assertIn("CHILD", result.information)
        self.assertEqual(len(llm.requests), 3)
        self.assertEqual(llm.tool_choices, ["none", None, "none"])
        fetch.assert_awaited_once()

    async def test_baseline_requests_keep_existing_behavior(self):
        for method in ("ragent", "search-o1"):
            with self.subTest(method=method):
                llm = FakeLLM([call("web_search", {"query": "Q"}), Reply(text="A")])
                with patch("searchgym.agent.LLM", return_value=llm):
                    agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(max_searches=1), method=method)
                await agent.run("Q", "Research", FakeTools(), MemoryTrace())
                self.assertIn("web_search", [s["function"]["name"] for s in llm.requests[1][1]])
                self.assertNotIn("Current available actions", str(llm.requests))
                self.assertEqual(llm.tool_choices, [None, None])

    async def test_transport_none_omits_tools_and_defaults_are_unchanged(self):
        llm = LLM.__new__(LLM)
        llm.model_name = "offline"
        llm.profile = SimpleNamespace(sampling={}, sampling_extra={}, thinking_kwarg=False)
        llm._create = AsyncMock(return_value=SimpleNamespace(choices=[SimpleNamespace(
            message=SimpleNamespace(content="A", tool_calls=[]), finish_reason="stop")], usage=None))
        specs = [{"type": "function", "function": {"name": "web_search"}}]
        await llm.chat([], max_tokens=20, tools=specs, tool_choice="none")
        request = llm._create.call_args.args[0]
        self.assertEqual(request["tool_choice"], "none")
        self.assertNotIn("tools", request)
        await llm.chat([], max_tokens=20, tools=specs)
        self.assertEqual(llm._create.call_args.args[0]["tool_choice"], "auto")
        await llm.chat([], max_tokens=20)
        self.assertNotIn("tool_choice", llm._create.call_args.args[0])
