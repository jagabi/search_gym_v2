#!/usr/bin/env bash
# vLLM 서버를 tmux 세션 'vllm'에 띄운다.
#
#   ./serve.sh                      # configs/eval.yaml의 모델
#   ./serve.sh qwen                 # 다른 모델
#   ./serve.sh gemma -n 4           # --max-num-seqs 4 (배칭)
#   ./serve.sh gemma -l 65536       # --max-model-len
#
#   tmux attach -t vllm             # 로그 보기 (빠져나오기: Ctrl+B 그다음 D)
#   ./serve.sh --stop               # 서버 내리기
#
# 서버는 vllm-env(전용 venv)에서 돈다. 클라이언트(run.sh)는 시스템 파이썬을 쓴다 —
# vLLM이 핀한 torch와 저장소 의존성이 서로 안 싸우게 분리해 둔 것이다.
set -euo pipefail

cd "$(dirname "$0")"
SESSION=${SESSION:-vllm}
VENV=${VLLM_VENV:-/workspace/vllm-env}
SEQS=1
LEN=""
MODEL=""

while [ $# -gt 0 ]; do
  case "$1" in
    --stop)  tmux kill-session -t "$SESSION" 2>/dev/null && echo "세션 '$SESSION' 종료" || echo "세션 '$SESSION' 없음"; exit 0 ;;
    -n)      SEQS=$2; shift 2 ;;
    -l)      LEN="--max-model-len $2"; shift 2 ;;
    -*)      echo "알 수 없는 옵션: $1" >&2; exit 1 ;;
    *)       MODEL=$1; shift ;;
  esac
done

command -v tmux >/dev/null || { echo "tmux가 없습니다:  apt-get update && apt-get install -y tmux" >&2; exit 1; }
[ -x "$VENV/bin/python" ] || { echo "vLLM venv가 없습니다: $VENV" >&2; exit 1; }

# 모델을 안 주면 설정에서 읽는다(서버와 클라이언트가 어긋나는 것을 막는다).
if [ -z "$MODEL" ]; then
  MODEL=$(/usr/bin/python3 - <<'PY' 2>/dev/null || echo gemma
import re, pathlib
m = re.search(r"^model:\s*(\S+)", pathlib.Path("configs/eval.yaml").read_text(encoding="utf-8"), re.M)
print(m.group(1) if m else "gemma")
PY
)
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "세션 '$SESSION'이 이미 돌고 있습니다. 내리려면:  ./serve.sh --stop"
  exit 1
fi

CMD=$("$VENV/bin/python" scripts/serve.py "$MODEL" --sh --max-num-seqs "$SEQS" $LEN)
echo "모델   : $MODEL   (max-num-seqs $SEQS)"
echo "명령   : $CMD"

tmux new-session -d -s "$SESSION" \
  "source '$VENV/bin/activate'; cd '$PWD'; $CMD; echo; echo '[서버 종료됨 — 창을 닫으려면 exit]'; exec bash"

cat <<EOF

세션 '$SESSION' 시작. 기동에 4~5분 걸립니다.

  tmux attach -t $SESSION     로그 보기 (빠져나오기: Ctrl+B 그다음 D)
  ./serve.sh --stop           내리기

준비되면:
  curl -s localhost:8000/v1/models
EOF
