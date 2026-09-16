"""Validate fetch arguments and unwrap accidental nested Reader URLs."""

import re
from urllib.parse import urlsplit


def normalize_fetch_url(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("url must be a non-empty absolute HTTP(S) URL")
    url = value.strip()
    for _ in range(4):
        try:
            parsed = urlsplit(url)
        except ValueError as exc:
            raise ValueError("malformed URL") from exc
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("url must include http:// or https:// and a hostname")
        if parsed.hostname.lower() != "r.jina.ai":
            return url
        url = url.split("://", 1)[1].split("/", 1)[-1]
    raise ValueError("too many nested Reader URLs; use the original page URL")


def reader_failure(text: str) -> str:
    """Recognize Reader metadata, never incidental '404' words in an article."""
    if not text.strip() or ("Markdown Content:" in text and not text.split("Markdown Content:", 1)[1].strip()):
        return "Empty source body; no readable evidence returned"
    match = re.search(r"^Warning:\s*Target URL returned error\s+([45]\d\d)\b[^\n]*",
                      text, re.MULTILINE | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    title = re.search(r"^Title:\s*(.*?)\s*$", text[:1000], re.MULTILINE | re.IGNORECASE)
    if title and title.group(1).strip().lower() in {
        "just a moment...", "access denied", "attention required! | cloudflare",
    }:
        return f"Access challenge: {title.group(1)}"
    if title and re.fullmatch(
        r"(?:404(?:\s*[-:|]\s*)?)?(?:page not found|not found|404 not found)"
        r"(?:\s*[-|\u2013\u2014]\s*[^\n]+)?", title.group(1).strip(), re.IGNORECASE
    ):
        return f"Missing page: {title.group(1)}"
    return ""
