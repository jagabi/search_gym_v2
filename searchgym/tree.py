"""문항 하나의 탐색 궤적을 트리로 그린다 (`tree.svg`).

세 방법 모두에 적용된다. ragent 와 search-o1 은 모양이 뻔하지만(평면), **뻔하다는
것을 눈으로 확인할 수 있어야** depthsearch 의 트리가 의미를 갖는다.

    ragent       ● 질문 ─┬─ ● search "..."
                         └─ ● fetch  url          (원문이 그대로 들어감)

    search-o1    ● 질문 ─── ● search "..." ─┬─ ○ doc url   (상위 k개 자동 페치)
                                            └─ ○ doc url

    depthsearch  ● 질문 ─┬─ ● search "..."
                         └─ ● fetch  url ─┬─ ● expand url  (depth 2)
                                          └─ ● expand url ─── ● expand url  (depth 3)

색으로 종류를 구분한다 — 파랑 search · 초록 fetch · 주황 expand · 회색 자동 페치 문서.
빨간 테두리는 실패했거나 예산에 막힌 노드다.

의존성 없이 SVG 문자열을 직접 쓴다. 예쁘지 않아도 되고, 브라우저로 열면 된다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # 순환 import 방지. 타입에만 쓴다.
    from .agent import RunResult

__all__ = ["Node", "build", "render", "write_svg"]

# 종류별 색. 채움 / 테두리.
COLORS: dict[str, tuple[str, str]] = {
    "question": ("#d9d9d9", "#666666"),
    "search": ("#8fb8de", "#2f6fb0"),
    "fetch": ("#8fd6ab", "#2e8b57"),
    "expand": ("#f0c47a", "#d08a2c"),
    "doc": ("#e2e2e2", "#999999"),
}
BAD = "#c0392b"           # 실패·거절 테두리
STATUS_MARK = {"answered": "✓", "partial": "~", "not_found": "×"}

RADIUS = 9
STEP_X = 26               # 깊이 한 칸(들여쓰기). 파일트리처럼 좁게 준다
STEP_Y = 26               # 한 줄
PAD = 16
CHAR_W = 6.2              # monospace 11px 의 대략적인 글자 폭


@dataclass
class Node:
    kind: str                       # question | search | fetch | expand | doc
    label: str = ""
    note: str = ""                  # 노드 옆에 붙는 짧은 꼬리표
    bad: bool = False               # 실패·거절
    children: list["Node"] = field(default_factory=list)

    # 레이아웃이 채운다
    x: float = 0.0
    y: float = 0.0

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()


# --- 트리 만들기 -------------------------------------------------------------


def build(result: "RunResult", question: str = "") -> Node:
    """RunResult 를 트리로 바꾼다. steps 의 도구 호출 순서가 그대로 형제 순서다."""
    root = Node(kind="question", label=_clip(question, 60) or "(question)")

    for call in result.tool_calls:
        if call.name == "web_search":
            node = Node(
                kind="search",
                label=_clip(call.query or "(no query)", 46),
                note="예산 초과" if call.refused else ("실패" if call.is_error else ""),
                bad=call.refused or call.is_error,
            )
        elif call.name == "web_fetch":
            node = Node(
                kind="fetch",
                label=_clip(_short_url(call.url), 46),
                note="예산 초과" if call.refused else ("실패" if call.is_error else ""),
                bad=call.refused or call.is_error,
            )
        else:
            node = Node(kind="doc", label=_clip(call.name, 46), bad=True)

        for exploration in call.explorations:
            node.children.extend(_from_exploration(exploration, own_url=call.url))
        root.children.append(node)

    return root


def _from_exploration(log: dict[str, Any], own_url: str = "") -> list[Node]:
    """explorer 호출 하나가 만든 자식들.

    search-o1 은 검색 하나가 문서 k개를 각각 읽으므로 그 문서들을 잎으로 단다.
    depthsearch 는 부모 노드가 이미 그 URL 자체이므로 문서를 다시 달지 않고 확장만
    이어 붙인다.
    """
    children: list[Node] = []

    urls = [u for u in (log.get("urls") or []) if u]
    if len(urls) > 1 or (urls and _short_url(urls[0]) != _short_url(own_url)):
        status = str(log.get("status") or "")
        for url in urls:
            children.append(
                Node(kind="doc", label=_clip(_short_url(url), 44), note=STATUS_MARK.get(status, ""))
            )

    for child in log.get("opened") or []:
        curls = [u for u in (child.get("urls") or []) if u]
        status = str(child.get("status") or "")
        node = Node(
            kind="expand",
            label=_clip(_short_url(curls[0] if curls else "?"), 44),
            note=("saved note" if child.get("reused") else
                  f"d{child.get('depth', '?')} {STATUS_MARK.get(status, status)} "
                  f"{child.get('extraction_state', '')}").strip(),
            bad=status == "not_found" or bool(child.get("error")) or
                child.get("extraction_state", "complete") != "complete",
        )
        node.children.extend(_from_exploration(child, own_url=curls[0] if curls else ""))
        children.append(node)

    return children


# --- 그리기 -----------------------------------------------------------------


def render(root: Node, title: str = "", subtitle: str = "") -> str:
    """트리를 SVG 문자열로.

    파일트리처럼 **한 노드에 한 줄**, 깊이는 들여쓰기로만 준다. 열을 넓게 벌리면
    depth 3 이 화면 밖으로 나가고 라벨끼리 겹친다.
    """
    cursor = [0]

    def place(node: Node, depth: int) -> None:
        node.x = PAD + depth * STEP_X + RADIUS
        node.y = cursor[0] * STEP_Y + RADIUS
        cursor[0] += 1
        for child in node.children:
            place(child, depth + 1)

    place(root, 0)
    nodes = list(root.walk())

    head = 60 if (title or subtitle) else 18
    label_end = max(
        (n.x + RADIUS + 8 + len(n.label + (f"  [{n.note}]" if n.note else "")) * CHAR_W)
        for n in nodes
    )
    # 제목·부제·범례도 넘치지 않게 폭에 반영한다.
    width = int(
        max(label_end, PAD + len(title) * 7.9, PAD + len(subtitle) * 6.4, 460) + PAD
    )
    height = head + cursor[0] * STEP_Y + PAD

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="monospace" font-size="11">',
        f'<rect width="{width}" height="{height}" fill="#fbfbfb"/>',
    ]
    if title:
        parts.append(f'<text x="{PAD}" y="17" font-size="13" fill="#222">{_esc(title)}</text>')
    if subtitle:
        parts.append(f'<text x="{PAD}" y="33" fill="#777">{_esc(subtitle)}</text>')
    parts.append(_legend())

    # 연결선: 부모 아래로 세로선 하나, 자식마다 가로 갈고리.
    for node in nodes:
        if not node.children:
            continue
        top = node.y + head + RADIUS
        bottom = node.children[-1].y + head
        parts.append(
            f'<path d="M{node.x} {top} V{bottom}" fill="none" stroke="#c8c8c8" stroke-width="1"/>'
        )
        for child in node.children:
            parts.append(
                f'<path d="M{node.x} {child.y + head} H{child.x - RADIUS}" '
                f'fill="none" stroke="#c8c8c8" stroke-width="1"/>'
            )

    for node in nodes:
        fill, stroke = COLORS.get(node.kind, COLORS["doc"])
        parts.append(
            f'<circle cx="{node.x}" cy="{node.y + head}" r="{RADIUS}" fill="{fill}" '
            f'stroke="{BAD if node.bad else stroke}" stroke-width="{3 if node.bad else 2}"/>'
        )
        parts.append(
            f'<text x="{node.x + RADIUS + 8}" y="{node.y + head + 4}" fill="#333">'
            f"{_esc(node.label)}</text>"
        )
        if node.note:
            offset = node.x + RADIUS + 8 + len(node.label) * CHAR_W + 10
            parts.append(
                f'<text x="{offset:.0f}" y="{node.y + head + 4}" fill="#999" '
                f'font-size="10">[{_esc(node.note)}]</text>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


def _legend() -> str:
    """왼쪽 위 한 줄. 오른쪽에 두면 라벨이 길어질 때 잘린다."""
    items = [
        ("search", "search"),
        ("fetch", "fetch"),
        ("expand", "expand d>=2"),
        ("doc", "auto doc"),
    ]
    out, x = [], PAD + 2
    for kind, name in items:
        fill, stroke = COLORS[kind]
        out.append(
            f'<circle cx="{x}" cy="49" r="5" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{x + 9}" y="53" fill="#888" font-size="10">{name}</text>'
        )
        x += 14 + len(name) * 5.6 + 12
    out.append(
        f'<circle cx="{x:.0f}" cy="49" r="5" fill="#fff" stroke="{BAD}" stroke-width="2"/>'
        f'<text x="{x + 9:.0f}" y="53" fill="#888" font-size="10">failed / refused</text>'
    )
    return "".join(out)


def write_svg(path: Any, result: "RunResult", question: str = "", subtitle: str = "") -> None:
    root = build(result, question)
    title = f"q · {_clip(question, 80)}" if question else ""
    path.write_text(render(root, title, subtitle), encoding="utf-8")


# --- 도우미 -----------------------------------------------------------------


def _short_url(url: str) -> str:
    """도메인 + 경로 끝만. 트리에서는 이게 더 잘 읽힌다."""
    text = (url or "").split("://", 1)[-1]
    if len(text) <= 44:
        return text
    host, _, rest = text.partition("/")
    tail = rest.rsplit("/", 1)[-1] or rest
    return f"{host}/…/{tail}"[:44]


def _clip(text: str, limit: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _esc(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
