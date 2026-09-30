# CS-13 — Consumer Routes, Documentation Boundary and Current-State Reconciliation

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Consumer:** cold repository inspectors, future development actors and research-only Current HOW fan-in.

## Question

How should a cold consumer traverse the current Observatory, where does the Product's analytical boundary stop, and where do accepted documentation, implementation, generated evidence, observed operation and prior Research currently agree or disagree?

## Evidence boundary

Inspected:

- root `README.md`, `AGENTS.md`, `SCHEMA.md`;
- `profiles/README.md`;
- active Development Epoch and research routing;
- current bounded Studies CS-01 through CS-12;
- prior Epoch Research Results on temporal semantics, metrics, rendering and visualization;
- current implementation/generated/Actions evidence already reconstructed by those Studies.

This Study reconciles existing evidence. It does not alter Product docs or accept any prior Research proposal.

## Canonical cold-consumer route

For a user asking about repositories rather than collector implementation, the current owner-defined route is:

```text
AGENTS.md / README.md
→ profiles/README.md
→ ForestTiger-GH/repositories.csv
→ ForestTiger-GH/<repository>/
→ relevant CSV family
→ SCHEMA.md for exact meaning
→ _collection status/run evidence when freshness/availability matters
```

This route is coherent with current file ownership.

A consumer should **not** begin with `scripts/` unless the question is about realization or an ambiguity cannot be resolved from owner/schema evidence.

## Current Product boundary: evidence collector, not analytics product

The strongest current repository-level boundary is repeated in root owners:

```text
Observatory stores repository-level evidence
not repository contents
not analytical conclusions
```

`AGENTS.md` explicitly forbids adding rankings, scores, trends, moving averages or similar analytics to the collection layer.

Therefore the current Product ends at:

- source-faithful high-level observations;
- canonical daily aggregates that are part of collection semantics;
- provenance, status and missing/UNKNOWN representation.

It does **not** currently own:

- portfolio ranking;
- growth/trend metrics;
- rolling analytical windows;
- productivity scores;
- dashboards/Pages;
- DORA-like derived metrics;
- work-type inference.

Prior Research explores many such extensions, but they remain Research/Target candidates.

## Documentation layers and authority

A cold actor must distinguish:

### Product orientation

`README.md`:

- what Observatory is;
- where to start;
- current collection model;
- high-level boundary.

### Development constraints

`AGENTS.md`:

- current non-negotiable collector constraints;
- what may not be persisted;
- evidence-vs-analytics boundary;
- update discipline.

### Data semantics

`SCHEMA.md`:

- exact date/provenance meaning;
- field semantics;
- missing/UNKNOWN;
- branch/default-ref semantics;
- backfill limits;
- Traffic privacy boundary.

### Consumer navigation

`profiles/README.md`:

- how to locate repository evidence;
- which family answers which class of question;
- instruction to return to `SCHEMA.md` for exact meaning.

### Generated evidence

`ForestTiger-GH/`:

- observations, not definitions.

### Research / Work history

`_mw/`:

- bounded findings, proposals, development inputs and Work state;
- not Product truth unless separately admitted through current owner/authority.

This owner graph is internally coherent.

## Reconciliation matrix

| Concern | Accepted docs | Implementation | Generated / observed operation | Prior Research | Current conclusion |
| --- | --- | --- | --- | --- | --- |
| Repository discovery | automatic owner-account universe | authenticated `/user/repos`, stable ID registry | 28 current repos discovered automatically | compatible | aligned |
| Product scope | compact evidence collector, not analytics | only source observations/aggregates persisted | generated corpus is evidence-only | prior Research proposes derived analytics/dashboard layers | Research is future input, not current Product |
| Daily partition | latest fully closed UTC day | `UTC date - 1` | latest normal run on Sep 30 writes Sep 29 | temporal Research proposes snapshots at T | current Product is T−1; Research differs |
| Observation freshness | exact `observed_at` | timestamp recorded at collector start/source calls | current runs observed ~07:xx UTC | compatible principle | aligned, but actual schedule is late |
| Schedule | “runs at 02:00 UTC” | cron `0 2 * * *` | all 8 schedule events created ~06:50–07:56 UTC | not controlling | configured schedule and actual execution differ |
| Activity | current default-ref reachable history, revisable | full GraphQL history rebuild | all current activity statuses successful | metrics Research builds on same baseline | aligned |
| File count | exact or UNKNOWN on truncated tree | recursive tree + explicit status | all 28 current counts exact | compatible | aligned |
| Traffic daily | recent source window, closed-day retention | refresh-and-retain | persisted history extends beyond Observatory start; AppDock includes Aug 31 observed Sep 22 | compatible at high level | source-window exact bound remains uncertain |
| Traffic detail | rolling snapshots; private detail not persisted | public-only referrer/path persistence | 12 public have detail, 16 private do not | visualization Research assumes same boundary | aligned |
| Private repository visibility | high-level private observations intentionally included | full discovery + selected high-level persistence | names/descriptions/metrics publicly visible | visualization Research says preserve approved boundary | aligned |
| Backfill | only supportable history, no fabricated snapshots | activity + current Traffic window; skip snapshots/detail | one successful backfill | compatible | aligned |
| Missing vs zero | explicit invariant | statuses and UNKNOWN fields | several successful Traffic collections still omit some dates | Research repeatedly preserves invariant | aligned |
| Dashboard/Pages | not current Product | absent | absent | detailed target proposals exist | Research only |
| Expanded metrics (PR/issues/Actions/releases/etc.) | not current schema | absent | absent | detailed candidates exist | Research only |

## Material current disagreement 1: declared schedule vs operated schedule

Root docs say routine collection runs at **02:00 UTC**.

Workflow configuration agrees.

Observed Actions operation does not: all eight current scheduled events were created roughly five hours later.

Therefore the phrase “runs at 02:00 UTC” has two possible readings:

1. **configured schedule** — true;
2. **actual observed execution time** — false for every current scheduled sample.

A cold consumer relying on freshness should use `observed_at` / `runs.csv`, not infer actual query time from cron configuration.

This is the clearest current Product documentation-vs-operation mismatch.

## Material current disagreement 2: current Product vs temporal Research proposal

Prior temporal and metrics Research proposes:

```text
snapshots / current state → T
daily flows              → T−1
rolling snapshots        → T
```

Current accepted Product instead uses one closed-day `data_date_utc=T−1` partition for normal snapshots, status/run and rolling snapshots, while retaining exact observation timestamps.

This is **not an internal Product inconsistency**.

It is:

```text
current Product decision/implementation
≠
unaccepted Research recommendation
```

Cold actors must not read newer-looking Research prose as if it had silently changed `SCHEMA.md`.

## Material current disagreement 3: documented GitHub Traffic window vs preserved source evidence

Current GitHub documentation describes a recent 14-day Traffic surface.

Preserved Observatory evidence includes at least one AppDock view row dated 2026-08-31 with `last_observed_at=2026-09-22T20:28:31Z`, exceeding that exact bound.

Current Product docs only say “recent window”, so the internal schema does not overstate 14 days.

The unresolved contradiction is between:

- current external source documentation;
- a preserved historical source response.

Exact reason remains UNKNOWN.

Thus consumer documentation should treat Traffic horizon as **source-bounded and empirically evidenced**, not assume a permanent exact day count.

## Route-oriented documentation is intentionally non-duplicative

`profiles/README.md` does not duplicate every schema caveat.

For example:

- it lists `referrers.csv` / `paths.csv` “when collected”;
- `SCHEMA.md` owns the public-only rule.

This is not a contradiction; it is deliberate routing.

Likewise, repository descriptions and generated counts should not be manually copied into README because generated evidence is the current owner for those values.

## Important consumer qualification: a file may be present but stale

Because per-family failures can be caught while older files remain:

```text
file exists
≠ current collection succeeded
```

A cold consumer making freshness/completeness claims should consult latest `repository-status.csv`.

The current latest run is clean, but the valid read path must preserve this qualification for future failures.

## Important consumer qualification: missing file/row semantics are typed

A cold reader must not use one universal rule.

Examples:

- private `referrers.csv` absent → intentional privacy policy;
- missing language partition + status ok → can mean empty map;
- missing activity day + fresh successful rebuild → zero currently reachable commits;
- missing Traffic day + Traffic status ok → still not necessarily zero;
- blank file count + `unknown_truncated` → UNKNOWN, not zero.

Therefore `SCHEMA.md` and status evidence are part of the data, not optional explanatory prose.

## Current analytics boundary and prior Research

Existing Research Results explore:

- richer daily metrics;
- derived analytical layers;
- dashboard semantic models;
- README SVG rendering;
- GitHub Pages;
- dynamic/interactive visualization.

Those documents often contain strong recommendations and proposed target structures.

Their correct current status is:

```text
Research Result / development input
not current collector/schema
not current dashboard
not current public analytical product
```

Some proposals explicitly depend on a temporal model that differs from current Product semantics.

Therefore a future development actor must rebind each proposal to the current baseline before implementation.

## Current consumer path for common questions

### “What repositories exist?”

```text
profiles/README
→ repositories.csv
```

### “What is repository X for?”

Use current registry/repository description only as GitHub's stored repository description. Do not infer internal design/content.

### “How active is repository X?”

```text
activity.csv
+ current activity status
+ SCHEMA activity semantics
```

Do not equate commit count with productivity or quality.

### “How many files does it have?”

Use latest `repository.csv.files` **with `files_status`**.

### “What languages?”

Use latest relevant `languages.csv` partition; bytes are GitHub/Linguist output, not work-type activity.

### “How many visitors?”

Use `traffic/views.csv`, but treat `uniques` as GitHub's source-defined daily field. Do not sum daily uniques into a longer-period unique visitor count unless a separate method justifies it.

### “Where does traffic come from?”

Public repositories only:

```text
referrers.csv / paths.csv
```

as overlapping rolling top-table snapshots, not daily flow.

### “Did collection succeed?”

```text
_collection/runs.csv
+ repository-status.csv
```

and remember run-level `repositories_succeeded` means “no `error_*` family status”, not universal availability.

## Negative findings

- No current owner document says Research Results automatically change Product.
- No current analytics/dashboard implementation exists in the Product baseline.
- No second consumer routing layer competes with `profiles/`.
- No current documentation instructs consumers to infer repository contents.
- No current Product documentation converts missing to zero.
- No current schema claims exact historical midnight snapshots.
- No hidden current T/T−1 implementation matching the prior Research proposal exists.

## UNKNOWN / limits

- External consumers may ignore the prescribed routes; their behavior is unknown.
- The precise reason for schedule delay is unknown.
- The precise reason preserved AppDock Traffic exceeds current source documentation is unknown.
- Future Product decisions may adopt parts of prior Research, but none are inferred here.
- Whether high-level private-repository public exposure should be changed is a policy question outside current-state reconstruction.

## Current HOW contribution

A safe cold-reader algorithm is:

```text
1. identify whether the question is about evidence or implementation
2. enter through profiles for evidence
3. resolve repository via registry
4. select the evidence family
5. read exact semantics in SCHEMA
6. bind semantic date + observation freshness
7. check status when availability/completeness matters
8. preserve missing / unavailable / UNKNOWN distinctions
9. derive analysis outside the collection layer
10. treat _mw Research as proposals/history unless explicitly admitted
```

## Research-cycle conclusion for bounded studies

With CS-13 complete, the qualified bounded current-state surface from Coverage Discovery has been reconstructed.

The studies now provide enough complementary evidence for a **research-only Current HOW fan-in**:

- owner/boundary model;
- discovery/identity;
- temporal semantics;
- repository/language snapshots;
- activity;
- Traffic;
- orchestration;
- scheduled operation;
- backfill/rerun;
- corpus integrity;
- reliability/scaling;
- security/privacy;
- consumer routing/reconciliation.

The fan-in can therefore proceed without pretending that its synthesis becomes Product truth or maintained Knowledge.

## Reopen / invalidation triggers

Reopen if:

- root owner/schema/profile routes change;
- a dashboard/analytics Product becomes current;
- prior Research is accepted into Product;
- schedule wording or actual operation changes;
- Traffic source behavior is resolved materially;
- consumer routing changes;
- new observation families materially alter the inspection path.
