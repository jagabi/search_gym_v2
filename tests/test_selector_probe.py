"""Ensure the cheap selector diagnostic cannot fetch or expose evaluation labels."""
import unittest
import json
import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from probe_selective_entry import inspect_probe, replay_case, main
from test_reader_integrity import FakeLLM, MemoryTrace, fetch_call
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.serving import profile_for


class ProbeTests(unittest.IsolatedAsyncioTestCase):
    def test_offline_inspection_distinguishes_failure_modes_without_model_calls(self):
        examples = [
            ({"text": "", "reasoning": "Thinking"}, "reasoning_only"),
            ({"text": ""}, "empty_response"),
            ({"text": '{"read":', "finish_reason": "length"}, "truncated"),
            ({"text": 'Here is my choice: {"read":"S1"}'}, "invalid_json_or_empty_object"),
            ({"text": '{"read":null}'}, "explicit_skip"),
            ({"text": '{"read":"S99"}'}, "invalid_source_id"),
            ({"text": '{"read":"S1"}'}, "selected_source"),
            ({"text": '{"reason":"useful"}'}, "missing_read_field"),
            ({"text": '{"read":"S1"}', "valid": False}, "rejected_despite_parseable_json"),
            ({"text": "", "tool_calls": 1}, "unexpected_tool_calls"),
            ({"text": "", "tool_calls": [{"name": "web_fetch", "arguments": "{}"}],
              "decision": "fetch", "selected": "S1"}, "fetch"),
            ({"text": "No need to read more.", "decision": "skip"}, "skip"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            for index, (fields, _) in enumerate(examples):
                trace = [{"event": "control.request", "messages": [
                    {"role": "user", "content": json.dumps({"selectable": ["S1"]})}]},
                    {"event": "control.response", "finish_reason": "stop", **fields}]
                (directory / f"q{index:05d}_1.jsonl").write_text(
                    "\n".join(json.dumps(e) for e in trace), encoding="utf-8")
            with patch("probe_selective_entry.SearchAgent", side_effect=AssertionError("No model")), redirect_stdout(io.StringIO()):
                report = inspect_probe(directory)
                # The CLI must bypass loading the original run, config and model.
                with patch("sys.argv", ["probe_selective_entry.py", "--inspect", str(directory)]), \
                     patch("probe_selective_entry.load_cases", side_effect=AssertionError("No source run required")):
                    main()
            self.assertEqual([r["category"] for r in report["rows"]], [c for _, c in examples])
            self.assertEqual(len(report["categories"]), len(examples))
            self.assertTrue((directory / "inspection.json").exists())

    async def test_replay_makes_one_model_call_without_target_labels(self):
        case = {"id": 999, "turn": 2, "question": "Which article contains the date?",
                "entries": [{"link": "https://example.org/Article", "title": "An interview", "snippet": "Held on 23 January."}],
                "reference": "https://example.org/Article", "group": "LABEL_SENTINEL", "gold_answer": "GOLD_SENTINEL"}
        llm = FakeLLM([fetch_call(case["reference"])])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(depthsearch_control=True))
        value = await replay_case(agent, case, MemoryTrace())
        self.assertEqual(value["usage"]["calls"], 1)
        self.assertTrue(value["reference_hit"])
        self.assertEqual(len(llm.requests), 1)
        self.assertNotIn("LABEL_SENTINEL", str(llm.requests))
        self.assertNotIn("GOLD_SENTINEL", str(llm.requests))
        self.assertNotIn("reference_url", str(llm.requests))
        self.assertEqual([t["function"]["name"] for t in llm.requests[0][1]], ["web_fetch"])
        self.assertEqual(llm.tool_choices, ["auto"])
