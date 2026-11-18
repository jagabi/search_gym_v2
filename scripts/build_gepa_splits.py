"""GEPA train/val for DSQA: 30 / 30 from the test questions outside grid100.

    python scripts/build_gepa_splits.py

Pool = data/deepsearchqa/test.json minus grid100.json (200 questions), so the GEPA test
set (grid100) never overlaps train/val. Each split keeps the main run's accuracy mix of
test.json: questions are bucketed by their F1 in the main gpt-oss + d3-mini run (0 / partial
/ 1) and drawn per bucket with largest-remainder allocation, seed fixed. Writes
gepa_train.json, gepa_val.json and gepa_split_meta.json next to the source.
"""
from __future__ import annotations

import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "deepsearchqa"
MAIN_RUN = "runs/test/20261110-2009_*deepsearchqa_decision_d3-mini_b2048_300"
SIZE, SEED = 30, 0


def bucket(f1: float) -> str:
    return "wrong" if f1 <= 0 else ("correct" if f1 >= 0.999 else "partial")


def main() -> None:
    test = json.loads((DATA / "test.json").read_text(encoding="utf-8"))
    grid = {x["index"] for x in json.loads((DATA / "grid100.json").read_text(encoding="utf-8"))}
    run = next(ROOT.glob(MAIN_RUN))
    f1 = {}
    for line in (run / "records.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            f1[row["index"]] = float(row.get("f1") or 0.0)

    pool = defaultdict(list)
    for item in test:
        if item["index"] not in grid:
            pool[bucket(f1[item["index"]])].append(item)

    # Target mix = the main run's buckets over all 300 test questions.
    target = Counter(bucket(f1[x["index"]]) for x in test)
    keys = sorted(target)
    exact = {k: SIZE * target[k] / len(test) for k in keys}
    quota = {k: int(exact[k]) for k in keys}
    for k in sorted(keys, key=lambda k: (-(exact[k] - quota[k]), k))[:SIZE - sum(quota.values())]:
        quota[k] += 1

    rng = random.Random(SEED)
    train, val = [], []
    for k in keys:
        drawn = rng.sample(sorted(pool[k], key=lambda x: x["index"]), 2 * quota[k])
        train += drawn[:quota[k]]
        val += drawn[quota[k]:]
    train.sort(key=lambda x: x["index"])
    val.sort(key=lambda x: x["index"])

    for name, items in (("gepa_train", train), ("gepa_val", val)):
        (DATA / f"{name}.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")

    def describe(items):
        return {"f1_bucket": dict(Counter(bucket(f1[x["index"]]) for x in items)),
                "mean_f1": round(sum(f1[x["index"]] for x in items) / len(items), 3),
                "answer_type": dict(Counter(x.get("answer_type") for x in items)),
                "category": dict(Counter(x["category"] for x in items)),
                "indices": [x["index"] for x in items]}

    meta = {"source": "data/deepsearchqa/test.json minus grid100.json",
            "stratified_by": "F1 bucket (0 / partial / 1) in " + run.name,
            "size": SIZE, "seed": SEED,
            "overlap": {"train_val": len({x["index"] for x in train} & {x["index"] for x in val}),
                        "train_grid100": len({x["index"] for x in train} & grid),
                        "val_grid100": len({x["index"] for x in val} & grid)},
            "test300": {k: v for k, v in describe(test).items() if k != "indices"},
            "train": describe(train), "val": describe(val)}
    (DATA / "gepa_split_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    for name in ("test300", "train", "val"):
        print(f"{name:8s} buckets {meta[name]['f1_bucket']}  mean F1 {meta[name]['mean_f1']}")
    print("overlap", meta["overlap"])


if __name__ == "__main__":
    main()
