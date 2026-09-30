# CS-09 — Backfill, Rerun and Replacement Semantics

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Observed backfill evidence:** workflow_dispatch on 2026-09-22, collector 20:28:31Z→20:31:29Z, 23 repositories, 0 recorded errors.  
**Consumer:** recovery/history consumers, corpus assurance and later reliability study.

## Question

How do manual backfill, same-day reruns and replacement semantics work now, and what historical states can or cannot be reconstructed?

## Evidence boundary

Inspected:

- `.github/workflows/backfill.yml`;
- `scripts/backfill.py`;
- shared `collect("backfill")` path;
- upsert/rewrite primitives;
- `SCHEMA.md`;
- current Actions metadata for the observed backfill;
- `_collection/runs.csv` and backfill status rows.

Only one current backfill run is empirically present. Same-day mixed-mode collision behavior below follows directly from current persistence keys but is not observed in the current corpus.

## Backfill is current-time reconstruction, not a dated historical replay

The backfill workflow has no date/range input.

It performs:

```text
workflow_dispatch at current time T
→ collect("backfill")
→ cutoff = current UTC date - 1
→ current repository discovery
→ current registry reconciliation
→ full current-reachable activity reconstruction
→ currently available closed-day views/clones
→ status/run records for current closed-day partition
```

Thus “backfill” means:

> populate/rebuild history that is supportable **from sources available now**.

It does not mean:

> ask GitHub what every repository looked like on arbitrary past date X.

## Families supported by backfill

### Activity: broad historical reach, bounded by current reachability

Activity is fully reconstructed from the current default-branch reachable graph and can therefore reach far earlier than Observatory's own start date.

This can recover:

- commit counts by current-reachable commit `committedDate`;
- changed-file occurrence aggregates when supplied.

It cannot recover:

- commits no longer reachable;
- historical default-branch choices;
- historical branch topology;
- discarded commit-level detail.

### Daily views/clones: source-window bounded

Backfill queries current GitHub Traffic and admits only closed-day rows still returned by the source.

The upstream API exposes a recent rolling window; backfill cannot query arbitrary old daily Traffic.

Older Traffic can exist in Observatory only if it was already persisted during a prior period when GitHub still returned it.

### Repository snapshots: deliberately not backfilled

```text
metadata_status = skipped_backfill_current_snapshot
```

No current repository metadata is copied backward into historical dates.

### Language snapshots: deliberately not backfilled

```text
languages_status = skipped_backfill_current_snapshot
```

No current language map is fabricated as past state.

### Rolling referrers/paths: deliberately not backfilled

`include_rolling_snapshot=false` causes Traffic collection to stop after daily views/clones.

Thus no historical top-table snapshots are invented.

## Registry still changes during backfill

A subtle but important current behavior:

```text
list_owned_repositories()
→ update_registry(...)
```

runs before mode-specific per-repository logic.

Therefore backfill **does**:

- discover current repositories;
- set current `last_seen_at`;
- set current presence;
- add newly discovered repositories;
- perform ordinary rename reconciliation.

Backfill skips current repository/language snapshots, but it is not read-only with respect to the global repository registry.

## Current observed backfill

Actions metadata:

```text
event = workflow_dispatch
created/start = 2026-09-22T20:28:23Z
conclusion = success
```

Collector durable record:

```text
data_date_utc = 2026-09-21
started_at    = 2026-09-22T20:28:31Z
finished_at   = 2026-09-22T20:31:29Z
mode          = backfill
repositories_seen = 23
repositories_succeeded = 23
repositories_with_errors = 0
```

The few-second difference between Actions start and collector start is consistent with workflow setup/step execution.

## Backfill Traffic status

Because backfill exits Traffic handling immediately after daily views/clones:

```text
traffic_status = ok_closed_days_only
```

on successful backfill regardless of public/private detail policy.

This means the status describes **mode-limited expected behavior**, not missing detail failure.

## Same-day rerun semantics

The current persistence model is largely **replacement-idempotent by semantic key**, not immutable-attempt logging.

### Repository snapshot

Key:

```text
data_date_utc
```

A rerun replaces that day's surviving snapshot row.

### Languages

Whole `data_date_utc` partition replaced.

### Activity

Entire current canonical history projection rewritten.

### Daily Traffic

Same `traffic_date_utc` values overwritten by newly returned source rows.

### Rolling Traffic

Whole current `data_date_utc` partition replaced.

### Run summary

Key:

```text
(data_date_utc, mode)
```

Same-mode rerun on the same closed day replaces the prior run summary.

### Repository status

Key:

```text
(data_date_utc, repository_id)
```

Same-day rerun replaces prior status for that repository.

## Key idempotence ≠ byte idempotence

Even if GitHub source facts do not change, rerunning can change:

- `observed_at`;
- `last_observed_at`;
- run start/finish timestamps;
- source-returned revisable Traffic values;
- current-reachable history after Git changes.

Therefore:

```text
no duplicate semantic key
≠ identical file bytes
≠ immutable attempt history
```

The current design preserves the latest supported representation for a key.

## Important mixed-mode status collision

`runs.csv` includes `mode` in its key.

`repository-status.csv` does **not** contain a `mode` field and is keyed only by:

```text
(data_date_utc, repository_id)
```

Therefore if normal collect and backfill both run for the same `data_date_utc`:

- two distinct run summaries can coexist in `runs.csv`;
- the later mode's repository-status row will replace the earlier mode's row.

This can erase whether the surviving source-family status came from normal collection or backfill.

No such same-day mixed-mode collision exists in the current observed corpus: backfill owns 2026-09-21 and the first normal collect owns 2026-09-22.

This is a current structural limitation, not an observed corruption event.

## Attempt-history ceiling

Because `runs.csv` retains one row per `(data_date_utc, mode)`, a same-mode rerun on the same closed day overwrites:

- prior started_at;
- prior finished_at;
- prior repository counts.

Similarly, per-repository status is overwritten for that date.

GitHub Actions remains a separate source of attempt history, but the in-repository ledger is **latest-result-per-key**, not an immutable run-attempt ledger.

## Recovery value

Backfill is valuable for two different recovery classes:

1. rebuilding activity from still-reachable canonical Git history;
2. recovering recent daily Traffic still exposed by GitHub.

It is not capable of recovering unsupported historical snapshot families.

This preserves epistemic honesty:

```text
current evidence that can support a historical claim
→ may be reconstructed

historical fact no longer available from source
→ remains unavailable
```

## Write amplification

Activity rebuild stamps current `last_observed_at` on every surviving activity row.

Therefore a backfill can rewrite many historical lines even when numeric activity has not changed.

This is expected current provenance behavior but contributes to runtime/write cost, routed to CS-11.

## Facet reconciliation

### Accepted/documented

Current schema says backfill is explicit/manual, reconstructs only supportable history and must not fabricate unavailable historical snapshots.

### Implemented

The backfill path exactly skips metadata/languages/rolling Traffic and rebuilds activity plus currently available daily Traffic.

### Observed

One successful backfill is currently present and shows the expected skipped snapshot statuses / closed-days-only Traffic behavior.

## Negative findings

- No arbitrary historical date input exists.
- No historical metadata or language reconstruction exists.
- No historical rolling referrer/path reconstruction exists.
- No unreachable Git history recovery exists.
- No immutable same-mode attempt log exists in `runs.csv`.
- No current same-day backfill/collect status collision is observed.

## UNKNOWN / limits

- Operational behavior after a failed backfill has not been observed.
- Exact Traffic history recoverable on a future backfill depends on what GitHub still returns at that time.
- Mixed-mode status collision is code-proven but not empirically exercised.
- External Actions attempt history can outlive or differ from in-repository run evidence; full retention policy is platform-owned.

## Current HOW contribution

```text
manual backfill at current T
→ discover current repositories
→ update current registry
→ rebuild all current-reachable closed-day activity
→ refresh only daily Traffic still available
→ deliberately skip current snapshot families and rolling detail
→ replace latest semantic keys rather than append attempts
```

Backfill is a **bounded recovery mechanism**, not time travel.

## Residue and routes

- Cross-corpus status/attempt interpretation → CS-10.
- Runtime/write amplification and recovery limits → CS-11.
- Consumer documentation of backfill semantics → CS-13.

## Reopen / invalidation triggers

Reopen if:

- backfill accepts date/range parameters;
- snapshot or rolling families become backfillable;
- run/status keys gain immutable attempt identity or mode;
- registry behavior is separated from backfill;
- Traffic source window changes;
- an actual rerun/mixed-mode collision provides materially new evidence.
