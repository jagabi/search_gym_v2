"""Post-hoc literal answer occurrence audit. Gold is never sent to models or retrieval."""
import argparse
import json
import re
from pathlib import Path


def normalize(text):
    return ' '.join(re.findall(r'\w+', text.casefold()))


def contains(text, answer):
    return (' ' + normalize(answer) + ' ') in (' ' + normalize(text) + ' ')


def rows(path):
    return [json.loads(s) for s in path.read_text(encoding='utf-8').split('\n') if s.strip()]


def audit(run, cohort):
    questions = {r['index']: r for r in json.loads(cohort.read_text(encoding='utf-8'))}
    output = []
    for record in rows(run/'records.jsonl'):
        answer = questions[record['index']]['answer']
        trace = rows(run/record['dir']/'trace.jsonl')
        sources = {}
        for event in trace:
            if event['event'] != 'explorer.extract_input':
                continue
            content = event['messages'][1].get('content', '')
            marker = '**Pages you were given:**\n'
            if marker not in content:
                continue
            content = content.split(marker, 1)[1]
            if contains(content, answer):
                sources[tuple(event['urls'])] = {'urls':event['urls'], 'depth':event['depth']}
        trees = json.loads((run/record['dir']/'explorer.json').read_text(encoding='utf-8'))
        returned = any(contains(t.get('information',''), answer) for t in trees)
        response = json.loads((run/record['dir']/'response.json').read_text(encoding='utf-8'))
        output.append({'index':record['index'], 'gold_literal':answer, 'accuracy':record['accuracy'],
                       'in_supplied_source':bool(sources), 'source_matches':list(sources.values()),
                       'in_returned_reading':returned, 'in_answer':contains(response['answer'],answer)})
    return {'scope':'Exact normalized phrase occurrence only, not supporting evidence or semantic correctness. '
                    'Aliases/titles can be missed; short answers and spam may match incidentally. '
                    'Gold is used only in this post-hoc analysis.', 'run':str(run), 'cases':output}


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('run',type=Path);p.add_argument('--cohort',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();data=audit(a.run,a.cohort)
    a.out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    for r in data['cases']:
        print(r['index'],r['accuracy'],'source',r['in_supplied_source'],
              'return',r['in_returned_reading'],'answer',r['in_answer'])
