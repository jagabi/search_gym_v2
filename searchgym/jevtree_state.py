"""Question conditions and source-backed candidate memory for JevTree only."""

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

READER_CONTRACT = """Return only a JSON object with this schema:
{
  "page_title": "title",
  "facts": [{"candidate": "exact name on the page, or empty for an unassigned clue",
    "condition_id": "C1", "relation": "supports|contradicts|mentions",
    "fact": "what the source explicitly states", "quote": "verbatim source excerpt"}],
  "leads": [{"name": "exact candidate name or title on the page",
    "quote": "verbatim excerpt containing that name", "condition_ids": ["C1"]}],
  "missing_condition_ids": ["C2"]
}
Use only the supplied condition IDs. 'mentions' means a partial clue, not a
verified match. Supports/contradicts require an explicit source statement about
the named candidate and condition. Do not infer a relation from separate names
on the page. Leads are candidates to investigate, not confirmed answers. Include
useful new candidates even if only one condition is relevant. Preserve exact
dates, numbers, names and relevant table rows in quotes. No deductions, invented
facts or overall answer. An unavailable/irrelevant page may return empty arrays.
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


def normalized(text: str) -> str:
    return " ".join(text.split())


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


def parse_reading(text: str, page: str, conditions: list[dict[str, str]]) -> dict[str, Any]:
    data = json_object(text)
    valid_ids = {c["id"] for c in conditions}
    source = normalized(page)
    facts, leads = data.get("facts"), data.get("leads")
    missing = data.get("missing_condition_ids")
    if not isinstance(facts, list) or not isinstance(leads, list) or not isinstance(missing, list):
        raise ValueError("facts, leads and missing_condition_ids must be arrays")
    if any(not isinstance(c, str) or c not in valid_ids for c in missing):
        raise ValueError("Unknown missing condition ID")
    clean_facts, clean_leads = [], []
    for fact in facts:
        if not isinstance(fact, dict):
            raise ValueError("Invalid fact")
        candidate, quote = fact.get("candidate"), fact.get("quote")
        if (not isinstance(candidate, str) or not isinstance(quote, str)
                or not normalized(quote) or normalized(quote) not in source
                or (candidate and normalized(candidate) not in normalized(quote))
                or fact.get("condition_id") not in valid_ids
                or fact.get("relation") not in {"supports", "contradicts", "mentions"}
                or not isinstance(fact.get("fact"), str) or not fact["fact"].strip()):
            raise ValueError("Facts need a known condition and a source quote containing the candidate")
        clean_facts.append({k: fact[k] for k in ("candidate", "condition_id", "relation", "fact", "quote")})
    for lead in leads:
        if not isinstance(lead, dict):
            raise ValueError("Invalid lead")
        name, quote, ids = lead.get("name"), lead.get("quote"), lead.get("condition_ids")
        if (not isinstance(name, str) or not name.strip() or not isinstance(quote, str)
                or not normalized(quote) or normalized(quote) not in source
                or normalized(name) not in normalized(quote) or not isinstance(ids, list)
                or not ids or any(not isinstance(c, str) or c not in valid_ids for c in ids)):
            raise ValueError("Leads need known conditions and a source quote containing their name")
        clean_leads.append({"name": name, "quote": quote, "condition_ids": ids})
    return {"page_title": str(data.get("page_title") or ""), "facts": clean_facts,
            "leads": clean_leads, "missing_condition_ids": missing}


CANDIDATE_UPDATES_SCHEMA = {
    "type": "array",
    "description": "Update remembered candidates before this search. Omit unchanged candidates; they persist.",
    "items": {
        "type": "object",
        "properties": {
            "candidate_id": {"type": "string"},
            "action": {"type": "string", "enum": ["retain", "verify", "reject"]},
            "reason": {"type": "string", "description": "Why this action follows from the evidence or missing condition."},
            "evidence_ids": {"type": "array", "items": {"type": "string"},
                             "description": "For reject, cite stored contradicting evidence for this candidate."},
        },
        "required": ["candidate_id", "action", "reason"],
        "additionalProperties": False,
    },
}


class CandidateMemory:
    def __init__(self) -> None:
        self.candidates: dict[str, dict[str, Any]] = {}
        self.evidence: dict[str, dict[str, Any]] = {}
        self._names: dict[str, str] = {}

    def _candidate(self, name: str) -> dict[str, Any]:
        key = normalized(name).casefold()
        if key not in self._names:
            cid = f"K{len(self.candidates) + 1}"
            self._names[key] = cid
            self.candidates[cid] = {"id": cid, "name": name, "status": "retained",
                                    "reason": "Source candidate; not yet verified", "evidence_ids": []}
        return self.candidates[self._names[key]]

    def ingest(self, reading: dict[str, Any], url: str) -> None:
        for fact in reading["facts"]:
            if fact["candidate"]:
                self._add(fact["candidate"], url, fact["condition_id"], fact["relation"], fact["quote"])
        for lead in reading["leads"]:
            for condition in lead["condition_ids"]:
                self._add(lead["name"], url, condition, "mentions", lead["quote"])

    def _add(self, name: str, url: str, condition: str, relation: str, quote: str) -> None:
        candidate = self._candidate(name)
        item = {"candidate_id": candidate["id"], "url": url, "condition_id": condition,
                "relation": relation, "quote": quote}
        if item in self.evidence.values():
            return
        eid = f"E{len(self.evidence) + 1}"
        self.evidence[eid] = item
        candidate["evidence_ids"].append(eid)
        # A rejected candidate stays visible; new evidence requires reconsideration.
        if candidate["status"] == "rejected":
            candidate.update(status="retained", reason="New source evidence; reconsider prior rejection")

    def update(self, updates: Any) -> None:
        if not isinstance(updates, list):
            raise ValueError("candidate_updates must be an array")
        # Validate the entire batch before changing any state.
        for item in updates:
            if not isinstance(item, dict):
                raise ValueError("Invalid candidate update")
            cid, action, reason = item.get("candidate_id"), item.get("action"), item.get("reason")
            ids = item.get("evidence_ids", [])
            if (not isinstance(cid, str) or cid not in self.candidates
                    or action not in ("retain", "verify", "reject")
                    or not isinstance(reason, str) or not reason.strip()
                    or not isinstance(ids, list)):
                raise ValueError("Candidate updates need a known ID, action and reason")
            if any(not isinstance(e, str) or e not in self.evidence
                   or self.evidence[e]["candidate_id"] != cid for e in ids):
                raise ValueError("Evidence must belong to the candidate being updated")
            if action == "reject" and not any(self.evidence[e]["relation"] == "contradicts" for e in ids):
                raise ValueError("Reject needs stored contradicting evidence; unknown facts cannot exclude a candidate")
        for item in updates:
            self.candidates[item["candidate_id"]].update(
                status={"retain": "retained", "verify": "verifying", "reject": "rejected"}[item["action"]],
                reason=item["reason"], decision_evidence_ids=item.get("evidence_ids", []))

    def render(self, conditions: list[dict[str, str]]) -> str:
        rows = []
        for candidate in self.candidates.values():
            relations = {"supports": {}, "contradicts": {}, "mentions": {}}
            for eid in candidate["evidence_ids"]:
                fact = self.evidence[eid]
                relations[fact["relation"]].setdefault(fact["condition_id"], []).append(eid)
            known = set(relations["supports"]) | set(relations["contradicts"])
            rows.append({**candidate, "conditions": relations,
                         "unknown": [c["id"] for c in conditions if c["id"] not in known]})
        return ("Persistent candidate memory (source claims, not established truth). Unknown is not false. "
                "Compare quotes with the original question. Use candidate_updates to record verification "
                "or evidence-backed rejection; omitted candidates remain.\n" + json.dumps(
                    {"question_conditions": conditions, "candidates": rows, "evidence": self.evidence},
                    ensure_ascii=False, separators=(",", ":")))
