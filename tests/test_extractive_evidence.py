"""Source integrity across paragraph selection, recursive returns and cache boundaries."""
import json
import unittest
from dataclasses import asdict, replace

from searchgym.explorer import (Explorer, ExplorerConfig, Budget, Document,
    _label_paragraphs, _paragraph_ids, _passage_note, _render_notes, _relation_overview)
from searchgym.llm import Reply, Usage
from searchgym.runner import _explorer_fingerprint
from test_reader_integrity import FakeLLM, MemoryTrace, note


class PassageTests(unittest.IsolatedAsyncioTestCase):
    def test_labels_preserve_table_blocks_and_original_characters(self):
        source = 'Title\n\n| City | Count |\n| --- | --- |\n| A | 42 |\n\nCafé\u2028verbatim'
        labeled, blocks = _label_paragraphs(source)
        self.assertEqual(blocks[1], '| City | Count |\n| --- | --- |\n| A | 42 |')
        self.assertIn('[P3]\nCafé\u2028verbatim', labeled)

    def test_ranges_are_bounded_and_references_deduplicated(self):
        ids, invalid = _paragraph_ids('[P2] P2-P4 [P5‑P6] [P0] P9-P99999999999999 P8-P7', 9)
        self.assertEqual(ids, [2, 3, 4, 5, 6])
        self.assertEqual(len(invalid), 3)

    async def test_only_evidence_ids_select_source_and_generated_facts_are_discarded(self):
        result = await _passage_note(
            '**Evidence:** Invented year 1900 [P2] [P999]\n**Connections:** invented relationship\n'
            '**Missing:** P1 is a hypothesis\n**Next links:** https://source.test/next | check date',
            ['UNSELECTED', 'Actual year 1840'], ['https://source.test'],
            'partial', 'complete', FakeLLM([]), 8192)
        rendered = _render_notes([result])
        self.assertEqual(result['source_evidence'], '[P2]\nActual year 1840')
        self.assertNotIn('1900', rendered)
        self.assertNotIn('invented relationship', rendered)
        self.assertNotIn('UNSELECTED', rendered)
        self.assertEqual(_relation_overview([result]), '')
        self.assertIn('Invalid paragraph', result['source_notice'])

    async def test_missing_or_invalid_evidence_cannot_claim_answered(self):
        for text in ('**Evidence:** none', '**Evidence:** [P7]', 'Unsupported answer'):
            result = await _passage_note(text, ['real source'], ['https://a.test'],
                                        'answered', 'complete', FakeLLM([]), 8192)
            self.assertEqual(result['status'], 'not_found')
            self.assertFalse(result['source_evidence'])
            self.assertIn('does not establish absence', result['source_notice'])

    async def test_excerpts_use_existing_return_limit_and_mark_truncation(self):
        result = await _passage_note('**Evidence:** [P1]', ['x' * 1000], ['https://a.test'],
                                    'partial', 'complete', FakeLLM([]), 20)
        self.assertLessEqual(len(result['source_evidence']), 60)
        self.assertTrue(result['evidence_truncated'])
        self.assertIn('truncated', result['source_notice'])

    async def test_recursive_source_passages_reach_parent_without_rewriting(self):
        root, child = 'https://a.test/root', 'https://a.test/child'
        llm = FakeLLM([note(f'**Evidence:** [P1]\n**Next links:** {child} | missing date\n**Expand:** yes'),
                       note('**Evidence:** [P1]\n**Expand:** no'), Reply(text='DONE')])
        async def fetch(url):
            self.assertEqual(url, child)
            return Document(url, 'CHILD date 1840')
        cfg = ExplorerConfig(max_depth=3, max_expansion_nodes=12, max_subtree_children=2,
            max_turns=6, isolate_extraction_context=True, prune_unhelpful_branches=True,
            extractive_evidence=True)
        explorer = Explorer(llm, cfg, 'Select source IDs.', fetch, relational_reading=True)
        budget, trace = Budget(12), MemoryTrace()
        result = await explorer.explore(question='Find date and place.', reasoning='PARENT GUESS 1900',
            query='wrong year', documents=[Document(root, f'ROOT place London [register]({child})')],
            budget=budget, trace=trace, usage=Usage())
        self.assertIsNone(result.error)
        self.assertEqual((result.nodes, budget.used, result.depth_reached), (1, 1, 2))
        self.assertEqual(len(result.notes), 2)
        self.assertIn('CHILD date 1840', result.render_for_gate())
        self.assertIn(f'ROOT place London [register]({child})', result.notes[0]['source_evidence'])
        child_input = [e for k,e in trace.events if k=='explorer.extract_input' and e['depth']==2][0]
        self.assertNotIn('ROOT place', json.dumps(child_input['messages']))
        self.assertNotIn('PARENT GUESS', json.dumps(child_input['messages']))
        navigation = str(llm.requests[-1][0])
        self.assertIn('ROOT place London', navigation)
        self.assertIn('CHILD date 1840', navigation)
        self.assertFalse(llm.replies)
        self.assertEqual(len(llm.requests), 3)  # two extracts and parent continuation, no extra stage

    def test_baseline_cache_identity_unchanged_and_new_contract_isolated(self):
        cfg = ExplorerConfig()
        previous = asdict(cfg); previous.pop('extractive_evidence'); previous.pop('source_return')
        self.assertEqual(_explorer_fingerprint(cfg, 'search-o1'), json.dumps(previous, sort_keys=True))
        self.assertNotEqual(_explorer_fingerprint(cfg, 'depthsearch'),
                            _explorer_fingerprint(replace(cfg, extractive_evidence=True), 'depthsearch'))


if __name__ == '__main__':
    unittest.main()
