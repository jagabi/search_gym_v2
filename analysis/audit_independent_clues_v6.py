"""Offline saved-run audit. No model, network, search, fetch, or judge calls."""
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    'ragent': '20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1',
    'o1': '20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1',
    'ds_original': '20260921-0016_depthsearch_gpt-oss-20b_browsecomp_paper_frozen_v1',
    'v3': '20260921-2144_depthsearch_gpt-oss-20b_browsecomp_ds_search_main_v3',
    'v4': '20260922-0859_depthsearch_gpt-oss-20b_browsecomp_ds_answer_phase_v4',
    'v6': '20260923-1829_depthsearch_gpt-oss-20b_browsecomp_ds_independent_clues_v6',
}
SMOKE = ROOT / 'runs/test/20260923-1815_depthsearch_gpt-oss-20b_browsecomp_ds_independent_clues_v6'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def norm(value):
    return ' '.join(re.findall(r'[a-z0-9]+', str(value).lower()))

def case_dir(method, row):
    directory = ROOT / 'runs/test' / RUNS[method] / row['dir']
    if not (directory / 'response.json').exists() and method == 'v6' and row.get('cached'):
        directory = SMOKE / row['dir']
    assert (directory / 'response.json').exists(), directory
    return directory

def main():
    records, overview, responses = {}, {}, {}
    for method, name in RUNS.items():
        rows = [json.loads(s) for s in (ROOT/'runs/test'/name/'records.jsonl').read_text(encoding='utf-8').splitlines()]
        assert len(rows) == len({r['index'] for r in rows}) == 300
        records[method] = {r['index']: r for r in rows}
        responses[method] = {r['index']: read(case_dir(method, r)/'response.json') for r in rows}
        overview[method] = {
            'correct': sum(r['f1'] == 1 for r in rows), 'empty': sum(not r['answer_chars'] for r in rows),
            'judge_errors': sum(bool(r['judge_error']) for r in rows),
            'calls': sum(r['llm_calls'] for r in rows), 'median_seconds': median(r['latency_s'] for r in rows),
            'mean_seconds': mean(r['latency_s'] for r in rows), 'searches': sum(r['searches'] for r in rows),
            'main_fetches': sum(r['fetches'] for r in rows), 'auto_fetches': sum(r.get('auto_fetches',0) for r in rows),
            'fetch_attempts': sum(r['fetch_attempts'] for r in rows), 'nodes': sum(r['expansion_nodes'] for r in rows),
            'with_recursion': sum(r['expansion_nodes']>0 for r in rows),
            'without_page_attempt': sum(r['fetch_attempts']==0 for r in rows),
            'without_reader': sum(r['explorer_calls']==0 for r in rows),
            'search_failures': sum(r['search_failures'] for r in rows),
            'invalid': sum(r.get('invalid_tool_calls',0) for r in rows),
            'categories': {c: sum(r['f1']==1 for r in rows if r['category']==c) for c in sorted({r['category'] for r in rows})},
        }
    ids = set(records['v6'])
    assert all(set(v) == ids for v in records.values())
    for i in ids:
        assert len({(responses[m][i]['question'], responses[m][i]['gold_answer']) for m in RUNS}) == 1
    paired = {}
    for method in RUNS.keys()-{'v6'}:
        win = sorted(i for i in ids if records['v6'][i]['f1']>records[method][i]['f1'])
        loss = sorted(i for i in ids if records['v6'][i]['f1']<records[method][i]['f1'])
        n=len(win)+len(loss)
        paired[method]={'win':win,'loss':loss,'both_correct':sum(records['v6'][i]['f1']==records[method][i]['f1']==1 for i in ids),
            'mcnemar_p': min(1,2*sum(math.comb(n,k) for k in range(min(len(win),len(loss))+1))/2**n) if n else 1}
    counts=defaultdict(Counter)
    cases={}
    for i,row in records['v6'].items():
        response=responses['v6'][i]
        gold=norm(response['gold_answer'])
        def mentions(value):
            return len(gold)>=4 and (' '+gold+' ') in (' '+norm(value)+' ')
        searches,fetches,invalids=[],[],[]
        searches_so_far=0
        for step in response['steps']:
            for call in step.get('tool_calls',[]):
                if call['name']=='web_search' and not call.get('refused'):
                    searches_so_far+=1
                    payload=call.get('result')
                    if isinstance(payload,str):
                        try: payload=json.JSONDecoder().raw_decode(payload)[0]
                        except (ValueError,TypeError): payload={}
                    if not isinstance(payload,dict): payload={}
                    entries=payload.get('organic',[])
                    searches.append({'n':searches_so_far,'turn':step['turn'],'query':call.get('arguments',{}).get('query'),
                        'entries':entries,'gold_mentions':[e for e in entries if mentions(json.dumps(e))]})
                elif call['name']=='web_fetch':
                    fetches.append({'turn':step['turn'],'searches_before':searches_so_far,'args':call.get('arguments'),
                        'refused':call.get('refused',False),'error':call.get('is_error',False),'result':call.get('result'),
                        'text':step.get('text',''),'reasoning':step.get('reasoning','')})
                if call.get('refused'):
                    invalids.append({'tool':call['name'],'arguments':call.get('arguments'),'result':call.get('result')})
        events=Counter(); notes=[]; tasks=[]; finals=[]; finalizing=[]; seed_inputs=[]; raw_hits=[]; unavailable=[]
        for line in (case_dir('v6',row)/'trace.jsonl').open(encoding='utf-8'):
            e=json.loads(line); kind=e['event']; events[kind]+=1
            if kind=='tool.invalid_arguments': counts['invalid_reasons'][e['error']]+=1
            if kind=='tool.unavailable': unavailable.append(e); counts['unavailable'][e.get('reason',e.get('tool','unknown'))]+=1
            if kind=='research.seed_request': seed_inputs.append(e)
            if kind=='research.reading_task': tasks.append(e)
            if kind=='run.finalizing': finalizing.append(e); counts['finalizing'][e['reason']]+=1
            if kind=='run.final_response': finals.append(e); counts['final_response'][('empty' if not e.get('raw_text') else 'text')+':'+str(e.get('finish_reason'))]+=1
            if kind=='explorer.response' and e.get('phase') in {'extract','recover'}:
                notes.append({'depth':e.get('depth'),'text':e.get('text',''),'gold':mentions(e.get('text',''))})
            if kind=='explorer.extract_input' and mentions(json.dumps(e.get('messages',[]))):
                raw_hits.append({'depth':e.get('depth'),'urls':e.get('urls'), 'turn':e.get('turn')})
        counts['events'].update(events)
        group='no_page_attempt' if row['fetch_attempts']==0 else 'with_page_attempt'
        counts['fetch_groups'][group+':n']+=1
        counts['fetch_groups'][group+':correct']+=row['f1']==1
        if row['fetch_attempts']==0:
            counts['fetch_groups']['no_attempt_with_refused_request']+=bool(fetches)
            counts['fetch_groups']['no_attempt_without_request']+=not fetches
            counts['fetch_groups']['ten_searches_no_attempt']+=row['searches']==10
        counts['fetch_groups']['without_successful_reader:n']+=row['explorer_calls']==0
        counts['fetch_groups']['without_successful_reader:correct']+=(row['explorer_calls']==0 and row['f1']==1)
        executed=[f for f in fetches if not f['refused']]
        first=str(executed[0]['searches_before']) if executed else 'never'
        counts['first_fetch'][first+':n']+=1
        counts['first_fetch'][first+':correct']+=row['f1']==1
        hits=[s['n'] for s in searches if s['gold_mentions']]
        if not row['f1']:
            counts['wrong_gold_mentions']['search']+=bool(hits)
            counts['wrong_gold_mentions']['raw_reader_input']+=bool(raw_hits)
            counts['wrong_gold_mentions']['notes']+=any(n['gold'] for n in notes)
            counts['wrong_gold_mentions']['only_last_search']+=bool(hits) and min(hits)==10
            counts['wrong_gold_mentions']['search_without_page_attempt']+=bool(hits) and row['fetch_attempts']==0
            counts['wrong_gold_mentions']['answer']+=mentions(response['answer'])
        if len(searches)>=2:
            q1,q2=searches[0]['query'],searches[1]['query']
            tokens1,tokens2=set(norm(q1).split()),set(norm(q2).split())
            jaccard=len(tokens1&tokens2)/max(1,len(tokens1|tokens2))
            urls1={e.get('link') for e in searches[0]['entries']}; urls2={e.get('link') for e in searches[1]['entries']}
            counts['seeds']['same_query']+=norm(q1)==norm(q2)
            counts['seeds']['query_jaccard_ge_0.8']+=jaccard>=0.8
            counts['seeds']['shared_result_url']+=bool(urls1&urls2)
            counts['seeds']['two_searches']+=1
        else: jaccard=None
        counts['reading_tasks']['all']+=len(tasks)
        counts['reading_tasks']['fallback_query']+=sum(t['goal'].startswith('Check the relation in this search query;') for t in tasks)
        if seed_inputs:
            for e in seed_inputs:
                if e['route']=='B':
                    assert [m['role'] for m in e['messages']] == ['system','user','user']
        cases[i]={'question':response['question'],'gold':response['gold_answer'],'answer':response['answer'],
            'scores':{m:records[m][i]['f1'] for m in RUNS},'searches':searches,'fetches':fetches,'invalids':invalids,
            'notes':notes,'raw_gold_hits':raw_hits,'gold_in_search':hits,'tasks':tasks,'finals':finals,
            'finalizing':finalizing,'unavailable':unavailable,'seed_jaccard':jaccard,
            'fetch_attempts':row['fetch_attempts'],'reader_calls':row['explorer_calls'],'nodes':row['expansion_nodes'],
            'calls':row['llm_calls'],'seconds':row['latency_s'],'events':dict(events)}
    for method in ['ragent','o1','v4']:
        loss=[cases[i] for i in paired[method]['loss']]
        paired[method]['loss_without_page_attempt']=sum(x['fetch_attempts']==0 for x in loss)
        paired[method]['loss_without_reader']=sum(x['reader_calls']==0 for x in loss)
    ra_timing=Counter()
    for i,response in responses['ragent'].items():
        used=0; first=None
        for step in response['steps']:
            for call in step.get('tool_calls',[]):
                if call['name']=='web_search' and not call.get('refused'): used+=1
                if call['name']=='web_fetch' and not call.get('refused'):
                    if first is None: first=used
                    ra_timing['fetches_after_search10']+=used>=10
        group='never' if first is None else 'after_search10' if first>=10 else 'before_search10'
        ra_timing[group+':n']+=1
        ra_timing[group+':correct']+=records['ragent'][i]['f1']==1
    result={'runs':RUNS,'overview':overview,'paired':paired,'counts':{k:dict(v) for k,v in counts.items()},
            'ragent_fetch_timing':dict(ra_timing),'cases':cases}
    out=ROOT/'analysis/independent_clues_v6_audit.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in {'cases','runs'}},ensure_ascii=False,indent=2))
    print(out)

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
