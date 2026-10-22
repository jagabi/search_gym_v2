exec((__import__('pathlib').Path(__file__).parent/'inspect_timeout_run.py').read_text(encoding='utf-8').split('report = {}')[0])
errors=Counter();phases=Counter();timeout_keys=Counter();fetcherr=Counter()
for r in records:
    folder=RUN/r['dir'];ev=[json.loads(s) for s in (folder/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    req={e['request_id']:e for e in ev if e['event']=='jev.request'}
    for e in ev:
        if e['event']=='jev.error':
            request=req[e['request_id']];kind=e['error'].split('(')[0];errors[kind]+=1
            phases[(kind,request['context']['phase'])]+=1
            if kind=='TimeoutError':timeout_keys[request['question_count']]+=1
        if e['event']=='rawtree.fetch_failed':
            err=e['error'];fetcherr['422' if '422' in err else '503' if '503' in err else 'other']+=1
    if r['index'] not in (57,326,516,598):continue
    print('\nQ',r['index'])
    starts={e['search_id']:e['query'] for e in ev if e['event']=='rawtree.start'}
    for e in ev:
        if e['event']=='rawtree.return':
            print('SEARCH_RETURN',starts[e['search_id']], 'pages',e.get('returned'),
                  'selections',[(x['id'],x.get('direct_answer'),x.get('query_answer'),x.get('objective')) for x in e['selected']])
        if e['event']=='rawtree.preview':
            url=e['url']
            if r['index']==516 and ('metacritic' in url or 'Sumpter' in url or 'Constant' in url):
                print('PREVIEW',e)
        if e['event']=='rawtree.bundles' and r['index']==516:
            print('BUNDLES',e['search_id'],e['node_id'],[(b.get('id'),b.get('direct_answer'),b.get('query_answer')) for b in e['bundles']], 'selected',e['selected_bundle_ids'])
        if e['event']=='rawtree.fetch_failed' and (r['index']==598 and 'revistadestatistica' in e['url'] or r['index']==57 and ('PMC7227421' in e['url'] or '1685381' in e['url'])):
            print('GOLD_ACCESS_FAIL',e['url'],e['error'][:600])
    if r['index']==516:
        for request in req.values():
            state=request['body']['state'];text=state.get('page_text','') if isinstance(state,dict) else ''
            if 'Peter King' in text or 'Peter\u00a0King' in text:
                related=[e for e in ev if e.get('request_id')==request['request_id'] and e['event'] in ('jev.result','jev.error','jev.cancelled')]
                print('GOLD_D3_INPUT',request['context'],'title',state.get('page_title'),'keys',request['question_count'],'RESULT',related)
        for e in ev:
            if e['event']=='rawtree.inspection_selection':print('INSPECT',e)
    if r['index']==598:
        for e in ev:
            if e['event'].startswith('run.final') or e['event']=='run.end':print('FINAL',str(e)[:1500])
print('AGGREGATE_ERRORS',errors,'PHASES',phases,'TIMEOUT_KEYS',timeout_keys,'FETCH',fetcherr)
