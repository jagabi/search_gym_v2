"""모델별 vllm serve 명령을 출력한다.

    python scripts/serve.py                    # 세 모델 전부 + 주의사항
    python scripts/serve.py gemma              # 하나만
    python scripts/serve.py gemma --sh         # 셸에 넘길 한 줄 (serve.sh가 쓴다)
    python scripts/serve.py gemma --max-num-seqs 4 --max-model-len 65536

가중치는 `models/` 아래에 받아 둔다. 있으면 로컬 경로로, 없으면 HF ID로 띄운다.
어느 쪽이든 `--served-model-name`이 repo ID로 고정되므로 클라이언트가 부르는 이름은 같다.

이 스크립트는 **서빙 환경(vllm-env)에서도 돈다** — 판정·최적화 쪽 의존성을 끌어오지
않는다. `searchgym/__init__.py`가 지연 import라 그렇다.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.report import enable_utf8  # noqa: E402
from searchgym.serving import PROFILES, profile_for  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="vllm serve 명령 출력")
    parser.add_argument("model", nargs="?", help="qwen | gemma | gpt-oss (생략하면 전부)")
    parser.add_argument("--sh", action="store_true", help="한 줄로만 출력(주석·설명 없음)")
    parser.add_argument("--max-model-len", type=int, default=None)
    parser.add_argument("--max-num-seqs", type=int, default=1)
    parser.add_argument("--gpu-util", type=float, default=0.90)
    parser.add_argument("--port", type=int, default=8000)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    kwargs = dict(
        max_model_len=args.max_model_len,
        gpu_util=args.gpu_util,
        max_num_seqs=args.max_num_seqs,
        port=args.port,
    )

    if args.sh:
        if not args.model:
            print("--sh 에는 모델을 지정해야 합니다.", file=sys.stderr)
            return 1
        print(profile_for(args.model).serve_command(**kwargs, oneline=True))
        return 0

    enable_utf8()
    targets = [profile_for(args.model)] if args.model else list(PROFILES.values())
    for profile in targets:
        where = "로컬" if profile.is_local else "미다운로드 — HF에서 스트리밍"
        print(f"\n# {profile.key}  {profile.repo}  [{where}]")
        if not profile.is_local:
            print(f"# hf download {profile.repo} --local-dir {profile.local_dir}")
        if profile.reasoning_effort:
            print(f"# 추론 강도: {profile.reasoning_effort} (시스템 프롬프트로 자동 주입)")
        print(profile.serve_command(**kwargs))
        if profile.notes:
            print("\n" + "\n".join(f"# {line}" for line in profile.notes.splitlines()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
