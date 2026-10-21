"""Saved-output audit; expected facts are used only here, never sent to d3."""
from collections import defaultdict
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'analysis/pilots/p19_marginal'

def returned_text(path):
    parts=[]
    if not path.exists():return ''
    for line in path.open(encoding='utf-8'):
        e=json.loads(line)
        if e.get('event')=='rawtree.return':
            for r in e.get('returned',[]):
                texts=r.get('texts',{})
                parts.extend(texts.values() if isinstance(texts,dict) else [])
    return '\n'.join(parts)

expected={
 'chemistry':[['7 November 1867'],['Warsaw']],
 'pep615':[['Paul Ganssle'],['22-Feb-2020','22 February 2020']],
 'direct':[['Final'],['22-Feb-2020','22 February 2020']],
 'bill':[['Peter Nzioki','Peter King Nzioki','Peter King']],
}
paths=[]
for p in sorted(FOLDER.glob('*.summary.json')):
    d=json.loads(p.read_text(encoding='utf-8'));case=d['case']
    text=returned_text(p.with_name(p.name.replace('.summary.json','.jsonl')))
    facts=[any(t.lower() in text.lower() for t in group) for group in expected[case]]
    stats=d.get('stats',{})
    paths.append(dict(case=case,variant=d['variant'],seconds=d['seconds'],error=d.get('error'),
        expected_facts=facts,all_facts=all(facts),nodes=d.get('nodes'),
        **{k:stats.get(k) for k in ['max_depth','reads','jev_requests','jev_input_tokens','fetch_failed']}))

requests={};totals=defaultdict(lambda:dict(calls=0,input_tokens=0,service_ms=0))
for p in sorted(FOLDER.glob('link_replay*.jsonl')):
    for line in p.open(encoding='utf-8'):
        e=json.loads(line)
        if e['event']=='jev.request':requests[e['request_id']]=e['context']
        if e['event']=='jev.result':
            c=requests[e['request_id']];key=(c['case'],c['variant'],p.name)
            t=totals[key];t['calls']+=1;t['input_tokens']+=e.get('usage',{}).get('input_tokens',0)
            t['service_ms']+=e.get('duration_ms',0)
links=json.loads((FOLDER/'link_summary.json').read_text(encoding='utf-8'))
compact=[]
for r in links:
    matching=[v for (case,variant,file),v in totals.items()
              if case==r['case'] and variant==r['variant'] and v['calls']==r['candidates']]
    cost=matching[-1] if matching else {}
    compact.append({k:r[k] for k in ['case','variant','seconds','candidates','expected']}|cost)
out=dict(links=compact,paths=paths,
    caveat='Fixed seeds and manual source-fact checks; no main-model accuracy or benchmark evaluation.')
(FOLDER/'audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=True,indent=2))
