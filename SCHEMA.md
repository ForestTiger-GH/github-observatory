# Data contract

All CSV files are UTF-8 with a header row. Empty means unknown/unavailable unless explicitly stated otherwise. Unknown is not converted to zero.

## Time convention

The Observatory uses UTC calendar days.

The scheduled collector runs at **01:00 UTC**. `data_date_utc` is the latest fully closed UTC day, normally the previous calendar date. `observed_at` is the exact UTC timestamp when GitHub was queried.

The one-hour delay is an operational buffer. Repository size, stars, forks, subscribers, total canonical commits, and language bytes are delayed snapshots observed after the day boundary and attributed to the just-closed `data_date_utc`. They are not claims that GitHub exposed an exact historical 00:00 UTC snapshot.

The current UTC day is excluded from `activity.csv`, `views.csv`, and `clones.csv`.

## Branch/ref boundary

Branch/ref names are not stored observation dimensions.

Internally, the collector resolves GitHub's current default ref and treats the commit graph reachable from it as the repository's current canonical history. The stored data does not expose the ref name.

A later merge or rebase can revise older activity dates if older commits newly become reachable. Such commits remain assigned to their own Git `committedDate`; they are not reassigned to the merge date.

## `ForestTiger-GH/repositories.csv`

Registry of repositories ever discovered:

- `repository_id`: stable GitHub repository ID.
- `name`, `full_name`: latest observed names.
- `visibility`, `archived`: latest GitHub metadata.
- `first_seen_at`, `last_seen_at`: Observatory discovery timestamps.
- `present_on_last_scan`: whether the repository was present in the latest universe scan.

No branch name is stored.

## `<repo>/repository.csv`

One delayed repository snapshot per `data_date_utc`. Rerunning the same closed day replaces that row.

Fields:

- `data_date_utc`, `observed_at`
- `repository_id`, `name`, `full_name`, `visibility`
- `archived`, `fork`
- `created_at`, `updated_at`, `pushed_at`
- `size_kb`: GitHub repository `size`
- `commits`: GitHub GraphQL `CommitHistoryConnection.totalCount` reachable from the internally resolved canonical/default ref at `observed_at`
- `stars`: `stargazers_count`
- `forks`: `forks_count`
- `subscribers`: `subscribers_count`

Backfill does not fabricate historical rows here.

## `<repo>/activity.csv`

Current canonical Git history grouped by UTC Git `committedDate`.

Fields:

- `activity_date_utc`
- `commits`
- `changed_file_occurrences`: sum of GitHub GraphQL `changedFilesIfAvailable` where available
- `commits_with_unknown_changed_files`: commits for which GitHub returned `null`
- `last_observed_at`

Rows from the current UTC day are excluded.

`changed_file_occurrences` is not a unique-file count. No per-commit dataset, commit message, author identity, file path, diff, or patch is persisted.

## `<repo>/languages.csv`

Long-format delayed snapshot:

- `data_date_utc`
- `observed_at`
- `language`
- `bytes`

No percentages are stored. Backfill does not fabricate historical language snapshots.

## `<repo>/traffic/views.csv`

Daily GitHub Traffic views:

- `traffic_date_utc`
- `count`
- `uniques`
- `last_observed_at`

Only fully closed UTC days are stored. Existing rows are refreshed while still present in GitHub's rolling Traffic window.

## `<repo>/traffic/clones.csv`

Same schema and closed-day rule as `views.csv`, for clones and unique cloners.

## `<repo>/traffic/referrers.csv`

Public repositories only. Snapshot of GitHub's current rolling top-referrer table:

- `data_date_utc`
- `observed_at`
- `referrer`
- `count`
- `uniques`

These are rolling-window snapshots, not daily referrer counts. Backfill does not fabricate historical snapshots from the current table.

## `<repo>/traffic/paths.csv`

Public repositories only. Snapshot of GitHub's current rolling popular-path table:

- `data_date_utc`
- `observed_at`
- `path`
- `title`
- `count`
- `uniques`

These are rolling-window snapshots, not daily path counts. Private paths/titles are never persisted.

## `_collection/repository-status.csv`

Per-repository collection/source status for each `data_date_utc`.

Backfill marks non-historical snapshot families as `skipped_backfill_current_snapshot`. Error/unavailable states are explicit and are never interpreted as zero.

## `_collection/runs.csv`

One row per `data_date_utc` and mode (`collect` or `backfill`) with exact start/end timestamps and repository success/error counts.

## Backfill boundary

Backfill reconstructs only historically supportable observations:

- canonical commit activity for all reachable commits whose `committedDate` is before the current UTC date;
- closed daily views/clones rows still available in GitHub's Traffic window.

Backfill does not reconstruct historical repository snapshots, language snapshots, rolling referrer/path snapshots, or commits no longer reachable from the current canonical history.

## Scope limitations

- `activity.csv` is a view of the current canonical reachable Git graph grouped by commit date, not an immutable log of every temporary branch.
- A later merge/rebase/history rewrite can revise older activity rows.
- GitHub Traffic history is limited to the recent window exposed by the Traffic API.
- Private Traffic availability depends on GitHub access/plan and token authorization; unavailable is recorded as unavailable, never zero.
