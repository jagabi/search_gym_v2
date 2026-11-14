"""Fixed 100-question DSQA subset for the bundle-size x top-n grid.

    python scripts/build_grid_subset.py

Drawn from data/deepsearchqa/test.json (the 300 main-result questions) so the main
run's 2048 x 4 cell can be reused on exactly these questions. Stratified by
category x answer_type with largest-remainder allocation; seed fixed. Writes
data/deepsearchqa/grid100.json (same item format, original `index` kept) and
grid100_meta.json.
"""
from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "deepsearchqa" / "test.json"
OUT = ROOT / "data" / "deepsearchqa" / "grid100.json"
SIZE, SEED = 100, 0


def main() -> None:
    items = json.loads(SOURCE.read_text(encoding="utf-8"))
    strata = defaultdict(list)
    for item in items:
        strata[(item["category"], item.get("answer_type") or "")].append(item)
    keys = sorted(strata)
    exact = {k: SIZE * len(strata[k]) / len(items) for k in keys}
    quota = {k: int(exact[k]) for k in keys}
    for k in sorted(keys, key=lambda k: (-(exact[k] - quota[k]), k))[:SIZE - sum(quota.values())]:
        quota[k] += 1
    rng = random.Random(SEED)
    chosen = []
    for k in keys:
        chosen += rng.sample(sorted(strata[k], key=lambda x: x["index"]), quota[k])
    chosen.sort(key=lambda x: x["index"])
    OUT.write_text(json.dumps(chosen, ensure_ascii=False, indent=1), encoding="utf-8")
    meta = {"source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"), "size": len(chosen), "seed": SEED,
            "stratified_by": ["category", "answer_type"],
            "category": dict(Counter(x["category"] for x in chosen)),
            "answer_type": dict(Counter(x.get("answer_type") for x in chosen)),
            "indices": [x["index"] for x in chosen]}
    OUT.with_name("grid100_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(chosen)} questions -> {OUT.relative_to(ROOT)}")
    print("category:", meta["category"])
    print("answer_type:", meta["answer_type"])


if __name__ == "__main__":
    main()
