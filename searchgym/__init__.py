"""search_gym — 검색 에이전트의 시스템 프롬프트를 GEPA로 최적화한다.

    searchgym/
      benchmarks/   문항 로딩 + 판정 프롬프트/스키마 (통일 레코드 형식)
      tools/        Serper·Jina를 MCP 도구로 노출 + 클라이언트
      agent.py      vLLM OpenAI 호환 서버 위의 도구 루프 (검색 예산·컨텍스트 상한)
      serving.py    모델별 vllm serve 프로파일
      judge.py      Gemini structured-output 판정
      runner.py     실행 + 채점 + 캐시 + 기록
      gepa.py       dspy 메트릭과 instruction proposer
      config.py     YAML -> 데이터클래스

**import는 지연시킨다.** `test.py` 만 돌릴 때는 dspy·litellm 이 필요 없고,
`scripts/build_splits.py` 는 openai·google-genai 없이도 돌아야 한다. 여기서 전부 미리
import 하면 그런 경로가 무거운 의존성 때문에 죽는다. 실제로 쓰는 것만 그때 불러온다.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # 타입 검사기와 IDE에게만 보이는 경로
    from .agent import METHODS, AgentConfig, RunResult, SearchAgent
    from .benchmarks import BENCHMARKS, Item, load_benchmark
    from .explorer import Budget, Explorer, ExplorerConfig, ExplorerResult
    from .llm import LLM, Usage
    from .judge import Judge, JudgeConfig
    from .runner import Record, Runner
    from .scoring import Judgement, aggregate
    from .serving import PROFILES, profile_for

# 공개 이름 -> 정의된 모듈.
_EXPORTS = {
    "METHODS": ".agent",
    "AgentConfig": ".agent",
    "RunResult": ".agent",
    "SearchAgent": ".agent",
    "Budget": ".explorer",
    "Explorer": ".explorer",
    "ExplorerConfig": ".explorer",
    "ExplorerResult": ".explorer",
    "LLM": ".llm",
    "Usage": ".llm",
    "BENCHMARKS": ".benchmarks",
    "Item": ".benchmarks",
    "load_benchmark": ".benchmarks",
    "Judge": ".judge",
    "JudgeConfig": ".judge",
    "Record": ".runner",
    "Runner": ".runner",
    "Judgement": ".scoring",
    "aggregate": ".scoring",
    "PROFILES": ".serving",
    "profile_for": ".serving",
}

__all__ = sorted(_EXPORTS)


def __getattr__(name: str) -> Any:
    if module := _EXPORTS.get(name):
        return getattr(importlib.import_module(module, __name__), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return __all__
