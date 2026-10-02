"""Offline regressions for candidate continuity, source grounding and dual ranking."""
import copy
import json
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from offline import FakeTools
from test_depthsearch_core import call
from test_reader_integrity import FakeLLM, MemoryTrace
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.explorer import Document, ExplorerConfig
from searchgym.jevtree import JevTree, TreeNode
from searchgym.jevtree_state import CandidateMemory, parse_conditions, parse_reading
from searchgym.llm import Reply, Usage
from searchgym.serving import profile_for


QUESTION = "Which film was published in 2019?"
CONDITIONS = [{"id": "C1", "text": "Which film"}, {"id": "C2", "text": "published in 2019"}]
PAGE = "Example Film was published in 2019."
URL = "https://source.example/film"


def reading(relation="supports", quote=PAGE):
    return {"page_title": "Film", "facts": [{"candidate": "Example Film", "condition_id": "C2",
            "relation": relation, "fact": quote, "quote": quote}],
            "leads": [{"name": "Example Film", "quote": quote, "condition_ids": ["C1"]}],
            "missing_condition_ids": ["C1"]}


class CandidateTests(unittest.TestCase):
    def test_question_conditions_cannot_introduce_guessed_country(self):
        self.assertEqual(parse_conditions(json.dumps({"conditions": [c["text"] for c in CONDITIONS]}),
                                          QUESTION), CONDITIONS)
        with self.assertRaises(ValueError):
            parse_conditions('{"conditions": ["from Ghana"]}', QUESTION)

    def test_quotes_and_candidate_names_must_come_from_page(self):
        self.assertEqual(parse_reading(json.dumps(reading()), PAGE, CONDITIONS), reading())
        for invalid in (reading(quote="Example Film was published in 2020."), reading()):
            if invalid["facts"][0]["quote"] == PAGE:
                invalid["facts"][0]["candidate"] = "Invented Film"
            with self.assertRaises(ValueError):
                parse_reading(json.dumps(invalid), PAGE, CONDITIONS)

    def test_candidate_persists_and_unknown_is_not_rejection_evidence(self):
        memory = CandidateMemory()
        memory.ingest(reading(), URL)
        original = copy.deepcopy(memory.candidates)
        with self.assertRaisesRegex(ValueError, "contradicting"):
            memory.update([{"candidate_id": "K1", "action": "verify", "reason": "Check book"},
                           {"candidate_id": "K1", "action": "reject", "reason": "Unknown author",
                            "evidence_ids": ["E1"]}])
        self.assertEqual(memory.candidates, original)  # failed batch is atomic
        memory.ingest({"facts": [], "leads": []}, "https://source.example/unrelated")
        self.assertIn("Example Film", memory.render(CONDITIONS))
        memory.update([{"candidate_id": "K1", "action": "verify", "reason": "Check author"}])
        self.assertEqual(memory.candidates["K1"]["status"], "verifying")
        self.assertIn('"unknown":["C1"]', memory.render(CONDITIONS))

    def test_rejection_retains_candidate_and_new_evidence_reopens_it(self):
        memory = CandidateMemory()
        memory.ingest(reading("contradicts"), URL)
        memory.update([{"candidate_id": "K1", "action": "reject", "reason": "Wrong year",
                        "evidence_ids": ["E1"]}])
        self.assertIn('"status":"rejected"', memory.render(CONDITIONS))
        memory.ingest(reading(), "https://other.example/film")
        self.assertEqual(memory.candidates["K1"]["status"], "retained")
        self.assertEqual(len(memory.candidates), 1)
        self.assertEqual(len(CandidateMemory().candidates), 0)


class PipelineTests(unittest.IsolatedAsyncioTestCase):
    def tree(self, llm, **overrides):
        config = dict(jev=SimpleNamespace(noul=AsyncMock()), llm=llm,
                      fetch=AsyncMock(return_value=Document(URL, PAGE)), reader_prompt="Extract sources",
                      reader_max_tokens=8192, entries=1, branch=3, depth=3, reads=6, floor=.15,
                      jev_page_tokens=20000, visited=set())
        config.update(overrides)
        return JevTree(**config)

    async def test_condition_extraction_runs_once_and_falls_back_without_guesses(self):
        llm = FakeLLM([Reply(text='{"conditions":["Ghana"]}'), Reply(text='invalid')])
        tree, trace, usage = self.tree(llm), MemoryTrace(), Usage()
        await tree.prepare(QUESTION, trace, usage)
        await tree.prepare(QUESTION, trace, usage)
        self.assertEqual(tree.conditions, [{"id": "C1", "text": QUESTION}])
        self.assertEqual(usage.calls, 2)
        self.assertTrue(any(k == "jevtree.conditions_fallback" for k, _ in trace.events))

    async def test_dual_selection_reserves_verification_and_deduplicates(self):
        tree = self.tree(FakeLLM([]), reads=4)
        nodes = [TreeNode(f"https://example.org/{i}", 1, identification=a, verification=b)
                 for i, (a, b) in enumerate([(.99, .9), (.98, .1), (.97, .1), (.96, .1), (.2, .95)])]
        chosen = tree._select_readers(nodes)
        self.assertEqual([n.url.rsplit('/', 1)[-1] for n in chosen], ["0", "4", "1", "2"])
        self.assertEqual(len({n.url for n in chosen}), 4)
        self.assertEqual(tree._select_readers([TreeNode("https://low.example", 1,
                                                      identification=.1, verification=.1)]), [])

    async def test_reader_retries_ungrounded_quote_and_never_receives_main_reasoning(self):
        llm = FakeLLM([Reply(text=json.dumps(reading(quote="Example Film invented fact."))),
                       Reply(text=json.dumps(reading()))])
        tree, trace = self.tree(llm), MemoryTrace()
        tree.conditions = CONDITIONS
        node = TreeNode(URL, 1, document=Document(URL, PAGE))
        await tree._read(node, QUESTION, trace, Usage())
        self.assertEqual(node.reading, reading())
        self.assertEqual(len(llm.requests), 2)
        for messages, _ in llm.requests:
            self.assertNotIn("main_reasoning", json.loads(messages[1]["content"]))
        self.assertTrue(any(k == "jevtree.reader_invalid" for k, _ in trace.events))

    async def test_truncated_reader_never_becomes_candidate_evidence(self):
        llm = FakeLLM([Reply(text=json.dumps(reading()), finish_reason="length"),
                       Reply(text="not JSON")])
        tree = self.tree(llm)
        tree.conditions = CONDITIONS
        node = TreeNode(URL, 1, document=Document(URL, PAGE))
        await tree._read(node, QUESTION, MemoryTrace(), Usage())
        self.assertIsNone(node.reading)
        self.assertIn("failed source/schema validation", node.notes)
        self.assertFalse(tree.memory.candidates)

    async def test_agent_keeps_candidate_through_empty_search_and_final_synthesis(self):
        updates = [{"candidate_id": "K1", "action": "verify", "reason": "Check original book"}]
        llm = FakeLLM([
            Reply(text=json.dumps({"conditions": [c["text"] for c in CONDITIONS]})),
            call("web_search", {"query": "film publication year original book"}),
            Reply(text=json.dumps(reading())),
            call("web_search", {"query": "Example Film original book", "candidate_updates": updates}),
            Reply(text="Example Film"), Reply(text="Example Film"),
        ])
        bodies = []

        async def noul(state, questions, trace, *, usage, context):
            bodies.append(copy.deepcopy(state))
            usage.calls += 1
            usage.attempts += 1
            return {key: .9 for key in questions}

        jev = SimpleNamespace(noul=noul)
        tools, trace = FakeTools(), MemoryTrace()
        tools.search = AsyncMock(return_value=({"organic": [{"link": URL, "title": "Film"}]},
            SimpleNamespace(is_error=False, duration_ms=1, text="search response")))
        tools.fetch = AsyncMock(return_value=Document(URL, PAGE))
        with patch("searchgym.agent.LLM", return_value=llm), patch("searchgym.agent.Jev", return_value=jev):
            agent = SearchAgent(profile_for("gpt-oss"), AgentConfig(
                jev_entries=1, jev_reads=1, max_searches=2, finalize_answer=True), method="jevtree",
                explorer_config=ExplorerConfig(max_depth=1))
        result = await agent.run(QUESTION, "Research", tools, trace)
        self.assertIsNone(result.error)
        self.assertEqual(result.answer, "Example Film")
        self.assertEqual(result.searches, 2)
        self.assertEqual(tools.fetch.await_count, 1)  # second search has no unread pages
        self.assertEqual(len(llm.requests), 6)
        for index in (3, 4, 5):
            self.assertIn("Example Film", str(llm.requests[index][0]))
            self.assertIn("Persistent candidate memory", str(llm.requests[index][0]))
        self.assertIn('"status":"verifying"', str(llm.requests[4][0]))
        schema = llm.requests[1][1][0]["function"]
        self.assertIn("candidate_updates", schema["parameters"]["properties"])
        self.assertNotIn("current reasoning guides", schema["description"])
        self.assertTrue(all("main_reasoning" not in body for body in bodies))
        self.assertTrue(all(body["question_conditions"] == CONDITIONS for body in bodies))
        self.assertTrue(any(k == "jevtree.candidate_update" for k, _ in trace.events))


if __name__ == "__main__":
    unittest.main()
