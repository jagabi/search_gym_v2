"""배선 점검 — 설정·데이터·도구·판정이 실제로 붙는지 확인한다.

    python scripts/smoke.py            # 도구와 판정까지 실제로 한 번씩 호출
    python scripts/smoke.py --offline  # 네트워크 없이 설정·데이터만

학생 모델(vLLM)은 확인하지 않는다. 서버가 떠 있어야 하므로 그건 eval.py --limit 1로
따로 본다.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.benchmarks import BENCHMARKS, load_benchmark  # noqa: E402
from searchgym.config import load_eval, load_train  # noqa: E402
from searchgym.judge import Judge  # noqa: E402
from searchgym.paths import load_env  # noqa: E402
from searchgym.report import enable_utf8, table  # noqa: E402
from searchgym.serving import PROFILES  # noqa: E402


async def check_tools() -> dict[str, str]:
    from searchgym.tools import WebTools

    async with WebTools() as tools:
        names = [spec.name for spec in tools.specs]
        search = await tools.call("web_search", {"query": "openai gpt-oss"})
        fetch = await tools.call("web_fetch", {"url": "https://example.com"})
    return {
        "tools": ", ".join(names),
        "web_search": f"{len(search.text):,}자, error={search.is_error}, {search.duration_ms:.0f}ms",
        "web_fetch": f"{len(fetch.text):,}자, error={fetch.is_error}, {fetch.duration_ms:.0f}ms",
    }


def check_judge() -> dict[str, str]:
    """정답/오답 한 건씩 실제로 채점해 본다."""
    out = {}
    for name, correct_response, wrong_response in (
        ("deepsearchqa", None, None),
        ("evobrowsecomp", None, None),
    ):
        benchmark = load_benchmark(name, f"data/{name}/train.json")
        item = benchmark.load(limit=1)[0]
        judge = Judge()
        good = judge.grade(benchmark, item, f"The answer is {item.answer}.")
        bad = judge.grade(benchmark, item, "I could not find this information.")
        out[f"{name} (정답)"] = f"{good.category} f1={good.metrics()['f1']:.2f} err={good.error}"
        out[f"{name} (오답)"] = f"{bad.category} f1={bad.metrics()['f1']:.2f} err={bad.error}"
    return out


def main() -> int:
    enable_utf8()
    load_env()
    parser = argparse.ArgumentParser(description="배선 점검")
    parser.add_argument("--offline", action="store_true", help="네트워크 호출을 건너뛴다")
    args = parser.parse_args()

    rows: dict[str, object] = {}

    train = load_train("configs/train.yaml")
    evaluation = load_eval("configs/eval.yaml")
    rows["train.yaml"] = f"model={train.model} benchmark={train.data.benchmark}"
    rows["eval.yaml"] = f"model={evaluation.model} datasets={len(evaluation.datasets)}"
    rows["reflection_prompt"] = f"{len(train.teacher.reflection_prompt.split())} words"
    rows["budget"] = f"search {train.agent.max_searches} / fetch {train.agent.max_fetches}"

    for key, profile in PROFILES.items():
        where = "local" if profile.is_local else "hub"
        rows[f"model:{key}"] = f"{profile.repo}  [{where}]  parser={profile.tool_call_parser}"

    for name in BENCHMARKS:
        counts = []
        for split in ("train", "validation", "test"):
            path = Path(f"data/{name}/{split}.json")
            counts.append(f"{split}={len(load_benchmark(name, path).load()) if path.exists() else '-'}")
        rows[f"data:{name}"] = "  ".join(counts)

    table("설정 · 데이터", rows)

    if args.offline:
        print("\n(--offline: 도구·판정 호출은 건너뜀)")
        return 0

    table("도구 (Serper + Jina)", asyncio.run(check_tools()))
    table("판정 (Gemini)", check_judge())
    print("\n다음: vLLM을 띄우고  python eval.py --limit 1 --benchmark evobrowsecomp")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
