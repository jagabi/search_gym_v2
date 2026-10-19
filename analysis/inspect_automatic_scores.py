"""Read only small traversal events from the saved automatic best-first run."""
import collections
import json
from pathlib import Path

RUN=Path('runs/test/20261017-2332_jevtree_gpt-oss-20b_browsecomp_raw_browser_p9_10')
OUT=Path('analysis/audit_20261019-0005/automatic_scores.json')
FLOORS=[0,.001,.01,.03,.05,.1,.15]

def quantiles(values):
    a=sorted(values)
    if not a: return {}
    return {'n':len(a),'mean':round(sum(a)/len(a),4),
            **{f'p{p}':round(a[min(len(a)-1,int((len(a)-1)*p/100))],5) for p in [10,25,50,75,90,95]},
            'below':{str(f):sum(v<f for v in a) for f in FLOORS}}

scores=[]; per_parent=collections.Counter(); nodes={}; edges={}; depth=collections.Counter(); rows=[]
for folder in sorted(RUN.glob('q*')):
    if not folder.is_dir(): continue
    local=[]
    with (folder/'trace.jsonl').open(encoding='utf8') as stream:
        for line in stream:
            # Skip model bodies and full documents without decoding them.
            if not any(t in line[:180] for t in ['rawtree.preview','rawtree.frontier']): continue
            e=json.loads(line); sid=(folder.name,e['search_id'])
            if e['event']=='rawtree.preview':
                nodes[(*sid,e['url'])]=e['depth']; depth[e['depth']]+=1
            elif e['event']=='rawtree.frontier':
                for c in e['candidates']:
                    score=c['score']; local.append(score)
                    per_parent[(*sid,c['parent'])]+=1
                    edges.setdefault((*sid,c['url']),[]).append(score)
    scores.extend(local)
    rows.append({'q':folder.name,'links':quantiles(local)})
visited=[]
def collect(node):
    if node['depth']>1 and node.get('link_score') is not None:
        visited.append(node['link_score'])
    for child in node.get('opened',[]): collect(child)
for path in RUN.glob('q*/explorer.json'):
    for root in json.loads(path.read_text(encoding='utf8')): collect(root)
result={'all_link_scores':quantiles(scores),'visited_link_scores':quantiles(visited),
        'links_per_parent_with_links':quantiles(list(per_parent.values())),
        'successful_preview_depths':dict(depth),'questions':rows,
        'limitations':'Observed p9 graph only; scores are not calibrated probabilities. Floors count existing scored edges, not requests avoided; online paths and future scores can change.'}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='questions'},ensure_ascii=False))
