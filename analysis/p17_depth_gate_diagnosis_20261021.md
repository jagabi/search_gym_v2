# p17 depth suppression: gate and scheduler audit

User reporting requirement going forward: report accuracy, searches and runtime
together with visits/successes/reads by depth, fraction of searches that expand,
proposed/selected parents, child nominations/admissions and stop reasons. Do not
infer healthy DepthSearch operation from accuracy/runtime alone.

Saved p17 logs and source were inspected without running tests, model requests,
benchmarks or replays. No source code changes were made in this diagnosis.

## Actual traversal

| Depth | Admitted visits | Successful previews | Read documents |
|---|---:|---:|---:|
| 1 | 417 | 315 | 80 |
| 2 | 12 | 9 | 4 |
| 3 | 0 | 0 | 0 |

Only 6/78 searches (7.7%) descend. Five of ten questions have any descendant
visit. Of 84 document reads, 80 (95.2%) are depth 1. The root failure rate is
102/417; child failure rate 3/12. These are visits, including body-cache reuse,
not all distinct network fetches.

## Where depth is blocked

Initial decisions across 324 successful page previews are RETURN 250, READ 66,
EXPAND 8. Among 256 pages with extracted candidate links, initial decisions are
RETURN 194 (75.8%), READ 54, EXPAND 8 (3.1%). Initial decisions differ from final
decisions because reading changes evidence and available actions.

After those decisions and re-evaluations there are only nine parent proposals;
the parent beam selects eight. Their 316 individual link scores produce sixteen
per-parent child nominations. One falls below the link floor and the global beam
removes three more, leaving twelve admitted children. Thus parent width and link
floor are not where most opportunities disappear in this run. This does not imply
the rejected parents had useful links; many extracted links are generic navigation.

Traversal reasons across 78 searches: branches_closed 63, read_budget 11,
frontier_exhausted 4. Empty result searches also contribute to branches_closed;
that label is not proof that d3 reviewed every possible route.

### 1. Reading budget is a hard expansion veto

`action_questions()` sets can_expand to `... and not read_budget_exhausted()`.
After two document reads, EXPAND is removed even for nodes with candidate links.
This is a code constraint, not a low model judgment. Twelve linked nodes have a
final post-read request with two evidence cards and no EXPAND key. Three initially
preferred EXPAND over all alternatives before the read cap removed the action.

Both depth-2 nodes that initially preferred EXPAND lose that choice:

- q1196 Sree Padmanabhaswamy temple: initial EXPAND .58193, RETURN .52148,
  positive reading value .44206. Final action scores contain only RETURN .43153.
- q1230 Scribd traffic-scorecard record: initial EXPAND .57246, RETURN .45884,
  positive reading value .49470. Final scores contain only RETURN .38139.

The third case is q40's World Athletics source at depth 1. These establish a
structural veto; they do not prove the omitted links would improve accuracy.

This restriction was introduced deliberately in the preceding design, but its
effect on depth was underreported. Simply deleting it is insufficient: after two
reads a newly discovered better child cannot enter the unchanged two-read budget.
Read allocation and traversal scheduling have to be considered together.

### 2. Any READ proposal takes precedence over every EXPAND proposal

The depth loop executes reading whenever `reads` is nonempty, then re-evaluates
survivors. It does not compare the strongest EXPAND proposal with the strongest
READ proposal across nodes. Another node's reading request can therefore consume
the second read slot before a promising expansion is considered.

READ also uses max(original-question usefulness, current-query usefulness), while
EXPAND asks about uncertain destination evidence. A source that may provide one
query fact and a route that may discover a missing entity are different judgments;
their scalar maximum is not a validated estimate of comparative search benefit.

### 3. Coarse expansion gating hides Markdown destinations

`numbered_page()` replaces candidate Markdown URLs with link ids. Its documentation
explicitly says URL mapping remains in the caller. The preview/branch state has
the numbered page and search lead, not the candidate URL mapping. Visible anchor
text remains; bare URL text also remains, so the gate is not completely blind.

However, many destination paths are not supplied until the later per-link
`link_question()`, which includes Destination and Anchor. The gate asks for a
concrete useful route before showing some of the available route information.
This is a confirmed input limitation; its causal share of RETURN decisions has
not been measured. Full original prefixes already contain those URLs and are
bounded by the existing page-token limit, so improving the gate observation need
not entail an additional fetch or a full-document model read.

### 4. Reading does not refresh the outgoing-link pool

`link_inputs` is constructed from the initial bounded prefix. Selected original
chunks can supply deeper source content, but their links are not merged into that
node's expansion candidates. `refresh_actions` updates evidence while keeping the
original numbered page/link pool. A useful route discovered during reading may
therefore have no available link action. Whether a particular gold route was lost
this way is not established by this run.

### 5. Minimum reading occurs after traversal has already stopped

Forty searches invoke the zero-read selection at exit. This protects source
delivery but does not re-enter branch evaluation afterward. New bridge evidence
can reach the main model, yet cannot trigger another hop within that search.
Therefore p17 minimum reading is not itself a depth-restoration mechanism.

## Direction for improvement, before implementing

Priority is the decision structure, not a larger configured maximum depth:

1. Show sufficient actual destination information in the coarse route judgment.
2. Stop treating every READ proposal as globally prior to every EXPAND proposal;
   preserve the second read slot when an unresolved route is more promising.
   Keep reading-page choice separate from branch closure, as in p17.
3. Revisit the coupling between two reads and expansion termination. Avoid merely
   removing the veto while leaving no slot to read newly found sources.
4. Feed links from already-selected original chunks into routing before final
   closure, within the existing parent/child/visit bounds. Consider re-evaluation
   after the first actual evidence observation rather than unconditional exit.
5. Keep d3 responsible for whether a route is worth following. Do not force every
   question to depth 3, score all 6,927 observed link candidates, or expand every
   page just to improve a depth metric. Those changes would reintroduce excessive
   latency without evidence of better answers.

The strongest measured blockage is before per-link scoring. The read-budget veto
also directly explains why the two initially expansion-preferring depth-2 nodes
could not attempt depth 3. More reading alone has not addressed either issue.
Any next server evaluation should report this funnel alongside quality and cost.
