"""Compact, offline inspection of the v10 diagnostic run; no model/network calls."""
import collections
import json
import sys
from pathlib import Path

RUN = Path('runs/test/20261019-0005_jevtree_gpt-oss-20b_browsecomp_raw_browser_p10_progressive10')
OUT = Path('analysis/audit_20261019-0005')

def read(p):
    return json.loads(p.read_text(encoding='utf8'))

def events(p):
    with p.open(encoding='utf8') as f:
        for line in f:
            yield json.loads(line)

def build():
    OUT.mkdir(exist_ok=True)
    rows = []
    for record in events(RUN/'records.jsonl'):
        p = RUN/record['dir']
        r = read(p/'response.json')
        state = r.get('research_state') or {}
        row = {k:r.get(k) for k in ['index','question','gold_answer','answer','stop_reason','turns','invalid_tool_calls','context_tokens']}
        row.update(score=record['score'], minutes=round(record['latency_s']/60,2),
                   stats=r['reader_stats'], candidates=state.get('candidates'),
                   state_metrics=state.get('metrics'), actions=[], errors=[], fetch_errors=[],
                   outputs=[], main=[], timeline=[])
        requests = {}
        for step in r['steps']:
            for call in step.get('tool_calls',[]):
                a=call.get('arguments') or {}
                if isinstance(a,str):
                    try: a=json.loads(a)
                    except ValueError: a={'raw':a[:300]}
                research=a.get('research') or {}
                row['actions'].append({'turn':step['turn'],'name':call.get('name',call.get('tool')),
                    'args':{k:v for k,v in a.items() if k!='research'},
                    'next_gap':research.get('next_gap'), 'candidates':research.get('candidates'),
                    'source_access':research.get('source_access'), 'thought':step.get('reasoning','')[:450]})
        for e in events(p/'trace.jsonl'):
            name=e['event']; sec=round(e['elapsed_ms']/1000,2)
            if name=='llm.request':
                requests[e['turn']]=sec
            elif name=='llm.response':
                row['main'].append({'turn':e['turn'],'s':round(sec-requests.get(e['turn'],sec),2),
                    'context_tokens':e.get('context_tokens'),'chars':len(e.get('text','')),
                    'reasoning_chars':e.get('reasoning_chars'),'tools':e.get('tool_calls'),
                    'finish':e.get('finish_reason')})
            if name in ['tool.error','tool.invalid','tool.result','tool.return']:
                compact={k:v for k,v in e.items() if k not in ['content','text','body','messages','result']}
                text=str(e.get('content',e.get('text',e.get('result',''))))
                row['timeline'].append({'s':sec,'event':name,'keys':list(e),'meta':compact,'text':text[:400]})
            if name=='fetch.raw' and e.get('is_error'):
                row['fetch_errors'].append({'s':sec,'url':e.get('url'),'duration_ms':e.get('duration_ms'),
                    'content':e.get('content','')[:350]})
            if name=='rawtree.return':
                row['outputs'].append({'s':sec,'action':e.get('action'),'goal':e.get('goal'),
                    'stats':e.get('stats'), 'sources':[{'id':x.get('source_id'),'url':x.get('source'),
                    'chunks':x.get('chunk_ids')} for x in e.get('returned',[])]})
            if 'invalid' in name or name.endswith('.error') or name.endswith('.refused'):
                row['errors'].append({k:v for k,v in e.items() if k not in ['body','messages','content','text']})
        (OUT/f'q{record["index"]:05d}_review.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf8')
        rows.append({'id':r['index'],'minutes':row['minutes'],'score':record['score'],
            'searches':r['searches'],'invalid':r['invalid_tool_calls'],'actions':dict(collections.Counter(a['name'] for a in row['actions'])),
            'candidates':len(state.get('candidates',[])), 'reads':r['reader_stats'].get('tree_reads'),
            'visits':r['reader_stats'].get('page_visits'), 'fetch_failures':r['fetch_failures'],
            'first_evidence_s':record.get('control_stats',{}).get('first_evidence_s')})
    (OUT/'overview.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(rows,ensure_ascii=False))

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf8')
    if len(sys.argv)==1: build()
    else:
        r=read(OUT/f'q{int(sys.argv[1]):05d}_review.json')
        keys=sys.argv[2:] or ['question','answer','actions']
        print(json.dumps({k:r.get(k) for k in keys},ensure_ascii=False,indent=2))
