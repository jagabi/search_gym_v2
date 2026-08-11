"""YAML 설정 → 데이터클래스.

설정 파일에 오타가 있으면 valset을 다 돌고 나서가 아니라 **시작 전에** 죽어야
한다. 그래서 알 수 없는 키와 잘못된 값은 여기서 전부 걸러낸다.
"""

from __future__ import annotations

import typing
from dataclasses import MISSING, dataclass, field, fields, is_dataclass
from pathlib import Path
from string import Formatter
from typing import Any

import yaml

from .agent import AgentConfig
from .benchmarks import BENCHMARKS
from .judge import JudgeConfig
from .paths import resolve
from .scoring import SCORE_FIELDS
from .serving import PROFILES

__all__ = ["EvalConfig", "TrainConfig", "load_eval", "load_train"]

# 피드백 템플릿에서 쓸 수 있는 치환자. 값은 runner가 채운다.
FEEDBACK_FIELDS = frozenset(
    {
        "question", "gold_answer", "answer", "score", "precision", "recall", "f1",
        "verdict", "failure_mode", "missed_parts", "excessive_answers",
        "searches", "fetches", "queries", "urls", "trajectory",
        "stop_reason", "turns", "latency_s", "error",
    }
)


@dataclass(slots=True)
class DataConfig:
    benchmark: str = "deepsearchqa"
    trainset: str = "data/deepsearchqa/train.json"
    valset: str = "data/deepsearchqa/validation.json"

    def __post_init__(self) -> None:
        _check_benchmark(self.benchmark)


@dataclass(slots=True)
class TeacherConfig:
    """GEPA reflection LM. dspy.LM(litellm)로 넘어가므로 "<provider>/<model>" 형식."""

    model: str = "anthropic/claude-opus-5"
    max_tokens: int = 32768
    extra: dict[str, Any] = field(default_factory=dict)
    reflection_prompt: str = ""
    # 학생 프롬프트의 토큰 상한. reflection_prompt의 <budget>에 치환된다.
    prompt_token_budget: int = 1024

    def __post_init__(self) -> None:
        if not self.reflection_prompt.strip():
            return
        missing = [k for k in ("<curr_param>", "<side_info>") if k not in self.reflection_prompt]
        if missing:
            raise ValueError(f"teacher.reflection_prompt에 필수 자리표시자가 없습니다: {missing}")


@dataclass(slots=True)
class FeedbackConfig:
    template: str = ""
    score: str = "f1"
    max_answer_chars: int = 4000
    max_trajectory_chars: int = 4000

    def __post_init__(self) -> None:
        if self.score not in SCORE_FIELDS:
            raise ValueError(f"feedback.score는 {SCORE_FIELDS} 중 하나여야 합니다.")
        used = {name for _, name, _, _ in Formatter().parse(self.template) if name}
        if unknown := sorted(used - FEEDBACK_FIELDS):
            raise ValueError(
                f"feedback.template에 알 수 없는 치환자가 있습니다: {unknown}\n"
                f"  사용 가능: {sorted(FEEDBACK_FIELDS)}"
            )


@dataclass(slots=True)
class GepaConfig:
    auto: str | None = "light"
    reflection_minibatch_size: int = 7
    num_threads: int = 1
    track_stats: bool = True
    failure_score: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RunConfig:
    tag: str = ""
    output_dir: str = "runs"
    seed: int = 0
    cache: bool = True
    workers: int = 1
    resume: bool = True


@dataclass(slots=True)
class DatasetRef:
    name: str = "deepsearchqa"
    path: str = ""
    limit: int | None = None

    def __post_init__(self) -> None:
        _check_benchmark(self.name)


@dataclass(slots=True)
class TrainConfig:
    model: str = "qwen"
    agent: AgentConfig = field(default_factory=AgentConfig)
    initial_prompt: str = ""
    data: DataConfig = field(default_factory=DataConfig)
    teacher: TeacherConfig = field(default_factory=TeacherConfig)
    feedback: FeedbackConfig = field(default_factory=FeedbackConfig)
    gepa: GepaConfig = field(default_factory=GepaConfig)
    judge: JudgeConfig = field(default_factory=JudgeConfig)
    run: RunConfig = field(default_factory=RunConfig)
    source: str = ""

    def __post_init__(self) -> None:
        _check_model(self.model)


@dataclass(slots=True)
class EvalConfig:
    model: str = "qwen"
    agent: AgentConfig = field(default_factory=AgentConfig)
    prompt_path: str = ""
    prompt_text: str = ""
    datasets: list[DatasetRef] = field(default_factory=list)
    judge: JudgeConfig = field(default_factory=JudgeConfig)
    run: RunConfig = field(default_factory=RunConfig)
    source: str = ""

    def __post_init__(self) -> None:
        _check_model(self.model)

    def system_prompt(self) -> str:
        """평가할 시스템 프롬프트. 둘 다 비면 프롬프트 없는 대조군이 된다."""
        if self.prompt_text.strip():
            return self.prompt_text.strip()
        if self.prompt_path:
            return resolve(self.prompt_path).read_text(encoding="utf-8").strip()
        return ""


def load_train(path: str | Path) -> TrainConfig:
    config = _build(TrainConfig, _read(path), "train")
    config.source = str(resolve(path))
    return config


def load_eval(path: str | Path) -> EvalConfig:
    config = _build(EvalConfig, _read(path), "eval")
    config.source = str(resolve(path))
    if not config.datasets:
        raise ValueError("eval 설정에 datasets가 비어 있습니다.")
    return config


# --- 내부 -------------------------------------------------------------------


def _check_benchmark(name: str) -> None:
    if name not in BENCHMARKS:
        raise ValueError(f"알 수 없는 벤치마크 '{name}'. 사용 가능: {', '.join(BENCHMARKS)}")


def _check_model(name: str) -> None:
    if name not in PROFILES and name not in {p.repo for p in PROFILES.values()}:
        raise ValueError(f"알 수 없는 모델 '{name}'. 사용 가능: {', '.join(PROFILES)}")


def _read(path: str | Path) -> dict[str, Any]:
    resolved = resolve(path)
    if not resolved.exists():
        raise FileNotFoundError(f"설정 파일이 없습니다: {resolved}")
    raw = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{resolved}는 최상위가 매핑이어야 합니다.")
    return raw


def _build(target: type, raw: dict[str, Any], where: str) -> Any:
    """dict를 데이터클래스로 재귀 변환한다. 알 수 없는 키는 즉시 실패."""
    names = {f.name for f in fields(target)}
    if unknown := sorted(set(raw) - names):
        raise ValueError(f"{where}에 알 수 없는 키가 있습니다: {unknown}\n  사용 가능: {sorted(names)}")

    kwargs: dict[str, Any] = {}
    for f in fields(target):
        if f.name not in raw:
            continue
        value = raw[f.name]
        nested = _nested_type(f.type)
        if nested is not None and isinstance(value, dict):
            kwargs[f.name] = _build(nested, value, f"{where}.{f.name}")
        elif f.name == "datasets" and isinstance(value, list):
            kwargs[f.name] = [
                _build(DatasetRef, entry, f"{where}.datasets[{i}]")
                for i, entry in enumerate(value)
            ]
        else:
            kwargs[f.name] = value
    return target(**kwargs)


def _nested_type(annotation: Any) -> type | None:
    if isinstance(annotation, str):
        annotation = _RESOLVED.get(annotation)
    return annotation if is_dataclass(annotation) else None


_RESOLVED: dict[str, Any] = {
    "AgentConfig": AgentConfig,
    "DataConfig": DataConfig,
    "DatasetRef": DatasetRef,
    "FeedbackConfig": FeedbackConfig,
    "GepaConfig": GepaConfig,
    "JudgeConfig": JudgeConfig,
    "RunConfig": RunConfig,
    "TeacherConfig": TeacherConfig,
}
