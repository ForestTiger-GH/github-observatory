# Data contract

All CSV files are UTF-8 with a header row. Empty means unknown/unavailable unless a field explicitly defines another meaning. Counts reported as zero are actual zero values returned or countable from the observed Git history; an unavailable value is not converted to zero.

## `ForestTiger-GH/repositories.csv`

Registry of repositories ever discovered by the collector.

- `repository_id`: stable numeric GitHub repository ID.
- `name`, `full_name`: latest observed repository names.
- `visibility`: GitHub visibility, normally `public` or `private`.
- `archived`: latest observed archived flag.
- `default_branch`: latest default branch name.
- `first_seen_at`: first Observatory discovery timestamp.
- `last_seen_at`: latest successful universe scan in which the repository was present.
- `present_on_last_scan`: whether the repository was present in the latest universe scan.

This registry is technical discovery state, not an analytical series.

## `<repo>/repository.csv`

One compact repository snapshot per UTC observation date. A manual rerun on the same UTC date replaces that date's row.

- `observation_date_utc`, `observed_at`: Observatory observation time.
- `repository_id`, `name`, `full_name`, `visibility`: GitHub identity fields.
- `archived`, `fork`: GitHub booleans.
- `created_at`, `updated_at`, `pushed_at`: GitHub timestamps.
- `size_kb`: GitHub repository `size` field as reported by the repository API.
- `default_branch`: current default branch.
- `default_branch_commits`: current GraphQL `CommitHistoryConnection.totalCount` reachable from the default branch.
- `stars`: GitHub `stargazers_count`.
- `forks`: GitHub `forks_count`.
- `subscribers`: GitHub `subscribers_count` (actual repository watchers/subscribers; deliberately not the historical REST `watchers_count` alias for stars).

## `<repo>/activity.csv`

Compact default-branch commit activity grouped by the UTC calendar date of Git `committedDate`.

- `activity_date_utc`: UTC date derived from GitHub's commit `committedDate`.
- `commits`: number of commits currently reachable from the default branch with that commit date.
- `changed_file_occurrences`: sum of GitHub GraphQL `changedFilesIfAvailable` for those commits when available.
- `commits_with_unknown_changed_files`: number of commits for which GitHub returned `null` for `changedFilesIfAvailable`.
- `last_observed_at`: latest collection that changed or rebuilt that date's row.

`changed_file_occurrences` is **not unique files per day**. The collector never requests or stores file paths merely to deduplicate them.

Per-commit OIDs are used transiently during traversal. Only one head OID per repository is retained in `.observatory/state.json` to support incremental collection; no per-commit dataset is stored.

## `<repo>/languages.csv`

One long-format language snapshot per UTC observation date.

- `observation_date_utc`, `observed_at`: observation time.
- `language`: GitHub/Linguist language name.
- `bytes`: number of bytes GitHub attributes to that language.

No percentages are stored. No row for a date can mean either an empty GitHub language result or a failed collection; use `_collection/repository-status.csv` to distinguish them.

## `<repo>/traffic/views.csv`

Daily GitHub Traffic view observations. GitHub aligns Traffic daily timestamps to UTC.

- `traffic_date_utc`
- `count`
- `uniques`
- `last_observed_at`

Rows are upserted by traffic date because GitHub exposes only a recent rolling window. Git history preserves any revisions made by later observations.

## `<repo>/traffic/clones.csv`

Same layout and semantics as `views.csv`, for repository clones and unique cloners.

## `<repo>/traffic/referrers.csv`

Daily snapshots of GitHub's top referrers for its current rolling Traffic window. This dataset is collected for **public repositories only** to avoid leaking navigation/referral details from private projects.

- `observation_date_utc`, `observed_at`
- `referrer`
- `count`, `uniques`

These rows are **not daily referrer counts**. They are observations of GitHub's rolling-window top-referrer table on that observation date.

## `<repo>/traffic/paths.csv`

Daily snapshots of GitHub's popular-path table for its current rolling Traffic window. This dataset is collected for **public repositories only** so private file/page names are never persisted in Observatory.

- `observation_date_utc`, `observed_at`
- `path`, `title`
- `count`, `uniques`

These rows are **not daily path counts**; they preserve the reported rolling-window table.

## `_collection/repository-status.csv`

Per-repository source availability and collection status for each UTC observation date.

Statuses such as `ok`, `unchanged`, `full_history`, `unavailable_http_403`, and `error_http_*` prevent missing data from being silently reinterpreted as zero.

## `_collection/runs.csv`

One row per UTC date and collection mode (`collect` or `backfill`) with start/end timestamps and repository success/error counts. These are operational provenance fields, not repository analytics.

## Scope limitations

- Activity covers commits reachable from the **current default branch**, not every branch in the repository.
- Backfill can reconstruct default-branch commit dates and changed-file counts from reachable Git history, but it cannot reconstruct historical repository-size snapshots or historical language classifications that GitHub does not expose.
- GitHub Traffic is only available for the recent window exposed by the Traffic API; Observatory cannot reconstruct Traffic from before the first successful collection.
- Traffic availability for private repositories depends on GitHub access/plan and API authorization. An unavailable Traffic endpoint is recorded as unavailable, never as zero traffic.
