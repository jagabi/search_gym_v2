"""Ensure the cheap selector diagnostic cannot fetch or expose evaluation labels."""
import unittest
from unittest.mock import patch

from probe_selective_entry import replay_case
from test_reader_integrity import FakeLLM, MemoryTrace
from test_selective_entry import control
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.serving import profile_for


class ProbeTests(unittest.IsolatedAsyncioTestCase):
    async def test_replay_makes_one_model_call_without_target_labels(self):
        case = {"id": 999, "turn": 2, "question": "Which article contains the date?",
                "entries": [{"link": "https://example.org/Article", "title": "An interview", "snippet": "Held on 23 January."}],
                "reference": "https://example.org/Article", "group": "LABEL_SENTINEL", "gold_answer": "GOLD_SENTINEL"}
        llm = FakeLLM([control("S1")])
        with patch("searchgym.agent.LLM", return_value=llm):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(depthsearch_control=True))
        value = await replay_case(agent, case, MemoryTrace())
        self.assertEqual(value["usage"]["calls"], 1)
        self.assertTrue(value["reference_hit"])
        self.assertEqual(len(llm.requests), 1)
        self.assertNotIn("LABEL_SENTINEL", str(llm.requests))
        self.assertNotIn("GOLD_SENTINEL", str(llm.requests))
        self.assertNotIn("reference_url", str(llm.requests))
        self.assertIsNone(llm.requests[0][1])
