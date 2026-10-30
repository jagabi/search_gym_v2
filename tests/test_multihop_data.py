"""MuSiQue (2/3/4-hop x 100) and Bamboogle (125) test sets and alias-aware judging."""
import json
import unittest
from collections import Counter

from searchgym.benchmarks import load_benchmark
from searchgym.paths import PROJECT_ROOT


class MultihopDataTests(unittest.TestCase):
    def test_musique_is_stratified_by_hop_and_reproducible(self):
        items = load_benchmark('musique').load()
        self.assertEqual(Counter(i.category for i in items), {'2hop': 100, '3hop': 100, '4hop': 100})
        self.assertEqual(len({i.index for i in items}), 300)
        meta = json.loads((PROJECT_ROOT / 'data' / 'musique' / 'sample_meta.json').read_text(encoding='utf-8'))
        self.assertEqual(sorted(meta['selected_indices']), sorted(i.index for i in items))
        self.assertEqual(meta['seed'], 0)

    def test_bamboogle_uses_every_question(self):
        self.assertEqual(len(load_benchmark('bamboogle').load()), 125)

    def test_aliases_reach_the_judge_only_when_present(self):
        items = load_benchmark('musique').load()
        aliased = next(i for i in items if i.answer_aliases)
        prompt = load_benchmark('musique').judge_prompt(aliased, 'response')
        self.assertIn('Also accepted as the same answer: ' + aliased.answer_aliases[0], prompt)
        plain = load_benchmark('browsecomp').load(limit=1)[0]
        self.assertNotIn('Also accepted', load_benchmark('browsecomp').judge_prompt(plain, 'response'))


if __name__ == '__main__':
    unittest.main()
