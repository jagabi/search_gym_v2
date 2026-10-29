"""Offline regressions for search-o1-decision: read every result, score every bundle, return top n."""
import unittest

from searchgym.config import load_test
from searchgym.explorer import Document
from searchgym.raw_policy import raw_policy
from searchgym.rawtree import RawTree
from test_rawtree import Capture
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config


def flat(**options):
    values = dict(jev_traversal='flat', jev_entries=4, jev_depth=1, jev_fetch_budget=4,
                  jev_floor=0.0, jev_top_n=2, jev_bundle_tokens=160, jev_page_tokens=4096,
                  jev_output_tokens=3000, jev_notice_tokens=500, jev_search_results=True,
                  jev_document_tree=False)
    values.update(options)
    return config(**values)


class FlatReadingTests(unittest.IsolatedAsyncioTestCase):
    async def run_search(self, bodies, **options):
        fetched = []

        async def fetch(url, *, engine):
            name = url.removeprefix(BASE)
            fetched.append(name)
            return Document(url, bodies[name], title='T ' + name)

        def score(state, key, ctx):
            text = state['page_text']
            return .9 if 'BEST' in text else .5 if 'GOOD' in text else .05

        decision = Decision(score)
        trace = Capture()
        tree = RawTree(decision, flat(**options), fetch)
        results = [{'link': BASE+name, 'title': 'Result '+name, 'snippet': 'snip '+name} for name in bodies]
        _, text, stats = await tree.run_search('q', results, question='original', trace=trace, usage=None)
        return decision, trace, fetched, text, stats

    async def test_every_result_read_every_bundle_scored_top_n_returned(self):
        filler = ' '.join(f'word{i}' for i in range(300))
        bodies = {'a': 'GOOD fact. ' + filler + ' [Link](' + BASE + 'never)',
                  'b': filler + ' BEST fact.',
                  'c': 'weak text only. ' + filler,
                  'd': 'GOOD other fact.'}
        decision, trace, fetched, text, stats = await self.run_search(bodies)
        self.assertEqual(sorted(fetched), ['a', 'b', 'c', 'd'])        # no gate, no links
        phases = {c['phase'] for _, _, c in decision.calls}
        self.assertEqual(phases, {'bundle'})                          # no preview, region or link calls
        self.assertTrue(all(set(q) == {'evidence_value'} for _, q, _ in decision.calls))
        bundles = [e for e in trace.events if e['event'] == 'rawtree.bundles']
        self.assertEqual(sum(len(e['bundles']) for e in bundles), sum(1 for _ in decision.calls))
        self.assertGreater(len(decision.calls), 4)                     # long pages give several bundles
        self.assertEqual(stats['bundles_returned'], 2)                 # top n
        self.assertIn('BEST fact', text)
        self.assertNotIn('weak text only', text.partition('Excerpts from the pages read')[2])
        self.assertIn('read in full; its passages ranked below the top excerpts.', text)
        scored = ' '.join(s['page_text'] for s, _, _ in decision.calls)
        self.assertNotIn(BASE + 'never', scored)                     # link destinations are not scored
        self.assertIn('Link', scored)                                 # its label stays

    def test_strip_links_keeps_labels_and_drops_images(self):
        from searchgym.jevtree_input import strip_links
        page = ('See [Ten Words](https://en.wikipedia.org/wiki/China_(book)) and '
                '[![Image 1](https://img.example/a.jpg)](https://example.org/x) photo. '
                '![Image 2: cover](https://img.example/b.png) Bare https://example.org/cite stays.')
        self.assertEqual(strip_links(page), 'See Ten Words and  photo.  Bare https://example.org/cite stays.')

    async def test_top_zero_keeps_every_bundle_within_budget(self):
        bodies = {'a': 'GOOD one.', 'b': 'BEST two.', 'c': 'GOOD three.'}
        _, _, _, _, stats = await self.run_search(bodies, jev_top_n=0, jev_entries=3, jev_fetch_budget=3)
        self.assertEqual(stats['bundles_returned'], 3)


class FlatConfigTests(unittest.TestCase):
    def test_method_config_selects_flat_reading(self):
        cfg = load_test(method='search-o1-decision')
        a = cfg.agent
        self.assertEqual((a.jev_traversal, a.jev_depth, a.jev_top_n, a.jev_document_tree), ('flat', 1, 4, False))
        policy = raw_policy(a, cfg.method)
        self.assertEqual(policy['traversal'], 'flat')
        self.assertIsNone(policy['branch_control'])
        self.assertEqual(policy['flat_reading']['pages'], 'all_search_results')
        self.assertIn('open every result page', cfg.system_prompt)
        self.assertNotIn('Birthplace', cfg.system_prompt)              # no tuned research rules
        self.assertFalse(a.jev_search_followup)
        self.assertFalse(policy['search_followup_notice'])

    def test_flat_belongs_only_to_search_o1_decision(self):
        with self.assertRaises(ValueError):
            load_test(method='jevtree', raw_traversal='flat')


if __name__ == '__main__':
    unittest.main()
