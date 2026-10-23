import json,re
from pathlib import Path
from audit_lost_paths import ROOT,CURRENT,read
for q in (8,26,74,157):
 row=json.loads((ROOT/f'analysis/p35_lost_five/q{q}.json').read_text(encoding='utf-8'));ev=read(CURRENT/row['p35_record']['dir']/'trace.jsonl')
 print('\nDETAIL',q)
 for e in ev:
  if q==8 and e.get('search_id')=='0074dc1fad3046d3a829a910fc99ef4c' and e['event'] in ('rawtree.frontier','rawtree.inspection_selection','rawtree.fetch_failed','rawtree.preview'):print(json.dumps(e,ensure_ascii=False)[:7000])
  if q==74 and e['event']=='rawtree.frontier' and e.get('search_id')=='2cb6ce890c694dc28a29276ccbc30a3a':print(json.dumps(e,ensure_ascii=False)[:6000])
  if q==26 and e['event']=='fetch.raw' and 'List_of_foreign_Premier' in e.get('url',''):
   s=e['content'];print('LIST LENGTH',len(s),'error',e.get('is_error'))
   for m in re.finditer(r'Somali|Ibrahim',s,re.I):print(s[max(0,m.start()-140):m.end()+200])
  if q==157 and e['event']=='rawtree.entries':
   for r in e['candidates']:
    lead=r['lead']
    if 'simonstown.org' in lead['url'] or 'pdf' in lead['url']:print('PDF_CANDIDATE',e['search_id'],lead)
  if q==157 and e['event']=='fetch.raw' and 'simonstown.org' in e.get('url',''):print('PDF_FETCH',e.get('url'),e.get('is_error'),e['content'][:500])
