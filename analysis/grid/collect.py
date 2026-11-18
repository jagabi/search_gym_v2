import json,glob,re,os,statistics as st,sys
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
T=lambda s: len(enc.encode(s,disallowed_special=())) if s else 0
os.chdir(sys.argv[1])
ids=json.load(open('data/deepsearchqa/grid100_meta.json',encoding='utf-8'))['indices']
runs={}
for d in glob.glob('runs/test/*_grid_b*_t*'):
    b,t=re.search(r'b(\d+)_t(\d)',d).groups(); runs[f'd3 {b}x{t}']=d
runs['d3 2048x4']=glob.glob('runs/test/*deepsearchqa_decision_d3-mini_b2048_300')[0]
runs['ragent']=glob.glob('runs/test/*ragent_gpt-oss-20b_deepsearchqa*')[0]
runs['search-o1']=glob.glob('runs/test/*search-o1_gpt-oss-20b_deepsearchqa*')[0]
MARK='Excerpts from the pages read'
def s(x): return x if isinstance(x,str) else json.dumps(x,ensure_ascii=False)
out={}
for name,d in runs.items():
    recs={}
    for l in open(d+'/records.jsonl',encoding='utf-8'):
        r=json.loads(l); recs[r['index']]=r
    rows=[]
    for i in ids:
        r=json.load(open(f'{d}/q{i:05d}/response.json',encoding='utf-8')); rec=recs[i]
        fixed=T(r['system_prompt'])+T(r['question'])
        lst=ev=oth=gen=0; units=[]
        for stp in r['steps']:
            gen+=T(stp.get('text') or '')
            for tc in stp.get('tool_calls') or []:
                gen+=T(s(tc.get('arguments')))
                res=s(tc.get('result') or '')
                if tc.get('is_error') or tc.get('refused'): oth+=T(res); continue
                if name.startswith('d3'):
                    k=res.find(MARK)
                    if k<0: lst+=T(res)
                    else:
                        a,b=T(res[:k]),T(res[k:]); lst+=a; ev+=b; units.append(b)
                elif name=='ragent':
                    t=T(res)
                    if tc['name']=='web_search': lst+=t
                    else: ev+=t; units.append(t)
                else:
                    t=T(res); ev+=t; units.append(t)
        ctx=r['context_tokens']
        main_in=None
        tp=f'{d}/q{i:05d}/trace.jsonl'
        if os.path.exists(tp):
            reqs=[json.loads(l) for l in open(tp,encoding='utf-8')]
            reqs=[e.get('context_tokens',0) for e in reqs if e.get('event')=='llm.request']
            main_in=sum(reqs[1:])+ctx
        rows.append(dict(i=i,f1=rec['f1'],searches=rec['searches'],ctx=ctx,fixed=fixed,lst=lst,ev=ev,oth=oth,gen=gen,
            resid=ctx-fixed-lst-ev-oth-gen,units=units,input=rec['input_tokens'],main_in=main_in,
            jev=(rec.get('reader_stats') or {}).get('jev_input_tokens',0)))
    out[name]=rows
    print(name,'done',file=sys.stderr)
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'))
