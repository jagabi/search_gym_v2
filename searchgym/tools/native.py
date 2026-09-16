"""Bounded public document download for linked CSV/PDF files.

File parsing is shared by every method. No search service or model is invoked.
"""
import csv
import io
import re
from urllib.parse import urlsplit

MAX_BYTES = 24 * 1024 * 1024


def checked_rows(rows):
    result, cells = [], 0
    for row in rows:
        cells += len(row)
        if cells > 1_000_000:
            raise ValueError("Table exceeds one million cells; use a smaller source file")
        result.append(["" if c is None else str(c) for c in row])
    return result


def file_kind(url):
    path = urlsplit(url).path.lower()
    return next((ext for ext in ("csv", "pdf") if path.endswith("." + ext)), "")


def decode_document(payload: bytes, kind: str, url: str) -> str:
    if kind == "csv":
        text = payload.decode("utf-8-sig")
        if text.lstrip().lower().startswith(("<!doctype", "<html")):
            raise ValueError("File URL returned HTML instead of tabular data")
        try:
            dialect = csv.Sniffer().sniff(text[:8192], delimiters=",\t;")
        except csv.Error:
            dialect = "excel"
        rows = checked_rows(csv.reader(io.StringIO(text), dialect))
        if not rows or max(map(len, rows)) < 2:
            raise ValueError("No tabular data in response")
        out = io.StringIO(newline="")
        csv.writer(out, lineterminator="\n").writerows(rows)
        return f"Title: CSV document\nURL Source: {url}\nMarkdown Content:\n" + out.getvalue()
    elif kind == "pdf":
        # A .pdf URL can return a text/HTML error with HTTP 200. Do not ask the
        # tolerant parser to reconstruct an unrelated payload as a damaged PDF.
        if b"%PDF-" not in payload[:1024]:
            raise ValueError("PDF URL returned a non-PDF body (missing %PDF- header)")
        from pypdf import PdfReader
        book = PdfReader(io.BytesIO(payload))
        if len(book.pages) > 1500:
            raise ValueError("PDF exceeds 1500 pages; select a smaller linked document")
        pages = [(i + 1, compact_pdf_text(page.extract_text(extraction_mode="layout") or "") if "/Contents" in page else "")
                 for i, page in enumerate(book.pages)]
        if not any(text.strip() for _, text in pages):
            raise ValueError("PDF has no extractable text; scanned/image evidence needs OCR or vision")
        return f"Title: PDF document\nURL Source: {url}\nMarkdown Content:\n" + "\n\n".join(
            f"[PDF page {i}]\n{text}" for i, text in pages)
    else:
        raise ValueError("Unsupported native format")


def compact_pdf_text(text: str) -> str:
    """Remove layout padding while retaining lines and visible column separation."""
    lines = [re.sub(r"[ \t]{3,}", "  ", line).strip() for line in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


async def fetch_native(url: str) -> str:
    import httpx
    kind = file_kind(url)
    if not kind:
        raise ValueError("Not a supported file URL")
    async with httpx.AsyncClient(timeout=30, follow_redirects=True, max_redirects=5) as client:
        async with client.stream("GET", url, headers={"User-Agent": "SearchGym source reader"}) as reply:
            reply.raise_for_status()
            chunks, size = [], 0
            async for chunk in reply.aiter_bytes():
                size += len(chunk)
                if size > MAX_BYTES:
                    raise ValueError("Source exceeds the 24 MiB download limit")
                chunks.append(chunk)
    import asyncio
    return await asyncio.to_thread(decode_document, b"".join(chunks), kind, url)
