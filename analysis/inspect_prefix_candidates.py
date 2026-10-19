"""Offline prefix sensitivity on saved initial-root documents; never fetches."""
import collections
import json
from pathlib import Path
from tokenizers import Tokenizer
from searchgym.jevtree import candidate_links
from searchgym.jevtree_input import complete_prefix
from searchgym.urls import normalize_fetch_url

RUN=Path('runs/test/20261017-2332_jevtree_gpt-oss-20b_browsecomp_raw_browser_p9_10')
encoder=Tokenizer.from_file(str(next((Path.home()/'.cache/huggingface/hub/models--vllm-sr--d3-mini/snapshots').glob('*/tokenizer.json'))))
encoder.no_padding(); encoder.no_truncation()
counts=collections.defaultdict(list); examples=[]
for folder in sorted(RUN.glob('q*')):
    if not folder.is_dir(): continue
    trees=json.loads((folder/'explorer.json').read_text(encoding='utf8'))
    roots={u for t in trees for n in t['opened'][:6] for u in n['urls']}
    seen=set(); taken=0
    with (folder/'trace.jsonl').open(encoding='utf8') as stream:
        for line in stream:
            if 'fetch.raw' not in line[:180]: continue
            e=json.loads(line); url=e['url']
            if url not in roots or url in seen or e.get('is_error'): continue
            seen.add(url); content=e['content']; enc=encoder.encode(content,add_special_tokens=False)
            row={'q':folder.name,'url':url}
            for size in [3000,4000,5000]:
                text=content if len(enc.ids)<=size else content[:enc.offsets[size-1][1]]
                prefix=complete_prefix(content,text)
                links=candidate_links(prefix,url,set())
                counts[size].append(len(links)); row[str(size)]=len(links)
            examples.append(row); taken+=1
            if taken>=20: break
result={'sample':'At most 20 unique successful initial-root documents per question from saved p9; empty visited set; not a live replay.',
    'n':len(examples),'counts':{k:{'mean':round(sum(v)/len(v),2),'median':sorted(v)[len(v)//2],'sum':sum(v)} for k,v in counts.items()},
    'examples':examples}
Path('analysis/audit_20261019-0005/prefix_candidates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k!='examples'}))
