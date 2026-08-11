"""모델별 vLLM 서빙 프로파일.

세 모델을 전부 vLLM의 OpenAI 호환 서버로 띄우므로 에이전트 코드는 하나면 된다.
다른 것은 서빙 플래그와 권장 샘플링뿐이라 그것만 여기 모은다.

    python scripts/serve.py qwen        # 띄울 명령을 출력한다

각 값의 출처는 HF 모델카드와 vLLM recipes다. 셋 다 툴콜과 추론(thinking)을
네이티브로 지원하고, vLLM이 `reasoning_content`와 `tool_calls`를 분리해 준다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .paths import PROJECT_ROOT

__all__ = ["MODELS_DIR", "PROFILES", "ServeProfile", "profile_for"]

# 가중치는 여기에 git clone 해 둔다. 있으면 로컬 경로로, 없으면 HF ID로 띄운다.
#
#   git lfs install
#   git clone https://huggingface.co/Qwen/Qwen3.5-9B models/Qwen3.5-9B
MODELS_DIR = PROJECT_ROOT / "models"


@dataclass(slots=True)
class ServeProfile:
    """한 모델을 띄우고 부르는 데 필요한 전부."""

    key: str
    repo: str  # HuggingFace 저장소 ID
    tool_call_parser: str
    reasoning_parser: str
    # 권장 샘플링. 모델카드 값을 그대로 쓴다.
    sampling: dict[str, Any] = field(default_factory=dict)
    # chat template를 따로 줘야 하는 모델만 채운다(vLLM 저장소 기준 상대 경로).
    chat_template: str = ""
    # 이 모델만 붙는 추가 플래그.
    extra_flags: list[str] = field(default_factory=list)
    # 이 모델만의 주의사항. serve 명령과 함께 출력된다.
    notes: str = ""
    max_model_len: int = 128000
    # 시스템 프롬프트에 "Reasoning: <값>" 한 줄로 추론 강도를 주는 모델(gpt-oss)만
    # 채운다. AgentConfig.reasoning_effort가 비어 있으면 이 값이 쓰인다.
    reasoning_effort: str = ""

    @property
    def local_dir(self) -> Path:
        """`models/<저장소 이름>`. clone 받아 둘 위치."""
        return MODELS_DIR / self.repo.rsplit("/", 1)[-1]

    @property
    def is_local(self) -> bool:
        return (self.local_dir / "config.json").exists()

    @property
    def model(self) -> str:
        """vLLM에 넘길 경로. 로컬 clone이 있으면 그쪽을 쓴다.

        `--served-model-name`으로 이름을 repo ID에 고정하므로, 클라이언트가 부르는
        모델 이름은 로컬이든 원격이든 동일하다.
        """
        return str(self.local_dir) if self.is_local else self.repo

    def clone_command(self) -> str:
        return f"git clone https://huggingface.co/{self.repo} {self.local_dir}"

    def serve_command(self, max_model_len: int | None = None, gpu_util: float = 0.90) -> str:
        parts = [
            "vllm serve",
            self.model,
            f"--served-model-name {self.repo}",
            f"--max-model-len {max_model_len or self.max_model_len}",
            f"--gpu-memory-utilization {gpu_util}",
            "--enable-auto-tool-choice",
            f"--tool-call-parser {self.tool_call_parser}",
            f"--reasoning-parser {self.reasoning_parser}",
        ]
        if self.chat_template:
            parts.append(f"--chat-template {self.chat_template}")
        parts += [*self.extra_flags, "--host 127.0.0.1", "--port 8000"]
        return " \\\n  ".join(parts)


PROFILES: dict[str, ServeProfile] = {
    "gemma": ServeProfile(
        key="gemma",
        repo="google/gemma-4-12B-it",
        tool_call_parser="gemma4",
        reasoning_parser="gemma4",
        # 비워 둔다. 모델에 딸려 온 chat template이 도구를 지원하므로 대개 필요 없고,
        # vLLM 저장소의 examples/ 경로를 그대로 주면 pip 설치본에는 그 파일이 없어
        # 기동 전에 죽는다. 내장 템플릿으로 툴콜이 안 되면 그때만 파일을 받아
        # 절대 경로로 지정한다:
        #   curl -sL -o /workspace/gemma4.jinja https://raw.githubusercontent.com/\
        #     vllm-project/vllm/main/examples/tool_chat_template_gemma4.jinja
        chat_template="",
        sampling={"temperature": 1.0, "top_p": 0.95},
        # 우리 워크로드는 텍스트 전용이다. 비전·오디오 프로파일링을 끄면 기동이
        # 빨라지고 그만큼 KV에 쓸 메모리가 남는다(vLLM 레시피 권장).
        extra_flags=["--limit-mm-per-prompt '{\"image\": 0, \"audio\": 0}'", "--async-scheduling"],
        notes=(
            "**transformers를 5.14.x로 내려야 뜬다 (실측: vLLM 0.27.1 + transformers 5.14.1).**\n"
            "vLLM은 이 아키텍처를 지원한다 — Gemma4UnifiedForConditionalGeneration이 supported\n"
            "archs에 있다. 문제는 transformers 5.15부터 config.head_dim 접근이 막히는 것이다:\n"
            "  AmbiguousGlobalPerLayerAttributeError: 'head_dim' is a per-layer attribute\n"
            "레이어마다 head_dim이 다른데(sliding 256 / global 512) vLLM의 get_head_size()가\n"
            "전역 값 하나를 읽기 때문이다. vLLM이 transformers 상한을 안 걸어 둬서(>=5.5.3)\n"
            "최신이 그냥 깔린다. 서버 환경에서만 내리면 된다:\n"
            "  uv pip install 'transformers==5.14.*'\n"
            "확인: AutoConfig.from_pretrained(경로).head_dim 이 256을 돌려주면 OK.\n"
            "너무 내리면 반대로 config 자체를 못 읽는다(Gemma4Unified가 신규 아키텍처).\n"
            "에러가 안내하는 allow_global_per_layer_attribute_access는 쓰지 말 것 —\n"
            "transformers 다운그레이드가 같은 효과를 내면서 훨씬 명시적이다.\n"
            "chat template은 모델 내장본이 tools를 지원하므로 --chat-template이 필요 없다\n"
            "(vLLM 저장소의 examples/ 경로를 주면 pip 설치본에는 그 파일이 없어 죽는다).\n"
            "셋 중 VRAM이 제일 빡빡하다. global 레이어 head_dim이 512라 KV가 비싸서"
            " 128K에서 KV ~16GB + 가중치 24GB = ~40GB다(A6000 48GB에 시리얼로 들어간다).\n"
            "전제는 슬라이딩 윈도우 하이브리드 KV가 제대로 잡히는 것이다. 안 잡히면 KV가"
            " 65GB로 뛰어 못 올라간다 — 기동 로그의 KV 블록 수로 반드시 확인할 것.\n"
            "빠듯하면 --kv-cache-dtype fp8로 KV를 절반(~8GB)으로 내린다."
        ),
    ),
    "qwen": ServeProfile(
        key="qwen",
        repo="Qwen/Qwen3.5-9B",
        tool_call_parser="qwen3_coder",
        reasoning_parser="qwen3",
        sampling={"temperature": 1.0, "top_p": 0.95, "top_k": 20, "presence_penalty": 1.5},
        notes=(
            "thinking이 기본으로 켜져 있다. 끄려면 요청에"
            ' chat_template_kwargs={"enable_thinking": false}를 넘긴다.\n'
            "네이티브 262K까지 되지만 128K로 잡아 둔다. 하이브리드 아키텍처"
            "(GatedDeltaNet + Attention)라 KV가 표준 트랜스포머보다 싸다."
        ),
    ),
    "gpt-oss": ServeProfile(
        key="gpt-oss",
        repo="openai/gpt-oss-20b",
        tool_call_parser="openai",
        reasoning_parser="openai_gptoss",
        sampling={"temperature": 1.0, "top_p": 1.0},
        # 이 모델만 추론 강도를 시스템 프롬프트로 받는다. medium으로 고정한다 —
        # high는 사고 토큰이 폭주하고(이전 실험에서 답변 449토큰에 사고 2만 토큰),
        # 이 과제에 필요한 것은 깊은 추론이 아니라 페이지를 열어 읽는 것이다.
        reasoning_effort="medium",
        notes=(
            "harmony 포맷 전용 모델이지만, vLLM의 OpenAI 호환 서버가 변환을 처리하므로"
            " /v1/chat/completions를 그대로 쓰면 된다(vLLM >= 0.10).\n"
            "추론 강도는 시스템 프롬프트의 'Reasoning: medium' 한 줄로 자동 주입된다"
            " (agent.reasoning_effort로 덮어쓸 수 있다)."
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
