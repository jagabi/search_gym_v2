"""Offline regressions for free-form reading without condition extraction."""
import copy
import json
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from offline import FakeTools
from test_depthsearch_core import call
from test_reader_integrity import FakeLLM, MemoryTrace
from searchgym.agent import AgentConfig, SearchAgent
from searchgym.config import load_test
from searchgym.explorer import Document, ExplorerConfig
from searchgym.jevtree import JevTree, TreeNode, SEARCH_FOLLOWUP
from searchgym.llm import Reply, Usage
from searchgym.serving import profile_for
from searchgym.runner import Runner, _agent_fingerprint


QUESTION = "Which film was published in 2019?"
PAGE = "Example Film was published in 2019."
URL = "https://source.example/film"


class CandidateTests(unittest.TestCase):
    def test_real_jevtree_config_builds_runner_cache_key_and_tracks_both_scores(self):
        config = load_test("conf.yaml", method="jevtree", model="gpt-oss",
                           benchmark="browsecomp", limit=10)
        # Exercise the production cache path with a nonempty jev_model. Default
        # AgentConfig used in most unit tests skips Jev's fingerprint branch.
        self.assertTrue(config.agent.jev_model)
        runner = Runner.__new__(Runner)
        runner.method = "jevtree"
        runner.profile = profile_for(config.model)
        runner.agent = SimpleNamespace(config=config.agent)
        runner.explorer_config = config.explorer
        runner.explorer_prompt = config.explorer_prompt
        benchmark = SimpleNamespace(build_prompt=lambda item: item.question)
        item = SimpleNamespace(question=QUESTION)
        def key():
            return runner.cache_key(benchmark, item, config.system_prompt)
        original = key()
        self.assertEqual(len(original), 64)
        self.assertEqual(key(), original)
        for name in ("IDENTIFICATION_QUESTION", "VERIFICATION_QUESTION"):
            with patch("searchgym.jevtree." + name, {"type": "noul", "instructions": "changed"}):
                self.assertNotEqual(key(), original)
        with patch("searchgym.jevtree_input.INPUT_VERSION", "changed"):
            self.assertNotEqual(key(), original)
        with patch("searchgym.jevtree.SEARCH_FOLLOWUP", "changed"):
            self.assertNotEqual(key(), original)

    def test_baseline_cache_fingerprint_does_not_include_jev_prompts(self):
        fingerprint = json.loads(_agent_fingerprint(AgentConfig()))
        self.assertFalse(any(k.startswith("jev_") for k in fingerprint))


class PipelineTests(unittest.IsolatedAsyncioTestCase):
    def tree(self, llm, **overrides):
        config = dict(jev=SimpleNamespace(noul=AsyncMock()), llm=llm,
                      fetch=AsyncMock(return_value=Document(URL, PAGE)), reader_prompt="Extract sources",
                      reader_max_tokens=8192, entries=1, branch=3, depth=3, reads=6, floor=.15,
                      jev_page_tokens=20000, visited=set())
        config.update(overrides)
        return JevTree(**config)

    async def test_search_without_pages_never_calls_condition_model(self):
        llm = FakeLLM([])
        tree, trace, usage = self.tree(llm), MemoryTrace(), Usage()
        await tree.run_search('query', [], question=QUESTION, main_reasoning='', trace=trace, usage=usage)
        self.assertEqual(usage.calls, 0)
        self.assertEqual(llm.requests, [])
        self.assertFalse(any('conditions' in k for k, _ in trace.events))

    async def test_dual_selection_reserves_verification_and_deduplicates(self):
        tree = self.tree(FakeLLM([]), reads=4)
        nodes = [TreeNode(f"https://example.org/{i}", 1, identification=a, verification=b)
                 for i, (a, b) in enumerate([(.99, .9), (.98, .1), (.97, .1), (.96, .1), (.2, .95)])]
        chosen = tree._select_readers(nodes)
        self.assertEqual([n.url.rsplit('/', 1)[-1] for n in chosen], ["0", "4", "1", "2"])
        self.assertEqual(len({n.url for n in chosen}), 4)
        self.assertEqual(tree._select_readers([TreeNode("https://low.example", 1,
                                                      identification=.1, verification=.1)]), [])

    async def test_reader_preserves_prose_without_format_or_quote_validation(self):
        text = 'A useful candidate is Example Film; the source suggests a 2019 publication.\nNext, check the author.'
        llm = FakeLLM([Reply(text=text)])
        tree, trace = self.tree(llm), MemoryTrace()
        node = TreeNode(URL, 1, document=Document(URL, PAGE))
        await tree._read(node, QUESTION, trace, Usage())
        self.assertEqual(node.notes, text)
        self.assertEqual(len(llm.requests), 1)
        messages = llm.requests[0][0]
        self.assertEqual(messages[0]['content'], tree.reader_prompt)
        self.assertNotIn('main_reasoning', json.loads(messages[1]['content']))
        self.assertNotIn('question_conditions', json.loads(messages[1]['content']))
        self.assertFalse(any(k in ('jevtree.reader_invalid', 'jevtree.reader_validated') for k, _ in trace.events))

    async def test_truncated_reader_preserves_partial_notes_without_retry(self):
        llm = FakeLLM([Reply(text='Example Film was published', finish_reason='length')])
        tree = self.tree(llm)
        node = TreeNode(URL, 1, document=Document(URL, PAGE))
        await tree._read(node, QUESTION, MemoryTrace(), Usage())
        self.assertEqual(node.notes, 'Example Film was published\n[Reader output truncated.]')
        self.assertEqual(len(llm.requests), 1)

    async def test_empty_reader_retries_once_without_requesting_json(self):
        llm = FakeLLM([Reply(text=''), Reply(text=PAGE)])
        tree = self.tree(llm)
        node = TreeNode(URL, 1, document=Document(URL, PAGE))
        await tree._read(node, QUESTION, MemoryTrace(), Usage())
        self.assertEqual(node.notes, PAGE)
        self.assertEqual(len(llm.requests), 2)
        self.assertIn('free-form prose', llm.requests[1][0][-1]['content'])

    async def test_agent_keeps_freeform_notes_through_empty_search_and_final_synthesis(self):
        llm = FakeLLM([
            call("web_search", {"query": "film publication year original book"}),
            Reply(text=PAGE),
            call("web_search", {"query": "Example Film original book"}),
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
        self.assertEqual(len(llm.requests), 5)
        for request_index, query in [(2, 'film publication year original book'),
                                     (3, 'Example Film original book')]:
            tool_messages = [m['content'] for m in llm.requests[request_index][0] if m['role'] == 'tool']
            suffix = SEARCH_FOLLOWUP.format(query=json.dumps(query, ensure_ascii=False))
            self.assertTrue(tool_messages[-1].endswith(suffix))
            self.assertEqual(tool_messages[-1].count('Next action:'), 1)
        for index in (2, 3, 4):
            self.assertIn("Example Film", str(llm.requests[index][0]))
            self.assertIn(PAGE, str(llm.requests[index][0]))
            self.assertNotIn("Persistent candidate memory", str(llm.requests[index][0]))
        schema = llm.requests[0][1][0]["function"]
        self.assertNotIn("candidate_updates", schema["parameters"]["properties"])
        self.assertNotIn("current reasoning guides", schema["description"])
        self.assertTrue(all("main_reasoning" not in body for body in bodies))
        self.assertTrue(all('question_conditions' not in body for body in bodies))
        self.assertFalse(any('conditions' in k for k, _ in trace.events))
        self.assertFalse(any(k == "jevtree.candidate_update" for k, _ in trace.events))

    async def test_followup_stays_last_when_search_result_is_trimmed(self):
        agent = object.__new__(SearchAgent)
        agent.config = AgentConfig(context_limit=600)
        agent.llm = FakeLLM([])
        suffix = '\n\n' + SEARCH_FOLLOWUP.format(query=json.dumps('new query'))
        from searchgym.agent import RunResult
        output, truncated = await agent._fit('source text ' * 1000, RunResult(), suffix=suffix)
        self.assertTrue(truncated)
        self.assertTrue(output.endswith(suffix))
        self.assertTrue(output.startswith('source text'))


if __name__ == "__main__":
    unittest.main()
