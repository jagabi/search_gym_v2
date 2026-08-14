"""문항 실행 + 채점 + 기록.

train과 eval이 공유하는 단 하나의 실행 경로다. 하는 일은 넷뿐이다.

    1. 디스크 캐시 조회 — (모델, 에이전트 설정, 시스템 프롬프트, 질문) 해시
    2. 에이전트 실행 → 문항별 JSONL 트레이스
    3. 판정 → 캐시
    4. 한 줄 요약을 `records.jsonl`에 append

같은 (프롬프트, 문항)을 여러 번 평가하는 것이 GEPA의 정상 동작이므로 캐시가 곧
비용이다. 진행 중인 키는 잠가서 같은 문항을 동시에 두 번 태우지 않는다.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .agent import AgentConfig, RunResult, SearchAgent
from .benchmarks import Benchmark, Item
from .judge import Judge
from .paths import resolve
from .scoring import Judgement, from_dict
from .serving import ServeProfile
from .trace import Trace

__all__ = ["Cache", "Record", "Runner"]


@dataclass(slots=True)
class Record:
    """문항 하나의 결과 요약. records.jsonl의 한 줄이자 리포트의 입력."""

    index: int
    category: str
    score: float
    judgement: Judgement
    result: RunResult
    cached: bool = False
    dir: str = ""

    def as_dict(self) -> dict[str, Any]:
        metrics = self.judgement.metrics()
        return {
            "index": self.index,
            "category": self.category,
            "score": round(self.score, 4),
            "correct": self.judgement.category,
            "judge_error": self.judgement.error,
            **{k: round(v, 4) for k, v in metrics.items()},
            "searches": self.result.searches,
            "fetches": self.result.fetches,
            "turns": self.result.turns,
            "answer_chars": len(self.result.answer),
            "stop_reason": self.result.stop_reason,
            "latency_s": round(self.result.latency_ms / 1000, 1),
            "input_tokens": self.result.usage.input_tokens,
            "output_tokens": self.result.usage.output_tokens,
            "reasoning_tokens": self.result.usage.reasoning_tokens,
            "error": self.result.error,
            "cached": self.cached,
            "dir": self.dir,
        }


class Cache:
    """내용 해시 → JSON 한 덩어리. 파일 하나당 항목 하나라 동시 쓰기에 안전하다."""

    def __init__(self, root: Path | str, enabled: bool = True) -> None:
        self.root = Path(root)
        self.enabled = enabled
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> dict[str, Any] | None:
        if not self.enabled:
            return None
        path = self._path(key)
        if not path.exists():
            self.misses += 1
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.misses += 1
            return None  # 깨진 항목은 없는 셈 친다
        self.hits += 1
        return payload if isinstance(payload, dict) else None

    def has(self, key: str) -> bool:
        """통계를 건드리지 않는 조회. 돌리기 전에 남은 문항을 세는 데 쓴다."""
        return self.enabled and self._path(key).exists()

    def put(self, key: str, payload: dict[str, Any]) -> None:
        if not self.enabled:
            return
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, default=str), encoding="utf-8")
        tmp.replace(path)

    def _path(self, key: str) -> Path:
        # 한 디렉터리에 파일 수만 개가 쌓이면 느려지므로 앞 두 글자로 쪼갠다.
        return self.root / key[:2] / f"{key}.json"


def digest(*parts: str) -> str:
    hasher = hashlib.sha256()
    for part in parts:
        hasher.update(part.encode("utf-8"))
        hasher.update(b"\x00")
    return hasher.hexdigest()


class Runner:
    """벤치마크 문항들을 실행하고 채점한다."""

    def __init__(
        self,
        profile: ServeProfile,
        agent_config: AgentConfig,
        judge: Judge,
        run_dir: Path,
        cache_root: Path | str = "runs/_cache",
        use_cache: bool = True,
        workers: int = 1,
    ) -> None:
        self.profile = profile
        self.agent = SearchAgent(profile, agent_config)
        self.judge = judge
        self.run_dir = run_dir
        self.workers = max(1, workers)
        root = resolve(cache_root)
        self._agent_cache = Cache(root / "agent", use_cache)
        self._judge_cache = Cache(root / "judge", use_cache)
        self._locks: dict[str, asyncio.Lock] = {}
        self._records_lock = threading.Lock()
        self._records_path = run_dir / "records.jsonl"

    # --- 공개 API -----------------------------------------------------------

    async def run_all(
        self,
        benchmark: Benchmark,
        items: Iterable[Item],
        system_prompt: str,
        score_field: str = "f1",
        stage: str = "",
    ) -> list[Record]:
        """문항들을 동시에 실행한다. 순서는 입력 순서대로 돌려준다."""
        from .tools import WebTools

        collected = list(items)
        semaphore = asyncio.Semaphore(self.workers)

        async with WebTools() as tools:
            async def one(item: Item) -> Record:
                async with semaphore:
                    return await self.run_one(
                        benchmark, item, system_prompt, tools, score_field, stage
                    )

            return list(await asyncio.gather(*(one(item) for item in collected)))

    async def run_one(
        self,
        benchmark: Benchmark,
        item: Item,
        system_prompt: str,
        tools: Any,
        score_field: str = "f1",
        stage: str = "",
    ) -> Record:
        key = self.cache_key(benchmark, item, system_prompt)
        # 같은 키가 이미 돌고 있으면 끝날 때까지 기다렸다가 캐시에서 집는다.
        lock = self._locks.setdefault(key, asyncio.Lock())
        async with lock:
            result, cached, qdir = await self._execute(
                benchmark, item, system_prompt, tools, key, stage
            )

        judgement = self._grade(benchmark, item, result.answer)
        score = 0.0 if judgement.error else float(judgement.metrics()[score_field])

        record = Record(
            index=item.index,
            category=item.category,
            score=score,
            judgement=judgement,
            result=result,
            cached=cached,
            dir=qdir,
        )
        self._append(record)
        return record

    def cache_key(self, benchmark: Benchmark, item: Item, system_prompt: str) -> str:
        """캐시 키. **실행 디렉터리와 무관하다** — 그래서 이어 돌리기가 성립한다."""
        return digest(
            "agent/1", self.profile.repo, _agent_fingerprint(self.agent.config),
            system_prompt, benchmark.build_prompt(item),
        )

    def pending(
        self, benchmark: Benchmark, items: Iterable[Item], system_prompt: str
    ) -> list[Item]:
        """아직 캐시에 없는 문항들. 실제로 모델을 태울 것만 남는다."""
        return [
            item
            for item in items
            if not self._agent_cache.has(self.cache_key(benchmark, item, system_prompt))
        ]

    def cache_stats(self) -> dict[str, int]:
        return {
            "agent_hits": self._agent_cache.hits,
            "agent_misses": self._agent_cache.misses,
            "judge_hits": self._judge_cache.hits,
            "judge_misses": self._judge_cache.misses,
        }

    # --- 내부 ---------------------------------------------------------------

    async def _execute(
        self, benchmark: Benchmark, item: Item, system_prompt: str, tools: Any, key: str, stage: str
    ) -> tuple[RunResult, bool, str]:
        # 빈 응답은 캐시에서 꺼내 쓰지 않는다. 대개 일시적 실패라 다시 돌리면 살아난다.
        if (payload := self._agent_cache.get(key)) and (payload.get("answer") or "").strip():
            return _result_from(payload), True, payload.get("dir", "")

        # 문항 하나 = 디렉터리 하나. 이름은 번호만 쓴다.
        #   <stage>/q00022/ trace.jsonl · response.json · search_o1.json
        # stage는 한 실행 안에서 국면이 나뉠 때만 쓴다(train의 optimize 등).
        # eval은 이미 벤치마크별로 run_dir이 갈려 있어 비워 둔다.
        qdir = (self.run_dir / stage if stage else self.run_dir) / f"q{item.index:05d}"
        qdir.mkdir(parents=True, exist_ok=True)
        trace = Trace(qdir / "trace.jsonl", run_id=f"{stage or 'run'}-q{item.index}")

        result = await self.agent.run(
            benchmark.build_prompt(item), system_prompt or None, tools, trace
        )

        _write(
            qdir / "response.json",
            {
                "index": item.index,
                "question": item.question,
                "gold_answer": item.answer,
                "category": item.category,
                "model": self.profile.repo,
                "system_prompt": system_prompt,
                **result.as_response(),
            },
        )
        # 정제는 요청(직전 추론·검색어·jina 원문)과 결과를 통째로 따로 남긴다.
        if result.refinements:
            _write(qdir / "search_o1.json", result.refinements)

        relative = str(qdir.relative_to(self.run_dir))
        # 실패한 실행과 빈 응답은 캐시하지 않는다.
        if result.error is None and result.answer.strip():
            self._agent_cache.put(key, {**result.as_dict(), "dir": relative})
        return result, False, relative

    def _grade(self, benchmark: Benchmark, item: Item, answer: str) -> Judgement:
        if not answer.strip():
            return Judgement(error="empty_response")
        key = digest("judge/1", self.judge.model, benchmark.name, item.question, answer)
        if payload := self._judge_cache.get(key):
            return from_dict(payload)
        judgement = self.judge.grade(benchmark, item, answer)
        if judgement.error is None:
            self._judge_cache.put(key, judgement.as_dict())
        return judgement

    def _append(self, record: Record) -> None:
        line = json.dumps(record.as_dict(), ensure_ascii=False, default=str)
        with self._records_lock:
            self._records_path.parent.mkdir(parents=True, exist_ok=True)
            with self._records_path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")


def _agent_fingerprint(config: AgentConfig) -> str:
    """캐시 키에 들어갈 에이전트 설정. 결과에 영향을 주는 값만 넣는다."""
    return "|".join(
        str(v)
        for v in (
            config.max_tokens, config.max_searches, config.max_fetches,
            config.max_turns, config.refine_fetched, config.reasoning_effort,
        )
    )


def _write(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )


def _result_from(payload: dict[str, Any]) -> RunResult:
    """캐시에 담긴 슬림 결과를 되살린다(도구 결과 본문과 정제 원문은 없다)."""
    from .agent import Step
    from .trace import ToolCall, Usage

    return RunResult(
        answer=payload.get("answer", ""),
        steps=[
            Step(
                turn=s.get("turn", 0),
                reasoning=s.get("reasoning", ""),
                text=s.get("text", ""),
                tool_calls=[
                    ToolCall(
                        name=c["name"],
                        arguments=c.get("arguments") or {},
                        result_chars=c.get("result_chars", 0),
                        is_error=c.get("is_error", False),
                        refused=c.get("refused", False),
                        duration_ms=c.get("duration_ms", 0.0),
                    )
                    for c in s.get("tool_calls") or []
                ],
            )
            for s in payload.get("steps") or []
        ],
        usage=Usage(**{k: v for k, v in (payload.get("usage") or {}).items()}),
        turns=payload.get("turns", 0),
        stop_reason=payload.get("stop_reason", ""),
        latency_ms=payload.get("latency_ms", 0.0),
        context_tokens=payload.get("context_tokens", 0),
    )
