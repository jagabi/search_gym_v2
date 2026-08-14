"""프롬프트 하나를 벤치마크에서 평가한다.

    python eval.py                              # configs/eval.yaml
    python eval.py --config configs/eval.yaml --tag baseline
    python eval.py --benchmark evobrowsecomp --limit 20

학습(train.py)과 완전히 분리돼 있다. 문항마다 트레이스를 즉시 쓰므로 중간에 죽어도
받은 응답은 남고, 캐시가 켜져 있으면 다시 돌릴 때 건너뛴다.

중간에 멈췄다면 `--resume`으로 **같은 디렉터리에** 이어 붙인다.

    python eval.py --tag baseline               # 어제
    python eval.py --tag baseline --resume      # 오늘, 끝난 문항은 건너뛴다
"""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import asdict
import sys
from pathlib import Path

from searchgym.benchmarks import default_dataset, load_benchmark
from searchgym.config import load_eval
from searchgym.judge import Judge
from searchgym.paths import PROJECT_ROOT, find_run, load_env, resolve, run_dir
from searchgym.report import enable_utf8, summarize, table, write_json
from searchgym.runner import Runner
from searchgym.serving import profile_for


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="검색 프롬프트를 벤치마크에서 평가한다")
    parser.add_argument("--config", default="configs/eval.yaml")
    parser.add_argument("--tag", default=None, help="실행 디렉터리 이름에 붙일 꼬리표")
    parser.add_argument("--benchmark", default=None, help="설정의 datasets 중 하나만 돈다")
    parser.add_argument("--prompt", default=None, help="prompt_path를 덮어쓴다")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument(
        "--resume",
        nargs="?",
        const="",
        default=None,
        metavar="DIR",
        help="새 디렉터리를 만들지 않고 기존 실행에 이어 붙인다. "
             "디렉터리를 생략하면 같은 model/benchmark/tag의 가장 최근 실행을 찾는다",
    )
    return parser.parse_args(argv)


async def main_async(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    config = load_eval(args.config)
    if args.prompt:
        config.prompt_path, config.prompt_text = args.prompt, ""
    if args.tag:
        config.run.tag = args.tag

    datasets = config.datasets
    if args.benchmark:
        datasets = [d for d in datasets if d.name == args.benchmark]
        if not datasets:
            print(f"설정에 '{args.benchmark}' 데이터셋이 없습니다.", file=sys.stderr)
            return 1
    datasets = [d for d in datasets if (args.limit if args.limit is not None else d.limit) != 0]
    if not datasets:
        print("돌릴 데이터셋이 없습니다 (limit이 전부 0입니다).", file=sys.stderr)
        return 1

    profile = profile_for(config.model)
    system_prompt = config.system_prompt()
    label = datasets[0].name if len(datasets) == 1 else "multi"

    # 이어 돌리기는 캐시가 전부다. 캐시를 끄면 이어 붙일 것이 없다.
    if args.resume is not None and args.no_cache:
        print("--resume과 --no-cache는 같이 못 씁니다.", file=sys.stderr)
        return 1

    if args.resume is None:
        out = run_dir("eval", profile.repo, label, config.run.tag, config.run.output_dir)
    elif args.resume:
        out = resolve(args.resume)
        if not out.is_dir():
            print(f"이어 돌릴 디렉터리가 없습니다: {out}", file=sys.stderr)
            return 1
    else:
        found = find_run("eval", profile.repo, label, config.run.tag, config.run.output_dir)
        if found is None:
            print(
                f"이어 돌릴 실행을 못 찾았습니다 "
                f"({profile.repo} / {label} / tag={config.run.tag or '없음'}). "
                f"--resume <디렉터리>로 직접 지정하세요.",
                file=sys.stderr,
            )
            return 1
        out = found

    table(
        "설정",
        {
            "model": f"{profile.key}  ({profile.repo})",
            "weights": "local" if profile.is_local else "hub",
            "endpoint": config.agent.base_url,
            "prompt": config.prompt_path or ("inline" if system_prompt else "(none)"),
            "prompt_chars": len(system_prompt),
            "budget": f"search {config.agent.max_searches} / fetch "
                      f"{config.agent.max_fetches or '무제한'} / "
                      f"context {config.agent.context_limit:,}",
            "refine": config.agent.refine_fetched,
            "judge": config.judge.model,
            "datasets": ", ".join(d.name for d in datasets),
            "workers": config.run.workers,
            "run_dir": f"{out}{'   (이어 돌리기)' if args.resume is not None else ''}",
        },
    )

    write_json(
        out / "config.json",
        {
            "source": config.source,
            "model": profile.repo,
            "agent": asdict(config.agent),
            "judge": asdict(config.judge),
            "prompt_source": config.prompt_path,
            "prompt_chars": len(system_prompt),
            "datasets": [d.name for d in datasets],
        },
    )
    if system_prompt:
        (out / "prompt.txt").write_text(system_prompt, encoding="utf-8")

    judge = Judge(config.judge)
    results: dict[str, dict] = {}

    for entry in datasets:
        dataset = entry.path or default_dataset(entry.name, "test")
        benchmark = load_benchmark(entry.name, dataset)
        limit = args.limit if args.limit is not None else entry.limit
        items = benchmark.load(limit=limit)

        runner = Runner(
            profile=profile,
            agent_config=config.agent,
            judge=judge,
            run_dir=out / entry.name,
            use_cache=config.run.cache and not args.no_cache,
            workers=config.run.workers,
        )

        if args.resume is not None:
            # 캐시에 있는 문항은 다시 안 태운다. 그래도 전부 훑어야 summary가
            # 온전하다 — 캐시 조회는 파일 읽기라 공짜다.
            todo = runner.pending(benchmark, items, system_prompt)
            print(f"\n[{entry.name}] 전체 {len(items)}문항 · 완료 {len(items) - len(todo)} · 남은 {len(todo)}")
            if not todo:
                print("  남은 문항이 없습니다. 집계만 다시 씁니다.")
            # 아래에서 모든 문항이 다시 기록되므로 지난 줄과 겹치지 않게 비운다.
            (out / entry.name / "records.jsonl").unlink(missing_ok=True)
        else:
            print(f"\n[{entry.name}] {len(items)}문항 실행 중...")

        records = await runner.run_all(benchmark, items, system_prompt, "f1")

        summary = summarize(records)
        results[entry.name] = summary
        write_json(out / entry.name / "summary.json", summary)
        table(f"{entry.name} 결과", {k: v for k, v in summary.items() if not isinstance(v, dict)})

    write_json(
        out / "summary.json",
        {
            "model": profile.repo,
            "prompt_source": config.prompt_path,
            "prompt_chars": len(system_prompt),
            "judge": config.judge.model,
            "budget": {"searches": config.agent.max_searches, "fetches": config.agent.max_fetches},
            "benchmarks": results,
        },
    )
    print(f"\n저장됨: {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    return asyncio.run(main_async(argv))


if __name__ == "__main__":
    raise SystemExit(main())
