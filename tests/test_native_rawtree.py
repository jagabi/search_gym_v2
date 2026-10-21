"""Offline backend download -> native library -> Docling -> d3 selection tests."""
import io
import unittest
from unittest.mock import AsyncMock, patch

import httpx

from searchgym.tools import WebTools
from searchgym.tools.native import decode_document
from searchgym.rawtree import RawTree
from test_rawtree import Capture, chunker
from test_rawtree_navigation import Decision
from test_rawtree_policy import config


def pdf_bytes():
    from pypdf import PdfWriter
    from pypdf.annotations import Link
    from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
    book = PdfWriter()
    font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
                             NameObject('/Subtype'): NameObject('/Type1'),
                             NameObject('/BaseFont'): NameObject('/Helvetica')})
    for text in ('Opening page with unrelated material. ' * 20, 'TAIL_EVIDENCE 174'):
        page = book.add_blank_page(width=600, height=800)
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Font'): DictionaryObject({NameObject('/F1'): font})})
        stream = DecodedStreamObject()
        stream.set_data(f'BT /F1 12 Tf 50 700 Td ({text}) Tj ET'.encode())
        page[NameObject('/Contents')] = stream
    book.add_annotation(page_number=1, annotation=Link(
        rect=(10, 10, 100, 30), url='https://example.org/record'))
    out = io.BytesIO(); book.write(out)
    return out.getvalue()


class NativeRawTests(unittest.IsolatedAsyncioTestCase):
    async def run_file(self, kind, payload):
        url = f'https://example.org/source.{kind}?download=1'
        seen = []
        def respond(request):
            seen.append(str(request.url))
            return httpx.Response(200, content=payload, headers={
                'content-type': 'application/pdf' if kind == 'pdf' else 'text/csv'})
        client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        tools = WebTools()
        tools.call = AsyncMock(side_effect=AssertionError('MCP fetch must not be used'))
        tools._fetch_engine = AsyncMock(side_effect=AssertionError('Jina must not be used'))
        def score(state, key, ctx):
            if ctx['phase'] == 'chunk':
                return .95 if 'TAIL_EVIDENCE' in state['target_chunk'] else .01
            return .1 if key == 'return_now' else .9
        decision, trace = Decision(score), Capture()
        cfg = config(jev_traversal='beam', jev_depth=1, jev_entries=1,
                     jev_reads=1, jev_direct_reads=1, jev_query_reads=0,
                     jev_page_tokens=20, jev_chunk_tokens=64)
        try:
            with patch('httpx.AsyncClient', return_value=client):
                _, text, stats = await RawTree(decision, cfg, tools.fetch).run_search(
                    'Find tail evidence', [{'link': url}], question='Which value?',
                    trace=trace, usage=None)
            self.assertEqual(seen, [url])
            tools.call.assert_not_awaited(); tools._fetch_engine.assert_not_awaited()
            self.assertEqual(stats['native_fetches'], 1)
            self.assertEqual(stats['browser_fetches'], 0)
            self.assertEqual(stats['reads'], 1)
            self.assertIn('TAIL_EVIDENCE', text)
            self.assertTrue(any(ctx['phase'] == 'bundle' for _, _, ctx in decision.calls))
            return text, trace, decision
        finally:
            await client.aclose()

    async def test_pdf_tail_page_passes_through_existing_chunk_selection(self):
        text, _, _ = await self.run_file('pdf', pdf_bytes())
        self.assertIn('[PDF page 2]', text)
        self.assertIn('https://example.org/record', text)

    async def test_csv_tail_rows_retain_columns_in_d3_input_and_output(self):
        payload = ('Entity,Count,Note\n' + ''.join(
            f'entity{i},{i},ordinary\n' for i in range(80)) +
            'TAIL_EVIDENCE,0,"quoted, value"\n').encode()
        text, _, decision = await self.run_file('csv', payload)
        self.assertIn('Entity,Count,Note', text)
        self.assertIn('TAIL_EVIDENCE,0,"quoted, value"', text)
        chunks = [state['target_chunk'] for state, _, ctx in decision.calls if ctx['phase'] == 'chunk']
        self.assertTrue(all('Entity,Count,Note' in c for c in chunks if 'entity' in c or 'TAIL_EVIDENCE' in c))

    async def test_native_origin_failure_does_not_retry_or_call_mcp_or_jina(self):
        seen = []
        def respond(request):
            seen.append(request)
            return httpx.Response(503, text='Unavailable')
        client = httpx.AsyncClient(transport=httpx.MockTransport(respond))
        tools = WebTools(); tools.call = AsyncMock(); tools._fetch_engine = AsyncMock()
        try:
            with patch('httpx.AsyncClient', return_value=client):
                doc = await tools.fetch('https://example.org/source.pdf', engine='browser')
            self.assertTrue(doc.is_error)
            self.assertEqual(len(seen), 1)
            self.assertEqual(doc.reader_metadata['source_http_status'], 503)
            self.assertEqual(doc.reader_metadata['failure_stage'], 'native_http')
            tools.call.assert_not_awaited(); tools._fetch_engine.assert_not_awaited()
        finally:
            await client.aclose()

    def test_csv_chunking_preserves_multiline_cells_empty_values_and_tail(self):
        text = decode_document(b'Entity,Count,Note\n"A, B",0,"line one\nline two"\nC,,tail\n',
                               'csv', 'https://example.org/source.csv')
        c = chunker(64)
        chunks = c.chunks(text)
        joined = '\n'.join(x.text for x in chunks)
        for value in ['Entity,Count,Note', '"A, B",0,"line one\nline two"', 'C,,tail']:
            self.assertIn(value, joined)
        self.assertTrue(all(x.tokens <= 64 for x in chunks))
