"""Offline candidate inventory for manually checking link false negatives."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'runs/test/20261022-1504_jevtree_gpt-oss-20b_browsecomp_raw_browser_p31_pplx_no_early_return_10'
rows=[]
for folder in sorted(RUN.glob('q*')):
    ev=[json.loads(s) for s in (folder/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    req={e['request_id']:e for e in ev if e['event']=='jev.request'}
    results={e['request_id']:e for e in ev if e['event']=='jev.result'}
    packets={}
    for rid,r in req.items():
        c=r['context']
        if c.get('phase')=='bundle':
            for k in r['body']['questions']:
                if k.startswith('link_'):packets[(c['search_id'],c['node_id'],c['bundle_id'],k)]=(rid,r)
    queries={e['search_id']:e['query'] for e in ev if e['event']=='rawtree.start'}
    for e in ev:
        if e['event']!='rawtree.links' or not e.get('joint'):continue
        for link in e['links']:
            if link.get('score') is None:continue
            pair=packets.get((e['search_id'],e['node_id'],e['bundle_id'],link['key']))
            if not pair:continue
            rid,r=pair
            if results.get(rid,{}).get('scores',{}).get(link['key'])!=link['score']:continue
            row={'q':int(folder.name[1:]),'query':queries[e['search_id']],'request_id':rid,
                 'source_title':r['body']['state'].get('page_title'), **link}
            rows.append(row)
(ROOT/'analysis/p31_diagnosis/all_scored_links.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
for row in rows:
    url=row['url'].lower()
    useful=(row['q']==40 and any(s in url for s in ('worldathletics.org','1999','10000','10,000'))
        or row['q']==516 and any(s in url for s in ('imdb.com/title','cast','credits','peter','king','metacritic','bill_condon','fifth_estate'))
        or row['q']==326 and any(s in url for s in ('manushkin','baby'))
        or row['q']==598 and any(s in url for s in ('revistadestatistica','jemna','jaba'))
        or row['q']==1196 and any(s in url for s in ('thiruvananthapuram','trivandrum','shashi','varma')))
    if useful:print(json.dumps(row,ensure_ascii=False))
