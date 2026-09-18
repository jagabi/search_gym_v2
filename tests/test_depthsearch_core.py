"""Offline regressions for CSV/PDF reading, recursion, tool limits and finalization."""
import io
import csv
import json
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from test_reader_integrity import FakeLLM, MemoryTrace, note, fetch_call
from offline import FakeTools
from searchgym.tools.native import decode_document, compact_pdf_text, file_kind
from searchgym.tools import WebTools
from searchgym.explorer import Budget, Document, Explorer, ExplorerConfig, _norm
from searchgym.agent import AgentConfig, RunResult, SearchAgent, Step, _looks_like_action, _clean_answer
from searchgym.llm import Reply, Usage, normalize_tool_names
from searchgym.serving import profile_for
from searchgym.config import load_test
from searchgym.urls import reader_failure


def call(name, args):
    return Reply(tool_calls=[SimpleNamespace(id="local", function=SimpleNamespace(
        name=name, arguments=json.dumps(args)))], finish_reason="tool_calls")


class SourceTests(unittest.TestCase):
    def test_csv_preserves_headers_empty_cells_zero_and_quoted_values(self):
        raw = 'Entity,2020,2021,Note\n"A, B",0,,"first\nsecond"\n'
        decoded = decode_document(raw.encode(), "csv", "https://a.example/data.csv")
        rows = list(csv.reader(io.StringIO(decoded.split("Markdown Content:\n", 1)[1])))
        self.assertEqual(rows, [["Entity", "2020", "2021", "Note"],
                                ["A, B", "0", "", "first\nsecond"]])

    def test_native_formats_are_limited_to_csv_and_pdf(self):
        for kind in ("csv", "pdf"):
            self.assertEqual(file_kind(f"https://a.example/file.{kind}?download=1"), kind)
        for kind in ("xls", "xlsx", "tsv"):
            self.assertEqual(file_kind(f"https://a.example/file.{kind}"), "")
            with self.assertRaisesRegex(ValueError, "Unsupported"):
                decode_document(b"irrelevant", kind, "https://a.example/file")

    def test_pdf_padding_is_removed_without_joining_rows_or_columns(self):
        text = " " * 400 + "Species" + " " * 500 + "Count\n\n\n"
        text += " " * 800 + "Example species" + " " * 500 + "12\n"
        self.assertEqual(compact_pdf_text(text), "Species  Count\n\nExample species  12")

    def test_protocol_residue_and_planning_are_not_short_answers(self):
        self.assertEqual(_clean_answer("to=...?...We need data. Let's try to fetch."), "")
        self.assertTrue(_looks_like_action("We need data. Let's try to fetch the source."))
        self.assertTrue(_looks_like_action("Hard to parse. I’ll produce partial results assuming the rest."))
        self.assertFalse(_looks_like_action("Norway"))
        self.assertEqual(_clean_answer("<|start|>assistant<|channel|>final<|message|>42<|end|>"), "42")

    def test_empty_pdf_is_explicit_failure(self):
        from pypdf import PdfWriter
        book = PdfWriter()
        book.add_blank_page(width=100, height=100)
        blob = io.BytesIO()
        book.write(blob)
        with self.assertRaisesRegex(ValueError, "OCR or vision"):
            decode_document(blob.getvalue(), "pdf", "https://a.example/p.pdf")
        self.assertIn("Empty source", reader_failure("Title: PDF\nURL Source: https://a.example\nMarkdown Content:\n"))


    def test_non_pdf_error_body_is_rejected_before_parsing(self):
        for payload in (b"----- access denied -----", b"<html>Not found</html>"):
            with patch("pypdf.PdfReader") as reader:
                with self.assertRaisesRegex(ValueError, "non-PDF body"):
                    decode_document(payload, "pdf", "https://a.example/file.pdf")
                reader.assert_not_called()


    def test_pdf_pages_and_tail_text_are_retained(self):
        from pypdf import PdfWriter
        from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
        book = PdfWriter()
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
        for text in ("First page", "Last page has target"):
            page = book.add_blank_page(width=600, height=800)
            page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
            stream = DecodedStreamObject()
            stream.set_data(f"BT /F1 12 Tf 50 700 Td ({text}) Tj ET".encode())
            page[NameObject("/Contents")] = stream
        blob = io.BytesIO()
        book.write(blob)
        text = decode_document(blob.getvalue(), "pdf", "https://a.example/doc.pdf")
        self.assertIn("[PDF page 2]", text)
        self.assertIn("Last page has target", text)


    def test_search_control_settings_are_unchanged(self):
        for method in ("depthsearch", "ragent", "search-o1"):
            cfg = load_test(method=method)
            self.assertEqual((cfg.agent.max_searches, cfg.agent.search_results), (10, 10))


    def test_protocol_normalization_is_conservative(self):
        specs = [{"function": {"name": "web_search"}}]
        for name in ("web_search]", "web_searchjson", "web_search<|channel|>json"):
            reply = call(name, {"query": "x"})
            self.assertEqual(normalize_tool_names(reply, specs)[0]["raw"], name)
            self.assertEqual(reply.tool_calls[0].function.name, "web_search")
        reply = call("web_search_other", {})
        self.assertFalse(normalize_tool_names(reply, specs))
        self.assertTrue(_looks_like_action("Great, we have the list. Now mean income. Let's fetch table."))
        self.assertFalse(_looks_like_action("The Open University"))


class FlowTests(unittest.IsolatedAsyncioTestCase):
    async def test_configured_depthsearch_exposes_only_web_tools(self):
        cfg = load_test(method="depthsearch")
        url = "https://a.example/record"
        llm = FakeLLM([fetch_call(url), note("Value: 42\n**Expand:** no"),
                       Reply(text="42"), Reply(text="42")])
        tools = FakeTools()
        tools.fetch = AsyncMock(return_value=Document(url, "Value: 42"))
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), cfg.agent, "depthsearch", cfg.explorer, cfg.explorer_prompt)
        result = await agent.run("What is the value?", cfg.system_prompt, tools, MemoryTrace())
        self.assertEqual(result.answer, "42")
        self.assertEqual({s["function"]["name"] for s in llm.requests[0][1]}, {"web_search", "web_fetch"})
        self.assertIsNone(llm.requests[1][1])  # Source extraction has no tools.
        self.assertIsNone(llm.requests[-1][1])  # Final synthesis has no tools.
        self.assertFalse(llm.replies)
        tools.fetch.assert_awaited_once()

    async def test_link_rich_index_can_reach_depth_three_and_keeps_source_notes(self):
        cfg = load_test(method="depthsearch").explorer
        budget, trace = Budget(cfg.max_expansion_nodes), MemoryTrace()
        item, detail = "https://a.example/item", "https://b.example/detail"
        llm = FakeLLM([
            note("PARENT INDEX ONLY\n**Next links:** " + item + "\n**Expand:** yes, target record", "not_found"),
            fetch_call(item),
            note("CHILD FIELD\n**Next links:** " + detail + "\n**Expand:** yes, missing measurement"),
            fetch_call(detail), note("LEAF VALUE: 42"), Reply(text="DONE"), Reply(text="DONE"),
        ])
        pages = {item: "CHILD FIELD. [measurement](" + detail + ")", detail: "LEAF VALUE: 42"}
        fetch = AsyncMock(side_effect=lambda url: Document(url, pages[url]))
        index = "PARENT INDEX ONLY\n[record](" + item + ")\n" + "\n".join(
            f"[other record {i}](https://a.example/other{i})" for i in range(20))
        result = await Explorer(llm, cfg, "Extract evidence", fetch).explore(
            question="Find the measurement.", reasoning="UNVERIFIED MAIN GUESS", query="measurement",
            documents=[Document("https://a.example/index", index)], budget=budget, trace=trace, usage=Usage())
        self.assertEqual(budget.nodes_by_depth, {2: 1, 3: 1})
        self.assertEqual((result.depth_reached, result.nodes, budget.remaining), (3, 2, 10))
        self.assertIsNone(budget.branch_ceiling)
        self.assertEqual(len(result.notes), 3)
        self.assertIn("LEAF VALUE: 42", result.information)
        for event, data in trace.events:
            if event == "explorer.extract_input" and data["depth"] > 1:
                self.assertNotIn("PARENT INDEX ONLY", json.dumps(data["messages"]))
                self.assertNotIn("UNVERIFIED MAIN GUESS", json.dumps(data["messages"]))
        self.assertFalse(llm.replies)
        self.assertIsNone(result.error)

    async def test_empty_final_output_gets_one_evidence_only_retry(self):
        llm = FakeLLM([Reply(text="Norway"), Reply(reasoning="ANALYSIS MUST NOT BE RECYCLED"), Reply(text="Norway")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(finalize_answer=True))
        result = await agent.run("Which country?", "Research", FakeTools(), MemoryTrace())
        self.assertEqual(result.answer, "Norway")
        self.assertEqual(result.stop_reason, "finalized")
        self.assertIsNone(llm.requests[-1][1])
        self.assertNotIn("ANALYSIS MUST NOT BE RECYCLED", json.dumps(llm.requests[-1][0]))
        self.assertEqual(len(llm.requests), 3)

    async def test_malformed_arguments_do_not_poison_history_or_consume_search(self):
        broken = call("web_search]", {})
        broken.tool_calls[0].function.arguments = '{"query":"x"}, "timeout":10000}'
        llm = FakeLLM([broken, call("web_search", {"query": "valid query"}), Reply(text="A")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig())
        tools = FakeTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertEqual(tools.searched, ["valid query"])
        self.assertEqual((result.searches, result.invalid_tool_calls), (1, 1))
        assistant = next(m for m in reversed(llm.requests[1][0]) if m.get("tool_calls"))
        self.assertEqual(assistant["tool_calls"][0]["function"]["arguments"], "{}")


    async def test_root_budget_reserves_nodes_for_other_sources(self):
        cfg = ExplorerConfig(max_depth=2, max_expansion_nodes=12, max_subtree_children=6,
                             max_root_nodes=2, max_turns=6)
        llm = FakeLLM([note("index"), fetch_call("https://a.example/1"), note("one"),
                       fetch_call("https://a.example/2"), note("two")])
        budget = Budget(12)
        explorer = Explorer(llm, cfg, "Extract", AsyncMock(side_effect=lambda u: Document(u, u)))
        await explorer.explore(question="Q", reasoning="", query="", documents=[Document("https://a.example", "index")],
                               budget=budget, trace=MemoryTrace(), usage=Usage())
        self.assertEqual((budget.used, budget.remaining), (2, 10))
        self.assertIsNone(budget.branch_ceiling)


    async def test_bad_native_search_names_execute_with_same_ten_call_limit(self):
        llm = FakeLLM([call("web_search]", {"query": f"q{i}"}) for i in range(11)] + [Reply(text="A")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig())
        tools = FakeTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertEqual(len(tools.searched), 10)
        self.assertEqual(result.searches, 10)
        self.assertEqual(result.invalid_tool_calls, 0)
        assistant = next(m for m in reversed(llm.requests[1][0]) if m.get("tool_calls"))
        self.assertEqual(assistant["tool_calls"][0]["function"]["name"], "web_search")


    async def test_final_stage_does_not_return_planned_action(self):
        llm = FakeLLM([Reply(text="Great, the list is here. Let's fetch table."), Reply(text="A, B")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(finalize_answer=True, max_tool_recoveries=0))
        result = await agent.run("Which names?", "Research", FakeTools(), MemoryTrace())
        self.assertEqual(result.answer, "A, B")
        self.assertIsNone(llm.requests[-1][1])
        self.assertNotIn("Let's fetch table", json.dumps(llm.requests[-1][0]))


    async def test_actual_finalization_keeps_short_draft_when_server_fails(self):
        llm = FakeLLM([Reply(text="Norway"), RuntimeError("server failed")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(finalize_answer=True))
        result = await agent.run("Which country?", "Research", FakeTools(), MemoryTrace())
        self.assertEqual(result.answer, "Norway")


    async def test_native_read_failure_falls_back_once_and_reports_empty_body(self):
        client = WebTools()
        client.call = AsyncMock(return_value=SimpleNamespace(text="Title: PDF\nMarkdown Content:\n", is_error=False))
        with patch("searchgym.tools.native.fetch_native", AsyncMock(side_effect=ValueError("image PDF"))):
            doc = await client.fetch("https://a.example/p.pdf")
        self.assertTrue(doc.is_error)
        self.assertEqual(doc.retrieval, "jina_fallback")
        client.call.assert_awaited_once()


