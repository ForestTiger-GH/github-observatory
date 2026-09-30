# CS-07 — Collector Orchestration, Failure Isolation and Terminal Status

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Consumer:** reliability, corpus-assurance, scheduled-operation and backfill studies.

## Question

How does one collector execution orchestrate GitHub requests, retries, per-repository failures, persistence and terminal status?

## Evidence boundary

Inspected:

- complete `collect()` control flow;
- `GitHubClient` request/retry/pagination behavior;
- normal/backfill entrypoints;
- both workflows;
- current `_collection/runs.csv` and `repository-status.csv`;
- current source-family implementations from CS-02 through CS-06.

No current recorded run contains a per-repository `error_*` status, so failure-path behavior is established from code/contract rather than current failure examples.

## Top-level execution sequence

```text
validate OBSERVATORY_TOKEN + mode
→ establish started / observed_at / closed-day cutoff
→ authenticated owner-repository discovery
→ update durable registry in runner workspace
→ for each discovered repository:
     activity
     metadata snapshot (collect only)
     languages (collect only)
     Traffic
     classify repository terminal status
→ write repository-status.csv
→ write runs.csv
→ print summary
→ return 0
```

The collector's own execution boundary ends before Git commit/push; workflow persistence is CS-08.

## Failure domains

Current implementation has two materially different failure classes.

### 1. Pre-loop / terminal infrastructure failure

These operations are not enclosed by the per-repository catch structure:

- token/mode validation;
- repository discovery;
- creation of the data root;
- registry reconciliation/write;
- final status/run writes;
- unexpected top-level exceptions.

A failure here can terminate Python non-zero before a same-run durable `runs.csv` record is written.

If the workflow step fails, subsequent commit/push steps are not normally executed.

Therefore:

```text
absence from runs.csv
does not prove
no workflow attempt occurred
```

External Actions metadata is a separate operational evidence plane.

### 2. Per-repository source-family failure

Inside each repository iteration, the collector isolates:

- activity;
- metadata;
- languages;
- Traffic.

Each family has an explicit status field.

A failure in one family does not automatically stop other families or later repositories.

This permits a **partial successful collection commit with explicit failure evidence**.

## Per-repository status initialization

For normal collect:

```text
metadata_status  = not_run
languages_status = not_run
activity_status  = not_run
traffic_status   = not_run
```

For backfill:

```text
metadata_status  = skipped_backfill_current_snapshot
languages_status = skipped_backfill_current_snapshot
```

Activity and Traffic still execute in backfill.

## Error classification

`status_for_error()` maps:

- `GitHubAPIError` → `error_http_<status|unknown>`;
- other exception → `error_<ExceptionClass>`.

But Traffic deliberately returns several **non-error availability/status outcomes**:

- `unavailable_http_403`;
- `unavailable_http_404`;
- `aggregate_ok_detail_unavailable_http_403`;
- `aggregate_ok_detail_unavailable_http_404`;
- `ok_aggregate_only_private`;
- `ok_closed_days_only`;
- `ok`.

These returned states do not begin with `error_`.

## Run-level “succeeded” semantics

After a repository finishes:

```python
if any(status.startswith("error_")):
    repositories_with_errors += 1
else:
    repositories_succeeded += 1
```

Therefore current `repositories_succeeded` means:

> repositories whose terminal source-family statuses contain no `error_*`.

It does **not** mean:

> every optional/desired observation family was available and persisted.

A repository with:

```text
traffic_status=unavailable_http_403
```

would still count as `repositories_succeeded`.

A private repository with:

```text
traffic_status=ok_aggregate_only_private
```

also counts as succeeded, correctly reflecting the intentional policy.

This is a critical interpretation boundary for `runs.csv`.

## Process exit semantics

After all per-repository processing and status/run writes, `collect()` returns `0` even when `repositories_with_errors > 0`.

Thus:

```text
GitHub Actions collector step success
≠ every repository/source family succeeded
```

Per-repository failure visibility lives in:

```text
repository-status.csv
+
runs.csv repositories_with_errors
```

No observed current run has a nonzero error count, but the contract explicitly permits it.

## HTTP client retry semantics

The stdlib-only client performs up to the initial attempt plus three retries for:

- HTTP 502;
- HTTP 503;
- HTTP 504;
- `URLError` network failures.

Backoff before retry is:

```text
1 second
2 seconds
4 seconds
```

Each HTTP request uses a 60-second timeout.

Other HTTP errors, including ordinary 403/404 outside the special Traffic handling, are not automatically retried by `GitHubClient`.

There is no current specialized rate-limit/backoff parser for `Retry-After`, primary/secondary rate-limit reset, or abuse responses. CS-11 owns scaling/rate-limit implications.

## Pagination

### REST repository discovery

`get_paginated()` uses:

- `per_page=100`;
- incrementing `page`;
- termination when returned page length is less than `per_page`.

### GraphQL activity

Commit history uses cursor pagination with `first:100` until `hasNextPage=false`.

There is no bounded maximum page count in current implementation.

## Intra-repository dependency and fallback

Activity attempts to resolve:

```text
head_oid
total_commits
```

first.

Metadata snapshot reuses those values if available.

If activity failed before they were established, metadata attempts `get_canonical_head_and_total()` again.

Thus metadata has a limited recovery path from an activity-stage failure.

Languages and Traffic do not depend on activity success.

## Write semantics inside the runner

CSV persistence is file-based and mostly whole-file rewrite:

- generic writes use `csv.DictWriter`;
- upserts reconstruct a merged in-memory map and rewrite the file;
- partitions are removed/replaced in memory and rewritten;
- activity is rebuilt and fully rewritten.

There is no temporary-file + atomic-rename mechanism in the Python writer.

However, accepted repository persistence is normally later gated by the Git workflow:

```text
collector process completes
→ git add ForestTiger-GH
→ one commit
→ push
```

An unhandled Python failure normally prevents the workflow's later commit step from running, so runner-local partial writes are not automatically promoted to `main`.

Caught per-repository failures are different: the collector intentionally completes, writes status evidence and allows successful partial results to be committed.

## Collection status as evidence

`repository-status.csv` is keyed by:

```text
(data_date_utc, repository_id)
```

A same-day rerun replaces the repository's status row.

`runs.csv` is keyed by:

```text
(data_date_utc, mode)
```

A same-day rerun of the same mode replaces the run summary rather than retaining every attempt.

Attempt-history implications belong to CS-09.

## Current observed operating state

At the Product cutoff:

- eight scheduled normal collection runs are durably represented after the initial backfill;
- the latest run saw 28 repositories;
- latest `repositories_with_errors=0`;
- every latest metadata/language/activity status is successful;
- public Traffic is `ok`;
- private Traffic is `ok_aggregate_only_private`.

Current operation therefore provides no empirical example of the error branches.

## Verification gate before collection

Both workflows run:

```text
python -m py_compile scripts/*.py
```

before executing the collector.

This verifies Python syntax/import compilation only. No separate test suite is present in current repository realization.

Operational success and generated/status evidence are therefore the primary current runtime evidence.

## Negative findings

- No retry for every HTTP error.
- No special rate-limit handler.
- No cross-run transaction database.
- No immutable per-attempt run ledger.
- No all-or-nothing requirement across repositories.
- No requirement that per-repository errors make the workflow fail.
- No unit/integration test suite found in the complete current tree.

## UNKNOWN / limits

- Actual behavior under primary/secondary GitHub rate limiting is not observed in current runs.
- Runner interruption during an individual CSV write is not observed.
- External concurrent pushes are outside the collector's own concurrency model.
- Whether a downstream consumer treats `repositories_succeeded` as “complete” is unknown and would be an external misuse, not established current Product behavior.

## Current HOW contribution

```text
global discovery / registry
→ per-repository independently guarded source families
→ explicit family statuses
→ partial progress allowed
→ repository success = no error_* status
→ final status/run summaries
→ process returns success even with recorded per-repository errors
```

The collector is intentionally **degradable and evidence-bearing**, not transactional across the entire repository universe.

## Residue and routes

- Workflow schedule/concurrency/commit/push boundary → CS-08.
- Same-day rerun/attempt replacement and backfill → CS-09.
- Corpus-wide interpretation of availability/error/missing → CS-10.
- Rate-limit/performance/recovery envelope → CS-11.

## Reopen / invalidation triggers

Reopen if:

- try/catch boundaries or status vocabulary change;
- per-repository errors begin to fail the process;
- retry/backoff logic changes;
- persistence becomes transactional/atomic or database-backed;
- status/run keys change;
- tests/gates change materially;
- an observed failure reveals behavior inconsistent with this code-derived model.
