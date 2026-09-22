# AGENTS.md

## Purpose

This repository is a compact observatory for GitHub-reported metadata and activity of repositories owned by `ForestTiger-GH`.

## Non-negotiable constraints

1. Do not ingest repository contents into the observatory.
2. Do not persist commit messages, authors, emails, file names, directory trees, diffs, patches, issue/PR bodies, workflow logs, artifacts, secrets, or security findings.
3. Keep public and private repositories discoverable by name and high-level metrics only.
4. Store observations, not analytical conclusions. Do not add moving averages, rates, ratios, rankings, scores, trend labels, or other derived analytics to the collection layer.
5. Preserve `unknown != zero`. Do not replace unavailable GitHub values with zero.
6. Repository discovery must remain automatic. Do not introduce a manually maintained allow-list for normal operation.
7. The default collection schedule is **01:00 UTC daily**. The collection's `data_date_utc` is always the latest fully closed UTC calendar day, normally the previous date.
8. Never persist branch/ref names as an observation dimension. Resolve GitHub's current default ref internally and observe the canonical commit history reachable from it.
9. Exclude the current UTC day from daily activity and Traffic series. Historical backfill must likewise include only fully closed UTC days.
10. Keep the implementation cheap and dependency-light. Prefer GitHub APIs and Python standard library; do not add infrastructure without a concrete need.
11. Historical backfill must remain a manual workflow and must not persist per-commit records.
12. Update README.md and SCHEMA.md whenever stored field semantics change.

## Stored-data boundary

Allowed examples: repository ID/name/visibility, dates, repository size, stars/forks/subscribers, total canonical commits, daily canonical commit count, aggregate changed-file occurrences, language bytes, aggregate GitHub Traffic, collection status. Public repositories may additionally store GitHub top-referrer and popular-path tables. Private repositories must not persist referrers, paths, or page titles.

Disallowed examples: branch names as stored observations, source files, private documentation, commit text, identities of commit authors, changed paths, code statistics derived by cloning repositories, or reconstructed content-level history.
