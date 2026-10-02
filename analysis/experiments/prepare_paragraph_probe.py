"""Prepare model-only evidence-citation diagnostics; do not change production code.

Paragraph labels reference only text already supplied to the saved reader. No
new source retrieval and no gold answers enter the requests.
"""
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / 'runs/test'
INSTRUCTION = '''Source paragraphs are labeled [P1], [P2], etc. Cite the supplied
paragraph IDs beside the factual evidence you extract. These references let the
parent receive the exact source paragraphs along with your note. A paragraph ID
supports only what that paragraph actually says. Keep different entities and
their conditions separate. Do not invent paragraph IDs. Keep the usual evidence,
coverage, missing fields and recursive next-link format.'''


def label_paragraphs(source):
    paragraphs = [p for p in re.split(r'\n\s*\n', source) if p.strip()]
    return '\n\n'.join(f'[P{i}]\n{p}' for i,p in enumerate(paragraphs,1)), paragraphs


specs = [
    ('20260925-1728_depthsearch_gpt-oss-20b_browsecomp_ds_links_v12_b', 'q01073', 'meteorologiaenred.com'),
    ('20260925-1728_depthsearch_gpt-oss-20b_browsecomp_ds_links_v12_b', 'q00265', 'noseinabook.co.uk'),
    ('20260925-1728_depthsearch_gpt-oss-20b_browsecomp_ds_links_v12_b', 'q00240', '/wiki/Marie_of_Romania'),
    ('20260925-1337_depthsearch_gpt-oss-20b_browsecomp_ds_batch_v9', 'q00008', '/wiki/White_Mischief_(film)'),
]

cases, manifest = [], []
for run, question, url_piece in specs:
    events = [json.loads(s) for s in (RUNS/run/question/'trace.jsonl').read_text(encoding='utf-8').split('\n') if s.strip()]
    event = next(e for e in events if e['event']=='explorer.extract_input' and any(url_piece in u for u in e['urls']))
    messages = copy.deepcopy(event['messages'])
    prefix, source = messages[1]['content'].split('**Pages you were given:**\n',1)
    labeled, paragraphs = label_paragraphs(source)
    messages[1]['content'] = prefix + '**Pages you were given:**\n' + labeled
    messages[-1]['content'] += '\n\n' + INSTRUCTION
    for repeat in range(2):
        cases.append({'name':f'{question}_paragraph_{repeat+1}', 'messages':messages, 'tool_choice':'none'})
    extractive = copy.deepcopy(messages)
    old = '**Evidence:** Exact relevant facts/rows and short supporting quotes.'
    assert old in extractive[0]['content']
    extractive[0]['content'] = extractive[0]['content'].replace(old,
        '**Evidence:** Cite the supplied paragraph IDs for relevant facts/rows. Their original text is returned automatically.')
    extractive[-1]['content'] += '''\n\nIn **Evidence:** return only source paragraph references, e.g. [P7] [P12].
Do not rewrite facts or reproduce quotations there: the cited original paragraphs
will be returned verbatim by the code. In **Connections:** keep only a brief,
tentative interpretation, not another fact list. Keep the coverage, missing fields,
useful next links, expansion decision and status. Cite only supplied paragraph IDs.'''
    for repeat in range(2):
        cases.append({'name':f'{question}_paragraph_extractive_{repeat+1}', 'messages':extractive, 'tool_choice':'none'})
    manifest.append({'question':question,'urls':event['urls'],'source_run':run,'depth':event['depth'],
                     'paragraphs':paragraphs,'annotation_chars':len(labeled)-len(source)})

out = ROOT/'analysis/experiments'
(out/'paragraph_probe_cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'paragraph_probe_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(cases)} model-only cases prepared; no calls made.')
for row in manifest:
    print(row['question'], 'paragraphs',len(row['paragraphs']),'annotation characters',row['annotation_chars'])
