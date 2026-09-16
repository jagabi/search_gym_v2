"""vLLM 엔드포인트가 우리가 기대하는 대로 동작하는지 확인한다.

    python tests/model.py                      # 전부
    python tests/model.py --only chat
    python tests/model.py --prompt "..."       # 아무 프롬프트나 던져 본다
    python tests/model.py --model gpt-oss

확인하는 것 넷.

    reach     /v1/models 가 응답하는가, 우리가 부르는 이름이 거기 있는가
    tokenize  /tokenize 가 응답하는가 (없으면 컨텍스트 절단이 근사치로 물러선다)
    chat      사고가 reasoning_content 로 **분리돼서** 나오는가
    tools     툴콜이 파싱돼서 나오는가 (사고와 툴콜을 동시에 켠 상태로)

세 번째와 네 번째가 중요하다. reasoning_content 가 비어 있고 사고가 content 에
섞여 나오면 서빙 플래그가 틀린 것이다(gemma-4 는 serving.py 의 notes 참고).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from searchgym.config import load_test  # noqa: E402
from searchgym.explorer import FETCH_TOOL  # noqa: E402
from searchgym.llm import LLM  # noqa: E402
from searchgym.paths import load_env  # noqa: E402
from searchgym.report import enable_utf8  # noqa: E402
from searchgym.serving import profile_for  # noqa: E402

CHECKS = ("reach", "tokenize", "chat", "tools")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="vLLM 엔드포인트 점검")
    parser.add_argument("--conf", default="conf.yaml")
    parser.add_argument("--model", default=None)
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--only", default=None, choices=CHECKS)
    parser.add_argument("--prompt", default=None, help="chat 검사에 쓸 프롬프트")
    parser.add_argument("--max-tokens", type=int, default=512)
    return parser.parse_args(argv)


async def main_async(argv: list[str] | None = None) -> int:
    enable_utf8()
    load_env()
    args = parse_args(argv)

    config = load_test(args.conf, model=args.model)
    profile = profile_for(config.model)
    base_url = args.base_url or config.agent.base_url
    llm = LLM(
        profile, base_url=base_url, api_key=config.agent.api_key,
        timeout_s=120, model_name=config.agent.model_name,
    )

    print(f"model     {profile.key}  → 요청은 {llm.model_name!r} 로 보낸다")
    print("팟 필수 인자  " + "  ".join(profile.required_flags()))
    print(f"endpoint  {base_url}")
    print(f"thinking  {'chat_template_kwargs' if profile.thinking_kwarg else 'system prompt'}"
          f"{'  reasoning=' + profile.reasoning_effort if profile.reasoning_effort else ''}")
    print(f"sampling  {json.dumps({**profile.sampling, **profile.sampling_extra})}")

    wanted = [args.only] if args.only else list(CHECKS)
    failed = 0
    try:
        for name in wanted:
            print(f"\n=== {name} " + "=" * (60 - len(name)))
            ok = await globals()[f"_check_{name}"](llm, args)
            failed += 0 if ok else 1
    finally:
        await llm.aclose()

    print(f"\n{'-' * 64}\n{len(wanted) - failed}/{len(wanted)} 통과")
    return 1 if failed else 0


async def _check_reach(llm: LLM, args) -> bool:
    import httpx

    root = llm.base_url.rstrip("/")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{root}/models")
            payload = response.json()
    except Exception as exc:
        print(f"실패: {exc!r}")
        print("vLLM 이 떠 있는지, 터널이 열려 있는지 확인하세요.")
        return False

    names = [m.get("id") for m in payload.get("data") or []]
    print("서버가 아는 이름:", ", ".join(str(n) for n in names) or "(없음)")
    if llm.profile.repo in names:
        print(f"OK — 우리가 부르는 이름 '{llm.profile.repo}' 이 있습니다.")
        return True
    print(
        f"실패 — 우리는 '{llm.profile.repo}' 로 부르는데 서버에 없습니다.\n"
        f"       vllm serve 에 --served-model-name {llm.profile.repo} 를 주세요."
    )
    return False


async def _check_tokenize(llm: LLM, args) -> bool:
    sample = "The quick brown fox jumps over the lazy dog. " * 20
    exact = await llm.count_tokens(sample)
    from searchgym.llm import estimate_tokens

    print(f"{len(sample):,}자 → {exact:,} 토큰   (근사치 {estimate_tokens(sample):,})")
    if exact == estimate_tokens(sample):
        print("경고 — /tokenize 가 실패해 근사치로 물러섰을 수 있습니다.")
        print("       컨텍스트 절단이 부정확해집니다(치명적이진 않습니다).")
        return False
    print("OK")
    return True


async def _check_chat(llm: LLM, args) -> bool:
    prompt = args.prompt or (
        "A train leaves at 14:05 and the journey takes 97 minutes. "
        "What time does it arrive? Answer with the time only."
    )
    messages = [{"role": "user", "content": _with_effort(llm, prompt)}]
    try:
        reply = await llm.chat(messages, max_tokens=args.max_tokens)
    except Exception as exc:
        print(f"실패: {exc!r}")
        return False

    print(f"finish_reason  {reply.finish_reason}")
    print(f"prompt/completion tokens  {reply.prompt_tokens} / {reply.completion_tokens}")
    print(f"\n--- reasoning_content ({len(reply.reasoning):,}자) ---")
    print(reply.reasoning or "(비어 있음)")
    print(f"\n--- content ({len(reply.text):,}자) ---")
    print(reply.text or "(비어 있음)")

    if not reply.reasoning:
        hint = (
            f"--reasoning-parser {llm.profile.reasoning_parser} 가 맞는지"
            if llm.profile.reasoning_parser
            else "이 모델은 harmony 내장 처리라 --reasoning-parser 를 주지 않습니다"
        )
        print(
            f"\n경고 — 사고가 분리되지 않았습니다. {hint},\n"
            "       gemma-4 라면 VLLM_USE_V2_MODEL_RUNNER=0 과 tool chat template 을\n"
            "       줬는지 확인하세요(serving.py notes)."
        )
        return False
    if reply.truncated:
        print("\n경고 — max_tokens 에 걸려 끊겼습니다. agent.max_tokens 를 올리세요.")
        return False
    print("\nOK — 사고와 응답이 분리되어 나왔습니다.")
    return True


async def _check_tools(llm: LLM, args) -> bool:
    prompt = (
        "You are reading a page about the Treaty of Waitangi. The page says the full "
        "text is at https://example.org/treaty/full. Open that page to confirm the "
        "signing date."
    )
    messages = [{"role": "user", "content": _with_effort(llm, prompt)}]
    try:
        reply = await llm.chat(messages, max_tokens=args.max_tokens, tools=[FETCH_TOOL])
    except Exception as exc:
        print(f"실패: {exc!r}")
        return False

    print(f"finish_reason  {reply.finish_reason}")
    print(f"reasoning {len(reply.reasoning):,}자 · content {len(reply.text):,}자")
    if not reply.tool_calls:
        print("\n--- content ---")
        print(reply.text or "(비어 있음)")
        print(
            "\n실패 — 툴콜이 안 나왔습니다. --enable-auto-tool-choice 와\n"
            f"       --tool-call-parser {llm.profile.tool_call_parser} 를 확인하세요.\n"
            "       (모델이 도구를 안 쓰기로 판단했을 수도 있으니 한 번 더 돌려 보세요.)"
        )
        return False

    for call in reply.tool_calls:
        print(f"\ntool_call  {call.function.name}")
        print(call.function.arguments)
    print("\nOK — 사고와 툴콜이 함께 나왔습니다.")
    return True


def _with_effort(llm: LLM, prompt: str) -> str:
    """gpt-oss 는 추론 강도를 프롬프트 한 줄로 받는다."""
    effort = llm.profile.reasoning_effort
    return f"Reasoning: {effort}\n{prompt}" if effort else prompt


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async()))
