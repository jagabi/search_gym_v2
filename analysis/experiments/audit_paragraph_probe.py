"""Map diagnostic citations to supplied source blocks; no factual-accuracy judge."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from searchgym.explorer import _paragraph_ids, _note_section


def audit(run):
    manifest = {r['question']: r for r in json.loads((ROOT/'analysis/experiments/paragraph_probe_manifest.json').read_text(encoding='utf-8'))}
    rows = []
    for path in sorted(run.glob('q*_paragraph_*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        question = data['name'].split('_',1)[0]
        source = manifest[question]
        response = data.get('response', {})
        choice = response.get('choices', [{}])[0]
        text = choice.get('message', {}).get('content') or ''
        valid, invalid = _paragraph_ids(_note_section(text, 'Evidence'), len(source['paragraphs']))
        blocks = {f'P{i}': source['paragraphs'][i-1] for i in valid}
        rows.append({'name':data['name'], 'urls':source['urls'], 'text':text,
                     'finish_reason':choice.get('finish_reason'), 'error':data.get('error'),
                     'valid_ids':valid, 'invalid_ids':invalid,
                     'selected_chars':sum(map(len,blocks.values())), 'source_blocks':blocks,
                     'usage':response.get('usage',{})})
    return {'run':str(run), 'scope':'Citation/return feasibility, not semantic correctness or benchmark accuracy.',
            'summary': {'calls':len(rows), 'nonempty':sum(bool(r['text']) for r in rows),
                'with_valid_citations':sum(bool(r['valid_ids']) for r in rows),
                'with_invalid_citations':sum(bool(r['invalid_ids']) for r in rows),
                'input_tokens':sum(r['usage'].get('prompt_tokens',0) for r in rows),
                'output_tokens':sum(r['usage'].get('completion_tokens',0) for r in rows)}, 'rows':rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser();parser.add_argument('run',type=Path);parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args();result = audit(args.run)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result['summary'],indent=2))
