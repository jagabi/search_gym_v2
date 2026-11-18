"""GEPA 교사에게 실제로 무엇이 가는지 본다 — GEPA 를 돌리지 않고.

    python tests/reflection.py --run runs/test/<런> --indices 3,5 --component decision
    python tests/reflection.py --run runs/test/<런> --component agent --call   # 교사 한 번 호출

이미 끝난 test 실행(response.json · trace.jsonl · records.jsonl)으로 문항별 side_info 를
만들고, reflection_prompt 에 채워 교사에게 갈 프롬프트 전체를 출력한다. 시드 프롬프트는
설정 그대로다. RawTree 방법(search-o1-decision)만 지원한다.

`--call` 이면 교사를 한 번 불러 제안을 출력한다(ANTHROPIC_API_KEY, anthropic 필요).
기본은 출력만 하므로 키도 패키지도 필요 없다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.agent import RAW_METHODS  # noqa: E402
from searchgym.benchmarks import Item  # noqa: E402
from searchgym.config import load_train  # noqa: E402
from searchgym.gepa import (  # noqa: E402
    Teacher, render_agent_example, render_decision_example, rollout_searches,
)
from searchgym.paths import load_env, resolve  # noqa: E402
from searchgym.rawtree import EVIDENCE_INSTRUCTIONS  # noqa: E402
from searchgym.report import enable_utf8  # noqa: E402
from searchgym.runner import Record, _result_from  # noqa: E402
from searchgym.scoring import Judgement  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GEPA 교사 입력 점검")
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--gepa", default="configs/gepa-decision.yaml")
    parser.add_argument("--method", default="search-o1-decision")
    parser.add_argument("--run", required=True, help="runs/test/<런> 디렉터리")
    parser.add_argument("--indices", default="", help="문항 index 목록(쉼표). 비우면 앞에서 5개")
    parser.add_argument("--component", default="agent", choices=["agent", "decision"])
    parser.add_argument("--call", action="store_true", help="교사를 실제로 한 번 부른다")
    parser.add_argument("--out", default="", help="교사 프롬프트를 파일로도 저장")
    return parser.parse_args(argv)


def load_records(run: Path, indices: list[int]) -> list[tuple[Item, Record]]:
    scores = {}
    for line in (run / "records.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            scores[row["index"]] = float(row.get("f1") or 0.0)
    dirs = sorted(run.glob("q*/response.json"))
    if not indices:
        indices = [int(p.parent.name[1:]) for p in dirs[:5]]
    out = []
    for index in indices:
        qdir = run / f"q{index:05d}"
        response = json.loads((qdir / "response.json").read_text(encoding="utf-8"))
        item = Item(index=index, question=response["question"], answer=response["gold_answer"],
                    category=response.get("category", ""))
        record = Record(index=index, category=item.category, score=scores.get(index, 0.0),
                        judgement=Judgement(), result=_result_from(response),
                        dir=qdir.name, trace_id=response.get("trace_id", ""),
                        trace_path=str((qdir / "trace.jsonl").resolve()))
        out.append((item, record))
    return out


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)
    config = load_train(args.conf, args.gepa, method=args.method)
    if config.base.method not in RAW_METHODS:
        print("RawTree 방법만 지원합니다.", file=sys.stderr)
        return 1

    run = resolve(args.run)
    indices = [int(x) for x in args.indices.split(",") if x.strip()]
    rows = load_records(run, indices)

    render = render_agent_example if args.component == "agent" else render_decision_example
    examples = [render(n, item, record, rollout_searches(record)) for n, (item, record) in enumerate(rows, 1)]
    current = (config.base.system_prompt if args.component == "agent"
               else config.base.agent.jev_evidence_instructions or EVIDENCE_INSTRUCTIONS)
    template = config.components[args.component].reflection_prompt
    prompt = template.replace("<curr_param>", current).replace("<side_info>", "\n\n".join(examples))

    print(prompt)
    print(f"\n[{args.component}] {len(rows)} examples, {len(prompt):,} chars", file=sys.stderr)
    if args.out:
        Path(args.out).write_text(prompt, encoding="utf-8")

    if args.call:
        teacher = Teacher(config.teacher, run / "_reflection_preview")
        proposed = teacher.propose(args.component, prompt)
        print("\n=== 제안 " + "=" * 50)
        print(proposed if proposed else "(제안 없음: 잘림/거절/코드펜스 없음)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
