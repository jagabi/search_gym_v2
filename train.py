"""GEPA 로 시스템 프롬프트를 최적화한다.

    python train.py                          # conf.yaml 의 method/model + configs/gepa.yaml
    python train.py --method depthsearch --tag g1

최적화 대상은 두 컴포넌트다.

    agent      메인 추론 모델의 시스템 프롬프트  (검색 정책)
    explorer   explorer 의 시스템 프롬프트       (추출 + 확장 정책)

explorer 가 확장 결정을 하지 않으면(= search-o1, ragent) 자동으로 agent 하나만
최적화한다.

산출물:
    runs/train/{날짜}_{방법}_{모델}_{벤치}_{태그}/
      prompt.txt           최적화된 메인 시스템 프롬프트   <- 결과물
      explorer_prompt.txt  최적화된 explorer 프롬프트      <- 결과물
      initial_*.txt        출발점
      candidates.json      GEPA 가 만든 후보 전부
      summary.json         점수 · val 곡선 · 탐색 행동 · 캐시 통계
      records.jsonl        문항별 한 줄 요약
      optimize/q00022/     문항별 트레이스
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from typing import Any

import dspy

from searchgym.benchmarks import load_benchmark
from searchgym.config import load_train
from searchgym.gepa import PolicyProposer, SearchMetric, SearchProgram
from searchgym.judge import Judge
from searchgym.paths import load_env, run_dir
from searchgym.report import enable_utf8, quiet_libraries, summarize, table, write_json
from searchgym.runner import Runner
from searchgym.serving import profile_for


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GEPA 프롬프트 최적화")
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--gepa", default="configs/gepa.yaml")
    parser.add_argument("--method", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--tag", default=None, help="실행 디렉터리 이름에 붙일 꼬리표")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--no-cache", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    quiet_libraries()
    load_env()
    args = parse_args(argv)

    config = load_train(
        args.conf, args.gepa, method=args.method, model=args.model, tag=args.tag
    )
    base = config.base
    if args.seed is not None:
        base.run.seed = args.seed
    if not base.run.tag:
        base.run.tag = f"seed{base.run.seed}"
    if args.no_cache:
        base.run.cache = False

    profile = profile_for(base.model)
    benchmark = load_benchmark(config.data.benchmark, config.data.trainset)
    trainset = benchmark.load()
    valset = load_benchmark(config.data.benchmark, config.data.valset).load()
    components = config.component_names

    out = run_dir(
        "train", base.method, profile.repo, config.data.benchmark,
        base.run.tag, base.run.output_dir,
    )
    table(
        "설정",
        {
            **base.describe(),
            "model": f"{profile.key}  ({base.agent.model_name or profile.repo})",
            "endpoint": base.agent.base_url,
            "benchmark": config.data.benchmark,
            "train / val": f"{len(trainset)} / {len(valset)}",
            "components": ", ".join(components),
            "teacher": config.teacher.model,
            "judge": base.judge.model,
            "gepa": f"auto={config.gepa.auto} extra={config.gepa.extra} "
                    f"minibatch={config.gepa.reflection_minibatch_size} merge={config.gepa.merge}",
            "seed": base.run.seed,
            "run_dir": out,
        },
    )

    if not base.system_prompt.strip():
        print("system_prompt 가 비어 있습니다.", file=sys.stderr)
        return 1

    (out / "initial_prompt.txt").write_text(base.system_prompt, encoding="utf-8")
    if "explorer" in components:
        (out / "initial_explorer_prompt.txt").write_text(base.explorer_prompt, encoding="utf-8")
    write_json(
        out / "config.json",
        {
            "sources": base.sources,
            "method": base.method,
            "model": profile.repo,
            "components": components,
            "agent": asdict(base.agent),
            "explorer": asdict(base.explorer) if base.uses_explorer else None,
            "teacher": asdict(config.teacher),
            "judge": asdict(base.judge),
            "gepa": asdict(config.gepa),
            "data": asdict(config.data),
            "seed": base.run.seed,
        },
    )

    # --- 구성 ---------------------------------------------------------------

    judge = Judge(base.judge)
    runner = Runner(
        profile=profile,
        agent_config=base.agent,
        judge=judge,
        run_dir=out,
        method=base.method,
        explorer_config=base.explorer if base.uses_explorer else None,
        explorer_prompt=base.explorer_prompt,
        use_cache=base.run.cache,
        workers=base.run.workers,
    )
    items = {item.index: item for item in trainset + valset}
    seed_prompts = {"agent": base.system_prompt, "explorer": base.explorer_prompt}
    metric = SearchMetric(runner, benchmark, items, config.feedback, seed_prompts)

    to_example = lambda item: dspy.Example(  # noqa: E731
        index=item.index, question=item.question
    ).with_inputs("index", "question")

    teacher = dspy.LM(
        model=config.teacher.model,
        temperature=1.0,
        max_tokens=config.teacher.max_tokens,
        **config.teacher.extra,
    )

    templates = {
        name: config.components[name].reflection_prompt
        for name in components
        if name in config.components
    }
    optimizer_kwargs: dict[str, Any] = {
        "metric": metric,
        "reflection_lm": teacher,
        "auto": config.gepa.auto,
        "reflection_minibatch_size": config.gepa.reflection_minibatch_size,
        "num_threads": config.gepa.num_threads,
        "track_stats": config.gepa.track_stats,
        "failure_score": config.gepa.failure_score,
        "seed": base.run.seed,
        "use_merge": config.gepa.merge,
        **config.gepa.extra,
    }
    if any(t.strip() for t in templates.values()):
        optimizer_kwargs["instruction_proposer"] = PolicyProposer(
            templates, config.teacher.prompt_token_budget
        )

    program = SearchProgram(
        base.system_prompt,
        base.explorer_prompt if "explorer" in components else "",
    )
    optimizer = _build_optimizer(optimizer_kwargs)

    # --- 최적화 -------------------------------------------------------------

    print("\n최적화 시작. Ctrl+C 로 끊어도 지금까지의 기록은 남습니다.\n")
    metric.stage("optimize")
    try:
        optimized = optimizer.compile(
            program,
            trainset=[to_example(i) for i in trainset],
            valset=[to_example(i) for i in valset],
        )
    except KeyboardInterrupt:
        print("\n중단됨. 지금까지의 기록만 저장합니다.", file=sys.stderr)
        optimized = program

    (out / "prompt.txt").write_text(optimized.agent_prompt, encoding="utf-8")
    if "explorer" in components:
        (out / "explorer_prompt.txt").write_text(optimized.explorer_prompt, encoding="utf-8")

    detailed = getattr(optimized, "detailed_results", None)
    candidates = [
        {"agent": getattr(c, "agent_prompt", ""), "explorer": getattr(c, "explorer_prompt", "")}
        for c in getattr(detailed, "candidates", [])
    ] if detailed else []
    if candidates:
        write_json(out / "candidates.json", candidates)

    summary = {
        "method": base.method,
        "model": profile.repo,
        "benchmark": config.data.benchmark,
        "components": components,
        "teacher": config.teacher.model,
        "judge": base.judge.model,
        "seed": base.run.seed,
        "initial_prompt_chars": len(base.system_prompt),
        "final_prompt_chars": len(optimized.agent_prompt),
        "initial_explorer_chars": len(base.explorer_prompt) if "explorer" in components else 0,
        "final_explorer_chars": len(optimized.explorer_prompt) if "explorer" in components else 0,
        "candidates": len(candidates) or 1,
        "metric_calls": len(metric.records),
        "cache": runner.cache_stats(),
        **summarize(metric.records),
    }
    if detailed is not None:
        summary["val_scores"] = list(getattr(detailed, "val_aggregate_scores", []) or [])
        summary["best_index"] = getattr(detailed, "best_idx", None)
    write_json(out / "summary.json", summary)

    table("결과", {k: v for k, v in summary.items() if not isinstance(v, (dict, list))})
    print(f"\n프롬프트: {out / 'prompt.txt'}")
    if "explorer" in components:
        print(f"explorer: {out / 'explorer_prompt.txt'}")
    print(f"저장됨:   {out}")
    return 0


def _build_optimizer(kwargs: dict[str, Any]):
    """dspy 버전에 따라 없는 키가 있을 수 있다. 하나씩 떼어 내며 만든다."""
    attempt = dict(kwargs)
    for _ in range(len(kwargs)):
        try:
            return dspy.GEPA(**attempt)
        except TypeError as exc:
            message = str(exc)
            dropped = next(
                (k for k in list(attempt) if f"'{k}'" in message and k != "metric"), None
            )
            if dropped is None:
                raise
            print(f"[warn] dspy.GEPA 가 '{dropped}' 를 받지 않습니다. 빼고 진행합니다.", file=sys.stderr)
            attempt.pop(dropped)
    return dspy.GEPA(**attempt)


if __name__ == "__main__":
    raise SystemExit(main())
