#!/usr/bin/env bash
# eval/train을 tmux 세션 'run'에서 돌린다. SSH가 끊겨도 살아남는다.
#
#   ./run.sh smoke                                   # 배선 점검
#   ./run.sh eval --limit 1 --tag wiring --no-cache   # 한 문항
#   ./run.sh eval --tag baseline                      # 전체
#   ./run.sh eval --tag baseline --resume             # 멈춘 실행 이어서
#   ./run.sh train --tag seed0
#
#   ./run.sh --attach              진행 상황 보기 (빠져나오기: Ctrl+B 그다음 D)
#   ./run.sh --stop                중단
#
# 클라이언트는 시스템 파이썬을 쓴다. vllm-env가 활성화돼 있어도 무시한다 —
# 그쪽에는 dspy·google-genai가 없다.
set -euo pipefail

cd "$(dirname "$0")"
SESSION=${SESSION:-run}
PY=/usr/bin/python3
[ -x "$PY" ] || PY=$(command -v python3)

case "${1:-}" in
  --attach|-a) exec tmux attach -t "$SESSION" ;;
  --stop)      tmux kill-session -t "$SESSION" 2>/dev/null && echo "세션 '$SESSION' 중단" || echo "세션 '$SESSION' 없음"; exit 0 ;;
  "")          echo "사용법: ./run.sh {smoke|eval|train} [옵션...]" >&2; exit 1 ;;
esac

command -v tmux >/dev/null || { echo "tmux가 없습니다:  apt-get update && apt-get install -y tmux" >&2; exit 1; }

TASK=$1; shift
case "$TASK" in
  smoke) SCRIPT="scripts/smoke.py" ;;
  eval)  SCRIPT="eval.py" ;;
  train) SCRIPT="train.py" ;;
  tool)  SCRIPT="scripts/tool.py" ;;
  *)     echo "알 수 없는 작업 '$TASK' (smoke|eval|train|tool)" >&2; exit 1 ;;
esac

# 서버가 떠 있는지 먼저 본다 — 없으면 문항마다 404를 맞으며 시간만 버린다.
if [ "$TASK" != "smoke" ] && ! curl -sf localhost:8000/v1/models >/dev/null 2>&1; then
  echo "vLLM이 응답하지 않습니다(localhost:8000). 먼저:  ./serve.sh" >&2
  exit 1
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "세션 '$SESSION'이 이미 돌고 있습니다.  ./run.sh --attach  또는  ./run.sh --stop"
  exit 1
fi

# 로그를 파일로도 남긴다. tmux 스크롤백은 길면 잘린다.
mkdir -p runs/logs
LOG="runs/logs/$(date +%Y%m%d-%H%M)_${TASK}.log"
printf -v ARGS '%q ' "$@"

echo "실행 : $PY $SCRIPT $ARGS"
echo "로그 : $LOG"

tmux new-session -d -s "$SESSION" \
  "cd '$PWD'; $PY $SCRIPT $ARGS 2>&1 | tee '$LOG'; echo; echo '[완료 — 창을 닫으려면 exit]'; exec bash"

cat <<EOF

세션 '$SESSION' 시작.

  ./run.sh --attach     진행 보기 (빠져나오기: Ctrl+B 그다음 D)
  tail -f $LOG          로그만 보기
  ./run.sh --stop       중단
EOF
