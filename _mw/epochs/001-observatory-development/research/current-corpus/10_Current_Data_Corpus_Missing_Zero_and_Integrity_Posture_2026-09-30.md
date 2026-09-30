# CS-10 — Current Data Corpus, Missing/Zero Semantics and Integrity Posture

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE for the declared current-corpus assurance frame  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Latest normal data partition:** `data_date_utc=2026-09-29`, collected 2026-09-30.  
**Consumer:** data consumers, future analytics, reliability/privacy studies and research-only Current HOW fan-in.

## Question

How complete and internally coherent is the generated corpus now, and how must a consumer distinguish zero, absent, unavailable, stale and UNKNOWN?

## Assurance boundary

This Study combines:

- complete Product-baseline Git tree census;
- complete current repository registry;
- complete current run/status ledgers;
- all 28 latest `repository.csv` file-count states;
- all 28 current `activity.csv` histories for changed-file UNKNOWN review;
- all 28 `views.csv` horizons;
- public/private Traffic family topology;
- implementation key/persistence semantics from CS-02..CS-09.

It is not a byte-for-byte independent validator of every historical field in all 167 CSV files. No separate validation tool currently exists. Claims below distinguish complete structural/current-state checks from mechanism-derived guarantees.

## Current corpus size and topology

At the Product baseline:

- complete recursive Git tree: **187 files**;
- generated CSV files under `ForestTiger-GH/`: **167**;
- discovered repositories: **28**;
- public: **12**;
- private: **16**;
- archived: **1**;
- latest registry rows marked present: **28**.

The 167 generated CSV files exactly match the current structural policy:

```text
16 private repos × 5 common families = 80
12 public repos  × 7 families        = 84
global registry + status + runs      =  3
                                       ---
                                       167
```

Common per-repository families:

- `repository.csv`;
- `activity.csv`;
- `languages.csv`;
- `traffic/views.csv`;
- `traffic/clones.csv`.

Public-only additional families:

- `traffic/referrers.csv`;
- `traffic/paths.csv`.

Complete tree inspection found:

- no public repository missing either detail file;
- no private repository containing either detail file;
- no repository missing any common family.

This is a strong structural-consistency result for the exact baseline.

## Current latest collection health

Latest normal run:

```text
data_date_utc              = 2026-09-29
repositories_seen          = 28
repositories_succeeded     = 28
repositories_with_errors   = 0
```

There are exactly 28 latest repository-status rows.

Status combinations:

```text
12 public:
metadata=ok
languages=ok
activity=full_canonical_history_closed_days
traffic=ok

16 private:
metadata=ok
languages=ok
activity=full_canonical_history_closed_days
traffic=ok_aggregate_only_private
```

The 12/16 split exactly matches the registry visibility distribution.

No latest current source-family error is recorded.

## Current run corpus

`runs.csv` contains 9 durable rows:

- 1 backfill;
- 8 normal collects;
- 0 rows with nonzero `repositories_with_errors`.

This does **not** prove there was never another workflow attempt, because same-key reruns replace and pre-terminal/unpushed failures may exist only in Actions metadata. Current Actions metadata examined in CS-08 matches these nine currently visible runs.

## Repository snapshot integrity

All 28 latest repository snapshots have:

```text
files_status = exact
```

At this cutoff:

- no `unknown_truncated`;
- no `exact_empty_repository`;
- no blank current file count.

Thus the current corpus has no observed file-count UNKNOWN.

This is empirical current-state evidence, not a guarantee against future truncation.

## Activity integrity

All 28 activity files were inspected for `commits_with_unknown_changed_files`.

Current result:

```text
sum of commits_with_unknown_changed_files across all activity rows = 0
```

Therefore no current stored activity row contains changed-file-count uncertainty.

Again, the field remains semantically necessary because the source can return unavailable values later.

Activity rows are sparse, full-current-reachable-history projections, so absence of a date has special semantics only when freshness/status establishes a successful current rebuild.

## Current period map

The corpus contains different historical horizons by design.

### Activity

Historical reach is determined by currently reachable default-branch history, not Observatory start.

Current examples extend back to:

```text
2021-03-05
```

and forward through the latest closed day for repositories with current activity.

### Repository and language snapshots

Normal snapshot collection begins with the first normal run for each discovered repository.

Current run-universe growth:

```text
backfill data_date 2026-09-21: 23 repositories
collect  data_date 2026-09-22: 25
collect  data_date 2026-09-23: 26
...
collect  data_date 2026-09-27: 28
collect  data_date 2026-09-29: 28
```

Therefore later-discovered repositories legitimately have shorter snapshot series.

### Daily Traffic

Current `views.csv` horizons commonly begin around 2026-09-08/09 even though Observatory's first durable run is later, because initial source retrieval/backfill can return earlier dated Traffic.

One especially important preserved case is AppDock:

```text
first current stored view date = 2026-08-31
last_observed_at on that row   = 2026-09-22T20:28:31Z
```

This is longer than GitHub's current official “last 14 days” documentation would predict.

The reason is **UNKNOWN** and has been fed back into CS-06.

### Rolling Traffic detail

Public rolling snapshots begin only when normal public collection returns top-table rows. Backfill does not create them. An empty successful top table can therefore leave no partition rows for a date.

## Missing ≠ zero matrix

The current Product cannot be consumed safely with a universal “missing = 0” rule.

| Surface | Explicit zero | Missing/absent can mean | Required context |
| --- | --- | --- | --- |
| repository file count | `files=0, files_status=exact_empty_repository` | UNKNOWN when blank with `unknown_truncated` | `files_status` |
| activity day | no zero row is materialized | no currently reachable commits **if** current rebuild succeeded; otherwise possibly stale/unavailable | activity status + `last_observed_at` |
| language row/partition | zero bytes could be returned per language; empty map produces no rows | successful empty language map or uncollected/stale file | language status + partition date |
| views/clones | explicit `count=0, uniques=0` can exist | source may omit the date; not collected; source unavailable; repository not yet present | Traffic status + freshness |
| referrer/path item | count can be positive when in top table | below top-10, no traffic, empty successful table, not collected, or private-policy omission | visibility + Traffic status + snapshot date |
| referrer/path file | rows for public only | expected absent for private | registry visibility |
| source-family status | explicit `error_*` / availability strings | older file can remain after later source failure | latest status row |
| registry presence | explicit `present_on_last_scan=false` | not currently discovered but retained historically | registry row |

This matrix is the practical enforcement of the root invariant:

> missing is not zero.

## Successful Traffic status does not guarantee a row for every day

Current `views.csv` inspection found several repositories whose latest stored view date is 2026-09-28 even though the 2026-09-29 collection has a successful Traffic status.

Other repositories have an explicit zero row for 2026-09-29.

Therefore the source/output behavior itself demonstrates:

```text
successful Traffic query
does not imply
a materialized row for every closed UTC date
```

Consumers must not synthesize missing daily rows to zero without an explicit analytic rule outside the evidence layer.

## Cross-family reconciliation: snapshot total vs closed-day activity

Several active repositories have:

```text
repository.csv current total commits
>
sum(activity.csv commits through cutoff)
```

This is expected when commits exist on the current UTC day:

- snapshot total is current at `observed_at`;
- activity intentionally excludes current-day commit events.

This is a valid temporal difference, not an integrity failure.

## Status semantics limit

As established in CS-07:

```text
repositories_succeeded
= repositories with no status beginning error_
```

Therefore availability states such as:

```text
unavailable_http_403
```

would still count as “succeeded” in the run summary.

The current latest run has no such state, so its 28/28 status is clean under both broad and stricter availability readings. But future consumers must not equate the field with universal family completeness.

## Rerun/attempt integrity limit

Several files are latest-value-per-key rather than immutable attempt histories.

Particularly:

- `runs.csv` replaces same `(data_date_utc, mode)`;
- `repository-status.csv` replaces same `(data_date_utc, repository_id)`;
- status does not retain `mode`.

Thus corpus integrity is oriented toward **latest supported state for a semantic key**, not forensic preservation of every collector attempt.

Actions metadata is a separate operational source.

## Provenance strengths

The current corpus consistently carries one or more of:

- `data_date_utc`;
- exact `observed_at`;
- `last_observed_at`;
- run start/finish;
- repository ID / directory context;
- explicit source-family status.

This makes many apparent inconsistencies explainable without hidden assumptions.

The strongest examples are:

- delayed snapshot attribution recoverable via `observed_at`;
- activity historical refresh recoverable via `last_observed_at`;
- private Traffic detail omission recoverable via visibility + status;
- file-count exactness recoverable via `files_status`.

## Current integrity findings

### Strong current results

- generated topology exactly matches current visibility policy;
- all 28 latest source status rows are present;
- latest run and latest statuses reconcile to 28 repositories / 0 errors;
- every latest file count is exact;
- no current activity changed-file UNKNOWN exists;
- public/private rolling-detail boundary is perfectly reflected in file topology;
- exact timestamps allow attribution-vs-observation distinctions.

### Material limitations

- no immutable collector-attempt ledger;
- no mode in repository-status key;
- no full independent row-level validator;
- Traffic source/documentation window is contradicted by at least one preserved historical response;
- missing daily Traffic rows can coexist with successful Traffic collection;
- old retained files can remain after a later source failure, so status/freshness is essential;
- no current operational failure examples test error recovery.

## No silent normalization

Nothing in this Study converts:

- absent row → zero;
- unavailable → zero;
- old last-observed value → fresh;
- top-table absence → no traffic;
- current snapshot total → closed-day daily activity;
- Research recommendation → Product semantics.

That discipline is necessary for future analytics.

## Current HOW contribution

A safe consumer model is:

```text
discover repository in registry
→ determine visibility/presence
→ locate family file
→ read exact schema semantics
→ bind semantic date and observation freshness
→ check current source-family status
→ distinguish explicit zero / empty / unavailable / UNKNOWN / policy omission
→ only then derive an analytical series
```

The generated corpus is internally coherent at the current structural/current-status level, but its evidence must be interpreted as a **typed, provenance-bound evidence set**, not as a rectangular database where every absent cell is zero.

## Residue and routes

- reliability/performance sources of future incompleteness → CS-11;
- privacy/access interpretation → CS-12;
- consumer-route/documentation guardrails → CS-13.
- An independent full historical row validator remains a future tooling/assurance possibility, not part of current Product or this Commission.

## Reopen / invalidation triggers

Reopen if:

- repository/family counts change materially;
- latest run records a source-family failure/unavailability;
- file-count UNKNOWN appears;
- changed-file UNKNOWN appears;
- generated schema/key topology changes;
- a row-level integrity defect is discovered;
- Traffic source-window evidence is better explained or changes;
- same-day mixed-mode status collision is observed.
