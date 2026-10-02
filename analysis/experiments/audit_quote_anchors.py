"""Offline feasibility check: exact quoted evidence mapped back to supplied paragraphs.

This does not change production extraction or make model/network calls. It never
uses question labels/answers to select quotes or paragraphs.
"""
import argparse
import json
import re
from pathlib import Path


def normalize(text):
    # Ignore presentation markup for matching; returned paragraphs stay verbatim.
    text = re.sub(r'\[([^\]\n]+)\]\([^\n]+?\)', r'\1', text)
    text = text.replace('**', '').replace('`', '')
    return ' '.join(text.split())


def anchors(source, note):
    quotes = list(dict.fromkeys(normalize(m.group(1)) for m in
        re.finditer(r'["“]([^"”\n]{20,600})["”]', note)
        if len(m.group(1).split()) >= 5))
    paragraphs = [p for p in re.split(r'\n\s*\n', source) if p.strip()]
    selected = []
    matched = []
    for quote in quotes:
        matches = [i for i,p in enumerate(paragraphs) if quote in normalize(p)]
        if matches:
            matched.append(quote)
            # Preserve each matching paragraph instead of resolving ambiguity
            # by guessing which occurrence the model intended.
            for index in matches:
                if index not in selected:
                    selected.append(index)
    return {'quotes': quotes, 'matched_quotes': matched,
            'paragraphs': [paragraphs[i] for i in sorted(selected)]}


def audit(run):
    rows = []
    for path in sorted(run.glob('q*/trace.jsonl')):
        pending = {}
        for line in path.read_text(encoding='utf-8').split('\n'):
            if not line.strip():
                continue
            event = json.loads(line)
            key = (event.get('depth'), tuple(event.get('urls', [])))
            if event['event'] == 'explorer.extract_input':
                text = event['messages'][1]['content']
                marker = '**Pages you were given:**\n'
                if marker in text:
                    pending[key] = text.split(marker, 1)[1]
            elif event['event'] == 'explorer.response' and event.get('phase') == 'extract' and key in pending:
                source = pending.pop(key)
                result = anchors(source, event.get('text', ''))
                rows.append({'question': path.parent.name, 'depth': key[0], 'urls': key[1],
                    'source_chars': len(source), 'note_chars': len(event.get('text', '')),
                    'anchor_chars': sum(map(len,result['paragraphs'])), **result})
    return {'run': str(run), 'scope': 'Exact whitespace-normalized matching; feasibility only, not factual validation.',
        'summary': {'extractions': len(rows), 'with_quotes': sum(bool(r['quotes']) for r in rows),
            'with_anchor': sum(bool(r['paragraphs']) for r in rows),
            'quote_count': sum(len(r['quotes']) for r in rows),
            'matched_quote_count': sum(len(r['matched_quotes']) for r in rows),
            'source_chars': sum(r['source_chars'] for r in rows),
            'anchor_chars': sum(r['anchor_chars'] for r in rows)}, 'rows': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.run)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result['summary'], indent=2))
