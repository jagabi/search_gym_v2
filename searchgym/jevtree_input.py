"""Number only complete URLs in the JEV prefix; no model preprocessing."""
import re

from .explorer import _balanced_markdown_links, _balanced_url_tokens, _norm

INPUT_VERSION = 'prefix-only-numbered-links/1'
LINK_CRITERIA = {'true': 'Helps find the answer.', 'false': 'Unrelated or navigation.'}


def _unescape(url: str) -> str:
    return re.sub(r'\\([\\`*_{}\[\]()#+\-.!~])', r'\1', url)


def complete_prefix(source: str, prefix: str) -> str:
    """Back off if the token cut bisects a Markdown link or bare URL.

    The suffix is inspected only to detect crossing spans, never sent to JEV
    or used to introduce candidates beyond the cut.
    """
    if len(prefix) >= len(source):
        return prefix
    boundary = len(prefix)
    for start, end, _label, _url in _balanced_markdown_links(source):
        if start < boundary < end:
            boundary = start
    for start, end, _url in _balanced_url_tokens(source):
        if start < boundary < end:
            boundary = start
    return source[:boundary]


def numbered_page(page: str, links: list[tuple[str, str]]) -> str:
    """Keep each link's location and label. URL mapping stays in the caller.

    Markdown destinations become link IDs; bare URLs keep their visible text
    because they have no label that could describe the destination.
    """
    ids = {_norm(url): f'link_{i}' for i, (url, _anchor) in enumerate(links)}
    edits, markdown_spans = [], []
    for start, end, label, url in _balanced_markdown_links(page):
        markdown_spans.append((start, end))
        key = ids.get(_norm(_unescape(url)))
        if key:
            edits.append((start, end, f'[{label}]({key})'))
    for start, end, url in _balanced_url_tokens(page):
        if any(lo <= start < hi for lo, hi in markdown_spans):
            continue
        key = ids.get(_norm(_unescape(url)))
        if key:
            edits.append((start, end, f'{page[start:end]} [{key}]'))
    parts, cursor = [], 0
    for start, end, replacement in sorted(edits):
        if start < cursor:
            continue
        parts.extend((page[cursor:start], replacement))
        cursor = end
    parts.append(page[cursor:])
    return ''.join(parts)


def page_requests(*, question: str, page_url: str, page: str, links: list[tuple[str, str]],
                  page_questions: dict, links_per_request: int) -> list[tuple[dict, dict]]:
    state = {'question': question, 'page_url': page_url, 'page_text': numbered_page(page, links)}
    packets = []
    for start in range(0, max(1, len(links)), links_per_request):
        questions = dict(page_questions) if start == 0 else {}
        for i in range(start, min(start + links_per_request, len(links))):
            questions[f'link_{i}'] = {
                'type': 'noul',
                'instructions': f'Would following link_{i} in page_text help answer question?',
                'criteria': LINK_CRITERIA,
            }
        packets.append((state, questions))
    return packets
