"""MuSiQue / Bamboogle → 통일 형식 test.json (Search-o1 과 같은 FlashRAG 원본).

    python scripts/build_multihop.py

원본: https://huggingface.co/datasets/RUC-NLPIR/FlashRAG_datasets
    data/musique/raw/dev.jsonl     MuSiQue-Ans dev 2,417문항 (FlashRAG 가공본)
    data/bamboogle/raw/test.jsonl  Bamboogle 125문항

MuSiQue 는 2·3·4홉 각 100문항을 뽑는다. FlashRAG 가 원래 id(2hop__, 3hop1__ ...)를
dev_N 으로 바꿔 두었으므로 홉 수는 하위 질문 수로, 구조 유형은 하위 질문이 앞
답(#1, #2 ...)을 참조하는 모양으로 정한다. 같은 홉 안에서는 구조 유형별 원래 비율대로
나눠 뽑고, 이미 뽑힌 문항과 첫 하위 질문(출발 대상)이 겹치는 문항은 건너뛴다.
출발 대상이 모자란 구조는 전체 하위 질문이 가장 덜 겹치는 문항으로 채우고 그 수를
sample_meta.json 에 기록한다. Bamboogle 은 전부 쓴다.

정답 외 표기(FlashRAG golden_answers 의 나머지)는 answer_aliases 로 남겨 판정에 넘긴다.
"""

from __future__ import annotations

import ast
import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://huggingface.co/datasets/RUC-NLPIR/FlashRAG_datasets"
SOURCE_COMMIT = "bcafb8dd07d453be3cbeeeb3f78be1841bddf92c"
SEED = 0
PER_HOP = 100


def _value(raw):
    """FlashRAG stores some fields as Python literals inside JSON strings."""
    return ast.literal_eval(raw) if isinstance(raw, str) else raw


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _answers(raw) -> tuple[str, list[str]]:
    answers = [str(a).strip() for a in _value(raw) if str(a).strip()]
    unique = list(dict.fromkeys(answers))
    return unique[0], unique[1:]


def _quotas(counts: dict, total: int) -> dict:
    """Largest-remainder split of `total` in proportion to `counts`."""
    size = sum(counts.values())
    exact = {k: total * v / size for k, v in counts.items()}
    quota = {k: int(x) for k, x in exact.items()}
    for k in sorted(exact, key=lambda k: (-(exact[k] - quota[k]), str(k)))[:total - sum(quota.values())]:
        quota[k] += 1
    return quota


def build_musique() -> dict:
    raw_path = ROOT / "data" / "musique" / "raw" / "dev.jsonl"
    rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    pool = defaultdict(list)
    skipped = Counter()
    for row in rows:
        meta = _value(row["metadata"])
        steps = meta.get("question_decomposition") or []
        if not meta.get("answerable", True):
            skipped["unanswerable"] += 1
            continue
        if not 2 <= len(steps) <= 4:
            skipped["hops_outside_2_4"] += 1
            continue
        # Which earlier answers (#k) each sub-question uses: the composition structure.
        shape = tuple(tuple(sorted({int(k) for k in re.findall(r"#(\d)", s["question"])})) for s in steps)
        answer, aliases = _answers(row["golden_answers"])
        pool[(len(steps), shape)].append({
            "index": int(str(row["id"]).removeprefix("dev_")),
            "question": row["question"].strip(),
            "answer": answer,
            "answer_aliases": aliases,
            "answer_type": "single",
            "category": f"{len(steps)}hop",
            "answer_parts": None,
            "_steps": [s["id"] for s in steps],
        })

    rng = random.Random(SEED)
    chosen, used_steps, quotas, structure_counts = [], set(), {}, {}
    relaxed, used_first = Counter(), set()
    for hops in (2, 3, 4):
        shapes = {shape: len(items) for (h, shape), items in pool.items() if h == hops}
        quota = _quotas(shapes, PER_HOP)
        for shape in sorted(shapes):
            candidates = sorted(pool[(hops, shape)], key=lambda r: r["index"])
            rng.shuffle(candidates)
            taken = []
            for item in candidates:
                if len(taken) == quota[shape]:
                    break
                # One question per starting entity (first sub-question).
                if item["_steps"][0] in used_first:
                    continue
                taken.append(item)
                used_first.add(item["_steps"][0])
                used_steps.update(item["_steps"])
            key = f"{hops}hop {json.dumps(shape)}"
            if len(taken) < quota[shape]:
                # MuSiQue reuses a few chains for some structures (e.g. 10 starting
                # entities for 64 questions): fill with the least overlapping ones.
                rest = [c for c in candidates if c not in taken]
                rest.sort(key=lambda c: (len(used_steps.intersection(c["_steps"])), candidates.index(c)))
                for item in rest[:quota[shape] - len(taken)]:
                    taken.append(item)
                    used_first.add(item["_steps"][0])
                    used_steps.update(item["_steps"])
                    relaxed[key] += 1
            chosen += taken
            quotas[key], structure_counts[key] = quota[shape], shapes[shape]

    chosen.sort(key=lambda r: (r["category"], r["index"]))
    records = [{k: v for k, v in r.items() if not k.startswith("_")} for r in chosen]
    out = ROOT / "data" / "musique" / "test.json"
    out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = {
        "source": SOURCE, "source_commit": SOURCE_COMMIT, "source_file": "musique/dev.jsonl",
        "source_sha256": _sha256(raw_path), "source_rows": len(rows), "skipped": dict(skipped),
        "seed": SEED, "per_hop": PER_HOP, "dev_hop_counts": dict(Counter(f"{h}hop" for (h, _), v in pool.items() for _ in v)),
        "structure_quota": quotas, "dev_structure_counts": structure_counts,
        "dedup": "one question per starting entity (first sub-question id); where a structure has too few, the least overlapping fill the quota",
        "dedup_relaxed": dict(relaxed),
        "selected_indices": [r["index"] for r in records],
    }
    (ROOT / "data" / "musique" / "sample_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def build_bamboogle() -> dict:
    raw_path = ROOT / "data" / "bamboogle" / "raw" / "test.jsonl"
    rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    records = []
    for i, row in enumerate(rows):
        answer, aliases = _answers(row["golden_answers"])
        records.append({"index": i, "question": row["question"].strip(), "answer": answer,
                        "answer_aliases": aliases, "answer_type": "single", "category": "",
                        "answer_parts": None})
    out = ROOT / "data" / "bamboogle" / "test.json"
    out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    meta = {"source": SOURCE, "source_commit": SOURCE_COMMIT, "source_file": "bamboogle/test.jsonl",
            "source_sha256": _sha256(raw_path), "rows": len(records), "sampling": "all questions"}
    (ROOT / "data" / "bamboogle" / "sample_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def main() -> int:
    musique, bamboogle = build_musique(), build_bamboogle()
    print("musique:", len(musique["selected_indices"]), "questions;", musique["structure_quota"])
    print("bamboogle:", bamboogle["rows"], "questions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
