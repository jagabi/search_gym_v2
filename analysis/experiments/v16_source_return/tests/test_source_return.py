"""Navigation cannot suppress supplied evidence; no model call is needed at leaves."""
import unittest
from dataclasses import asdict
import json

from searchgym.explorer import Explorer, ExplorerConfig, Budget, Document
from searchgym.llm import Reply, Usage
from searchgym.runner import _explorer_fingerprint
from test_reader_integrity import FakeLLM, MemoryTrace, fetch_call


class SourceReturnTests(unittest.IsolatedAsyncioTestCase):
    async def read(self, replies, pages=None, **overrides):
        llm, trace, usage, budget = FakeLLM(replies), MemoryTrace(), Usage(), Budget(12)
        root, child = 'https://a.test/root', 'https://a.test/child'
        pages = pages or {root: f'ROOT candidate [register]({child})', child: 'CHILD date 1840'}
        async def fetch(url):
            return Document(url, pages[url])
        cfg = ExplorerConfig(**dict(dict(max_depth=2, max_subtree_children=2,
            max_expansion_nodes=12, max_turns=6, max_tokens=8192,
            source_return=True, prune_unhelpful_branches=True), **overrides))
        reader = Explorer(llm, cfg, 'Navigate or finish.', fetch,
                          relational_reading=True, preserve_source_evidence=True)
        result = await reader.explore(question='Find the date and place.', reasoning='PARENT GUESS',
            query='date', documents=[Document(root, pages[root])], budget=budget,
            trace=trace, usage=usage)
        return result, llm, trace, usage, budget

    async def test_navigation_declining_does_not_discard_candidate(self):
        result, llm, trace, usage, budget = await self.read([Reply(text='No match. DONE')])
        self.assertIn('ROOT candidate', result.render_for_gate())
        self.assertIn('relevance: unassessed', result.render_for_gate())
        self.assertNotIn('No match', result.render_for_gate())
        self.assertEqual(usage.calls, 1)
        self.assertEqual(budget.used, 0)
        self.assertFalse(any(k == 'explorer.extract_input' for k, _ in trace.events))

    async def test_leaf_zero_calls_then_parent_resumes_with_both_sources(self):
        result, llm, trace, usage, budget = await self.read([
            fetch_call('https://a.test/child'), Reply(text='DONE')])
        self.assertIsNone(result.error)
        self.assertEqual((result.nodes, budget.used, result.depth_reached), (1, 1, 2))
        self.assertEqual(usage.calls, 2)
        self.assertEqual(len(llm.requests), 2)
        self.assertIn('CHILD date 1840', str(llm.requests[-1][0]))
        self.assertIn('ROOT candidate', str(llm.requests[-1][0]))
        self.assertEqual(len(result.notes), 2)
        self.assertNotIn('PARENT GUESS', result.notes[1]['source_evidence'])
        self.assertIn('CHILD date 1840', result.render_for_gate())

    async def test_navigation_error_keeps_source(self):
        result, *_ = await self.read([RuntimeError('model failed')])
        self.assertIn('model failed', result.error)
        self.assertIn('ROOT candidate', result.render_for_gate())

    async def test_depth_limit_returns_verbatim_without_model(self):
        result, llm, _, usage, _ = await self.read([], max_depth=1)
        self.assertEqual(usage.calls, 0)
        self.assertFalse(llm.requests)
        self.assertIn('ROOT candidate', result.render_for_gate())

    async def test_source_limit_is_explicit_and_access_screens_are_not_evidence(self):
        root = 'https://a.test/root'
        result, *_ = await self.read([], {root: 'long source ' * 100}, max_depth=1, max_tokens=20)
        self.assertTrue(result.notes[0]['source_truncated'])
        self.assertLessEqual(len(result.notes[0]['source_evidence']), 60)
        self.assertIn('omitted content remains unknown', result.render_for_gate())
        blocked, _, _, usage, _ = await self.read([], {root:
            'Title: 18+ Access\nMarkdown Content:\n18+ only\nContinue to access'})
        self.assertEqual(usage.calls, 0)
        self.assertEqual(blocked.status, 'not_found')
        self.assertFalse(blocked.notes[0]['source_evidence'])

    def test_baseline_fingerprint_is_unchanged(self):
        cfg = ExplorerConfig()
        old = asdict(cfg)
        old.pop('source_return'); old.pop('extractive_evidence')
        self.assertEqual(_explorer_fingerprint(cfg, 'search-o1'), json.dumps(old, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
