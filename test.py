"""한 방법을 한 벤치마크에서 평가한다.

    python test.py                                   # conf.yaml 그대로
    python test.py --method search-o1 --tag s1
    python test.py --limit 5                         # 배선 확인
    python test.py --split test                      # 마지막에만
    python test.py --tag baseline --resume           # 멈춘 실행 이어서
    python test.py --tag baseline --resume --retry-errors  # 실패만 교체, 전체 재집계

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
import json
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
    parser.add_argument("--retry-errors", action="store_true",
                        help="--resume 실행의 빈 답변·실행 오류·채점 오류만 재시도 (정상 0점은 유지)")
    parser.add_argument("--dry-run", action="store_true",
                        help="--retry-errors 대상만 확인. 실행/채점/파일 수정 없음")
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
    if args.retry_errors and args.resume is None:
        print("--retry-errors는 --resume과 함께 사용하세요.", file=sys.stderr)
        return 1
    if args.dry_run and not args.retry_errors:
        print("--dry-run은 --retry-errors와 함께 사용하세요.", file=sys.stderr)
        return 1

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

    retry_plan = None
    if args.retry_errors:
        from searchgym.retry import plan_retry
        try:
            retry_plan = plan_retry(out, items, config, profile)
        except (OSError, ValueError, KeyError) as exc:
            print(f"실패 재시도 준비 오류: {exc}", file=sys.stderr)
            return 1
        agent_n = sum(kind == "agent" for kind in retry_plan.targets.values())
        judge_n = sum(kind == "judge" for kind in retry_plan.targets.values())
        print(f"\n전체 {len(items)} · 유지 {len(items) - len(retry_plan.targets)} · "
              f"답변 재실행 {agent_n} · 채점만 재시도 {judge_n}")
        print("  대상: " + (", ".join(f"q{i:05d}" for i in sorted(retry_plan.targets)) or "없음"))
        if args.dry_run or not retry_plan.targets:
            return 0

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

    if retry_plan is None:
        _write_run_config(out, config, profile, dataset, items)

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

    if retry_plan is not None:
        print("  실패 기록을 retry_history에 백업하고, 완료되는 문항부터 전체 결과를 갱신합니다.")
    elif args.resume is not None:
        todo = runner.pending(benchmark, items, config.system_prompt)
        print(f"\n전체 {len(items)}문항 · 완료 {len(items) - len(todo)} · 남은 {len(todo)}")
        if not todo:
            print("  남은 문항이 없습니다. 집계만 다시 씁니다.")
        (out / "records.jsonl").unlink(missing_ok=True)
    else:
        print(f"\n{len(items)}문항 실행 중...")

    total = len(retry_plan.targets) if retry_plan is not None else len(items)
    bar = tqdm(total=total, unit="q", dynamic_ncols=True,
               bar_format="  {l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]{postfix}")
    tally = {"score": 0.0, "n": 0, "zero": 0, "cached": 0, "bad": 0}

    def progress(record, total: int) -> None:
        tally["n"] += 1
        tally["score"] += record.score
        tally["zero"] += record.score == 0
        tally["cached"] += bool(record.cached)
        tally["bad"] += bool(record.result.error or not record.result.answer.strip())
        label = "재시도 f1" if retry_plan is not None else "f1"
        post = f"{label}={tally['score'] / tally['n']:.3f} 0점={tally['zero']}"
        if tally["cached"]:
            post += f" 캐시={tally['cached']}"
        if tally["bad"]:
            post += f" 실패={tally['bad']}"
        bar.set_postfix_str(post, refresh=False)
        bar.update(1)

    try:
        if retry_plan is not None:
            from searchgym.retry import retry_failed
            records = await retry_failed(runner, retry_plan, benchmark, config.system_prompt, progress)
        else:
            records = await runner.run_all(
                benchmark, items, config.system_prompt, score_field="f1", on_record=progress
            )
    finally:
        bar.close()
        await runner.aclose()

    if retry_plan is not None:
        summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    else:
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


def _write_run_config(out, config, profile, dataset, items):
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
    if config.method == "depthsearch" and config.agent.depthsearch_control:
        from searchgym.agent import FINAL_SYSTEM
        from searchgym.research_state import CONTROL_PROMPT, SELECT_PROMPT, SELECT_FETCH_TOOL
        (out / "final_prompt.txt").write_text(FINAL_SYSTEM, encoding="utf-8")
        (out / "controller_prompt.txt").write_text(CONTROL_PROMPT, encoding="utf-8")
        (out / "selector_prompt.txt").write_text(SELECT_PROMPT, encoding="utf-8")
        (out / "selector_tool.json").write_text(json.dumps(SELECT_FETCH_TOOL, indent=2), encoding="utf-8")

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
