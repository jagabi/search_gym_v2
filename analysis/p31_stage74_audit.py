"""Audit actual frontier admission and inspection attrition without rescoring links."""
exec((__import__('pathlib').Path(__file__).parent/'diagnose_p31.py').read_text(encoding='utf-8').split('summaries=[]')[0])
audit=[]
for r in records:
    ev=[json.loads(s) for s in (RUN/r['dir']/'trace.jsonl').read_text(encoding='utf-8').splitlines()]
    nodes={};inspected=set();queries={};examples=[]
    for e in ev:
        if e['event']=='rawtree.start':queries[e['search_id']]=e['query']
        if e['event'] in ('rawtree.preview','rawtree.fetch_failed'):
            key=(e['search_id'],e['node_id'])
            nodes[key]={'url':e['url'],'failed':e['event']=='rawtree.fetch_failed',
                        'preview':e.get('scores',{}).get('inspect_value')}
        if e['event']=='rawtree.inspection_selection':
            inspected.update((e['search_id'],n) for n in e['selected'])
    counts=Counter();reasons=Counter();selection=[]
    for e in ev:
        if e['event']=='rawtree.inspection_selection' and e['depth']==1:
            counts['root_gate_candidates']+=len(e['candidates'])
            counts['root_selected']+=len(e['selected'])
            counts['root_gate_candidates_not_selected']+=len(set(e['candidates'])-set(e['selected']))
    for e in ev:
        if e['event']=='rawtree.traversal_end':reasons[e['reason']]+=1
        if e['event']!='rawtree.frontier':continue
        selected=[nodes[(e['search_id'],n)] for n in e['selected'] if (e['search_id'],n) in nodes]
        for n in e['selected']:
            key=(e['search_id'],n);node=nodes.get(key,{})
            counts['admitted_children']+=1
            if node.get('failed'):counts['child_fetch_failed']+=1
            elif key in inspected:counts['child_inspected']+=1
            else:
                counts['child_not_inspected']+=1
                counts['child_preview_below_floor' if node.get('preview',1)<.15 else 'child_other_skip']+=1
        candidate_parents={c['parent'] for c in e['candidates'] if c['score']>=.1}
        parents=[]
        for n in selected:
            parents.extend(c['parent'] for c in e['candidates'] if c['url']==n['url'])
        if len(selected)==2 and len(set(parents))==1 and len(candidate_parents)>1:
            counts['two_slots_from_same_parent']+=1
            examples.append({'query':queries[e['search_id']],'depth':e['depth'],
                'selected':[n['url'] for n in selected],'candidates':e['candidates']})
        if e['depth']<3 and not e['selected'] and any(c['score']>=.1 for c in e['candidates']):
            counts['eligible_but_no_admission']+=1
        if selected and any(n.get('failed') for n in selected):
            selection.append({'query':queries[e['search_id']],'depth':e['depth'],
                'selected':selected,'candidates':e['candidates']})
    row={'index':r['index'],'correct':r['score'],**dict(counts),'end_reasons':dict(reasons),
         'same_parent_examples':examples,'failed_child_examples':selection}
    audit.append(row)
    print(json.dumps({k:v for k,v in row.items() if not k.endswith('examples')},ensure_ascii=False))
(out/'stage74.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
print('TOTAL',dict(sum((Counter({k:v for k,v in r.items() if isinstance(v,int) and k!='index'}) for r in audit),Counter())))
