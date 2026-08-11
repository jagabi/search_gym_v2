"""벤치마크 공통 골격과 **통일된 레코드 형식**.

데이터셋 JSON은 어떤 벤치마크든 아래 형식의 객체 배열이다. 새 벤치마크를 붙일 때
이 형식으로만 변환해 두면 실행·채점·집계 경로를 건드릴 필요가 없다.

    {
      "index":        0,               # 원본 행 번호. 로그 파일 이름이 여기 맞춰진다
      "question":     "...",           # 모델에게 그대로 보낼 질문
      "answer":       "...",           # 정답 원문
      "answer_type":  "single"|"set",  # 정답이 하나인가, 목록인가
      "category":     "Sports",        # 없으면 ""
      "answer_parts": ["...", ...]     # set일 때 결정적으로 쪼갠 파트. 모르면 null
    }

`answer_type`이 판정 방식을 정한다.
    single  판정 모델이 boolean 하나를 돌려준다        -> f1 == accuracy
    set     파트별 boolean + 여분 답 목록을 돌려준다   -> f1이 부분점수로 움직인다
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..paths import resolve
from ..scoring import Judgement

__all__ = ["Benchmark", "Item"]


@dataclass(slots=True)
class Item:
    index: int
    question: str
    answer: str
    answer_type: str = "single"
    category: str = ""
    answer_parts: list[str] | None = None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> Item:
        return cls(
            index=int(record["index"]),
            question=str(record["question"]).strip(),
            answer=str(record["answer"]).strip(),
            answer_type=str(record.get("answer_type") or "single"),
            category=str(record.get("category") or ""),
            answer_parts=record.get("answer_parts") or None,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "question": self.question,
            "answer": self.answer,
            "answer_type": self.answer_type,
            "category": self.category,
            "answer_parts": self.answer_parts,
        }


class Benchmark(ABC):
    """문항 로딩 + 판정 프롬프트/스키마/파싱. 실행 경로는 이것만 안다."""

    name: str

    def __init__(self, dataset: str | Path) -> None:
        self.dataset_path = resolve(dataset)

    def load(self, limit: int | None = None) -> list[Item]:
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"{self.dataset_path}가 없습니다. scripts/build_splits.py로 먼저 만드세요."
            )
        records = json.loads(self.dataset_path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError(f"{self.dataset_path}는 객체 배열이어야 합니다.")
        items = [Item.from_record(record) for record in records]
        return items[:limit] if limit is not None else items

    def build_prompt(self, item: Item) -> str:
        """수행 모델에게 보낼 프롬프트. 기본은 질문 원문 그대로."""
        return item.question

    # --- 채점 ---------------------------------------------------------------

    @abstractmethod
    def judge_prompt(self, item: Item, response: str) -> str: ...

    @abstractmethod
    def judge_schema(self, item: Item) -> dict[str, Any]: ...

    @abstractmethod
    def parse_judgement(self, item: Item, payload: dict[str, Any]) -> Judgement: ...
