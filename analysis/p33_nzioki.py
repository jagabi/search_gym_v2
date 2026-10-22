exec((__import__('pathlib').Path(__file__).parent/'p33_target_audit.py').read_text(encoding='utf-8').split('for q in (57,516')[0])
ev=events(RUN/'q00516'/'trace.jsonl');sid='0fb414b68efe49aa8ba185c42d6a183f'
results={e['request_id']:e for e in ev if e['event']=='jev.result'}
for e in ev:
    if e.get('context',{}).get('search_id')==sid and e['event']=='jev.request' and 'Nzioki' in json.dumps(e['body']):
        print('CONTEXT',e['context']);scores=results.get(e['request_id'],{}).get('scores',{})
        print('FACT_SCORES',{k:v for k,v in scores.items() if not k.startswith('link')})
        for k,v in e['body']['questions'].items():
            if 'Nzioki' in str(v):print('QUESTION',k,v,'SCORE',scores.get(k))
    if e.get('search_id')==sid and e['event']=='rawtree.frontier':print('FRONTIER',json.dumps(e,ensure_ascii=False))
    if e.get('search_id')==sid and e['event']=='rawtree.return':
        for x in e['returned']:print('RETURN',x['source'])
