"""Export real LDS actions to individual SVGs and an offline replay viewer.

python -m searchgym.lds_visualize runs/test/<run>
Uses logged deltas only: no future descendants leak into earlier frames.
"""
from __future__ import annotations
import argparse
import html
import json
import math
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

TITLES={"entry_ranked":"검색 결과 JEV 평가 완료", "select":"다음 fetch 대상 선택",
        "fetch_start":"fetch 시작", "fetch_end":"fetch 응답 도착", "fetch_failed":"fetch 실패",
        "duplicate":"중복 본문 확인", "skip":"이미 방문한 URL 건너뜀", "jev_start":"JEV 평가 시작",
        "jev_end":"JEV 평가 응답", "jev_failed":"JEV 평가 실패", "candidates":"자식 후보 공개",
        "roots_ready":"시작점 확보 완료", "phase":"허용 이탈 단계 변경", "expansion_end":"트리 확장 종료",
        "reader_selection":"reader에 넘길 문서 선택", "search_end":"독해 및 검색 종료"}
STATUS={"pending":"대기", "reserved":"선택", "fetching":"요청 중", "fetch_returned":"평가 전",
        "scoring":"평가 중", "scored":"평가 완료", "failed":"실패", "duplicate":"중복",
        "skipped_visited":"방문 중복", "score_failed":"평가 실패", "depth_limit":"깊이 한도",
        "ready":"확장 가능", "no_candidates":"후보 없음"}


def render(action,known,config,query,total):
    focus={n['id'] for n in action['updates']}
    if action['kind'] in ('entry_ranked','search_end','roots_ready'): focus=set()
    parent=action.get('parent_id') or next((known[i].get('parent_id') for i in focus if known[i].get('parent_id')),None)
    roots=[n for n in known.values() if not n['parent_id']]
    roots.sort(key=lambda n:n['rank'])
    visible_roots=[n for n in roots if n.get('fetch_order') or n['rank']<=config['entries']]
    positions,groups={},{}
    cursor=0
    def layout(n):
        nonlocal cursor
        children=[known[c] for c in n['children'] if c in known]
        opened=[c for c in children if c.get('fetch_order') or c['id'] in focus]
        pending=[c for c in children if c not in opened]
        xs=[layout(c) for c in opened]
        if pending:
            groups[n['id']]=(cursor,n['depth']+1,len(pending));xs.append(cursor);cursor+=1
        if not xs: xs=[cursor];cursor+=1
        positions[n['id']]=(sum(xs)/len(xs),n['depth'])
        return positions[n['id']][0]
    for root in visible_roots: layout(root);cursor+=.8
    W=max(1700,math.ceil(cursor)*65+200);H=1280
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">',
           f'<title>Action {action["action"]}: {TITLES[action["kind"]]}</title>',
           '<style>text{font-family:"Malgun Gothic",sans-serif;fill:#172c40}</style>',
           '<rect width="100%" height="100%" fill="white"/>']
    def text(x,y,s,size=22,anchor='start',color='#172c40'):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" style="fill:{color}">{html.escape(str(s))}</text>')
    def box(x,y,w,h,fill,stroke):
        parts.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    def line(x,y,u,v,color='#cad3df',dash=False):
        parts.append(f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="{color}" stroke-width="2"'+(' stroke-dasharray="4 5"' if dash else '')+'/>')
    text(40,43,f'Action #{action["action"]} / {total}  ·  {TITLES[action["kind"]]}',31)
    text(40,86,'검색어: '+query[:125],22)
    text(40,128,f'fetch 시도 {action["fetch_attempts"]}/{config["fetch_budget"]}  ·  허용 이탈 {action["discrepancy_limit"]}  ·  검색 시작 후 {action["elapsed_ms"]/1000:.1f}초',24)
    text(40,168,'주황 = 이번 행동  /  파랑 = 요청한 페이지  /  빨강 = 실패·중복  /  +N = 발견한 대기 후보',20)
    for i,n in enumerate(roots):
        x=100+i*(W-170)/max(len(roots),1)
        box(x,217,125,49,'#eaf2fc' if n.get('fetch_order') else '#f4f5f6','#9db0c4')
        text(x,211,f'R{n["rank"]} · {n["id"]}',16,'middle')
        text(x,234,f'{n["score"]:.2f}',18,'middle')
    def xy(x,depth):return 105+x*(W-180)/max(cursor-1,1),307+(depth-1)*103
    for dep in range(1,config['depth']+1):
        y=307+(dep-1)*103;line(65,y,W-40,y,'#f1f3f5');text(15,y+6,f'd{dep}',19)
    for nid,pos in positions.items():
        n=known[nid]
        if n['parent_id']:
            px,py=xy(*positions[n['parent_id']]);cx,cy=xy(*pos);line(px,py+25,cx,cy-25)
    for nid,(x,depth,count) in groups.items():
        px,py=xy(*positions[nid]);cx,cy=xy(x,depth);line(px,py+25,cx,cy,'#bdc7d3',True)
        box(cx,cy,35,32,'#f5f6f8','#c2cbd7');text(cx,cy+6,f'+{count}',16,'middle')
    for nid,pos in positions.items():
        n=known[nid];cx,cy=xy(*pos)
        bad=n['status'] in ('failed','duplicate','score_failed')
        box(cx,cy,57,52,'#fbe9e7' if bad else '#e8f1fb' if n.get('fetch_order') else '#fff', '#df861c' if nid in focus else '#a3b4c6')
        text(cx,cy-5,nid,14,'middle');text(cx,cy+17,f'{n["score"]:.2f}',16,'middle')
        text(cx,cy+42,'reader' if n['read'] else STATUS[n['status']],12,'middle','#647387')
    line(40,883,W-40,883)
    focus_id=next(iter(sorted(focus)),None)
    if focus_id:
        n=known[focus_id]
        text(40,921,f'{focus_id}: '+n['url'][:145],21)
        if n['error']:text(40,958,'오류: '+n['error'].replace('\n',' ')[:135],19,color='#9a352a')
        elif n['parent_id']:
            text(40,958,f'부모 {n["parent_id"]}의 {n["rank"]}순위 · 경로 이탈 {n["discrepancy"]}회 · 상태 {STATUS[n["status"]]}',22)
        else:text(40,958,'검색 결과에서 확보한 시작점. 뿌리의 순위와 관계없이 경로 이탈은 0.',22)
    else:
        text(40,921,action['reason'][:145],21)
    if parent and parent in known:
        pn=known[parent];kids=[known[c] for c in pn['children'] if c in known]
        text(40,1005,f'현재 갈림길: {parent}의 후보',22)
        for i,n in enumerate(kids[:config['candidates_per_parent']]):
            x=190+i*320
            box(x,1060,292,76,'#fff4df' if n['id'] in focus else '#f4f7fa','#c0cbd6')
            text(x,1048,f'{n["rank"]}순위 {n["id"]} · {n["score"]:.2f}',20,'middle')
            text(x,1080,f'이탈 {n["discrepancy"]} · {STATUS[n["status"]]}',18,'middle')
    else:
        text(40,1010,'같은 차례의 뿌리들을 병렬 처리한다. 점수는 같은 부모 안에서의 순위에만 사용한다.',22)
    text(40,1158,'기록: '+action['reason'][:145],19)
    text(40,1201,'실제 실행 로그 재생 · 완료된 요청/평가만 반영 · 원문·전체 후보·시각은 structure.json / actions.jsonl / pages/에 저장',18,color='#647387')
    text(40,1240,'fetch 수는 논리적 요청 시도 수. 전송 계층의 HTTP 재시도는 포함하지 않는다. 부모로 돌아갈 때 재-fetch하지 않는다.',18,color='#647387')
    parts.append('</svg>')
    return ''.join(parts)


def export_run(run):
    run=Path(run).resolve();out=run/'lds_viewer';out.mkdir(exist_ok=True)
    groups=[]
    for qdir in sorted(run.glob('q*')):
        structures=sorted(qdir.glob('lds/*/structure.json'),key=lambda p:p.stat().st_mtime)
        for si,path in enumerate(structures,1):
            data=json.loads(path.read_text(encoding='utf-8'))
            actions_path=path.parent/'actions.jsonl'
            actions=[json.loads(l) for l in actions_path.read_text(encoding='utf-8').splitlines()]
            relative=f'{qdir.name}/search_{si:02}'
            target=out/relative;target.mkdir(parents=True,exist_ok=True)
            known={};frames=[]
            for a in actions:
                known.update({n['id']:n for n in a['updates']})
                name=f'action_{a["action"]:04}.svg'
                content=render(a,known,data['config'],data['query'],len(actions))
                ET.fromstring(content)
                (target/name).write_text(content,encoding='utf-8')
                frames.append(dict(path=f'{relative}/{name}',action=a['action'],title=TITLES[a['kind']],
                                   fetch=a['fetch_attempts'],seconds=round(a['elapsed_ms']/1000,1)))
            groups.append(dict(label=f'{qdir.name} · 검색 {si}: {data["query"]}',frames=frames,
                               structure=f'../{qdir.name}/lds/{data["search_id"]}/structure.json'))
    template=Path(__file__).with_name('lds_viewer.html').read_text(encoding='utf-8')
    embedded=json.dumps(groups,ensure_ascii=False).replace('<','\\u003c')
    (out/'index.html').write_text(template.replace('__GROUPS__',embedded),encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf-8')
    return dict(viewer=str(out/'index.html'),searches=len(groups),svgs=sum(len(g['frames']) for g in groups))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run_dir')
    print(json.dumps(export_run(p.parse_args().run_dir),ensure_ascii=False))
