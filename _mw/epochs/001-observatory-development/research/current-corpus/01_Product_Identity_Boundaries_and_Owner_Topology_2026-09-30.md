# CS-01 — Product Identity, Boundaries and Current Owner Topology

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Research-control baseline at study start:** Agenda established through `c2faa929c7c134beb803b7fa97cf8135bad5aa12`  
**Consumer:** all later current-state studies and any research-only fan-in.

## Question

What is GitHub Observatory **now**, what does it intentionally observe, and which current surfaces own purpose, stored-data semantics, realization, generated evidence, consumer routing, and Work history?

## Boundary and evidence accounting

Inspected current Product/Work surfaces:

- root `README.md`;
- root `AGENTS.md`;
- root `SCHEMA.md`;
- complete recursive repository tree at the Product baseline;
- `profiles/README.md`;
- `scripts/*.py`;
- `.github/workflows/*.yml`;
- `ForestTiger-GH/README.md` and generated observation topology;
- `_mw/AGENTS.md`, active Epoch README, research README and Results README.

The recursive Git tree was complete rather than truncated. At the Product baseline it contained 187 files. The physical repository therefore gives a bounded, inspectable current topology.

Not inspected here: claim-level semantics of every CSV family, every implementation branch, GitHub platform internals, or historical rationale. Those belong to later studies.

## Current mechanism model

### 1. Purpose

The current Product is a **compact repository-level evidence collector** for repositories discovered under one owner account.

Its declared current job is to preserve reusable high-level observations over time without copying repository contents. It explicitly is **not** an analytics Product.

This distinction is owned jointly by repository orientation/development contracts:

- `README.md` owns the public route and operating-model description;
- `AGENTS.md` owns development constraints;
- `SCHEMA.md` owns stored-field and time/provenance semantics.

No Research Result under `_mw/` silently changes those owners.

### 2. Engineering-object boundary

The current Product consists of four different semantic surfaces that are physically co-located but not interchangeable:

```text
CONTROL / SEMANTIC CONTRACT
  README.md
  AGENTS.md
  SCHEMA.md

REALIZATION
  scripts/
  .github/workflows/

GENERATED OBSERVATION CORPUS
  ForestTiger-GH/

CONSUMER ROUTING
  profiles/
```

The Work plane is separate:

```text
_mw/
  workspace passport
  Development Epoch
  Research
  Research Results
```

Physical presence in one repository does not transfer semantic ownership between these surfaces.

### 3. Owner topology

| Fact / concern class | Current owner / route | What it does not own |
| --- | --- | --- |
| repository orientation and high-level operating model | `README.md` | exact CSV-field semantics |
| development invariants and prohibited persistence | `AGENTS.md` | generated observations |
| stored-data semantics, provenance, missing/zero rules, backfill limits | `SCHEMA.md` | collector implementation |
| collector realization | `scripts/` | normative meaning of fields beyond its accepted contract |
| scheduled/manual execution realization | `.github/workflows/` | semantic meaning of observations |
| generated current/historical observation records | `ForestTiger-GH/` | definitions of what fields mean |
| repository inspection read path | `profiles/README.md` | duplicate metric truth |
| Work architecture and development state | `_mw/` | Product truth unless a later authorized owner transition occurs |

This is a strong current distinction: **generated evidence is not the schema owner, code is not the documentation owner, and Research is not Product truth**.

### 4. Product topology is deliberately small

Outside the generated corpus and Work plane, the Product realization is compact:

- four root files including `.gitignore`;
- four Python modules under `scripts/`;
- two workflow definitions;
- one profile front door.

There is no separate database, service, dashboard, analytics engine, issue/PR ingestion subsystem, or branch-level observation store in the current Product baseline.

This is a statement about the complete repository tree at this baseline, not a claim that such mechanisms can never exist externally or later.

### 5. The generated corpus is part of Product operation, not Product semantics ownership

`ForestTiger-GH/` is workflow-managed. It contains:

- the discovered repository registry;
- collection health/run records;
- one directory per discovered repository;
- per-repository observation CSVs.

The corpus is mutable operational evidence. It changes through scheduled/manual collector runs. Its records support claims about observed repository state/activity, but their meaning comes from `SCHEMA.md` plus exact collection implementation/provenance.

### 6. Repository-content boundary

The current Product intentionally does **not** persist:

- source files or repository contents;
- commit messages;
- author identities/emails;
- diffs/patches;
- changed paths or directory trees;
- issue/PR bodies;
- workflow logs/artifacts;
- secrets or security findings.

It does transiently traverse some Git structure, for example to count blob entries, but only persists permitted high-level observations.

### 7. Visibility boundary

The discovered universe includes repositories regardless of visibility. Names, descriptions, visibility and other permitted high-level observations for private repositories are intentionally represented in the public Observatory corpus.

Private repositories do **not** get popular-path/referrer detail persisted. This is a deliberate current privacy boundary, not an accidental omission.

Whether this exposure remains desirable is a Target/Decision question and is out of scope for this Study.

## Representative current read path

A cold consumer inspecting repositories is expected to follow:

```text
root AGENTS / README
→ profiles/README
→ ForestTiger-GH/repositories.csv
→ ForestTiger-GH/<repository>/
→ relevant observation CSV
→ SCHEMA.md for exact meaning
→ _collection status/run evidence when freshness or availability matters
```

The route avoids requiring collector-code reading for ordinary observation use.

## Current facets and mismatches

### Accepted/documented facet

The documentation presents a compact evidence collector with automatic repository discovery, closed-day UTC semantics, strict provenance/missing-value rules, no content copying and no stored branch dimension.

### Implemented facet

The implementation matches this broad shape: GitHub API discovery, high-level metadata, current default-ref history aggregation, language bytes, Traffic data, status/run evidence and CSV persistence.

Detailed semantic mismatches are deferred to their exact studies rather than smoothed here.

### Operated facet

The generated corpus demonstrates that the collector is actively running and evolving the observations. The current Actions/run timing differs from the declared schedule timing and is routed to CS-08.

### Research facet

Prior Research under `_mw/.../research/results/` contains proposals for changed temporal semantics, expanded metrics and presentation. Those are development inputs, not current Product state.

## Negative findings

Within the complete current repository tree:

- no separate current analytics Product exists;
- no current dashboard/site implementation exists;
- no alternative schema owner was found;
- no second generated repository registry was found;
- no file-backed human inbox/outbox is enabled by the workspace passport.

These negative findings are bounded to repository realization at the exact baseline.

## UNKNOWN / limitations

- GitHub platform internals and account-side configuration are outside this Study.
- Historical reasons for individual Product choices are not reconstructed.
- External consumers may exist that are not represented in this repository; their reliance is UNKNOWN.
- Whether current private-repository metadata exposure is acceptable to all stakeholders is a governance question, not established here.

## Contribution to later Current HOW

This Study establishes the object/owner boundary for later studies:

```text
meaning / semantics owners
≠ realization
≠ generated observations
≠ routing projection
≠ Work / Research history
```

Later studies must preserve these distinctions. A contradiction between Research and Product docs is not a Product contradiction until an authorized owner changes.

## Residue and routes

- Detailed repository-discovery/registry lifecycle → CS-02.
- Temporal semantics → CS-03.
- Operational schedule mismatch → CS-08.
- Privacy/access implications → CS-12.
- Consumer routing and docs-vs-operation reconciliation → CS-13.

## Reopen / invalidation triggers

Reopen this Study if:

- repository purpose or analytics boundary changes;
- root owner documents change materially;
- a new current Product surface (dashboard, database, separate analytics layer, content ingestion, branch-level store) is admitted;
- workspace/Product boundary changes;
- repository visibility changes in a way that alters current exposure;
- generated evidence is moved to another owner or persistence topology.

