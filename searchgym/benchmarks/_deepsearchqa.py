"""DeepSearchQA — 정답이 목록인 벤치마크.

채점 프롬프트는 논문 부록 A의 Grader Prompt를 옮겼다. 다만 "Output Format" 절
(중첩 JSON 구조 지시 + 이스케이프 당부 + 예시 블록)은 뺐다. structured output으로
스키마를 강제하므로 무의미할 뿐 아니라, 스키마와 프롬프트가 다른 형태를 요구하면
판정 모델이 흔들린다.

정답 파트 스키마는 문항별로 다르다.
    locked  `answer_parts`가 있는 문항. 파트 수를 스키마에 못박아 recall의 분모가
            판정 모델 재량이 아니라 ground truth로 확정된다.
    free    분해가 모호한 문항. 논문 프로토콜대로 판정 모델이 알아서 쪼갠다.
"""

from __future__ import annotations

from typing import Any

from ..scoring import Judgement
from ._base import Benchmark, Item

__all__ = ["DeepSearchQA", "schema_keys"]


def schema_keys(parts: list[str]) -> list[str]:
    """정답 파트를 JSON 객체 키로 바꾼다.

    같은 값이 두 번 나오는 정답이 있다("Iowa, Iowa" — 하위 질문 둘의 답이 모두
    Iowa). 키는 유일해야 하므로 중복된 값에만 번호를 붙이고, 한 번뿐인 파트는
    원문 그대로 둔다.
    """
    totals: dict[str, int] = {}
    for part in parts:
        totals[part] = totals.get(part, 0) + 1

    seen: dict[str, int] = {}
    keys: list[str] = []
    for part in parts:
        if totals[part] == 1:
            keys.append(part)
            continue
        seen[part] = seen.get(part, 0) + 1
        keys.append(f"{part}_{seen[part]}")
    return keys


class DeepSearchQA(Benchmark):
    name = "deepsearchqa"

    def judge_prompt(self, item: Item, response: str) -> str:
        parts = item.answer_parts
        section = ""
        if parts:
            listed = "\n".join(f"        {i}. {part}" for i, part in enumerate(parts, 1))
            section = (
                '    *   **Expected answer parts:** The "Correct Answer" decomposes into'
                f" exactly {len(parts)} part(s). Judge each one independently, in this"
                f" order:\n{listed}\n"
            )
        return _GRADER.format(
            prompt=item.question.strip(),
            prompt_type=_prompt_type(item),
            answer=item.answer.strip(),
            response=response.strip(),
            parts_section=section,
        )

    def judge_schema(self, item: Item) -> dict[str, Any]:
        parts = item.answer_parts
        if parts:
            keys = schema_keys(parts)
            details: dict[str, Any] = {
                "type": "object",
                "description": "One boolean per expected answer part.",
                "properties": {
                    key: {
                        "type": "boolean",
                        "description": f"Whether the response contains this expected part: {part}",
                    }
                    for key, part in zip(keys, parts)
                },
                "required": keys,
            }
        else:
            details = {
                "type": "array",
                "description": "One entry per expected answer part.",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "expected_answer": {"type": "string"},
                        "found": {"type": "boolean"},
                    },
                    "required": ["expected_answer", "found"],
                },
            }

        return {
            "type": "object",
            "properties": {
                "explanation": {
                    "type": "string",
                    "description": "Brief justification referencing the response and the correct answer.",
                },
                "correctness_details": details,
                "excessive_answers": {
                    "type": "array",
                    "description": "Answers the response gave that are NOT in the correct answer.",
                    "items": {"type": "string"},
                },
            },
            "required": ["explanation", "correctness_details", "excessive_answers"],
        }

    def parse_judgement(self, item: Item, payload: dict[str, Any]) -> Judgement:
        details = payload.get("correctness_details")
        excessive = [str(a) for a in payload.get("excessive_answers") or []]
        explanation = str(payload.get("explanation") or "")
        parts = item.answer_parts

        if parts:
            if not isinstance(details, dict):
                return Judgement(error="correctness_details가 객체가 아닙니다.")
            keys = schema_keys(parts)
            if missing := [key for key in keys if key not in details]:
                return Judgement(error=f"판정에서 빠진 정답 파트: {missing}")
            # 점수는 원문 파트 기준으로 남긴다. 키의 _1/_2는 스키마 사정일 뿐이다.
            pairs = [(part, bool(details[key])) for key, part in zip(keys, parts)]
        else:
            if not isinstance(details, list):
                return Judgement(error="correctness_details가 배열이 아닙니다.")
            pairs = [
                (str(e.get("expected_answer", "")), bool(e.get("found")))
                for e in details
                if isinstance(e, dict)
            ]

        if not pairs:
            return Judgement(error="정답 파트가 비어 있습니다.")
        return Judgement(parts=pairs, excessive=excessive, explanation=explanation)


def _prompt_type(item: Item) -> str:
    return "Set Answer" if item.answer_type == "set" else "Single Answer"


_GRADER = """\
Your task is to evaluate whether a given "AI Response" for a specific "User Prompt" arrived at the correct answer.

**Answer Correctness Task**
*   **Purpose:** Assess whether the AI response provides the correct answer(s) based on the provided "Correct Answer" and "Prompt Type".
*   **Process:**
    *   Identify the "Prompt Type": "{prompt_type}".
    *   Refer to the "Correct Answer": "{answer}".
    *   Based on the "Prompt Type", determine if the "AI Response" contains the expected answer(s).
        *   **'Single Answer'**: Check if the response provides the answer that addresses the user's question. It does not have to match the exact wording of the provided answer.
        *   **'Set Answer'**: Check if the response includes *each* item from the provided ground truth answers. The order might not matter unless specified otherwise. The response might include more answers than the list. Determine the correctness *only* based on the list first and then check if the response includes answers not in the list.
    *   **Explanation:** Provide a brief explanation justifying your assessment of answer correctness, referencing specific parts of the AI response and the correct answer.
    *   **Correctness Details:** For each expected answer part, a boolean indicating whether that part was found in the response.
    *   **Excessive Answers:** A list of strings, each indicating an excessive answer part. If the response provides answers that are **not** in the "Correct Answer" list, add these answers as excessive answers. Return an empty list when there's no excessive answers in the response.
{parts_section}
**Now, proceed with the evaluation using the provided User Prompt, AI Response, and Correct Answer.**

User Prompt (Wrapped in <prompt> and </prompt>):
<prompt>
{prompt}
</prompt>
--------------------
**  Correct Answer (Wrapped in <answer> and </answer>):
Prompt Type: {prompt_type}
<answer>
{answer}
</answer>
--------------------
AI assistant response (Wrapped in <response> and </response>):
<response>
{response}
</response>
--------------------
Rating:"""
