"""벤치마크 레지스트리.

새 벤치마크는 여기 한 줄만 추가하면 된다. 데이터 파일이 `_base.py`의 통일 형식을
따르고 정답이 하나면 `SingleAnswerBenchmark`를 그대로 쓸 수 있다.
"""

from __future__ import annotations

from pathlib import Path

from ..paths import PROJECT_ROOT
from ._base import Benchmark, Item
from ._deepsearchqa import DeepSearchQA
from ._single import SingleAnswerBenchmark

__all__ = ["BENCHMARKS", "Benchmark", "Item", "default_dataset", "load_benchmark"]


def _single(name: str) -> type[Benchmark]:
    """이름만 다른 단일 정답 벤치마크를 찍어낸다."""
    return type(name, (SingleAnswerBenchmark,), {"name": name})


_REGISTRY: dict[str, type[Benchmark]] = {
    "deepsearchqa": DeepSearchQA,
    "evobrowsecomp": _single("evobrowsecomp"),
    "browsecomp": _single("browsecomp"),
    "kbrowsecomp": _single("kbrowsecomp"),
}

BENCHMARKS = tuple(_REGISTRY)


def default_dataset(name: str, split: str = "test") -> Path:
    return PROJECT_ROOT / "data" / name / f"{split}.json"


def load_benchmark(name: str, dataset: str | Path | None = None) -> Benchmark:
    if name not in _REGISTRY:
        raise ValueError(f"알 수 없는 벤치마크 '{name}'. 사용 가능: {', '.join(BENCHMARKS)}")
    return _REGISTRY[name](dataset or default_dataset(name))
