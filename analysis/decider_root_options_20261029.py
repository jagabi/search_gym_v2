import json
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = 'http://172.16.3.192:8101'
def post(body, path='/'):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={'Content-Type':'application/json'})
    start = time.perf_counter()
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with client.open(req, timeout=30) as res:
            text = res.read().decode()
            return {'status': res.status, 'seconds': time.perf_counter()-start, 'response': json.loads(text)}
    except urllib.error.HTTPError as err:
        return {'status': err.code, 'seconds': time.perf_counter()-start, 'body':err.read().decode()}

if __name__ == '__main__':
    question = {'type':'choice', 'instructions':'Which letter is present in the context?', 'criteria':{'A':'A','B':'B'}}
    small = {'state':'A', 'questions':{'q1':question}}
    cases = [
        ('array_body', [small, dict(small, state='B')]),
        ('requests_array', {'requests':[small, dict(small,state='B')]}),
        ('state_array', dict(small,state=['A','B'])),
        ('questions_batch', {'state':'', 'questions':{
            'q1':dict(question, instructions='A. Which letter is present in this context?'),
            'q2':dict(question, instructions='B. Which letter is present in this context?')}, 'cache_salt':'root-probe-unique-20261029'}),
        ('digits_16', {'state':'', 'questions':{'q1':dict(question,instructions=' '.join('1234567890123456'))}}),
        ('digits_32', {'state':'', 'questions':{'q1':dict(question,instructions=' '.join('12345678901234567890123456789012'))}}),
    ]
    rows=[]
    for label, body in cases:
        row={'case':label,**post(body)}
        rows.append(row)
        print(json.dumps(row),flush=True)
    Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
