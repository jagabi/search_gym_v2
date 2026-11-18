import json,statistics as st,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D=json.load(open(sys.argv[1],encoding='utf-8')); out=sys.argv[2]
m=lambda n,k: st.mean(r[k] for r in D[n])
fig,axes=plt.subplots(1,2,figsize=(12,4.6))
cols={1024:'#2a6fdb',2048:'#d9480f',512:'#adb5bd'}
for ax,(key,lab) in zip(axes,[('input','Main LLM input tokens per question (mean)'),('ctx','Final context tokens (mean)')]):
    for b in (512,1024,2048):
        xs=[m(f'd3 {b}x{t}',key)/1e3 for t in (1,2,3,4)]; ys=[m(f'd3 {b}x{t}','f1') for t in (1,2,3,4)]
        ax.plot(xs,ys,'-o',color=cols[b],label=f'decision {b}'+(' (invalid: pages unbundlable)' if b==512 else ''),ls='--' if b==512 else '-')
        for t,x,y in zip((1,2,3,4),xs,ys): ax.annotate(f'top{t}',(x,y),textcoords='offset points',xytext=(4,4),fontsize=8,color=cols[b])
    for n,mk in (('ragent','s'),('search-o1','^')):
        ax.scatter([m(n,key)/1e3],[m(n,'f1')],marker=mk,s=80,color='black',zorder=5); ax.annotate(n,(m(n,key)/1e3,m(n,'f1')),textcoords='offset points',xytext=(6,-10))
    ax.set_xlabel(lab+' (K)'); ax.set_ylabel('F1 (DSQA grid100)'); ax.grid(alpha=.3)
axes[0].legend(fontsize=8,loc='lower right')
fig.suptitle('Accuracy vs token cost — gpt-oss-20b + d3-mini, DeepSearchQA 100 questions')
fig.tight_layout(); fig.savefig(out+'/pareto.png',dpi=150)
# stacked breakdown
order=[f'd3 {b}x{t}' for b in (1024,2048) for t in (1,2,3,4)]+['ragent','search-o1']
parts=[('fixed','system+question'),('lst','search result list'),('ev','evidence payload'),('gen','queries/answer'),('oth','tool errors'),('resid','retained reasoning/other')]
fig,ax=plt.subplots(figsize=(11,4.6)); bottom=[0]*len(order)
for k,lab in parts:
    v=[m(n,k)/1e3 for n in order]; ax.bar(order,v,bottom=bottom,label=lab); bottom=[a+b for a,b in zip(bottom,v)]
ax.set_ylabel('Final context tokens (K, mean)'); ax.legend(fontsize=8); plt.xticks(rotation=30,ha='right'); ax.grid(axis='y',alpha=.3)
fig.tight_layout(); fig.savefig(out+'/context_breakdown.png',dpi=150)
