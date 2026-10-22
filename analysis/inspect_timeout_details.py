exec((__import__('pathlib').Path(__file__).parent/'inspect_timeout_run.py').read_text(encoding='utf-8').split('report = {}')[0])
import statistics
print('TOTAL', {'correct':sum(r['score'] for r in records),'seconds':sum(r['latency_s'] for r in records),
    'searches':sum(r['searches'] for r in records), 'attempts':sum(r['reader_stats']['jev_attempts'] for r in records)})
for r in records:
    if r['score']:continue
    f=RUN/r['dir'];res=json.loads((f/'response.json').read_text(encoding='utf-8'))
    ev=[json.loads(s) for s in (f/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    print('\nQ',r['index'],'QUESTION',res['question'],'\nGOLD',res['gold_answer'],'\nANSWER',res['answer'])
    print('QUERIES',[e['query'] for e in ev if e['event']=='rawtree.start'])
    for name in ('rawtree.preview','rawtree.bundles','rawtree.return','rawtree.pages_selected','rawtree.early_return_requested','rawtree.fetch_failed'):
        rows=[e for e in ev if e['event']==name]
        print('SCHEMA',name,list(rows[0]) if rows else [])
    req={e['request_id']:e for e in ev if e['event']=='jev.request'}
    print('ERRORS',[(req[e['request_id']].get('context'),req[e['request_id']]['question_count'],e['error'],e.get('duration_ms')) for e in ev if e['event']=='jev.error'])
    for e in ev:
        if e['event']=='rawtree.return':print('RETURN',str(e)[:1200])
        if e['event']=='rawtree.early_return_requested':print('EARLY',e)
    gold=res['gold_answer'].lower()
    terms={57:['vanderbilt','career development','lutetium-177 dotatate'],326:[],516:[],598:[]}[r['index']]
    terms += [gold]
    for e in ev:
        if e['event'] in ('fetch.raw','tool.result'):
            text=str(e.get('content',e.get('text',e.get('result',''))))
            for term in terms:
                pos=text.lower().find(term)
                if pos>=0: print('HIT',e['event'],e.get('url'),term,text[max(0,pos-130):pos+240].replace('\n',' '))
