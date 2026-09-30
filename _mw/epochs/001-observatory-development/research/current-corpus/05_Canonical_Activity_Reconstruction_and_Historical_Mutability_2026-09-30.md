# CS-05 — Canonical Activity Reconstruction and Historical Mutability

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Consumer:** activity consumers, future analytics, backfill/reliability studies.

## Question

What exactly does `activity.csv` mean now, how is it reconstructed, what does absence mean, and how can historical rows change?

## Evidence boundary

Inspected:

- GraphQL head/history queries;
- `iter_canonical_history()`, `aggregate_commits()`, `rebuild_activity()`;
- current `activity.csv` for all 28 discovered repositories;
- latest `repository.csv` commit totals;
- `SCHEMA.md`;
- current collection-status records.

No merge/rebase rewrite was deliberately performed. Historical mutability is established from the source/algorithm contract rather than from an induced destructive experiment.

## Source model

For every repository, the collector resolves the **current default branch** and walks its reachable commit history through GraphQL:

```graphql
defaultBranchRef {
  target {
    ... on Commit {
      history(first: 100, after: $after) {
        nodes {
          committedDate
          changedFilesIfAvailable
        }
      }
    }
  }
}
```

All pages are traversed until `hasNextPage=false`.

The collector does not store:

- branch/ref name;
- commit SHA;
- author;
- commit message;
- changed paths;
- diff.

Only the permitted daily aggregate survives.

## Daily aggregation

For each reachable commit:

```text
day = committedDate[:10]
if day <= current closed-day cutoff:
    commits += 1
    if changedFilesIfAvailable is known:
        changed_file_occurrences += changedFilesIfAvailable
    else:
        commits_with_unknown_changed_files += 1
```

Result rows are:

```text
activity_date_utc
commits
changed_file_occurrences
commits_with_unknown_changed_files
last_observed_at
```

## Meaning of the three activity measures

### `commits`

Number of commits in the **current reachable default-branch history** whose GitHub `committedDate` falls on that UTC calendar date.

It is not:

- number of pushes;
- number of PRs;
- number of authored commits across all branches;
- number of commits that first became reachable that day.

### `changed_file_occurrences`

Sum of `changedFilesIfAvailable` over those commits.

It is **not unique files changed**.

If the same file changes in ten commits, its occurrence can contribute ten times. It is also not line churn.

### `commits_with_unknown_changed_files`

Count of included commits where GitHub did not provide `changedFilesIfAvailable`.

This prevents missing changed-file counts from silently becoming zero.

## Full rebuild semantics

Every collector execution calls:

```text
rebuild_activity(...)
```

which:

1. traverses the full current reachable default-branch history;
2. aggregates every eligible closed-day commit;
3. rewrites the entire `activity.csv`;
4. stamps every surviving row with the current run's `last_observed_at`.

Therefore `activity.csv` is a **materialized current projection of canonical reachable history**, not an append-only event log.

## Historical mutability

Because the source is current reachability:

```text
merge / rebase / force-push / history rewrite / default-branch change
→ reachable graph changes
→ a later full rebuild can change old activity dates
```

A 2026-05 row can legitimately differ after a September observation if the current canonical graph changed.

The row's `activity_date_utc` is the commit event date.  
The row's `last_observed_at` is the freshness of this current reconstruction.

These must not be conflated.

## Sparse-day semantics

The aggregator creates a row only for dates that have at least one included commit.

Thus `activity.csv` is sparse.

For a repository whose latest activity rebuild status is:

```text
full_canonical_history_closed_days
```

and whose file is fresh for that run, an absent closed date within the relevant history means no currently reachable commit is assigned to that date.

However, **absence without current status/freshness is not sufficient**: a failed activity collection could leave an older file in place.

Consumer logic therefore needs:

```text
activity rows
+ repository-status
+ last_observed_at
```

before interpreting absence as zero current canonical activity.

## Current-day exclusion and cross-family totals

`repository.csv.commits` is current GraphQL `history.totalCount` observed at run time.

`activity.csv` excludes commits whose `committedDate` is after the closed-day cutoff.

Therefore:

```text
sum(activity.csv.commits)
may be less than
repository.csv.commits
```

without any inconsistency when current-day commits exist.

At the current cutoff this is visible in several active `mandat-*` repositories. For example:

- `mandat-analytics`: latest repository total = 437, closed-day activity sum through 2026-09-29 = 382;
- `mandat-communication`: 141 vs 86;
- `mandat-forecast`: 415 vs 338.

The difference is compatible with commits whose `committedDate` is on the current UTC day 2026-09-30 and therefore intentionally excluded from `activity.csv`.

This is a material Current HOW distinction, not a defect.

## Current empirical state across all 28 activity files

At the Product baseline:

- all 28 repositories have an `activity.csv`;
- each current status reports `activity_status=full_canonical_history_closed_days`;
- across all inspected current activity rows, `commits_with_unknown_changed_files=0`;
- activity history lengths vary naturally with repository history, from one populated UTC day to more than one hundred;
- the oldest current reachable example in the corpus extends to 2021.

“No UNKNOWN changed-file counts currently observed” does not remove the field's semantics; future GraphQL responses can still exercise it.

## Default-branch identity is not stored

The collector resolves the current default branch but does not persist its name/ref as an observation dimension.

Consequences:

- the file always describes the current canonical reachable history as defined at observation time;
- later readers cannot reconstruct from `activity.csv` alone which branch name supplied that history;
- a default-branch switch can materially change history projection while remaining within the current Product contract.

The repository metadata timestamps and `last_observed_at` preserve temporal provenance but not ref identity.

## Backfill relationship

Backfill uses the same full-rebuild activity mechanism.

Therefore historical activity can be reconstructed as far back as the **currently reachable canonical history** allows, regardless of when Observatory itself began.

It cannot recover:

- commits no longer reachable from the current default branch;
- historical branch topology;
- historical default-branch choices;
- historical per-commit changed paths/details that were never stored.

CS-09 owns the complete backfill/recovery implications.

## Failure semantics

Activity reconstruction has a per-repository try/catch.

If it fails:

- `activity_status` becomes an explicit error status;
- metadata collection may retry head/total resolution separately;
- other repository families can still be collected;
- the prior `activity.csv` is not explicitly deleted.

Thus a consumer must use status/freshness to distinguish a current successful reconstruction from a stale retained prior file.

No such activity error is present in the current observed status corpus.

## Accepted/documented vs implemented vs observed

### Accepted/documented

`SCHEMA.md` says activity follows the current default ref/current reachable graph and old dates can change after merge/rebase/history rewrite.

### Implemented

The collector performs exactly that full paginated reconstruction every run.

### Observed

All current activity collections are successful; no changed-file UNKNOWN currently appears. Current-day exclusion is directly visible when compared with live snapshot total counts.

## Negative findings

- No append-only activity ledger exists.
- No all-branch activity is collected.
- No author/person productivity measure is stored.
- No commit-level identity survives in the generated corpus.
- No daily zero rows are materialized.
- No historical activity is frozen merely because it is old.

## UNKNOWN / limits

- Exact past canonical topology cannot be reconstructed from aggregate files.
- A real observed rebase/force-push changing historical rows was not captured as a controlled example in this Study.
- GitHub GraphQL's internal `changedFilesIfAvailable` availability rules are external; current corpus happens to have zero UNKNOWN occurrences.
- Commit `committedDate` can differ from author date; Observatory intentionally uses the former.

## Current HOW contribution

```text
current default-ref reachable graph
→ page complete commit history
→ group by UTC committedDate
→ exclude current-day commits
→ preserve changed-file availability
→ rewrite whole activity projection
→ stamp reconstruction freshness
```

The resulting historical series is **revisable canonical-history evidence**, not immutable “what Observatory saw on that past day”.

## Residue and routes

- API/retry/orchestration cost of full rebuild → CS-07 / CS-11.
- Backfill ceiling and rerun semantics → CS-09.
- Stale-file/status interpretation → CS-10.

## Reopen / invalidation triggers

Reopen if:

- activity source changes from current default-ref history;
- per-commit identity or branch dimension is added;
- aggregation/date field changes;
- current-day commits become included;
- append-only history replaces full rebuild;
- a real history rewrite exposes a materially different behavior;
- GraphQL changed-file availability semantics materially change.
