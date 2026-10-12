"""Online reveal demo: only the environment owns the hidden logged subtree."""
import copy
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / 'visuals'
source = json.loads((OUT / 'lds_q660_simulation.json').read_text(encoding='utf-8'))
hidden = {n['id']: n for n in source['nodes']}

def candidate(nid):
    n = hidden[nid]
    return {k: n[k] for k in ['id', 'label', 'url', 'parent', 'depth',
                              'rank_among_retained_siblings', 'link_score', 'discrepancies']}

def fetch_environment(nid):
    # This is the ONLY place the scheduler learns a page's score and children.
    n = hidden[nid]
    return {'direct_answer': n['direct_answer'],
            'children': [candidate(cid) for cid in n['children']]}

known = {'R': candidate('R')}
visited = []
snapshots = []
limit = 0
H, BUDGET = 3, 10

def snapshot(next_id=None):
    return {'fetches': len(visited), 'limit': limit, 'next': next_id,
            'order': list(visited), 'known': copy.deepcopy(known)}

snapshots.append(snapshot('R'))

def expand(nid, used):
    n = known[nid]
    if not n.get('fetched'):
        if len(visited) >= BUDGET:
            return
        snapshots[-1]['next'] = nid
        snapshots[-1]['limit'] = limit
        result = fetch_environment(nid)
        n.update(fetched=True, direct_answer=result['direct_answer'], children=[])
        visited.append(nid)
        if n['depth'] < H:
            for child in result['children']:
                known[child['id']] = child
                n['children'].append(child['id'])
        snapshots.append(snapshot())
    if len(visited) >= BUDGET or n['depth'] >= H:
        return
    kids = n['children']
    choices = kids[1:] + kids[:1] if used < limit else kids[:1]
    for cid in choices:
        cost = int(known[cid]['rank_among_retained_siblings'] > 1)
        if used + cost <= limit:
            expand(cid, used + cost)

for limit in range(H):
    expand('R', 0)
    if len(visited) >= BUDGET:
        break

assert visited == ['R', 'A', 'A1', 'B', 'B1', 'C', 'C1', 'A2', 'A3', 'B2']
for state in snapshots:
    for nid, n in state['known'].items():
        if n['parent']:
            assert state['known'][n['parent']].get('fetched')
        if not n.get('fetched'):
            assert 'direct_answer' not in n and 'children' not in n
assert 'B2' not in snapshots[3]['known']
assert 'B2' in snapshots[4]['known'] and 'direct_answer' not in snapshots[4]['known']['B2']

data = {
    'source': source['source'], 'source_search': 4, 'source_root': 3,
    'description': 'Online expansion against a hidden, pruned, observed subtree fixture; not a full web replay.',
    'policy': 'Multiway LDS; non-first sibling costs 1; early deviations first; cached pages reused.',
    'depth_cap': H, 'fetch_budget': BUDGET,
    'limitations': [
        'Only 13 previously observed successful pages; duplicate removed. Other links and failures excluded.',
        'Depth 3 means expansion cap, not a claim that the web pages have no outgoing links.',
        'One root only. Full-search root scheduling and direct/query budget split remain undesigned.',
        'New query-answer scoring does not exist in these logs; incoming link scores are historical original-question scores.',
        'No ground truth or future page scores are used by the scheduler.',
        'The original run found Glover evidence but still answered incorrectly.',
    ],
    'snapshots': snapshots,
}
(OUT / 'lds_online_expansion.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

W, HEIGHT = 2400, 2790
BG, INK, MUTED, LINE = '#F8FAFC', '#15283E', '#53657A', '#CCD6E1'
BLUE, PALE, ORANGE = '#276CB0', '#E4EFFA', '#BD6713'
im = Image.new('RGB', (W, HEIGHT), BG)
d = ImageDraw.Draw(im)
fonts = {}
def text(x, y, s, size=26, fill=INK, bold=False, anchor=None):
    key = (size, bold)
    if key not in fonts:
        fonts[key] = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf' if bold else 'C:/Windows/Fonts/malgun.ttf', size)
    d.text((x,y), s, font=fonts[key], fill=fill, anchor=anchor)

text(80, 45, 'LDS로 트리를 만들어 가기', 58, bold=True)
text(82, 128, 'fetch → 페이지 평가 + 자식 후보 발견 → 다음 fetch 선택 → 반복', 33, BLUE, True)
text(82, 185, 'q660 로그의 한 뿌리를 숨겨 둔 환경으로 사용. 탐색기는 열린 페이지에서 얻은 정보만 볼 수 있다.', 27, MUTED)
text(82, 232, '예시 설정: fetch 예산 10회 · 최대 깊이 3 · 1순위 선택은 이탈 0, 2·3순위 선택은 이탈 +1', 27, MUTED)
d.line((80, 291, 2320, 291), fill=LINE, width=2)
text(80, 315, '파랑 채움 = fetch 완료     빈 상자 = 발견만 한 후보     주황 테두리 = 다음 fetch', 27, bold=True)
text(80, 361, '미발견 노드는 그리지 않는다. L = 부모에서 받은 링크 점수 / D = fetch 후 알게 되는 direct_answer', 25, MUTED)

panel_steps = [0, 1, 2, 3, 4, 10]
titles = [
    '시작: 검색에서 뿌리 R만 받은 상태',
    'R을 열자 A·B·C가 처음 등장',
    'A를 열자 A1·A2·A3가 처음 등장',
    'A1은 깊이 한도. 이탈 허용을 1로 올림',
    'B를 열고서야 Glover 링크를 발견',
    '10회 예산 소진: B2 본문까지 확보',
]
notes = [
    ['R의 본문·D·자식 링크는 아직 모른다.', '다음: R을 fetch.'],
    ['A·B·C의 D는 모두 모른다.', '형제 1순위 A를 선택한다.'],
    ['B의 자식은 여전히 전혀 모른다.', 'A의 1순위 A1을 선택한다.'],
    ['이탈 0으로 더 열 수 있는 후보가 없다.', '이번 변형은 얕은 갈림길 B부터 바꾼다.'],
    ['B2의 URL은 알지만 본문·D는 모른다.', 'B까지 이탈 1회 사용 → 우선 B1로 간다.'],
    ['B2: 2순위 → 2순위, 누적 이탈 2회.', '정답 여부가 아니라 정한 예산 때문에 멈춘다.'],
]

for pi, step in enumerate(panel_steps):
    state = snapshots[step]
    ox = 80 + (pi % 2) * 1200
    oy = 440 + (pi // 2) * 605
    text(ox, oy, f'{pi+1:02}  {titles[pi]}', 31, bold=True)
    fetched = state['fetches']
    pending = len(state['known']) - fetched
    text(ox, oy+51, f'fetch {fetched}/10   ·   대기 {pending}개   ·   허용 이탈 {state["limit"]}회', 25, MUTED)
    pos = {'R': (ox+530, oy+145), 'A': (ox+170, oy+265),
           'B': (ox+530, oy+265), 'C': (ox+890, oy+265)}
    for p, start in [('A', 52), ('B', 412), ('C', 772)]:
        for i in range(1,4):
            pos[p+str(i)] = (ox+start+(i-1)*118, oy+398)
    for nid, n in state['known'].items():
        if n['parent']:
            px,py = pos[n['parent']]; x,y = pos[nid]
            d.line((px,py+34,x,y-34), fill=LINE, width=3)
    for nid,n in state['known'].items():
        x,y = pos[nid]
        done = n.get('fetched', False)
        chosen = state['next'] == nid
        width = 200 if len(nid)==1 else 112
        d.rounded_rectangle((x-width/2,y-37,x+width/2,y+37), radius=8,
                            fill=PALE if done else '#FFFFFF',
                            outline=ORANGE if chosen else BLUE if done else LINE,
                            width=4 if chosen else 2)
        label = nid if len(nid)>1 else nid+' '+{'R':'작가 소개','A':'화랑 소개','B':'작가 목록','C':'화랑 소식'}[nid]
        text(x,y-15,label,23,bold=True,anchor='mm')
        score = f'D {n["direct_answer"]:.2f}' if done else f'L {n["link_score"]:.2f}'
        text(x,y+16,score,21,BLUE if done else MUTED,anchor='mm')
        if len(nid)>1:
            text(x,y+57, '깊이 한도' if done else 'D ? / 자식 ?', 17, MUTED, anchor='mm')
    text(ox, oy+484, notes[pi][0], 26, bold=True)
    text(ox, oy+525, notes[pi][1], 25, MUTED)

d.line((80, 2270, 2320, 2270), fill=LINE, width=2)
text(80, 2300, '온라인 시뮬레이션의 fetch 순서', 32, bold=True)
text(80, 2353, '이탈 0: R → A → A1     |     이탈 1: B → B1 → C → C1 → A2 → A3     |     이탈 2: B2', 29, BLUE, True)
text(80, 2410, 'A1 = Ecotechnics / A2·A3 = 이미지 / B1 = 이미지 / B2 = Ablade Glover / B3 = Wilde', 24, MUTED)
text(80, 2450, 'C1 = 교육 사이트 / C2 = Benji Reid / C3 = 전시 페이지. 예산 종료 시 B3·C2·C3는 아직 대기 중.', 24, MUTED)
text(80, 2520, '이 그림이 보여 주는 것: 전체 트리 없이도, 발견된 후보의 형제 순위만으로 확장 순서를 정한다.', 29, bold=True)
text(80, 2571, '아직 정해야 할 것: 깊이 한도 · 여러 뿌리의 배분 · 원 질문/검색 쿼리 목적별 예산과 순위.', 28, bold=True)
text(80, 2630, '관측된 성공 문서 13개로 후보를 제한한 설명용 환경이다. 미방문 링크·실패·다른 뿌리는 생략했다.', 24, MUTED)
text(80, 2671, '깊이 3에서 자식을 멈춘 것은 설계 한도이지 실제 웹의 끝이 아니다. 새 쿼리 목적 점수도 아직 없다.', 24, MUTED)
text(80, 2712, 'Glover는 사후 확인한 정답 근거이며 정책은 이를 모른다. 원 실행은 이 근거를 얻고도 최종 오답이었다.', 24, MUTED)
path = OUT / 'lds_online_expansion.png'
im.save(path)
print(json.dumps({'image':str(path), 'order':visited, 'validated_snapshots':len(snapshots)}, ensure_ascii=False))
