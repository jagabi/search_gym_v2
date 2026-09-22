"""No network: selective entry, evidence validation, accounting and recovery."""
import json
import unittest
from dataclasses import asdict
from types import SimpleNamespace
from unittest.mock import patch

from offline import FakeTools
from test_reader_integrity import FakeLLM, MemoryTrace, note, fetch_call
from test_tool_availability import call
from searchgym.agent import AgentConfig, RunResult, SearchAgent
from searchgym.config import load_test
from searchgym.explorer import Document, ExplorerConfig, _parse_final
from searchgym.llm import Reply, Usage
from searchgym.research_state import ResearchState, is_search_endpoint, parse_control
from searchgym.runner import _agent_fingerprint, _result_from
from searchgym.serving import profile_for


URL = "https://source.example/Author-Profile.html"
FACT = "The artist records as River and was born in November 1998."


def control(read=None, **updates):
    if read is not None:
        return fetch_call({"S1": "https://other.example/music", "S2": URL}.get(read, read))
    if not updates:
        return Reply(text="No useful unread page to open.", finish_reason="stop")
    return Reply(text=json.dumps({"read": read, **updates}), finish_reason="stop")


def checkpoint():
    return {"candidates": [{"name": "River", "disposition": "active", "support": [
        {"source": "S2", "quote": FACT}], "unknown": ["project start month"]}],
        "draft": {"text": "River", "sources": ["S2"]}}


class SourceTools(FakeTools):
    async def search(self, query):
        self.searched.append(query)
        data = {"organic": [
            {"title": "Generic music", "link": "https://other.example/music", "snippet": "A music index."},
            {"title": "Artist profile", "link": URL, "snippet": FACT}]}
        return data, SimpleNamespace(is_error=False, duration_ms=1, text=json.dumps(data))

    async def fetch(self, url):
        self.fetched.append(url)
        return Document(url, FACT)


class StateTests(unittest.TestCase):
    def test_source_ids_preserve_case_and_ambiguous_urls_are_not_rewritten(self):
        state = ResearchState()
        a = state.register(URL, snippet=FACT)
        b = state.register(URL.replace("Author-Profile", "author-profile"))
        self.assertNotEqual(a, b)
        self.assertEqual(state.resolve(a), URL)
        with self.assertRaises(ValueError):
            state.resolve("S999")

    def test_quotes_and_draft_refs_must_exist_in_supplied_evidence(self):
        state = ResearchState()
        state.register("https://other.example/music")
        state.register(URL, snippet=FACT)
        state.apply(checkpoint(), {"S2"})
        self.assertEqual(state.draft["text"], "River")
        state.apply({"candidates": [{"name": "Invented", "support": [
            {"source": "S2", "quote": "This artist is Invented"}]}],
            "draft": {"text": "Invented", "sources": ["S999"]}}, {"S2"})
        self.assertNotIn("Invented", state.candidates)
        self.assertEqual(state.draft["text"], "River")
        # Missing a condition does not erase the existing supported item.
        state.apply({"candidates": [{"name": "River", "unknown": ["birthplace"]}]}, {"S2"})
        self.assertEqual(len(state.candidates["River"]["support"]), 1)
        self.assertEqual(state.draft["text"], "River")

    def test_rejecting_only_candidate_invalidates_old_draft_without_losing_evidence(self):
        state = ResearchState()
        state.register("https://other.example/music")
        state.register(URL, snippet=FACT)
        state.apply(checkpoint(), {"S2"})
        state.apply({"candidates": [{"name": "River", "disposition": "rejected", "against": [
            {"source": "S2", "quote": "born in November 1998"}]}]}, {"S2"})
        self.assertFalse(state.draft)
        self.assertEqual(len(state.candidates["River"]["support"]), 1)

    def test_search_endpoint_detection_leaves_document_and_site_navigation_available(self):
        for url in ("https://www.google.com/search?q=artist", "https://www.google.co.kr/search?q=x",
                    "https://duckduckgo.com/?q=x", "https://bing.com/search?q=x",
                    "https://r.jina.ai/https://google.com/search?q=x"):
            self.assertTrue(is_search_endpoint(url), url)
        for url in ("https://en.wikipedia.org/w/index.php?search=artist",
                    "https://www.google.com/maps?q=museum", URL):
            self.assertFalse(is_search_endpoint(url), url)

    def test_baseline_fingerprint_is_unchanged(self):
        cfg = AgentConfig()
        previous = {k: v for k, v in asdict(cfg).items()
                    if k not in {"base_url", "api_key", "timeout_s", "depthsearch_control"}}
        self.assertEqual(_agent_fingerprint(cfg), json.dumps(previous, sort_keys=True, ensure_ascii=False))
        self.assertNotEqual(_agent_fingerprint(cfg), _agent_fingerprint(AgentConfig(depthsearch_control=True)))

    def test_settings_keep_search_controls_and_enable_only_ds(self):
        for method in ("ragent", "search-o1", "depthsearch"):
            cfg = load_test(method=method)
            self.assertEqual((cfg.agent.max_searches, cfg.agent.search_results), (10, 10))
            self.assertEqual(cfg.agent.depthsearch_control, method == "depthsearch")

    def test_ds_status_explanation_does_not_change_baseline_parser(self):
        text = "Access challenge.\n**Status:** not_found – no article body"
        self.assertEqual(_parse_final(text, allow_explanation=True)[1], "not_found")
        self.assertEqual(_parse_final(text)[1], "partial")


class ControllerTests(unittest.IsolatedAsyncioTestCase):
    def make(self, replies, **kwargs):
        llm = FakeLLM(replies)
        cfg = AgentConfig(depthsearch_control=True, **kwargs)
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), cfg, method="depthsearch",
                                explorer_config=ExplorerConfig(max_depth=1, max_expansion_nodes=0))
        return agent, llm

    async def test_search_selects_nonfirst_exact_url_preserves_results_and_accounts_calls(self):
        agent, llm = self.make([call("web_search", {"query": "artist profile"}), control("S2"),
                               note(FACT), control(**checkpoint()), Reply(text="River")])
        tools, trace = SourceTools(), MemoryTrace()
        result = await agent.run("Which artist?", "Research", tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, "River")
        self.assertEqual(tools.searched, ["artist profile"])
        self.assertEqual(tools.fetched, [URL])
        self.assertEqual((result.searches, result.fetches, result.auto_fetches, result.fetch_attempts), (1, 0, 1, 1))
        self.assertEqual(result.usage.calls, 5)
        self.assertEqual(result.research_state.metrics["controller_calls"], 2)
        returned = result.steps[0].tool_calls[0].result
        self.assertIn("Generic music", returned)
        self.assertIn(FACT, returned)
        self.assertTrue(result.steps[0].tool_calls[0].explorations)
        # Selector sees source observations, not the main model's accumulated guesses.
        self.assertNotIn("reasoning", json.loads(llm.requests[1][0][-1]["content"])["working_state"])
        self.assertEqual(llm.tool_choices[1:4], ["auto", "none", "none"])
        self.assertEqual([t["function"]["name"] for t in llm.requests[1][1]], ["web_fetch"])

    async def test_invalid_selector_has_no_fetch_or_state_mutation(self):
        for reply in (Reply(text="not json"), control("S999"), control(None), Reply(text='{"read":"S2"}', finish_reason="length")):
            agent, _ = self.make([call("web_search", {"query": "artist"}), reply, Reply(text="unknown")])
            tools = SourceTools()
            result = await agent.run("Q", "Research", tools, MemoryTrace())
            self.assertIsNone(result.error)
            self.assertEqual(tools.fetched, [])
            self.assertEqual(result.searches, 1)

    async def test_fetch_decision_distinguishes_skip_empty_and_invalid_without_retry(self):
        malformed = fetch_call(URL)
        malformed.tool_calls[0].function.arguments = '{"url":'
        multiple = fetch_call(URL)
        multiple.tool_calls += fetch_call("https://other.example/music").tool_calls
        truncated = fetch_call(URL)
        truncated.finish_reason = "length"
        extra_argument = fetch_call(URL)
        extra_argument.tool_calls[0].function.arguments = json.dumps({"url": URL, "goal": "read"})
        for reply, metric in (
            (Reply(text="No additional page is useful.", finish_reason="stop"), "controller_skips"),
            (Reply(reasoning="Open S2", finish_reason="stop"), "controller_invalid"),
            (malformed, "controller_invalid"),
            (multiple, "controller_invalid"),
            (truncated, "controller_invalid"),
            (extra_argument, "controller_invalid"),
            (call("web_search", {"query": "artist"}), "controller_invalid"),
            (fetch_call(URL.lower()), "controller_invalid"),
        ):
            with self.subTest(metric=metric, reply=reply):
                agent, llm = self.make([reply])
                state = ResearchState()
                sid = state.register(URL, snippet=FACT, search_entry=True)
                result = RunResult(research_state=state)
                trace = MemoryTrace()
                selected = await agent._control("Which artist?", result, trace, [sid], select=True)
                self.assertIsNone(selected)
                self.assertEqual(state.metrics[metric], 1)
                self.assertFalse(state.candidates)
                self.assertEqual(len(llm.requests), 1)
                self.assertEqual(llm.tool_choices, ["auto"])

    async def test_no_selectable_sources_needs_no_decision_call(self):
        agent, llm = self.make([])
        state = ResearchState()
        sid = state.add_note(URL, FACT, "partial")
        selected = await agent._control("Q", RunResult(research_state=state), MemoryTrace(), [sid], select=True)
        self.assertIsNone(selected)
        self.assertFalse(llm.requests)

    async def test_plain_selection_reply_returns_to_main_for_another_search(self):
        skip = Reply(text="No page needs reading yet.", finish_reason="stop")
        agent, llm = self.make([
            call("web_search", {"query": "first clue"}), skip,
            call("web_search", {"query": "different clue"}), skip,
            Reply(text="Main model's final answer", finish_reason="stop"),
        ])
        tools, trace = SourceTools(), MemoryTrace()
        result = await agent.run("Q", "Research", tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(tools.searched, ["first clue", "different clue"])
        self.assertEqual(result.answer, "Main model's final answer")
        self.assertEqual(result.turns, 3)
        self.assertEqual(result.research_state.metrics["controller_skips"], 2)
        self.assertFalse(tools.fetched)
        self.assertEqual(result.expansion_nodes, 0)
        self.assertEqual(result.max_depth_reached, 1)
        self.assertEqual(len(llm.requests), 5)
        self.assertFalse(llm.replies)
        # Search observations return as a tool result; the internal stop is not
        # mistaken for the main assistant's final answer.
        for index in (2, 4):
            history, specs = llm.requests[index]
            self.assertTrue(any(m["role"] == "tool" and FACT in m["content"] for m in history))
            self.assertEqual({s["function"]["name"] for s in specs}, {"web_search"})

    async def test_controller_error_does_not_discard_search_results(self):
        agent, _ = self.make([call("web_search", {"query": "artist"}), RuntimeError("offline error"), Reply(text="River")])
        result = await agent.run("Q", "Research", SourceTools(), MemoryTrace())
        self.assertIsNone(result.error)
        self.assertIn(FACT, result.steps[0].tool_calls[0].result)
        self.assertEqual(result.research_state.metrics["controller_errors"], 1)

    async def test_auto_fetch_obeys_cap_and_stale_main_fetch_cannot_bypass_it(self):
        agent, llm = self.make([call("web_search", {"query": "artist"}), control("S2"), note(FACT),
                               control(**checkpoint()), fetch_call("S1"), Reply(text="River")],
                              max_searches=1, max_fetches=1)
        tools = SourceTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [URL])
        self.assertEqual(result.fetches, 0)
        self.assertIsNone(llm.requests[4][1])

    async def test_max_turn_finalization_receives_grounded_checkpoint(self):
        agent, llm = self.make([call("web_search", {"query": "artist"}), control("S2"), note(FACT),
                               control(**checkpoint()), Reply(text="River")], max_turns=1)
        result = await agent.run("Q", "Research", SourceTools(), MemoryTrace())
        self.assertEqual(result.answer, "River")
        final_request = str(llm.requests[-1][0])
        self.assertIn("provisional answer", final_request)
        self.assertIn(FACT, final_request)
        self.assertIn("River", final_request)
        self.assertEqual(llm.tool_choices[-1], "none")

    async def test_main_fetch_is_not_offered_and_cannot_execute_even_with_budget(self):
        agent, llm = self.make([call("web_search", {"query": "artist"}), control(None),
                               fetch_call(URL), Reply(text="River")])
        tools = SourceTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [])
        self.assertEqual(result.fetches, 0)
        self.assertTrue(result.steps[1].tool_calls[0].refused)
        self.assertIn("not a main action", result.steps[1].tool_calls[0].result)
        for index in (0, 2, 3):
            self.assertEqual([s["function"]["name"] for s in llm.requests[index][1]], ["web_search"])

    async def test_blocked_search_fetch_never_reaches_network_including_reader_path(self):
        agent, _ = self.make([])
        tools = SourceTools()
        result = RunResult(research_state=ResearchState())
        doc = await agent._document("https://r.jina.ai/https://google.com/search?q=x", tools, "Q", MemoryTrace(), result)
        self.assertTrue(doc.is_error)
        self.assertFalse(tools.fetched)
        self.assertEqual(result.fetch_attempts, 0)

    async def test_plan_is_retried_without_rejecting_short_answer(self):
        agent, _ = self.make([Reply(text='Need source for "Do It For Me". Another page. Open.'), Reply(text="Rosenfeld")])
        answer = await agent._salvage([{"role": "user", "content": "Who?"}], MemoryTrace(), Usage())
        self.assertEqual(answer, "Rosenfeld")

    async def test_cache_roundtrip_retains_controller_usage_and_checkpoint(self):
        agent, _ = self.make([call("web_search", {"query": "artist"}), control("S2"), note(FACT),
                             control(**checkpoint()), Reply(text="River")])
        result = await agent.run("Q", "Research", SourceTools(), MemoryTrace())
        restored = _result_from(result.as_dict())
        self.assertEqual(restored.auto_fetches, result.auto_fetches)
        self.assertEqual(restored.research_state.snapshot(), result.research_state.snapshot())
        self.assertEqual(restored.usage.as_dict(), result.usage.as_dict())

    async def test_selected_entry_can_recurse_with_same_global_node_budget(self):
        child = "https://source.example/Register"
        class LinkedTools(SourceTools):
            async def fetch(self, url):
                self.fetched.append(url)
                return Document(url, FACT + (f" [register]({child})" if url == URL else ""))
        agent, llm = self.make([call("web_search", {"query": "artist"}), control("S2", reason="Read the artist register"),
            note(FACT + "\n**Expand:** yes"), fetch_call(child), note(FACT),
            control(**checkpoint()), Reply(text="River")])
        agent.explorer_config = ExplorerConfig(max_depth=2, max_expansion_nodes=1, max_subtree_children=1)
        tools = LinkedTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [URL, child])
        self.assertEqual(result.expansion_nodes, 1)
        self.assertEqual(result.max_depth_reached, 2)
        self.assertEqual(result.searches, 1)
        self.assertEqual(result.auto_fetches, 1)
        self.assertEqual(result.research_state.source(child)["status"], "read")
        self.assertFalse(llm.replies)

    async def test_exhausted_search_refuses_stale_main_fetch_calls(self):
        agent, llm = self.make([call("web_search", {"query": "artist"}), control("S2"), note(FACT),
            control(**checkpoint()), fetch_call("S2"), Reply(text="River")], max_searches=1)
        tools = SourceTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(tools.fetched, [URL])
        self.assertIsNone(llm.requests[-1][1])
        self.assertEqual(llm.tool_choices[-1], "none")
        self.assertEqual(result.answer, "River")
        self.assertFalse(llm.replies)

    async def test_last_search_finishes_reading_then_calls_main_without_tools(self):
        agent, llm = self.make([call("web_search", {"query": "artist"}), control("S2"),
                               note(FACT), control(**checkpoint()), Reply(text="River")], max_searches=1)
        tools = SourceTools()
        result = await agent.run("Q", "Research", tools, MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual((result.searches, result.auto_fetches, result.fetches), (1, 1, 0))
        self.assertEqual(tools.fetched, [URL])
        self.assertEqual(result.answer, "River")
        self.assertEqual(result.turns, 2)
        self.assertIsNone(llm.requests[-1][1])
        self.assertEqual(llm.tool_choices[-1], "none")
        self.assertTrue(any(m["role"] == "user" and FACT in m["content"] for m in llm.requests[-1][0]))
        self.assertFalse(llm.replies)

    async def test_last_search_skip_still_calls_main_for_final_answer(self):
        agent, llm = self.make([call("web_search", {"query": "artist"}), control(None),
                               Reply(text="Main answer")], max_searches=1)
        result = await agent.run("Q", "Research", SourceTools(), MemoryTrace())
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, "Main answer")
        self.assertEqual(result.turns, 2)
        self.assertEqual(result.auto_fetches, 0)
        self.assertEqual(llm.tool_choices[-1], "none")
        self.assertIsNone(llm.requests[-1][1])
        self.assertFalse(llm.replies)

    async def test_exhaustion_switches_system_and_retries_empty_answer_exactly_once(self):
        for second, expected in ((Reply(text="River"), "River"), (Reply(reasoning="Still no body"), "")):
            with self.subTest(expected=expected):
                agent, llm = self.make([call("web_search", {"query": "artist"}), control(None),
                                       Reply(reasoning="No body"), second], max_searches=1)
                trace = MemoryTrace()
                result = await agent.run("Which artist?", "SEARCH_POLICY_SENTINEL", SourceTools(), trace)
                self.assertEqual(result.answer, expected)
                self.assertEqual(result.stop_reason, "finalized" if expected else "no_answer")
                self.assertEqual(len(llm.requests), 4)  # Search, selector, final, one retry.
                self.assertFalse(llm.replies)
                for messages, tools in llm.requests[-2:]:
                    self.assertIsNone(tools)
                    self.assertIn("Research has ended", messages[0]["content"])
                    self.assertNotIn("SEARCH_POLICY_SENTINEL", str(messages))
                    self.assertIn("Which artist?", str(messages))
                    self.assertIn(FACT, str(messages))
                    self.assertFalse(any(m["role"] in {"assistant", "tool"} for m in messages))
                self.assertEqual(llm.tool_choices[-2:], ["none", "none"])
                final_events = [e for kind, e in trace.events if kind == "run.final_response"]
                self.assertEqual(len(final_events), 2)
                self.assertEqual(final_events[0]["reasoning"], "No body")

    async def test_large_history_finalization_keeps_checkpoint_instead_of_overflowing(self):
        agent, llm = self.make([Reply(text="River")], context_limit=2000)
        messages = [{"role": "system", "content": "Research"}, {"role": "user", "content": "Which artist?"},
                    {"role": "tool", "content": "Repeated old information. " * 2000}]
        answer = await agent._salvage(messages, MemoryTrace(), Usage(), checkpoint="Draft: River. Source: " + FACT)
        self.assertEqual(answer, "River")
        self.assertIn(FACT, str(llm.requests[-1][0]))
        self.assertNotIn("Repeated old information", str(llm.requests[-1][0]))

    async def test_baselines_ignore_controller_even_if_flag_enabled(self):
        for method in ("ragent", "search-o1"):
            llm = FakeLLM([call("web_search", {"query": "artist"}), Reply(text="River")])
            with patch("searchgym.agent.LLM", return_value=llm):
                agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(depthsearch_control=True), method=method)
            tools = SourceTools()
            result = await agent.run("Q", "Research", tools, MemoryTrace())
            self.assertIsNone(result.research_state)
            self.assertFalse(tools.fetched)
            self.assertEqual(result.usage.calls, 2)
