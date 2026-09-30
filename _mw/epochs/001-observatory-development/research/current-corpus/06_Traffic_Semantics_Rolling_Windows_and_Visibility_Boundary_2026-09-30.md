# CS-06 — Traffic Semantics, Rolling Windows and Visibility Boundary

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**External platform reference checked:** GitHub REST API version 2026-03-10 documentation current on 2026-09-30.  
**Consumer:** Traffic/profile consumers, privacy/reliability studies and future analytics.

## Question

What do views, clones, referrers and popular paths mean now, and how do API-window, availability, visibility and persistence behavior affect valid reliance?

## Evidence boundary

Inspected:

- `collect_traffic()`;
- `SCHEMA.md`;
- complete Product-baseline tree for presence/absence of Traffic families;
- latest collection-status patterns;
- representative daily and rolling CSVs;
- official GitHub Traffic API documentation for the source window and access contract.

## External source contract

GitHub's current official REST documentation states:

- page views can be returned as daily/weekly breakdowns for the **last 14 days**;
- clones can be returned as daily/weekly breakdowns for the **last 14 days**;
- top referral paths are the top 10 popular contents over the **last 14 days**;
- top referral sources are the top 10 referrers over the **last 14 days**;
- Traffic data is UTC-aligned;
- access requires repository Traffic permission / suitable repository access.

Official reference:

- https://docs.github.com/en/rest/metrics/traffic?apiVersion=2026-03-10
- https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository

The Observatory is therefore preserving a bounded upstream surface, not querying an unlimited historical source.

## Daily aggregate path

For every repository, normal and backfill modes first call:

```text
GET /traffic/views?per=day
GET /traffic/clones?per=day
```

Returned daily items are converted to:

```text
traffic_date_utc = timestamp[:10]
count
uniques
last_observed_at
```

Only dates at or before the current closed-day cutoff are admitted.

### Persistence behavior

`upsert_closed_daily_rows()`:

1. retains already stored rows whose date is <= current cutoff;
2. overlays newly returned rows for the same date;
3. rejects current/future-day rows;
4. rewrites the sorted historical file.

Consequently the Observatory can accumulate a Traffic series longer than GitHub's live 14-day API window.

Old persisted rows survive after GitHub stops returning them.

This is the mechanism that turns a rolling upstream source into a longer locally retained daily evidence series.

## Refresh semantics

While a daily date remains inside GitHub's returned window, a later collection can overwrite its `count` and `uniques`.

Therefore Traffic daily rows are not immutable immediately after first observation.

`last_observed_at` records the last source observation that supplied the surviving value.

Once a date falls outside the source window, Observatory can retain it but cannot independently refresh it from that endpoint.

## Zero semantics in daily Traffic

GitHub currently returns explicit zero-valued daily entries in representative responses, and Observatory persists them.

Thus:

```text
daily row with count=0, uniques=0
≠ missing daily row
```

A missing row may instead reflect source-window history, unavailable collection, a repository not yet observed, or another bounded cause. CS-10 owns the corpus-level missing/zero matrix.

## Aggregate Traffic failure behavior

Views and clones are queried inside one try block.

If either request raises GitHub `403` or `404`:

```text
collect_traffic()
→ return unavailable_http_403 / unavailable_http_404
```

and the function returns before persisting the current response pair.

Other errors propagate to the outer per-repository handler and become `error_*`.

Implication:

```text
traffic_status=unavailable_http_403
is an explicit availability state,
not a numeric zero
```

It is also not currently classified as `error_*` for the run-level error counter; CS-07/CS-10 own that cross-layer meaning.

## Rolling detail path

Only in normal collect mode, and only after daily aggregate Traffic succeeds:

```text
if backfill:
    stop after daily aggregate

if repository is private:
    stop after daily aggregate

if repository is public:
    GET /traffic/popular/referrers
    GET /traffic/popular/paths
    replace current data_date partition
```

The two detail calls are also paired in one try block.

If either returns 403/404:

```text
traffic_status =
aggregate_ok_detail_unavailable_http_403
or
aggregate_ok_detail_unavailable_http_404
```

Daily aggregate Traffic remains persisted; the current rolling-detail partition is not updated.

## Visibility/privacy boundary

Current Product deliberately collects daily aggregate views/clones for both public and private repositories when authorized.

It persists rolling `referrers.csv` and `paths.csv` **only for public repositories**.

Complete tree inspection at the Product baseline confirms:

- all 12 public repositories have views, clones, referrers and paths files;
- all 16 private repositories have views and clones;
- none of the 16 private repositories has a persisted referrers or paths file.

This exactly matches the implemented privacy policy.

For a private repository with successful aggregate Traffic:

```text
traffic_status = ok_aggregate_only_private
```

This is not a failure.

## Rolling snapshots are not daily series

GitHub returns top-N summaries for the last 14 days, not one value per calendar day.

Observatory persists each query result as a partition labelled with current Product `data_date_utc=T−1` and exact `observed_at`.

Thus adjacent snapshots overlap.

For example:

```text
snapshot stored under Sep 28
and
snapshot stored under Sep 29
```

can both summarize substantially the same prior 14-day window.

They must not be summed or differenced as daily referrer/path traffic without an additional valid model.

## Top-N truncation

The source returns top 10 referrers / popular contents.

Absence from `referrers.csv` or `paths.csv` does not prove zero traffic for that source/path. It may simply fall below the source top-N cutoff.

Therefore:

```text
not present in rolling top table
≠ zero
≠ never occurred
```

This is a source limitation, not an Observatory data-loss defect.

## Same-day rolling replacement

`replace_partition()` removes the existing partition for current `data_date_utc` and inserts the latest returned top table.

A same-closed-day rerun therefore keeps only the latest rolling snapshot for that partition.

If the source returns an empty list successfully, the prior partition for that day is removed and no rows remain; current `traffic_status=ok` is needed to distinguish “empty successful top table” from unavailable collection.

## Backfill boundary

Backfill:

- refreshes/persists daily views/clones still available from GitHub;
- does not collect rolling referrers/paths;
- cannot reconstruct daily Traffic older than the upstream window unless Observatory had already persisted it previously;
- cannot reconstruct historical rolling top tables at all.

No historical rolling snapshots are fabricated.

## Current observed status pattern

At the latest Product-baseline run:

- public repositories have `traffic_status=ok`;
- private repositories have `traffic_status=ok_aggregate_only_private`;
- no latest repository has a Traffic error/unavailable status.

Thus failure semantics above are code/documented current mechanisms, not presently observed failures in the latest run.

## Important observed source-window contradiction

After this Study was first closed, corpus-wide inspection found a material counterexample to treating the documented 14-day window as an exact observed bound.

`AppDock/traffic/views.csv` contains:

```text
traffic_date_utc=2026-08-31
last_observed_at=2026-09-22T20:28:31Z
```

and continuous rows from that date forward. The `last_observed_at` equals the first observed backfill execution, so this early row was supplied/refreshed during that backfill rather than merely surviving with an older Observatory timestamp.

August 31 to September 22 exceeds the currently documented “last 14 days” surface.

Therefore the evidence must remain split:

```text
GitHub current documentation:
views/clones daily breakdown for last 14 days

Observed Observatory source response at 2026-09-22:
at least one repository yielded a longer dated series

Exact reason:
UNKNOWN
```

Possible explanations such as platform behavior changing over time, documentation lag, account-specific source behavior or another undocumented rule are not established by current evidence.

Accordingly, **14 days is the current documented source contract, not a safe empirical hard bound for every historical response already preserved by Observatory**.

## Facet reconciliation

### Accepted/documented

`SCHEMA.md` distinguishes daily Traffic from rolling snapshots and explicitly suppresses private navigation/referral detail.

### Implemented

The collector matches this split and preserves daily history across the upstream rolling window.

### Observed

The generated tree and latest statuses exactly exhibit the public/private family topology described above.

## Negative findings

- No private popular-path/referrer detail is persisted.
- No rolling snapshot backfill exists.
- No daily referrer/path semantics exist.
- No top-N absence is safe to interpret as zero.
- No full-clone content or visitor identity is stored.
- No current Traffic failure is present in the latest status set.

## UNKNOWN / limits

- GitHub's hidden aggregation/update mechanics beyond documented behavior are outside Observatory; preserved AppDock evidence materially exceeds the current documented 14-day window, and the reason is UNKNOWN.
- Older persisted daily Traffic cannot be independently re-queried after it leaves GitHub's window.
- The current corpus has not exercised the 403/404 branches in the latest runs, so recovery from those states is implementation-established rather than observed.
- Exact semantics of GitHub `uniques` are source-defined and not independently validated by Observatory.

## Current HOW contribution

```text
authorized Traffic access
→ daily views + clones (currently documented as a last-14-day upstream window; preserved evidence includes a longer historical response)
→ admit only closed UTC days
→ refresh while source still returns them
→ retain older daily history locally

normal collect + public repository
→ top-10 referrers + paths for rolling last-14-day window
→ replace current snapshot partition

private repository
→ aggregate only
→ no navigation/referral detail persisted
```

## Residue and routes

- Paired-call errors, retries and run-level success semantics → CS-07.
- Backfill/rerun evidence limits → CS-09.
- Missing/zero/unavailable status interpretation → CS-10.
- Privacy/access posture → CS-12.

## Reopen / invalidation triggers

Reopen if:

- GitHub changes the Traffic window, top-N, permission or timestamp semantics;
- collector changes detail visibility policy;
- rolling snapshots become daily or backfillable;
- daily retention/upsert rules change;
- `traffic_status` classification changes;
- a real Traffic availability failure yields materially new operational evidence.
