"""모델별 vllm serve 명령과 주의사항을 출력한다.

    python scripts/serve.py                    # 세 모델 전부
    python scripts/serve.py qwen               # 하나만
    python scripts/serve.py gemma --gpu-util 0.92

가중치는 `models/` 아래에 clone해 둔다. 있으면 로컬 경로로, 없으면 HF ID로 띄운다.
어느 쪽이든 `--served-model-name`이 repo ID로 고정되므로 클라이언트가 부르는
모델 이름은 같다.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.report import enable_utf8  # noqa: E402
from searchgym.serving import PROFILES, profile_for  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    enable_utf8()
    parser = argparse.ArgumentParser(description="vllm serve 명령 출력")
    parser.add_argument("model", nargs="?", help="qwen | gemma | gpt-oss (생략하면 전부)")
    parser.add_argument("--max-model-len", type=int, default=None)
    parser.add_argument("--gpu-util", type=float, default=0.90)
    args = parser.parse_args(argv)

    targets = [profile_for(args.model)] if args.model else list(PROFILES.values())
    for profile in targets:
        where = "로컬" if profile.is_local else "미다운로드 — HF에서 스트리밍"
        print(f"\n# {profile.key}  {profile.repo}  [{where}]")
        if not profile.is_local:
            print(f"# git lfs install && {profile.clone_command()}")
        if profile.reasoning_effort:
            print(f"# 추론 강도: {profile.reasoning_effort} (시스템 프롬프트로 자동 주입)")
        print(profile.serve_command(args.max_model_len, args.gpu_util))
        if profile.notes:
            print("\n" + "\n".join(f"# {line}" for line in profile.notes.splitlines()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
