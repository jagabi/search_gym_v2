"""search_gym — 검색 에이전트의 시스템 프롬프트를 GEPA로 최적화한다.

    searchgym/
      benchmarks/   문항 로딩 + 판정 프롬프트/스키마 (통일 레코드 형식)
      tools/        Serper·Jina를 MCP 도구로 노출 + 클라이언트
      agent.py      vLLM OpenAI 호환 서버 위의 도구 루프 (검색 예산 하드캡)
      serving.py    모델별 vllm serve 프로파일
      judge.py      Gemini structured-output 판정
      runner.py     실행 + 채점 + 캐시 + 기록
      gepa.py       dspy 메트릭과 instruction proposer
      config.py     YAML -> 데이터클래스
"""

from .agent import AgentConfig, RunResult, SearchAgent
from .benchmarks import BENCHMARKS, Item, load_benchmark
from .judge import Judge, JudgeConfig
from .runner import Record, Runner
from .scoring import Judgement, aggregate
from .serving import PROFILES, profile_for

__all__ = [
    "AgentConfig",
    "BENCHMARKS",
    "Item",
    "Judge",
    "JudgeConfig",
    "Judgement",
    "PROFILES",
    "Record",
    "RunResult",
    "Runner",
    "SearchAgent",
    "aggregate",
    "load_benchmark",
    "profile_for",
]
