# GitHub Observatory: Visualization Inventory and Progressive Automated Reporting Requirements

**Research result date:** 2026-10-18  
**Status:** COMPLETE AS AN INVENTORY / PROPOSED PRESENTATION REQUIREMENTS; NOT AN IMPLEMENTED PRODUCT CHANGE  
**Scope:** requested, rendered, and researched visualization patterns for the repository observatory through 2026-10-18; observable data through the latest fully closed UTC day, 2026-10-17.  
**Authority boundary:** This document specifies a candidate presentation layer. It does not amend collection, the data contract, GitHub Actions, repository discovery, or the storage policy.

## 1. Main findings and decision posture

The requested visualization program is **not a single dashboard chart**. It is a sequence of views that moves from an account-wide picture to category composition, individual repositories, detailed metric histories, unusual events, and evidence-quality checks. The same question is often intentionally revisited at different time resolutions.

The stable, user-requested core is:

1. **Monthly portfolio composition, year to date**, both grouped and repository-detailed.
2. **ISO-weekly portfolio composition, year to date**, in the same two resolutions.
3. **Daily portfolio activity**, including a trailing two- or three-month history, short-term bursts, and a selected month's detailed composition.
4. **Repository-specific development and physical-growth curves**, plus rankings and a repository-by-week activity heatmap.
5. **Daily, non-rolling GitHub Traffic viewers and cloners**, particularly the independent daily unique viewers of Tabularium.
6. **One repository with the highest daily unique viewers per day**, colored by repository identity, with explicit completeness and tie handling.
7. **Public referrers and popular paths**, treated exclusively as independently observed rolling-window snapshots rather than daily visitor/path attribution.
8. **Collector health, data coverage, and the distinction between observed zero and unavailable information**.

The original output preference is for attractive, consistent charts rather than isolated raw CSVs: colors identify broad groups, per-project shades stay within their parent group's hue, and monthly and weekly charts share exactly the same classification, labels, and legend logic.

**Core semantic non-negotiable:** Never sum daily unique viewers or daily unique cloners across different days or repositories and label the result as people. Never treat the GitHub rolling referral/path uniqueness fields as daily uniqueness. A daily cross-repository maximum is valid as the *maximum repository-level observed daily uniques*, not as the number of distinct viewers of the owner account.

### 1.1 Status labels used below

- **RENDERED** — at least one variant was actually graphed, tabulated, or repeatedly reported during analysis.
- **REQUESTED** — a desired presentation or analytical cut explicitly requested, but no complete independently verified graphic is established for that exact variant.
- **RESEARCHED / NOT RENDERED** — described in prior visualization/metrics research as a candidate, not to be represented as a completed chart.
- **NOT IN SOURCE** — requires new observations or a separate authorized collection feature, not a transformation of existing canonical CSVs.

A chart can be rendered as one visual in a conversation and also have additional requested variations; the variants are distinguished where relevant. Historical images and reported figures are examples of this inventory, not authoritative permanent snapshots.

### 1.2 Available data and presentation boundary

Canonical observations currently support: discovered-repository registry; delayed repository snapshots (file count, repository size, canonical commit count, stars/forks/subscribers); language byte snapshots; canonical reachable-commit activity and changed-file occurrences by committed UTC day; daily views/clones and their independent daily unique counts; public-only rolling top referrers and popular paths; and collection runs and source statuses.

The collector is intended to remain a **compact evidence store**. Derived rankings, maxima, monthly/weekly charts, comparisons, heatmaps, color assignments, annotations, and written interpretations belong in a separately generated, reproducible presentation model. Do not add scores, aggregated uniqueness, inferred source-code inventories, or rankings as though they were canonical collected facts.

## 2. One stable classification and one color system

### 2.1 Agreed six-category grouping

| Stable group | Parent color | Repository membership / rule | Interpretation |
| --- | --- | --- | --- |
| Platforms | Turquoise | AppDock; Lepilot; stratbox-windows | Application platforms, interfaces, and desktop delivery. |
| Data | Blue | LIN-Core; lincore-dock-private; newsflow; tabularium; stratbox; github-observatory | Data infrastructure, repositories, ingestion, and observatory evidence. |
| Trading | Amber | Compass; Navigator (provisional placement) | Markets, trading, and portfolio analysis methodologies. |
| Engineering AI-methodology | Violet | MADAR; MADARAII; MADAR-supplements; madaraii-pilot and numbered pilots; all mandat-*; CYBERSECLEX | Engineering methods, executable methodology, and security methodology. |
| AI architecture and memory | Green | PROTOS; CMemory | AI architecture and cognitive memory standards. |
| Others | Slate gray | analytics; LEPILOT_old; COTRA; fin-business; Finance-Board; otherwise unclassified until explicitly assigned | Residual category, not a synonym for unmonitored. |

Group names and project names are visualization identities, not additions to GitHub's stored observation dimensions. New repositories are discovered automatically; category assignment is an independent, versioned presentation decision. Do not introduce a fixed allowlist for **collector discovery** merely because charts need a grouping mapping.

**Color principle:** choose a distinct base hue for each category. Assign stable shades to individual repositories within their parent hue. A project must not arbitrarily change color from daily to weekly or from monthly to YTD views. Category colors must remain distinguishable under light/dark themes; supplementary labels/patterns make charts usable without relying solely on color. Do not use green/red to decorate ordinary categories as though all groups represent statuses.

### 2.2 Dimensions, permitted aggregations, and defaults

| Dimension | Default / policy |
| --- | --- |
| Time | UTC, with separate observed-at and closed-day boundaries. |
| Monthly | Calendar months, January through latest closed day; final month is month-to-date and explicitly incomplete. |
| Weekly | ISO Monday–Sunday calendar weeks (week index anchored to 2025-12-29 for 2026). Year-opening and current weeks visibly marked as partial. |
| Daily | Each independent closed UTC day; useful windows: latest 14/28 days, 2–3 months, month-to-date, and full available history. |
| Categories | Stable six-group taxonomy above; optional category filter. |
| Repositories | All auto-discovered repositories, including eligible public and private aggregate observations; visibility filter and per-repository drill-down. |
| Commits | Additive by repository and disjoint committed-day interval **within the current canonical reachable history**; history may be revised after merge/rebase. |
| Changed-file occurrences | Additive occurrences, not distinct modified files; nullable/unknown component must remain visible. |
| Daily view/clone counts | Day-level event counts may be aggregated as events when dates do not overlap and coverage is sufficient. |
| Daily unique viewers/cloners | **Only per-repository, per-day values. No summing across repositories or days; no rolling presentation masquerading as daily.** |
| Repository snapshots | Stocks observed after the close of the attributed day, not exact 00:00 states; different from daily activity. |
| Referrers / popular paths | GitHub rolling top-N snapshots observed at collection time; neither daily, exhaustive, nor joined to each other. |
| Missing values | Missing != 0. No zero-filling of unavailable source-family records and no unmarked interpolation. |
| Ties | Preserve exact ties where informative; deterministic highlight may use secondary raw view count but must declare the rule. |
| Comparisons | Recompute from canonical CSV on each render; do not append values to old rendered files or silently smooth the history. |

The possible month-day bins 1–7, 8–14, 15–21, 22–end-of-month were explicitly considered. They are **not** the default: their last bin has variable length and their discontinuity at month boundaries makes period comparisons misleading. Retain them only as an optional clearly labeled within-month operational view, never as ISO weeks.

## 3. Portfolio-wide views: from broad summary to grouped and repository composition

This is the **first visual layer**. It answers: how much development happened, when did the overall regime change, and which groups/projects drove each phase?

### 3.1 Chart inventory — activity and composition

| ID / status | Chart and visual form | Horizontal axis | Vertical axis / value | Breakdown and controls | Source / critical notes |
| --- | --- | --- | --- | --- | --- |
| ACT-01 RENDERED | **Monthly commits, grouped** — stacked bars by month, YTD | Calendar month Jan…current | Count of commits | Six fixed group colors; total per bar; optional group selection | Per-repository activity.csv, commits; final month partial; classification applied at render time. |
| ACT-02 RENDERED | **Monthly commits, project-detailed** — same stacked bars with shades | Calendar month | Count of commits | Repository shades nested under six groups; hierarchical/grouped legend; group-level total equals ACT-01 | Same source and period as ACT-01; projects with zero can remain in selector, not clutter the legend. |
| ACT-03 RENDERED | **Weekly commits, grouped** — stacked bars from start of year | ISO week or explicit Monday–Sunday date range | Count of commits | Six group colors; partial first/current week annotation | Activity.csv; use ISO weeks throughout the year, not four monthly buckets. |
| ACT-04 RENDERED | **Weekly commits, project-detailed** — shades of group colors | ISO week | Count of commits | Each active repository within parent hue, sortable/zoomable legend | Same totals as ACT-03; 40+ bars and many projects need zoom/tooltip, not tiny labels. |
| ACT-05 RENDERED | **Daily total portfolio commits** — line or slender bars, trailing 2–3 months | UTC day | Commits/day | All repositories; optional group filter, 28d/60d/90d presets | Explicit zeros only for confirmed zero-activity days; canonical history is revisable. |
| ACT-06 RENDERED | **Daily commits by groups** — stacked bars | UTC day, selected month or recent 28/60/90d | Commits/day | Six colors; separate highlighted bursts and daily total | In practice repeatedly graphed for October; YTD daily zoom optional. |
| ACT-07 RENDERED | **Daily project composition** — interactive stacked bars or small multiples | UTC day | Commits/day | Repositories colored by group shade; selected repos/top-N/one group | Project-specific daily series and daily leaders were graphed for several active repositories; comprehensive all-repo layered variant is the drill-down form. |
| ACT-08 RENDERED | **Top active repositories** — descending horizontal bars | Repository, sorted by value | Count of commits in selected period | 7d, 28d, MTD, YTD; group-colored project bars | Distinguish absolute monthly rank from *latest-day* rank; no persistent rank in collector. |
| ACT-09 RENDERED | **One-day portfolio leaderboard / event breakdown** — horizontal bars or compact scorecard | Active repository | Commits on selected day | Project grouping + sorted descending + selected day | Useful for burst attribution and explicit dormant projects. |
| ACT-10 RENDERED | **Repository × ISO-week activity matrix** — heatmap | ISO week across year | Repository rows, organized by six groups | Saturation proportional to weekly commits, optionally log-scaled or per-repo normalized | State chosen normalization in caption; within-row normalized color does **not** express cross-repo absolute volumes. |
| ACT-11 RESEARCHED / NOT RENDERED | **Normalized work mix** — 100% weekly/monthly stacked bars | ISO week or month | % of additive commits or occurrences | Six groups, 100% composition | Complements absolute ACT-01/03; do not mislabel language byte share as work type. |
| ACT-12 REQUESTED / RESEARCHED | **Activity calendar heatmap** — day-of-year cells | Calendar week position | Weekday | Day total or selected-repo commits as fill color | Useful for year-scale cadence, gaps, concentration, weekday patterns. |
| ACT-13 REQUESTED / RESEARCHED | **Active repository breadth** — line/bars | UTC day, ISO week, or month | Number of distinct repositories with >0 commits in disjoint period | All / group / visibility / active-vs-monitored | Count each repo once per interval, not sum daily active-repo counts to call it weekly distinct. |
| ACT-14 REQUESTED / RESEARCHED | **Cumulative commits / YTD progress** — line | UTC day or month end | Cumulative canonical commits since Jan 1 | Group or project lines; YTD only | Additive commit metric permits cumulative plot, but an observed Git rewrite can revise earlier points. Do not confuse with lifetime snapshot total. |
| ACT-15 RESEARCHED / NOT RENDERED | **Concentration and active-group shares** — ranked bars / normalized stacked | Month/week or repository rank | Share of additive commits | Top-3/top-4 projects; group shares; threshold options | Analytical composition only; no opaque performance/quality score. |
| ACT-16 RESEARCHED / NOT RENDERED | **Activity cadence and relative regime changes** — small multiples / calendar | Time | Commits and active-day signal in separate panels | Group and repo filters | Direct values preferred; no unexplained moving-average, composite momentum or burst score. |

ACT-01 through ACT-10 cover the repeated monthly, weekly, daily, and leaderboards/heatmap visualizations requested and produced in the conversation. ACT-11 through ACT-16 add explicitly discussed, related presentation requirements, not silently assert that they already exist as finished charts.

### 3.2 Required time perspectives and default drill-down

- **Year overview:** ACT-01 first, with ACT-02 one click away.
- **Year weekly:** ACT-03 followed by ACT-04; ACT-10 offers a complementary repository-first matrix.
- **Recent pulse:** ACT-05 and ACT-06.
- **Selected event:** open one day or ISO week to ACT-07/09 and the individual repositories that contributed.
- **Project focus:** repository timelines and non-development signals from Sections 4 and 5.

In every period, totals for a parent group must equal the sum of its child projects, and all group totals must equal the all-repository total for the same date cut and observation universe.

## 4. Development depth and physical repository state

This is the **second visual layer**. It answers: did the repository physically grow, how wide were the changes, and did an apparent burst correspond to many commits, many affected-file occurrences, or a large new file corpus?

### 4.1 Chart inventory — canonical activity and snapshots

| ID / status | Chart and form | Horizontal axis | Vertical axis / value | Breakdowns and controls | Source / caveats |
| --- | --- | --- | --- | --- | --- |
| DEV-01 RENDERED | **Individual daily commit timelines** — lines/bars | UTC day | Commits/day | Selected repo, multiple project overlays or small multiples | activity.csv; examples included burst and post-burst cooling in individual projects. |
| DEV-02 RENDERED | **Repository physical file growth** — multi-series line | Attributed snapshot day | Exact Git blob file count | Selected repositories, separate hues | repository.csv files only where files_status exact; observed snapshots can already include the following UTC day's work. |
| DEV-03 RENDERED | **Repository size development** — lines or paired change bars | Snapshot date | GitHub-reported size_kb | Selected repositories, absolute / observed change | repository.csv size_kb; is not LOC, source code lines, or the amount of knowledge. Reorganization can reduce size while activity increases. |
| DEV-04 RENDERED | **Canonical lifetime commits snapshot vs daily commits** — paired panels | Snapshot date or UTC day | Canonical reachable total / daily committed counts | Selected repository, axes kept separate | repository.csv commits vs activity.csv commits; avoid naive same-day reconciliation of delayed snapshot and UTC daily event. |
| DEV-05 RENDERED | **Changed-file occurrences/day** — bars/lines | UTC day, ISO week, or month | Sum of changed_file_occurrences | Repo, group, portfolio, and selected burst | activity.csv; occurrences count repeated file modifications, not distinct files. |
| DEV-06 RENDERED | **Average changed-file occurrences per commit** — grouped bars | Repository + comparable periods | Occurrences/commit, explicitly derived | Period A vs B; examples compared consecutive October days | Calculate when commits >0 and unknown coverage is acceptable; mark unknown changed-files; number measures granularity, not quality. |
| DEV-07 RENDERED | **Daily commits vs changed-file occurrences** — dual small multiples | UTC day | Commits in first panel; occurrences in second | Same repo/group/period | Avoid dual-Y-axis visual distortion; bursts with many CSV updates can produce large occurrences per single collector commit. |
| DEV-08 REQUESTED / RESEARCHED | **Languages by repository and across time** — stacked bars/lines | Snapshot date or repository | GitHub language bytes | Language × repo; top-N; change in language mix | languages.csv; language bytes do not equal authored lines or semantic work type. |
| DEV-09 REQUESTED / RESEARCHED | **File count and size rank at latest snapshot** — paired horizontal bars | Repository | Exact file count or size_kb (separate panels) | Group / visibility / selected latest observation | Only comparable with complete coverage; do not infer quality or output volume from size. |
| DEV-10 RESEARCHED / NOT RENDERED | **Repository age / newly discovered universe growth** — step/bar | Observation date | Count of discovered repositories | Present/absent, active/archived, visibility | Registry first_seen_at is Observatory discovery, not necessarily repository creation; snapshot facts separate. |
| DEV-11 RESEARCHED / NOT RENDERED | **Stars, forks, subscribers** — mini-lines / table | Snapshot date | Integer count per metric | Repositories and visibility filter | repository.csv snapshots; separate from daily event history. |
| DEV-12 NOT IN SOURCE | **Code and knowledge corpus growth** — lines/stacks | UTC day, week, month | LOC, readable-text lines, bytes by document type, new/changed research/artifact units | Source code vs documentation / human-readable / machine-readable knowledge | Explicitly desired in later discussion, **not collected** under current evidence-only repository contract. Requires an independent authorization and privacy-preserving source design before rendering. |
| DEV-13 NOT IN SOURCE | **File additions/deletions, source-path or document taxonomy flow** — grouped bars, waterfall | UTC day / week | Newly created/deleted files per type | Knowledge form, section, file format | Current collector does not persist change paths, document inventories, diffs or new-file IDs. Do not infer from a change in total blob count that every difference is a newly written file. |
| DEV-14 NOT IN SOURCE | **Feature/requirements/test conformance coverage** — matrix/scorecard | Requirement family / release | Verified coverage, passed/failed tests | Product release and test suite | Requires separate domain-specific evidence; repository activity alone cannot establish completion or quality. |

Current usage establishes DEV-01 to DEV-07 as directly valued views. DEV-12 to DEV-14 represent the repeatedly raised need to move beyond simple commit counts but are **out of scope for automatic generation from the existing collector**.

### 4.2 Safe interpretations

- Commit count measures commits in the current reachable Git history; one commit can change one file or many.
- Changed-file occurrences are not unique changed files and should never be presented under that ambiguous label.
- A delayed repository snapshot can overlap part of the next UTC day; physical snapshots and completed-day activity must not be forced into a one-to-one reconciliation.
- Size and file count can increase, stay flat, or decrease independently of commits.
- New-language detection requires valid observations on both sides; absent language bytes with missing snapshot is not evidence of language removal.

## 5. External attention and GitHub Traffic

This is the **third visual layer**. It answers: which repositories attracted GitHub UI viewers, which were cloned, and which public referrers or specific paths appeared in GitHub's top-N windows?

### 5.1 Daily viewers, cloners, and cross-repository maxima

| ID / status | Chart and visual form | Horizontal axis | Vertical axis / value | Color / breakdown / controls | Exact semantics |
| --- | --- | --- | --- | --- | --- |
| TRF-01 RENDERED | **Tabularium daily unique viewers** — clear line or discrete bars | Each UTC calendar day | One repository's daily views.csv uniques, integer | Tabularium, full retained history or selected 28/60/90d period | **Absolutely no rolling, no inter-day summation, no values from popular paths or referrers.** |
| TRF-02 RENDERED | **Tabularium daily viewers vs daily unique cloners** — paired series | UTC day | Daily unique viewers and daily unique cloners; two series | Same repository, per-day values | Distinct measurement populations; never add series together or infer identical humans. |
| TRF-03 RENDERED | **Tabularium daily view events vs unique viewers** — bars and separate lines/small multiples | UTC day | Daily view count / independent daily uniques | Event count and unique measure explicitly labeled | View count can be much larger than uniques because repeated repository UI activity is counted. |
| TRF-04 RENDERED | **Stratbox daily unique cloners** — line | UTC day | Daily clones.csv uniques | Highlight peaks, downtrend, missing days | One-repo daily uniques; the observed multi-day clone storm is a motivating example, not a classification of client identities. |
| TRF-05 RENDERED | **Stratbox clone events vs daily unique cloners** — paired small multiples | UTC day | Daily clone count, daily unique cloners | Same dates, separate labels | Events vs identifiers, not equivalent measures. |
| TRF-06 RENDERED | **Repository commits vs daily unique cloners** — two overlaid or synchronized small-multiple series | UTC day | Commits/day and daily unique cloners | Selected repository, exact shared date window | Illustrates coincident peaks; does not establish that development caused cloning. |
| TRF-07 RENDERED | **Daily maximum repository-level unique viewers across the monitored universe** — **one colored bar per day** | Closed UTC day | max(views.csv uniques among available repositories for that same day) | Bar color identifies selected winner; repository group shade; tooltip lists ties and data coverage | **Maximum only**, never a sum or account-wide distinct-user count; do not interpret missing as zero. |
| TRF-08 RENDERED | **Winner / coverage companion for TRF-07** — strip/labels/table | Closed UTC day | Repositories with an actual daily views observation; total eligible for that day | Winner, tie indicator, coverage proportion, missing-repo list on drill-down | Winning repository identity is only justified over the *observed* eligible subset; coverage changes across dates. |
| TRF-09 REQUESTED / RESEARCHED | **Daily maximum unique cloners across repositories** — same pattern as TRF-07 | Closed UTC day | max(clones.csv uniques among available repos) | Winning repository + coverage + tie logic | Applies same non-additivity and missing-state rules to clone clients. |
| TRF-10 REQUESTED / RESEARCHED | **Most-viewed repositories by raw daily views** — ranked bars | Repo or UTC day | Additive raw view events or repo-level daily view count | Source views.csv count; daily winner or top-N | Different ranking from unique viewers. Never call raw views 'visitors'. |
| TRF-11 REQUESTED / RESEARCHED | **Most-cloned repositories by raw clone events** — ranked bars | Repo or day | Raw clone events | Top-N, portfolio period, group shades | Clone events additive where valid; unique cloners are not. |
| TRF-12 RESEARCHED / NOT RENDERED | **View/clone attention panel** — separate 28d tiles or small multiples | UTC day or repository | Raw events and daily uniques as separately labeled panels | Search, compare, visibility, repository detail | A first-page summary can show raw event totals, but no false owner-wide unique headcount. |

The **TRF-07 winning-repository contract** is particularly important:

1. For each UTC day, include only repositories with a real views.csv row for that date and permissible visibility.
2. Compute the maximum daily unique-viewers value among those rows.
3. If the maximum is **zero**, display “0 observed, no positive leader”; never assign a fake winner by alphabetic order.
4. At a positive tie, preserve the full list of co-leaders in metadata and tooltip. A single highlighted representative may be selected by greater raw views.csv count, then a stable repository ID/name order; document that secondary convention visibly.
5. Bar height **remains the unique-viewer maximum** even if the tiebreak uses raw views; do not substitute raw views for the Y value.
6. Bar color follows the winning repository's own stable project shade. It is not a group-wide total or a sum of winners.
7. Show an explicit coverage strip or indicator for each day: rows present / repositories eligible for observation, and distinguish repositories not yet discovered from unavailable daily records.
8. A top repository with 4 viewers gives only a lower-bound observation of four distinct viewers across the account's repository set; no deduplicated owner-wide count is available.
9. Do not invent leading repositories on dates before their creation or when they lack source evidence.
10. When source coverage is partial, the title or subtitle must say "leader among observed repositories", not "guaranteed leader across all".

### 5.2 Rolling public discovery: referrers and popular paths

| ID / status | Chart and form | Horizontal axis | Vertical axis / value | Breakdown | Source / interpretation |
| --- | --- | --- | --- | --- | --- |
| REF-01 RENDERED | **Current top public referrers** — ranked table/horizontal bars | Referrer hostname | Rolling top-N count and separately labeled rolling uniques | One public repo, selected observation timestamp | traffic/referrers.csv; independent rolling-window snapshot, not daily counts. |
| REF-02 RENDERED | **Historical referrer appearance/disappearance** — timeline/table | Exact observed_at or attributed snapshot | Presence in rolling top-N and observed count/uniques | Domain × public repo, discovery/last-seen | A new top-N entry is not necessarily a first-ever visit; disappearance may be window expiry or top-N displacement. |
| REF-03 RENDERED | **Referrer concentration across public repositories** — matrix/table | Public repository | Present referrer domains and snapshot top-N values | Public only, name/domain | Used to compare whether security-intelligence/AI discovery hostnames appeared outside Tabularium. |
| REF-04 RENDERED | **Popular repository paths** — descending ranked bars/table | Reported path or human-readable title | Rolling top-N count and separate rolling uniques | Public repository, selected snapshot | traffic/paths.csv; no inference of a specific visit date from a rolling total. |
| REF-05 RENDERED AS QUALITATIVE ANALYSIS | **Referrer/path coincidence investigation** — synchronized time table plus external repository events | Adjacent snapshot timestamps / selected days | Changes in rolling top-N entries; qualifying path and activity changes | Public repo, referrer host, observed paths | Investigative juxtaposition only; GitHub does **not** expose a direct referrer-to-path join or individual visitor journey. |
| REF-06 REQUESTED / RESEARCHED | **New external-hostname watchlist** — appearance matrix or notification digest | Detection timestamp | New/reappearing rolling referrer hostname | Public repo; optionally categorized as AI discovery, search, security intelligence, other | Classification describes provider category, not visitor identity, motives or security incident. |
| REF-07 NOT IN SOURCE | **Exact host → visited file/page or human identity** | N/A | N/A | N/A | Not supported by GitHub Traffic source; no invented join, timestamp attribution, visitor identity or hidden access log. |

The discussions of Nautilus, ETHIC, ChatGPT, Perplexity, Bing and GitHub referrals illustrate why this family matters. They do **not** establish individual viewer identity, intent, organizational affiliation of a particular session, or exact file-level referral attribution.

No graph should silently merge REF-family rolling uniqueness with daily TRF-family uniqueness.

### 5.3 Important traffic distinction

- A repository with zero recorded GitHub UI viewers can still have independently observed Git clones.
- A high number of daily unique cloners can coincide with intensive development, bots, CI or other tools, but its precise origin is not observed.
- Absence of a browser referrer cannot explain or rule out cloning, because clone requests are a separate traffic family.
- Public top-N referral/path listings do not enumerate all traffic.
- Private repositories may retain aggregate Traffic without public referral/path detail; do not work around that boundary.

## 6. Observatory operation, completeness and measurement reliability

This is the **fourth visual layer**. It answers: can the chart be trusted, did the collector actually run, and where do missing/late source values arise?

| ID / status | Chart and form | Horizontal axis | Vertical axis / value | Breakdown and controls | Source / notes |
| --- | --- | --- | --- | --- | --- |
| OPS-01 RENDERED AS KPI/TABLE | **Collector collection health** — 3–5 KPI tiles/table | Latest run or history | Seen/succeeded/errored repository count | Per run and repository subset | _collection/runs.csv. "Success" is not synonymous with every source family having a complete row. |
| OPS-02 RENDERED AS TREND/TABLE | **Scheduled-vs-actual start lag** — line/bars | Scheduled UTC day | Actual start lag in minutes/hours | Runs only; highlight earliest/latest and late clusters | _collection/runs.csv and declared 02:00 UTC schedule; avoid guessing the exact platform cause. |
| OPS-03 RENDERED AS KPI/TABLE | **Collector execution duration** — line | Run observation date | finished_at − started_at in minutes | Run mode, successful/partial/error | Execution duration is not the same as scheduler start lag. |
| OPS-04 RENDERED AS COVERAGE STRIP | **Per-day traffic coverage** — strip/heatmap | Closed UTC day | Count of repositories with a legitimate daily observation | Views vs clones, public/private status and repository age | repository-status.csv + day rows; a missing file/date stays unavailable rather than zero. |
| OPS-05 RESEARCHED / NOT RENDERED | **Source-family health matrix** — heatmap | UTC observation day | Repository rows | Metadata, languages, activity, traffic statuses by categorical color/pattern | _collection/repository-status.csv; distinguish ok, aggregate-only-private, unavailable, error, skipped, unknown. |
| OPS-06 RESEARCHED / NOT RENDERED | **Universe discovery / active and archived state** — timeline | Scan date | Newly seen, present, absent and archived repositories | Public/private cohorts, new projects | Registry/snapshot facts; first_seen is discovery, not creation. |
| OPS-07 RESEARCHED / NOT RENDERED | **Observation freshness** — latency bars | Observation date / repository | Last fresh observation age by source family | Different expected cadence for flows vs stocks vs rolling top-N | Avoid blanket declaration of stale data from a source-family with different legitimate update behavior. |
| OPS-08 RESEARCHED / NOT RENDERED | **Historical revision check** — annotated comparison/table | Rebuild date and committed day | Same-day activity values before/after current reachable-graph revision | Repo/day where saved historical versions exist | Current CSV may revise old dates after merge/rebase; only compare if earlier version evidence exists. |
| OPS-09 RESEARCHED / NOT RENDERED | **Workflow/API resource consumption** — duration/count panels | Run or day | Requests, retry/error counts, runtime and future API costs | Collector phase and source family | Some quantities not persisted; must not pretend to reconstruct them from unrelated data. |

Always show **latest closed day**, **collection observed-at timestamp**, repository coverage, and missing-state handling near the charts. A successful collector run with incomplete GitHub Traffic availability must not be shown as full traffic coverage.

## 7. Adjacent research interests that are not current Observatory charts

The prior research also considered a broader analytics product, but those subjects must be separated from the observed chart inventory and from existing data capabilities.

| Area / status | Candidate visual representation | Metric family needed | Gate |
| --- | --- | --- | --- |
| Development flow — RESEARCHED | Opened/merged/closed pull requests, review times, PR size distributions, issues opened/closed, backlog and lead-time trends | Additional aggregate PR/issue observations | Separately approved schema, API and privacy contract. |
| Human vs automation / work type — RESEARCHED | Grouped work composition by human/tool origin or classified change kind | Additional reliable classification evidence | No inferred identities, authors, commit contents, or arbitrary categorization from current CSV. |
| Automation / Actions — RESEARCHED | Workflow runs, failures, reruns, queue delay, job durations, failure recovery, per-workflow health | New Actions observations | Keep credentials/logs/artifacts out of public stores; source support and authorizations required. |
| Delivery — RESEARCHED | Releases, deployments, release cadence, valid DORA-related distributions | New releases/deployment aggregates | Do not infer production performance from commit count alone. |
| Governance — RESEARCHED | Branch protections, policy/configuration drift, repository state history | New governance snapshot fields | Repository access limits; do not introduce refs as a current stored dimension without decision. |
| Repository knowledge/content — REQUESTED, NOT IN SOURCE | LOC, text lines, markdown/document count by format, new research/article knowledge forms, product acceptance/coverage | New source-level methodology and storage model | Currently prohibited from the compact observation core without separately authorized contract change. |
| Portfolio custom comparison — RESEARCHED | Normalized small multiples, user-selected project compare and side-by-side period delta | Existing additive or stock data; optional new metrics | Must retain metric-specific comparability and explicit period widths. |

An item in this section is **not** a demand to expand the live collector in the same change as chart rendering. It is retained to avoid losing prior investigative interests.

## 8. Recommended visualization sequence: progressive disclosure

The user explicitly prefers progression **from general pictures to detailed sizes and representations**. The following is a proposed, navigable sequence, rather than a flat list of independent dashboard tiles.

### Level 0 — Universe, date cut, and evidence quality

Show latest collection timestamp, last fully closed UTC day, discovered repositories, successful/failed sources, selected period, and metric-family completeness. Expose the difference between zero, unavailable, not yet created/discovered, and rolling-window source data.

### Level 1 — Whole portfolio, YTD and recent regime

Primary visuals: monthly grouped commits (ACT-01), weekly grouped commits (ACT-03), recent daily total activity (ACT-05), and collection quality (OPS-01). Focus on overall portfolio structure and transitions.

### Level 2 — Explain composition

Next: monthly and weekly project-detailed counterparts (ACT-02/04), category/group shares (ACT-11/15), project-by-week heatmap (ACT-10), recent category pulse (ACT-06), active repository breadth (ACT-13). Give every project its parent color family.

### Level 3 — Identify actual drivers

Next: top repositories for selected period (ACT-08/09), selected repository daily activity (DEV-01), file count/size/canonical snapshot (DEV-02/03/04), changed-file occurrences and per-commit width (DEV-05/06/07), language composition (DEV-08). Drill-down retains the original period and project selection.

### Level 4 — Audience and discovery

Next: per-repository daily Traffic (TRF-01/02/03/04/05), portfolio **maximum daily unique viewers** with winner and coverage (TRF-07/08), clone vs activity coincidence (TRF-06), public referrers and popular paths (REF-01…06). Referrers and paths remain **separate rolling snapshots**, never attributed to the winning daily viewer or joined into exact access journeys.

### Level 5 — Incidents, edge cases, and provenance

Investigate specific burst dates and traffic anomalies, scheduler lag, partial collection, repository revisions and missing observations. Link each chart to available source rows and their semantics rather than persist guessed stories.

### Level 6 — Separate future research extensions

Only after defining an explicitly authorized evidence model: LOC/document growth, CI development, delivery, governance, work types, knowledge classification and acceptance/test coverage. These do not contaminate the simpler existing product contract.

## 9. Publishing: repository landing page, interactive exploration, and evidence

A coherent future implementation can have three presentation surfaces:

| Surface | Recommended responsibility | Content |
| --- | --- | --- |
| Repository landing summary | Low-latency overview and navigation | Last closed day, scan health, monthly/weekly grouped view, recent activity, attention indicator; small generated static images. |
| Interactive exploratory dashboard | Progressive drill-down from level 1 to level 5 | Project colors, filters, ISO calendar controls, synchronized timelines, tooltips, per-day winners, source-data coverage, tables, compare mode. |
| Evidence route | Underlying canonical observations and exact data contract | Links to contributing CSV and explicit metadata about the chart window, cohort, completeness, transformation, and timestamp. |

The same **derived semantic chart model** should supply the static and interactive presentations. Rendering must not create a new interpretation of “unique viewers”, or treat an absent Traffic row as a known zero.

Possible generated outputs: accessible SVG for static repository views; static HTML/JS for an interactive interface; per-chart structured JSON for client rendering; user-requested downloadable PNG/CSV/ZIP exports. These are **derived and reproducible**, not a replacement for canonical observations.

The collection workflow should commit/verifiably preserve observed facts **before** a potentially failing dashboard-render step. Renderer failure should never prevent preservation of a newly observed daily record. A separate render-and-publish workflow or isolated job is appropriate, subject to later design/authorization; no workflow is changed by this research.

## 10. Chart registry for eventual Actions implementation

Each chart needs a deterministic, testable contract. The registry is part of the proposed derived presentation layer, not the observation store.

Suggested common fields:

| Field | Purpose |
| --- | --- |
| chart_id | Stable identifier such as ACT-01 or TRF-07. |
| status | Rendered example, requested, researched only, or gated on new data. |
| title and subtitle | Clear exact metric, time scope and missing-state semantics. |
| source_families | Which canonical CSV families and schema versions are required. |
| statistic and unit | commits, changed-file occurrences, files, size_kb, unique viewers, etc. |
| temporal_grain | closed UTC day, ISO week, calendar month, delayed snapshot, rolling top-N snapshot. |
| interval and completeness | from/to, last closed day, partial period flag, coverage by source family. |
| grouping_version | The six-group mapping and stable repository identity colors used for the render. |
| project_filter / visibility | Included repo IDs or whole discovered universe, public/private eligibility. |
| x, y, series, sort | Axes and displayed entities; stacking/normalization policy. |
| null_and_zero_policy | Empty vs observed zero vs not-yet-created vs unavailable. |
| tie_policy | Required for daily winners and leaderboards. |
| privacy_policy | Scope of data exposed by public artifacts. |
| presentation_targets | Landing-page graphic, exploratory chart, downloadable data. |
| provenance | Collection observed-at and evidence source identifiers, without source-content replication. |

### 10.1 Rendering invariants and tests

**R1 — arithmetic:** All portfolio/group/repository commit totals agree for identical period, universe, and baseline. Monthly and ISO-week totals reconcile with their constituent daily counts.

**R2 — temporal:** No contribution from the open UTC day. Display partial first/current month/week; use real calendar week boundaries.

**R3 — uniqueness:** Daily unique viewers or cloners must never be added across repositories/days to represent distinct people. TRF-07 uses a maximum of daily uniques, not a sum. Raw counts remain separately labeled.

**R4 — winner semantics:** No winner for a zero maximum; a tied maximum remains discoverable. If one winner is highlighted by raw-view tie-break, the Y value remains the original maximum unique count.

**R5 — absence:** Missing != 0. Charts preserve observation coverage and do not silently interpolate or extrapolate absent daily Traffic.

**R6 — source-family isolation:** Rolling referrer/path values never enter daily viewers/cloners; public-only path detail is not generated for private repositories.

**R7 — stable colors:** A repository's shade belongs to its category; colors and project assignments do not change simply because a new repository is discovered.

**R8 — revisions:** Every chart is rebuilt from the current canonical evidence; no append-only historical rendering assumption.

**R9 — ownership:** Presentation success/failure cannot prevent collector evidence persistence. No new canonical rankings, rates, or work types are silently introduced into stored observations.

**R10 — scope:** No repository contents, personal identities, private navigation detail, commit messages/diffs or inferred security findings are exported through a public dashboard.

**R11 — ratio coverage:** An occurrences-per-commit chart reports unknown changed-file coverage and does not divide by zero.

**R12 — semantic labeling:** Snapshot totals, cumulative flows, event counts, individual-day uniques, rolling top-N and unknown values have distinct visible labels.

### 10.2 Suggested implementation waves

**Wave A — reproduce existing charts from current data:** ACT-01…10, DEV-01…07, TRF-01…08, REF-01…05, and OPS-01…04, excluding any unsupported variants. Focus on determinism, missing-state tests, correct colors and accurate traceable numbers.

**Wave B — interactive exploration and comparative views:** ACT-11…16, DEV-08…11, TRF-09…12, REF-06, OPS-05…08, cross-filters and source-linked drill-down. These are presentation-only wherever data already exists.

**Wave C — separately commissioned observation extensions:** additional source families for code/knowledge corpus, development automation, delivery, governance and conformance. Establish privacy, costs, scope and schema contracts first. Do not treat Wave C as pre-authorized collector mutation.

## 11. Open design questions for a later development commission

1. Should the public landing page show all private-repository **aggregates**, or only a visibility-safe approved subset? Follow existing access and source policies; do not leak private paths or content.
2. Which charts are rendered permanently as committed static assets, and which are compiled only for the dashboard or exported on demand?
3. Should one universal project-shade map be stored in derived rendering configuration, and how are aliases/renames bound to stable GitHub repository IDs?
4. Which historical Traffic coverage horizon can actually be retained and corrected for the full repository universe? Do not assume every repo has a daily observation for every period.
5. Which data-quality surfaces are essential on every chart versus available only on drill-down?
6. Should new code/knowledge-size metrics be investigated in an independent source contract, instead of changing the compact evidence collector?
7. What is the correct interactive display for tied daily audience maxima — a deterministic representative bar plus visible co-leaders, or patterned ties?

## 12. Completion statement

**Inventory status: COMPLETE for the known conversational chart families and their distinguishable researched extensions as of 2026-10-18.** The highest-priority product requirement is a **progressive, color-consistent visualization system** whose defaults move from portfolio YTD/monthly, to weekly/project breakdown, to daily/event and individual-repository detail, to evidence and reliability checks.

This file is a **durable Research Result and proposed visualization catalog only**. It does not claim that all named figures were independently implemented, that unavailable sources can be reconstructed, or that a change to GitHub Actions, the collector, or stored observations has been approved.
