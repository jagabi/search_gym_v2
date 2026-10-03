"""Question-condition extraction for JevTree; reader notes are not parsed."""

from __future__ import annotations

import json
import re
from typing import Any


CONDITION_PROMPT = """Extract the identifying conditions in the original question.
Return only JSON: {"conditions": ["exact contiguous excerpt from the question", ...]}.
Keep dates, ranges, relations, qualifiers and the requested answer type. Each item
must be copied verbatim from the question; do not guess any names, countries,
nationalities, years or answers. Cover all conditions without adding hypotheses.
"""

def json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value


def parse_conditions(text: str, question: str) -> list[dict[str, str]]:
    items = json_object(text).get("conditions")
    if not isinstance(items, list) or not items:
        raise ValueError("conditions must be a non-empty list")
    excerpts = []
    for item in items:
        if not isinstance(item, str) or not item.strip() or item not in question:
            raise ValueError("Every condition must be an exact excerpt of the question")
        if item not in excerpts:
            excerpts.append(item)
    return [{"id": f"C{i}", "text": item} for i, item in enumerate(excerpts, 1)]
