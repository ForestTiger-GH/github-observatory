# CS-11 — Reliability, Recovery, API Economics and Scaling Envelope

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE for the current observed/implemented envelope  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Operational cutoff:** Actions/runs through 2026-09-30.  
**Consumer:** future development/reliability work and research-only Current HOW fan-in.

## Question

What are the current reliability, recovery, performance and scaling limits of the collector, including API request geometry, rate-limit handling, large history/tree behavior and failure recovery?

## Evidence boundary

Inspected:

- current collector/API client/workflow implementation;
- all current run durations;
- current repository count and latest canonical commit totals;
- current request topology from CS-02..CS-07;
- current GitHub REST/GraphQL rate-limit and best-practice documentation.

No load test, synthetic rate-limit test, runner-kill experiment or very-large-repository experiment was performed. Scaling claims below distinguish direct request-count reconstruction from extrapolation.

## Current operational reliability evidence

Current durable run set:

- 8 scheduled normal collections;
- 1 manual backfill;
- 0 recorded repository-error runs;
- all corresponding Actions runs successful.

Normal collector durations:

```text
min   = 204 s  (3m24s)
max   = 275 s  (4m35s)
mean  = 226.6 s (~3m47s)
```

Observed backfill collector duration:

```text
178 s (~2m58s)
```

Workflow timeouts:

- normal collect: 30 minutes;
- backfill: 120 minutes.

At the current 28-repository corpus, execution time is therefore well inside the configured job timeout.

The multi-hour schedule delay found in CS-08 is upstream of collector runtime and must not be misclassified as collector slowness.

## Current request geometry

Current latest canonical commit total across the 28 repositories is about **6,550**.

With GraphQL history pages of 100 commits, the current repository set requires approximately:

```text
83 GraphQL history pages
+ 28 GraphQL head/total queries
= 111 GraphQL requests
```

per full activity rebuild, excluding retries.

At the current 12-public / 16-private visibility split, normal REST work is approximately:

```text
1 owner-repository discovery page

16 private ×:
  repository detail
  recursive tree
  languages
  views
  clones
= 80

12 public ×:
  same 5
  + referrers
  + paths
= 84

total REST ≈ 165
```

So a current successful normal run is roughly:

```text
165 REST requests
+ 111 GraphQL requests
≈ 276 API calls
```

before retries and before extra discovery pages if the repository universe grows beyond one 100-item page.

Backfill avoids metadata/tree/languages/rolling detail, so its current geometry is roughly:

```text
1 discovery
+ 2 × 28 daily Traffic
= 57 REST

+ 111 GraphQL activity calls
```

again before retries.

These are call counts, **not GraphQL point costs**.

## Scaling function

A useful current implementation model is:

```text
normal REST calls
≈ discovery_pages + 5N + 2P

normal GraphQL calls
≈ N + Σ history_pages(repo_i)

history_pages(repo_i)
≈ ceil(current_reachable_commits_i / 100)

backfill REST calls
≈ discovery_pages + 2N

backfill GraphQL calls
≈ normal GraphQL activity cost
```

where:

- `N` = discovered repositories;
- `P` = public repositories receiving rolling detail.

This exposes the primary scaling drivers:

1. repository count;
2. total reachable canonical history;
3. public-repository fraction;
4. recursive-tree response size;
5. retained CSV history and rewrite cost.

## Activity is the strongest long-history amplifier

Every normal run and backfill traverses the **entire current reachable commit history** for every repository.

There is no incremental “since last commit” cursor.

Thus a repository with 1,751 current commits (Compass) already requires 18 history pages each run; as histories grow, GraphQL request and processing cost grow even when daily activity is small.

This is deliberate current semantics, because full rebuild permits history rewrite/rebase reconciliation, but it creates a real cost curve.

## Tree-size behavior

File counts use one recursive tree request per repository.

If GitHub marks the recursive response truncated:

```text
files = blank
files_status = unknown_truncated
```

This protects correctness but does not reduce the cost of asking for the recursive tree.

Current latest corpus has no truncated tree. The largest latest exact file count observed is 1,966, so the present corpus has not empirically tested very large tree behavior.

## Local file rewrite amplification

Several persistence paths rewrite whole CSV files:

- activity: every current row every run;
- repository snapshots: whole file after upsert;
- languages: whole file after partition replacement;
- Traffic daily: whole file after upsert;
- rolling detail: whole file after partition replacement;
- status/run ledgers: whole file after upsert.

Consequences over long horizons:

```text
API cost can grow with history
and
local read/write cost can grow with retained day count
```

At current scale this is not causing an observed timeout, but the mechanism is linear rather than bounded by “today only”.

## Rate-limit contract vs current client

Current GitHub documentation says authenticated REST access commonly has a primary limit of 5,000 requests/hour for user-scoped authentication, with different limits for some GitHub App/Enterprise cases. GraphQL has a separate point budget. GitHub also applies secondary limits and recommends honoring:

- `Retry-After`;
- `x-ratelimit-remaining`;
- `x-ratelimit-reset`;
- longer/exponential waits for secondary limit failures.

Official references:

- https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
- https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api

The exact type/scopes/rate budget of `OBSERVATORY_TOKEN` are **UNKNOWN** to the repository and are intentionally not persisted.

## Current rate-limit handling gap

`GitHubClient` automatically retries only:

- HTTP 502;
- HTTP 503;
- HTTP 504;
- `URLError`.

It does **not** currently:

- read rate-limit response headers;
- query `/rate_limit`;
- wait until `x-ratelimit-reset`;
- honor `Retry-After`;
- specially retry 429;
- distinguish rate-limit 403 from permission 403.

This is a current reliability limitation.

### Traffic-specific ambiguity

Traffic code converts any Traffic HTTP 403/404 into an availability status.

Therefore a Traffic `403` caused by rate limiting would be represented the same way as another 403 availability/permission cause:

```text
unavailable_http_403
```

or:

```text
aggregate_ok_detail_unavailable_http_403
```

and would not count as `error_*` in the run-level error total.

No current run exercises this ambiguity.

## Serial request behavior

The collector issues requests serially rather than fan-out concurrency.

GitHub's current best-practice guidance recommends serial requests to reduce secondary-limit risk.

This is a current robustness property, albeit at the cost of wall-clock latency.

## Timeout amplification per request

Each request has a 60-second network timeout.

For a retried 502/503/504/network failure, the client can make the initial request plus three retries with 1/2/4-second sleeps.

A single pathological request can therefore consume several minutes before surfacing failure.

Because normal job timeout is 30 minutes, repeated slow failures across repositories can consume a significant fraction of the workflow budget even though current healthy runs finish in ~4 minutes.

This has not been observed in the current run set.

## Recovery model

### Per-repository degradation

Caught source-family errors:

- are recorded;
- allow later families/repositories to continue;
- can still lead to a successful workflow commit with partial data.

This is good for bounded progress and explicit evidence.

### No intra-run durable checkpoint

Generated files are committed/pushed only after the whole collector command returns successfully.

If a top-level/unhandled failure occurs late:

- earlier runner-local work may exist;
- no Git commit is created by the later step;
- next run/backfill must reconstruct from source again.

There is no repository-level checkpoint/commit after each repository.

### Next-run recovery

For recoverable source conditions, the next daily run can naturally retry current collection.

Manual backfill can reconstruct:

- current-reachable activity history;
- current source-window daily Traffic.

It cannot recover unavailable historical snapshot facts.

### Push failure

A plain final `git push` can fail if another actor advanced `main` after checkout. Shared collect/backfill concurrency does not protect against external pushes.

In that case collector work may be successful but unpersisted. Actions records the failure; in-repo `runs.csv` does not receive the unpushed attempt.

No current push failure is observed.

## Verification/recovery limitations

Current pre-run verification is only:

```text
python -m py_compile scripts/*.py
```

There is no test suite, simulation harness, API fixture replay or explicit recovery test in current Product realization.

Thus current high confidence is based mainly on:

- simple implementation;
- exact status/provenance;
- repeated successful production runs.

That is real evidence, but narrower than fault-injection assurance.

## Observed headroom and extrapolation limit

Current normal execution uses roughly 3.4–4.6 minutes of a 30-minute timeout.

This suggests substantial **current** runtime headroom.

It does not justify a linear forecast to arbitrary repository/history growth because:

- network latency varies;
- rate-limit behavior is nonlinear;
- one large tree/history can dominate;
- secondary limits can appear before primary budgets are exhausted;
- whole-file rewrite cost grows over time.

No performance model beyond the current request geometry has been validated.

## Negative findings

- No current run exceeds timeout.
- No current run records repository errors.
- No current file tree is truncated.
- No adaptive rate-limit handler exists.
- No incremental activity cursor exists.
- No conditional REST requests/ETags are used.
- No persistent intra-run checkpoint exists.
- No automatic workflow-level retry is configured.
- No concurrent API fan-out is used.

## UNKNOWN / limits

- Exact `OBSERVATORY_TOKEN` authentication type and primary budgets are UNKNOWN.
- GraphQL query point cost is not measured by the collector.
- Behavior under real rate limiting is unobserved.
- Very large repository trees/histories are untested.
- Long-horizon CSV rewrite performance is not benchmarked.
- GitHub-hosted runner/network variance is external.

## Current HOW contribution

```text
simple serial polling
+ full canonical activity rebuild
+ exact tree query
+ explicit per-family failure isolation
+ one final Git persistence boundary
```

works reliably at the current 28-repository / ~6,550-commit scale, with healthy runs around four minutes.

The dominant future cost curve is not today’s daily delta; it is repeated traversal/rewrite of accumulated state.

## Residue and routes

- Security/token exposure and workflow permissions → CS-12.
- Documentation of current operating limits and consumer assumptions → CS-13.
- Any redesign of incremental collection, rate-limit handling or checkpointing is explicitly outside this Study.

## Reopen / invalidation triggers

Reopen if:

- repository count/history/tree size materially increases;
- normal duration approaches workflow timeout;
- rate-limit/429/secondary-limit failure is observed;
- token/authentication model changes;
- API call/pagination strategy changes;
- activity becomes incremental;
- persistence/checkpoint architecture changes;
- current workflow gains retries/tests/fault injection.
