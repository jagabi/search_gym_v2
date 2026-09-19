"""Retry saved failures without rerunning or regrading completed answers."""
from __future__ import annotations

import asyncio
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from .report import summarize
from .runner import Record, _result_from, _DEPLOYMENT_ONLY
from .scoring import Judgement


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic(path, text):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


class _SavedJudgement(Judgement):
    """Use the published rounded metrics; never invent missing judge details."""
    def __init__(self, row):
        super().__init__(error=row.get("judge_error"))
        self.row = row

    @property
    def category(self):
        return self.row["correct"]

    def metrics(self):
        return {k: self.row[k] for k in ("f1", "precision", "recall", "accuracy")}


@dataclass
class RetryPlan:
    rows: dict
    records: dict
    items: dict
    targets: dict  # index -> agent or judge


def plan_retry(out, items, config, profile):
    """Read-only validation. Cached successes are not required."""
    saved = _read(out / "config.json")
    current = {"method": config.method, "model": profile.repo,
               "agent": asdict(config.agent),
               "explorer": asdict(config.explorer) if config.uses_explorer else None,
               "judge": asdict(config.judge)}
    for key in current:
        a, b = saved.get(key), current[key]
        if key == "agent":
            a = {k: v for k, v in (a or {}).items() if k not in _DEPLOYMENT_ONLY}
            b = {k: v for k, v in b.items() if k not in _DEPLOYMENT_ONLY}
        if a != b:
            raise ValueError(f"기존 실행과 {key} 설정이 다릅니다. 같은 설정으로 재시도하세요.")
    for filename, prompt in (("prompt.txt", config.system_prompt),
                             ("explorer_prompt.txt", config.explorer_prompt)):
        if filename == "explorer_prompt.txt" and not config.uses_explorer:
            continue
        if (out / filename).read_text(encoding="utf-8").strip() != prompt.strip():
            raise ValueError(f"기존 실행과 {filename}이 다릅니다.")
    rows = {}
    for line in (out / "records.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["index"] in rows:
            raise ValueError("records.jsonl에 중복 문항이 있습니다.")
        rows[row["index"]] = row
    items = {item.index: item for item in items}
    if set(rows) != set(items):
        raise ValueError("저장된 문항과 실행 대상이 다릅니다. 기존 --limit/--split/데이터셋을 맞추세요. "
                         "미완료 실행은 일반 --resume을 사용하세요.")
    records, targets = {}, {}
    for i, row in rows.items():
        qdir = out / f"q{i:05d}"
        response = _read(qdir / "response.json")
        if response["question"] != items[i].question or response["gold_answer"] != items[i].answer:
            raise ValueError(f"q{i:05d}의 질문 또는 정답이 기존 실행과 다릅니다.")
        result = _result_from(response)
        records[i] = Record(i, row["category"], row["score"], _SavedJudgement(row), result,
                            cached=row.get("cached", False), dir=row["dir"])
        if not result.answer.strip() or result.error or row.get("error"):
            targets[i] = "agent"
        elif row.get("judge_error"):
            targets[i] = "judge"
    return RetryPlan(rows, records, items, targets)


async def retry_failed(runner, plan, benchmark, system_prompt, on_record=None):
    """Archive originals, replace each failure once, and checkpoint the full run."""
    if not plan.targets:
        return list(plan.records.values())
    from .tools import WebTools

    out = runner.run_dir
    snapshot = out / "retry_history" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    snapshot.mkdir(parents=True)
    for name in ("records.jsonl", "summary.json", "config.json", "prompt.txt", "explorer_prompt.txt"):
        if (out / name).exists():
            shutil.copy2(out / name, snapshot / name)
    for i in plan.targets:
        shutil.copytree(out / f"q{i:05d}", snapshot / f"q{i:05d}")
    manifest = {"targets": plan.targets, "completed": [],
                "agent_config": asdict(runner.agent.config),
                "selection": "empty answer / run error: regenerate; judge error only: regrade"}
    manifest["agent_config"].pop("api_key", None)
    metadata = _read(out / "summary.json") if (out / "summary.json").exists() else {}

    def checkpoint():
        _atomic(out / "records.jsonl", "".join(json.dumps(row, ensure_ascii=False) + "\n"
                                                for row in plan.rows.values()))
        summary = {**metadata, **summarize(plan.records.values()),
                   "cache": runner.cache_stats(),
                   "retry": {"history": str(snapshot.relative_to(out)),
                             "requested": len(plan.targets), "completed": len(manifest["completed"])}}
        _atomic(out / "summary.json", json.dumps(summary, ensure_ascii=False, indent=2))
        _atomic(snapshot / "attempt.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    checkpoint()
    original_records_path = runner._records_path
    runner._records_path = snapshot / "attempt_records.jsonl"
    semaphore = asyncio.Semaphore(runner.workers)
    try:
        async with WebTools(search_results=runner.agent.config.search_results) as tools:
            async def one(i, kind):
                async with semaphore:
                    item = plan.items[i]
                    if kind == "agent":
                        record = await runner.run_one(benchmark, item, system_prompt, tools, force=True)
                    else:
                        record = plan.records[i]
                        record.judgement = runner._grade(benchmark, item, record.result.answer)
                        record.score = 0.0 if record.judgement.error else record.judgement.metrics()["f1"]
                        runner._append(record)
                    plan.records[i] = record
                    plan.rows[i] = record.as_dict()
                    manifest["completed"].append(i)
                    checkpoint()
                    if on_record:
                        on_record(record, len(plan.targets))
            tasks = [asyncio.create_task(one(i, kind)) for i, kind in plan.targets.items()]
            try:
                await asyncio.gather(*tasks)
            finally:
                for task in tasks:
                    if not task.done():
                        task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        runner._records_path = original_records_path
    return list(plan.records.values())
