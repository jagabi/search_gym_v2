"""원본 데이터셋 → 통일 형식 + train/validation/test split.

    python scripts/build_splits.py deepsearchqa --force
    python scripts/build_splits.py evobrowsecomp --force

`--stratify`(기본 켜짐)면 카테고리를 균등하게 뽑는다. DeepSearchQA는 카테고리가
심하게 치우쳐 있어서(Politics 148건 대 Linguistics 1건) 무작위로 뽑으면 30문항짜리
valset이 사실상 두 분야로 채워지고, 최적화가 그 분야의 검색 습관에만 맞춰진다.

출력은 `searchgym/benchmarks/_base.py`의 통일 레코드 형식이다. 새 벤치마크
(browsecomp, kbrowsecomp)를 붙일 때는 `_READERS`에 원본 → 통일 형식 변환 함수를
한 줄 추가하면 된다.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.paths import PROJECT_ROOT, resolve  # noqa: E402
from searchgym.report import enable_utf8, table  # noqa: E402

# 정답에 이런 게 섞여 있으면 콤마 분해가 원본 의미를 깬다.
#   "* Allisha Gray, University of South Carolina\n* ..."  개행 그룹
#   "Hungary: 2009, 2020, Bulgaria: 2009, 2020"            키:값 그룹
_UNSAFE = ("\n", ":")


# --- 원본 리더 ---------------------------------------------------------------


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _read_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path}는 객체 배열이어야 합니다.")
    return data


def read_deepsearchqa(path: Path) -> list[dict[str, Any]]:
    """problem/answer/answer_type/problem_category → 통일 형식."""
    records = []
    for index, row in enumerate(_read_json(path)):
        question = (row.get("problem") or row.get("question") or "").strip()
        answer = (row.get("answer") or "").strip()
        if not question or not answer:
            continue
        is_set = (row.get("answer_type") or "").strip().lower().startswith("set")
        records.append(
            {
                "index": int(row.get("index", index)),
                "question": question,
                "answer": answer,
                "answer_type": "set" if is_set else "single",
                "category": (row.get("problem_category") or "").strip(),
                "answer_parts": row.get("answer_parts") or (split_answer(answer) if is_set else [answer]),
            }
        )
    return records


def read_single(path: Path) -> list[dict[str, Any]]:
    """question/answer 두 필드짜리 단일 정답 원본(jsonl 또는 json)."""
    rows = _read_jsonl(path) if path.suffix == ".jsonl" else _read_json(path)
    records = []
    for index, row in enumerate(rows):
        question = (row.get("question") or row.get("problem") or "").strip()
        answer = (row.get("answer") or "").strip()
        if not question or not answer:
            continue
        records.append(
            {
                "index": int(row.get("index", index)),
                "question": question,
                "answer": answer,
                "answer_type": "single",
                "category": (row.get("category") or row.get("problem_category") or "").strip(),
                "answer_parts": [answer],
            }
        )
    return records


_READERS: dict[str, Callable[[Path], list[dict[str, Any]]]] = {
    "deepsearchqa": read_deepsearchqa,
    "evobrowsecomp": read_single,
    "browsecomp": read_single,
    "kbrowsecomp": read_single,
}


# --- 정답 분해 ---------------------------------------------------------------


def split_answer(answer: str) -> list[str] | None:
    """목록형 정답을 결정적으로 쪼갠다. 모호하면 None(= 판정 모델에게 맡김)."""
    answer = answer.strip()
    if not answer or any(marker in answer for marker in _UNSAFE):
        return None
    if " and " in answer.lower() or "," not in answer:
        return None
    parts = _split_top_level(answer)
    return parts if parts and len(parts) >= 2 else None


def _split_top_level(text: str) -> list[str] | None:
    """괄호·따옴표 **밖**의 콤마에서만 자른다.

    그냥 split(",")을 쓰면 "Den (Tokyo, Japan), Odette (Singapore)"가
    ['Den (Tokyo', 'Japan)', ...]로 깨진다.
    """
    parts: list[str] = []
    buffer: list[str] = []
    depth = 0
    quoted = False

    for char in text:
        if char == '"':
            quoted = not quoted
        elif not quoted:
            if char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
                if depth < 0:
                    return None
            elif char == "," and depth == 0:
                parts.append("".join(buffer))
                buffer = []
                continue
        buffer.append(char)

    if depth != 0 or quoted:
        return None
    parts.append("".join(buffer))
    return [p.strip() for p in parts if p.strip()]


# --- 분할 -------------------------------------------------------------------


def stratified(
    records: list[dict[str, Any]], sizes: dict[str, int], seed: int, stratify: bool
) -> dict[str, list[dict[str, Any]]]:
    """카테고리를 최대한 균등하게 채우며 split을 만든다. 서로 겹치지 않는다."""
    rng = random.Random(seed)
    pools: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        pools[record["category"] if stratify else ""].append(record)
    for pool in pools.values():
        rng.shuffle(pool)

    order = sorted(pools, key=lambda c: (-len(pools[c]), c))
    splits: dict[str, list[dict[str, Any]]] = {}

    for name, size in sizes.items():
        chosen: list[dict[str, Any]] = []
        # 카테고리를 라운드로빈으로 한 건씩 가져간다. 큰 카테고리가 독점하지 않는다.
        while len(chosen) < size:
            took = False
            for category in order:
                if len(chosen) >= size:
                    break
                if pools[category]:
                    chosen.append(pools[category].pop())
                    took = True
            if not took:
                break
        if len(chosen) < size:
            raise ValueError(f"{name}에 {size}개가 필요한데 남은 문항이 {len(chosen)}개뿐입니다.")
        chosen.sort(key=lambda r: r["index"])
        splits[name] = chosen
    return splits


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    parser = argparse.ArgumentParser(description="원본 → 통일 형식 + split")
    parser.add_argument("benchmark", choices=sorted(_READERS))
    parser.add_argument("--raw", default=None, help="원본 파일 (기본: data/<벤치>/raw.* 또는 source.json)")
    parser.add_argument("--out", default=None, help="출력 디렉터리 (기본: data/<벤치>)")
    parser.add_argument("--train", type=int, default=30)
    parser.add_argument("--val", type=int, default=30)
    parser.add_argument("--test", type=int, default=300)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--no-stratify", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    out_dir = resolve(args.out or f"data/{args.benchmark}")
    raw_path = resolve(args.raw) if args.raw else _find_raw(out_dir)
    if raw_path is None or not raw_path.exists():
        print(f"원본을 찾지 못했습니다. --raw로 지정하세요. (본 곳: {out_dir})", file=sys.stderr)
        return 1

    records = _READERS[args.benchmark](raw_path)
    sizes = {"train": args.train, "validation": args.val, "test": args.test}
    wanted = sum(sizes.values())
    if len(records) < wanted:
        print(f"원본이 {len(records)}행뿐입니다. {wanted}개가 필요합니다.", file=sys.stderr)
        return 1

    targets = {"source": records}
    targets.update(stratified(records, sizes, args.seed, not args.no_stratify))

    existing = [n for n in targets if (out_dir / f"{n}.json").exists()]
    if existing and not args.force:
        print(f"이미 있습니다: {', '.join(existing)}. --force로 덮어쓰세요.", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in targets.items():
        (out_dir / f"{name}.json").write_text(
            json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    overlap = _overlap(targets)
    (out_dir / "split_meta.json").write_text(
        json.dumps(
            {
                "benchmark": args.benchmark,
                "raw": str(raw_path.relative_to(PROJECT_ROOT)),
                "seed": args.seed,
                "stratified": not args.no_stratify,
                "sizes": {k: len(v) for k, v in targets.items()},
                "overlap": overlap,
                "categories": {
                    name: dict(Counter(r["category"] for r in rows).most_common())
                    for name, rows in targets.items()
                    if name != "source"
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    lengths = sorted(len(r["answer"]) for r in records)
    table(
        f"{args.benchmark} split",
        {
            "원본": f"{raw_path.name}  ({len(records)}행)",
            **{name: len(rows) for name, rows in targets.items()},
            "split 간 중복": f"{overlap}건 (0이어야 정상)",
            "set answer": sum(1 for r in records if r["answer_type"] == "set"),
            "정답 길이": f"중앙값 {lengths[len(lengths) // 2]}자 / 최대 {lengths[-1]}자",
            "출력": out_dir,
        },
    )
    return 0


def _find_raw(out_dir: Path) -> Path | None:
    for name in ("raw.jsonl", "raw.json", "source.json"):
        if (candidate := out_dir / name).exists():
            return candidate
    return None


def _overlap(targets: dict[str, list[dict[str, Any]]]) -> int:
    names = [n for n in ("train", "validation", "test") if n in targets]
    seen: set[int] = set()
    duplicated: set[int] = set()
    for name in names:
        indices = {r["index"] for r in targets[name]}
        duplicated |= seen & indices
        seen |= indices
    return len(duplicated)


if __name__ == "__main__":
    raise SystemExit(main())
