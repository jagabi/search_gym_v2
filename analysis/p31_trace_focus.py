exec((__import__('pathlib').Path(__file__).parent/'diagnose_p31.py').read_text(encoding='utf-8').split('summaries=[]')[0])
for q in (326,516,598,746,1196,1230):
    ev=[json.loads(s) for s in (RUN/f'q{q:05}'/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    req={e['request_id']:e for e in ev if e['event']=='jev.request'}
    print('\nQ',q)
    if q in (326,598):
        for e in ev:
            if e['event']=='rawtree.return':
                print('RETURN_SOURCES',[s['source'] for s in e['returned']])
                if q==326:
                    text=e['text'];pos=text.lower().find('baby');print('BABY',text[max(0,pos-250):pos+400])
    for e in ev:
        if e['event']=='rawtree.links' and q==516:
            chosen=[x for x in e['links'] if x.get('score',0) is not None and x.get('score',0)>.3]
            if chosen:print('HIGH_LINKS',e['search_id'],e['node_id'],[(x['url'],round(x['score'],3),x['anchor']) for x in chosen][:15])
        if e['event']=='rawtree.frontier' and q==516: print('FRONTIER',e['search_id'],e['depth'],e['candidates'],e['selected'])
        if e['event']=='rawtree.return' and q==1196:
            text=e['text'];pos=text.lower().find('3.25');
            if pos>=0:print('3.25_RETURN',text[max(0,pos-180):pos+300])
        if e['event']=='tool.result' and q==1196:
            pass
        if e['event']=='rawtree.preview' and q==746 and any(t in e['url'].lower() for t in ('minnesota','iowa','wisconsin','michigan')):
            print('STATE_PREVIEW',e['url'],e['scores'])
    if q in (516,746,1196):
        terms={516:['Peter King','Metacritic','Kinsey','policeman'],746:['1938','Minneapolis','Wisconsin','Iowa'],1196:['Thiruvananthapuram','3.25']}[q]
        for term in terms:
            hits=[]
            for e in ev:
                if e['event'] in ('search.raw','search.result','search.source','rawtree.entries') and term.lower() in json.dumps(e).lower():
                    hits.append(e['event'])
            print('CANDIDATE_HITS',term,Counter(hits))
    if q==1230:
        for e in ev:
            if e['event']=='rawtree.bundles':
                best=sorted(e['bundles'],key=lambda b:-max(b.get('direct_answer',0),b.get('query_answer',0)))[:1]
                print('BUNDLE_BEST',e['search_id'],e['node_id'],[{k:v for k,v in b.items() if k in ('id','direct_answer','query_answer')} for b in best])
