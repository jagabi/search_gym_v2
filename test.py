"""한 방법을 한 벤치마크에서 평가한다.

    python test.py                                   # conf.yaml 그대로
    python test.py --method search-o1 --tag s1
    python test.py --limit 5                         # 배선 확인
    python test.py --split test                      # 마지막에만
    python test.py --tag baseline --resume           # 멈춘 실행 이어서

문항마다 트레이스를 즉시 쓰므로 중간에 죽어도 받은 응답은 남고, 캐시가 켜져 있으면
다시 돌릴 때 건너뛴다. `--resume` 은 새 디렉터리를 만들지 않고 같은 조건의 가장
최근 실행에 이어 붙인다.

산출물:
    runs/test/{날짜}_{방법}_{모델}_{벤치}_{태그}/
      config.json          무엇을 돌렸는가
      prompt.txt           메인 모델 시스템 프롬프트
      explorer_prompt.txt  explorer 시스템 프롬프트
      summary.json         점수 · 탐색 행동 · 예산 사용량
      records.jsonl        문항별 한 줄 요약
      q00022/
        trace.jsonl        이벤트 로그
        response.json      추론 · 응답 · 도구 호출 · 도구 결과
        explorer.json      explorer 호출 트리 (읽은 문서 · 확장 · 반환 요약)
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import asdict

from tqdm import tqdm
from pathlib import Path

from searchgym.benchmarks import load_benchmark
from searchgym.config import load_test
from searchgym.judge import Judge
from searchgym.paths import find_run, load_env, resolve, run_dir
from searchgym.report import enable_utf8, quiet_libraries, summarize, table, write_json
from searchgym.runner import Runner
from searchgym.serving import profile_for


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="검색 방법을 벤치마크에서 평가한다")
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--method", default=None, help="ragent | search-o1 | depthsearch")
    parser.add_argument("--model", default=None, help="qwen | gpt-oss | gemma")
    parser.add_argument("--benchmark", default=None, help="데이터셋 이름")
    parser.add_argument("--path", default=None, help="데이터셋 파일을 직접 지정")
    parser.add_argument("--split", default=None, help="validation | test | train")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--tag", default=None, help="실행 디렉터리 이름에 붙일 꼬리표")
    parser.add_argument("--prompt", default=None, help="메인 시스템 프롬프트를 파일에서 읽는다")
    parser.add_argument("--explorer-prompt", default=None, help="explorer 프롬프트 파일")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument(
        "--resume",
        nargs="?",
        const="",
        default=None,
        metavar="DIR",
        help="새 디렉터리를 만들지 않고 기존 실행에 이어 붙인다. "
             "디렉터리를 생략하면 같은 조건의 가장 최근 실행을 찾는다",
    )
    return parser.parse_args(argv)


async def main_async(argv: list[str] | None = None) -> int:
    enable_utf8()
    quiet_libraries()
    load_env()
    args = parse_args(argv)

    config = load_test(
        args.conf,
        method=args.method,
        model=args.model,
        benchmark=args.benchmark,
        path=args.path,
        limit=args.limit,
        tag=args.tag,
    )
    if args.prompt:
        config.system_prompt = resolve(args.prompt).read_text(encoding="utf-8").strip()
    if args.explorer_prompt:
        config.explorer_prompt = resolve(args.explorer_prompt).read_text(encoding="utf-8").strip()
    if args.no_cache:
        config.run.cache = False

    if args.resume is not None and not config.run.cache:
        print("--resume 과 --no-cache 는 같이 못 씁니다.", file=sys.stderr)
        return 1

    profile = profile_for(config.model)
    dataset = config.benchmark.dataset(args.split or "validation")
    benchmark = load_benchmark(config.benchmark.name, dataset)
    items = benchmark.load(limit=config.benchmark.limit)

    out = _resolve_dir(args, config, profile)
    if out is None:
        return 1

    table(
        "설정",
        {
            **config.describe(),
            "model": f"{profile.key}  ({config.agent.model_name or profile.repo})",
            "endpoint": config.agent.base_url,
            "dataset": f"{config.benchmark.name}  {dataset.name}  ({len(items)}문항)",
            "judge": config.judge.model,
            "workers": config.run.workers,
            "cache": config.run.cache,
            "run_dir": f"{out}{'   (이어 돌리기)' if args.resume is not None else ''}",
        },
    )

    write_json(
        out / "config.json",
        {
            "sources": config.sources,
            "method": config.method,
            "model": profile.repo,
            "dataset": str(dataset),
            "items": len(items),
            "agent": asdict(config.agent),
            "explorer": asdict(config.explorer) if config.uses_explorer else None,
            "judge": asdict(config.judge),
            "run": asdict(config.run),
        },
    )
    (out / "prompt.txt").write_text(config.system_prompt, encoding="utf-8")
    if config.uses_explorer:
        (out / "explorer_prompt.txt").write_text(config.explorer_prompt, encoding="utf-8")

    judge = Judge(config.judge)
    runner = Runner(
        profile=profile,
        agent_config=config.agent,
        judge=judge,
        run_dir=out,
        method=config.method,
        explorer_config=config.explorer if config.uses_explorer else None,
        explorer_prompt=config.explorer_prompt,
        use_cache=config.run.cache,
        workers=config.run.workers,
    )

    if args.resume is not None:
        todo = runner.pending(benchmark, items, config.system_prompt)
        print(f"\n전체 {len(items)}문항 · 완료 {len(items) - len(todo)} · 남은 {len(todo)}")
        if not todo:
            print("  남은 문항이 없습니다. 집계만 다시 씁니다.")
        # 아래에서 모든 문항이 다시 기록되므로 지난 줄과 겹치지 않게 비운다.
        (out / "records.jsonl").unlink(missing_ok=True)
    else:
        print(f"\n{len(items)}문항 실행 중...")

    # 진행 상황은 막대 하나로만 보여 준다. 문항마다 한 줄씩 찍으면 300문항에서
    # 화면이 흐르고 남은 시간을 읽을 수 없다. 끝난 문항의 결과는 records.jsonl 에
    # 즉시 쌓이므로, 막대에는 지금까지의 평균과 실패 수만 얹는다.
    bar = tqdm(total=len(items), unit="q", dynamic_ncols=True,
               bar_format="  {l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]{postfix}")
    tally = {"score": 0.0, "n": 0, "zero": 0, "cached": 0, "bad": 0}

    def progress(record, total: int) -> None:
        tally["n"] += 1
        tally["score"] += record.score
        tally["zero"] += record.score == 0
        tally["cached"] += bool(record.cached)
        tally["bad"] += bool(record.result.error or not record.result.answer.strip())
        post = f"f1={tally['score'] / tally['n']:.3f} 0점={tally['zero']}"
        if tally["cached"]:
            post += f" 캐시={tally['cached']}"
        if tally["bad"]:
            post += f" 실패={tally['bad']}"
        bar.set_postfix_str(post, refresh=False)
        bar.update(1)

    try:
        records = await runner.run_all(
            benchmark, items, config.system_prompt, score_field="f1", on_record=progress
        )
    finally:
        bar.close()
        await runner.aclose()

    summary = {
        "method": config.method,
        "model": profile.repo,
        "benchmark": config.benchmark.name,
        "dataset": str(dataset),
        "system_prompt_chars": len(config.system_prompt),
        "explorer_prompt_chars": len(config.explorer_prompt) if config.uses_explorer else 0,
        "judge": config.judge.model,
        "budget": {
            "searches": config.agent.max_searches,
            "search_top_k": config.agent.search_top_k,
            "expansion_nodes": config.explorer.max_expansion_nodes if config.uses_explorer else 0,
            "max_depth": config.explorer.max_depth if config.uses_explorer else 0,
            "context_limit": config.agent.context_limit,
        },
        "cache": runner.cache_stats(),
        **summarize(records),
    }
    write_json(out / "summary.json", summary)
    table("결과", {k: v for k, v in summary.items() if not isinstance(v, dict)})
    print(f"\n저장됨: {out}")
    return 0


def _resolve_dir(args, config, profile) -> Path | None:
    stage, tag = "test", config.run.tag
    if args.resume is None:
        return run_dir(
            stage, config.method, profile.repo, config.benchmark.name, tag, config.run.output_dir
        )
    if args.resume:
        out = resolve(args.resume)
        if not out.is_dir():
            print(f"이어 돌릴 디렉터리가 없습니다: {out}", file=sys.stderr)
            return None
        return out
    found = find_run(
        stage, config.method, profile.repo, config.benchmark.name, tag, config.run.output_dir
    )
    if found is None:
        print(
            f"이어 돌릴 실행을 못 찾았습니다 "
            f"({config.method} / {profile.repo} / {config.benchmark.name} / tag={tag or '없음'}). "
            f"--resume <디렉터리> 로 직접 지정하세요.",
            file=sys.stderr,
        )
    return found


def main(argv: list[str] | None = None) -> int:
    return asyncio.run(main_async(argv))


if __name__ == "__main__":
    raise SystemExit(main())
