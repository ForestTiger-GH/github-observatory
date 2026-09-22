# github-observatory

`github-observatory` is a private, compact observability repository for the repositories owned by `ForestTiger-GH`.

Its purpose is to preserve a small set of GitHub-reported repository observations over time without copying repository contents. Public and private repositories are discovered automatically on every run. A newly created repository therefore enters the observatory without editing a repository list by hand.

## Design principles

- **Metadata, not content.** The collector does not persist commit messages, authors, file names, diffs, patches, file contents, issue bodies, pull-request bodies, workflow logs, or artifacts.
- **Compact observations.** Stored data consists of repository snapshots, language byte counts, commit counts, changed-file counts, and GitHub Traffic statistics where the API permits access.
- **No analytical layer.** The repository does not calculate moving averages, growth rates, ratios, scores, trends, or other derived analytics.
- **Unknown is not zero.** If GitHub cannot calculate `changedFilesIfAvailable`, that commit is counted in `commits_with_unknown_changed_files`; it is never silently treated as zero changed files.
- **Default branch scope.** Commit activity is the history reachable from each repository's current default branch.
- **Automatic repository discovery.** Each run calls the authenticated-user repository API with owner/all-visibility scope and filters to `ForestTiger-GH`.

## What is collected

For every repository visible to the read-only Observatory token:

- repository identity and visibility;
- archived/fork status;
- creation/update/push timestamps;
- GitHub repository size;
- current default branch and total reachable commit count;
- stars, forks, and subscribers;
- GitHub language classification in bytes;
- commits by UTC commit date;
- the sum of GitHub's per-commit `changedFilesIfAvailable` values, stored as `changed_file_occurrences`;
- Traffic views, unique visitors, clones, and unique cloners when GitHub makes Traffic available; top referrers and popular paths are collected only for public repositories.

The changed-file metric is deliberately **not** a count of unique file paths. If the same file is changed in ten commits, it can contribute ten occurrences. No file names are stored.

## Repository layout

```text
.github/workflows/
  collect.yml          # daily 06:00 Europe/Helsinki + manual run
  backfill.yml         # manual one-time/history rebuild

scripts/
  github_api.py        # minimal REST + GraphQL client
  observatory.py       # discovery, collection, storage
  collect.py           # regular collector entry point
  backfill.py          # historical backfill entry point

.observatory/
  state.json           # technical state; one last default-branch head OID per repo

ForestTiger-GH/
  repositories.csv     # current/past discovered repository registry
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
      referrers.csv     # public repositories only
      paths.csv         # public repositories only
```

`ForestTiger-GH/<repository>/` directories are generated automatically. If a repository is renamed, the collector moves the existing directory to the new repository name using the stable GitHub repository ID. If a repository later disappears from the token's view, its historical directory is retained and `present_on_last_scan` becomes `false` in the registry.

## Authentication

Create one **fine-grained personal access token** for `ForestTiger-GH` with repository access set to **All repositories**. Give it read-only repository permissions:

- **Metadata: Read**
- **Contents: Read**
- **Administration: Read**

Store the token in this repository as the Actions secret:

```text
OBSERVATORY_TOKEN
```

The token is used only to read the repositories being observed. The workflow's short-lived `GITHUB_TOKEN` has `contents: write` only for committing generated Observatory data back to `github-observatory`.

## First run

Run **Actions → Backfill GitHub Observatory → Run workflow** once after adding `OBSERVATORY_TOKEN`.

Backfill performs the same automatic repository discovery as the daily collector and then:

1. stores the current repository snapshot and language classification;
2. walks the complete history reachable from each current default branch, requesting only commit OID, commit timestamp, and `changedFilesIfAvailable`;
3. aggregates those transient commit records into daily `activity.csv` rows and does **not** persist per-commit records;
4. captures the Traffic window currently available from GitHub (views/clones are limited by GitHub to the recent window; older Traffic cannot be reconstructed retroactively).

After that, `collect.yml` runs daily at **06:00 Europe/Helsinki**, including daylight-saving changes automatically.

## Routine collection

The daily collector does not rescan every commit in every repository. It remembers the last observed default-branch head OID and walks only commits newly reachable from the current head until the previous head is found. If the previous head is no longer an ancestor (for example after a force push), the collector rebuilds that repository's compact activity history from the currently reachable default-branch history.

## Cost profile

The implementation uses only GitHub-hosted Actions, GitHub APIs, Python's standard library, and normal Git storage. It installs no third-party Python packages and stores no Actions artifacts or caches.

See [SCHEMA.md](SCHEMA.md) for exact field semantics.
