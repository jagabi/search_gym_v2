"""판정 결과 → 점수.

정답을 파트 단위로 보고 세 숫자를 센다. 단일 정답 벤치마크는 파트가 하나뿐이라
자동으로 f1 == precision == recall == accuracy가 된다.

    TP  맞춘 파트        FN  놓친 파트        FP  엉뚱하게 덧붙인 답

    Recall = TP/(TP+FN)   Precision = TP/(TP+FP)   F1 = 2PR/(P+R)

    fully_correct            FN == 0 and FP == 0
    correct_with_extraneous  FN == 0 and FP > 0
    partially_correct        TP > 0 and FN > 0
    fully_incorrect          TP == 0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

__all__ = ["CATEGORIES", "SCORE_FIELDS", "Judgement", "aggregate", "score_of"]

CATEGORIES = (
    "fully_correct",
    "partially_correct",
    "correct_with_extraneous",
    "fully_incorrect",
)

SCORE_FIELDS = ("f1", "precision", "recall", "accuracy")


@dataclass(slots=True)
class Judgement:
    """판정 한 건의 정규화 결과."""

    parts: list[tuple[str, bool]] = field(default_factory=list)
    excessive: list[str] = field(default_factory=list)
    explanation: str = ""
    extracted: str = ""
    error: str | None = None
    raw: dict[str, Any] | None = None
    usage: dict[str, int] = field(default_factory=dict)
    latency_ms: float = 0.0

    @property
    def tp(self) -> int:
        return sum(1 for _, found in self.parts if found)

    @property
    def fn(self) -> int:
        return sum(1 for _, found in self.parts if not found)

    @property
    def fp(self) -> int:
        return len(self.excessive)

    @property
    def category(self) -> str:
        """순서가 곧 우선순위라 항상 하나만 배정된다."""
        if self.tp == 0:
            return "fully_incorrect"
        if self.fn == 0:
            return "fully_correct" if self.fp == 0 else "correct_with_extraneous"
        return "partially_correct"

    def metrics(self) -> dict[str, float]:
        precision = _ratio(self.tp, self.tp + self.fp)
        recall = _ratio(self.tp, self.tp + self.fn)
        total = precision + recall
        return {
            "precision": precision,
            "recall": recall,
            "f1": 2 * precision * recall / total if total else 0.0,
            "accuracy": 1.0 if self.category == "fully_correct" else 0.0,
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            **{k: round(v, 4) for k, v in self.metrics().items()},
            "tp": self.tp,
            "fn": self.fn,
            "fp": self.fp,
            "extracted": self.extracted,
            "explanation": self.explanation,
            "correctness_details": [
                {"expected": text, "found": found} for text, found in self.parts
            ],
            "excessive_answers": self.excessive,
            "error": self.error,
            "usage": self.usage,
            "latency_ms": round(self.latency_ms, 1),
            "raw": self.raw,
        }


def from_dict(payload: dict[str, Any]) -> Judgement:
    """`Judgement.as_dict()`를 되돌린다(캐시 적중·resume 시 집계에 쓴다)."""
    return Judgement(
        parts=[
            (entry["expected"], bool(entry["found"]))
            for entry in payload.get("correctness_details") or []
        ],
        excessive=list(payload.get("excessive_answers") or []),
        explanation=payload.get("explanation", ""),
        extracted=payload.get("extracted", ""),
        error=payload.get("error"),
        raw=payload.get("raw"),
        usage=payload.get("usage") or {},
        latency_ms=payload.get("latency_ms", 0.0),
    )


def score_of(judgement: Judgement, field_name: str) -> float:
    """설정이 가리키는 점수 하나를 뽑는다. 판정 실패는 0점."""
    if judgement.error is not None:
        return 0.0
    return float(judgement.metrics()[field_name])


def aggregate(judgements: Iterable[Judgement]) -> dict[str, Any]:
    """유효한 판정만 모아 macro 평균과 범주 분포를 낸다."""
    items = list(judgements)
    valid = [j for j in items if j.error is None]
    scores = [j.metrics() for j in valid]
    counts = {name: sum(1 for j in valid if j.category == name) for name in CATEGORIES}

    return {
        "n": len(items),
        "judged": len(valid),
        "judge_errors": len(items) - len(valid),
        **{
            key: round(_mean(s[key] for s in scores), 4)
            for key in ("accuracy", "f1", "precision", "recall")
        },
        "categories": counts,
    }


def _ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _mean(values: Iterable[float]) -> float:
    collected = list(values)
    return sum(collected) / len(collected) if collected else 0.0
