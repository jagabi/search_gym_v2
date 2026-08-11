"""정답이 하나인 벤치마크 — EvoBrowseComp / BrowseComp / K-BrowseComp.

셋 다 짧은 단일 정답이라 판정 로직이 같다. 이름과 데이터만 다르므로 클래스 하나를
공유한다. 판정 모델에게는 boolean 하나만 받는다.

    correctness_details = [(정답, 맞았나)]   길이 1
    excessive_answers   = []                 쓰지 않음

단일 정답 문항에서 "여분의 답"은 정의되지 않는다. 넣으면 precision이 임의로
깎이므로 비워 둔다 — 그래서 f1 == precision == recall == accuracy가 된다.
"""

from __future__ import annotations

from typing import Any

from ..scoring import Judgement
from ._base import Benchmark, Item

__all__ = ["SingleAnswerBenchmark"]


class SingleAnswerBenchmark(Benchmark):
    name = "single_answer"

    def judge_prompt(self, item: Item, response: str) -> str:
        return _GRADER.format(
            question=item.question.strip(),
            answer=item.answer.strip(),
            response=response.strip(),
        )

    def judge_schema(self, item: Item) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "extracted_final_answer": {
                    "type": "string",
                    "description": (
                        "The final answer the response commits to, quoted verbatim."
                        " Use 'None' if it states no answer."
                    ),
                },
                "explanation": {
                    "type": "string",
                    "description": "One or two sentences comparing it with the correct answer.",
                },
                "correct": {
                    "type": "boolean",
                    "description": "True only if the extracted answer means the same as the correct answer.",
                },
            },
            "required": ["extracted_final_answer", "explanation", "correct"],
        }

    def parse_judgement(self, item: Item, payload: dict[str, Any]) -> Judgement:
        if "correct" not in payload:
            return Judgement(error="판정에 'correct'가 없습니다.")
        return Judgement(
            parts=[(item.answer.strip(), bool(payload["correct"]))],
            excessive=[],
            explanation=str(payload.get("explanation") or ""),
            extracted=str(payload.get("extracted_final_answer") or "").strip(),
        )


_GRADER = """\
Judge whether the AI response reaches the correct answer to the question.

The question has exactly one correct answer. Judge only whether the response arrives
at it — not how it got there, how it is worded, or how much else it says.

*   Extract the final answer the response commits to. If it states no answer, or only
    reports that it could not find one, the extraction is "None" and it is incorrect.
*   Correct when it means the same thing as the correct answer. Wording, formatting,
    added units, and equivalent forms of the same value ("22" and "22 years", a name
    with and without a middle initial) do not matter.
*   Incorrect when it names a different entity or value, when it hedges across several
    candidates without committing to one, or when the correct answer appears only
    inside reasoning that the response then rejects.

Question (wrapped in <question> and </question>):
<question>
{question}
</question>
--------------------
Correct answer (wrapped in <answer> and </answer>):
<answer>
{answer}
</answer>
--------------------
AI assistant response (wrapped in <response> and </response>):
<response>
{response}
</response>
--------------------
Rating:"""
