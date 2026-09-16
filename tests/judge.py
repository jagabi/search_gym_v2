"""판정(LLM-as-a-judge)이 실제로 어떻게 채점하는지 눈으로 본다.

    python tests/judge.py                          # deepsearchqa 첫 문항
    python tests/judge.py --benchmark evobrowsecomp
    python tests/judge.py --index 3 --prompt       # 판정 모델에게 가는 프롬프트도 출력
    python tests/judge.py --answer "직접 쓴 응답"

정답·오답·"못 찾았다" 세 가지를 같은 문항에 넣어 보고, 파트별 boolean 과 f1 이
기대대로 움직이는지 확인한다. 여기서 정답이 오답으로 찍히면 채점 프롬프트나
answer_parts 가 잘못된 것이지 에이전트 문제가 아니다.

GOOGLE_API_KEY (또는 GEMINI_API_KEY) 가 필요하다. 모델은 안 띄워도 된다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.benchmarks import load_benchmark  # noqa: E402
from searchgym.config import load_test  # noqa: E402
from searchgym.judge import Judge  # noqa: E402
from searchgym.paths import load_env  # noqa: E402
from searchgym.report import enable_utf8, table  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="판정 모델 점검")
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--benchmark", default=None, help="기본은 conf.yaml 의 벤치마크")
    parser.add_argument("--split", default="validation")
    parser.add_argument("--index", type=int, default=0, help="데이터셋에서 몇 번째 문항인가")
    parser.add_argument("--answer", default=None, help="이 응답 하나만 채점한다")
    parser.add_argument("--prompt", action="store_true", help="판정 프롬프트 전문을 출력")
    parser.add_argument("--schema", action="store_true", help="structured output 스키마를 출력")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    config = load_test(args.conf, benchmark=args.benchmark)
    dataset = config.benchmark.dataset(args.split)
    benchmark = load_benchmark(config.benchmark.name, dataset)
    items = benchmark.load()
    if not 0 <= args.index < len(items):
        print(f"index 는 0..{len(items) - 1} 이어야 합니다.", file=sys.stderr)
        return 1
    item = items[args.index]

    table(
        "문항",
        {
            "benchmark": f"{benchmark.name}  ({dataset.name})",
            "index": item.index,
            "answer_type": item.answer_type,
            "category": item.category or "(없음)",
            "answer_parts": len(item.answer_parts or []) or "(없음 — 판정 모델이 쪼갠다)",
            "judge": config.judge.model,
        },
    )
    print(f"\n질문:\n{item.question}\n\n정답:\n{item.answer}")

    if args.schema:
        print("\n=== 스키마 " + "=" * 50)
        print(json.dumps(benchmark.judge_schema(item), ensure_ascii=False, indent=2))

    # 정답을 그대로 문장에 넣은 것 / 엉뚱한 것 / 못 찾았다는 것.
    cases = (
        [("직접 입력", args.answer)]
        if args.answer
        else [
            ("정답", f"After checking the sources, the answer is {item.answer}."),
            ("오답", "Based on my research, the answer is Antarctica in 1911."),
            ("회피", "I could not find this information."),
        ]
    )

    judge = Judge(config.judge)
    for label, response in cases:
        print(f"\n=== {label} " + "=" * (54 - len(label)))
        if args.prompt:
            print("--- 판정 프롬프트 ---")
            print(benchmark.judge_prompt(item, response))
            print("--- /판정 프롬프트 ---\n")
        print(f"응답: {response}\n")

        judgement = judge.grade(benchmark, item, response)
        if judgement.error:
            print(f"판정 실패: {judgement.error}", file=sys.stderr)
            continue

        metrics = judgement.metrics()
        table(
            "판정",
            {
                "category": judgement.category,
                "f1 / precision / recall": (
                    f"{metrics['f1']:.2f} / {metrics['precision']:.2f} / {metrics['recall']:.2f}"
                ),
                "accuracy": f"{metrics['accuracy']:.0f}",
                "tp / fn / fp": f"{judgement.tp} / {judgement.fn} / {judgement.fp}",
                "extracted": judgement.extracted or "(없음)",
                "latency": f"{judgement.latency_ms:.0f}ms",
                "usage": judgement.usage or "(없음)",
            },
        )
        if judgement.explanation:
            print(f"  설명: {judgement.explanation}")
        for text, found in judgement.parts:
            print(f"  [{'O' if found else 'X'}] {text}")
        for extra in judgement.excessive:
            print(f"  [+] 여분: {extra}")

    print("\n기대: 정답 = fully_correct(f1 1.0) · 오답 = fully_incorrect · 회피 = fully_incorrect")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
