"""문항 실행 + 채점 + 기록.

test.py 와 train.py 가 공유하는 단 하나의 실행 경로다. 하는 일은 넷뿐이다.

    1. 디스크 캐시 조회 — (방법, 모델, 설정, 프롬프트 둘, 질문) 해시
    2. 에이전트 실행 → 문항별 JSONL 트레이스
    3. 판정 → 캐시
    4. 한 줄 요약을 `records.jsonl` 에 append

같은 (프롬프트, 문항)을 여러 번 평가하는 것이 GEPA 의 정상 동작이므로 캐시가 곧
비용이다. 진행 중인 키는 잠가서 같은 문항을 동시에 두 번 태우지 않는다.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import threading
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .agent import AgentConfig, RunResult, SearchAgent, Step
from .benchmarks import Benchmark, Item
from .explorer import ExplorerConfig
from .judge import Judge
from .llm import Usage
from .paths import resolve
from .scoring import Judgement, from_dict
from .serving import ServeProfile
from .trace import ToolCall, Trace
from .tree import write_svg

__all__ = ["Cache", "Record", "Runner"]

# 캐시 키 버전. 실행 결과의 의미가 바뀌면 올린다.
# agent/16 — 문서 예산을 균등분할에서 워터필링으로 바꿨다(작은 문서가 남긴
# 몫을 큰 문서에 돌려준다). search-o1 이 보는 내용이 달라지므로 이전 결과는 못 쓴다.
CACHE_VERSION = "agent/35"
JUDGE_VERSION = "judge/1"


@dataclass(slots=True)
class Record:
    """문항 하나의 결과 요약. records.jsonl 의 한 줄이자 리포트의 입력."""

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
            "fetch_attempts": self.result.fetch_attempts,
            "fetch_failures": self.result.fetch_failures,
            "search_attempts": self.result.search_attempts,
            "search_failures": self.result.search_failures,
            "expansion_nodes": self.result.expansion_nodes,
            "nodes_by_depth": self.result.budget.get("nodes_by_depth") or {},
            "links_stripped": self.result.budget.get("links_stripped") or 0,
            "duplicates": self.result.budget.get("duplicates") or 0,
            "off_page": self.result.budget.get("off_page") or 0,
            "same_site": self.result.budget.get("same_site") or 0,
            "repeats": self.result.budget.get("repeats") or 0,
            "visited_urls": self.result.budget.get("visited") or 0,
            "max_depth_reached": self.result.max_depth_reached,
            "explorer_calls": self.result.explorer_calls,
            "dead_dives": self.result.dead_dives,
            "budget_exhausted": self.result.budget_exhausted,
            "context_exhausted": self.result.context_exhausted,
            "turns": self.result.turns,
            "answer_chars": len(self.result.answer),
            "stop_reason": self.result.stop_reason,
            "latency_s": round(self.result.latency_ms / 1000, 1),
            "input_tokens": self.result.usage.input_tokens,
            "output_tokens": self.result.usage.output_tokens,
            "reasoning_tokens": self.result.usage.reasoning_tokens,
            "llm_calls": self.result.usage.calls,
            "error": self.result.error,
            "reader_stats": self.result.reader_stats,
            "invalid_tool_calls": self.result.invalid_tool_calls,
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
        method: str = "depthsearch",
        explorer_config: ExplorerConfig | None = None,
        explorer_prompt: str = "",
        cache_root: Path | str = "runs/_cache",
        use_cache: bool = True,
        workers: int = 1,
    ) -> None:
        self.profile = profile
        self.method = method
        self.explorer_config = explorer_config
        self.explorer_prompt = explorer_prompt
        self.agent = SearchAgent(
            profile,
            agent_config,
            method=method,
            explorer_config=explorer_config,
            explorer_prompt=explorer_prompt,
        )
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
        explorer_prompt: str | None = None,
        score_field: str = "f1",
        stage: str = "",
        on_record: Any = None,
    ) -> list[Record]:
        """문항들을 동시에 실행한다. 순서는 입력 순서대로 돌려준다."""
        from .tools import WebTools

        collected = list(items)
        semaphore = asyncio.Semaphore(self.workers)

        async with WebTools(search_results=self.agent.config.search_results) as tools:
            async def one(item: Item) -> Record:
                async with semaphore:
                    record = await self.run_one(
                        benchmark, item, system_prompt, tools,
                        explorer_prompt=explorer_prompt,
                        score_field=score_field, stage=stage,
                    )
                    if on_record is not None:
                        on_record(record, len(collected))
                    return record

            return list(await asyncio.gather(*(one(item) for item in collected)))

    async def run_one(
        self,
        benchmark: Benchmark,
        item: Item,
        system_prompt: str,
        tools: Any,
        explorer_prompt: str | None = None,
        score_field: str = "f1",
        stage: str = "",
    ) -> Record:
        explorer_prompt = (
            self.explorer_prompt if explorer_prompt is None else explorer_prompt
        )
        key = self.cache_key(benchmark, item, system_prompt, explorer_prompt)
        # 같은 키가 이미 돌고 있으면 끝날 때까지 기다렸다가 캐시에서 집는다.
        lock = self._locks.setdefault(key, asyncio.Lock())
        async with lock:
            result, cached, qdir = await self._execute(
                benchmark, item, system_prompt, explorer_prompt, tools, key, stage
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

    def cache_key(
        self,
        benchmark: Benchmark,
        item: Item,
        system_prompt: str,
        explorer_prompt: str | None = None,
    ) -> str:
        """캐시 키. **실행 디렉터리와 무관하다** — 그래서 이어 돌리기가 성립한다.

        결과에 영향을 주는 것은 전부 들어가야 한다. 특히 method 와 explorer 설정이
        빠지면 depth 1 결과를 depth 3 실행이 조용히 재사용한다.
        """
        return digest(
            CACHE_VERSION,
            self.method,
            self.profile.repo,
            _agent_fingerprint(self.agent.config),
            _explorer_fingerprint(self.explorer_config, self.method),
            system_prompt,
            self.explorer_prompt if explorer_prompt is None else explorer_prompt,
            benchmark.build_prompt(item),
        )

    def pending(
        self,
        benchmark: Benchmark,
        items: Iterable[Item],
        system_prompt: str,
        explorer_prompt: str | None = None,
    ) -> list[Item]:
        """아직 캐시에 없는 문항들. 실제로 모델을 태울 것만 남는다."""
        return [
            item
            for item in items
            if not self._agent_cache.has(
                self.cache_key(benchmark, item, system_prompt, explorer_prompt)
            )
        ]

    def cache_stats(self) -> dict[str, int]:
        return {
            "agent_hits": self._agent_cache.hits,
            "agent_misses": self._agent_cache.misses,
            "judge_hits": self._judge_cache.hits,
            "judge_misses": self._judge_cache.misses,
        }

    async def aclose(self) -> None:
        await self.agent.aclose()

    # --- 내부 ---------------------------------------------------------------

    async def _execute(
        self,
        benchmark: Benchmark,
        item: Item,
        system_prompt: str,
        explorer_prompt: str,
        tools: Any,
        key: str,
        stage: str,
    ) -> tuple[RunResult, bool, str]:
        # 빈 응답은 캐시에서 꺼내 쓰지 않는다. 대개 일시적 실패라 다시 돌리면 살아난다.
        if (payload := self._agent_cache.get(key)) and (payload.get("answer") or "").strip():
            return _result_from(payload), True, payload.get("dir", "")

        # 문항 하나 = 디렉터리 하나.
        #   <stage>/q00022/ trace.jsonl · response.json · explorer.json
        qdir = (self.run_dir / stage if stage else self.run_dir) / f"q{item.index:05d}"
        qdir.mkdir(parents=True, exist_ok=True)
        trace = Trace(qdir / "trace.jsonl", run_id=f"{stage or 'run'}-q{item.index}")

        agent = self.agent
        if explorer_prompt != agent.explorer_prompt:
            # GEPA 가 explorer 프롬프트를 바꿔 가며 부른다. 클라이언트는 공유한다.
            agent = SearchAgent(
                self.profile,
                self.agent.config,
                method=self.method,
                explorer_config=self.explorer_config,
                explorer_prompt=explorer_prompt,
            )
            agent.llm = self.agent.llm

        result = await agent.run(
            benchmark.build_prompt(item), system_prompt or None, tools, trace
        )

        _write(
            qdir / "response.json",
            {
                "index": item.index,
                "question": item.question,
                "gold_answer": item.answer,
                "category": item.category,
                "method": self.method,
                "model": self.profile.repo,
                "system_prompt": system_prompt,
                "explorer_prompt": explorer_prompt,
                **result.as_response(),
            },
        )
        # explorer 트리는 통째로 따로 남긴다. 확장 정책 분석의 원본이다.
        if result.explorations:
            _write(qdir / "explorer.json", result.explorations)

        # 탐색 궤적 그림. 세 방법 모두 그린다 — ragent/search-o1 이 평면이라는 것을
        # 눈으로 확인할 수 있어야 depthsearch 의 트리가 의미를 갖는다.
        write_svg(
            qdir / "tree.svg",
            result,
            question=item.question,
            subtitle=(
                f"{self.method} · searches {result.searches} · fetches {result.fetches}"
                f" · expansion {result.expansion_nodes} · depth {result.max_depth_reached}"
                f" · {result.stop_reason}"
            ),
        )

        relative = str(qdir.relative_to(self.run_dir))
        # 실패한 실행과 빈 응답은 캐시하지 않는다.
        if (result.error is None and result.answer.strip()
                and result.stop_reason in {"answered", "finalized"}
                and not any(result.reader_stats.get(k, 0) for k in (
                    "empty_output", "reader_error", "invalid_output", "truncated", "context_limit",
                    "navigation_errors",
                ))):
            self._agent_cache.put(key, {**result.as_dict(), "dir": relative})
        return result, False, relative

    def _grade(self, benchmark: Benchmark, item: Item, answer: str) -> Judgement:
        if not answer.strip():
            return Judgement(error="empty_response")
        key = digest(JUDGE_VERSION, self.judge.model, benchmark.name, item.question, answer)
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
    return json.dumps({k: v for k, v in asdict(config).items() if k != "api_key"},
                      sort_keys=True, ensure_ascii=False)


def _explorer_fingerprint(config: ExplorerConfig | None, method: str) -> str:
    """explorer 설정. **깊이와 예산이 반드시 들어가야** 조건 간 캐시가 안 섞인다."""
    if config is None or method == "ragent":
        return "none"
    return json.dumps(asdict(config), sort_keys=True, ensure_ascii=False)


def _write(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )


def _result_from(payload: dict[str, Any]) -> RunResult:
    """캐시에 담긴 슬림 결과를 되살린다(도구 결과 본문과 explorer 트리는 없다)."""
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
                        leaked=c.get("leaked", 0),
                        duration_ms=c.get("duration_ms", 0.0),
                        explorations=(
                            c.get("explorations")
                            or ([c["exploration"]] if c.get("exploration") else [])
                        ),
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
        context_exhausted=payload.get("context_exhausted", False),
        reader_stats=payload.get("reader_stats") or {},
        invalid_tool_calls=payload.get("invalid_tool_calls", 0),
        error=payload.get("error"),
        budget=payload.get("budget") or {},
        expansion_nodes=payload.get("expansion_nodes", 0),
        max_depth_reached=payload.get("max_depth_reached", 1),
        explorer_calls=payload.get("explorer_calls", 0),
        dead_dives=payload.get("dead_dives", 0),
        fetch_attempts=payload.get("fetch_attempts", 0),
        fetch_failures=payload.get("fetch_failures", 0),
        search_attempts=payload.get("search_attempts", 0),
        search_failures=payload.get("search_failures", 0),
    )
