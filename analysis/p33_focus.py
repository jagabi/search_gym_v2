exec((__import__('pathlib').Path(__file__).parent/'p33_target_audit.py').read_text(encoding='utf-8').split('for q in (57,516')[0])
for q,term in [(516,'The_Fifth_Estate'),(598,'apl-apl0000357'),(598,'timeuse.org'),(1196,'704082208')]:
    ev=events(RUN/f'q{q:05d}'/'trace.jsonl')
    targets={(e['search_id'],e['node_id']) for e in ev if e['event']=='rawtree.preview' and term.lower() in e['url'].lower()}
    print('\nTARGET',q,term,targets)
    for sid,nid in targets:
        for e in ev:
            if e.get('search_id')!=sid:continue
            if e['event']=='rawtree.start':print('QUERY',e['query'])
            if e['event']=='rawtree.preview':print('PREVIEW',e['node_id'],e['url'],e['scores'])
            if e['event']=='rawtree.inspection_selection':print('INSPECTION',e['depth'],e['selected'])
            if e.get('node_id')==nid and e['event']=='rawtree.bundles':print('BUNDLES',json.dumps(e,ensure_ascii=False)[:6000])
            if e['event']=='rawtree.return':print('RETURN_SOURCES',[x['source'] for x in e['returned']])
    if q==598 and 'apl' in term:
        for e in ev:
            if e['event']=='fetch.raw' and term in e.get('url',''):
                c=e.get('content','')
                print('APA_START',c[:1700])
                for word in ['HDS','2007','2012','Acknowledg','Hogan']:
                    p=c.lower().find(word.lower());print('APA_TERM',word,c[max(0,p-80):p+250] if p>=0 else 'ABSENT')
allrows=[]
for r in [json.loads(x) for x in (RUN/'records.jsonl').read_text(encoding='utf-8').splitlines()]:
    ev=events(RUN/r['dir']/'trace.jsonl'); http=[e['duration_ms']/1000 for e in ev if e['event']=='jev.response']
    allrows.extend(http)
    print('ROW',r['index'], 'DECISION',len(http),'FAIL',sum(e['event']=='rawtree.fetch_failed' for e in ev),'FETCH',sum(e['event']=='fetch.raw' for e in ev))
import statistics
print('HTTP',len(allrows),statistics.mean(allrows),statistics.median(allrows),sorted(allrows)[int(.95*len(allrows))],max(allrows))
