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

    def test_runpod_proxy_is_allowed_only_as_https_pod_address(self):
        pod = "https://aoj0o49uwd2v1g-8081.proxy.runpod.net"
        self.assertEqual(local_reader_url(pod + "/"), pod)
        for url in ("http://aoj0o49uwd2v1g-8081.proxy.runpod.net", "https://proxy.runpod.net",
                    "https://.proxy.runpod.net", "https://x.proxy.runpod.net.evil.com",
                    "https://x.proxy.runpod.net:8443", "https://u:p@x.proxy.runpod.net"):
            with self.subTest(url=url), self.assertRaises(RuntimeError):
                local_reader_url(url)

    def test_fetch_sends_runpod_target_in_body_and_keeps_local_get(self):
        from searchgym.tools import server
        target = "https://en.wikipedia.org/w/index.php?title=X&action=history"
        with patch.object(server, "JINA_BASE_URL", "https://pod-8081.proxy.runpod.net"), \
                patch.object(server, "_request", return_value="Title: X") as request:
            server.fetch(target)
        host, method, path, headers, body = request.call_args.args
        self.assertEqual((host, method, path), ("pod-8081.proxy.runpod.net", "POST", "/"))
        self.assertEqual(json.loads(body), {"url": target})
        self.assertEqual(headers["Content-Type"], "application/json")
        with patch.object(server, "JINA_BASE_URL", LOCAL), \
                patch.object(server, "_request", return_value="Title: X") as request:
            server.fetch(target)
        host, method, path, headers, body = request.call_args.args
        self.assertEqual((host, method, path, body), ("100.111.87.95:3001", "GET", "/" + target, None))
        self.assertNotIn("Content-Type", headers)

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

    async def test_engine_fetch_posts_to_runpod_and_gets_from_local(self):
        url = "https://en.wikipedia.org/wiki/X"
        payload = {"code": 200, "data": {"title": "X", "content": "body", "url": url}}
        for base, verb in (("https://pod-8081.proxy.runpod.net", "post"), (LOCAL, "get")):
            tools = WebTools()
            tools.reader_status = {**READY, "jina_base_url": base}
            response = Mock(status_code=200, headers={"content-type": "application/json"},
                            json=Mock(return_value=payload), text=json.dumps(payload),
                            content=json.dumps(payload).encode())
            tools._reader_http = SimpleNamespace(get=AsyncMock(return_value=response),
                                                 post=AsyncMock(return_value=response))
            with self.subTest(base=base):
                try:
                    await tools._fetch_engine(url, "curl")
                except Exception:
                    pass  # Only the transport form is under test here.
                called = getattr(tools._reader_http, verb)
                other = tools._reader_http.get if verb == "post" else tools._reader_http.post
                called.assert_awaited_once()
                other.assert_not_awaited()
                if verb == "post":
                    self.assertEqual(called.await_args.args, (base + "/",))
                    self.assertEqual(called.await_args.kwargs["json"], {"url": url})
                else:
                    self.assertEqual(called.await_args.args, (f"{base}/{url}",))

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
