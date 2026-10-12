"""Render a deterministic LDS illustration from q660's observed subtree.

No network, application edits, or new model calls. Simulation is intentionally
limited to already-observed successful pages; it is not a replay of live crawling.
"""
import json
from collections import deque
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'analysis/visuals'
OUT.mkdir(exist_ok=True)
RUN = ROOT/'runs/test/20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10/q00660'
tree = json.loads((RUN/'explorer.json').read_text(encoding='utf-8'))[3]
origin = tree['opened'][2]
labels = {
    'R': 'El Anatsui 소개', 'A': '화랑 소개', 'B': '작가 목록', 'C': '화랑 소식',
    'A1': 'Ecotechnics', 'A2': '건물 이미지', 'A3': '전시 이미지',
    'B1': '작가 이미지', 'B2': 'Ablade Glover', 'B3': 'Wilde 소개',
    'C1': '교육 사이트', 'C2': 'Benji Reid 소개', 'C3': '전시 페이지',
}
nodes = {}


def add(raw, nid, parent=None, rank=0, disc=0):
    nodes[nid] = {
        'id': nid, 'label': labels[nid], 'url': raw['urls'][0],
        'parent': parent, 'rank_among_retained_siblings': rank,
        'discrepancies': disc, 'depth': raw['depth'],
        'link_score': raw.get('link_score'),
        'direct_answer': raw.get('identification_score'),
        'answer_likelihood': raw.get('verification_score'), 'children': [],
    }
    valid = [c for c in raw.get('opened', []) if not c.get('error')]
    for i, child in enumerate(valid, 1):
        cid = chr(64+i) if nid == 'R' else nid+str(i)
        nodes[nid]['children'].append(cid)
        add(child, cid, nid, i, disc + int(i > 1))


add(origin, 'R')
assert len(nodes) == 13
assert nodes['B2']['url'].endswith('/artists/glover')
assert nodes['B2']['discrepancies'] == 2

# A deterministic multiway LDS variant. Any non-first child consumes one
# discrepancy; rank 2 precedes rank 3. At equal discrepancy budget, try an early
# deviation before a later one. Revisited pages are cached and incur no new visit.
seen, order, phases = set(), [], []
for limit in range(3):
    fresh = []

    def dfs(nid, used):
        if nid not in seen:
            seen.add(nid)
            order.append(nid)
            fresh.append(nid)
        kids = nodes[nid]['children']
        if not kids:
            return
        choices = kids[1:]+kids[:1] if used < limit else kids[:1]
        for cid in choices:
            cost = int(nodes[cid]['rank_among_retained_siblings'] > 1)
            if used+cost <= limit:
                dfs(cid, used+cost)

    dfs('R', 0)
    phases.append({'limit': limit, 'new_visits': fresh, 'cumulative': list(order)})

queue, bfs = deque(['R']), []
while queue:
    nid = queue.popleft()
    bfs.append(nid)
    queue.extend(nodes[nid]['children'])
assert len(order) == len(set(order)) == 13
assert order.index('B2')+1 == 10 and bfs.index('B2')+1 == 9
for seq in [order, bfs]:
    for i, nid in enumerate(seq):
        assert nodes[nid]['parent'] is None or nodes[nid]['parent'] in seq[:i]

data = {
    'source': str(RUN/'explorer.json'), 'search_number': 4, 'root_number': 3,
    'query': tree['query'],
    'method': 'Multiway LDS; any non-first child costs one discrepancy; early deviations first; tie order follows retained original sibling order; cache shared visits.',
    'assumptions': [
        'Only 13 observed successful pages under root 3 are available.',
        'One duplicate child under the news page is removed; remaining siblings retain order.',
        'Unvisited links, other roots, failed fetches, parallelism and elapsed time are excluded.',
        'One new document counts as one simulated visit. Actual elapsed time and success rate are not estimated.',
        'Ground-truth highlight is for the reader of the diagram, never used by the policy.',
        'Actual q660 run found and summarized Glover, but the final answer was wrong.',
    ],
    'nodes': list(nodes.values()), 'lds': order, 'phases': phases, 'bfs': bfs,
    'target_first_visit': {'lds': 10, 'bfs': 9},
}
(OUT/'lds_q660_simulation.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

W, H = 2200, 2230
BG, INK, MUTED = '#F7F8FA', '#142538', '#526174'
LINE, PANEL = '#CAD3DF', '#FFFFFF'
PHASE = ['#2676C8', '#C4771E', '#7C59B9']
LIGHT = ['#E7F0FB', '#FCF0DF', '#F0EAF8']
GREEN, GREEN_BG = '#157858', '#E4F4EC'
im = Image.new('RGB', (W,H), BG)
d = ImageDraw.Draw(im)
FONT = 'C:/Windows/Fonts/malgun.ttf'
BOLD = 'C:/Windows/Fonts/malgunbd.ttf'


def text(x,y,s,size=26,fill=INK,bold=False,anchor=None):
    f = ImageFont.truetype(BOLD if bold else FONT,size)
    d.text((x,y),s,font=f,fill=fill,anchor=anchor)


def box(x,y,w,h,fill=PANEL,border=LINE,width=2,radius=14):
    d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),radius=radius,fill=fill,outline=border,width=width)


def edge(p1,p2,fill=LINE,width=3):
    d.line([p1,p2],fill=fill,width=width)


text(90,58,'LDS는 낮은 점수의 경유지를 언제 방문할까?',54,bold=True)
text(92,139,'q660 실제 로그 기반  ·  검색 4의 세 번째 뿌리  ·  탐색 순서만 바꾼 시뮬레이션',27,MUTED)
d.line((90,200,2110,200),fill=LINE,width=2)
text(90,229,'원 검색',24,MUTED)
text(230,225,tree['query'],30,bold=True)
text(90,280,'실제 경로',24,MUTED)
text(230,276,'El Anatsui 소개  →  작가 목록  →  Ablade Glover',30,bold=True)
text(90,326,'중복 1개를 제외한 성공 문서 13개. 이름·점수·부모-자식 관계는 로그 값이다.',24,MUTED)

pos = {'R':(1100,444),'A':(410,615),'B':(1100,615),'C':(1790,615)}
for parent,xs in [('A',[170,410,650]),('B',[860,1100,1340]),('C',[1550,1790,2030])]:
    for i,x in enumerate(xs,1):pos[parent+str(i)] = (x,843)

for nid,n in nodes.items():
    if not n['parent']:continue
    x,y=pos[nid];px,py=pos[n['parent']]
    highlight=nid in ['B','B2']
    edge((px,py+48),(x,y-51),GREEN if highlight else LINE,5 if highlight else 3)
    if len(nid)==1:
        text((x+px)/2,(y+py)/2+2,f"{n['rank_among_retained_siblings']}순위",24,GREEN if highlight else MUTED,anchor='mm')

for nid,n in nodes.items():
    x,y=pos[nid];target=nid=='B2';bridge=nid=='B'
    width=310 if len(nid)==1 else 212
    box(x,y,width,108,GREEN_BG if target or bridge else PANEL,GREEN if target or bridge else LINE,3 if target or bridge else 2)
    text(x,y-31,f"{nid}  {n['label']}",25 if len(nid)==1 else 23,bold=True,anchor='mm')
    score=f"D {n['direct_answer']:.2f}" if nid=='R' else f"L {n['link_score']:.2f}   D {n['direct_answer']:.2f}"
    text(x,y+9,score,24,MUTED,anchor='mm')
    if len(nid)==2:text(x,y+36,f"형제 {n['rank_among_retained_siblings']}순위",20,MUTED,anchor='mm')

text(1100,965,'L = 링크 점수   ·   D = 원 질문 direct_answer   ·   확장에는 D가 아니라 링크의 형제 순위를 사용',24,MUTED,anchor='mm')
text(1100,1007,'정답 근거로 가는 선택은 2순위 → 2순위. 따라서 1순위에서 두 번 벗어나야 한다.',28,GREEN,bold=True,anchor='mm')
d.line((90,1060,2110,1060),fill=LINE,width=2)

def miniature(cx,phase):
    x0=cx-300
    p={'R':(cx,1235),'A':(x0+100,1330),'B':(x0+300,1330),'C':(x0+500,1330)}
    for parent,start in [('A',35),('B',235),('C',435)]:
        for i in range(1,4):p[parent+str(i)]=(x0+start+(i-1)*65,1440)
    visited=set(phases[phase]['cumulative']);fresh=set(phases[phase]['new_visits'])
    for nid,n in nodes.items():
        if n['parent']:
            edge(p[n['parent']],p[nid],PHASE[phase] if nid in fresh else LINE,3)
    for nid,(x,y) in p.items():
        active=nid in fresh;old=nid in visited and not active
        fill=LIGHT[phase] if active else '#E4E9EF' if old else PANEL
        border=PHASE[phase] if active else LINE
        if nid=='B2' and nid in visited:fill,border=GREEN_BG,GREEN
        d.ellipse((x-24,y-24,x+24,y+24),fill=fill,outline=border,width=3 if active else 2)
        text(x,y,nid,22,INK if nid in visited else '#8C99A8',bold=True,anchor='mm')
        if nid in visited:text(x,y+39,f"#{order.index(nid)+1}",18,MUTED,anchor='mm')

for k,cx in enumerate([395,1100,1805]):
    text(cx,1120,f"단계 {k}  ·  이탈 {k}회까지",30,PHASE[k],True,anchor='mm')
    text(cx,1170,f"새 문서 +{len(phases[k]['new_visits'])}개  /  누적 {len(phases[k]['cumulative'])}개",24,MUTED,anchor='mm')
    miniature(cx,k)
    subtitle=['1순위만 끝까지 따라간다','한 지점에서 2·3순위도 허용한다','두 지점에서 바꿔 Glover에 도달한다'][k]
    text(cx,1534,subtitle,25,bold=True,anchor='mm')

text(90,1612,'같은 부모에서 2순위·3순위 모두 ‘이탈 1회’. 이 그림은 얕은 지점의 변경을 먼저 살피는 LDS 변형이다.',23,MUTED)
d.line((90,1660,2110,1660),fill=LINE,width=2)
text(90,1691,'새 문서 방문 순서',33,bold=True)
text(570,1698,'숫자는 시뮬레이션 순서이며 실제 요청 시각이 아니다.',23,MUTED)

phase_of={nid:k for k,p in enumerate(phases) for nid in p['new_visits']}
for y,label,seq in [(1800,'LDS',order),(1896,'너비우선',bfs)]:
    text(90,y,label,28,bold=True,anchor='lm')
    for i,nid in enumerate(seq):
        x=340+i*140
        fill=LIGHT[phase_of[nid]] if label=='LDS' else '#EEF1F5'
        border=GREEN if nid=='B2' else BG
        box(x,y,123,73,GREEN_BG if nid=='B2' else fill,border,4 if nid=='B2' else 1,10)
        text(x,y-13,nid,25,bold=True,anchor='mm')
        text(x,y+17,str(i+1),19,MUTED,anchor='mm')

text(90,1970,'이 부분트리에서는 LDS가 더 빠르지 않다.',31,bold=True)
text(90,2020,'Glover 근거 도달: LDS 10번째 / 너비우선 9번째. 이탈을 1회까지만 허용하면 Glover는 방문하지 않는다.',25)
text(90,2072,'범위: 깊이 3의 관측된 부분트리만 사용. 다른 뿌리·미방문 링크·실패·병렬 처리·소요시간은 제외.',23,MUTED)
text(90,2110,'초록색은 사후에 확인한 정답 근거 표시이며 탐색 정책에는 사용하지 않았다. 실제 q660의 최종 답은 오답이었다.',23,MUTED)
text(90,2165,'핵심: LDS는 무작위 탐색이 아니라, 좋은 순위에서 벗어나는 횟수를 늘려가며 대안을 탐색하는 순서다.',25,bold=True)

png=OUT/'lds_q660_simulation.png'
im.save(png)
print(json.dumps({'image':str(png),'size':im.size,'lds':order,'bfs':bfs,'phases':phases},ensure_ascii=False))
