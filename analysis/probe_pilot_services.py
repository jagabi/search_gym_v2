"""Only local Reader/d3 readiness; never invokes a main reasoning model."""
import json
import os
from pathlib import Path
import re
import time
import urllib.request


def settings():
    root = Path(__file__).resolve().parents[1]
    cfg = (root / 'configs/jevtree.yaml').read_text(encoding='utf-8')
    d3 = re.search(r'^\s+jev_base_url:\s*(\S+)', cfg, re.M).group(1).rstrip('/')
    model = re.search(r'^\s+jev_model:\s*(\S+)', cfg, re.M).group(1)
    reader = os.getenv('JINA_BASE_URL')
    if not reader:
        for line in (root / '.env').read_text(encoding='utf-8-sig').splitlines():
            if line.strip().startswith('JINA_BASE_URL='):
                reader = line.split('=', 1)[1].strip().strip('\"\'')
    return d3, model, (reader or '').rstrip('/')


def main():
    d3, model, reader = settings()
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    probes = [('d3_models', d3+'/v1/models', None),
              ('reader_root', reader+'/', None),
              ('d3_inference', d3+'/v1/systemone', {
                  'model': model, 'state': {'page_text': 'Paris is the capital of France.'},
                  'questions': {'fact': {'type': 'noul', 'instructions':
                      'Does this source explicitly identify the capital of France?'}},
                  'request_id': 'pilot-service-check'})]
    for name, url, payload in probes:
        started = time.perf_counter()
        try:
            body = json.dumps(payload).encode() if payload else None
            req = urllib.request.Request(url, data=body,
                headers={'Content-Type': 'application/json'} if body else {})
            with opener.open(req, timeout=12) as response:
                text = response.read(1500).decode('utf-8', errors='replace')
                print(json.dumps({'probe': name, 'status': response.status,
                    'seconds': round(time.perf_counter()-started, 3), 'body': text},
                    ensure_ascii=True), flush=True)
        except Exception as exc:
            print(json.dumps({'probe': name, 'seconds': round(time.perf_counter()-started, 3),
                              'error': repr(exc)}, ensure_ascii=True), flush=True)


if __name__ == '__main__':
    main()
