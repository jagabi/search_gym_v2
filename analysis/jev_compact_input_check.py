"""Offline payload-size audit. Character ratios are NOT billing-token ratios."""
import json
from pathlib import Path

from searchgym.jevtree import IDENTIFICATION_QUESTION, VERIFICATION_QUESTION, ENTRY_NOTE, ENTRY_CRITERIA
from searchgym.jevtree_input import page_requests, complete_prefix

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'runs/test/20261003-2043_jevtree_gpt-oss-20b_browsecomp_jevtree_v65_diagnostic10'


def size(body):
    return len(json.dumps(body, ensure_ascii=False))


def main():
    rows = []
    for qid in [40, 117, 516, 1196]:
        groups, old_chars, entry_chars, old_calls, entry_calls = {}, 0, 0, 0, 0
        for line in (RUN / f'q{qid:05d}/trace.jsonl').open(encoding='utf-8'):
            e = json.loads(line)
            if e['event'] != 'jev.request':
                continue
            old_calls += 1
            old_chars += size(e['body'])
            ctx = e['context']
            if ctx['phase'] == 'entry':
                entry_state = {k: v for k, v in e['body']['state'].items() if k != 'question_conditions'}
                entry_questions = {k: {'type': 'noul',
                    'instructions': ENTRY_NOTE + f' Would {k} help find the answer?',
                    'criteria': ENTRY_CRITERIA} for k in e['body']['questions']}
                entry_chars += size(dict(model='jev-1.13.0', state=entry_state, questions=entry_questions))
                entry_calls += 1
                continue
            key = (ctx['search_id'], ctx['page_url'])
            group = groups.setdefault(key, dict(state=e['body']['state'], links={}))
            for name, question in e['body']['questions'].items():
                if name.startswith('link_'):
                    data = json.loads(question['instructions'].split('Source data: ', 1)[1])
                    group['links'][int(name[5:])] = (data['url'], data['anchor'])
        new_chars, new_calls, link_count, old_links = entry_chars, entry_calls, 0, 0
        for group in groups.values():
            state = group['state']
            old_candidates = [v for _, v in sorted(group['links'].items())]
            source = state['page_text']
            # Same fallback used by LLM.cap when the tokenizer server is absent:
            # len(text)//3. This is a local preview, not an exact 5000-token cut.
            excerpt = complete_prefix(source, source[:15000])
            # Keep only previously eligible candidates fully visible in this prefix.
            # Re-extraction without the original visited set would add visited URLs.
            from searchgym.jevtree import candidate_links
            visible = {u for u, _ in candidate_links(excerpt, state['page_url'], set())}
            links = [(u, a) for u, a in old_candidates if u in visible]
            old_links += len(old_candidates)
            packets = page_requests(question=state['question'], page_url=state['page_url'],
                page=excerpt, links=links,
                page_questions={'direct_answer': IDENTIFICATION_QUESTION,
                                'answer_likelihood': VERIFICATION_QUESTION}, links_per_request=100)
            link_count += len(links)
            assert all(f'link_{i}' in packets[0][0]['page_text'] for i in range(len(links)))
            for s, q in packets:
                new_chars += size(dict(model='jev-1.13.0', state=s, questions=q))
                new_calls += 1
            if qid == 516 and state['page_url'] == 'https://en.wikipedia.org/wiki/Peter_Nzioki':
                (ROOT / 'analysis/jev_compact_input_example.json').write_text(
                    json.dumps([dict(model='jev-1.13.0', state=s, questions=q) for s, q in packets],
                               ensure_ascii=False, indent=2), encoding='utf-8')
        rows.append(dict(qid=qid, old_chars=old_chars, new_chars=new_chars,
                         remaining_ratio=round(new_chars / old_chars, 4), old_requests=old_calls,
                         new_requests=new_calls, old_links=old_links, retained_links=link_count))
    result = dict(note='Offline JSON character sizes; 5000-token excerpts approximated as 15000 characters. No API calls or score validation.',
                  rows=rows, remaining_ratio=sum(r['new_chars'] for r in rows) / sum(r['old_chars'] for r in rows))
    (ROOT / 'analysis/jev_compact_input_check.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
