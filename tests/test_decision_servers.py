"""--decision pplx | d3-mini | d3-flash: self-hosted servers and the startup identity check."""
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


if __name__ == '__main__':
    unittest.main()
