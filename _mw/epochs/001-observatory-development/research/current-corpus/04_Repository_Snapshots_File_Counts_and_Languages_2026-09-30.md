# CS-04 — Repository Snapshots, File Counts and Language Snapshots

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Consumer:** repository-profile readers, future analytics and data-quality studies.

## Question

How are current repository snapshots, exact file counts and language snapshots constructed, replaced and bounded?

## Evidence boundary

Inspected:

- `get_canonical_head_and_total()`;
- `get_canonical_file_count()`;
- `collect_repository_snapshot()`;
- `collect_languages()`;
- normal/backfill orchestration around those functions;
- `SCHEMA.md`;
- latest `repository.csv` rows for all 28 currently discovered repositories;
- representative language snapshots and collection-status records.

No large-tree truncation or empty-repository case is currently observed in the latest corpus, so those branches are implementation-established but not empirically exercised here.

## Repository snapshot mechanism

For each repository in a normal `collect` run:

```text
GraphQL defaultBranchRef
→ current head OID
→ current reachable history.totalCount

REST repository detail
→ current metadata

Git tree(head OID, recursive=1)
→ current canonical blob count or bounded UNKNOWN

combine
→ one repository.csv row
→ upsert by data_date_utc
```

The snapshot includes current repository metadata plus file/commit state derived relative to the current default branch.

## Commit-count semantics in repository snapshots

`commits` is **not** “commits made during the day”.

It is the GraphQL:

```text
defaultBranchRef.target.history.totalCount
```

for the current default branch at observation time.

Therefore:

```text
repository.csv.commits
= current total reachable canonical commit count
```

while:

```text
activity.csv.commits
= daily event count by committedDate
```

These are different fact classes.

## Exact file-count semantics

The collector asks GitHub for the recursive Git tree of the current head OID and counts entries with:

```text
type == "blob"
```

It does not infer file count from repository size or directory listing.

Three explicit states exist:

| State | Stored `files` | `files_status` | Meaning |
| --- | --- | --- | --- |
| normal complete recursive tree | integer | `exact` | exact count of returned blob entries |
| repository has no default-branch head | `0` | `exact_empty_repository` | exact empty canonical repository |
| GitHub marks recursive tree response truncated | blank | `unknown_truncated` | exact count cannot be established |

This is a strong current implementation of:

```text
UNKNOWN ≠ 0
```

The collector refuses to persist a partial recursive-tree count as if complete.

## Current observed file-count state

At the Product baseline, all 28 latest per-repository snapshot rows have:

```text
files_status = exact
```

No latest row has `exact_empty_repository` or `unknown_truncated`.

Observed latest exact file counts range from 2 files for the smallest current repositories to 1,966 for AppDock; `tabularium` has 875 and `github-observatory` itself has 187 at the Product cutoff.

These values describe the current default-branch tree at their exact `observed_at`, under the delayed T−1 attribution described in CS-03.

## Snapshot metadata source

The repository row also includes current REST repository-detail fields:

- stable ID;
- name/full name;
- description;
- visibility;
- archived/fork flags;
- created/updated/pushed timestamps;
- GitHub `size`;
- stars, forks and subscribers.

These are direct GitHub observations, not derived analytic scores.

## Rerun / replacement behavior

`repository.csv` is upserted with key:

```text
(data_date_utc)
```

A second normal run for the same closed day replaces the row for that partition. It does not append a second immutable snapshot.

Thus exact attempt history is not present in `repository.csv`; `observed_at` describes the surviving row.

## Language snapshot mechanism

The collector calls:

```text
GET /repos/{OWNER}/{repo}/languages
```

and persists one row per returned language:

```text
data_date_utc
observed_at
language
bytes
```

Rows are sorted by language name.

For the current partition, `replace_partition()` removes any prior rows with the same `data_date_utc` before adding the new response.

Therefore a same-day rerun replaces the **whole language partition**.

## Empty language response

If GitHub returns an empty language map:

```json
{}
```

the collector writes no language rows for that partition while still reporting `languages_status=ok`.

Therefore:

```text
absence of a language row
alone
does not distinguish
valid empty language map from uncollected/unavailable
```

The interpretation requires collection status and repository presence.

This is a concrete case where file/row absence must not be read as source failure or zero without the status context.

## Backfill behavior

In `backfill` mode:

- repository snapshots are deliberately skipped;
- language snapshots are deliberately skipped;
- status values are `skipped_backfill_current_snapshot`.

The system does not fabricate historical repository or language state from current values.

This matches the accepted `SCHEMA.md` boundary.

## Failure isolation

Within a normal per-repository iteration:

- activity/head discovery runs first;
- metadata snapshot has its own try/catch;
- language collection has a separate try/catch.

If the first head query failed, metadata collection attempts to resolve head/total again before snapshotting.

Therefore metadata and language availability are tracked independently in `repository-status.csv`.

A metadata failure does not automatically prevent the language request; a language failure does not erase a successful repository snapshot.

## Facets

### Accepted/documented

Current schema describes repository/language records as delayed daily snapshots, exact file counts only when the recursive tree is complete, and explicit UNKNOWN on truncation.

### Implemented

The implementation follows those semantics directly, including exact empty/truncated distinction and partition replacement.

### Observed

All 28 latest current file-count rows are exact. No operational evidence currently exercises `unknown_truncated` or `exact_empty_repository`.

## Negative findings

- No approximate file count is persisted.
- No recursive-tree partial count is silently accepted after truncation.
- No historical repository/language snapshot backfill is attempted.
- No language percentages are stored.
- No second immutable row is retained for a same-day rerun.
- No branch/ref name is persisted as a snapshot dimension.

## UNKNOWN / limits

- The current corpus provides no large-tree truncation example.
- The current corpus provides no empty-repository example.
- GitHub Linguist's internal classification semantics are external to this Study; Observatory preserves returned byte counts.
- A repository changing default branch between observations changes the canonical tree/history target without storing the branch name. The snapshot remains provenance-bound to observation time but does not retain the branch locator.

## Current HOW contribution

```text
current default branch
→ head OID + reachable commit total
→ recursive tree completeness check
→ exact/empty/UNKNOWN file count
+
current REST repository metadata
→ delayed repository snapshot

current languages endpoint
→ replace whole language partition
```

The key assurance principle is that exactness is explicit: file counts become UNKNOWN rather than partial when the source response says the recursive tree is incomplete.

## Residue and routes

- Historical default-ref mutability → CS-05.
- Same-day run attempt retention → CS-09.
- Empty/missing/status interpretation across the complete corpus → CS-10.
- Scaling cost of recursive trees and language calls → CS-11.

## Reopen / invalidation triggers

Reopen if:

- file-count source or truncation semantics change;
- default-branch/head resolution changes;
- snapshot schema/key changes;
- language collection or partition behavior changes;
- backfill begins reconstructing snapshots;
- a real empty/truncated-tree case appears and materially changes understanding.
