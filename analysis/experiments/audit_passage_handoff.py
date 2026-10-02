"""Read-only structural diagnostics for extractive recursive handoff, including live runs."""
import argparse
from collections import Counter
import json
from pathlib import Path


def lines(path):
    if not path.exists():
        return []
    # A live writer can leave only its last JSON record unfinished.
    text = path.read_text(encoding='utf-8')
    rows = text.split('\n')
    if rows[-1].strip():
        try:
            json.loads(rows[-1])
        except json.JSONDecodeError:
            rows.pop()
    return [json.loads(row) for row in rows if row.strip()]


def audit(run):
    completed = {r['index']: r for r in lines(run/'records.jsonl')}
    totals, cases = Counter(), []
    for tracepath in sorted(run.glob('q*/trace.jsonl')):
        events = lines(tracepath)
        counts, depths, selections = Counter(), Counter(), []
        for e in events:
            if e['event'] == 'explorer.passage_selection':
                counts['selections'] += 1
                counts['empty_selections'] += not bool(e['selected_ids'])
                counts['invalid_selections'] += bool(e['invalid_ids'])
                counts['clipped_selections'] += e['evidence_truncated']
                counts['source_paragraphs'] += e['paragraph_count']
                counts['selected_paragraphs'] += len(e['selected_ids'])
                counts['returned_source_chars'] += e['evidence_chars']
                depths[str(e['depth'])] += 1
                selections.append({key: e[key] for key in (
                    'depth','urls','paragraph_count','selected_ids','invalid_ids','evidence_chars','evidence_truncated')})
            elif e['event'] == 'explorer.response':
                phase = e['phase']
                counts[phase + '_calls'] += 1
                counts[phase + '_input_tokens'] += e.get('prompt_tokens') or 0
                counts[phase + '_output_tokens'] += e.get('completion_tokens') or 0
            elif e['event'] == 'expand.return':
                counts['recursive_returns'] += 1
            elif e['event'] in ('explorer.error', 'control.error'):
                counts['errors'] += 1
        index = int(tracepath.parent.name[1:])
        record = completed.get(index)
        totals.update(counts)
        cases.append({'index': index, 'completed': record is not None,
                      'accuracy': record['accuracy'] if record else None,
                      'counts': dict(counts), 'depths': dict(depths),
                      'last_event': events[-1]['event'] if events else None,
                      'selections': selections})
    return {'run': str(run), 'completed':len(completed), 'totals':dict(totals), 'cases':cases,
            'scope':'Structural diagnostics only. Valid IDs do not establish relevance or source truth.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('run',type=Path);parser.add_argument('--out',type=Path)
    args=parser.parse_args(); data=audit(args.run)
    print(json.dumps({'completed':data['completed'],**data['totals']},indent=2))
    if args.out:
        args.out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
