# Page-batch failure diagnosis

Run: `20261017-1028_jevtree_gpt-oss-20b_browsecomp_raw_d3_pagebatch_serial10`.

All three completed questions failed on the same server response:

```json
{"error":{"message":"questions: at most 64 for this model","type":"BadRequestError","param":null,"code":400}}
```

| Question | First failing node | Links | Total judgment keys | Elapsed until question end |
|---|---|---:|---:|---:|
| 40 | n0 | 70 | 72 | 9.9 s |
| 57 | n17 | 118 | 120 | 169.3 s |
| 117 | n2 | 112 | 114 | 148.0 s |

This was an invalid request, not an accuracy result. The prior change bundled
every judgment without implementing the server's 64-key limit.

A second defect is visible in question 40: its trace contains another HTTP 400
at 114.4 seconds although the question had ended at 9.9 seconds. Default
asyncio.gather propagated the first exception without cancelling sibling work.
Question-level workers=1 did not prevent these orphaned tasks from overlapping
the next question.

Fix (rawtree version 3):

- At most 64 keys per HTTP request; retain every candidate and score key.
- Keep direct/query page scores with the first 62 links. Overflow links use the
  fewest additional packets with identical source content; merge before ranking.
  The observed 72/120/114-key pages each require two requests.
- Cancel and join sibling workers on errors or parent cancellation at every
  tree/read/bundle/chunk gather boundary.
- Include server error text in propagated errors; log packet counts and request
  cancellation. The server's own compute cancellation is outside this guarantee.
- Bump the rawtree version so cached agent results cannot be confused with the
  preceding implementation.

Validation: 12 offline tests passed. They cover strict mock-server rejection
above 64 keys, all three observed request sizes, 64/65/128/129 boundaries,
302 keys, score/key preservation, shared source content, normal single packets,
active and queued sibling cleanup, nested cancellation, and existing tree/chunk
behavior. No live benchmark or model inference was launched.
