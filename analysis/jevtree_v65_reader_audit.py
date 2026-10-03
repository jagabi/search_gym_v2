"""Offline locator and evidence export; keyword hits are not loss verdicts."""
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'runs/test/20261003-1643_jevtree_gpt-oss-20b_browsecomp_jevtree_v65_10'
TERMS = {
    3: ['Rosalea Murphy', 'Pink Adobe'], 7: ['Lush Life', 'Lori Petty'],
    8: ['White Mischief'], 13: ['Red Lake'], 15: ['12:30', '12.30', 'half past twelve'],
    21: ['Jin Air Green Wings', 'Jin Air Greenwings', 'Teddy'],
    22: ['12th Fail', 'Vidhu', 'Manoj Sharma'],
    26: ['Abdisalam', 'Abdulsalam'], 27: ['21 October 1955', 'October 21, 1955'],
    32: ['Australian', 'Ruth Werner'],
}


def norm(text):
    return ' '.join(unicodedata.normalize('NFKC', text).casefold().split())


def contains(text, term):
    return re.search(r'(?<!\w)' + re.escape(norm(term)) + r'(?!\w)', norm(text)) is not None


def main():
    rows, evidence = [], []
    for directory in sorted(RUN.glob('q*')):
        qid = int(directory.name[1:])
        response = json.loads((directory / 'response.json').read_text(encoding='utf-8'))
        requests = {}
        pairs = []
        with (directory / 'trace.jsonl').open(encoding='utf-8') as stream:
            for line_no, line in enumerate(stream, 1):
                event = json.loads(line)
                key = (event.get('url'), event.get('attempt'))
                if event['event'] == 'jevtree.reader_request':
                    payload = json.loads(event['messages'][1]['content'])
                    requests[key] = (line_no, payload)
                elif event['event'] == 'jevtree.read':
                    request_line, payload = requests.pop(key)
                    body, note = payload['page_text'], event['text']
                    hits = [dict(term=t, in_note=contains(note, t))
                            for t in TERMS[qid] if contains(body, t)]
                    pairs.append(dict(url=key[0], request_line=request_line,
                                      read_line=line_no, hits=hits))
                    if (qid == 21 and line_no in (339, 503, 1048)) or (qid == 8 and line_no in (633, 636, 638)):
                        excerpts = []
                        for term in (['JackeyLove', 'Teddy', 'Jin Air', 'EDward'] if qid == 21 else ['White Mischief', 'comedy writer']):
                            for match in list(re.finditer(re.escape(term), body, re.I))[:3]:
                                excerpts.append(body[max(0, match.start()-150):match.end()+320])
                        evidence.append(dict(qid=qid, question=response['question'],
                            gold=response['gold_answer'], url=key[0], request_line=request_line,
                            read_line=line_no, source_excerpts=excerpts, reader_output=note))
        assert not requests, (qid, 'unpaired requests')
        rows.append(dict(qid=qid, gold=response['gold_answer'], reader_pairs=len(pairs),
                         matches=[p for p in pairs if p['hits']]))
    result = dict(warning='Keyword locator only. A missing term may be irrelevant navigation, another entity, or a paraphrase. No loss rate is inferred.',
                  total_pairs=sum(r['reader_pairs'] for r in rows), questions=rows,
                  reviewed_evidence=evidence)
    output = ROOT / 'analysis/jevtree_v65_reader_audit.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Paired reader calls:', result['total_pairs'])
    for row in rows:
        print(row['qid'], 'pairs', row['reader_pairs'], 'matched pages', len(row['matches']),
              'omission candidates', sum(any(not h['in_note'] for h in p['hits']) for p in row['matches']))


if __name__ == '__main__':
    main()
