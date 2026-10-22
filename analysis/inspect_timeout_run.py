import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'runs/test/20261022-1354_jevtree_gpt-oss-20b_browsecomp_raw_browser_key_timeout_10'
records = [json.loads(s) for s in (RUN/'records.jsonl').read_text(encoding='utf-8').splitlines()]
report = {}
for record in records:
    folder = RUN / record['dir']
    response = json.loads((folder/'response.json').read_text(encoding='utf-8'))
    events = [json.loads(s) for s in (folder/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    print('\nQUESTION', record['index'], response['question'], '\nGOLD', response['gold_answer'])
    print('RESPONSE_KEYS', list(response))
    print('ANSWER', response.get('answer', response.get('response', '')))
    counts = Counter(e['event'] for e in events)
    print('EVENTS', dict(counts))
    requests = {e['request_id']: e for e in events if e['event']=='jev.request'}
    errors = []
    for e in events:
        if e['event']=='jev.error':
            req = requests.get(e['request_id'], {})
            errors.append({'context': req.get('context'), 'keys': req.get('question_count'), **e})
    print('ERRORS', json.dumps(errors, ensure_ascii=False))
    print('FINAL_LLM', json.dumps([e for e in events if e['event']=='llm.response'][-1], ensure_ascii=False))
    searches = [e for e in events if e['event']=='rawtree.start']
    print('QUERIES', json.dumps(searches, ensure_ascii=False))
    if not record['score']:
        wanted = {'rawtree.inspection_selection','rawtree.early_return_requested','rawtree.frontier',
                  'rawtree.traversal_end','rawtree.read','rawtree.result','rawtree.document_candidates'}
        selected = [e for e in events if e['event'] in wanted]
        (ROOT/'analysis'/f"timeout_q{record['index']}_selected.json").write_text(
            json.dumps(selected, ensure_ascii=False, indent=2), encoding='utf-8')
        print('SELECTED_EVENTS', json.dumps(selected, ensure_ascii=False)[:12000])
    report[str(record['index'])] = {'record': record, 'errors': errors, 'queries': searches}
(ROOT/'analysis/timeout_run_diagnosis.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
