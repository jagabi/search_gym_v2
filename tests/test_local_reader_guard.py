"""Local Jina startup guards; no network or model requests."""
import json
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from searchgym.local_reader import local_reader_url, probe_local_reader
from searchgym.tools import ToolResult, WebTools


LOCAL = "http://100.111.87.95:3001"
READY = {"ready": True, "jina_base_url": LOCAL, "jina_rpm": 0,
         "jina_max_concurrent": 50, "verified_by": "fetch_server"}


class ReaderProbeTests(unittest.TestCase):
    def test_missing_hosted_public_and_credential_urls_are_blocked(self):
        for url in ("", "https://r.jina.ai", "https://8.8.8.8", "http://0.0.0.0:3001",
                    "http://user:pass@127.0.0.1:3001", "http://127.0.0.1:bad",
                    "ftp://127.0.0.1", "http://127.0.0.1?forward=r.jina.ai"):
            with self.subTest(url=url), self.assertRaises(RuntimeError):
                local_reader_url(url)

    def test_loopback_lan_and_tailscale_are_allowed(self):
        for url in (LOCAL, "http://localhost:3001", "http://127.0.0.1:3001",
                    "http://192.168.0.3:8081", "http://[::1]:3001"):
            self.assertEqual(local_reader_url(url + "/"), url)

    def test_disconnected_reader_aborts_and_closes_connection(self):
        conn = Mock()
        conn.request.side_effect = ConnectionRefusedError("reader stopped")
        with patch("searchgym.local_reader.http.client.HTTPConnection", return_value=conn):
            with self.assertRaisesRegex(RuntimeError, "Run blocked"):
                probe_local_reader(LOCAL)
        conn.close.assert_called_once()

    def test_redirects_errors_and_non_jina_services_are_not_ready(self):
        for status, body in ((302, b""), (503, b""), (200, b"not JSON"),
                             (200, b'{"code":200,"data":{}}'), (200, b"[]")):
            conn = Mock()
            conn.getresponse.return_value = SimpleNamespace(status=status, read=lambda _: body)
            with self.subTest(status=status, body=body):
                with patch("searchgym.local_reader.http.client.HTTPConnection", return_value=conn):
                    with self.assertRaises(RuntimeError):
                        probe_local_reader(LOCAL)
                conn.request.assert_called_once()  # No redirect or retry.

    def test_healthy_reader_checks_metadata_without_fetching_a_website(self):
        conn = Mock()
        body = b'{"code":200,"data":{"homepage":"https://jina.ai/reader"}}'
        conn.getresponse.return_value = SimpleNamespace(status=200, read=lambda _: body)
        with patch("searchgym.local_reader.http.client.HTTPConnection", return_value=conn):
            probe_local_reader(LOCAL)
        conn.request.assert_called_once_with("GET", "/", headers={"Accept": "application/json"})

    def test_fetch_server_refuses_public_endpoint_without_request(self):
        from searchgym.tools import server
        with patch.object(server, "JINA_BASE_URL", "https://r.jina.ai"), patch.object(server, "_request") as request:
            with self.assertRaisesRegex(RuntimeError, "Local Jina is required"):
                server.fetch("https://example.com")
            request.assert_not_called()

    def test_lds_logs_verified_server_settings_not_parent_environment(self):
        from searchgym.lds import LDSRecord
        tree = SimpleNamespace(entries=5, reader_budgets={}, depth=6, branch=5,
                               fetch_budget=40, reader_status=READY)
        with patch.dict("os.environ", {"JINA_BASE_URL": "https://r.jina.ai", "JINA_RPM": "18"}):
            record = LDSRecord(tree, SimpleNamespace(url="search: test"),
                               SimpleNamespace(), {}, "search-id")
        self.assertEqual(record.config["jina_base_url"], LOCAL)
        self.assertEqual(record.config["jina_rpm"], 0)
        self.assertEqual(record.config["jina_verified_by"], "fetch_server")


class ClientGuardTests(unittest.IsolatedAsyncioTestCase):
    async def test_server_errors_unready_or_hosted_status_abort(self):
        for reply in (ToolResult("offline", is_error=True), ToolResult("bad JSON"),
                      ToolResult(json.dumps({**READY, "ready": False})),
                      ToolResult(json.dumps({**READY, "jina_base_url": "https://r.jina.ai"}))):
            tools = WebTools()
            tools.call = AsyncMock(return_value=reply)
            with self.assertRaises(RuntimeError):
                await tools._check_local_reader()
            self.assertEqual(tools.reader_status, {})

    async def test_remote_server_settings_are_authoritative(self):
        tools = WebTools()
        tools.call = AsyncMock(return_value=ToolResult(json.dumps(READY)))
        with patch.dict("os.environ", {"JINA_BASE_URL": "https://r.jina.ai"}):
            await tools._check_local_reader()
        self.assertEqual(tools.reader_status, READY)
        tools.call.assert_awaited_once_with("local_reader_status", {})

    async def session(self, names, reply):
        tools = WebTools(url="http://mcp.test/mcp")
        session = AsyncMock()
        session.list_tools.return_value = SimpleNamespace(tools=[
            SimpleNamespace(name=n, description="", inputSchema={}) for n in names])
        session.call_tool.return_value = SimpleNamespace(
            content=[SimpleNamespace(text=json.dumps(reply))], isError=False)
        transport = AsyncMock()
        transport.__aenter__.return_value = (None, None)
        context = AsyncMock()
        context.__aenter__.return_value = session
        return tools, session, transport, context

    async def test_old_mcp_server_is_rejected_before_any_tool_or_model_call(self):
        tools, session, transport, context = await self.session(["web_search", "web_fetch"], READY)
        with patch("searchgym.tools.streamable_http_client", return_value=transport), \
                patch("searchgym.tools.ClientSession", return_value=context):
            with self.assertRaisesRegex(RuntimeError, "Update/restart"):
                async with tools:
                    self.fail("benchmark body must not start")
        session.call_tool.assert_not_awaited()
        context.__aexit__.assert_awaited_once()

    async def test_failed_preflight_prevents_entering_benchmark(self):
        tools, session, transport, context = await self.session(
            ["web_search", "web_fetch", "local_reader_status"], {**READY, "ready": False})
        with patch("searchgym.tools.streamable_http_client", return_value=transport), \
                patch("searchgym.tools.ClientSession", return_value=context):
            with self.assertRaises(RuntimeError):
                async with tools:
                    self.fail("benchmark body must not start")
        session.call_tool.assert_awaited_once_with("local_reader_status", {})

    async def test_preflight_is_hidden_from_model_tools(self):
        tools, session, transport, context = await self.session(
            ["web_search", "web_fetch", "local_reader_status"], READY)
        with patch("searchgym.tools.streamable_http_client", return_value=transport), \
                patch("searchgym.tools.ClientSession", return_value=context):
            async with tools:
                self.assertEqual([s.name for s in tools.specs], ["web_search", "web_fetch"])
                self.assertEqual(tools.reader_status, READY)


if __name__ == "__main__":
    unittest.main()
