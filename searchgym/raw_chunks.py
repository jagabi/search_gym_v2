"""Docling HybridChunker over source Markdown, with lossless block ingestion.

No PDF/layout models or generative rewriting. Headings are structural; other
Markdown blocks (including tables and code) remain source text in Docling items.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import csv
import io
import threading


@dataclass
class Chunk:
    index: int
    text: str
    tokens: int
    headings: list[str]


class SourceChunker:
    def __init__(self, model: str, chunk_tokens: int):
        from tokenizers import Tokenizer
        from docling_core.transforms.chunker.tokenizer.base import BaseTokenizer
        from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
        from markdown_it import MarkdownIt

        class DecisionTokenizer(BaseTokenizer):
            encoder: Any
            limit: int

            def count_tokens(self, text: str) -> int:
                return len(self.encoder.encode(text, add_special_tokens=False).ids)

            def get_max_tokens(self) -> int:
                return self.limit

            def get_tokenizer(self):
                # semchunk accepts a callable token counter.
                return self.count_tokens

        self.encoder = Tokenizer.from_pretrained(model)
        self.encoder.no_truncation()
        self.encoder.no_padding()
        self.tokenizer = DecisionTokenizer(encoder=self.encoder, limit=chunk_tokens)
        self.hybrid = HybridChunker(
            tokenizer=self.tokenizer, merge_peers=True, always_emit_headings=True,
        )
        self.markdown = MarkdownIt("commonmark").enable("table")
        self._lock = threading.Lock()

    def count(self, text: str) -> int:
        return self.tokenizer.count_tokens(text)

    def prefix(self, text: str, limit: int) -> str:
        encoded = self.encoder.encode(text, add_special_tokens=False)
        if len(encoded.ids) <= limit:
            return text
        # Preserve source characters instead of decoding/normalizing token text.
        end = encoded.offsets[limit - 1][1]
        while end and self.count(text[:end]) > limit:
            end -= 1
        return text[:end]

    def chunks(self, text: str) -> list[Chunk]:
        with self._lock:
            return self._chunks(text)

    def sections(self, text: str) -> list[dict]:
        from .raw_navigation import source_sections
        with self._lock:
            return source_sections(text, self.markdown)

    def _chunks(self, text: str) -> list[Chunk]:
        from docling_core.types.doc import DoclingDocument, DocItemLabel
        doc = DoclingDocument(name="source")
        lines = text.splitlines(keepends=True)
        cursor = 0
        # Native CSV is kept losslessly as CSV, not guessed into Markdown.
        # Give HybridChunker the first row as structural column context so it
        # repeats that context when a long table is split into later chunks.
        native_csv = text.startswith('Title: CSV document\n') and 'Markdown Content:\n' in text
        if native_csv:
            header, body = text.split('Markdown Content:\n', 1)
            doc.add_text(label=DocItemLabel.TEXT, text=header.strip())
            rows = csv.reader(io.StringIO(body))
            for i, row in enumerate(rows):
                out = io.StringIO(newline='')
                csv.writer(out, lineterminator='\n').writerow(row)
                value = out.getvalue().rstrip('\n')
                if i == 0:
                    doc.add_heading(text='CSV columns (first row): ' + value, level=1)
                else:
                    # Literal CSV records: Markdown must not reinterpret a
                    # quoted newline, URL, pipe, or punctuation inside a cell.
                    doc.add_code(text=value)
            cursor = len(lines)
        for token in ([] if native_csv else self.markdown.parse(text)):
            if token.level != 0 or token.map is None or token.map[0] < cursor:
                continue
            start, end = token.map
            if start > cursor:
                gap = "".join(lines[cursor:start]).strip()
                if gap:
                    doc.add_text(label=DocItemLabel.TEXT, text=gap)
            block = "".join(lines[start:end]).strip()
            if block:
                if token.type == "heading_open":
                    doc.add_heading(text=block, level=int(token.tag[1:]))
                else:
                    doc.add_text(label=DocItemLabel.TEXT, text=block)
            cursor = end
        tail = "".join(lines[cursor:]).strip()
        if tail:
            doc.add_text(label=DocItemLabel.TEXT, text=tail)
        chunks = []
        for item in self.hybrid.chunk(dl_doc=doc):
            # Contextualization repeats headings, but never generates facts.
            value = self.hybrid.contextualize(chunk=item)
            if value.strip():
                chunks.append(Chunk(len(chunks), value, self.count(value), list(item.meta.headings or [])))
        # A page containing only a heading still has observable source content.
        if not chunks and text.strip():
            chunks = [Chunk(0, text.strip(), self.count(text.strip()), [])]
        return chunks

    def bundles(self, chunks: list[Chunk], limit: int, overlap: int) -> list[dict]:
        bundles, start = [], 0
        while start < len(chunks):
            end = start
            while end < len(chunks):
                text = "\n\n".join(c.text for c in chunks[start:end + 1])
                if self.count(text) > limit:
                    break
                end += 1
            if end == start:
                raise ValueError("A Docling chunk exceeds the bundle token budget")
            text = "\n\n".join(c.text for c in chunks[start:end])
            bundles.append({"id": len(bundles), "chunk_ids": list(range(start, end)),
                            "text": text, "tokens": self.count(text)})
            if end == len(chunks):
                break
            start = max(start + 1, end - overlap)
        return bundles
