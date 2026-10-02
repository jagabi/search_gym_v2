import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx

from searchgym.agent import RunResult, SearchAgent
from searchgym.explorer import Document
from searchgym.jevtree import Jev, JevTree, JevUsage
from searchgym.llm import Usage
from searchgym.trace import Trace, ToolCall


class JevLoggingTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.trace = Trace(Path(self.tmp.name) / "trace.jsonl", "test")
        with patch.dict("os.environ", {"TYPESAFE_API_KEY": "test-secret-not-for-logs"}):
            self.jev = Jev("jev-test")
        await self.jev._http.aclose()
        self.addAsyncCleanup(self.jev.aclose)

    def transport(self, handler):
        self.jev._http = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    def events(self, trace=None):
        return [json.loads(line) for line in (trace or self.trace).path.read_text(
            encoding="utf-8").splitlines()]

    def tree(self, fetch, **overrides):
        async def cap(text, _limit):
            return text, False

        config = dict(jev=self.jev, llm=SimpleNamespace(cap=cap), fetch=fetch,
                      reader_prompt="read", reader_max_tokens=100, entries=1,
                      branch=1, depth=2, reads=0, floor=.15,
                      jev_page_tokens=20000, visited=set())
        config.update(overrides)
        return JevTree(**config)

    async def test_full_payload_and_all_link_scores_across_chunks(self):
        received = []

        def handler(request):
            body = json.loads(request.content)
            received.append(body)
            answers = {key: {"noul": .9 if key in ("result_0", "link_100") else .2}
                       for key in body["questions"]}
            return httpx.Response(200, json={"answers": answers,
                                           "usage": {"input_tokens": len(answers)},
                                           "extra": {"preserve": "unparsed server metadata"}})

        self.transport(handler)
        root = "https://example.org/root"
        page = "Full page text\n" + "\n".join(
            f"[Anchor {i}](https://example.org/child/{i})" for i in range(101))

        async def fetch(url):
            return Document(url=url, content=page if url == root else "child evidence")

        log, _, stats = await self.tree(fetch).run_search(
            "query", [{"link": root, "title": "Title", "snippet": "Full snippet"}],
            question="Original question", main_reasoning="Current hypothesis",
            trace=self.trace, usage=Usage())
        events = self.events()
        requests = [e for e in events if e["event"] == "jev.request"]
        responses = [e for e in events if e["event"] == "jev.response"]
        self.assertEqual([e["body"] for e in requests], received)
        for body in received:
            self.assertNotIn("main_reasoning", body["state"])
            self.assertNotIn("main_reasoning", json.dumps(body["questions"]))
            self.assertNotIn("Current hypothesis", json.dumps(body))
            self.assertEqual(body["state"]["question"], "Original question")
        self.assertEqual(len(requests), 4)  # entry + two link chunks + child
        self.assertEqual(len({e["request_id"] for e in requests}), 4)
        self.assertEqual({e["request_id"] for e in requests},
                         {e["request_id"] for e in responses})
        root_requests = [e for e in requests if e["body"]["state"].get("page_url") == root]
        self.assertEqual([len(e["body"]["questions"]) for e in root_requests], [101, 1])
        self.assertTrue(all(e["body"]["state"]["page_text"] == page for e in root_requests))
        self.assertEqual([e["context"]["chunk_index"] for e in root_requests], [0, 1])
        self.assertTrue(all(e["context"]["search_id"] == log["search_id"] for e in requests))
        self.assertTrue(all(json.loads(e["response_text"])["extra"]["preserve"]
                            == "unparsed server metadata" for e in responses))
        scored = next(e for e in events if e["event"] == "jevtree.scored" and e["url"] == root)
        self.assertEqual(len(scored["link_scores"]), 101)
        self.assertEqual(scored["link_scores"][100], {
            "id": "link_100", "url": "https://example.org/child/100",
            "anchor": "Anchor 100", "score": .9})
        self.assertEqual(log["opened"][0]["opened"][0]["urls"], ["https://example.org/child/100"])
        self.assertEqual((stats["jev_requests"], stats["jev_attempts"],
                          stats["jev_input_tokens"], stats["jev_failures"]), (4, 4, 104, 0))
        self.assertNotIn("test-secret-not-for-logs", self.trace.path.read_text(encoding="utf-8"))

    async def test_concurrent_agent_searches_keep_usage_local(self):
        ready = asyncio.Event()
        arrivals = 0

        async def handler(request):
            nonlocal arrivals
            body = json.loads(request.content)
            arrivals += 1
            if arrivals == 2:
                ready.set()
            await asyncio.wait_for(ready.wait(), timeout=2)
            tokens = 11 if body["state"]["question"] == "A" else 29
            return httpx.Response(200, json={"answers": {"result_0": {"noul": .01}},
                                           "usage": {"input_tokens": tokens}})

        self.transport(handler)
        agent = object.__new__(SearchAgent)

        async def run(question):
            result = RunResult()
            trace = Trace(Path(self.tmp.name) / f"{question}.jsonl", question)
            fetch = AsyncMock(side_effect=AssertionError("Below-floor entry must not be fetched"))
            await agent._jev_reading(
                self.tree(fetch), "query", {"organic": [{"link": "https://example.org/root"}]},
                result, ToolCall("web_search"), trace, question, "hypothesis")
            return result.reader_stats, trace

        (a, ta), (b, tb) = await asyncio.gather(run("A"), run("B"))
        for stats, tokens in [(a, 11), (b, 29)]:
            self.assertEqual(stats["jev_requests"], 1)
            self.assertEqual(stats["jev_attempts"], 1)
            self.assertEqual(stats["jev_input_tokens"], tokens)
            self.assertEqual(stats["jev_failures"], 0)
        ids_a = {e["request_id"] for e in self.events(ta) if "request_id" in e}
        ids_b = {e["request_id"] for e in self.events(tb) if "request_id" in e}
        self.assertTrue(ids_a.isdisjoint(ids_b))

    async def test_retry_preserves_full_error_and_success_bodies(self):
        error_body = "rate limited: " + "x" * 2000
        replies = [httpx.Response(429, text=error_body),
                   httpx.Response(200, json={"answers": {"check": {"noul": .75}},
                                            "usage": {"input_tokens": 23}})]
        self.transport(lambda request: replies.pop(0))
        usage = JevUsage()
        with patch("searchgym.jevtree.asyncio.sleep", new_callable=AsyncMock):
            scores = await self.jev.noul({"page_text": "body"}, {"check": {"type": "noul"}},
                                         self.trace, usage=usage)
        events = self.events()
        self.assertEqual(scores, {"check": .75})
        responses = [e for e in events if e["event"] == "jev.response"]
        self.assertEqual([e["status_code"] for e in responses], [429, 200])
        self.assertEqual(responses[0]["response_text"], error_body)
        self.assertEqual(len({e["request_id"] for e in events}), 1)
        self.assertTrue(all(e["duration_ms"] >= 0 for e in responses))
        self.assertEqual((usage.calls, usage.attempts, usage.input_tokens, usage.failures), (1, 2, 23, 0))

    async def test_transport_and_invalid_json_failures_are_logged(self):
        calls = 0

        def handler(request):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise httpx.ReadTimeout("timed out", request=request)
            return httpx.Response(200, text="invalid json " + "z" * 1000)

        self.transport(handler)
        usage = JevUsage()
        with patch("searchgym.jevtree.asyncio.sleep", new_callable=AsyncMock):
            scores = await self.jev.noul({}, {}, self.trace, usage=usage)
        events = self.events()
        self.assertEqual(scores, {})
        self.assertEqual(sum(e["event"] == "jev.error" for e in events), 3)
        self.assertEqual(sum(e["event"] == "jev.response" for e in events), 2)
        self.assertEqual((usage.calls, usage.attempts, usage.failures), (0, 3, 1))
        self.assertTrue(events[-1]["failed"])


if __name__ == "__main__":
    unittest.main()
