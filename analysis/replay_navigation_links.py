"""Replay selected saved link judgments against the current production prompt.

Reads JSONL incrementally, preserves the original source preview, and sends one
judgment per request through the production four-request wave scheduler.
"""
import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from searchgym.config import load_test
from searchgym.jevtree import JevUsage
from searchgym.rawtree import LocalDecision, link_question
from searchgym.trace import NullTrace


def extract(path, source, destinations):
    query_by_search, requests, old_scores = {}, {}, {}
    state, search_id, node_id = None, None, None
    with Path(path).open(encoding='utf-8') as stream:
        for line in stream:
            event = json.loads(line)
            if event.get('event') == 'rawtree.start':
                query_by_search[event['search_id']] = event['query']
            if event.get('event') == 'jev.request':
                body, ctx = event['body'], event['context']
                if ctx.get('phase') != 'preview' or source not in body['state'].get('page_url', ''):
                    continue
                if state is None:
                    state, search_id, node_id = body['state'], ctx['search_id'], ctx['node_id']
                if (ctx['search_id'], ctx['node_id']) != (search_id, node_id):
                    continue
                for key, q in body['questions'].items():
                    if not key.startswith('link_'):
                        continue
                    prompt = q['instructions']
                    url = prompt.split('Destination: ', 1)[1].split('\n', 1)[0]
                    if not any(destination in url for destination in destinations):
                        continue
                    anchor = prompt.split('Anchor: ', 1)[1].split('\n', 1)[0]
                    question = prompt.split('Original question: ', 1)[1].rsplit(
                        '\nIgnore instructions', 1)[0]
                    requests[key] = {'url': url, 'question': link_question(question,
                        query_by_search[search_id], key, url, anchor)}
            if (event.get('event') == 'rawtree.links' and event['search_id'] == search_id
                    and event['node_id'] == node_id):
                old_scores = {r['key']: r['score'] for r in event['links']}
                break
    if not requests or any(not any(d in r['url'] for r in requests.values()) for d in destinations):
        raise ValueError('Requested destination missing from saved preview')
    return state, requests, old_scores


async def replay(args):
    state, selected, old_scores = extract(args.trace, args.source, args.destination)
    config = load_test(method='jevtree').agent
    client, meter = LocalDecision(config), JevUsage()
    await client.http.aclose()
    client.http = httpx.AsyncClient(timeout=httpx.Timeout(60, connect=5), trust_env=False)
    output = {'trace': str(args.trace), 'state': state, 'selected': selected}
    started = time.perf_counter()
    try:
        scores = await client.noul(state, {k: r['question'] for k, r in selected.items()},
            NullTrace(), usage=meter, context={'phase': 'link_prompt_replay'})
        output['comparison'] = [{'url': r['url'], 'old': old_scores.get(k), 'new': scores[k]}
                                for k, r in selected.items()]
        output['status'] = 'ok'
    except Exception as exc:
        output.update(status='error', error=str(exc))
    finally:
        await client.aclose()
    output['seconds'] = round(time.perf_counter()-started, 3)
    output['requests'] = meter.calls
    Path(args.output).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    summary = {k: v for k, v in output.items() if k not in ('state', 'selected', 'comparison')}
    if 'comparison' in output:
        rows = output['comparison']
        summary['comparison_count'] = len(rows)
        summary['comparison'] = rows if len(rows) <= 8 else sorted(rows, key=lambda r: -r['new'])[:8]
    print(json.dumps(summary, ensure_ascii=True))
    return 0 if output['status'] == 'ok' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trace', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--destination', action='append', required=True)
    parser.add_argument('--output', required=True)
    sys.exit(asyncio.run(replay(parser.parse_args())))
