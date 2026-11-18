import json,statistics as st,sys
D=json.load(open(sys.argv[1],encoding='utf-8'))
order=[f'd3 {b}x{t}' for b in (512,1024,2048) for t in (1,2,3,4)]+['ragent','search-o1']
m=lambda xs: st.mean(xs) if xs else 0
def pct(xs,p):
    xs=sorted(xs); return xs[min(len(xs)-1,int(p*len(xs)))] if xs else 0
print('== 1. context breakdown (mean tokens)')
print('name ctx fixed list evid gen err resid')
for n in order:
    R=D[n]; print(n, *[round(m([r[k] for r in R])) for k in ('ctx','fixed','lst','ev','gen','oth','resid')])
print('== 2. per-search evidence')
for n in order:
    R=D[n]; U=[u for r in R for u in r['units']]
    ps=[r['ev']/r['searches'] for r in R if r['searches']]
    print(n,'searches',round(m([r['searches'] for r in R]),2),'ev/search mean',round(m(ps)),'unit mean',round(m(U)),'p90',pct(U,.9),'max',max(U) if U else 0,'n',len(U))
print('== 3. main vs aux')
for n in order:
    R=D[n]
    mi=[r['main_in'] for r in R if r['main_in'] is not None]
    print(n,'input',round(m([r['input'] for r in R])),'main_from_trace',round(m(mi)) if mi else None,'jev',round(m([r['jev'] for r in R])),'f1',round(m([r['f1'] for r in R]),3))
