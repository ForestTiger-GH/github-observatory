# CS-03 — Current Temporal Semantics, Attribution and Freshness

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Observed cutoff:** latest normal collect started 2026-09-30T07:41:31Z and persisted `data_date_utc=2026-09-29`.  
**Consumer:** any reader or future analytics that compares observation families over time.

## Question

What temporal semantics do current records actually implement, including attribution, freshness, closed-day rules and rolling snapshots?

## Evidence boundary

Inspected:

- `SCHEMA.md`;
- date/time functions and persistence keys in `scripts/observatory.py`;
- workflow schedule contract;
- generated `repository.csv`, `languages.csv`, daily Traffic, rolling referrer snapshots and `_collection/runs.csv`;
- existing `GitHub_Observatory_Temporal_Semantics_2026-09-24.md` strictly as a non-authoritative Research proposal.

This Study describes current Product behavior. It does not adopt the prior proposal.

## Core current time model

The collector computes:

```python
started = utc_now()
observed_at = started in UTC
cutoff_date = UTC(started).date() - 1 day
data_date = cutoff_date
```

Thus a normal run on calendar day **T** assigns the common Product partition **T−1**.

Current accepted semantics can be written:

```text
observation occurs at T / observed_at
but ordinary stored partition is the latest fully closed UTC day T−1
```

This is deliberate in `SCHEMA.md`.

## Family-by-family semantics

| Family | Primary date field | Current meaning |
| --- | --- | --- |
| `repositories.csv` | no daily partition; exact `first_seen_at`, `last_seen_at` | discovery observations at actual observed timestamps |
| per-repo `repository.csv` | `data_date_utc=T−1` + `observed_at=T` | delayed current snapshot observed after the day boundary and attributed to the closed day |
| `languages.csv` | `data_date_utc=T−1` + `observed_at=T` | delayed language snapshot attributed to the closed day |
| `activity.csv` | `activity_date_utc` from commit `committedDate` | event-date daily aggregate for all currently reachable commits with date ≤ cutoff |
| `traffic/views.csv` / `clones.csv` | GitHub-returned `traffic_date_utc` | calendar-day Traffic facts ≤ cutoff; current UTC day excluded |
| `referrers.csv` / `paths.csv` | `data_date_utc=T−1` + `observed_at=T` | current rolling top-table snapshot, stored in the closed-day partition |
| `repository-status.csv` | `data_date_utc=T−1` + `observed_at=T` | source-family status of the run attributed to the closed day |
| `runs.csv` | `data_date_utc=T−1`, exact start/finish at T | collector execution that processed the closed-day partition |

The system therefore uses **one closed-day attribution convention across several semantically different families**, while retaining exact observation timestamps where required.

## Important distinction: attribution date is not snapshot instant

A row such as:

```text
data_date_utc = 2026-09-29
observed_at   = 2026-09-30T07:41:31Z
```

in `repository.csv` does **not** mean:

> this was the exact repository state at 2026-09-29T23:59:59Z.

It means:

> this current state was observed on 2026-09-30 after 2026-09-29 had fully closed and is attributed to that closed-day partition.

The current `SCHEMA.md` explicitly treats these as delayed daily snapshots. Any repository changes between midnight UTC and actual observation time can therefore be reflected in the row attributed to the previous day.

This is not hidden; `observed_at` preserves the exact collection timestamp.

## Representative current evidence

For `github-observatory`:

```text
repository.csv:
2026-09-29, observed_at=2026-09-30T07:41:31Z, files=187, commits=32

languages.csv:
2026-09-29, observed_at=2026-09-30T07:41:31Z, Python=25912 bytes

runs.csv:
data_date_utc=2026-09-29
started_at=2026-09-30T07:41:31Z
finished_at=2026-09-30T07:46:06Z
```

The exact observation/run timestamps are coherent across these families.

## Daily event families

### Activity

Commit events are assigned by the first ten characters of GitHub GraphQL `committedDate`:

```text
committedDate UTC calendar date
→ activity_date_utc
```

Only dates `<= cutoff_date` are written.

The current UTC day is excluded.

Because activity is rebuilt from the **current reachable default-ref history**, old event dates remain real commit dates, but the membership of the current history can change later. Temporal event date and historical stability are separate concerns; CS-05 owns the latter.

### Views and clones

GitHub supplies timestamped daily Traffic rows. The collector persists only rows whose `traffic_date_utc <= cutoff_date`.

Returned rows inside the still-available GitHub window can overwrite prior values for the same date. Older persisted rows survive after they leave the returned window.

`last_observed_at` therefore records when a particular daily value was last refreshed.

## Rolling Traffic snapshots

`referrers.csv` and `paths.csv` do **not** represent daily events.

They are a top-table snapshot of GitHub's current rolling Traffic surface at `observed_at`.

Current Product stores the snapshot under `data_date_utc=T−1`.

A later run produces a new partition even if the rolling window overlaps heavily with the previous one. Adjacent rows cannot be differenced as if they were independent daily counts.

## Rerun semantics within one closed-day partition

Several families use key-based upsert or partition replacement:

- `repository.csv`: one row keyed by `data_date_utc`;
- languages: the whole language partition for `data_date_utc` is replaced;
- rolling paths/referrers: the whole `data_date_utc` partition is replaced;
- run rows: one row per `(data_date_utc, mode)`;
- repository status: one row per `(data_date_utc, repository_id)`.

A same-day rerun therefore updates/replaces the current closed-day representation rather than appending a second immutable observation attempt.

Exact attempt-history implications are routed to CS-09.

## Actual schedule timing does not redefine the current date rule

The workflow declares 02:00 UTC. Actual current scheduled runs were created and started much later, around 06:50–07:56 UTC.

The collector's date rule is not based on “two hours after midnight”; it is simply:

```text
current UTC date - 1
```

Therefore the observed multi-hour delay still results in the same T−1 partition.

The reason for the schedule delay is not established here and remains CS-08.

## Current Product vs prior temporal Research proposal

The existing Research Result `GitHub_Observatory_Temporal_Semantics_2026-09-24.md` proposes:

```text
snapshots / observations → T
daily flows              → T−1
```

and suggests observation-day partitions for repository/languages/runs/status/referrers/paths.

That is **not the current Product state** at this baseline.

Current Product instead intentionally uses:

```text
shared closed-day attribution T−1
+ exact observed_at/start/finish timestamps
```

for ordinary snapshot/run/status partitions.

This is a clean example of:

```text
Research proposal
≠ accepted Product semantics
```

## Freshness model

Freshness is not represented by date field alone.

A consumer may need:

```text
semantic date
+ observed_at / last_observed_at
+ latest repository-status
+ source-family behavior
```

Examples:

- an old activity row can be freshly re-derived today from current reachable history;
- an old Traffic row can have a later `last_observed_at` while still in GitHub's window;
- a rolling snapshot's `data_date_utc` is an attribution partition while `observed_at` identifies the actual query time.

## Negative findings

- No local-timezone partition is used; the current model is UTC-based.
- No exact end-of-day snapshot capture exists.
- No current Product implementation of the prior T/T−1 proposal exists.
- No current-day activity/views/clones row is intentionally persisted by normal collection.
- No immutable per-attempt timestamp key exists for run/status snapshots.

## UNKNOWN / limits

- GitHub's internal Traffic aggregation and eventual-consistency behavior is outside this repository; the collector preserves returned values/provenance but cannot establish the platform's hidden aggregation time.
- The schedule delay cause is UNKNOWN here.
- Consequences of a scheduler delay crossing into a later UTC date have not been operationally observed in the current corpus.
- External consumers that ignore `observed_at` may misread attribution as exact state time; their behavior is UNKNOWN.

## Current HOW contribution

```text
UTC observation at T
→ compute closed-day partition T−1
→ collect current snapshots and eligible daily facts
→ preserve exact observation timestamps
→ exclude current-day event rows
→ refresh revisable/rolling source data while available
→ persist one current representation per closed-day key
```

The shared partition creates convenient daily alignment, but it must never erase the distinction between **event date**, **attribution date**, and **actual observation time**.

## Residue and routes

- Snapshot implementation → CS-04.
- Activity historical mutability → CS-05.
- Traffic window/rolling semantics → CS-06.
- Same-day rerun and backfill → CS-09.
- Cross-family completeness/freshness checks → CS-10.

## Reopen / invalidation triggers

Reopen if:

- `latest_closed_utc_date` or `data_date` logic changes;
- schema date fields are renamed or redefined;
- snapshots move to observation-day semantics;
- workflow cadence or time zone changes materially;
- Traffic source behavior changes;
- current-day facts begin to be persisted;
- a Decision adopts the prior temporal Research proposal or another temporal model.
