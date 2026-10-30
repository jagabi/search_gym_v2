"""--decision pplx | d3-mini | d3-flash: self-hosted servers and the startup identity check."""
import json
import unittest
from unittest.mock import patch

import httpx

from searchgym.config import load_test
from searchgym.pplx_decision import DeciderDecision, decision_client, verify_decision_server
from searchgym.raw_policy import raw_policy
from searchgym.rawtree import LocalDecision


def server(models=None, models_status=200, probe=0.9):
    def respond(request):
        if request.method == 'GET' and request.url.path == '/v1/models':
            if models_status != 200:
                return httpx.Response(models_status, text='Internal Server Error')
            return httpx.Response(200, json={'data': [{'id': m} for m in models or []]})
        if request.method == 'POST' and request.url.path == '/v1/systemone':
            return httpx.Response(200, json={'answers': {'probe': {'type': 'noul', 'noul': probe}},
                                             'usage': {'input_tokens': 20}})
        return httpx.Response(500)
    return httpx.AsyncClient(transport=httpx.MockTransport(respond))


class DecisionOptionTests(unittest.TestCase):
    def test_options_select_the_expected_model(self):
        for option, model in (('d3-mini', 'vllm-sr/d3-mini'), ('d3-flash', 'vllm-sr/d3-flash'),
                              ('pplx', 'pplx-decider'), ('d3', 'vllm-sr/d3-mini')):
            a = load_test(method='search-o1-decision', decision_provider=option).agent
            self.assertEqual(a.jev_model, model)
            self.assertEqual(a.jev_tokenizer, 'vllm-sr/d3-mini')      # same bundles for every model
            policy = raw_policy(a, 'search-o1-decision')
            self.assertEqual(policy['decision_model'], model)
            self.assertNotIn('decision_limits', policy)                # no external API pacing
        with self.assertRaises(ValueError):
            load_test(method='search-o1-decision', decision_provider='gemini')

    def test_pplx_uses_the_self_hosted_decider_client(self):
        self.assertIsInstance(decision_client(load_test(method='jevtree', decision_provider='pplx').agent),
                              DeciderDecision)
        client = decision_client(load_test(method='jevtree', decision_provider='d3-flash').agent)
        self.assertIs(type(client), LocalDecision)
        self.assertTrue(client.endpoint.endswith('/v1/systemone'))


class IdentityCheckTests(unittest.IsolatedAsyncioTestCase):
    async def check(self, option, http):
        cfg = load_test(method='search-o1-decision', decision_provider=option).agent
        with patch('searchgym.rawtree.SourceChunker'), patch('searchgym.pplx_decision.SourceChunker'), \
                patch('searchgym.rawtree.httpx.AsyncClient', return_value=http):
            await verify_decision_server(cfg)

    async def test_d3_option_must_match_the_served_model(self):
        await self.check('d3-flash', server(['vllm-sr/d3-flash']))
        with self.assertRaisesRegex(RuntimeError, r'--decision d3-mini expects vllm-sr/d3-mini'):
            await self.check('d3-mini', server(['vllm-sr/d3-flash']))

    async def test_pplx_rejects_a_d3_server_and_requires_a_decision_answer(self):
        await self.check('pplx', server(models_status=500))           # decider exposes no model list
        with self.assertRaisesRegex(RuntimeError, 'reports d3 models'):
            await self.check('pplx', server(['vllm-sr/d3-mini']))
        with self.assertRaisesRegex(RuntimeError, 'invalid probe probability'):
            await self.check('pplx', server(models_status=500, probe=3.0))


class ParallelQuestionTests(unittest.IsolatedAsyncioTestCase):
    async def test_two_questions_share_one_agent_without_mixing(self):
        import asyncio
        from searchgym.agent import SearchAgent
        from searchgym.llm import Reply
        from searchgym.serving import profile_for
        from offline import FakeTools
        from test_depthsearch_core import call
        from test_rawtree import Capture
        from test_rawtree_navigation import Decision

        class LLM:
            profile = profile_for('gpt-oss')
            model_name = 'offline'

            async def chat(self, messages, *, max_tokens, tools=None, usage=None, tool_choice=None):
                question = next(m['content'] for m in messages if m['role'] == 'user')
                await asyncio.sleep(0.01)                    # interleave the two questions
                if not any(m['role'] == 'tool' for m in messages):
                    return call('web_search', {'query': question[:20]})
                return Reply(text='answer to ' + question)

            async def count_tokens(self, text):
                return len(text) // 3

            async def cap(self, text, limit):
                return text, False

        class Tools(FakeTools):
            async def fetch(self, url, engine=None):
                return await super().fetch(url)

        cfg = load_test(method='search-o1-decision', decision_provider='pplx')
        self.assertEqual(cfg.run.workers, 2)
        with patch('searchgym.agent.LLM', return_value=LLM()), \
                patch('searchgym.pplx_decision.DeciderDecision', return_value=Decision()):
            agent = SearchAgent(profile_for('gpt-oss'), cfg.agent, method='search-o1-decision',
                                explorer_config=cfg.explorer, explorer_prompt=cfg.explorer_prompt)
        tools, traces = Tools(), [Capture(), Capture()]
        results = await asyncio.gather(*(agent.run(q, cfg.system_prompt, tools, t)
                                         for q, t in zip(('Question one?', 'Question two?'), traces)))
        self.assertEqual([r.answer for r in results], ['answer to Question one?', 'answer to Question two?'])
        self.assertEqual([r.searches for r in results], [1, 1])
        for trace, query in zip(traces, ('Question one?', 'Question two?')):
            returns = [e for e in trace.events if e['event'] == 'rawtree.return']
            self.assertEqual(len(returns), 1)                # each trace holds only its own search
            self.assertIn(query[:12], json.dumps([e for e in trace.events if e['event'] == 'tool.call']))


if __name__ == '__main__':
    unittest.main()
