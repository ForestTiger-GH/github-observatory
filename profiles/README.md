# Repository profiles

Start here when the goal is to inspect the repositories observed by github-observatory.

This directory is a routing layer. It does not duplicate generated metrics.

## Repository universe

Open:

`../ForestTiger-GH/repositories.csv`

It is the current registry of discovered repositories and includes the latest repository name, GitHub description, visibility, archived state, and discovery provenance.

The observatory intentionally covers the discovered repository universe at a high level, including repositories that are not public.

## One repository

For a repository named `<repository>`, continue to:

`../ForestTiger-GH/<repository>/`

Use the available files as follows:

- `repository.csv` — delayed daily repository snapshots such as description, size, exact file count when available, canonical commits, stars, forks, and subscribers.
- `activity.csv` — canonical commit activity grouped by UTC commit date.
- `languages.csv` — GitHub/Linguist language-byte snapshots.
- `traffic/views.csv` — daily views.
- `traffic/clones.csv` — daily clones.
- `traffic/referrers.csv`, `traffic/paths.csv` — rolling Traffic surfaces when collected.

A file may legitimately be absent before its first supportable observation.

## Semantics

For exact meanings, source boundaries, missing-value rules, backfill limits, and merge/rebase behavior, read:

`../SCHEMA.md`

Do not infer source code, internal documentation, authors, paths, or other content-level facts from profile-level observations.
