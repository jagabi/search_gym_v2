"""경로 규칙과 실행 디렉터리 이름.

실행 디렉터리 하나가 실험 하나다. 이름만 보고 무엇을 돌린 것인지 알 수 있어야
하므로 `{단계}/{날짜}_{모델}_{벤치}_{태그}` 형태로 짓는다.

    runs/train/20260811-2104_qwen3.5-9b_deepsearchqa_seed0/
    runs/eval/20260811-2130_gpt-oss-20b_evobrowsecomp_final/
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

__all__ = ["PROJECT_ROOT", "find_run", "load_env", "resolve", "run_dir", "slug"]

PROJECT_ROOT = Path(__file__).resolve().parents[1]

_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")
_loaded = False


def load_env() -> None:
    """`.env`를 한 번만 읽는다. 여러 번 불러도 안전하다."""
    global _loaded
    if not _loaded:
        load_dotenv(PROJECT_ROOT / ".env")
        _loaded = True


def resolve(path: str | Path) -> Path:
    """상대 경로는 저장소 루트 기준으로 푼다.

    어느 디렉터리에서 실행하든 설정에 적힌 `data/deepsearchqa/train.json`이
    같은 파일을 가리켜야 한다.
    """
    candidate = Path(path).expanduser()
    return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate


def slug(value: str) -> str:
    """모델 ID 등을 디렉터리 이름에 쓸 수 있게 다듬는다.

    `Qwen/Qwen3.5-9B` -> `qwen3.5-9b`
    """
    tail = value.rsplit("/", 1)[-1]
    return _UNSAFE.sub("-", tail).strip("-").lower() or "unnamed"


def run_dir(stage: str, model: str, benchmark: str, tag: str = "", root: str | Path = "runs") -> Path:
    """실행 디렉터리를 만들고 돌려준다. 이미 있으면 뒤에 번호를 붙인다."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    parts = [stamp, slug(model), slug(benchmark)]
    if tag:
        parts.append(slug(tag))
    base = resolve(root) / stage
    path = base / "_".join(parts)

    counter = 2
    while path.exists():
        path = base / ("_".join(parts) + f"-{counter}")
        counter += 1
    path.mkdir(parents=True)
    return path


def find_run(
    stage: str, model: str, benchmark: str, tag: str = "", root: str | Path = "runs"
) -> Path | None:
    """같은 조건으로 돌린 **가장 최근** 실행 디렉터리. 이어서 돌릴 때 쓴다.

    이름이 `{날짜}_{나머지}`라 앞의 타임스탬프만 떼면 조건이 남는다. 사전순 최대가
    곧 최신이다(날짜 형식이 고정 폭이라 그렇다).
    """
    parts = [slug(model), slug(benchmark)]
    if tag:
        parts.append(slug(tag))
    want = "_".join(parts)

    base = resolve(root) / stage
    if not base.is_dir():
        return None
    matches = [
        path
        for path in base.iterdir()
        if path.is_dir()
        # 이름이 겹쳐 뒤에 -2, -3이 붙은 것도 같은 조건이다.
        and ((rest := path.name.partition("_")[2]) == want or rest.startswith(f"{want}-"))
    ]
    return max(matches, key=lambda path: path.name) if matches else None


def env(*names: str) -> str | None:
    load_env()
    for name in names:
        if value := os.getenv(name):
            return value
    return None


def require_env(*names: str) -> str:
    if value := env(*names):
        return value
    raise RuntimeError(f"{' 또는 '.join(names)}가 설정되지 않았습니다. .env를 확인하세요.")
