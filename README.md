# github-observatory

`github-observatory` is a private, compact observability repository for repositories owned by `ForestTiger-GH`.

It preserves high-level GitHub-reported observations without copying repository contents. Public and private repositories are discovered automatically on every run, so new repositories enter the observatory without a manually maintained list.

## Core contract

- **Metadata, not content.** Do not persist commit messages, authors, file names, diffs, patches, file contents, issue/PR bodies, workflow logs, or artifacts.
- **Repository-level view.** Branch/ref names are not stored as an observation dimension. GitHub's current default ref is resolved only internally; activity represents the canonical commit history reachable from it.
- **Closed UTC days only.** The scheduled collector runs at **01:00 UTC**. `data_date_utc` is the latest fully closed UTC calendar day, normally yesterday.
- **No current-day daily rows.** Commit activity and daily Traffic rows from the unfinished UTC day are excluded.
- **No analytical layer.** Moving averages, rates, scores, rankings, growth, and other derived analytics do not belong in the collection layer.
- **Unknown is not zero.** A missing GitHub value is never silently replaced by zero.

## Time model

If the collector runs on `2026-09-24` at 01:00 UTC, its normal `data_date_utc` is `2026-09-23`.

Repository/language values are delayed snapshots observed at the exact `observed_at` timestamp and attributed to that just-closed day. GitHub does not expose exact historical end-of-day snapshots for repository size, stars, forks, subscribers, or language bytes, so backfill does not fabricate them.

Daily views/clones and commit activity are stored only for dates strictly before the current UTC date.

## Canonical activity and merges

Observatory does **not** sum branch activity.

On each run, `activity.csv` is rebuilt from the current canonical Git history reachable from GitHub's current default ref. The ref name is not persisted.

If an older commit becomes canonical through a later merge, it remains counted under its own Git `committedDate`; the merge commit is counted on its own date. A later merge, rebase, or history rewrite can therefore revise older activity rows. This is intentional: `activity.csv` is the current canonical history grouped by commit date, not an immutable log of every temporary branch.

## Stored data

For each repository the collector can store:

- repository identity, visibility, archived/fork status, timestamps, GitHub size, total canonical commits, stars, forks, subscribers;
- GitHub/Linguist language bytes;
- canonical commits by UTC `committedDate`;
- aggregate `changedFilesIfAvailable` as `changed_file_occurrences`;
- Traffic views, unique visitors, clones, and unique cloners;
- for public repositories only, rolling top-referrer and popular-path snapshots.

`changed_file_occurrences` is not unique file count. No file paths are requested merely to deduplicate it.

## Layout

```text
.github/workflows/
  collect.yml          # daily 01:00 UTC + manual
  backfill.yml         # manual historical initialization

scripts/
  github_api.py
  observatory.py
  collect.py
  backfill.py

ForestTiger-GH/
  repositories.csv
  _collection/
    runs.csv
    repository-status.csv
  <repository>/
    repository.csv
    activity.csv
    languages.csv
    traffic/
      views.csv
      clones.csv
      referrers.csv     # public only
      paths.csv         # public only
```

Repository directories are generated automatically. Stable GitHub repository IDs are used to preserve continuity through renames. If a repository disappears from the token's view, historical data remains and the registry marks it absent from the latest scan.

## Authentication

Create a fine-grained token for `ForestTiger-GH` with **All repositories** and read-only repository permissions:

- **Metadata: Read**
- **Contents: Read**
- **Administration: Read**

Store it as the Actions secret:

```text
OBSERVATORY_TOKEN
```

The read token observes source repositories. The workflow's short-lived `GITHUB_TOKEN` only writes generated Observatory data back to this repository.

## First run: backfill

Run **Actions → Backfill GitHub Observatory → Run workflow** once after adding `OBSERVATORY_TOKEN`.

Backfill:

1. discovers all current public and private repositories owned by `ForestTiger-GH`;
2. reconstructs canonical commit activity for all fully closed UTC days before today;
3. captures all closed daily views/clones rows still available in GitHub's Traffic window;
4. does **not** fabricate historical repository snapshots, language snapshots, or rolling referrer/path snapshots from current unfinished-day state.

The first normal 01:00 UTC collection creates the first repository/language snapshot and rolling public referrer/path snapshot for the just-closed day.

## Routine collection

Every day at 01:00 UTC the collector rediscovers the repository universe, rebuilds compact canonical activity through the latest closed day, refreshes closed views/clones rows, writes one delayed repository/language snapshot for `data_date_utc`, writes public rolling referrer/path snapshots, and commits all changes in one Git commit.

Current-day partial rows are never persisted.

See [SCHEMA.md](SCHEMA.md) for exact field semantics.
