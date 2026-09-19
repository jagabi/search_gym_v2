"""Saved-run retry tests; all generation, grading and web access are fake."""
import json
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import test as cli
from searchgym.agent import RunResult
from searchgym.config import load_test
from searchgym.report import summarize
from searchgym.retry import plan_retry, retry_failed
from searchgym.runner import Record, Runner
from searchgym.scoring import Judgement
from searchgym.serving import profile_for


class FakeWeb:
    def __init__(self, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


class RetryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.config = load_test(method="depthsearch")
        self.profile = profile_for(self.config.model)
        self.items = [SimpleNamespace(index=i, question=f"Q{i}", answer="A", category="Test")
                      for i in range(1, 6)]
        self.benchmark = SimpleNamespace(name="fake", build_prompt=lambda item: item.question)
        cli._write_run_config(self.out, self.config, self.profile, Path("fake.json"), self.items)
        self.rows = []
        self.records = []
        # Normal wrong answer, empty response, judge failure, run failure, normal correct answer.
        for item, answer, error, judge_error in zip(
                self.items, ["wrong", "", "A", "unfinished", "A"],
                [None, None, None, "timeout", None],
                [None, "empty_response", "judge timeout", None, None]):
            result = RunResult(answer=answer, error=error,
                               stop_reason="max_turns" if not answer else "answered")
            judgement = Judgement(parts=[("A", answer == "A")], error=judge_error)
            record = Record(item.index, "Test", 0 if judge_error else judgement.metrics()["f1"],
                            judgement, result, dir=f"q{item.index:05d}")
            qdir = self.out / record.dir
            qdir.mkdir()
            self.write(qdir / "response.json", {"question": item.question, "gold_answer": item.answer,
                                               **result.as_response()})
            (qdir / "trace.jsonl").write_text("ORIGINAL TRACE", encoding="utf-8")
            self.write(qdir / "explorer.json", ["OLD TREE"])
            self.rows.append(record.as_dict())
            self.records.append(record)
        (self.out / "records.jsonl").write_text(
            "".join(json.dumps(row) + "\n" for row in self.rows), encoding="utf-8")
        self.write(self.out / "summary.json", {"method": "depthsearch", **summarize(self.records)})

    def write(self, path, data):
        path.write_text(json.dumps(data), encoding="utf-8")

    def plan(self):
        return plan_retry(self.out, self.items, self.config, self.profile)

    def runner(self):
        judge = SimpleNamespace(model="fake", grade=lambda *args: Judgement(parts=[("A", True)]))
        with patch("searchgym.agent.LLM", return_value=SimpleNamespace(aclose=AsyncMock())):
            runner = Runner(self.profile, self.config.agent, judge, self.out,
                            explorer_config=self.config.explorer, explorer_prompt=self.config.explorer_prompt,
                            cache_root=self.out / "cache")
        async def run(*args):
            args[-1].event("fresh.retry")
            return RunResult(answer="A", stop_reason="answered")
        runner.agent.run = AsyncMock(side_effect=run)
        return runner

    def test_selection_preserves_normal_zero_without_cache(self):
        before = (self.out / "records.jsonl").read_bytes()
        plan = self.plan()
        self.assertEqual(plan.targets, {2: "agent", 3: "judge", 4: "agent"})
        self.assertEqual((self.out / "records.jsonl").read_bytes(), before)
        self.assertFalse((self.out / "retry_history").exists())

    def test_wrong_items_or_changed_settings_are_rejected_before_writing(self):
        with self.assertRaisesRegex(ValueError, "문항"):
            plan_retry(self.out, self.items[:2], self.config, self.profile)
        self.config.agent.max_searches += 1
        with self.assertRaisesRegex(ValueError, "agent"):
            self.plan()
        self.assertFalse((self.out / "retry_history").exists())

    def test_deployment_endpoint_can_change(self):
        self.config.agent.base_url = "http://changed.example/v1"
        self.assertEqual(len(self.plan().targets), 3)

    async def test_retries_only_failures_bypasses_agent_cache_and_updates_full_summary(self):
        runner = self.runner()
        plan = self.plan()
        good_bytes = (self.out / "q00001/response.json").read_bytes()
        for i in (2, 4):
            key = runner.cache_key(self.benchmark, self.items[i - 1], self.config.system_prompt)
            runner._agent_cache.put(key, {"answer": "STALE CACHED ANSWER"})
        with patch("searchgym.tools.WebTools", FakeWeb):
            result = await retry_failed(runner, plan, self.benchmark, self.config.system_prompt)
        self.assertEqual(runner.agent.run.await_count, 2)
        self.assertEqual(len(result), 5)
        rows = [json.loads(s) for s in (self.out / "records.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0], self.rows[0])
        self.assertEqual(rows[4], self.rows[4])
        self.assertEqual((self.out / "q00001/response.json").read_bytes(), good_bytes)
        summary = json.loads((self.out / "summary.json").read_text())
        self.assertEqual((summary["n"], summary["f1"], summary["empty_answers"]), (5, .8, 0))
        self.assertEqual(summary["retry"]["completed"], 3)
        backup = next((self.out / "retry_history").iterdir())
        self.assertEqual((backup / "q00002/trace.jsonl").read_text(), "ORIGINAL TRACE")
        self.assertNotIn("ORIGINAL", (self.out / "q00002/trace.jsonl").read_text())
        self.assertFalse((self.out / "q00002/explorer.json").exists())
        self.assertEqual((self.out / "q00003/trace.jsonl").read_text(), "ORIGINAL TRACE")
        self.assertEqual(self.plan().targets, {})

    async def test_interruption_keeps_all_records_and_completed_updates(self):
        runner = self.runner()
        runner.agent.run = AsyncMock(side_effect=[RunResult(answer="A", stop_reason="answered"),
                                                RuntimeError("interrupted")])
        with patch("searchgym.tools.WebTools", FakeWeb):
            with self.assertRaisesRegex(RuntimeError, "interrupted"):
                await retry_failed(runner, self.plan(), self.benchmark, self.config.system_prompt)
        summary = json.loads((self.out / "summary.json").read_text())
        self.assertEqual(summary["n"], 5)
        self.assertEqual(summary["retry"]["completed"], 2)
        self.assertEqual(self.plan().targets, {4: "agent"})
        self.assertEqual(runner._records_path, self.out / "records.jsonl")

    async def test_no_failures_does_not_open_web_or_write(self):
        plan = self.plan()
        plan.targets.clear()
        runner = self.runner()
        with patch("searchgym.tools.WebTools", side_effect=AssertionError("Must not open web")):
            records = await retry_failed(runner, plan, self.benchmark, self.config.system_prompt)
        self.assertEqual(len(records), 5)
        self.assertFalse((self.out / "retry_history").exists())

    async def test_cli_dry_run_does_not_construct_judge_or_runner(self):
        with patch.object(cli, "_resolve_dir", return_value=self.out), \
             patch.object(cli, "load_benchmark", return_value=SimpleNamespace(load=lambda **kw: self.items)), \
             patch.object(cli, "Judge", side_effect=AssertionError("Must not construct judge")), \
             patch.object(cli, "Runner", side_effect=AssertionError("Must not construct runner")):
            self.assertEqual(await cli.main_async(["--method", "depthsearch", "--resume", "--retry-errors", "--dry-run"]), 0)
        self.assertFalse((self.out / "retry_history").exists())


if __name__ == "__main__":
    unittest.main()
