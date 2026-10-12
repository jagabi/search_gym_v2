"""One standalone SVG per action, with a local previous/next viewer.

Fixed illustrative policy: five mandatory roots, depth cap 6, 40 fetches,
top-five candidates, round-robin roots, multiway LDS with early deviations.
Only stdlib. No app edits, network, matplotlib, or image-generation model.
"""
import copy
import hashlib
import html
import json
import random
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parents[1]
OUT = BASE/'analysis/visuals/lds_actions'
OUT.mkdir(parents=True, exist_ok=True)
dist = json.loads((BASE/'analysis/visuals/lds_depth7/empirical_score_vectors.json').read_text())
BUDGET, DEPTH, K, SEED = 40, 6, 5, 17
nodes, actions = {}, []
fetch_count = jev_count = limit = 0
roots = [f'R{i}' for i in range(1, 11)]

def record(title, reason, focus=None, parent=None, kind='local'):
    actions.append(dict(number=len(actions)+1,title=title,reason=reason,focus=focus,parent=parent,
                        kind=kind,fetch=fetch_count,jev=jev_count,limit=limit,nodes=copy.deepcopy(nodes)))

for rank,nid in enumerate(roots,1):
    nodes[nid]=dict(id=nid,label=nid,parent=None,depth=1,rank=rank,score=None,
                    fetched=False,evaluated=False,disc=0,selected=False)
record('검색 결과 10개 도착', '아직 페이지 본문을 열지 않았다. 검색 결과의 제목·설명을 JEV에 함께 넣는다.',kind='search')
for nid,score in zip(roots,sorted(dist['entry_vectors'][1],reverse=True)):
    nodes[nid]['score']=score
jev_count+=1
record('JEV 1회로 검색 결과 10개 평가', '점수순으로 R1~R10을 정렬했다. 이것은 페이지 fetch가 아니다.',kind='jev')
for nid in roots[:5]: nodes[nid]['selected']=True
record('상위 5개를 필수 시작점으로 지정', 'R1~R5는 각각 이탈 0에서 시작한다. R6~R10은 이번 예시의 확장 대상에서 제외한다.')

def fetch_page(nid):
    global fetch_count,jev_count
    n=nodes[nid]
    assert not n['fetched']
    fetch_count+=1
    n.update(fetched=True,fetch=fetch_count)
    record(f'{n["label"]} 페이지 fetch', '본문을 가져왔다. 자식 후보의 JEV 평가는 아직 하지 않았다.',nid,n['parent'],'fetch')
    if n['depth']==DEPTH:
        n['capped']=True
        record(f'{n["label"]}: 깊이 6 도달', '확장 한도라 자식 평가를 생략한다. 실제 웹에 자식이 없다는 뜻은 아니다.',nid,n['parent'])
        return
    if fetch_count>=BUDGET:
        record(f'{n["label"]}: fetch 예산 소진', '더 확장할 예산이 없으므로 이 페이지의 자식 평가도 생략한다.',nid,n['parent'])
        return
    rng=random.Random(int.from_bytes(hashlib.sha256(f'{SEED}:{nid}'.encode()).digest()[:8],'big'))
    vector=rng.choice(dist['page_vectors'])[:K]
    n.update(evaluated=True,children=[])
    for rank,score in enumerate(vector,1):
        cid=nid+'.'+str(rank)
        nodes[cid]=dict(id=cid,label=f'n{len(nodes)-9:02}',parent=nid,depth=n['depth']+1,
                        rank=rank,score=score,disc=n['disc']+int(rank>1),fetched=False,evaluated=False)
        n['children'].append(cid)
    jev_count+=1
    description=('새 후보의 점수와 형제 순위를 알게 됐다. 후보를 발견한 것만으로 fetch 횟수는 늘지 않는다.'
                 if vector else '후보 묶음이 비어 있어 이 페이지에서는 더 내려갈 수 없다. 점수 기준으로 중단한 것이 아니다.')
    record(f'JEV: {n["label"]}에서 자식 후보 {len(vector)}개 확인',description,nid,nid,'jev')

for root in roots[:5]:
    record(f'{root} 선택: 필수 시작점', '먼저 시작점 5개를 모두 연다. 아직 특정 뿌리의 아래로 내려가지 않는다.',root)
    fetch_page(root)

def walk(nid):
    n=nodes[nid]
    if not n['fetched']:
        yield nid
    children=n.get('children',[])
    choices=children[1:]+children[:1] if n['disc']<limit else children[:1]
    for cid in choices:
        if nodes[cid]['disc']<=limit:
            yield from walk(cid)

for phase in range(DEPTH):
    if fetch_count>=BUDGET: break
    limit=phase
    record(f'이탈 {limit}회까지 허용하고 탐색',
           ('각 뿌리의 1순위 경로부터 본다. R1→R2→R3→R4→R5 순으로 fetch 기회를 번갈아 준다.' if limit==0 else
            f'이탈 {limit-1}회 이하에서 갈 곳이 끝났다. 허용량을 올리고, 저장된 후보에서 대안을 찾는다. 재-fetch는 하지 않는다.'))
    generators=[(r,walk(r)) for r in roots[:5]]
    while generators and fetch_count<BUDGET:
        remaining=[]
        for root,generator in generators:
            if fetch_count>=BUDGET: break
            try: nid=next(generator)
            except StopIteration: continue
            n=nodes[nid]; p=nodes[n['parent']]
            record(f'{root} 차례: {n["label"]} 선택',
                   f'{p["label"]}의 {n["rank"]}순위. 경로 이탈 {p["disc"]} + {int(n["rank"]>1)} = {n["disc"]}회, 허용 {limit}회 안에 든다.',nid,n['parent'])
            fetch_page(nid)
            remaining.append((root,generator))
        generators=remaining
record('종료',f'총 fetch {fetch_count}회. '+('40회 예산을 다 썼다. 남은 후보는 열지 않는다.' if fetch_count==BUDGET else '설정 안에서 더 열 후보가 없다.'))

# Validate causal visibility, accounting, and unique fetches.
assert sum(a['kind']=='fetch' for a in actions)==fetch_count
assert sum(a['kind']=='jev' for a in actions)==jev_count
assert len({n['fetch'] for n in nodes.values() if n['fetched']})==fetch_count
assert all(nodes[r]['fetched'] for r in roots[:5])
for a in actions:
    for n in a['nodes'].values():
        assert n['depth']<=DEPTH
        if n['parent']: assert a['nodes'][n['parent']]['evaluated']
        if not n['fetched']: assert not n.get('children')

def svg(a):
    ns=a['nodes']; W,H=1700,1230
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">',
           f'<title>Action {a["number"]}: {html.escape(a["title"])}</title>',
           '<style>text{font-family:"Malgun Gothic",sans-serif;fill:#192a3d} .small{fill:#5b697b}</style>',
           '<rect width="100%" height="100%" fill="#fff"/>']
    def text(x,y,s,size=22,color=None,anchor='start',bold=False):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}"'+
                     (f' style="fill:{color}"' if color else '')+(' font-weight="bold"' if bold else '')+'>'+html.escape(str(s))+'</text>')
    def line(x1,y1,x2,y2,color='#c4cdd7',dash=False):
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"'+(' stroke-dasharray="4 5"' if dash else '')+'/>')
    def box(x,y,w,h,fill,stroke):
        parts.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    text(45,48,f'Action #{a["number"]:03} / {len(actions)}  ·  {a["title"]}',32,bold=True)
    text(45,91,a['reason'],22)
    text(45,137,f'fetch {a["fetch"]}/40회     JEV {a["jev"]}회     허용 이탈 {a["limit"]}회     최대 깊이 6',25,bold=True)
    text(45,178,'주황 = 이번 대상  /  파랑 채움 = fetch 완료  /  빈 상자 = 미방문  /  +N = 발견했지만 아직 열지 않은 후보',20)
    text(45,219,'검색 10개',20,bold=True)
    for i,r in enumerate(roots):
        n=ns[r];x=235+i*145
        box(x,212,129,47,'#e8f1fb' if n['selected'] else '#f2f3f5','#3778b8' if n['selected'] else '#ccd2da')
        text(x,219,f'{r}  '+('?' if n['score'] is None else f'{n["score"]:.2f}'),20,anchor='middle')
    positions,collapsed={},{}
    cursor=0
    def layout(nid):
        nonlocal cursor
        n=ns[nid]
        kids=n.get('children',[])
        opened=[c for c in kids if ns[c]['fetched']]
        waiting=[c for c in kids if not ns[c]['fetched']]
        xs=[layout(c) for c in opened]
        if waiting:
            collapsed[nid]=(cursor,n['depth']+1,waiting)
            xs.append(cursor);cursor+=1
        if not xs: xs=[cursor];cursor+=1
        x=sum(xs)/len(xs)
        positions[nid]=(x,n['depth'])
        return x
    for r in roots[:5]: layout(r);cursor+=.7
    def xy(x,depth): return 125+x*1490/max(cursor-1,1),300+(depth-1)*104
    unit=1490/max(cursor-1,1)
    node_width=min(67,unit*.84)
    label_size=17 if node_width>=55 else 14
    for depth in range(1,7):
        y=300+(depth-1)*104
        text(24,y+8,f'd{depth}',19,color='#68778b')
        line(67,y,1650,y,'#f0f2f5')
    for nid,(x,depth) in positions.items():
        n=ns[nid]
        if n['parent']:
            px,py=xy(*positions[n['parent']]);cx,cy=xy(x,depth)
            line(px,py+23,cx,cy-23)
    for nid,(x,depth,waiting) in collapsed.items():
        px,py=xy(*positions[nid]);cx,cy=xy(x,depth)
        active=a['focus'] in waiting
        line(px,py+23,cx,cy-18,'#d58b30' if active else '#b8c2ce',True)
        box(cx,cy,min(51,unit*.65),35,'#fff7e9' if active else '#f3f5f7','#d58b30' if active else '#c4cdd7')
        text(cx,cy+6,f'+{len(waiting)}',14 if unit<65 else 18,anchor='middle')
    for nid,(x,depth) in positions.items():
        n=ns[nid];cx,cy=xy(x,depth)
        box(cx,cy,node_width,49,'#e7f1fc' if n['fetched'] else '#fff','#d27816' if a['focus']==nid else '#3976ad' if n['fetched'] else '#9aa8b8')
        text(cx,cy-3,n['label'],label_size,anchor='middle',bold=True)
        text(cx,cy+17,'?' if n['score'] is None else f'{n["score"]:.2f}',label_size-1,anchor='middle')
        status=''
        if n.get('capped'): status='깊이 한도'
        elif n['evaluated'] and not n.get('children'): status='후보 없음'
        elif n['fetched'] and not n['evaluated']: status='미평가'
        if status:
            if unit<65: status={'깊이 한도':'한도','후보 없음':'없음','미평가':'미평가'}[status]
            text(cx,cy+42,status,11 if unit<65 else 14,color='#677689',anchor='middle')
    line(45,886,1655,886)
    parent=a['parent']
    if parent and ns[parent]['evaluated']:
        pn=ns[parent]; kids=pn.get('children',[])
        text(45,925,f'이번 갈림길: {pn["label"]}의 자식 후보 · 부모 경로 이탈 {pn["disc"]}회',25,bold=True)
        if not kids: text(45,977,'자식 후보 없음. 이 경로는 여기서 끝난다.',23)
        for i,cid in enumerate(kids):
            n=ns[cid];cx=193+i*322
            active=cid==a['focus']
            box(cx,1000,291,109,'#e7f1fc' if n['fetched'] else '#fff7e9' if active else '#fff','#d27816' if active else '#a7b6c5')
            text(cx,978,f'{n["rank"]}순위  {n["label"]}  ·  {n["score"]:.2f}',22,anchor='middle',bold=True)
            text(cx,1012,f'경로 이탈 {n["disc"]}회 / 허용 {a["limit"]}회',20,anchor='middle')
            text(cx,1041,'fetch 완료' if n['fetched'] else '이번 선택' if active else '대기',18,anchor='middle')
    else:
        text(45,928,'진행 규칙',25,bold=True)
        text(45,971,'시작점 5개는 모두 이탈 0. 이후 1순위는 +0, 다른 순위는 +1. 뿌리별 fetch 기회는 번갈아 준다.',23)
        text(45,1017,'갈 곳이 없으면 허용 이탈을 늘린다. 이는 고정한 예시 정책이며 현재 서비스 코드의 동작은 아니다.',22)
    nxt=actions[a['number']]['title'] if a['number']<len(actions) else '없음 — 종료'
    text(45,1110,'다음 행동: '+nxt,24,bold=True)
    text(45,1160,'후보 점수 묶음은 실제 로그 분포에서 재추출한 가상 값. 자식은 fetch 후 JEV 평가 때만 공개한다.',19,color='#68778b')
    text(45,1197,'대기 후보는 트리에서 +N으로 묶고, 현재 갈림길의 개별 점수는 아래에 펼쳐 표시했다. 깊이 4~6은 분포 외삽이다.',18,color='#68778b')
    parts.append('</svg>')
    return ''.join(parts)

for a in actions:
    content=svg(a)
    ET.fromstring(content)
    (OUT/f'action_{a["number"]:03}.svg').write_text(content,encoding='utf-8')
manifest=[{k:v for k,v in a.items() if k!='nodes'} for a in actions]
(OUT/'actions.json').write_text(json.dumps(dict(config=dict(roots=5,depth=DEPTH,budget=BUDGET,seed=SEED),actions=actions),ensure_ascii=False,indent=2),encoding='utf-8')
template=(BASE/'analysis/lds_action_viewer_template.html').read_text(encoding='utf-8')
(OUT/'index.html').write_text(template.replace('__ACTION_DATA__',json.dumps(manifest,ensure_ascii=False)),encoding='utf-8')
print(json.dumps(dict(directory=str(OUT),actions=len(actions),fetch=fetch_count,jev=jev_count,
                      max_depth=max(n['depth'] for n in nodes.values() if n['fetched']),
                      deviation_changes=[a['number'] for a in actions if a['title'].startswith('이탈 ')]),ensure_ascii=True))
