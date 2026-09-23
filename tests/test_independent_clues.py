"""Offline integration: independent evidence seeds and scoped recursive checks."""
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from offline import FakeTools
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.explorer import ExplorerConfig, Document
from searchgym.llm import Reply
from searchgym.research_state import ResearchState
from searchgym.serving import profile_for
from test_reader_integrity import FakeLLM, MemoryTrace, note, fetch_call
from test_tool_availability import call


A = "https://archive.example/interview"
B = "https://report.example/tour"
C = "https://archive.example/person"


class ClueTools(FakeTools):
    async def search(self, query):
        self.searched.append(query)
        url = A if len(self.searched) == 1 else B
        value = {"organic": [{"link": url, "title": "interview" if url == A else "tour record",
                               "snippet": "ANCHOR_SECRET person N" if url == A else "TARGET_SECRET person N"}]}
        return value, SimpleNamespace(is_error=False, text=json.dumps(value), duration_ms=1)

    async def fetch(self, url):
        self.fetched.append(url)
        return Document(url, f"Record for person N. [Profile]({C})" if url == A else "Person N profile facts")


class IndependentClueTests(unittest.IsolatedAsyncioTestCase):
    def make(self, replies, **kwargs):
        llm = FakeLLM(replies)
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(
                depthsearch_control=True, independent_clues=True, **kwargs), "depthsearch",
                ExplorerConfig(max_depth=2, max_expansion_nodes=1, max_subtree_children=1,
                               extract_before_expand=True, isolate_extraction_context=True,
                               prune_unhelpful_branches=True, max_turns=2))
        return agent, llm

    def seeds(self):
        return [call("web_search", {"query": "IDENTITY_QUERY_SECRET"}),
                call("web_search", {"query": "target event record"})]

    async def test_blind_second_seed_then_merged_planning_without_controller_calls(self):
        agent, llm = self.make([*self.seeds(), fetch_call(A),
                               note("Person N\n**Expand:** no"), Reply(text="N")])
        trace, tools = MemoryTrace(), ClueTools()
        with patch.object(agent, "_control", side_effect=AssertionError("No auxiliary model calls")):
            result = await agent.run("Find a person's visit time.", "Research", tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, "N")
        self.assertEqual(result.usage.calls, 5)  # 2 seeds, main fetch, reader, main answer.
        self.assertEqual((result.searches, result.fetches, result.auto_fetches), (2, 1, 0))
        for forbidden in ("ANCHOR_SECRET", "IDENTITY_QUERY_SECRET", A):
            self.assertNotIn(forbidden, str(llm.requests[1][0]))
        merged = str(llm.requests[2][0])
        self.assertIn("ANCHOR_SECRET", merged)
        self.assertIn("TARGET_SECRET", merged)
        self.assertEqual({t["function"]["name"] for t in llm.requests[2][1]}, {"web_search", "web_fetch"})
        self.assertEqual(result.research_state.source(A)["origins"], [{"route": "A", "query": "IDENTITY_QUERY_SECRET"}])
        # Fetching an A source after search B retains the A source's task, not B's query.
        reader_input = str(llm.requests[3][0])
        self.assertIn("IDENTITY_QUERY_SECRET", reader_input)
        self.assertNotIn("target event record", reader_input)
        self.assertFalse(any(k == "control.request" for k, _ in trace.events))
        self.assertFalse(llm.replies)

    async def test_local_relation_reaches_child_without_parent_fact_contamination(self):
        fetch = fetch_call(A)
        fetch.text = "Check: Does this profile establish the person's birth country?"
        agent, llm = self.make([*self.seeds(), fetch,
            note("PARENT_FACT_SENTINEL\n**Expand:** yes"), fetch_call(C),
            note("Child states birth country\n**Expand:** no"), Reply(text="Answer")])
        trace, tools = MemoryTrace(), ClueTools()
        result = await agent.run("Find the person and country.", "Research", tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [A, C])
        self.assertEqual((result.expansion_nodes, result.max_depth_reached), (1, 2))
        extraction = [e for k, e in trace.events if k == "explorer.extract_input"]
        self.assertEqual(len(extraction), 2)
        self.assertIn("birth country", str(extraction[1]["messages"]))
        self.assertNotIn("PARENT_FACT_SENTINEL", str(extraction[1]["messages"]))
        self.assertEqual(result.research_state.source(C)["origins"][0]["route"], "A")
        self.assertFalse(result.research_state.source(C)["search_entry"])
        self.assertFalse(llm.replies)

    async def test_seed_batch_does_not_consume_second_independent_search(self):
        first = self.seeds()[0]
        first.tool_calls += call("web_search", {"query": "must not execute"}).tool_calls
        agent, llm = self.make([first, self.seeds()[1], Reply(text="Answer")])
        tools = ClueTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.searched, ["IDENTITY_QUERY_SECRET", "target event record"])
        self.assertTrue(result.tool_calls[1].refused)
        self.assertNotIn("IDENTITY_QUERY_SECRET", str(llm.requests[1][0]))

    async def test_search_exhaustion_uses_answer_only_and_one_empty_retry(self):
        agent, llm = self.make([*self.seeds(), Reply(text=""), Reply(text="Answer")], max_searches=2)
        result = await agent.run("Q", "Research", ClueTools(), MemoryTrace())
        self.assertEqual(result.answer, "Answer")
        self.assertEqual(result.searches, 2)
        self.assertEqual(llm.tool_choices[-2:], ["none", "none"])
        self.assertTrue(all(specs is None for _, specs in llm.requests[-2:]))
        self.assertIn("ANCHOR_SECRET", str(llm.requests[-1][0]))
        self.assertIn("TARGET_SECRET", str(llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_page_only_link_cannot_become_free_main_root(self):
        agent, llm = self.make([*self.seeds(), fetch_call(A),
            note(f"Useful next link: {C}\n**Expand:** no"), fetch_call(C), Reply(text="Answer")])
        tools = ClueTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [A])
        self.assertTrue(result.tool_calls[-1].refused)
        self.assertIn("recursive child", result.tool_calls[-1].result)
        self.assertFalse(llm.replies)

    async def test_origins_survive_cache_without_turning_url_overlap_into_proof(self):
        state = ResearchState()
        sid = state.register(A, search_entry=True, route="A", query="identity")
        self.assertEqual(state.register(A, search_entry=True, route="B", query="event"), sid)
        restored = ResearchState.from_snapshot(state.snapshot())
        self.assertEqual(len(restored.sources), 1)
        self.assertEqual([o["route"] for o in restored.source(A)["origins"]], ["A", "B"])
        self.assertFalse(restored.candidates)
        self.assertFalse(restored.draft)

    async def test_baselines_ignore_new_policy_even_when_flag_is_set(self):
        for method in ("ragent", "search-o1"):
            llm = FakeLLM([Reply(text="Answer")])
            with patch("searchgym.agent.LLM", return_value=llm):
                agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(independent_clues=True), method)
            trace = MemoryTrace()
            result = await agent.run("Q", "Research", ClueTools(), trace)
            self.assertIsNone(result.research_state)
            self.assertFalse(any(k == "research.seed_request" for k, _ in trace.events))
            self.assertEqual(result.answer, "Answer")
