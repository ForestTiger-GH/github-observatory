# Current Corpus Research — Epoch 001

This directory contains bounded current-state studies of GitHub Observatory performed under the current-state research cycle commissioned on 2026-09-30.

## Reliance boundary

- Research here is **evidence and Work Result**, not current Product truth.
- Root `AGENTS.md`, `README.md`, `SCHEMA.md`, collector/workflow implementation, and generated observations retain their existing ownership.
- A Study Result contributes evidence-bound Current HOW material. It does not authorize Product mutation, Target design, or admission into maintained Current HOW.
- The stable Product baseline for the initial cycle is `github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`. Research-only commits made by this cycle do not change that Product baseline.
- Current MADARAII baseline: `MADARAII@37d4115d715554625da3123a186f44218fb1f8bc`.

## Cold entry

1. Read repository root `AGENTS.md`.
2. Read `_mw/AGENTS.md` and the active Epoch README.
3. Read `../AGENDA.md`.
4. Read the Result(s) relevant to the study being resumed.
5. Revalidate Product and MADARAII baselines before continuing.

## Current results

| Result | Work kind | Status | Purpose |
| --- | --- | --- | --- |
| [00 — Current-State Coverage Discovery](./00_Current_State_Coverage_Discovery_2026-09-30.md) | MADARAII-05 | COMPLETE | Bounds the current mechanism surface and qualifies bounded studies. |
| [01 — Product Identity, Boundaries and Owner Topology](./01_Product_Identity_Boundaries_and_Owner_Topology_2026-09-30.md) | MADARAII-06 | COMPLETE | Establishes current Product/Work boundaries, owner routes and reliance distinctions. |
| [02 — Repository Discovery, Identity and Registry Lifecycle](./02_Repository_Discovery_Identity_and_Registry_Lifecycle_2026-09-30.md) | MADARAII-06 | COMPLETE | Reconstructs automatic owner-repository discovery, stable identity, presence and rename lifecycle. |
| [03 — Current Temporal Semantics, Attribution and Freshness](./03_Current_Temporal_Semantics_Attribution_and_Freshness_2026-09-30.md) | MADARAII-06 | COMPLETE | Establishes current closed-day attribution, event-date, observation-time and rolling-snapshot semantics. |
| [04 — Repository Snapshots, File Counts and Languages](./04_Repository_Snapshots_File_Counts_and_Languages_2026-09-30.md) | MADARAII-06 | COMPLETE | Reconstructs repository metadata, exact/UNKNOWN file counts, language partitions and backfill limits. |
| [05 — Canonical Activity Reconstruction and Historical Mutability](./05_Canonical_Activity_Reconstruction_and_Historical_Mutability_2026-09-30.md) | MADARAII-06 | COMPLETE | Reconstructs default-ref activity projection, sparse days, changed-file UNKNOWN and historical revisability. |

## Status vocabulary

Agenda study states are: `OPEN`, `IN_PROGRESS`, `DONE`, `BLOCKED`, `SUPERSEDED`, `NOT_MATERIAL`, `ROUTED`.

## Update discipline

For each completed bounded study:

1. establish the standalone Study Result here;
2. update this README as the current-corpus navigation surface;
3. update `../AGENDA.md` with status, exact Result locator, residue and reopen triggers.

If a study becomes stale before completion, preserve the stale baseline and re-enter from current owners rather than silently rewriting history.
