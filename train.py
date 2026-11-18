"""GEPA 로 시스템 프롬프트를 최적화한다.

    python train.py                          # conf.yaml 의 method/model + configs/gepa.yaml
    python train.py --method depthsearch --tag g1
    python train.py --gepa configs/gepa-decision.yaml --method search-o1-decision --model gpt-oss         --decision d3-mini --bundle-tokens 1024 --top-n 1 --tag gepa_b1024_t1

최적화 대상은 두 컴포넌트다.

    agent      메인 추론 모델의 시스템 프롬프트  (검색 정책)
    explorer   explorer 의 시스템 프롬프트       (추출 + 확장 정책)

explorer 가 확장 결정을 하지 않으면(= search-o1, ragent) 자동으로 agent 하나만
최적화한다. search-o1-decision 은 agent + decision(decision 모델의 evidence 지시문)이다.

산출물:
    runs/train/{날짜}_{방법}_{모델}_{벤치}_{태그}/
      prompt.txt           최적화된 메인 시스템 프롬프트   <- 결과물
      explorer_prompt.txt  최적화된 explorer 프롬프트      <- 결과물
      decision_prompt.txt  최적화된 decision 지시문        <- 결과물 (test.py --decision-prompt)
      initial_*.txt        출발점
      candidates.json      GEPA 가 만든 후보 전부 (val 점수 · 부모)
      teacher/             교사 호출마다 프롬프트(side_info 포함) · 응답 · 사용량
      gepa/                gepa 상태 파일
      summary.json         점수 · val 곡선 · 탐색 행동 · 캐시 통계
      records.jsonl        문항별 한 줄 요약
      optimize/q00022/     문항별 트레이스
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import asdict

from searchgym.agent import RAW_METHODS
from searchgym.benchmarks import load_benchmark
from searchgym.config import load_train
from searchgym.gepa import SearchAdapter, Teacher
from searchgym.judge import Judge
from searchgym.paths import load_env, run_dir
from searchgym.rawtree import EVIDENCE_INSTRUCTIONS
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
    parser.add_argument("--decision", "--decision-provider", dest="decision_provider", default=None,
                        help="pplx | d3-mini | d3-flash (search-o1-decision 필수)")
    parser.add_argument("--bundle-tokens", type=int, default=None, help="decision bundle 크기")
    parser.add_argument("--top-n", type=int, default=None, help="검색당 넘기는 bundle 수")
    parser.add_argument("--no-cache", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    quiet_libraries()
    load_env()
    args = parse_args(argv)

    config = load_train(
        args.conf, args.gepa, method=args.method, model=args.model, tag=args.tag,
        decision_provider=args.decision_provider, raw_top_n=args.top_n,
        raw_bundle_tokens=args.bundle_tokens,
    )
    base = config.base
    if args.seed is not None:
        base.run.seed = args.seed
    if not base.run.tag:
        base.run.tag = f"seed{base.run.seed}"
    if args.no_cache:
        base.run.cache = False

    if base.method in RAW_METHODS and args.decision_provider is None:
        print(f"{base.method} 는 --decision pplx|d3-mini|d3-flash 가 필요합니다.", file=sys.stderr)
        return 1
    decision_seed = base.agent.jev_evidence_instructions or EVIDENCE_INSTRUCTIONS
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
            "decision": (f"{base.agent.decision_provider} bundle={base.agent.jev_bundle_tokens} "
                         f"top_n={base.agent.jev_top_n}") if "decision" in components else "-",
            "teacher": f"{config.teacher.model} effort={config.teacher.effort}",
            "judge": base.judge.model,
            "gepa": f"max_metric_calls={config.gepa.max_metric_calls} "
                    f"minibatch={config.gepa.reflection_minibatch_size} merge={config.gepa.merge} "
                    f"select={config.gepa.candidate_selection_strategy} extra={config.gepa.extra}",
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
    if "decision" in components:
        (out / "initial_decision_prompt.txt").write_text(decision_seed, encoding="utf-8")
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

    import gepa

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
    seed = {"agent": base.system_prompt}
    if "explorer" in components:
        seed["explorer"] = base.explorer_prompt
    if "decision" in components:
        seed["decision"] = decision_seed

    templates = {name: config.components[name].reflection_prompt for name in components}
    teacher = Teacher(config.teacher, out / "teacher")
    adapter = SearchAdapter(
        runner, benchmark, {item.index: item for item in trainset + valset}, config.feedback,
        templates, teacher, native_side_info=base.method in RAW_METHODS,
    )

    # --- 최적화 -------------------------------------------------------------

    print("\n최적화 시작. Ctrl+C 로 끊어도 지금까지의 기록은 남습니다.\n")
    result = None
    try:
        result = gepa.optimize(
            seed_candidate=seed,
            trainset=trainset,
            valset=valset,
            adapter=adapter,
            candidate_selection_strategy=config.gepa.candidate_selection_strategy,
            reflection_minibatch_size=config.gepa.reflection_minibatch_size,
            module_selector=config.gepa.module_selector,
            use_merge=config.gepa.merge,
            max_metric_calls=config.gepa.max_metric_calls,
            run_dir=str(out / "gepa"),
            seed=base.run.seed,
            display_progress_bar=True,
            **config.gepa.extra,
        )
    except KeyboardInterrupt:
        print("\n중단됨. 지금까지의 기록만 저장합니다.", file=sys.stderr)

    best = dict(result.best_candidate) if result is not None else dict(seed)
    (out / "prompt.txt").write_text(best["agent"], encoding="utf-8")
    if "explorer" in components:
        (out / "explorer_prompt.txt").write_text(best["explorer"], encoding="utf-8")
    if "decision" in components:
        (out / "decision_prompt.txt").write_text(best["decision"], encoding="utf-8")

    candidates = []
    if result is not None:
        candidates = [
            {"index": i, "val_score": score, "parents": list(result.parents[i] or []), **dict(c)}
            for i, (c, score) in enumerate(zip(result.candidates, result.val_aggregate_scores))
        ]
        write_json(out / "candidates.json", candidates)

    summary = {
        "method": base.method,
        "model": profile.repo,
        "benchmark": config.data.benchmark,
        "components": components,
        "teacher": f"{teacher.model} effort={config.teacher.effort}",
        "teacher_calls": teacher.calls,
        "judge": base.judge.model,
        "seed": base.run.seed,
        **{f"initial_{k}_chars": len(v) for k, v in seed.items()},
        **{f"final_{k}_chars": len(v) for k, v in best.items()},
        "candidates": len(candidates) or 1,
        "best_index": result.best_idx if result is not None else 0,
        "val_scores": list(result.val_aggregate_scores) if result is not None else [],
        "metric_calls": len(adapter.records),
        "cache": runner.cache_stats(),
        **summarize(adapter.records),
    }
    write_json(out / "summary.json", summary)

    table("결과", {k: v for k, v in summary.items() if not isinstance(v, (dict, list))})
    print(f"\n프롬프트: {out / 'prompt.txt'}")
    if "explorer" in components:
        print(f"explorer: {out / 'explorer_prompt.txt'}")
    if "decision" in components:
        print(f"decision: {out / 'decision_prompt.txt'}")
    print(f"저장됨:   {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
