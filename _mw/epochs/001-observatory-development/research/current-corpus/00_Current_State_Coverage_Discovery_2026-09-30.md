# Current-State Coverage Discovery — GitHub Observatory

**Work kind:** `CURRENT_STATE_COVERAGE_DISCOVERY` (MADARAII-05)  
**Status:** COMPLETE for the declared discovery frame  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**MADARAII baseline:** `ForestTiger-GH/MADARAII@37d4115d715554625da3123a186f44218fb1f8bc`  
**Cutoff:** current repository state and generated observations available at the Product baseline; latest generated `data_date_utc=2026-09-29`, observed 2026-09-30.

## Purpose and consumer

Purpose: discover the material current-state mechanisms that must be reconstructed so a cold future actor can understand how GitHub Observatory actually works now, where current evidence is authoritative, where accepted documentation and realization disagree, and what remains UNKNOWN.

Primary consumers:

- this Development Epoch's bounded current-state studies;
- a later research-only fan-in of Current HOW contributions if justified;
- future development planning that needs an evidence-bound current baseline.

This Result is a discovery projection. It is not Current HOW, Product truth, Target design, or authorization to change the collector.

## Discovery frame

The Engineering Object is GitHub Observatory as currently realized by:

- repository operating contracts and data semantics;
- collector and API client implementation;
- scheduled/manual workflows;
- generated registry, observations, collection status and run records;
- repository-profile routing;
- externally observable GitHub Actions run metadata needed to understand actual operation.

Research and Work artifacts are evidence/history only and do not replace those Product owners.

### Materiality rule

A concern is material when misunderstanding it can change interpretation of stored observations, the meaning of missing/zero/UNKNOWN, recovery or reliability expectations, privacy/access assumptions, current operational behavior, scalability, or a future change decision.

### Discovery methods

Complementary probes were used across:

- owner/document routes;
- repository tree and file topology;
- collector control flow;
- GitHub API interaction;
- generated registry/status/run evidence;
- workflow definitions;
- actual Actions run metadata;
- existing Epoch research Results as non-authoritative supplementary evidence.

### Detector limits

This pass can support claims about the inspected repository baseline and the externally visible Actions metadata queried for it. It does **not** prove absence of hidden GitHub platform behavior, token/account configuration, transient runner state, deleted/unreachable Git history, unavailable Traffic history, or facts GitHub APIs do not expose. “Not found” is not “absent” beyond those boundaries.

## Inspected surfaces

- root `AGENTS.md`, `README.md`, `SCHEMA.md`;
- `_mw/AGENTS.md`, active Epoch README and research routing;
- `profiles/README.md`;
- `scripts/collect.py`, `scripts/backfill.py`, `scripts/observatory.py`, `scripts/github_api.py`;
- `.github/workflows/collect.yml`, `.github/workflows/backfill.yml`;
- generated repository tree, `ForestTiger-GH/repositories.csv`, `_collection/runs.csv`, `_collection/repository-status.csv`, representative per-repository observation files;
- current GitHub Actions run list;
- current MADARAII FOUNDATION, MADARAII-05/06/15 and matching examples.

## Explicitly uninspected or only sampled in discovery

- every row of every generated CSV;
- every historical commit and workflow job log;
- secret/token scopes and account-side configuration;
- GitHub-internal scheduler implementation;
- inaccessible historical Traffic outside the API window;
- deleted/unreachable commit history;
- all existing Research Results in full;
- performance under repository universes substantially larger than the current one.

These boundaries are assigned to bounded studies or retained as limitations.

## Coverage map

| Current concern | Discovery evidence | Initial disposition | Bounded study |
| --- | --- | --- | --- |
| Product identity, purpose, owner boundaries and repository topology | README, AGENTS, SCHEMA, tree, workspace passport | material; documented but needs facet reconciliation | CS-01 |
| Automatic repository discovery and registry lifecycle | collector + repositories.csv | material current mechanism | CS-02 |
| Temporal model and date attribution | SCHEMA + collector + generated records | material; accepted current semantics differ from prior Research proposal | CS-03 |
| Repository snapshot, exact file count and language snapshots | collector + SCHEMA + generated files | material current mechanism | CS-04 |
| Canonical activity reconstruction | GraphQL queries + rewrite logic + activity.csv | material; history is revisable | CS-05 |
| Daily Traffic and rolling referrer/path snapshots | collector + SCHEMA + visibility policy | material; API-window and availability semantics | CS-06 |
| Collector orchestration, API client, error and partial-success behavior | observatory.py + github_api.py | material cross-cutting mechanism | CS-07 |
| Scheduled collection, Actions execution, concurrency and persistence | workflows + Actions run metadata + runs.csv | material; observed schedule mismatch | CS-08 |
| Backfill, rerun and idempotent replacement semantics | backfill workflow + shared collector + upsert logic | material lifecycle | CS-09 |
| Status/run evidence, missing/zero/UNKNOWN and corpus consistency | SCHEMA + status/runs + generated corpus | material assurance/interpretation concern | CS-10 |
| Reliability, recovery, performance, API/rate-limit and scaling limits | workflows + API client + collection geometry | material; partly inferred, limited operational failures observed | CS-11 |
| Security/privacy/access boundary | AGENTS + SCHEMA + public Observatory exposure + visibility handling | material; intentional exposure must be distinguished from defect | CS-12 |
| Profiles/navigation, analytics boundary and documentation-vs-operation consistency | profiles + README/AGENTS + existing research | material consumer route and boundary | CS-13 |

## Cross-cutting current paths to reconstruct

### Normal scheduled collection

```text
GitHub schedule event
→ Actions runner / checkout
→ py_compile
→ collect.py
→ collect("collect")
→ authenticated repository discovery
→ registry update
→ per-repository activity
→ repository snapshot
→ language snapshot
→ Traffic
→ repository-status + run record
→ git add ForestTiger-GH
→ commit
→ push
→ next cold consumer reads generated evidence
```

### Backfill

```text
manual workflow_dispatch
→ backfill.py
→ collect("backfill")
→ current repository discovery
→ full current-reachable canonical history reconstruction
→ currently available closed-day Traffic
→ no fabricated historical snapshot families
→ status + run record
→ commit + push
```

### Consumer interpretation

```text
profiles/README
→ repositories.csv
→ repository-specific CSV family
→ SCHEMA semantics
→ _collection status/run evidence when availability or freshness matters
```

These are discovery paths only; each bounded study must verify the relevant edges.

## Early observations that require deep study

1. The accepted workflow declares `cron: 0 2 * * *`, while all eight current scheduled Actions runs were created/started between 06:50 and 07:56 UTC. They are `event=schedule`, not manual dispatch. The internal collector starts only seconds after the Actions run starts. The cause is currently **UNKNOWN**.
2. Current Product semantics deliberately attribute repository/language snapshots and collection status/run records to the latest fully closed UTC day, although they are observed later. A prior Research Result recommended a different T/T−1 model; that Research proposal is not current Product truth.
3. `activity.csv` is rebuilt from the full currently reachable default-branch commit graph on each run. Historical rows can therefore change after merge/rebase/history rewrite.
4. Per-repository failures are caught and recorded; the collector can still exit successfully and allow a partial observation commit. GitHub workflow success therefore does not by itself establish complete source-family success.
5. Traffic `403/404` availability states are represented as non-error status strings; they do not increment `repositories_with_errors`. The exact meaning of “succeeded” therefore needs explicit reconstruction.
6. The Observatory repository is public while the discovered universe intentionally includes private repository names, descriptions and high-level metrics. Private Traffic referrers/paths are suppressed. This is an explicit current boundary, not automatically a defect.
7. The collector reconstructs full canonical history on every daily run and obtains recursive trees for file counts, creating scaling cost that grows with repository count/history/tree size.

## Existing coverage and prior Research

Existing Research Results on temporal semantics, metrics, dynamic rendering and visualization are relevant evidence and historical development input. They are **not** accepted current Product semantics merely because they exist under `research/results/`. Bounded studies must test their claims against the current Product baseline.

## Saturation basis

Breadth discovery reached saturation for this Commission because independent probes from owner documentation, implementation, generated evidence and actual Actions operation all map into the thirteen bounded concerns above; another repository-wide pass is unlikely to change the immediate study geometry.

## Reopen / invalidation triggers

Reopen coverage discovery if any of the following materially changes:

- Product purpose or boundary in root owner documents;
- collector/workflow/API-client architecture;
- stored schema or generated-data family set;
- repository discovery policy;
- new operational surface such as a dashboard or separate analytics product becoming current Product;
- a bounded study discovers a distinct mechanism with independent consumer/lifecycle not represented above;
- current GitHub platform behavior exposes a materially new source or limitation.

