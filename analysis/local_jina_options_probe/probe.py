"""Compare local Reader extraction options; no model/JEV or hosted Reader calls."""
import concurrent.futures
import http.client
import json
from pathlib import Path
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(__file__).resolve().parent
URL = "https://weartesters.com/and1-the-best-shoes-of-a-legendary-brand/"
VARIANTS = {
    "current_markdown": {"X-Return-Format": "markdown"},
    "content": {"X-Respond-With": "content"},
    "markdown_remove_nav": {"X-Respond-With": "markdown", "X-Remove-Selector": "nav, header, footer, aside, [role=navigation]"},
    "markdown_article": {"X-Respond-With": "markdown", "X-Target-Selector": "article"},
}


def probe(item):
    name, options = item
    start = time.perf_counter()
    conn = http.client.HTTPConnection("100.111.87.95", 3001, timeout=45)
    result = {"name": name, "url": URL, "headers": options}
    try:
        conn.request("GET", "/" + URL, headers={"Accept": "text/plain", "X-No-Cache": "true", **options})
        response = conn.getresponse()
        body = response.read().decode("utf-8", errors="replace")
        (OUT / f"{name}.md").write_text(body, encoding="utf-8")
        terms = {}
        for label, pattern in {
            "founded_1993": r"began its journey in 1993",
            "university": r"University of Pennsylvania",
            "promotion_1999": r"summer of 1999",
            "retail_history": r"most successful in U.S. retail history",
        }.items():
            match = re.search(pattern, body, re.I)
            terms[label] = match.start() if match else None
        result.update(status=response.status, chars=len(body), term_positions=terms,
                      markdown_links=len(re.findall(r"\]\(https?://", body)))
    except Exception as exc:
        result["error"] = repr(exc)
    finally:
        conn.close()
    result["seconds"] = round(time.perf_counter() - start, 2)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(probe, VARIANTS.items()))
    (OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
