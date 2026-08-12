#!/usr/bin/env bash
# RunPod pod을 Stop -> Start 한 뒤 복구한다.
#
#   bash scripts/runpod_setup.sh
#
# /workspace(볼륨)에 있는 것은 Stop을 견딘다 — 저장소, models/, vllm-env, runs/.
# 컨테이너 디스크에 있던 시스템 pip 패키지만 날아가므로 그것만 다시 깐다.
set -euo pipefail

cd "$(dirname "$0")/.."
echo "== 작업 디렉터리: $(pwd)"

echo "== 클라이언트 의존성 (시스템 파이썬)"
pip install -q -r requirements.txt --break-system-packages
# fastmcp는 server extra가 있어야 FastMCP가 딸려 온다. Debian이 깐 cryptography는 건드리지 않는다.
pip install -q "fastmcp-slim[server]" --break-system-packages --ignore-installed cryptography

echo "== 확인"
python - <<'PY'
import importlib
for mod in ("dspy", "openai", "google.genai", "mcp", "fastmcp", "yaml"):
    try:
        importlib.import_module(mod)
        print(f"   OK    {mod}")
    except Exception as exc:
        print(f"   FAIL  {mod}: {exc}")
PY

if [ -d /workspace/vllm-env ]; then
  echo "== vLLM venv 확인 (transformers는 5.14.x여야 gemma-4가 뜬다)"
  /workspace/vllm-env/bin/python - <<'PY'
import transformers, vllm
print(f"   vllm {vllm.__version__} / transformers {transformers.__version__}")
if not transformers.__version__.startswith("5.14"):
    print("   !! gemma-4를 쓸 거면: uv pip install 'transformers==5.14.*'")
PY
else
  echo "== /workspace/vllm-env 없음 — gemma-4용 venv를 다시 만들어야 한다"
fi

cat <<'EOF'

== 다음
  1) 서버 (별도 터미널)
       source /workspace/vllm-env/bin/activate
       python scripts/serve.py gemma        # 명령 확인 후 --max-num-seqs 1 붙여 실행
  2) 배선 점검
       python scripts/smoke.py
EOF
