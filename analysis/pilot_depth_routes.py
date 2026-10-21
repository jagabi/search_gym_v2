"""Live Jina + d3 pilots; fixed URL leads, no search/main/judge model calls."""
import argparse
import asyncio
from dataclasses import asdict
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import httpx
import yaml
from searchgym.agent import AgentConfig
from searchgym.explorer import Document
from searchgym.rawtree import LocalDecision, RawTree, VERSION
from searchgym.tools import WebTools
from probe_pilot_services import settings

CASES = {
    'direct': ('When was Python 3.11.9 released?', [
        'https://www.python.org/downloads/release/python-3119/']),
    'route': ('Who authored the PEP introducing BaseException.add_note in Python 3.11, and when was that PEP created?', [
        'https://docs.python.org/3.11/whatsnew/index.html']),
    'siblings': ('When was Python 3.11.9 released?', [
        'https://docs.python.org/3.11/library/turtle.html',
        'https://www.python.org/downloads/release/python-3119/']),
    'article': ('Who authored the PEP introducing BaseException.add_note in Python 3.11, and when was that PEP created?', [
        'https://docs.python.org/3.11/whatsnew/3.11.html']),
    'tailroute': ('Who authored the PEP introducing tomllib in Python 3.11, and when was that PEP created?', [
        'https://docs.python.org/3.11/whatsnew/3.11.html']),
    'nobel': ('On what date and in what town was the recipient of the 1921 Nobel Prize in Physics born?', [
        'https://www.nobelprize.org/prizes/physics/1921/summary/']),
}

class Trace:
    def __init__(self, path):
        self.events = []
        self.file = path.open('w', encoding='utf-8')
    def event(self, event, **data):
        row = {'event': event, **data}
        self.events.append(row)
        self.file.write(json.dumps(row, ensure_ascii=False, default=str)+'\n')
        self.file.flush()
        if event in ('rawtree.preview', 'rawtree.node_action', 'rawtree.traversal_end', 'rawtree.fetch_failed'):
            print(json.dumps({k:v for k,v in row.items() if k in (
                'event','node_id','url','depth','action','scores','reason')}, ensure_ascii=True), flush=True)

async def main(args):
    global LocalDecision, RawTree, VERSION
    import hashlib
    source = (ROOT/'searchgym/rawtree.py').read_text(encoding='utf-8')
    if args.baseline:
        import subprocess
        import types
        source = subprocess.run(['git','show','HEAD:searchgym/rawtree.py'], cwd=ROOT,
                                capture_output=True,check=True,encoding='utf-8').stdout
        module = types.ModuleType('searchgym._pilot_baseline')
        module.__package__ = 'searchgym'
        exec(compile(source,'committed_rawtree.py','exec'), module.__dict__)
        LocalDecision, RawTree, VERSION = module.LocalDecision, module.RawTree, module.VERSION
    folder = ROOT / 'analysis' / 'pilots' / args.label
    folder.mkdir(parents=True, exist_ok=True)
    cache = ROOT / 'analysis' / 'pilots' / 'bodies'
    cache.mkdir(parents=True, exist_ok=True)
    config = yaml.safe_load((ROOT/'configs/jevtree.yaml').read_text(encoding='utf-8'))['agent']
    cfg = AgentConfig(**config)
    # Fixed leads isolate routing from entry ranking; all traversal/read limits stay unchanged.
    cfg.jev_rank_entries = False
    d3, model, reader = settings()
    assert cfg.jev_base_url.rstrip('/') == d3 and cfg.jev_model == model
    decision = LocalDecision(cfg)
    tools = WebTools()
    tools.reader_status = {'jina_base_url': reader}
    tools._reader_http = httpx.AsyncClient(timeout=45, trust_env=False)
    try:
        await decision.prepare()
        for name in args.cases:
            trace = Trace(folder/f'{name}.jsonl')
            fetches = []
            async def fetch(url, *, engine):
                import hashlib
                dest = cache / (hashlib.sha256(url.encode()).hexdigest()+'.json')
                started = time.perf_counter()
                reused = dest.exists() and not args.fresh
                if reused:
                    doc = Document(**json.loads(dest.read_text(encoding='utf-8')))
                else:
                    doc = await tools.fetch(url, engine=engine)
                    if not doc.is_error:
                        dest.write_text(json.dumps(asdict(doc), ensure_ascii=False), encoding='utf-8')
                row = dict(url=url, cached=reused, seconds=time.perf_counter()-started, failed=doc.is_error)
                fetches.append(row)
                trace.event('pilot.fetch', **row)
                return doc
            question, urls = CASES[name]
            started = time.perf_counter()
            try:
                tree, text, stats = await asyncio.wait_for(RawTree(decision,cfg,fetch).run_search(
                    question, [{'link':u} for u in urls], question=question, trace=trace, usage=None), args.timeout)
                report = dict(version=VERSION, code_sha256=hashlib.sha256(source.encode()).hexdigest(),
                              case=name, seconds=time.perf_counter()-started,
                              stats=stats, fetches=fetches, tree=tree)
                (folder/f'{name}.evidence.txt').write_text(text,encoding='utf-8')
                print(json.dumps({k:v for k,v in report.items() if k != 'tree'}),flush=True)
            except Exception as exc:
                report = dict(version=VERSION,case=name,error=repr(exc),seconds=time.perf_counter()-started,fetches=fetches)
                print(json.dumps(report),flush=True)
            finally:
                trace.file.close()
            (folder/f'{name}.summary.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    finally:
        await decision.aclose()
        await tools._reader_http.aclose()

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--label', required=True)
    p.add_argument('--cases',nargs='+',choices=CASES,default=['direct','route','siblings'])
    p.add_argument('--fresh',action='store_true',help='Fetch live Jina bodies again instead of body cache')
    p.add_argument('--baseline',action='store_true',help='Use committed rawtree code in memory')
    p.add_argument('--timeout',type=float,default=180)
    asyncio.run(main(p.parse_args()))
