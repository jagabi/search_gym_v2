"""Offline regressions for evidence loss, recursion, recovery and evaluation.

Run: python -m unittest discover -s tests -p test_reader_integrity.py -v
All model, fetch and judge responses are local fakes; no API calls are made.
"""

import copy
import json
import unittest
import tempfile
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from searchgym.agent import AgentConfig, RunResult, SearchAgent, Step, _looks_like_action, _clean_answer
from searchgym.config import load_test
from searchgym.explorer import (Budget, Document, Explorer, ExplorerConfig, _parse_final, _norm,
                                _parse_expansion_decision)
from searchgym.llm import Reply, Usage, recover_tool_calls
from searchgym.runner import _agent_fingerprint, _explorer_fingerprint, _result_from
from searchgym.runner import Runner
from searchgym.benchmarks import load_benchmark
from searchgym.report import summarize
from searchgym.scoring import Judgement, aggregate
from searchgym.serving import profile_for
from searchgym.trace import NullTrace
from searchgym.urls import normalize_fetch_url, reader_failure


def note(text, status="partial"):
    return Reply(text=f"**Final Information**\n{text}\n**Status:** {status}", finish_reason="stop")


def fetch_call(url):
    return Reply(tool_calls=[SimpleNamespace(
        id="call", function=SimpleNamespace(name="web_fetch", arguments=json.dumps({"url": url}))
    )], reasoning="The page links to the missing measurement.", finish_reason="tool_calls")


class MemoryTrace(NullTrace):
    def __init__(self):
        super().__init__()
        self.events = []

    def event(self, kind, **fields):
        self.events.append((kind, copy.deepcopy(fields)))


class FakeLLM:
    profile = SimpleNamespace(reasoning_effort="")
    model_name = "offline"

    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []
        self.tool_choices = []

    async def chat(self, messages, *, max_tokens, tools=None, usage=None, tool_choice=None):
        self.requests.append((copy.deepcopy(messages), tools))
        self.tool_choices.append(tool_choice)
        if not self.replies:
            raise AssertionError("Unexpected model call")
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if usage is not None:
            usage.add(100, 20)
        return reply

    async def count_tokens(self, text):
        return max(1, len(text) // 3)

    async def cap(self, text, limit_tokens):
        return text[:limit_tokens * 3], len(text) > limit_tokens * 3

    async def aclose(self):
        pass


class ReaderTests(unittest.IsolatedAsyncioTestCase):
    async def read(self, replies, config=None, documents=None):
        llm, trace, budget = FakeLLM(replies), MemoryTrace(), Budget(4)
        fetched = []

        async def fetch(url):
            fetched.append(url)
            return Document(url, "Child page: signed on 6 February 1840.")

        explorer = Explorer(llm, config or ExplorerConfig(max_depth=1), "Read evidence.", fetch)
        result = await explorer.explore(
            question="Find date and place.", reasoning="Unverified hypothesis: 1900.",
            query="date", documents=documents or [Document(
                "https://a.example/root", "Place: London. [register](https://b.example/register)"
            )], budget=budget, trace=trace, usage=Usage(),
        )
        self.assertFalse(llm.replies, "Scripted calls were not consumed")
        return result, llm, trace, budget, fetched

    async def test_leaf_recovers_reasoning_only_output(self):
        result, llm, trace, _, fetched = await self.read([
            Reply(reasoning="I can see the date.", finish_reason="stop"), note("Date: 1840")
        ])
        self.assertIn("1840", result.information)
        self.assertEqual(result.extraction_state, "complete")
        self.assertEqual(result.log["recovery_attempts"], 1)
        self.assertTrue(all(not tools for _, tools in llm.requests))
        self.assertEqual(len([e for e in trace.events if e[0] == "explorer.response"]), 2)
        self.assertEqual(fetched, [])

    async def test_empty_reader_is_not_reported_as_no_evidence(self):
        result, *_ = await self.read([Reply(), Reply()])
        self.assertEqual(result.extraction_state, "empty_output")
        self.assertIn("does not mean", result.render_for_gate())
        self.assertNotIn("No relevant evidence", result.render_for_gate())

    async def test_truncated_evidence_survives_failed_recovery(self):
        result, *_ = await self.read([Reply(text="Date: 1840", finish_reason="length"), Reply()])
        self.assertIn("1840", result.information)
        self.assertEqual(result.extraction_state, "truncated")

    async def test_network_error_retries_locally_and_preserves_state(self):
        result, *_ = await self.read([RuntimeError("offline simulated failure"), note("Date: 1840")])
        self.assertEqual(result.extraction_state, "complete")

    async def test_parent_and_child_survive_empty_navigation_reply(self):
        config = ExplorerConfig(max_depth=2, max_expansion_nodes=4,
                                max_subtree_children=2, max_turns=4)
        result, llm, _, budget, fetched = await self.read([
            note("Place: London"), fetch_call("https://b.example/register"),
            note("Date: 6 February 1840"), Reply(),
        ], config)
        self.assertIn("Place: London", result.information)
        self.assertIn("Date: 6 February 1840", result.information)
        self.assertEqual(result.nodes, 1)
        self.assertEqual(budget.used, 1)
        self.assertEqual(result.depth_reached, 2)
        self.assertEqual(fetched, ["https://b.example/register"])
        child_input = llm.requests[2][0][1]["content"]
        self.assertIn("Place: London", child_input)
        self.assertIn("parent page", child_input)
        self.assertEqual(result.calls, 2)

    async def test_reused_child_keeps_notes_without_charging_another_node(self):
        config = ExplorerConfig(max_depth=2, max_expansion_nodes=4,
                                max_subtree_children=2, max_turns=4)
        result, _, _, budget, fetched = await self.read([
            note("Place: London"), fetch_call("https://b.example/register"), note("Date: 1840"),
            fetch_call("https://b.example/register"), Reply(text="DONE"),
        ], config)
        self.assertEqual(len(fetched), 1)
        self.assertEqual((result.nodes, budget.used, budget.reused), (1, 1, 1))
        self.assertEqual(result.information.count("Date: 1840"), 1)

    async def test_same_site_navigation_remains_allowed(self):
        config = ExplorerConfig(max_depth=2, max_subtree_children=1)
        result, _, _, _, fetched = await self.read([
            note("Archive: 1840"), fetch_call("https://a.example/archive/1841"), note("Date: 1841")
        ], config)
        self.assertEqual(fetched, ["https://a.example/archive/1841"])
        self.assertEqual(result.nodes, 1)

    async def test_budget_stops_recursion_and_never_erases_page_note(self):
        config = ExplorerConfig(max_depth=3, max_subtree_children=1)
        llm, trace, budget = FakeLLM([note("Own evidence")]), MemoryTrace(), Budget(0)
        async def fetch(url):
            self.fail("No page may be fetched with a zero budget")
        result = await Explorer(llm, config, "Read", fetch).explore(
            question="Q", reasoning="", query="Q", documents=[Document("https://a.test", "D")],
            budget=budget, trace=trace, usage=Usage(),
        )
        self.assertIn("Own evidence", result.information)
        self.assertEqual(result.nodes, 0)

    async def test_leaf_with_no_evidence_does_not_get_retried(self):
        result, llm, *_ = await self.read([note("No helpful information found.", "not_found")])
        self.assertEqual(len(llm.requests), 1)
        self.assertEqual(result.status, "not_found")
        self.assertEqual(result.extraction_state, "complete")

    async def test_navigation_error_preserves_own_and_child_notes(self):
        config = ExplorerConfig(max_depth=2, max_subtree_children=2, max_turns=4)
        result, *_ = await self.read([
            note("Place: London"), fetch_call("https://b.example/register"), note("Date: 1840"),
            RuntimeError("navigation failed"),
        ], config)
        self.assertIn("Place: London", result.information)
        self.assertIn("Date: 1840", result.information)
        self.assertIn("navigation failed", result.error)

    async def test_failed_child_fetch_is_reported_and_budget_refunded(self):
        llm = FakeLLM([note("Place: London"), fetch_call("https://a.test/missing"), Reply(text="DONE")])
        budget = Budget(1)
        async def fetch(url):
            return Document(url, "HTTP 404", is_error=True)
        result = await Explorer(llm, ExplorerConfig(max_depth=2, max_subtree_children=1,
                                max_turns=3), "Read", fetch).explore(
            question="Q", reasoning="", query="Q", documents=[Document("https://a.test", "D")],
            budget=budget, trace=MemoryTrace(), usage=Usage(),
        )
        self.assertEqual((budget.used, result.nodes), (0, 0))
        self.assertIn("HTTP 404", result.information)
        self.assertEqual(result.extraction_state, "partial_failure")


class DepthSearchPolicyTests(unittest.IsolatedAsyncioTestCase):
    async def run_reader(self, replies, pages, *, depth=3, children=2):
        llm, trace, budget = FakeLLM(replies), MemoryTrace(), Budget(4)
        fetched = []
        async def fetch(url):
            fetched.append(url)
            return Document(url, pages[url])
        config = ExplorerConfig(max_depth=depth, max_subtree_children=children, max_turns=4,
                                isolate_extraction_context=True, prune_unhelpful_branches=True)
        result = await Explorer(llm, config, "Extract evidence; choose expansions.", fetch).explore(
            question="Find the 2020 district winners and their totals.",
            reasoning="UNVERIFIED_MAIN: the winner must be Mary.",
            parent_reasoning="PARENT_ONLY: Sam received 912 votes.",
            query="SPECULATIVE_QUERY Mary winning 912 votes",
            documents=[Document("https://a.test/root", pages["https://a.test/root"])],
            budget=budget, trace=trace, usage=Usage(),
        )
        self.assertFalse(llm.replies, "Unexpectedly skipped a scripted request")
        self.assertIsNone(result.error)
        return result, llm, trace, budget, fetched

    async def test_extraction_and_recovery_never_receive_parent_or_main_guesses(self):
        result, llm, trace, _, _ = await self.run_reader(
            [Reply(), note("Local fact: Ann won.\n**Expand:** no - no onward route")],
            {"https://a.test/root": "2020 district winner: Ann."},
        )
        self.assertIn("Ann won", result.information)
        for messages, tools in llm.requests:
            history = json.dumps(messages)
            for excluded in ("UNVERIFIED_MAIN", "PARENT_ONLY", "SPECULATIVE_QUERY", "912"):
                self.assertNotIn(excluded, history)
            self.assertIn("2020 district winner: Ann", history)
            self.assertIsNone(tools)
        self.assertEqual(len([e for e in trace.events if e[0] == "explorer.extract_input"]), 2)

    async def test_navigation_keeps_context_while_child_extraction_is_isolated(self):
        result, llm, _, budget, fetched = await self.run_reader([
            note("ROOT_ONLY: Ann won.\n**Expand:** yes - linked totals"),
            fetch_call("https://b.test/totals"), note("Total: 123.\n**Expand:** no - no further link"),
            Reply(text="DONE"),
        ], {"https://a.test/root": "Ann won. [totals](https://b.test/totals)",
            "https://b.test/totals": "Total votes: 123."})
        navigation = json.dumps(llm.requests[1][0])
        self.assertIn("UNVERIFIED_MAIN", navigation)
        self.assertIn("ROOT_ONLY", navigation)
        child_input = json.dumps(llm.requests[2][0])
        for excluded in ("UNVERIFIED_MAIN", "PARENT_ONLY", "ROOT_ONLY", "SPECULATIVE_QUERY"):
            self.assertNotIn(excluded, child_input)
        self.assertIn("Total votes: 123", child_input)
        self.assertIn("ROOT_ONLY", result.information)
        self.assertIn("123", result.information)
        self.assertEqual((result.nodes, budget.used), (1, 1))
        self.assertEqual(fetched, ["https://b.test/totals"])

    async def test_irrelevant_branch_stops_and_sibling_can_use_remaining_budget(self):
        result, _, trace, budget, fetched = await self.run_reader([
            note("Index.\n**Expand:** yes - two district records"),
            fetch_call("https://a.test/wrong"),
            note("This is 2026, no link to 2020.\n**Expand:** no - wrong year", "not_found"),
            fetch_call("https://a.test/right"),
            note("2020: Ann, 123.\n**Expand:** no - record complete", "answered"),
        ], {"https://a.test/root": "[record](https://a.test/wrong) [record](https://a.test/right)",
            "https://a.test/wrong": "2026 elections. [footer](https://a.test/footer)",
            "https://a.test/right": "2020: Ann, 123."})
        self.assertEqual(fetched, ["https://a.test/wrong", "https://a.test/right"])
        self.assertEqual(budget.remaining, 2)
        self.assertIn("Ann, 123", result.information)
        self.assertTrue(any(k == "expand.pruned" for k, _ in trace.events))

    async def test_index_without_answer_facts_can_still_follow_a_link(self):
        result, _, _, _, fetched = await self.run_reader([
            note("Index has a link to the 2020 register.\n**Expand:** yes - 2020 register", "not_found"),
            fetch_call("https://a.test/2020"), note("Ann, 123.", "answered"),
        ], {"https://a.test/root": "[2020 register](https://a.test/2020)",
            "https://a.test/2020": "Ann, 123."}, depth=2, children=1)
        self.assertEqual(result.nodes, 1)
        self.assertEqual(fetched, ["https://a.test/2020"])

    async def test_repeated_body_under_new_url_cannot_expand_again(self):
        body = "Index. [next](https://a.test/root?page=2)"
        result, _, _, budget, fetched = await self.run_reader([
            note("Index.\n**Expand:** yes - next page"), fetch_call("https://a.test/root?page=2"),
            note("Same index.\n**Expand:** yes - next page"),
        ], {"https://a.test/root": "URL Source: https://a.test/root\nMarkdown Content:\n" + body,
            "https://a.test/root?page=2": "URL Source: https://a.test/root?page=2\nMarkdown Content:\n" + body},
            children=1)
        self.assertEqual(result.log["opened"][0]["expansion_stop_reason"], "repeated_content")
        self.assertEqual(budget.used, 1)
        self.assertEqual(len(fetched), 1)

    async def test_no_evidence_without_a_route_conserves_budget(self):
        result, _, _, budget, fetched = await self.run_reader(
            [note("Unrelated page; only a contact link.", "not_found")],
            {"https://a.test/root": "[Contact](https://a.test/contact)"},
        )
        self.assertEqual(result.log["expansion_stop_reason"], "no_evidence_or_route")
        self.assertEqual(budget.used, 0)
        self.assertEqual(fetched, [])


class AgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_observed_malformed_first_search_is_executed_without_finalizing(self):
        from offline import FakeTools
        query = "Bureau of Labor Statistics Mountain-Plains region states"
        raw = ('<|start|>assistant<|channel|>commentary to=functions.web_search]{\n'
               f'  "query": "{query}"\n' + '}<|call|>')
        llm, trace, tools = FakeLLM([Reply(text=raw, finish_reason="stop"), Reply(text="A")]), MemoryTrace(), FakeTools()
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method="depthsearch")
        result = await agent.run("Which schools?", "Research", tools, trace)
        self.assertEqual(tools.searched, [query])
        self.assertEqual((result.answer, result.searches, result.stop_reason), ("A", 1, "answered"))
        self.assertIsNone(result.error)
        response = next(v for k, v in trace.events if k == "llm.response")
        self.assertTrue(response["recovered_tool_call"])
        self.assertEqual(response["raw_text"], raw)
        self.assertFalse(any(k == "run.finalizing" for k, _ in trace.events))
        assistant = next(m for m in reversed(llm.requests[1][0]) if m.get("tool_calls"))
        self.assertIn('"query"', assistant["tool_calls"][0]["function"]["arguments"])

    async def test_empty_first_turn_keeps_tools_for_one_retry(self):
        from offline import FakeTools
        search = Reply(tool_calls=[SimpleNamespace(id="s", function=SimpleNamespace(
            name="web_search", arguments='{"query":"regional office"}'))])
        llm, tools, trace = FakeLLM([Reply(reasoning="Search."), search, Reply(text="A")]), FakeTools(), MemoryTrace()
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method="depthsearch")
        result = await agent.run("Q", "Research", tools, trace)
        self.assertEqual((result.searches, result.answer), (1, "A"))
        self.assertTrue(llm.requests[1][1])
        self.assertEqual(len([k for k, _ in trace.events if k == "run.resume_tools"]), 1)

    async def test_empty_tool_recovery_is_bounded(self):
        from offline import FakeTools
        llm, trace = FakeLLM([Reply(), Reply(), Reply()]), MemoryTrace()
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method="depthsearch")
        result = await agent.run("Q", "Research", FakeTools(), trace)
        self.assertEqual(result.stop_reason, "no_answer")
        self.assertEqual(result.usage.calls, 3)
        self.assertTrue(llm.requests[0][1])
        self.assertTrue(llm.requests[1][1])
        self.assertIsNone(llm.requests[2][1])

    async def test_short_final_is_preserved_and_raw_output_is_logged(self):
        raw = "<|start|>assistant<|channel|>final<|message|>Norway<|end|>"
        llm, trace = FakeLLM([Reply(text=raw)]), MemoryTrace()
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method="ragent")
        result = await agent.run("Which country?", "Research",
                                 SimpleNamespace(specs_for=lambda names: []), trace)
        self.assertEqual(result.answer, "Norway")
        event = next(v for k, v in trace.events if k == "llm.response")
        self.assertEqual(event["raw_text"], raw)
        self.assertTrue(event["cleanup_changed"])
        self.assertEqual(result.usage.calls, 1)

    async def test_salvage_logs_raw_short_answer(self):
        raw = "2015<|fim_suffix|>"
        llm, trace = FakeLLM([Reply(), Reply(text=raw)]), MemoryTrace()
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method="ragent")
        result = await agent.run("Which year?", "Research",
                                 SimpleNamespace(specs_for=lambda names: []), trace)
        self.assertEqual((result.answer, result.stop_reason), ("2015", "finalized"))
        event = next(v for k, v in trace.events if k == "run.final_response")
        self.assertEqual(event["raw_text"], raw)

    async def test_depthsearch_search_guidance_does_not_mutate_shared_tools(self):
        spec = {"type": "function", "function": {"name": "web_search", "description": "Search"}}
        tools = SimpleNamespace(specs_for=lambda names: [SimpleNamespace(as_openai=lambda: spec)])
        for method in ("depthsearch", "ragent"):
            llm = FakeLLM([Reply(text="A")])
            with patch("searchgym.agent.LLM", return_value=llm):
                agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method=method)
            await agent.run("Q", "Research", tools, MemoryTrace())
            description = llm.requests[0][1][0]["function"]["description"]
            self.assertEqual("entry page" in description, method == "depthsearch")
        self.assertEqual(spec["function"]["description"], "Search")

    async def test_action_only_answer_is_finalized_without_tools(self):
        llm = FakeLLM([Reply(text="Open the thoracic."), Reply(text="The supported factors are A and B.")])
        tools = SimpleNamespace(specs_for=lambda names: [])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method="ragent")
        result = await agent.run("Which factors?", "Research", tools, MemoryTrace())
        self.assertEqual(result.stop_reason, "finalized")
        self.assertEqual(result.answer, "The supported factors are A and B.")
        self.assertEqual(result.usage.calls, 2)
        self.assertIsNone(llm.requests[-1][1])

    async def test_invalid_fetch_arguments_never_reach_the_network(self):
        with patch("searchgym.agent.LLM", return_value=FakeLLM([])):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(), method="ragent")
        call = SimpleNamespace(function=SimpleNamespace(name="web_fetch", arguments='{"_raw":"open it"}'))
        result, step = RunResult(), Step(1)
        result.steps.append(step)
        response = await agent._run_tool(call=call, tools=None, explorer=None, budget=Budget(0),
                                         result=result, step=step, trace=MemoryTrace(), question="Q")
        self.assertIn("Invalid web_fetch arguments", response)
        self.assertEqual(result.fetch_attempts, 0)
        self.assertEqual(result.invalid_tool_calls, 1)


class ParsingAndMetricsTests(unittest.TestCase):
    def test_tool_recovery_requires_explicit_offered_call_and_complete_json(self):
        specs = [{"function": {"name": "web_search"}}]
        raw = '<|start|>assistant<|channel|>commentary to=functions.web_search]{"query":"x"}<|call|>'
        for text, finish, offered in [
            (raw, "length", specs), (raw, "stop", []),
            (raw.replace("web_search", "delete_files"), "stop", specs),
            (raw.replace('{"query":"x"}', '{"query":"x"'), "stop", specs),
            ("Example: " + raw, "stop", specs),
            (raw + "This is just an example.", "stop", specs),
        ]:
            with self.subTest(text=text, finish=finish):
                reply = Reply(text=text, finish_reason=finish)
                self.assertFalse(recover_tool_calls(reply, offered))
                self.assertEqual(reply.tool_calls, [])

    def test_expansion_control_is_removed_without_erasing_source_evidence(self):
        body, status = _parse_final(
            "**Final Information**\n**Evidence:** 2020: Ann, 123.\n"
            "**Expand:** **no** - no useful route\n**Status:** partial"
        )
        evidence, decision = _parse_expansion_decision(body)
        self.assertEqual((decision, status), ("no", "partial"))
        self.assertIn("2020: Ann, 123.", evidence)
        self.assertNotIn("Expand:", evidence)

    def test_clean_answer_preserves_short_facts_but_rejects_tool_envelopes(self):
        for raw, expected in [
            ("Europe<|end|>", "Europe"), ("2015<|fim_suffix|>", "2015"),
            ("<|im_start|>assistant<|meta_sep|>final<|im_sep|>A, B<|im_end|>", "A, B"),
            ("<|start|>assistant<|channel|>analysis<|message|>Guessing...<|end|>"
             "<|start|>assistant<|channel|>final<|message|>A<|end|>", "A"),
            ("<|start|>assistant<|channel|>commentary to=functions.web_search}<|call|>", ""),
            ("<|start|>assistant to=functions.web_search<|message|>{\"query\":\"x\"}<|call|>", ""),
            ("<|start|>assistant<|channel|>analysis<|message|>Still thinking<|end|>", ""),
            ("The literal string is to=functions.web_search.<|end|>",
             "The literal string is to=functions.web_search."),
        ]:
            with self.subTest(raw=raw):
                self.assertEqual(_clean_answer(raw), expected)

    def test_all_method_configs_load(self):
        for method in ("ragent", "search-o1", "depthsearch"):
            config = load_test(method=method)
            self.assertEqual(config.method, method)
        self.assertTrue(load_test(method="depthsearch").explorer.extract_before_expand)

    def test_embedded_empty_phrase_does_not_erase_facts(self):
        body, status = _parse_final(
            '**Final Information**\nDate: 1840. Child said "No helpful information found."\n**Status:** partial'
        )
        self.assertIn("1840", body)
        self.assertEqual(status, "partial")

    def test_standalone_sentinel_is_empty(self):
        self.assertEqual(_parse_final("**Final Information**\nNo helpful information found.\n**Status:** not_found"),
                         ("", "not_found"))

    def test_only_final_status_is_metadata(self):
        body, status = _parse_final("**Final Information**\nChild note:\n**Status:** not_found\nDate: 1840\n**Status:** partial")
        self.assertEqual(status, "partial")
        self.assertIn("**Status:** not_found", body)

    def test_embedded_heading_does_not_erase_preceding_evidence(self):
        body, _ = _parse_final('Date: 1840. A child used the heading **Final Information**.')
        self.assertIn("Date: 1840", body)

    def test_url_identity_keeps_path_and_query_case(self):
        self.assertNotEqual(_norm("https://a.test/Record?key=A"), _norm("https://a.test/record?key=a"))
        self.assertEqual(_norm("https://A.TEST/Record#section"), _norm("https://a.test/Record"))

    def test_empty_response_remains_in_score_denominator(self):
        result = aggregate([Judgement(parts=[("A", True)]), Judgement(error="empty_response")])
        self.assertEqual(result["f1"], .5)
        self.assertEqual(result["f1_valid_only"], 1)
        self.assertEqual(result["score_denominator"], 2)

    def test_relevant_configuration_changes_invalidate_cache(self):
        agent, explorer = AgentConfig(), ExplorerConfig()
        for field, value in {"fetch_max_tokens": 1024, "model_name": "different"}.items():
            self.assertNotEqual(_agent_fingerprint(agent), _agent_fingerprint(replace(agent, **{field: value})))
        for field, value in {"context_limit": 64000, "max_link_menu": 0, "extract_before_expand": False,
                             "isolate_extraction_context": True, "prune_unhelpful_branches": True}.items():
            self.assertNotEqual(_explorer_fingerprint(explorer, "depthsearch"),
                                _explorer_fingerprint(replace(explorer, **{field: value}), "depthsearch"))

    def test_diagnostics_survive_result_cache_roundtrip(self):
        result = RunResult(reader_stats={"empty_output": 2}, invalid_tool_calls=1,
                           budget={"total": 4, "used": 4, "refused": 0})
        restored = _result_from(result.as_dict())
        self.assertEqual(restored.reader_stats, {"empty_output": 2})
        self.assertEqual(restored.invalid_tool_calls, 1)
        self.assertTrue(restored.budget_exhausted)

    def test_reader_urls_are_unwrapped_without_losing_query(self):
        self.assertEqual(normalize_fetch_url("https://r.jina.ai/http://r.jina.ai/https://a.test/path?year=2021"),
                         "https://a.test/path?year=2021")
        for value in (None, {}, "", "relative/path", "file:///etc/passwd"):
            with self.assertRaises(ValueError):
                normalize_fetch_url(value)

    def test_reader_error_detection_does_not_match_article_body(self):
        self.assertTrue(reader_failure("Title: Missing\nWarning: Target URL returned error 404: Not Found\n"))
        self.assertFalse(reader_failure("Title: HTTP documentation\nAn HTTP 404 means Not Found."))
        self.assertTrue(reader_failure("Title: Page Not Found - Site Help\nMarkdown Content:\nNavigation"))
        self.assertTrue(reader_failure("Title: 404 Not Found\nMarkdown Content:\nNavigation"))
        self.assertFalse(reader_failure("Title: How to fix Page Not Found errors\nError tutorial"))

    def test_short_fact_is_not_an_action(self):
        self.assertFalse(_looks_like_action("Europe."))
        self.assertFalse(_looks_like_action("Open access journals include A and B.\nThese meet the conditions."))


class RunnerIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_actual_runner_persists_notes_metrics_and_cache_without_apis(self):
        # A real dataset record exercises loading/scoring shape; its fake answer is
        # never submitted to a model or treated as a benchmark measurement.
        from offline import FakeTools, FakeLLM as OfflineLLM, FakeJudge
        for method in ("ragent", "search-o1", "depthsearch"):
            config = load_test(method=method)
            profile = profile_for(config.model)
            fake = OfflineLLM(profile, config.explorer_prompt.splitlines()[0] if config.explorer_prompt else "\0")
            with tempfile.TemporaryDirectory(prefix="searchgym-regression-") as temp:
                out = Path(temp)
                with patch("searchgym.agent.LLM", return_value=fake):
                    runner = Runner(profile, config.agent, FakeJudge(), out, method=method,
                                    explorer_config=config.explorer, explorer_prompt=config.explorer_prompt,
                                    cache_root=out / "cache", use_cache=True)
                benchmark = load_benchmark(config.benchmark.name, config.benchmark.dataset("validation"))
                item = benchmark.load(limit=1)[0]
                record = await runner.run_one(benchmark, item, config.system_prompt, FakeTools())
                self.assertTrue(record.result.answer)
                self.assertIsNone(record.result.error)
                self.assertTrue((out / record.dir / "tree.svg").exists())
                if method == "depthsearch":
                    self.assertGreater(record.result.expansion_nodes, 0)
                    self.assertIn("Page note", record.result.tool_calls[-1].result)
                    self.assertGreater(summarize([record])["reader_stats"]["sessions"], 0)
                again = await runner.run_one(benchmark, item, config.system_prompt, FakeTools())
                self.assertTrue(again.cached)
                self.assertEqual(record.result.reader_stats, again.result.reader_stats)
                await runner.aclose()


if __name__ == "__main__":
    unittest.main()
