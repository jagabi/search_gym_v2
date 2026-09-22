"""Saved-state replay must not expose answer labels or execute page fetching."""
import json
import unittest
from unittest.mock import patch

from probe_entry_decisions import replay_case, restore_state
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.serving import profile_for
from test_reader_integrity import FakeLLM, MemoryTrace, fetch_call


class SavedDecisionProbeTests(unittest.IsolatedAsyncioTestCase):
    def case(self):
        urls = [f"https://source.example/{i}" for i in range(4)]
        sources = [{"id": f"S{i + 1}", "url": u, "title": f"Title {i}",
                    "status": "read" if i == 2 else "unread", "evidence": f"Saved evidence {i}"}
                   for i, u in enumerate(urls)]
        return {"case": "q00001_t4_invalid", "group": "INVALID_LABEL_SENTINEL", "old_menu_size": 3,
            "question": "Question", "query": "Current query", "gold_answer": "GOLD_SENTINEL",
            "payload": {"working_state": {"sources": sources, "metrics": {"controller_calls": 50}},
                        "sources": sources},
            "search_entries": [{"link": u} for u in urls[:3]], "fresh_entries": [{"link": urls[1]}]}

    async def test_recovery_stops_before_fetch_and_excludes_labels_page_only_links_and_read_sources(self):
        case = self.case()
        llm = FakeLLM([fetch_call("https://google.com/search?q=test"), fetch_call("https://source.example/1")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(depthsearch_control=True, max_tool_recoveries=2),
                                method="depthsearch")
        with patch.object(agent, "_fetch", side_effect=AssertionError("Probe must not fetch")):
            row = await replay_case(agent, case, MemoryTrace())
        self.assertEqual(row["decisions"], ["invalid_tool_call", "fetch"])
        self.assertEqual(row["usage"]["calls"], 2)
        self.assertEqual(row["metrics"]["controller_calls"], 2)
        request = json.loads(llm.requests[0][0][1]["content"])
        self.assertEqual(request["selectable"], ["S1", "S2"])
        self.assertEqual(request["current_query"], "Current query")
        self.assertIn("Saved evidence 0", request["previous_sources"][0]["evidence"])
        self.assertIn("Saved evidence 1", request["sources"][0]["evidence"])
        self.assertNotIn("GOLD_SENTINEL", str(llm.requests))
        self.assertNotIn("INVALID_LABEL_SENTINEL", str(llm.requests))
        self.assertFalse(llm.replies)
        # The original case remains reusable for independent repetitions.
        state, focus = restore_state(case)
        self.assertEqual(state.selectable(), ["S1", "S2"])
        self.assertEqual(focus, ["S2"])
        self.assertEqual(state.metrics["controller_calls"], 50)
