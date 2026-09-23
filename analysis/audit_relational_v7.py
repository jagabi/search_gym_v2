"""Offline matched-run audit. No model, search, fetch, or judge calls."""
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
RUNS = {
    'v7': '20260923-2239_depthsearch_gpt-oss-20b_browsecomp_ds_relational_v7',
    'v4': '20260922-0859_depthsearch_gpt-oss-20b_browsecomp_ds_answer_phase_v4',
    'v6': '20260923-1829_depthsearch_gpt-oss-20b_browsecomp_ds_independent_clues_v6',
    'o1': '20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1',
    'ra': '20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1',
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def records(folder):
    return {r['index']: r for line in (folder / 'records.jsonl').read_text(encoding='utf-8').splitlines()
            if line.strip() for r in [json.loads(line)]}


def audit(folder, row):
    counts, tokens = Counter(), Counter()
    invalid, session_ends, goals = Counter(), Counter(), Counter()
    events, timings = Counter(), defaultdict(list)
    calls_by_depth, roots_per_search = Counter(), Counter()
    request = None
    request_final = None
    extraction = {}
    gate_inputs = set()
    selected, seen, queries = [], {}, []
    search_start = None
    main_turn = 0
    main_result_chars = []
    input_chars = []
    invalid_examples = []
    case = {'index': row['index'], 'record': row, 'queries': queries, 'roots': selected}
    for line in (folder / row['dir'] / 'trace.jsonl').open(encoding='utf-8'):
        e = json.loads(line)
        kind = e['event']
        events[kind] += 1
        if kind == 'llm.request':
            request_main = e['elapsed_ms']
        elif kind == 'llm.response':
            counts['main'] += 1
            timings['main_ms'].append(e['elapsed_ms'] - request_main)
        elif kind == 'run.final_request':
            request_final = e['elapsed_ms']
        elif kind == 'run.final_response':
            counts['final'] += 1
            if request_final is not None:
                timings['final_ms'].append(e['elapsed_ms'] - request_final)
        elif kind == 'tool.call' and e['tool'] == 'web_search':
            main_turn = e['turn']
            queries.append({'turn': main_turn, 'query': e['arguments'].get('query'), 'elapsed_ms': e['elapsed_ms']})
            search_start = e['elapsed_ms']
        elif kind == 'tool.result' and e['tool'] == 'web_search':
            main_result_chars.append(e['result_chars'])
            if search_start is not None:
                timings['search_with_reading_ms'].append(e['elapsed_ms'] - search_start)
        elif kind == 'control.request':
            request = e
            input_chars.append(sum(len(str(m.get('content', ''))) for m in e['messages']))
        elif kind == 'control.response':
            counts['entry_' + e['mode']] += 1
            timings['entry_ms'].append(e['elapsed_ms'] - request['elapsed_ms'])
            if not e['valid']:
                decision = e.get('decision', 'invalid')
                if decision == 'invalid_tool_call':
                    payload = json.loads(request['messages'][1]['content'])
                    tools = e.get('tool_calls', [])
                    if len(tools) != 1:
                        decision = 'multiple_calls'
                    else:
                        try:
                            args = json.loads(tools[0]['arguments'])
                            url = args.get('url', '')
                            if tools[0]['name'] != 'web_fetch':
                                decision = 'wrong_tool'
                            elif url in seen:
                                decision = 'previously_selected_root'
                            elif any(s.get('url') == url or s.get('id') == url for s in payload['sources']):
                                decision = 'menu_entry_other_invalidity'
                            elif 'google.com/search' in url or 'bing.com/search' in url:
                                decision = 'search_url'
                            else:
                                decision = 'outside_current_menu'
                        except (ValueError, TypeError, AttributeError):
                            decision = 'malformed_args'
                invalid[decision] += 1
                if len(invalid_examples) < 3:
                    invalid_examples.append({'decision': decision, 'calls': e.get('tool_calls'), 'reasoning': e.get('reasoning', '')[:1400]})
        elif kind == 'search.selected_entry':
            roots_per_search[e['turn']] += 1
            seen[e['url']] = e['source']
            seen[e['source']] = e['url']
            selected.append({'turn': e['turn'], 'url': e['url'], 'source': e['source']})
        elif kind == 'search.entry_session_end':
            session_ends[e['reason']] += 1
        elif kind == 'explorer.extract_input':
            extraction[(e['depth'], tuple(e['urls']))] = e['elapsed_ms']
            supplied = '\n'.join(str(m.get('content', '')) for m in e['messages'][1:-1])
            if '18+ Access' in supplied:
                gate_inputs.add((e['depth'], tuple(e['urls'])))
        elif kind == 'explorer.response':
            phase = e['phase']
            counts['reader_' + phase] += 1
            calls_by_depth[f"d{e['depth']}_{phase}"] += 1
            tokens[phase + '_input'] += e.get('prompt_tokens', 0)
            tokens[phase + '_output'] += e.get('completion_tokens', 0)
            if phase in {'extract', 'recover'}:
                timings['extract_ms'].append(e['elapsed_ms'] - extraction[(e['depth'], tuple(e['urls']))])
            if phase == 'extract' and (e['depth'], tuple(e['urls'])) in gate_inputs:
                events['audit.age_gate_extractions'] += 1
            if phase == 'expand':
                counts['navigation_fetch' if e.get('tool_calls') else 'navigation_return'] += 1
        elif kind == 'expand.relation_task':
            goals['specific' if e['goal'] else 'fallback_original_question'] += 1
        elif kind == 'run.end':
            case['final_context_tokens'] = e.get('context_tokens')
    # navigation_fetch/navigation_return are subcounts, not additional calls.
    counted = sum(v for k, v in counts.items() if not k.startswith('navigation_'))
    return {
        'calls': dict(counts), 'calls_by_depth': dict(calls_by_depth), 'reader_tokens': dict(tokens),
        'record_calls': row['llm_calls'], 'counted_calls': counted,
        'invalid': dict(invalid), 'session_ends': dict(session_ends), 'goals': dict(goals),
        'events': dict(events), 'root_selections': len(selected),
        'roots_per_search': list(roots_per_search.values()),
        'timing_sums_ms': {k: sum(v) for k, v in timings.items()},
        'entry_input_chars': input_chars, 'main_result_chars': main_result_chars,
        'case': case, 'invalid_examples': invalid_examples,
    }


def main():
    folders = {k: ROOT / 'runs/test' / v for k, v in RUNS.items()}
    data = {k: records(p) for k, p in folders.items()}
    ids = sorted(data['v7'])
    overview = {}
    for name, rows in data.items():
        chosen = [rows[i] for i in ids]
        overview[name] = {
            'n': len(chosen), 'correct': sum(r['accuracy'] == 1 for r in chosen),
            'median_seconds': median(r['latency_s'] for r in chosen),
            'mean_seconds': mean(r['latency_s'] for r in chosen),
            **{field: sum(r.get(field, 0) for r in chosen) for field in
               ['llm_calls', 'input_tokens', 'output_tokens', 'reasoning_tokens', 'fetch_attempts',
                'fetch_failures', 'auto_fetches', 'expansion_nodes', 'searches']},
        }
    results = {}
    for name in ['v7', 'v4']:
        results[name] = {i: audit(folders[name], data[name][i]) for i in ids}
    aggregates = {}
    for name, audits in results.items():
        agg = {}
        for field in ['calls', 'calls_by_depth', 'reader_tokens', 'invalid', 'session_ends', 'goals', 'events', 'timing_sums_ms']:
            total = Counter()
            for a in audits.values():
                total.update(a[field])
            agg[field] = dict(total)
        for field in ['entry_input_chars', 'main_result_chars', 'roots_per_search']:
            vals = [v for a in audits.values() for v in a[field]]
            agg[field] = {'n': len(vals), 'mean': mean(vals) if vals else 0, 'median': median(vals) if vals else 0, 'max': max(vals, default=0)}
        agg['call_count_mismatches'] = [i for i, a in audits.items() if a['record_calls'] != a['counted_calls']]
        aggregates[name] = agg
    out = {'ids': ids, 'overview': overview, 'aggregates': aggregates, 'audits': results}
    path = ROOT / 'analysis/relational_v7_audit.json'
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'ids_n': len(ids), 'overview': overview, 'aggregates': aggregates}, indent=2))


if __name__ == '__main__':
    main()
