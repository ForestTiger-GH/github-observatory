# github-observatory

A compact repository-level observatory for the GitHub repositories discovered under one owner account.

It preserves reusable, high-level observations over time without copying repository contents. Collection is automatic, branch names are not an observation dimension, and daily data is tied to fully closed UTC calendar days.

## Routes

- `profiles/` — start here when the goal is to inspect the repository landscape.
- `ForestTiger-GH/` — generated registry and per-repository observations.
- `SCHEMA.md` — exact field semantics, provenance boundaries, and known limitations.
- `scripts/` — collector implementation.
- `.github/workflows/` — scheduled collection and manual backfill.

## Collection model

The routine collector runs daily at **02:00 UTC** and records the latest fully closed UTC day. Activity is reconstructed from the current canonical Git history reachable from GitHub's default ref, but ref names are not persisted.

Stored observations include repository metadata and descriptions, canonical file and commit counts, language bytes, daily commit activity, changed-file occurrences, and available GitHub Traffic data.

Historical backfill is manual and only reconstructs observations that GitHub can support historically; it does not fabricate past snapshots.

## Boundary

Observatory stores repository-level evidence, not repository contents or analytical conclusions. It does not persist source files, commit messages, author identities, diffs, changed paths, or directory trees.

See [SCHEMA.md](SCHEMA.md) for the data contract.
