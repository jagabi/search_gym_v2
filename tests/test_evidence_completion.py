"""Offline regressions for source handoff and draft-aware DepthSearch review."""
import unittest
from unittest.mock import AsyncMock, patch

from offline import FakeTools
from test_reader_integrity import FakeLLM, MemoryTrace, fetch_call, note
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.explorer import Budget, Document, Explorer, ExplorerConfig, _norm, _render_notes
from searchgym.llm import Reply, Usage
from searchgym.serving import profile_for


SOURCE = ("Title: PDF document\nMarkdown Content:\n[PDF page 1]\n"
          "Institution  Winners (2023)\nAlpha University  16\n"
          "Beta University  13\nGamma University  26")


class SourceHandoffTests(unittest.IsolatedAsyncioTestCase):
    async def read(self, content=SOURCE, *, enabled=True, config=None, budget=None, url=None):
        url = url or "https://source.example/table.pdf"
        llm = FakeLLM([note("Alpha University: 16. (Continue with all rows.)")])
        fetch = AsyncMock(side_effect=AssertionError("No extra fetch is allowed"))
        budget = budget or Budget(0)
        explorer = Explorer(llm, config or ExplorerConfig(max_depth=1), "Read", fetch,
                            preserve_source_evidence=enabled)
        result = await explorer.explore(question="Which universities satisfy both conditions?",
                                        reasoning="Parent guess: 999", query="universities",
                                        documents=[Document(url, content)], budget=budget,
                                        trace=MemoryTrace(), usage=Usage())
        self.assertEqual(len(llm.requests), 1)
        fetch.assert_not_awaited()
        return result, budget

    async def test_omitted_rows_survive_handoff_and_cache_without_model_rewrite(self):
        result, budget = await self.read()
        self.assertNotIn("Beta", result.log["own_information"])
        self.assertIn("Beta University  13", result.render_for_parent())
        self.assertIn("Winners (2023)", result.information)
        self.assertNotIn("999", result.information)
        cached = _render_notes(budget.readings[_norm("https://source.example/table.pdf")])
        self.assertIn("Gamma University  26", cached)
        self.assertGreater(result.log["source_evidence_chars"], 0)

    async def test_baseline_keeps_summary_only(self):
        result, _ = await self.read(enabled=False)
        self.assertNotIn("source_evidence", result.notes[0])
        self.assertNotIn("Beta University", result.information)
        self.assertNotIn("Source coverage notice", result.information)

    async def test_large_source_is_not_silently_prefix_copied(self):
        result, _ = await self.read(config=ExplorerConfig(max_depth=1, max_tokens=20))
        self.assertNotIn("source_evidence", result.notes[0])
        self.assertIn("exceeds the verbatim supplement limit", result.information)
        self.assertIn("Summary omissions do not establish absence", result.information)

    async def test_only_visible_source_is_preserved_and_truncation_is_explicit(self):
        result, _ = await self.read(SOURCE + "\n" + "unseen " * 100 + "SECRET_TAIL",
                                   config=ExplorerConfig(max_depth=1, max_document_tokens=75))
        self.assertNotIn("SECRET_TAIL", result.information)
        self.assertIn("unseen rows remain unknown", result.information)

    async def test_repeated_body_reports_no_progress_without_duplicating_raw_source(self):
        first, budget = await self.read()
        repeated, _ = await self.read(budget=budget, url="https://source.example/table.pdf?size=2000")
        self.assertIn("source_evidence", first.notes[0])
        self.assertNotIn("source_evidence", repeated.notes[0])
        self.assertIn("adds no new source rows", repeated.information)

    async def test_csv_and_markdown_tables_but_not_ordinary_prose(self):
        for source in ("Title: CSV document\nname,value\nBeta,13",
                       "Year 2023\n| Name | Value |\n| --- | --- |\n| Beta | 13 |"):
            result, _ = await self.read(source)
            self.assertIn(source, result.notes[0]["source_evidence"])
        result, _ = await self.read("An ordinary prose page.")
        self.assertNotIn("source_evidence", result.notes[0])

    async def test_child_source_survives_recursive_return(self):
        child = "https://source.example/table.pdf"
        llm = FakeLLM([note("An index links to the missing data."), fetch_call(child),
                       note("Alpha University: 16")])
        fetch = AsyncMock(return_value=Document(child, SOURCE))
        result = await Explorer(llm, ExplorerConfig(max_depth=2, max_subtree_children=1),
                                "Read", fetch, preserve_source_evidence=True).explore(
            question="Find universities", reasoning="", query="universities",
            documents=[Document("https://source.example/index", f"[data]({child})")],
            budget=Budget(1), trace=MemoryTrace(), usage=Usage())
        self.assertEqual(result.nodes, 1)
        self.assertIn("Beta University  13", result.information)
        self.assertNotIn("source_evidence", result.notes[0])
        self.assertIn("source_evidence", result.notes[1])
        self.assertEqual(len(llm.requests), 3)


class DraftReviewTests(unittest.IsolatedAsyncioTestCase):
    async def test_normal_review_preserves_draft_synthesis_and_tool_history(self):
        url = "https://source.example/data"
        llm = FakeLLM([fetch_call(url), note("A: 2; B: 1"),
                       Reply(text="A", reasoning="Adding the source rows gives A the largest total."),
                       Reply(text="A")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(finalize_answer=True),
                                method="depthsearch", explorer_config=ExplorerConfig(max_depth=1))
        result = await agent.run("Which group?", "Research", FakeTools(), MemoryTrace())
        messages, tools = llm.requests[-1]
        self.assertEqual(result.answer, "A")
        self.assertEqual(result.stop_reason, "finalized")
        self.assertIn("Draft answer:\nA", messages[-2]["content"])
        self.assertIn("Adding the source rows", messages[-2]["content"])
        self.assertTrue(any(m.get("tool_calls") for m in messages))
        self.assertTrue(any(m["role"] == "tool" for m in messages))
        self.assertIn("Correct unsupported claims", messages[-1]["content"])
        self.assertIsNone(tools)
        self.assertEqual(llm.tool_choices[-1], "none")
        self.assertFalse(llm.replies)

    async def test_failed_review_retains_valid_draft(self):
        llm = FakeLLM([Reply(text="A"), RuntimeError("offline failure")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(finalize_answer=True), method="depthsearch")
        result = await agent.run("Q", "Research", FakeTools(), MemoryTrace())
        self.assertEqual(result.answer, "A")
        self.assertEqual(result.stop_reason, "answered")

    async def test_malformed_output_uses_recovery_not_draft_review(self):
        llm = FakeLLM([Reply(), Reply(text="A")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(max_tool_recoveries=0), method="depthsearch")
        result = await agent.run("Q", "Research", FakeTools(), MemoryTrace())
        self.assertEqual(result.answer, "A")
        self.assertFalse(any(m["role"] == "assistant" for m in llm.requests[-1][0]))
        self.assertEqual(llm.tool_choices[-1], "none")

    async def test_baseline_finalization_is_unchanged(self):
        for method in ("ragent", "search-o1"):
            with self.subTest(method=method):
                llm = FakeLLM([Reply(text="OLD_DRAFT"), Reply(text="A")])
                with patch("searchgym.agent.LLM", return_value=llm):
                    agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(finalize_answer=True), method=method)
                result = await agent.run("Q", "Research", FakeTools(), MemoryTrace())
                self.assertEqual(result.answer, "A")
                self.assertNotIn("OLD_DRAFT", str(llm.requests[-1][0]))
                self.assertIsNone(llm.tool_choices[-1])


if __name__ == "__main__":
    unittest.main()
