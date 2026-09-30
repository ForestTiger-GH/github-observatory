# CS-08 — Scheduled Collection: Declared Cron vs Actual Actions Operation

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Operational evidence cutoff:** GitHub Actions runs through 2026-09-30.  
**Consumer:** operations, reliability and temporal-semantics consumers.

## Question

How does scheduled collection actually run now, and what can be established about the repeated difference between the declared 02:00 UTC cron and the much later observed executions?

## Evidence boundary

Inspected:

- `.github/workflows/collect.yml`;
- `.github/workflows/backfill.yml`;
- current GitHub Actions run metadata for every recorded Observatory workflow run;
- `ForestTiger-GH/_collection/runs.csv`;
- collector control flow from CS-07;
- current GitHub Actions documentation for `schedule`.

No GitHub-internal scheduler telemetry is available. Platform-causal attribution is therefore bounded.

## Declared scheduled workflow

Current collect trigger:

```yaml
on:
  schedule:
    - cron: "0 2 * * *"
  workflow_dispatch:
```

With no explicit timezone attached, this is a daily **02:00 UTC** schedule.

The job then:

```text
checkout (fetch-depth 1)
→ setup Python 3.13
→ py_compile scripts/*.py
→ python scripts/collect.py
→ git add ForestTiger-GH
→ if changed: commit
→ git push
```

Timeout: 30 minutes.

## Current concurrency boundary

Both normal collect and backfill use:

```yaml
concurrency:
  group: github-observatory-write
  cancel-in-progress: false
```

Therefore these two workflows are serialized against each other by GitHub Actions rather than intentionally running concurrently.

This does not serialize unrelated external/user pushes to the branch.

## Actual scheduled-run evidence

All eight normal collection runs currently visible in Actions are:

- `event=schedule`;
- completed successfully;
- created and marked started at essentially the same timestamp;
- started far later than 02:00 UTC.

| Run | Date | Declared cron | Actions created / started | Delay from 02:00 |
| ---: | --- | --- | --- | ---: |
| 1 | 2026-09-23 | 02:00 | 06:57:26Z | 297.4 min |
| 2 | 2026-09-24 | 02:00 | 06:55:43Z | 295.7 min |
| 3 | 2026-09-25 | 02:00 | 06:50:05Z | 290.1 min |
| 4 | 2026-09-26 | 02:00 | 06:50:05Z | 290.1 min |
| 5 | 2026-09-27 | 02:00 | 07:19:05Z | 319.1 min |
| 6 | 2026-09-28 | 02:00 | 07:56:18Z | 356.3 min |
| 7 | 2026-09-29 | 02:00 | 07:39:35Z | 339.6 min |
| 8 | 2026-09-30 | 02:00 | 07:41:24Z | 341.4 min |

Observed range:

```text
4h 50m 05s
to
5h 56m 18s
```

Mean observed delay is about **316.2 minutes (5h 16m)**.

This is persistent current operational behavior across all eight scheduled samples, not a one-off outlier.

## The delay occurs before collector execution

Compare the latest run:

```text
Actions run started:
2026-09-30T07:41:24Z

collector runs.csv started_at:
2026-09-30T07:41:31Z
```

Only ~7 seconds separate Actions run start and collector timestamp establishment.

The same pattern holds across the current run set.

Therefore the multi-hour discrepancy is **not created by the collector doing hours of work before writing `started_at`**.

Current evidence localizes it to:

```text
declared schedule
→ delayed Actions schedule-event/run creation
→ runner starts
→ collector starts seconds later
```

## It is not manual dispatch

Every normal run metadata record has:

```text
event = schedule
```

The one observed backfill run has:

```text
event = workflow_dispatch
```

Thus the late normal executions cannot be explained as the user manually launching the collector at 06:50–07:56 UTC.

## GitHub's documented platform behavior

Current GitHub documentation states that scheduled events **can be delayed during periods of high Actions load** and specifically notes the start of every hour as a high-load period. It recommends scheduling at a different minute to reduce delay risk.

Official references:

- https://docs.github.com/en/actions/how-tos/troubleshoot-workflows
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

The current Observatory schedule is exactly at minute `0`, one of the documented higher-load positions.

### Causal status

The platform documentation makes GitHub-side scheduling delay a **credible mechanism**.

However, Observatory has no GitHub-internal queue/scheduler evidence proving that high load caused these particular eight delays.

Therefore the current strongest defensible statement is:

```text
Observed:
schedule events are created ~4h50m–5h56m after declared cron.

Supported platform mechanism:
GitHub documents that schedule events may be delayed under high load,
especially at the start of an hour.

Exact cause for these runs:
UNKNOWN.
```

It would be overclaiming to promote “high load caused all eight” to fact.

## Schedule semantics on default branch

GitHub documents that scheduled workflows run on the default branch and use the latest default-branch commit.

The current observed scheduled run metadata confirms different `head_sha` values over time as the branch advances.

Thus normal execution is bound to whatever Product/workflow state is current on `main` when GitHub creates the scheduled run, not to a pre-reserved 02:00 commit.

## Relationship to closed-day data semantics

Even with the operational delay:

```text
latest_closed_utc_date(started)
= UTC(started).date() - 1
```

So a 07:41 UTC start on Sep 30 still produces:

```text
data_date_utc = Sep 29
```

The delay increases the time between day-close and observation, but does not change the current T−1 partition formula.

Therefore current Product time semantics remain internally consistent while actual freshness is materially later than the README/workflow schedule might lead a reader to expect.

## Collector duration vs schedule delay

Current collector execution durations are only a few minutes.

For the latest normal run:

```text
collector:
07:41:31 → 07:46:06
≈ 4m35s

Actions run:
07:41:24 → 07:46:12
≈ 4m48s
```

The dominant timing discrepancy is upstream schedule delay, not collector runtime.

## Commit/push boundary

After collector success the workflow stages **only**:

```text
ForestTiger-GH
```

and commits generated observations if there are changes.

The commit message uses current UTC wall date:

```text
Collect repository observations YYYY-MM-DD
```

which is normally one day later than `data_date_utc`.

Example:

```text
commit message date: 2026-09-30
data_date_utc:       2026-09-29
```

These encode different facts and are consistent with CS-03.

## Persistence conflict boundary

The workflow performs a plain:

```text
git push
```

after a shallow checkout and does not pull/rebase immediately before pushing.

The shared workflow concurrency group prevents collect/backfill from racing each other, but it does not prevent a separate user/agent push to `main` after checkout.

Therefore an external concurrent branch advance can cause push failure even if collection itself succeeded.

If that happens:

- runner-local generated data and `runs.csv` changes are not persisted to `main`;
- Actions run records the workflow failure;
- the in-repository run ledger does not contain that unpushed attempt.

No such push failure appears in the current eight scheduled runs.

## No-change path

If:

```text
git diff --cached --quiet
```

the workflow exits the commit step successfully with “No observable changes.”

Because `runs.csv`, status freshness and reconstructed activity timestamps normally change on a completed run, current normal runs ordinarily produce a commit. The no-change branch nonetheless exists as current workflow behavior.

## Public-repository inactivity rule

GitHub documents that scheduled workflows in public repositories can be disabled after 60 days with no repository activity.

The current Observatory is active and all current scheduled runs execute, so this is a future platform condition rather than a current failure.

## Facet reconciliation

### Accepted/documented

Repository docs and workflow declare daily collection at 02:00 UTC.

### Implemented

The workflow cron is indeed `0 2 * * *`; the collector itself has no extra sleep or 07:xx schedule.

### Operated

Every current scheduled run starts around 06:50–07:56 UTC.

This is a real **documented/implemented vs operated timing mismatch**.

The Product still records exact `observed_at`, so evidence can recover actual freshness.

## Negative findings

- Current late runs are not manual dispatches.
- No multi-hour collector startup work precedes `started_at`.
- No alternate 07:xx cron exists in the current workflow file.
- No current collect/backfill overlap is observed; shared concurrency forbids intentional overlap.
- No current scheduled run failed.
- No current evidence proves the platform-internal cause of delay.

## UNKNOWN / limits

- Exact GitHub scheduler/queue cause for the repeated delay is UNKNOWN.
- Whether the delay pattern persists after the current eight samples is not established.
- Queue telemetry prior to run creation is not exposed in the inspected Actions metadata.
- External push races are code/workflow-derived risk, not currently observed failure.

## Current HOW contribution

```text
declared 02:00 UTC cron
→ GitHub schedule service
→ observed run creation ~06:50–07:56 UTC
→ checkout latest default-branch commit
→ syntax gate
→ collector starts seconds later
→ ~3–5 min collection
→ generated-data commit
→ push
```

The correct current statement is:

> collection is **scheduled for 02:00 UTC but currently observed to execute roughly five hours later**; exact timestamps in the corpus remain authoritative for freshness.

## Residue and routes

- Backfill/manual execution and reruns → CS-09.
- Corpus/run health implications → CS-10.
- Scheduler/rate-limit/scaling/recovery risks → CS-11.

## Reopen / invalidation triggers

Reopen if:

- cron/timezone/workflow changes;
- scheduled run start-time pattern materially changes;
- GitHub publishes or exposes stronger causal scheduler evidence;
- a scheduled run is dropped/fails;
- concurrency or commit/push flow changes;
- Product docs redefine schedule vs freshness claims.
