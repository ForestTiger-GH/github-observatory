# GitHub Observatory Current-State Research Agenda

**Development Epoch:** `001-observatory-development`  
**Agenda purpose:** durable control surface for the current-state research cycle commissioned on 2026-09-30.  
**Product baseline at cycle formation:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**MADARAII baseline at cycle formation:** `ForestTiger-GH/MADARAII@37d4115d715554625da3123a186f44218fb1f8bc`  
**Coverage Result:** [current-corpus/00_Current_State_Coverage_Discovery_2026-09-30.md](./current-corpus/00_Current_State_Coverage_Discovery_2026-09-30.md)

This Agenda records qualified Work candidates and their durable state. An entry is not a Product Decision and does not authorize Product mutation beyond this Commission.

## Shared research contract

Primary consumer: a cold future actor needing an evidence-bound model of how GitHub Observatory actually works now, plus later development Work that needs a trustworthy current baseline.

Global completion standard for each bounded study:

- exact current question and baseline are bound;
- accepted/documented, implemented, generated/observed and externally operated facets are separated when they differ;
- representative paths are traceable to evidence;
- negative findings, contradictions and UNKNOWNs survive;
- downstream reliance and limitations are explicit;
- no Target design or repair is performed.

Shared Product cutoff for the first wave: repository Product surfaces and generated observations at `d0119ec7...`, including `data_date_utc=2026-09-29` observed on 2026-09-30 where present.

## Study state

| ID | Exact current question | Subject / boundary | Consumer | Baseline / cutoff | Primary work kind | Expected evidence | Dependencies | Status | Result locator | Findings / Questions / residue | Reopen / invalidation triggers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CS-01 | What is GitHub Observatory now, what does it intentionally observe, and which surfaces own purpose, semantics, realization and Work history? | Repository identity, Product/Work boundary, root and workspace owner routes | all later studies | Product baseline + workspace/MADARAII baselines | `CURRENT_STATE_BOUNDED_STUDY` | README, AGENTS, SCHEMA, tree, epoch/workspace routes | coverage discovery | OPEN | — | distinguish Product truth from Research proposals and generated evidence | owner-route, purpose, visibility or repository topology changes |
| CS-02 | How are repositories discovered, identified, renamed, retained and represented in the registry? | `list_owned_repositories`, `update_registry`, `repositories.csv` | corpus/data consumers | Product baseline; latest registry observation | `CURRENT_STATE_BOUNDED_STUDY` | code, registry rows, current repo metadata | CS-01 helpful, not blocking | OPEN | — | owner-account boundary, stable ID, disappearance and rename behavior | discovery/API/registry schema changes |
| CS-03 | What temporal semantics do current records actually implement, including attribution, freshness, closed-day rules and rolling snapshots? | all date-bearing families | data consumers / future analytics | Product baseline + latest generated rows | `CURRENT_STATE_BOUNDED_STUDY` | SCHEMA, code, CSV examples, prior temporal Research as non-authoritative input | CS-01 | OPEN | — | explicitly reconcile current Product with prior T/T−1 proposal | date/schema/collection timing changes |
| CS-04 | How are repository snapshots, exact file counts and language snapshots constructed, replaced and bounded? | repository + language families | profile/current-state consumers | Product baseline | `CURRENT_STATE_BOUNDED_STUDY` | REST/GraphQL calls, tree truncation logic, CSVs, status | CS-02, CS-03 | OPEN | — | empty repository, truncated tree, snapshot replacement and provenance | API/schema/file-count mechanism changes |
| CS-05 | What exactly does `activity.csv` mean and how can historical rows change? | current default-ref reachable history → daily activity | activity consumers / future analytics | Product baseline | `CURRENT_STATE_BOUNDED_STUDY` | GraphQL queries, aggregation/rewrite code, representative activity rows | CS-03 | OPEN | — | sparse days, changed-file UNKNOWN, merge/rebase/history-rewrite semantics | default-ref/activity query/schema changes |
| CS-06 | What do views, clones, referrers and popular paths mean now, and how do availability, visibility and rolling-window limits affect reliance? | GitHub Traffic families | traffic/profile consumers | Product baseline + current Traffic window | `CURRENT_STATE_BOUNDED_STUDY` | code, SCHEMA, public/private files, status rows, GitHub API behavior | CS-03 | OPEN | — | daily vs rolling; 403/404; private detail suppression; stale prior snapshots | Traffic API/schema/policy changes |
| CS-07 | How does one collector execution orchestrate GitHub requests, partial failures, retries, writes and terminal status? | `observatory.py` + `github_api.py` execution contour | reliability/data-integrity consumers | Product baseline | `CURRENT_STATE_BOUNDED_STUDY` | implementation, status/run evidence, workflow step contract | CS-02..CS-06 useful | OPEN | — | distinguish API retry from per-repo continuation and process exit semantics | collector/API-client changes |
| CS-08 | How does scheduled collection actually run, and why does observed execution differ from the declared 02:00 UTC schedule? | collect workflow from schedule event through push | operations/reliability consumer | workflow at Product baseline; Actions runs through 2026-09-30 | `CURRENT_STATE_BOUNDED_STUDY` | workflow YAML, Actions run metadata, runs.csv, commit history | CS-07 | OPEN | — | observed scheduled starts 06:50–07:56 UTC; cause currently UNKNOWN | workflow schedule/platform behavior/run metadata changes |
| CS-09 | How do manual backfill, same-day reruns and replacement semantics behave, and what history cannot be reconstructed? | backfill workflow + shared collector persistence | recovery/history consumer | Product baseline; observed backfill run 2026-09-22 | `CURRENT_STATE_BOUNDED_STUDY` | code, workflow, SCHEMA, run/status/CSV keys | CS-03, CS-07 | OPEN | — | exact idempotence ceiling; run-attempt replacement; unsupported historical snapshots | backfill/upsert/schema changes |
| CS-10 | How are collection health, missing, zero, unavailable and UNKNOWN represented across the current corpus, and is the generated corpus internally consistent? | `_collection` + all generated CSV families | assurance/data consumers | generated corpus at Product baseline | `CURRENT_STATE_BOUNDED_STUDY` | complete structural census, status/run rows, representative/all-row integrity checks | CS-02..CS-09 useful | OPEN | — | availability states vs `repositories_succeeded`; absent files/partitions; duplicate/key checks | generated corpus/schema/status semantics change |
| CS-11 | What are current reliability, recovery, performance and scaling limits of the collector, including rate-limit and large-history/tree behavior? | collector + workflow operational envelope | future development/reliability consumer | Product baseline + observed run durations | `CURRENT_STATE_BOUNDED_STUDY` | request geometry, pagination, timeouts/retries, Actions durations, limits | CS-07, CS-08, CS-09 | OPEN | — | distinguish observed limits from code-derived risks; little failure evidence currently | repository universe/history/tree size, API or workflow limits change |
| CS-12 | What security, privacy and access boundary is actually implemented for public and private repositories? | token/API access → public Observatory persistence | security/privacy consumer | Product baseline + latest registry/files | `CURRENT_STATE_BOUNDED_STUDY` | AGENTS/SCHEMA, visibility handling, generated public surface, workflow permissions | CS-02, CS-06, CS-07 | OPEN | — | private names/descriptions/high-level metrics intentionally visible; private navigation details suppressed | visibility policy/token/workflow/repository exposure changes |
| CS-13 | How do profiles and documentation route consumers, where does analysis stop, and where do docs, implementation and observed operation currently disagree? | consumer read path and analytics boundary | cold external/current-state consumer | Product baseline + existing Research route | `CURRENT_STATE_BOUNDED_STUDY` | README/AGENTS/SCHEMA/profiles, implementation, observed operation, existing research | CS-01 and later studies | OPEN | — | consolidate contradictions without promoting Research to Product truth | owner docs/profile route/current mechanisms change |

## Fan-in posture

No MADARAII-15 Work is currently marked executable. It becomes justified only after enough `CS-*` contributions are `DONE` to form a coherent consumer-fit current mechanism model and an embedded Current HOW assembly contract can be bound without claiming Product or maintained-Knowledge admission. Any such fan-in remains a Research Result under this Commission.

## Current priority / next eligible Work

Initial execution order follows semantic dependency rather than file order:

```text
CS-01
→ CS-02 + CS-03
→ CS-04 + CS-05 + CS-06
→ CS-07
→ CS-08 + CS-09
→ CS-10 + CS-11 + CS-12
→ CS-13
→ optional research-only fan-in if justified
```

Independent studies may be reordered when evidence availability makes that more efficient, provided their exact dependencies remain satisfied.
