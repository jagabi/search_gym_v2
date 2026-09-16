"""모델별 프로파일.

**이 저장소는 모델을 띄우지 않는다.** vLLM 은 RunPod 등의 기성 이미지로 팟에서
돌고, 우리는 OpenAI 호환 엔드포인트에 요청만 보낸다. 그래서 여기 남는 것은
"부를 때 필요한 것" 뿐이다 — 모델 이름, 권장 샘플링, 추론을 켜는 방식.

    도구는 팟이 모른다.  MCP 서버는 로컬에서 돌고, 우리가 도구 스키마를 요청 본문의
    `tools=[...]` 에 실어 보낸다. 팟은 툴콜을 **파싱해서 돌려주기만** 하면 된다.

그래서 팟의 vLLM 실행 인자에 파서가 켜져 있어야 한다. 없으면 툴콜이 파싱되지 않아
모델이 도구 호출을 평문으로 뱉고, 사고가 content 에 섞여 나온다. 필요한 인자는
`profile.required_flags()` 가 준다.

**파서 이름과 필요 여부는 모델·vLLM 빌드마다 다르다.**

    qwen      --tool-call-parser qwen3_coder  --reasoning-parser qwen3
    gemma     --tool-call-parser gemma4       --reasoning-parser gemma4
    gpt-oss   --tool-call-parser openai       --reasoning-parser openai_gptoss
              **이미지는 vllm/vllm-openai:latest.** :gptoss 태그에는 gpt-oss 용
              tool-call 파서가 아직 없어 기동조차 못 한다.

잘못 주면 기동 시 invalid choice 로 죽으면서 그 빌드가 아는 목록을 찍어 준다.
`python tests/model.py` 가 실제로 켜졌는지 확인한다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__all__ = ["PROFILES", "ServeProfile", "profile_for"]


@dataclass(slots=True)
class ServeProfile:
    """한 모델을 **부르는 데** 필요한 전부."""

    key: str
    # 요청의 `model` 필드로 보내는 이름. 팟이 다른 이름으로 서빙하면
    # conf.yaml 의 served_model_name 으로 덮어쓴다.
    repo: str
    # 팟의 vLLM 이 이 파서로 떠 있어야 한다. 우리가 쓰는 값은 아니고 점검용이다.
    tool_call_parser: str
    reasoning_parser: str
    # 권장 샘플링. 모델카드 값을 그대로 쓴다(OpenAI 표준 파라미터만).
    sampling: dict[str, Any] = field(default_factory=dict)
    # OpenAI 표준이 아닌 샘플링(repetition_penalty, top_k 등)은 extra_body 로 나간다.
    sampling_extra: dict[str, Any] = field(default_factory=dict)
    # 시스템 프롬프트에 "Reasoning: <값>" 한 줄로 추론 강도를 주는 모델(gpt-oss)만
    # 채운다. 비어 있으면 시스템 프롬프트에 아무것도 붙이지 않는다.
    reasoning_effort: str = ""
    # chat_template_kwargs={"enable_thinking": ...} 를 이해하는 모델인가.
    # gpt-oss 는 harmony 포맷이라 이 키를 모르고 reasoning_effort 로 대신 받는다.
    thinking_kwarg: bool = True
    # 팟을 띄울 때 알아야 할 것. tests/model.py 가 실패하면 여기부터 본다.
    notes: str = ""

    def required_flags(self) -> list[str]:
        """팟의 vLLM 이 반드시 들고 떠야 하는 인자.

        파서 이름은 **vLLM 빌드마다 다르다.** 잘못 주면 기동 시 invalid choice 로
        죽으면서 그 빌드가 아는 목록을 찍어 준다 — 그걸 보고 맞추면 된다.
        """
        flags = ["--enable-auto-tool-choice"]
        if self.tool_call_parser:
            flags.append(f"--tool-call-parser {self.tool_call_parser}")
        if self.reasoning_parser:
            flags.append(f"--reasoning-parser {self.reasoning_parser}")
        flags.append(f"--served-model-name {self.repo}")
        return flags


PROFILES: dict[str, ServeProfile] = {
    "qwen": ServeProfile(
        key="qwen",
        repo="Qwen/Qwen3.5-9B",
        tool_call_parser="qwen3_coder",
        reasoning_parser="qwen3",
        sampling={"temperature": 1.0, "top_p": 0.95, "presence_penalty": 1.5},
        sampling_extra={"top_k": 20},
        notes=(
            "thinking 이 기본으로 켜져 있다. 우리는 항상 켜므로 따로 할 일이 없다.\n"
            "네이티브 262K 까지 되지만 128K 로 잡아도 충분하다 — agent.context_limit 은\n"
            "그 값에서 답변 여유를 뺀 120K 다. 팟의 --max-model-len 이 그보다 작으면\n"
            "context_limit 을 같이 내려야 한다."
        ),
    ),
    "gpt-oss": ServeProfile(
        key="gpt-oss",
        repo="openai/gpt-oss-20b",
        tool_call_parser="openai",
        # **둘 다 필요하다(실측).** vLLM recipe 의 "reasoning and final text output
        # will be returned structurally" 는 파서 없이도 분리된다는 뜻이 아니다.
        # 파서를 빼면 reasoning_content 가 늘 비고 CoT 가 content 에 섞여 나온다.
        reasoning_parser="openai_gptoss",
        sampling={"temperature": 1.0, "top_p": 1.0},
        # 이 모델만 추론 강도를 시스템 프롬프트로 받는다. medium 으로 고정한다 —
        # high 는 사고 토큰이 폭주하고(이전 실험에서 답변 449토큰에 사고 2만 토큰),
        # 이 과제에 필요한 것은 깊은 추론이 아니라 페이지를 열어 읽는 것이다.
        reasoning_effort="medium",
        thinking_kwarg=False,
        notes=(
            "**이미지를 vllm/vllm-openai:latest 로 쓸 것.** :gptoss 태그는 출시 무렵에\n"
            "핀된 스냅샷이라 gpt-oss 용 --tool-call-parser openai 가 아직 없다\n"
            "(기동 시 KeyError: 'invalid tool call parser: openai' 로 죽는다).\n"
            "\n"
            "vLLM recipe (docs.vllm.ai/projects/recipes → OpenAI → GPT OSS):\n"
            "  Function calling: --tool-call-parser openai --enable-auto-tool-choice\n"
            "여기에 **--reasoning-parser openai_gptoss 도 반드시 넣는다(실측).** 문서의\n"
            "'reasoning and final text output will be returned structurally' 는 파서\n"
            "없이도 분리된다는 뜻이 아니다 — 빼고 돌리면 reasoning_content 가 늘 비고\n"
            "CoT 가 content 에 섞여 나온다. 그러면 explorer 에게 넘길 누적 추론이\n"
            "사라져 '(none yet)' 만 내려간다.\n"
            "\n"
            "**--reasoning-parser openai_gptoss 는 openai_harmony 를 초기화하고, 그게 tiktoken\n"
            "vocab 파일을 원격 CDN 에서 받는다(HuggingFace 가 아니다).** 컨테이너에 DNS 가\n"
            "없으면 httpx.ConnectError 로 서버가 통째로 죽는다 — 파서를 빼면 뜨는데\n"
            "reasoning_content 가 비므로, 증상만 보고 파서 탓을 하면 안 된다.\n"
            "  TIKTOKEN_RS_CACHE_DIR=/root/.cache/huggingface/tiktoken\n"
            "볼륨 안이라 한 번만 받으면 영구 캐시된다(첫 1회는 DNS 필요).\n"
            "미리 받아두려면 DNS 되는 곳에서:\n"
            "  pip install openai-harmony\n"
            "  TIKTOKEN_RS_CACHE_DIR=./vocab python -c \\\n"
            "    \"from openai_harmony import load_harmony_encoding;\\\n"
            "     load_harmony_encoding('HarmonyGptOss')\"\n"
            "생긴 해시 이름 파일을 팟의 캐시 디렉터리에 넣는다.\n"
            "\n"
            "Known Limitations: H100 TP1 에서 기본 gpu-memory-utilization 이면 OOM 이 난다.\n"
            "--gpu-memory-utilization 0.95 (필요하면 --max-num-batched-tokens 1024).\n"
            "Ampere(A100)도 TRITON_ATTN + Marlin MXFP4 로 기본 동작한다.\n"
            "\n"
            "추론 강도는 시스템 프롬프트의 'Reasoning: medium' 한 줄로 자동 주입된다."
        ),
    ),
    "gemma": ServeProfile(
        key="gemma",
        repo="google/gemma-4-12B-it",
        tool_call_parser="gemma4",
        reasoning_parser="gemma4",
        sampling={"temperature": 1.0, "top_p": 0.95},
        # 사고 중 같은 문단을 되풀이하다 max_tokens 에 걸리는 것을 막는다(실측).
        sampling_extra={"repetition_penalty": 1.05},
        notes=(
            "**사고와 툴콜을 동시에 켜면 기성 이미지로는 잘 안 된다.** 팟 템플릿에\n"
            "아래 셋을 다 넣어야 한다 — 전부 실측이다.\n"
            "  1) 환경변수 VLLM_USE_V2_MODEL_RUNNER=0\n"
            "     V2 러너는 gemma-4 의 thinking_token_budget 을 지원하지 않아 사고가\n"
            "     통째로 죽는다 — reasoning_content 가 늘 비고 사고가 content 로 섞인다.\n"
            "     기동 로그의 'does not yet support the thinking_token_budget' 이 신호다.\n"
            "     이때 --async-scheduling 은 빼야 할 수 있다.\n"
            "  2) --chat-template <tool_chat_template_gemma4.jinja 절대경로>\n"
            "     vLLM 저장소에 있고 pip 설치본에는 없다. 팟에 따로 넣어야 한다.\n"
            "  3) repetition_penalty 1.05 (이 프로파일이 요청마다 보낸다)\n"
            "또 transformers 5.15+ 에서 config.head_dim 접근이 막혀 vLLM 이 못 뜬다\n"
            "(AmbiguousGlobalPerLayerAttributeError). 이미지의 transformers 가 5.15 이상이면\n"
            "  pip install 'transformers==5.14.*'\n"
            "확인: AutoConfig.from_pretrained(경로).head_dim 이 256 이면 OK.\n"
            "셋 중 VRAM 이 제일 빡빡하다(128K 에서 KV ~16GB + 가중치 23GB).\n"
            "빠듯하면 --kv-cache-dtype fp8."
        ),
    ),
}


def profile_for(name: str) -> ServeProfile:
    """프로파일 키('qwen') 또는 HuggingFace 저장소 ID로 찾는다."""
    if name in PROFILES:
        return PROFILES[name]
    for profile in PROFILES.values():
        if profile.repo.lower() == name.lower():
            return profile
    raise ValueError(
        f"알 수 없는 모델 '{name}'. 사용 가능: {', '.join(PROFILES)} "
        f"(또는 {', '.join(p.repo for p in PROFILES.values())})"
    )
