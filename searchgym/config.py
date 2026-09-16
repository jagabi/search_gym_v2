"""YAML 설정 → 데이터클래스.

설정 파일에 오타가 있으면 valset을 다 돌고 나서가 아니라 **시작 전에** 죽어야
한다. 그래서 알 수 없는 키와 잘못된 값은 여기서 전부 걸러낸다.

파일이 둘로 나뉜다.

    conf.yaml               무엇을 돌릴지만 — 방법 · 모델 · 벤치마크
    configs/<방법>.yaml     그 방법의 예산 · 프롬프트
    configs/gepa.yaml       학습에만 쓰는 것 — 교사 · 피드백 · GEPA 예산

확장 사고와 추론 강도는 **설정에 없다.** 항상 켜고, gpt-oss 는 프로파일의
`reasoning_effort`(medium)를 쓴다. 모델별로 다르게 두면 비교가 성립하지 않는다.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from pathlib import Path
from string import Formatter
from typing import Any

import yaml

from .agent import METHODS, AgentConfig
from .benchmarks import BENCHMARKS
from .explorer import ExplorerConfig
from .judge import JudgeConfig
from .paths import PROJECT_ROOT, resolve
from .scoring import SCORE_FIELDS
from .serving import PROFILES

__all__ = [
    "BenchmarkRef",
    "FEEDBACK_FIELDS",
    "GepaConfig",
    "RunConfig",
    "TestConfig",
    "TrainConfig",
    "load_test",
    "load_train",
]

CONFIG_DIR = PROJECT_ROOT / "configs"

# 피드백 템플릿에서 쓸 수 있는 치환자. 값은 gepa.SearchMetric 이 채운다.
FEEDBACK_FIELDS = frozenset(
    {
        "question", "gold_answer", "answer", "score", "precision", "recall", "f1",
        "verdict", "failure_mode", "missed_parts", "excessive_answers",
        "searches", "fetches", "queries", "urls", "trajectory",
        "stop_reason", "turns", "latency_s", "error",
        # 확장 관련
        "expansion_nodes", "max_depth_reached", "explorer_calls", "dead_dives",
        "budget_exhausted", "explorer_log", "context_exhausted",
    }
)


@dataclass(slots=True)
class BenchmarkRef:
    name: str = "deepsearchqa"
    path: str = ""
    limit: int | None = None

    def __post_init__(self) -> None:
        if self.name not in BENCHMARKS:
            raise ValueError(f"알 수 없는 벤치마크 '{self.name}'. 사용 가능: {', '.join(BENCHMARKS)}")

    def dataset(self, split: str = "validation") -> Path:
        return resolve(self.path) if self.path else PROJECT_ROOT / "data" / self.name / f"{split}.json"


@dataclass(slots=True)
class RunConfig:
    tag: str = ""
    output_dir: str = "runs"
    seed: int = 0
    cache: bool = True
    workers: int = 1


@dataclass(slots=True)
class TeacherConfig:
    """GEPA reflection LM. dspy.LM(litellm) 로 넘어가므로 "<provider>/<model>" 형식."""

    model: str = "anthropic/claude-opus-5"
    max_tokens: int = 32768
    extra: dict[str, Any] = field(default_factory=dict)
    prompt_token_budget: int = 1024


@dataclass(slots=True)
class ComponentConfig:
    reflection_prompt: str = ""

    def __post_init__(self) -> None:
        if not self.reflection_prompt.strip():
            return
        missing = [k for k in ("<curr_param>", "<side_info>") if k not in self.reflection_prompt]
        if missing:
            raise ValueError(f"reflection_prompt 에 필수 자리표시자가 없습니다: {missing}")


@dataclass(slots=True)
class FeedbackConfig:
    template: str = ""
    explorer_template: str = ""
    score: str = "f1"
    max_answer_chars: int = 4000
    max_trajectory_chars: int = 4000

    def __post_init__(self) -> None:
        if self.score not in SCORE_FIELDS:
            raise ValueError(f"feedback.score 는 {SCORE_FIELDS} 중 하나여야 합니다.")
        for label, template in (("template", self.template), ("explorer_template", self.explorer_template)):
            used = {name for _, name, _, _ in Formatter().parse(template) if name}
            if unknown := sorted(used - FEEDBACK_FIELDS):
                raise ValueError(
                    f"feedback.{label} 에 알 수 없는 치환자가 있습니다: {unknown}\n"
                    f"  사용 가능: {sorted(FEEDBACK_FIELDS)}"
                )


@dataclass(slots=True)
class GepaConfig:
    auto: str | None = None
    reflection_minibatch_size: int = 7
    num_threads: int = 1
    track_stats: bool = True
    failure_score: float = 0.0
    merge: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DataConfig:
    benchmark: str = "deepsearchqa"
    trainset: str = "data/deepsearchqa/train.json"
    valset: str = "data/deepsearchqa/validation.json"

    def __post_init__(self) -> None:
        if self.benchmark not in BENCHMARKS:
            raise ValueError(f"알 수 없는 벤치마크 '{self.benchmark}'.")


# --- 방법 설정 (configs/<방법>.yaml) ----------------------------------------


@dataclass(slots=True)
class MethodConfig:
    agent: AgentConfig = field(default_factory=AgentConfig)
    explorer: ExplorerConfig = field(default_factory=ExplorerConfig)
    system_prompt: str = ""
    explorer_prompt: str = ""


# --- 최종 설정 --------------------------------------------------------------


@dataclass(slots=True)
class TestConfig:
    method: str = "depthsearch"
    model: str = "qwen"
    benchmark: BenchmarkRef = field(default_factory=BenchmarkRef)
    judge: JudgeConfig = field(default_factory=JudgeConfig)
    run: RunConfig = field(default_factory=RunConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    explorer: ExplorerConfig = field(default_factory=ExplorerConfig)
    system_prompt: str = ""
    explorer_prompt: str = ""
    sources: list[str] = field(default_factory=list)

    @property
    def uses_explorer(self) -> bool:
        return self.method != "ragent"

    def describe(self) -> dict[str, Any]:
        budget = f"search {self.agent.max_searches}"
        if self.agent.search_top_k:
            budget += f" / 자동페치 top-{self.agent.search_top_k}"
        else:
            budget += f" / fetch {self.agent.max_fetches or '무제한'}"
        if self.uses_explorer and self.explorer.recursive:
            budget += (
                f" / depth {self.explorer.max_depth}"
                f" / nodes {self.explorer.max_expansion_nodes}"
                f" / children {self.explorer.max_subtree_children}"
            )
        budget += f" / context {self.agent.context_limit:,}"
        return {
            "method": self.method,
            "budget": budget,
            "system_prompt_chars": len(self.system_prompt),
            "explorer_prompt_chars": len(self.explorer_prompt) if self.uses_explorer else 0,
        }


@dataclass(slots=True)
class TrainConfig:
    base: TestConfig = field(default_factory=TestConfig)
    data: DataConfig = field(default_factory=DataConfig)
    teacher: TeacherConfig = field(default_factory=TeacherConfig)
    components: dict[str, ComponentConfig] = field(default_factory=dict)
    feedback: FeedbackConfig = field(default_factory=FeedbackConfig)
    gepa: GepaConfig = field(default_factory=GepaConfig)

    @property
    def component_names(self) -> list[str]:
        """실제로 최적화할 컴포넌트.

        explorer 가 확장 결정을 하지 않으면(= search-o1) 최적화할 정책이 없고,
        ragent 는 explorer 자체가 없다.
        """
        names = ["agent"]
        if self.base.uses_explorer and self.base.explorer.recursive:
            names.append("explorer")
        return [n for n in names if n in self.components]


# --- 로더 -------------------------------------------------------------------


def load_test(
    conf_path: str | Path = "conf.yaml",
    *,
    method: str | None = None,
    model: str | None = None,
    benchmark: str | None = None,
    path: str | None = None,
    limit: int | None = None,
    tag: str | None = None,
) -> TestConfig:
    raw = _read(conf_path)
    outer = _build(_Outer, raw, "conf")

    chosen = method or outer.method
    if chosen not in METHODS:
        raise ValueError(f"알 수 없는 method '{chosen}'. 사용 가능: {', '.join(METHODS)}")
    method_path = CONFIG_DIR / f"{chosen}.yaml"
    method_config = _build(MethodConfig, _read(method_path), chosen)

    if model or outer.model:
        _check_model(model or outer.model)

    reference = outer.benchmark
    if benchmark:
        reference = BenchmarkRef(name=benchmark, path=path or "", limit=limit)
    else:
        if path:
            reference.path = path
        if limit is not None:
            reference.limit = limit

    config = TestConfig(
        method=chosen,
        model=model or outer.model,
        benchmark=reference,
        judge=outer.judge,
        run=outer.run,
        agent=method_config.agent,
        explorer=method_config.explorer,
        system_prompt=method_config.system_prompt.strip(),
        explorer_prompt=method_config.explorer_prompt.strip(),
        sources=[str(resolve(conf_path)), str(method_path)],
    )
    # 엔드포인트와 서빙 이름은 배포 사실이라 conf.yaml 에 있고, 방법 설정과 무관하다.
    if outer.base_url:
        config.agent.base_url = outer.base_url
    if outer.served_model_name:
        config.agent.model_name = outer.served_model_name
    if tag:
        config.run.tag = tag
    _validate(config)
    return config


def load_train(
    conf_path: str | Path = "conf.yaml",
    gepa_path: str | Path = "configs/gepa.yaml",
    **overrides: Any,
) -> TrainConfig:
    base = load_test(conf_path, **overrides)
    raw = _read(gepa_path)

    components_raw = raw.pop("components", {}) or {}
    if not isinstance(components_raw, dict):
        raise ValueError("gepa.components 는 매핑이어야 합니다.")
    components = {
        name: _build(ComponentConfig, entry or {}, f"gepa.components.{name}")
        for name, entry in components_raw.items()
    }
    if unknown := sorted(set(components) - {"agent", "explorer"}):
        raise ValueError(f"gepa.components 에 알 수 없는 컴포넌트가 있습니다: {unknown}")

    shell = _build(_GepaShell, raw, "gepa")
    config = TrainConfig(
        base=base,
        data=shell.data,
        teacher=shell.teacher,
        components=components,
        feedback=shell.feedback,
        gepa=shell.gepa,
    )
    base.sources.append(str(resolve(gepa_path)))

    if not config.feedback.template.strip():
        raise ValueError("gepa.feedback.template 이 비어 있습니다.")
    if "explorer" in config.component_names and not config.feedback.explorer_template.strip():
        raise ValueError(
            "explorer 컴포넌트를 최적화하려면 gepa.feedback.explorer_template 이 필요합니다."
        )
    return config


# --- 내부 -------------------------------------------------------------------


@dataclass(slots=True)
class _Outer:
    """conf.yaml 의 스키마."""

    method: str = "depthsearch"
    model: str = "qwen"
    base_url: str = ""
    served_model_name: str = ""
    benchmark: BenchmarkRef = field(default_factory=BenchmarkRef)
    judge: JudgeConfig = field(default_factory=JudgeConfig)
    run: RunConfig = field(default_factory=RunConfig)


@dataclass(slots=True)
class _GepaShell:
    data: DataConfig = field(default_factory=DataConfig)
    teacher: TeacherConfig = field(default_factory=TeacherConfig)
    feedback: FeedbackConfig = field(default_factory=FeedbackConfig)
    gepa: GepaConfig = field(default_factory=GepaConfig)


def _validate(config: TestConfig) -> None:
    if config.agent.max_searches < 0 or config.agent.search_results <= 0:
        raise ValueError("Search count must be nonnegative and result count positive")
    if config.agent.max_tool_recoveries < 0:
        raise ValueError("Recovery budgets must be nonnegative")
    if config.explorer.max_root_nodes < 0:
        raise ValueError("Reader root budget must be nonnegative")
    if not config.system_prompt:
        raise ValueError(f"configs/{config.method}.yaml 의 system_prompt 가 비어 있습니다.")
    # 산술이 안 맞으면 문항을 다 돌고 나서가 아니라 **시작 전에** 죽어야 한다.
    # GPU 시간이 나가는 실행이라 여기서 잡는 값이 곧 돈이다.
    if config.agent.max_tokens >= config.agent.context_limit:
        raise ValueError(
            f"agent.max_tokens({config.agent.max_tokens:,}) 가 "
            f"context_limit({config.agent.context_limit:,}) 이상입니다."
        )

    if config.uses_explorer:
        if not config.explorer_prompt:
            raise ValueError(f"configs/{config.method}.yaml 의 explorer_prompt 가 비어 있습니다.")
        if config.explorer.max_depth < 1:
            raise ValueError("explorer.max_depth 는 1 이상이어야 합니다.")

        # explorer 한 세션은 (문서 묶음 + 자기 출력) 이 컨텍스트에 들어가야 한다.
        need = config.explorer.max_document_tokens + config.explorer.max_tokens
        if need > config.explorer.context_limit:
            raise ValueError(
                f"explorer 의 max_document_tokens({config.explorer.max_document_tokens:,})"
                f" + max_tokens({config.explorer.max_tokens:,}) = {need:,} 가 "
                f"context_limit({config.explorer.context_limit:,}) 을 넘습니다."
            )
        # 자동 페치한 k개는 **각각** explorer 를 하나씩 태우므로 예산을 나눠 갖지
        # 않는다. max_document_tokens 가 곧 페이지 하나의 상한이고, 세 방법이 같은
        # 값이어야 "같은 분량의 웹을 봤다"가 성립한다.
        if config.explorer.max_document_tokens != config.agent.fetch_max_tokens:
            raise ValueError(
                f"explorer.max_document_tokens({config.explorer.max_document_tokens:,})"
                f" 와 agent.fetch_max_tokens({config.agent.fetch_max_tokens:,}) 가 다릅니다. "
                "페이지 하나의 분량이 방법마다 달라지면 비교가 깨집니다."
            )
        if config.explorer.max_depth > 1 and config.explorer.max_subtree_children <= 0:
            raise ValueError(
                "max_depth 가 1보다 크면 max_subtree_children 도 1 이상이어야 합니다."
            )

    # 자동 페치는 search-o1 만 한다. 나머지 둘은 메인 모델이 검색 결과를 보고 고른다.
    if config.method == "search-o1":
        if config.agent.search_top_k <= 0:
            raise ValueError("search-o1 은 agent.search_top_k 가 1 이상이어야 합니다.")
    elif config.agent.search_top_k:
        raise ValueError(
            f"{config.method} 는 메인 모델이 페치를 고릅니다. "
            "agent.search_top_k 를 0 으로 두세요."
        )


def _check_model(name: str) -> None:
    if name not in PROFILES and name not in {p.repo for p in PROFILES.values()}:
        raise ValueError(f"알 수 없는 모델 '{name}'. 사용 가능: {', '.join(PROFILES)}")


def _read(path: str | Path) -> dict[str, Any]:
    resolved = resolve(path)
    if not resolved.exists():
        raise FileNotFoundError(f"설정 파일이 없습니다: {resolved}")
    raw = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{resolved} 는 최상위가 매핑이어야 합니다.")
    return raw


def _build(target: type, raw: dict[str, Any], where: str) -> Any:
    """dict 를 데이터클래스로 재귀 변환한다. 알 수 없는 키는 즉시 실패."""
    names = {f.name for f in fields(target)}
    if unknown := sorted(set(raw) - names):
        raise ValueError(f"{where} 에 알 수 없는 키가 있습니다: {unknown}\n  사용 가능: {sorted(names)}")

    kwargs: dict[str, Any] = {}
    for f in fields(target):
        if f.name not in raw:
            continue
        value = raw[f.name]
        nested = _nested_type(f.type)
        if nested is not None and isinstance(value, dict):
            kwargs[f.name] = _build(nested, value, f"{where}.{f.name}")
        else:
            kwargs[f.name] = value
    return target(**kwargs)


def _nested_type(annotation: Any) -> type | None:
    if isinstance(annotation, str):
        annotation = _RESOLVED.get(annotation)
    return annotation if is_dataclass(annotation) else None


_RESOLVED: dict[str, Any] = {
    "AgentConfig": AgentConfig,
    "BenchmarkRef": BenchmarkRef,
    "ComponentConfig": ComponentConfig,
    "DataConfig": DataConfig,
    "ExplorerConfig": ExplorerConfig,
    "FeedbackConfig": FeedbackConfig,
    "GepaConfig": GepaConfig,
    "JudgeConfig": JudgeConfig,
    "MethodConfig": MethodConfig,
    "RunConfig": RunConfig,
    "TeacherConfig": TeacherConfig,
    "TestConfig": TestConfig,
}
