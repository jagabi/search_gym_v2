"""Recover actual scored link markers, inputs and local destinations from traces."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10'
rows=[]
for q in (40,516,746,1196,1230):
    events=[json.loads(s) for s in (RUN/f'q{q:05}'/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    requests={e['request_id']:e for e in events if e['event']=='jev.request'}
    results={e['request_id']:e for e in events if e['event']=='jev.result'}
    queries={e['search_id']:e['query'] for e in events if e['event']=='rawtree.start'}
    previews={(e['search_id'],e['node_id']):e for e in events if e['event']=='rawtree.preview'}
    for e in events:
        if e['event']!='rawtree.links' or not e.get('joint'):continue
        for link in e['links']:
            if link.get('score') is None:continue
            url=link['url']
            # Target known suspicious routes for inspection; never a retrieval policy.
            suspect=(q==516 and any(s in url for s in ('IMDb_(identifier)','The_Proposition_', 'Danny_Huston', 'Jack_Huston'))
                     or q==40 and '/wiki/World_Athletics' in url)
            if not suspect:continue
            for request_id,request in requests.items():
                c=request['context']
                if not (c.get('search_id')==e['search_id'] and c.get('node_id')==e['node_id']
                        and c.get('bundle_id')==e.get('bundle_id') and c.get('phase')=='bundle'):continue
                if link['key'] not in request['body']['questions']:continue
                result=results.get(request_id,{})
                if result.get('scores',{}).get(link['key'])!=link['score']:continue
                state=request['body']['state'];text=state['page_text']
                marker=link['key'];matches=list(re.finditer(r'(?<!\w)'+re.escape(marker)+r'(?!\w)',text))
                snippets=[text[max(0,m.start()-250):m.end()+300] for m in matches[:3]]
                row={'question':q,'query':queries[e['search_id']], 'source_url':previews.get((e['search_id'],e['node_id']),{}).get('url'),
                     'title':state['page_title'], 'link':link,'visible_marker_contexts':snippets,
                     'instructions':request['body']['questions'][marker], 'request_id':request_id,
                     'input_state':state,'other_keys':list(request['body']['questions'])}
                rows.append(row)
                break
out=ROOT/'analysis/p31_diagnosis/link_input_audit.json'
out.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for row in rows:
    print(json.dumps({k:v for k,v in row.items() if k not in ('input_state','other_keys','instructions')},ensure_ascii=False))
if rows:print('EXACT_QUESTION',json.dumps(rows[0]['instructions'],ensure_ascii=False))
print('CASES',len(rows))
for q in (40,516):
    events=[json.loads(s) for s in (RUN/f'q{q:05}'/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    for e in events:
        if e['event']=='rawtree.entries' and q==516:
            text=json.dumps(e)
            if 'imdb.com/title/tt0387131' in text:
                print('IMDB_INITIAL_ENTRY',e.get('search_id'),list(e),text[:3000])
        if e['event']=='rawtree.fetch_failed' and ('imdb.com/title/tt0387131' in e['url'] or q==40 and 'World_Athletics' in e['url']):
            print('DIRECT_ACCESS',q,e['search_id'],e['node_id'],e['url'],e['elapsed_ms'])
        if e['event']=='rawtree.preview' and ('IMDb_(identifier)' in e['url'] or e['url'].endswith('/World_Athletics')):
            print('BAD_DESTINATION_PREVIEW',q,e['search_id'],e['url'],e['scores'])
