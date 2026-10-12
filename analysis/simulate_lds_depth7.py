"""Synthetic online LDS, matplotlib only. No model/web calls or app edits.

python analysis/simulate_lds_depth7.py --budget 100 --depth 7 --children 5 --seed 42
Score = incoming link utility, not correctness. Only sibling ranks guide LDS.
"""
import argparse
import copy
import hashlib
import json
import random
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'analysis/visuals/lds_depth7'
RUN = BASE / 'runs/test/20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10'

def load_distribution():
    cache = OUT / 'empirical_score_vectors.json'
    if cache.exists():
        return json.loads(cache.read_text(encoding='utf-8'))
    paths = sorted(RUN.glob('q*/trace.jsonl'))
    selected = [paths[i] for i in np.linspace(0, len(paths)-1, 12, dtype=int)]
    pages, entries, sources = [], [], []
    for path in selected:
        count = 0
        for line in path.open(encoding='utf-8'):
            head = line[:400]
            if '"jevtree.entry_scores"' in head:
                e = json.loads(line)
                scores = [float(v[0]) for v in e['scores']]
                if len(scores) == 10:
                    entries.append(scores)
            elif '"jevtree.scored"' in head:
                e = json.loads(line)
                # Preserve within-page ties and score scale; deduplicate URLs.
                by_url = {}
                for v in e.get('link_scores', []):
                    by_url.setdefault(v['url'], float(v['score']))
                pages.append(sorted(by_url.values(), reverse=True))
                count += 1
                if count >= 20:
                    break
        sources.append({'path': str(path), 'sampled_pages': count})
    assert entries and pages
    result = {'entry_vectors': entries, 'page_vectors': pages, 'sources': sources,
              'sampling': '12 evenly spaced question folders; first 20 scored pages each; entry vectors with exactly 10 results.'}
    cache.write_text(json.dumps(result, indent=2), encoding='utf-8')
    return result

def run(args, dist):
    # Stable per-path randomness: unrevealed branches are never materialized.
    def page_candidates(path):
        digest = hashlib.sha256(f'{args.seed}:{path}'.encode()).digest()
        rng = random.Random(int.from_bytes(digest[:8], 'big'))
        vector = rng.choice(dist['page_vectors'])
        return vector[:args.children], len(vector)

    root_scores = sorted(random.Random(args.seed).choice(dist['entry_vectors']), reverse=True)
    nodes = {}
    roots = []
    for rank, score in enumerate(root_scores, 1):
        nid = f'R{rank}'
        roots.append(nid)
        nodes[nid] = dict(id=nid, parent=None, root=nid, depth=1, rank=rank,
                          score=score, discrepancy=int(rank>1), fetched=False)
    events, snapshots = [], []
    limit = 0
    def snap():
        return dict(fetches=len(events), limit=limit, nodes=copy.deepcopy(nodes), next=None)
    snapshots.append(snap())

    def visit(nid):
        n = nodes[nid]
        if len(events) >= args.budget:
            return
        if not n['fetched']:
            snapshots[-1].update(next=nid, limit=limit)
            n.update(fetched=True, visit=len(events)+1, children=[])
            if n['depth'] < args.depth:
                scores, available = page_candidates(nid)
                n['available_links'] = available
                for rank, score in enumerate(scores, 1):
                    cid = f'{nid}.{rank}'
                    nodes[cid] = dict(id=cid, parent=nid, root=n['root'], depth=n['depth']+1,
                                      rank=rank, score=score, discrepancy=n['discrepancy']+int(rank>1), fetched=False)
                    n['children'].append(cid)
            events.append({k:n[k] for k in ['id','root','depth','rank','score','discrepancy','visit']})
            events[-1]['limit'] = limit
            snapshots.append(snap())
        kids = n['children']
        # Explicit multiway LDS variant: early deviations first; any non-first
        # choice costs one, including choosing R2..R10 at the virtual root.
        choices = kids[1:]+kids[:1] if n['discrepancy'] < limit else kids[:1]
        for child in choices:
            if nodes[child]['discrepancy'] <= limit:
                visit(child)

    for limit in range(args.depth+1):
        for root in (roots[1:]+roots[:1] if limit else roots[:1]):
            if nodes[root]['discrepancy'] <= limit:
                visit(root)
        if len(events) >= args.budget:
            break
    for state in snapshots:
        for n in state['nodes'].values():
            assert n['depth'] <= args.depth
            if not n['fetched']:
                assert 'children' not in n
            if n['parent']:
                assert state['nodes'][n['parent']]['fetched']
    assert len({e['id'] for e in events}) == len(events)
    return roots, events, snapshots

def plot_tree(ax, state, roots, depth, compact=False):
    nodes = state['nodes']
    positions, aggregates = {}, {}
    cursor = 0
    def layout(nid):
        nonlocal cursor
        n = nodes[nid]
        children = n.get('children', [])
        opened = [c for c in children if nodes[c]['fetched']]
        pending = [c for c in children if not nodes[c]['fetched']]
        xs = [layout(c) for c in opened]
        if pending:
            aggregates[nid] = (cursor, n['depth']+1, len(pending), state['next'] in pending)
            xs.append(cursor)
            cursor += 1
        if not xs:
            xs = [cursor]
            cursor += 1
        x = float(np.mean(xs))
        positions[nid] = (x, n['depth'])
        return x
    for root in roots:
        layout(root)
        cursor += .65
    for nid, (x,y) in positions.items():
        n = nodes[nid]
        if n['parent']:
            px,py = positions[n['parent']]
            ax.plot([px,x], [py,y], color='#b5c0cd', lw=.8, zorder=1)
    for nid,(x,y,count,chosen) in aggregates.items():
        px,py=positions[nid]
        ax.plot([px,x],[py,y],color='#c7ced8',lw=.8,ls=':')
        ax.scatter(x,y,marker='v',s=44 if compact else 70,color='#d47b19' if chosen else '#b8c0ca',zorder=2)
        ax.annotate(f'+{count}',(x,y),xytext=(0,-15),textcoords='offset points',ha='center',fontsize=6 if compact else 9,color='#616b78')
    for nid,(x,y) in positions.items():
        n=nodes[nid]
        ax.scatter(x,y,s=85 if compact else 160,facecolor='#dceafb' if n['fetched'] else 'white',
                   edgecolor='#df7c17' if state['next']==nid else '#316aa4' if n['fetched'] else '#8794a2',zorder=3)
        # Dense overviews omit intermediate labels; the separate final figure
        # preserves every value with order above and score below each node.
        label_visible = not compact or state['fetches'] < 50 or n['parent'] is None or n.get('visit') == state['fetches']
        if label_visible:
            ax.annotate(f'{n["score"]:.2f}',(x,y),xytext=(0,-13),textcoords='offset points',ha='center',fontsize=6 if compact else 8)
            if n['fetched']:
                ax.annotate(f'#{n["visit"]}',(x,y),xytext=(0,9),textcoords='offset points',ha='center',fontsize=6 if compact else 8)
        if n['parent'] is None:
            ax.annotate(nid,(x,y),xytext=(0,26),textcoords='offset points',ha='center',fontsize=7 if compact else 10,fontweight='bold')
    ax.set_ylim(depth+.55,.15)
    ax.set_xlim(-1,max(cursor,2))
    ax.set_yticks(range(1,depth+1))
    ax.set_ylabel('Depth')
    ax.set_xticks([])
    ax.grid(axis='y',color='#eeeeee',lw=.6)
    for sp in ax.spines.values(): sp.set_visible(False)
    pending=sum(not n['fetched'] for n in nodes.values())
    ax.set_title(f'Fetch {state["fetches"]} | allowed deviations {state["limit"]} | pending {pending}',loc='left',fontsize=11 if compact else 16,pad=23)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--budget',type=int,default=100)
    p.add_argument('--depth',type=int,default=7)
    p.add_argument('--children',type=int,default=5)
    p.add_argument('--seed',type=int,default=42)
    args=p.parse_args()
    if min(args.budget,args.depth,args.children)<1: p.error('limits must be positive')
    OUT.mkdir(parents=True,exist_ok=True)
    dist=load_distribution()
    roots,events,states=run(args,dist)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    legend=[Line2D([],[],marker='o',color='none',markerfacecolor='#dceafb',markeredgecolor='#316aa4',label='Fetched (#order, score)'),
            Line2D([],[],marker='o',color='none',markeredgecolor='#8794a2',label='Unopened search result (score)'),
            Line2D([],[],marker='v',color='#b8c0ca',ls='none',label='+N discovered, unopened children'),
            Line2D([],[],marker='v',color='#df7c17',ls='none',label='Contains next fetch')]
    steps=[0,1,min(7,len(events)),min(20,len(events)),min(50,len(events)),len(events)]
    fig,axes=plt.subplots(3,2,figsize=(27,24))
    for ax,step in zip(axes.flat,steps): plot_tree(ax,states[step],roots,args.depth,True)
    fig.suptitle(f'Online LDS: 10 search results -> depth {args.depth}\nSynthetic score vectors resampled from logs | top {args.children} candidates/page | budget {args.budget} | seed {args.seed}',fontsize=20,y=.988)
    fig.legend(handles=legend,loc='upper center',bbox_to_anchor=(.5,.95),ncol=4,fontsize=11)
    fig.text(.03,.013,'Only fetched nodes reveal children. +N = discovered, unopened children. Dense panels omit intermediate labels; see final_forest.png for all values.\nScore is incoming link utility, NOT answer correctness. No score threshold. Depth 4+ extrapolates the observed distribution.',fontsize=12)
    fig.tight_layout(rect=(0,.05,1,.925),h_pad=4)
    fig.savefig(OUT/'expansion_steps.png',dpi=160)
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(40,12))
    plot_tree(ax,states[-1],roots,args.depth)
    fig.suptitle('Final revealed forest | one score per link | no hidden descendants shown',fontsize=21,y=.985)
    fig.legend(handles=legend,loc='lower center',ncol=4,fontsize=12)
    fig.tight_layout(rect=(0,.055,1,.94))
    fig.savefig(OUT/'final_forest.png',dpi=160)
    fig.savefig(OUT/'final_forest.svg')
    plt.close(fig)
    fig,(a,b)=plt.subplots(2,1,figsize=(19,8),sharex=True)
    x=[e['visit'] for e in events]
    a.plot(x,[e['score'] for e in events],'.-',lw=.7,color='#316aa4')
    a.set(ylabel='Incoming link score',ylim=(-.03,1.03),title='Fetch order: scores may rise, collapse, or tie; LDS uses local rank, not global score')
    b.plot(x,[e['depth'] for e in events],'.-',lw=.8,color='#316aa4')
    b.set(ylabel='Depth',xlabel='Fetch number',yticks=range(1,args.depth+1))
    prev=None
    for e in events:
        if e['root']!=prev:
            b.axvline(e['visit'],color='#cccccc',lw=.7)
            b.text(e['visit'],.45,e['root'],fontsize=8)
        prev=e['root']
    for ax in (a,b): ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(OUT/'fetch_sequence.png',dpi=160)
    plt.close(fig)
    empirical=[s for v in dist['page_vectors'] for s in v]
    summary={'config':vars(args),'sampled_questions':len(dist['sources']),
             'sampled_pages':len(dist['page_vectors']),'sampled_link_scores':len(empirical),
             'link_score_quantiles':dict(zip(['p10','p50','p90'],np.quantile(empirical,[.1,.5,.9]).tolist())),
             'fetched':len(events),'max_depth_reached':max(e['depth'] for e in events),
             'fetched_per_root':{r:sum(e['root']==r for e in events) for r in roots},
             'pending':sum(not n['fetched'] for n in states[-1]['nodes'].values()),
             'assumptions':['Each page independently resamples a whole observed score vector; cross-depth correlation is not fitted.',
                            'Root rank>1 and child rank>1 each cost one discrepancy; early deviations first.',
                            'Depth 4-7 are extrapolated. Failures, duplicates across pages, and latency are not simulated.',
                            'Synthetic utility only; no ground truth, accuracy, reader, or success metric.'],
             'events':events}
    (OUT/'simulation.json').write_text(json.dumps({'summary':summary,'snapshots':states},indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='events'},indent=2))

if __name__=='__main__': main()
