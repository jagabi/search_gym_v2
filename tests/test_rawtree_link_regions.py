"""Offline structural routing checks, not d3 accuracy or benchmark experiments."""
import asyncio
import unittest

from searchgym.explorer import Document
from searchgym.rawtree import LocalDecisionError, RawTree, link_state
from searchgym.jevtree_input import numbered_page
from test_rawtree import Capture, chunker
from test_rawtree_navigation import Decision
from test_rawtree_policy import BASE, config


class LinkRegionTests(unittest.IsolatedAsyncioTestCase):
    async def run_graph(self, bodies, *, region_score=None, link_score=None, **options):
        def score(state, key, ctx):
            if ctx['phase'] == 'link_region':
                return region_score(state, ctx) if region_score else .9
            if ctx['phase'] == 'links':
                return link_score(state, ctx) if link_score else .9
            if ctx['phase'] in ('bundle', 'chunk'):
                return .9
            if key in ('direct_answer', 'query_answer'):
                return .95 if 'FINAL_FACT' in state['page_text'] else .02
            return .99 if key == 'expand_now' else .01

        decision, trace, fetched = Decision(score), Capture(), []
        async def fetch(url, *, engine):
            fetched.append(url)
            return Document(url, bodies[url], title='Original title: '+url.removeprefix(BASE))
        settings = dict(jev_traversal='beam', jev_entries=1, jev_branch=2,
                        jev_frontier_width=2, jev_fetch_budget=10, jev_depth=3,
                        jev_reads=1, jev_direct_reads=1, jev_query_reads=0,
                        jev_page_tokens=32, jev_link_floor=.1)
        settings.update(options)
        result = await asyncio.wait_for(RawTree(decision, config(**settings), fetch).run_search(
            'Missing relation', [{'link': BASE+'root'}], question='Original question',
            main_reasoning='PRIVATE_REASONING_NOT_FOR_D3', trace=trace, usage=None), 5)
        self.assertTrue(all('PRIVATE_REASONING' not in str(state) for state, _, _ in decision.calls))
        return decision, trace, fetched, result

    async def test_only_selected_section_links_are_scored_even_beyond_prefix(self):
        body = '# Study\n\n' + 'Opening facts without the requested relation. '*30
        body += '\n\n## General navigation\n\n' + '\n'.join(
            f'[Item {i}]({BASE}menu{i})' for i in range(60))
        body += '\n\n## Supplementary materials\n\nLinked original appendix [Record]('+BASE+'appendix.pdf).'
        decision, trace, fetched, (_, text, stats) = await self.run_graph(
            {BASE+'root': body, BASE+'appendix.pdf': 'FINAL_FACT value 174.'},
            region_score=lambda state, ctx: .95 if 'Supplementary materials' in state['page_text'] else .01)
        self.assertEqual(fetched, [BASE+'root', BASE+'appendix.pdf'])
        self.assertEqual(stats['links_scored'], 1)
        self.assertEqual(stats['max_depth'], 2)
        self.assertIn('FINAL_FACT', text)
        links = [(s, q, c) for s, q, c in decision.calls if c['phase'] == 'links']
        self.assertEqual(len(links), 1)
        state = links[0][0]
        self.assertIn('Supplementary materials', state['section_path'])
        self.assertEqual(state['page_title'], 'Original title: root')
        self.assertNotIn('menu59', str(state['outgoing_links']))
        phases = [ctx['phase'] for _, _, ctx in decision.calls]
        self.assertLess(phases.index('link_region'), phases.index('links'))
        selections = [e for e in trace.events if e['event'] == 'rawtree.link_regions']
        self.assertEqual(len(selections[-1]['selected']), 1)

    async def test_navigation_menu_can_be_selected_when_d3_finds_a_route(self):
        _, _, fetched, _ = await self.run_graph({
            BASE+'root': '# Navigation\n\n[Archive]('+BASE+'archive)',
            BASE+'archive': 'FINAL_FACT original record.'})
        self.assertEqual(fetched, [BASE+'root', BASE+'archive'])

    async def test_parent_section_and_route_history_reach_the_child(self):
        decision, _, fetched, _ = await self.run_graph({
            BASE+'root': '# Study\n\n## Records\n\n[Identifying record]('+BASE+'bridge)',
            BASE+'bridge': '# Record\n\n## Supporting document\n\n[Appendix]('+BASE+'leaf)',
            BASE+'leaf': 'FINAL_FACT original appendix.'})
        self.assertEqual(fetched, [BASE+'root', BASE+'bridge', BASE+'leaf'])
        child_link = next(s for s, _, c in decision.calls
                          if c['phase'] == 'links' and s['page_url'] == BASE+'bridge')
        self.assertEqual([r['url'] for r in child_link['navigation_path']],
                         [BASE+'root', BASE+'bridge'])
        self.assertIn('Records', child_link['navigation_path'][-1]['incoming_section'])
        self.assertEqual(child_link['navigation_path'][-1]['incoming_anchor'], 'Identifying record')

    async def test_many_sections_use_bounded_hierarchical_selection(self):
        body = '\n\n'.join(f'## Section {i}\n\n[Record]({BASE}record{i})' for i in range(24))
        decision, _, fetched, (_, _, stats) = await self.run_graph(
            {BASE+'root': body, BASE+'record23': 'FINAL_FACT original source.'},
            region_score=lambda state, ctx: .9 if '## Section 23' in state['page_text'] else .01)
        self.assertEqual(fetched, [BASE+'root', BASE+'record23'])
        self.assertLess(stats['link_region_evaluations'], 24)
        self.assertEqual(stats['links_scored'], 1)

    async def test_leaf_limit_smaller_than_beam_still_terminates(self):
        body = '\n\n'.join(f'## Section {i}\n\n[Record]({BASE}record{i})' for i in range(8))
        _, _, fetched, _ = await self.run_graph(
            {BASE+'root': body, **{BASE+f'record{i}': 'FINAL_FACT original source.' for i in range(8)}},
            jev_leaf_bundles=1, jev_region_beam=2)
        self.assertEqual(len(fetched), 2)

    async def test_repeated_destination_keeps_best_section_context(self):
        body = '# First\n\n[One]('+BASE+'leaf)\n\n# Second\n\n[Two]('+BASE+'leaf)'
        decision, trace, fetched, _ = await self.run_graph(
            {BASE+'root': body, BASE+'leaf': 'FINAL_FACT original source.'},
            link_score=lambda state, ctx: .8 if 'Second' in state['section_path'] else .2)
        self.assertEqual(fetched, [BASE+'root', BASE+'leaf'])
        previews = [s for s, _, c in decision.calls if c['phase'] == 'preview' and s['page_url'] == BASE+'leaf']
        self.assertIn('Second', previews[0]['navigation_path'][-1]['incoming_section'])
        event = next(e for e in trace.events if e['event'] == 'rawtree.links')
        self.assertEqual(len({r['key'] for r in event['links']}), 2)

    async def test_unknown_region_is_reported_and_retained_inside_beam(self):
        def region(state, ctx):
            if state['section_range'] == [0, 1]:
                raise LocalDecisionError('Synthetic unavailable region judgment')
            return .01
        _, trace, fetched, (_, _, stats) = await self.run_graph({
            BASE+'root': '# Unknown\n\n[Record]('+BASE+'leaf)\n\n# Other\n\n[Other]('+BASE+'other)',
            BASE+'leaf': 'FINAL_FACT original source.'}, region_score=region)
        self.assertEqual(fetched, [BASE+'root', BASE+'leaf'])
        self.assertEqual(stats['page_eval_failures'], 1)
        decision = next(e for e in trace.events if e['event'] == 'rawtree.link_regions')
        self.assertTrue(decision['candidates'][0]['unknown'])
        self.assertIsNone(decision['candidates'][0]['score'])

    async def test_existing_link_cap_is_shared_between_selected_sections(self):
        body = '\n\n'.join('# Group '+str(group)+'\n\n' + '\n'.join(
            f'[Record {i}]({BASE}{group}_{i})' for i in range(180)) for group in range(2))
        bodies = {BASE+'root': body, BASE+'0_0': 'FINAL_FACT source zero.',
                  BASE+'0_1': 'FINAL_FACT source one.'}
        decision, trace, _, (_, _, stats) = await self.run_graph(bodies)
        self.assertEqual(stats['links_scored'], 300)
        event = next(e for e in trace.events if e['event'] == 'rawtree.links')
        self.assertEqual(sum(r['section_id'] == 0 for r in event['links']), 150)
        self.assertEqual(sum(r['section_id'] == 1 for r in event['links']), 150)
        for state, questions, ctx in decision.calls:
            if ctx['phase'] == 'links':
                key = next(iter(questions))
                self.assertIn(key, state['page_text'])
                self.assertLessEqual(decision.chunker.count(state['page_text']), 32)

    def test_structural_sections_preserve_source_and_ignore_code_headings(self):
        c = chunker(64)
        text = 'Opening\n\n# Main\n\nBody\n\n```\n# literal data\n```\n\n## Appendix\n\nTail'
        sections = c.sections(text)
        self.assertEqual(''.join(s['text'] for s in sections), text)
        self.assertEqual(len(sections), 3)
        self.assertEqual(sections[-1]['headings'], ['# Main', '## Appendix'])

    def test_long_link_context_centers_exact_marker_and_respects_budget(self):
        c = chunker(64)
        text = '[Other](link_10) ' + 'ordinary '*500 + '[Target](link_1) source relation'
        state = link_state({'page_text': text, 'outgoing_links': {'link_1': BASE+'target'}},
                           'link_1', chunker=c, limit=32)
        self.assertIn('(link_1)', state['page_text'])
        self.assertNotIn('(link_10)', state['page_text'])
        self.assertLessEqual(c.count(state['page_text']), 32)
        numbered = numbered_page('[Target]('+BASE+'target)', [(BASE+'target', 'Target')], key_offset=7)
        self.assertEqual(numbered, '[Target](link_7)')
