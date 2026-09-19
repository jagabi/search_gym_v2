"""raw.* → 카테고리 균등 추출 source.json.

    python scripts/sample_source.py browsecomp --size 300

원본이 너무 크거나 카테고리가 치우쳐 있을 때 쓴다. `build_splits.py`의 리더와
라운드로빈 추출을 그대로 재사용하므로 결과 형식과 seed 의미가 같다. split 없이
source.json 하나만 필요한 경우를 위한 스크립트다.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_splits import _READERS, _find_raw, stratified  # noqa: E402

from searchgym.paths import resolve  # noqa: E402
from searchgym.report import enable_utf8, table  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    parser = argparse.ArgumentParser(description="카테고리 균등 추출 → source.json")
    parser.add_argument("benchmark", choices=sorted(_READERS))
    parser.add_argument("--raw", default=None)
    parser.add_argument("--out", default=None)
    parser.add_argument("--size", type=int, default=300)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--no-stratify", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    out_dir = resolve(args.out or f"data/{args.benchmark}")
    raw_path = resolve(args.raw) if args.raw else _find_raw(out_dir)
    if raw_path is None or not raw_path.exists():
        print(f"원본을 찾지 못했습니다. --raw로 지정하세요. (본 곳: {out_dir})", file=sys.stderr)
        return 1
    if raw_path.name == "source.json":
        print("source.json을 원본으로 읽으면 자기 자신을 덮어씁니다. --raw로 지정하세요.", file=sys.stderr)
        return 1

    records = _READERS[args.benchmark](raw_path)
    if len(records) < args.size:
        print(f"원본이 {len(records)}행뿐입니다. {args.size}개가 필요합니다.", file=sys.stderr)
        return 1

    out_path = out_dir / "source.json"
    if out_path.exists() and not args.force:
        print(f"이미 있습니다: {out_path}. --force로 덮어쓰세요.", file=sys.stderr)
        return 1

    chosen = stratified(records, {"source": args.size}, args.seed, not args.no_stratify)["source"]

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(chosen, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = Counter(r["category"] for r in chosen).most_common()
    lengths = sorted(len(r["answer"]) for r in chosen)
    table(
        f"{args.benchmark} source",
        {
            "원본": f"{raw_path.name}  ({len(records)}행)",
            "추출": f"{len(chosen)}행  (seed {args.seed})",
            "카테고리": ", ".join(f"{c or '(없음)'} {n}" for c, n in counts),
            "정답 길이": f"중앙값 {lengths[len(lengths) // 2]}자 / 최대 {lengths[-1]}자",
            "출력": out_path,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
