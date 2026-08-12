#!/usr/bin/env bash
# RunPod pod을 Stop -> Start 한 뒤 복구한다.
#
#   bash scripts/runpod_setup.sh
#
# /workspace(볼륨)에 있는 것은 Stop을 견딘다 — 저장소, models/, vllm-env, runs/.
# 컨테이너 디스크에 있던 시스템 pip 패키지만 날아가므로 그것만 다시 깐다.
#
# 서버(vLLM)와 클라이언트(eval.py)는 **다른 환경**을 쓴다. 이 스크립트는 클라이언트
# 쪽만 복구하며, vllm-env가 활성화돼 있어도 시스템 파이썬에 설치한다.
set -euo pipefail

cd "$(dirname "$0")/.."
echo "== 작업 디렉터리: $(pwd)"

# venv가 켜져 있어도 클라이언트는 시스템 파이썬에 깐다.
PY=/usr/bin/python3
[ -x "$PY" ] || PY=$(command -v python3)
if [ -n "${VIRTUAL_ENV:-}" ]; then
  echo "== venv(${VIRTUAL_ENV})가 활성화돼 있지만 클라이언트는 $PY 에 설치한다"
fi

# Debian이 깐 cryptography는 RECORD가 없어 pip이 지우지 못한다. 건드리지 않게 한다.
PIP_FLAGS=(--break-system-packages --ignore-installed cryptography)

echo "== 클라이언트 의존성"
"$PY" -m pip install -q -r requirements.txt "${PIP_FLAGS[@]}"

echo "== 확인"
"$PY" - <<'PY'
import importlib
for mod in ("dspy", "openai", "google.genai", "mcp", "fastmcp", "yaml", "httpx"):
    try:
        importlib.import_module(mod)
        print(f"   OK    {mod}")
    except Exception as exc:
        print(f"   FAIL  {mod}: {exc}")
PY

if [ -d /workspace/vllm-env ]; then
  echo "== vLLM venv (transformers는 5.14.x여야 gemma-4가 뜬다)"
  /workspace/vllm-env/bin/python - <<'PY'
import transformers, vllm
ok = transformers.__version__.startswith("5.14")
print(f"   vllm {vllm.__version__} / transformers {transformers.__version__}"
      f"{'' if ok else '   <-- gemma-4가 안 뜬다'}")
if not ok:
    print("   고치기: source /workspace/vllm-env/bin/activate && uv pip install 'transformers==5.14.*'")
PY
else
  echo "== /workspace/vllm-env 없음 — gemma-4용 venv를 다시 만들어야 한다"
fi

cat <<'EOF'

== 다음
  1) 서버 (별도 터미널)
       source /workspace/vllm-env/bin/activate
       cd /workspace/search_gym_v2
       python scripts/serve.py gemma      # 명령 확인, --max-num-seqs 1 붙여 실행
  2) 배선 점검 (이 터미널, venv 아님)
       python scripts/smoke.py
       python eval.py --limit 1 --benchmark deepsearchqa --tag wiring --no-cache
EOF
