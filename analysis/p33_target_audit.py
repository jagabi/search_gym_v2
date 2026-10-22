import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-1705_jevtree_gpt-oss-20b_browsecomp_raw_browser_p33_fetch_all10_10'
def events(path):
    out=[]
    for line in path.read_text(encoding='utf-8').splitlines():
        try:out.append(json.loads(line))
        except json.JSONDecodeError:pass
    return out
for q in (57,516,598,746,1230):
    ev=events(RUN/f'q{q:05d}'/'trace.jsonl')
    queries={e['search_id']:e['query'] for e in ev if e['event']=='rawtree.start'}
    print('\nQUESTION',q,'FAIL',sum(e['event']=='rawtree.fetch_failed' for e in ev),'FETCH',sum(e['event']=='fetch.raw' for e in ev))
    if q==598:terms=['HDS','romjef','Romanian Statistical','rsr.ro','Jaba']
    elif q==516:terms=['metacritic','Peter King','Nzioki','fullcredits','tvguide','cast/']
    elif q==1230:terms=['Regal','Colombo','Sri Lanka']
    elif q==57:terms=['PMC7227421','1685381']
    else:terms=['Humphrey','Mondale','Hamlin']
    previews={(e['search_id'],e['node_id']):e for e in ev if e['event']=='rawtree.preview'}
    inspected={(e['search_id'],n) for e in ev if e['event']=='rawtree.inspection_selection' for n in e['selected']}
    for e in ev:
        if e['event']=='rawtree.entries':
            for item in e['candidates']:
                lead=item.get('lead',item)
                if any(t.lower() in json.dumps(lead).lower() for t in terms):print('ENTRY',queries[e['search_id']],json.dumps(lead,ensure_ascii=False))
        if e['event']=='rawtree.preview' and any(t.lower() in e['url'].lower() for t in terms):print('PREVIEW',e['url'],e['scores'],'INSPECTED', (e['search_id'],e['node_id']) in inspected)
        if e['event']=='fetch.raw' and any(t.lower() in e.get('url','').lower() for t in terms):
            print('FETCH_TARGET',e['url'],'ERROR',e.get('is_error'),'CHARS',len(e.get('content','')))
        if e['event']=='rawtree.return':
            for item in e['returned']:
                text=json.dumps(item,ensure_ascii=False)
                if any(t.lower() in text.lower() for t in terms):
                    print('RETURN_TARGET',queries[e['search_id']],text[:1800])
        if e['event']=='fetch.raw' and not e.get('is_error'):
            content=e.get('content','')
            for t in terms:
                pos=content.lower().find(t.lower())
                if pos>=0 and t not in ('HDS','Hamlin','Humphrey','Mondale'):print('TEXT_TARGET',e.get('url'),t,content[max(0,pos-100):pos+400].replace('\n',' '))
    if q==598:
        for e in ev:
            if e['event']=='rawtree.return' and 'apa.org' in json.dumps(e['returned']):
                (ROOT/'analysis/p33_diagnosis/q598_apa_return.json').write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
    responses=[e for e in ev if e['event']=='jev.response']
    print('DECISIONS',len(responses),Counter(e['status_code'] for e in responses))
prev=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10/q00598'
for e in events(prev/'trace.jsonl'):
    if e['event']=='rawtree.start':print('PREV598_QUERY',e['query'])
    if e['event']=='rawtree.return':print('PREV598_SOURCES',[x['source'] for x in e['returned']])
