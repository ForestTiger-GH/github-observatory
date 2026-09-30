# GitHub Observatory — Current HOW Research Synthesis

**Work kind:** `CURRENT_HOW_ASSEMBLY_AND_RECONSTRUCTION` (MADARAII-15)  
**Status:** COMPLETE AS RESEARCH-ONLY CURRENT HOW CANDIDATE  
**Admission status:** NOT ADMITTED as Product truth or maintained Knowledge  
**Current Product baseline reconstructed:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Research synthesis baseline:** current-corpus studies established through repository state `70b69b5eb5337dd8114c1f12ff5755089d7773f8` before this synthesis write  
**MADARAII baseline:** `ForestTiger-GH/MADARAII@37d4115d715554625da3123a186f44218fb1f8bc`  
**Primary consumer:** a cold future actor who must understand how GitHub Observatory actually works now without re-reading the full research history.

This document is a **research Result**. It reconciles current-state evidence into one consumer-ready Current HOW candidate, but it does not replace `README.md`, `AGENTS.md`, `SCHEMA.md`, collector/workflow implementation, or generated evidence as their current semantic owners.

---

## 1. Assembly contract

### Purpose

Reconstruct the actual current GitHub Observatory mechanism at the declared Product baseline across:

- structure and ownership;
- repository discovery and identity;
- temporal semantics;
- snapshot families;
- canonical activity;
- Traffic;
- collector orchestration;
- scheduled operation;
- backfill and reruns;
- generated-corpus integrity;
- reliability/scaling;
- security/privacy;
- consumer routing and documentation.

### Materiality rule

A fact is material here when misunderstanding it can change:

- what a stored observation means;
- whether a value may be relied upon;
- whether missing/zero/UNKNOWN can be distinguished;
- how current or historical a fact is;
- whether collection succeeded;
- what a failure/recovery path does;
- what private information is public;
- how future Product change should bind the current baseline.

### Closure boundary

This synthesis claims bounded completeness only for the mechanism surface discovered and studied under the 2026-09-30 current-state cycle.

It does not claim:

- complete reconstruction of historical intent;
- proof of GitHub platform internals;
- full assurance under unobserved failures;
- Target design;
- Product acceptance of prior Research;
- correctness of every historical CSV cell by independent recomputation.

---

# 2. Contribution disposition

| Contribution | Disposition in this synthesis |
| --- | --- |
| 00 — Current-State Coverage Discovery | retained as scope/coverage controller; not treated as mechanism truth by itself |
| 01 — Product Identity, Boundaries and Owner Topology | admitted into owner, boundary and consumer model |
| 02 — Repository Discovery, Identity and Registry Lifecycle | admitted into identity/discovery/state model |
| 03 — Current Temporal Semantics, Attribution and Freshness | admitted into temporal/provenance model |
| 04 — Repository Snapshots, File Counts and Languages | admitted into snapshot/evidence model |
| 05 — Canonical Activity Reconstruction and Historical Mutability | admitted into activity/history model |
| 06 — Traffic Semantics, Rolling Windows and Visibility Boundary | admitted into Traffic/source-limit/privacy model |
| 07 — Collector Orchestration, Failure Isolation and Terminal Status | admitted into control/failure model |
| 08 — Scheduled Collection: Declared Cron vs Actual Actions Operation | admitted as distinct configured-vs-operated facet |
| 09 — Backfill, Rerun and Replacement Semantics | admitted into recovery/replacement model |
| 10 — Current Data Corpus, Missing/Zero and Integrity Posture | admitted into assurance/consumer-reliance model |
| 11 — Reliability, Recovery, API Economics and Scaling Envelope | admitted into operation/scaling model |
| 12 — Security, Privacy and Access Boundary | admitted into access/confidentiality model |
| 13 — Consumer Routes, Documentation and Current-State Reconciliation | admitted into reader route and facet-reconciliation model |

Existing older Epoch Research on temporal redesign, expanded metrics, dynamic rendering and visualization remains **Research / target-development input**. It is not admitted as current Product state where it differs from the baseline reconstructed here.

---

# 3. One-page Current HOW

GitHub Observatory is currently a **small public evidence collector** for repositories automatically discovered under one configured GitHub owner account.

Its core behavior is:

```text
authenticated GitHub owner-repository discovery
→ stable repository-ID registry
→ one per-repository collection pass
     → full current-reachable canonical activity reconstruction
     → current repository metadata + exact/UNKNOWN file count
     → current language-byte snapshot
     → daily GitHub Traffic
     → public-only rolling referrer/path detail
→ explicit per-family status
→ run summary
→ Git commit of ForestTiger-GH/
→ push to main
```

The routine workflow is **configured** for 02:00 UTC, but all eight observed scheduled executions at the reconstruction cutoff were created by GitHub around 06:50–07:56 UTC. Exact `observed_at` and run timestamps, not cron configuration, are the authoritative freshness evidence.

Normal collection attributes most snapshot/status/run families to the latest fully closed UTC day:

```text
data_date_utc = current UTC date - 1
```

while preserving the actual query time separately.

The collector is intentionally not transactional across the whole repository universe. Per-repository source-family errors are caught and recorded so other families/repositories may continue. A workflow can therefore succeed and commit partial current evidence when explicit error statuses exist.

The generated corpus is not a rectangular database where blank means zero. Missing, empty, unavailable, UNKNOWN and intentional policy omission have different semantics and often require `repository-status.csv`, visibility and freshness context.

---

# 4. Current owner and representation model

## 4.1 Semantic owners

```text
README.md
→ repository orientation / operating model / routes

AGENTS.md
→ development invariants and prohibited persistence

SCHEMA.md
→ stored-data semantics and provenance

scripts/
→ collector realization

.github/workflows/
→ execution realization

ForestTiger-GH/
→ generated evidence

profiles/
→ consumer navigation projection

_mw/
→ Work / Research history and development state
```

These are not interchangeable.

Key invariant:

```text
generated evidence
≠ schema owner
≠ implementation owner
≠ Research
```

## 4.2 Product boundary

The current Product stores high-level evidence, not repository contents or analytical conclusions.

It intentionally excludes:

- source files;
- commit messages;
- authors/emails;
- diffs/patches;
- changed paths/directory trees;
- issue/PR bodies;
- workflow logs/artifacts;
- secrets/security findings.

It also intentionally excludes collection-layer rankings, scores, trends and moving averages.

---

# 5. Repository identity and discovery model

## 5.1 Discovery

Each run enumerates repositories through authenticated GitHub `/user/repos` with:

- owner affiliation;
- all visibility states;
- pagination;
- a defensive owner-login check.

There is no normal-operation allow-list.

## 5.2 Identity

```text
repository_id
= stable Observatory registry identity

name/full_name
= mutable current locators/display labels
```

The current generated directory is name-based:

```text
ForestTiger-GH/<repo-name>/
```

so rename reconciliation matters.

## 5.3 Registry lifecycle

At each scan:

1. prior rows are provisionally marked `present_on_last_scan=false`;
2. returned repositories refresh current metadata;
3. existing IDs preserve `first_seen_at`;
4. `last_seen_at` is refreshed;
5. returned repositories become present;
6. missing repositories remain in historical registry state rather than being deleted.

Ordinary rename behavior attempts to move the prior per-repository directory when the old path exists and new path does not.

No rename collision is currently observed.

---

# 6. Temporal model

The current Product uses three distinct time concepts.

## 6.1 Observation time

`observed_at`, `last_observed_at`, run start/finish.

This is when GitHub was actually queried/reconstructed.

## 6.2 Attribution partition

For normal snapshot/status/run partitions:

```text
data_date_utc = latest fully closed UTC day
```

A Sep 30 07:41 observation can therefore live in a Sep 29 partition.

It is **not** an exact Sep 29 23:59 snapshot.

## 6.3 Event date

Activity uses commit `committedDate`; daily Traffic uses GitHub-returned Traffic dates.

Current UTC-day activity/Traffic rows are excluded.

## 6.4 Prior Research difference

Earlier Research proposed:

```text
snapshots = T
flows = T−1
rolling snapshots = T
```

That proposal is not the current Product baseline.

Current Product instead uses the closed-day partition for ordinary snapshot/status/run and rolling snapshot families while retaining exact observation timestamps.

---

# 7. Repository and language snapshot model

A normal repository snapshot combines:

```text
current REST repository metadata
+
current default-branch head
+
current reachable history.totalCount
+
recursive Git tree blob count
```

## 7.1 File-count state

Three states exist:

```text
exact
exact_empty_repository
unknown_truncated
```

A truncated recursive Git tree produces UNKNOWN rather than a partial numeric count.

At the baseline all 28 latest file counts are exact.

## 7.2 Commit total

`repository.csv.commits` is the **current total reachable default-branch commit count**, not commits made during the partition date.

## 7.3 Languages

GitHub language bytes are stored in a long-form per-date partition.

A same-day rerun replaces the whole language partition.

A successful empty language response can yield no language rows, so row absence is not self-interpreting.

## 7.4 Backfill

Repository and language snapshots are deliberately not fabricated historically during backfill.

---

# 8. Canonical activity model

Every normal run and backfill fully traverses the **current default-branch reachable commit history**.

For every eligible commit:

```text
committedDate → UTC activity date
commits += 1
changed_file_occurrences += changedFilesIfAvailable
or
commits_with_unknown_changed_files += 1
```

Then the entire `activity.csv` is rewritten.

## 8.1 Consequence: history is revisable

```text
rebase / merge / force push / history rewrite / default-branch change
→ current reachable graph changes
→ old activity rows may change
```

Therefore `activity.csv` is not an immutable event ledger.

## 8.2 Sparse dates

Only dates with currently reachable commits get rows.

An absent activity day may be interpreted as zero current-reachable commits only when current activity status/freshness shows that the rebuild succeeded.

## 8.3 Current-day difference

`repository.csv.commits` may exceed the sum of activity rows because repository total count is current at observation time while activity excludes current-day commit dates.

This is a temporal distinction, not an integrity defect.

---

# 9. Traffic model

## 9.1 Daily views/clones

The collector retrieves GitHub daily views/clones, filters to closed UTC dates and refreshes same-date rows while the source still returns them.

Old locally persisted daily rows survive after they leave the source window.

A present row with:

```text
count=0
uniques=0
```

is an explicit zero.

A missing daily row is not automatically zero.

## 9.2 Source-window uncertainty

Current GitHub documentation describes a recent 14-day Traffic surface.

However, preserved AppDock evidence includes a row dated 2026-08-31 with `last_observed_at=2026-09-22T20:28:31Z`, materially exceeding that exact documented interval.

Therefore:

```text
current documented source bound = 14 days
preserved observed historical response = longer in at least one case
exact explanation = UNKNOWN
```

The safe current model is “source-bounded recent Traffic whose exact historical response horizon has not been stable enough to treat the documented day count as a universal empirical constant.”

## 9.3 Rolling detail

For public repositories only, normal collection stores:

- top referrers;
- popular paths.

These are overlapping rolling top-table snapshots, not daily flows.

Absence from the top table does not prove zero.

Backfill does not reconstruct them.

## 9.4 Private repositories

Private repositories may have aggregate views/clones.

They do not have persisted referrer/path detail.

---

# 10. Collector control and failure model

Per repository:

```text
activity try/catch
metadata try/catch
languages try/catch
Traffic try/catch
→ status row
```

A family failure does not automatically stop later families or later repositories.

## 10.1 Status semantics

Errors are generally:

```text
error_http_<code>
error_<ExceptionClass>
```

Traffic also has non-`error_*` availability/policy states such as:

```text
unavailable_http_403
unavailable_http_404
aggregate_ok_detail_unavailable_http_403
aggregate_ok_detail_unavailable_http_404
ok_aggregate_only_private
ok_closed_days_only
ok
```

## 10.2 Run success counter

A repository counts as `repositories_succeeded` when none of its statuses begins with `error_`.

Therefore:

```text
repositories_succeeded
≠ all optional data was available
```

## 10.3 Process exit

After per-repository failures are recorded, the collector can still return process exit code 0.

Thus:

```text
workflow collector step success
≠ universal source-family success
```

Consumers must read status/run evidence.

## 10.4 Retry

The API client retries only 502/503/504 and network `URLError`, with bounded exponential waits.

There is no current rate-limit-aware `Retry-After` / reset handling.

---

# 11. Scheduled operation

## 11.1 Configured schedule

```text
cron = 0 2 * * *
```

## 11.2 Observed schedule

All eight observed normal runs are genuine `event=schedule` runs.

They were created/started roughly:

```text
06:50–07:56 UTC
```

instead of 02:00 UTC.

Observed delay:

```text
4h50m–5h56m
mean ≈ 5h16m
```

Collector starts only seconds after Actions run start.

GitHub documents that scheduled workflows may be delayed under load, particularly near the start of the hour. That is a credible platform mechanism, but the exact cause for these eight runs is **UNKNOWN**.

## 11.3 Operational freshness rule

A consumer needing actual freshness must use:

- `observed_at`;
- run timestamps;

not the cron declaration.

---

# 12. Workflow persistence and concurrency

Both collect and backfill share:

```text
concurrency group = github-observatory-write
cancel-in-progress = false
```

so those workflows are serialized against one another.

After successful collector completion:

```text
git add ForestTiger-GH
→ commit if changed
→ plain git push
```

Only generated data is staged by normal automation.

A separate external push can still advance `main` and cause push failure; workflow concurrency does not fence unrelated writers.

No such failure is currently observed.

---

# 13. Backfill and rerun model

Backfill is a **current-time bounded reconstruction**, not historical time travel.

It performs:

- current repository discovery/registry update;
- full current-reachable activity reconstruction;
- currently available closed-day views/clones;
- status/run write.

It skips:

- historical repository snapshots;
- historical language snapshots;
- historical rolling referrer/path snapshots.

## 13.1 Replacement-idempotence

Current persistence usually keeps one latest representation per semantic key.

Examples:

```text
repository snapshot → key data_date_utc
runs → key (data_date_utc, mode)
repository status → key (data_date_utc, repository_id)
rolling detail → replace whole data_date partition
activity → rewrite whole current projection
```

Thus rerun does not mean byte-identical output or immutable attempt history.

## 13.2 Mixed-mode status limitation

`runs.csv` stores mode.

`repository-status.csv` does not.

So collect + backfill on the same `data_date_utc` can coexist as two run rows while the later one overwrites the earlier per-repository statuses.

This is code-established but not currently observed.

---

# 14. Generated corpus assurance

At the baseline:

```text
28 repositories
12 public
16 private
167 generated CSV files
```

The generated file topology exactly matches current policy:

```text
16 private × 5 common families = 80
12 public  × 7 families        = 84
global registry/status/runs    =  3
total                           = 167
```

Latest normal run:

```text
28 seen
28 succeeded
0 error repositories
```

Latest status topology:

```text
12 public:
  metadata ok
  languages ok
  activity full_canonical_history_closed_days
  traffic ok

16 private:
  metadata ok
  languages ok
  activity full_canonical_history_closed_days
  traffic ok_aggregate_only_private
```

Current activity data contains no changed-file UNKNOWNs.

All latest file counts are exact.

These are current empirical facts, not guarantees under future failure.

---

# 15. Missing, zero, unavailable and UNKNOWN

The Product invariant:

```text
missing != zero
unknown != zero
```

must be applied by family.

| Evidence condition | Current meaning |
| --- | --- |
| `files=0, files_status=exact_empty_repository` | known zero files |
| blank files + `unknown_truncated` | unknown exact file count |
| missing activity day + fresh successful rebuild | zero currently reachable commits for that date |
| missing activity day + failed/stale rebuild | not safely interpretable as zero |
| views/clones row with 0/0 | explicit source zero |
| missing Traffic date + successful query | still not necessarily zero |
| missing public top-table item | may be below top-N or absent |
| missing private referrer/path file | intentional policy omission |
| no language rows + languages status ok | can be successful empty map |
| old file after current family error | retained evidence, not current success |

A correct analytical layer must preserve these distinctions.

---

# 16. Reliability and scaling envelope

At the current scale:

- 28 repositories;
- about 6,550 current reachable commits;
- healthy normal collector runtime roughly 3.4–4.6 minutes;
- 30-minute normal workflow timeout.

Approximate current successful normal request geometry:

```text
~165 REST calls
~111 GraphQL calls
~276 calls total before retries
```

The dominant growing cost is repeated traversal of accumulated state:

- full canonical commit history every run;
- recursive Git tree every run;
- whole CSV rewrites.

There is no incremental activity cursor, conditional REST cache, or rate-limit-aware adaptive scheduler.

Current scale is healthy; arbitrary future scale is not validated.

---

# 17. Security and privacy model

The Observatory repository is public.

It intentionally exposes selected high-level facts about private repositories:

- existence;
- name/full name;
- description;
- visibility/archive status;
- high-level repository metrics;
- daily activity aggregates;
- language bytes;
- aggregate daily Traffic when authorized.

It intentionally does **not** expose:

- private repository contents;
- commit identities/messages;
- paths/diffs;
- private popular paths/referrers.

The source-observation credential is injected as `OBSERVATORY_TOKEN` only to the collector step.

The workflow separately has `contents: write` for Observatory persistence.

Exact token type/scopes and least-privilege sufficiency are **UNKNOWN** from repository evidence.

---

# 18. Current facets and mismatches

A correct Current HOW must retain different current facets rather than smooth them.

## 18.1 Accepted/configured vs operated schedule

```text
accepted/configured:
02:00 UTC daily

observed:
scheduled event starts ~06:50–07:56 UTC
```

Both are current facts about different facets.

## 18.2 Current Product vs prior Research temporal proposal

```text
current Product:
closed-day T−1 partition + exact observation time

prior Research proposal:
snapshots T / flows T−1 / rolling T
```

Research has not changed Product.

## 18.3 Current source documentation vs preserved Traffic evidence

```text
current GitHub docs:
recent 14-day Traffic surface

preserved source-derived evidence:
at least one longer response horizon

cause:
UNKNOWN
```

## 18.4 Current implementation vs historical intent

The current mechanism can be reconstructed.

Historical reasons why every design choice was originally made cannot be reconstructed reliably from surviving code/docs alone.

No intent is invented here.

---

# 19. Representative end-to-end paths

## 19.1 Normal scheduled collection

```text
GitHub schedule configuration
→ GitHub eventually creates schedule event
→ latest main checkout
→ Python syntax compile
→ collector starts
→ current owner-repo discovery
→ registry reconciliation
→ per-repo activity
→ repository snapshot
→ languages
→ Traffic
→ status
→ run summary
→ stage ForestTiger-GH
→ commit
→ push
```

## 19.2 Backfill

```text
manual workflow_dispatch
→ current repository discovery
→ current registry update
→ full current-reachable history rebuild
→ recent daily Traffic retrieval
→ intentionally skip historical snapshots/detail
→ status + run
→ commit + push
```

## 19.3 Cold repository inspection

```text
profiles/README
→ repositories.csv
→ repository directory
→ selected CSV
→ SCHEMA
→ status/run if freshness/availability matters
→ derive any analytics outside the collection layer
```

## 19.4 File-count reliance

```text
repository.csv
→ select latest relevant snapshot
→ inspect files
→ inspect files_status
→ only treat number as exact when status says exact/exact_empty_repository
```

## 19.5 Activity reliance

```text
activity.csv
→ check latest activity status/freshness
→ interpret row as current reachable canonical-history aggregate
→ preserve historical revisability
→ do not infer authorship/productivity
```

## 19.6 Traffic-source reliance

```text
visibility
→ daily views/clones always possible when authorized
→ rolling detail only if public
→ check status
→ interpret daily vs rolling separately
→ never map absent top-table item to zero
```

---

# 20. Cross-concern invariants

The following invariants are supported across multiple current facets.

1. **Stable identity is repository ID, not repository name.**
2. **Observation time is distinct from attribution/event date.**
3. **Missing and UNKNOWN are not zero.**
4. **Current reachable Git history is revisable, not immutable historical observation.**
5. **Private repository contents remain outside the Product; selected high-level metadata does not.**
6. **Generated evidence does not own its own semantics.**
7. **Research does not silently change Product.**
8. **Partial collection may be valid when explicitly status-bearing.**
9. **Backfill reconstructs only evidence still supportable now.**
10. **Configured schedule does not establish actual freshness.**
11. **Analytics are downstream derivations, not canonical collection facts.**
12. **A successful workflow/process does not by itself prove every source family was available.**

---

# 21. Supported reliance

This synthesis supports a cold consumer relying on current Observatory to answer, with stated boundaries:

- what repositories were discovered;
- current high-level repository state by delayed snapshot;
- current exact file count when `files_status` permits;
- current default-branch reachable commit total;
- current-reachable historical daily activity;
- current GitHub language-byte snapshots;
- retained daily Traffic evidence;
- public rolling referrer/path top tables;
- collection health/status/run timing;
- basic current reliability/operational facts.

It does not support, without additional derivation/evidence:

- repository content claims;
- developer productivity or quality judgments;
- immutable historical canonical-history claims;
- exact midnight repository snapshots;
- unique visitors over a multi-day period from summing daily uniques;
- daily referrer/path flows;
- exact Traffic-source horizon as an invariant;
- historical snapshots before observation;
- every collector attempt from in-repo ledgers alone;
- least-privilege claims about the secret token;
- DORA/product-delivery claims;
- dashboard/portfolio rankings proposed only in Research.

---

# 22. Lookup routes

| Need | Primary route | Required qualification |
| --- | --- | --- |
| repository universe | `profiles/README.md → ForestTiger-GH/repositories.csv` | presence and visibility are current observations |
| current repo snapshot | `<repo>/repository.csv` | use `observed_at`; file count requires `files_status` |
| historical commit activity | `<repo>/activity.csv` | current-reachable, revisable canonical history |
| languages | `<repo>/languages.csv` | snapshot partition, not work-type activity |
| views/clones | `<repo>/traffic/views.csv`, `clones.csv` | daily source facts; missing not universally zero |
| referrers/paths | public repo detail files | rolling top-table snapshot only |
| collection freshness | `_collection/runs.csv` | same-mode same-day attempts replaced |
| family availability | `_collection/repository-status.csv` | mode not retained in key |
| exact semantics | `SCHEMA.md` | current semantic owner |
| implementation | `scripts/` | realization, not semantic owner |
| schedule/runtime | workflow YAML + Actions evidence + `runs.csv` | configured and observed facets differ |
| research proposals | `_mw/.../research/results/` | non-authoritative unless separately adopted |
| detailed current-state evidence | `research/current-corpus/01..13` | study/provenance route, not ordinary Product route |

---

# 23. Negative findings retained by fan-in

The following absences are material and remain visible:

- no current analytics/dashboard Product;
- no repository allow-list;
- no stored branch/ref dimension;
- no content-level corpus;
- no immutable per-attempt collector ledger;
- no current rate-limit-aware retry strategy;
- no incremental activity collection;
- no current operational source-family failures in the observed run set;
- no observed recursive-tree truncation;
- no observed changed-file UNKNOWN;
- no observed rename collision;
- no current private referrer/path persistence;
- no evidence proving exact cause of schedule delay;
- no evidence proving why historical AppDock Traffic exceeded current documented window.

---

# 24. Residual UNKNOWNs and bounded gaps

Material unresolved current-state questions are now narrow rather than architectural.

## UNKNOWN-1 — Scheduled-run delay cause

Observed consistently; GitHub high-load delay is a supported possible mechanism; exact cause not established.

## UNKNOWN-2 — Traffic documented-window contradiction

Preserved historical source response exceeds current documentation; exact explanation not established.

## UNKNOWN-3 — Actual `OBSERVATORY_TOKEN` least privilege

Repository cannot establish secret scopes/type.

## UNKNOWN-4 — Behavior under real rate limiting

Current client lacks dedicated handling; no empirical rate-limit failure in observed run set.

## UNKNOWN-5 — Large-tree truncation in this universe

Mechanism exists; no current observed case.

## UNKNOWN-6 — Actual same-day collect/backfill status collision

Current keys permit it; no current observed instance.

## UNKNOWN-7 — Historical design intent

Not reconstructed where no explicit record exists.

These do not block ordinary current mechanism understanding.

---

# 25. Prior Research disposition

The existing 2026-09-24 Research corpus is valuable but must remain typed.

## Temporal semantics Research

Useful proposal for a future T/T−1 redesign.

Disposition now:

```text
not current Product
requires a future Product Decision/change
```

## Expanded daily metrics Research

Useful target-development input for PR/issues/Actions/releases/deployments/derived layers.

Disposition now:

```text
not current observation family
not safe to assume implemented
```

## Dynamic rendering / visualization / Pages Research

Useful presentation/analytics architecture candidates.

Disposition now:

```text
no current dashboard exists
any implementation must preserve collector/analytics separation
```

No prior Research Result is discarded; none is promoted by repetition.

---

# 26. Bounded completeness and assurance statement

Within the declared Product baseline and discovered material current-state surface, this research cycle has:

- mapped all current Product/Work owner surfaces;
- reconstructed every current generated observation family;
- traced normal scheduled collection end to end;
- traced backfill end to end;
- reconciled configured vs observed operation;
- reconciled Product vs prior Research;
- audited current file-family topology;
- inspected all current activity files for changed-file UNKNOWN;
- inspected all latest repository file-count statuses;
- bound current public/private exposure;
- quantified current run duration/request geometry;
- preserved contradictions and UNKNOWNs.

The synthesis is therefore adequate as a **cold-entry current mechanism candidate** for development/research use.

It is not an assurance that all future runs, all GitHub platform behavior or all historical data are correct.

---

# 27. Admission and current-owner posture

This synthesis is intentionally **not admitted** as a new Product owner.

No Product owner transition was commissioned.

Therefore the current authoritative paths remain:

```text
README.md
AGENTS.md
SCHEMA.md
scripts/
.github/workflows/
ForestTiger-GH/
profiles/
```

This synthesis acts as:

```text
research fan-in
+ cold re-entry model
+ evidence-bound development baseline
```

The individual studies remain the deeper challenge/provenance route.

There is no duplicate “maintained Current HOW” claim.

---

# 28. Reopen triggers

Reopen the affected slice, not automatically the entire synthesis, when any of the following changes materially:

- root Product purpose/boundary;
- schema semantics;
- repository discovery or identity;
- temporal attribution;
- source-family schemas;
- activity source/rebuild method;
- Traffic API behavior;
- collector failure/status semantics;
- workflow schedule/concurrency/persistence;
- backfill semantics;
- repository visibility/privacy policy;
- token/permission architecture;
- repository universe/history scale;
- dashboard/analytics becoming current Product;
- a previously UNKNOWN operational branch is materially exercised.

Re-run broad Coverage Discovery only if a genuinely new mechanism/consumer/lifecycle appears outside the existing concern map.

---

# 29. Final current mechanism capsule

```text
GitHub Observatory today
=
public, dependency-light, GitHub-API evidence collector

automatic owner-repository discovery
+
stable ID / mutable-name registry
+
closed-day attributed current snapshots
+
full current-reachable canonical-history activity rebuild
+
retained daily Traffic
+
public-only rolling Traffic detail
+
explicit collection status and provenance
+
manual bounded backfill
+
Git-backed publication

with:
missing != zero
UNKNOWN != zero
Research != Product
configured schedule != observed freshness
current reachable history != immutable historical log
private contents != public high-level private metadata
```

That is the coherent current HOW supported by the 2026-09-30 research cycle.
