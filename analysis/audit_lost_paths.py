import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CURRENT=ROOT/'runs/test/20261022-2100_jevtree_gpt-oss-20b_browsecomp_raw_browser_p35_unified_score_50'
def read(path):return [json.loads(l) for l in path.read_text(encoding='utf-8').split('\n') if l.strip()]
terms={8:r'White Mischief|James Fox',26:r'Abdisalam|Somali',74:r'Rassoul|Diouf|Mankodiya|Nicholas Constant',128:r'Carlingwood|wasabi|bubblegum',157:r'Guinevere|Bierman'}
for q,pattern in terms.items():
 row=json.loads((ROOT/f'analysis/p35_lost_five/q{q}.json').read_text(encoding='utf-8'))
 nr=row['p35_record'];ev=read(CURRENT/nr['dir']/'trace.jsonl')
 print('\nTARGET',q)
 for e in ev:
  typ=e['event']
  if typ not in ('rawtree.entries','fetch.raw','rawtree.return','rawtree.preview','rawtree.links','jev.request'):continue
  s=json.dumps(e,ensure_ascii=False)
  hits=list(re.finditer(pattern,s,re.I))
  if not hits:continue
  print('HIT',typ,e.get('search_id'),e.get('node_id'),e.get('url',''), 'COUNT',len(hits))
  if typ=='rawtree.return':
   for r in e['returned']:
    t=json.dumps(r,ensure_ascii=False)
    if re.search(pattern,t,re.I):print('RETURN_SOURCE',r['source'])
  for m in hits[:3]:print(s[max(0,m.start()-160):m.end()+230])
 olddir=Path(row['old_run'])/row['old_record']['dir']
 old=json.loads((olddir/'response.json').read_text(encoding='utf-8'))
 print('OLD_TOOL_MATCHES')
 for i,step in enumerate(old['steps']):
  for call in step.get('tool_calls',[]):
   s=json.dumps(call,ensure_ascii=False)
   if re.search(pattern,s,re.I):
    print('STEP',i,'KEYS',list(call),'ARGS',call.get('arguments'))
    for m in list(re.finditer(pattern,s,re.I))[:4]:print(s[max(0,m.start()-220):m.end()+350])
