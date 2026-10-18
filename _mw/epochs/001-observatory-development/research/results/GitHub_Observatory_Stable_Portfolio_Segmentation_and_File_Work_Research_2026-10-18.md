# GitHub Observatory — Stable Portfolio Segmentation and File-Work Analytics

**Date:** 2026-10-18  
**Status:** Completed research; owner-confirmed target group names and scope, candidate presentation model. No collector, schema, workflow, or product changes.  
**Scope:** 32 observed GitHub repositories in the latest fully closed collection (2026-10-17). DEAEX is a planned future project, not a discovered repository.  
**Outcome:** Seven primary sectors; overlapping program/activity cohorts; orthogonal classification of documentation, code, data and other material; stable colors and comfortable hatching for future graphical reporting.

## 1. Conclusions and permanent analytical architecture

The Observatory should never compress repository ownership, participation in a wider ecosystem and the kind of work performed into one overloaded taxonomy. Its stable visual classification comprises **three orthogonal dimensions**:

1. **Primary sector** — exactly one of **Platforms, Intelligent Architecture & Infrastructure, Cognitive Engineering, Data, Business, Trading, Others** for every currently classified repository. These seven sector names are the desired durable vocabulary.
2. **Activity/program cohort** — zero, one or several memberships: ARMADA, Methodology, Methodology Extended, Cognitive Knowledge Bases, Programming and other specifically admitted views. Membership may span sectors and may cover only qualified material within a repository.
3. **Changed or held file material** — exclusive file-role classes, with additional independent semantic facets such as source language, research/maintained knowledge, or verified CMemory-compatible access.

**Required chart semantics:** Hue indicates primary sector; stable shades distinguish member projects; a restrained, legible pattern (fine diagonal lines or dots) distinguishes measured documentation/knowledge from source-code activity. The pattern must not be applied to an unmeasured statistic or double-count mixed commits.

The seven-sector group assignments can be adopted now in a **derived presentation configuration** using current recorded repository identifiers. Documentation-versus-code activity cannot yet be derived accurately from the existing evidence fields, because the Observatory intentionally stores no file paths, diffs, file contents or commit-file role observations. Any additional file-work measurement requires a separately authorized, bounded, privacy-safe design.

The permanent sector names must not become a fixed repository-discovery allowlist. Repositories are automatically discovered. Unreviewed newcomers are explicitly **PENDING CLASSIFICATION** for visualization, never silently omitted or transformed into synthetic zeros.

## 2. The seven primary sectors

| Sector | Meaning and classification criterion | Observed members | Count | Proposed hue |
| --- | --- | --- | ---: | --- |
| **Platforms** | Independent deployment platforms, application surfaces and client applications | AppDock; Lepilot; stratbox-windows | 3 | Turquoise |
| **Intelligent Architecture & Infrastructure** | General intelligent-system architecture, AI and cognitive-memory/access infrastructure | PROTOS; CMemory | 2 | Green |
| **Cognitive Engineering** | Reusable engineering methodology, special studies, executive method catalogs, method pilots and security engineering | MADAR; MADARAII; MADAR-supplements; CYBERSECLEX; 4 MADARAII pilots; 6 mandat repositories | 14 | Violet |
| **Data** | Data acquisition, normalization, persistent source corpora and source/data interfaces | LIN-Core; Tabularium; Newsflow; lincore-dock-private | 4 | Blue |
| **Business** | Financial/business domain logic and specialized business analysis, except for the separate Trading sector | stratbox; fin-business; COTRA; Finance-Board | 4 | Copper |
| **Trading** | Trading, investing, strategies and investment/capital-management methodology or implementation | Compass; Navigator; LEPILOT_old | 3 | Amber |
| **Others** | Observability and general analytical work not owned by the preceding sectors | github-observatory; analytics | 2 | Slate |
| **TOTAL** | One primary membership for each actually observed repository | **32 unique repositories** | **32** | |

**This is a seven-sector model, not six.** The exact short sector label is **Trading**. The former question of whether Compass, Navigator and LEPILOT_old belong to Platforms, Business or Cognitive Engineering has been resolved by assigning **all three to Trading**. **Lepilot, without “old”, remains Platforms.**

### 2.1 Platforms and future Strategy Box surfaces

AppDock is a general platform for packaging, delivering and operating application worlds. Lepilot is the **current** capital-management application/platform surface. The Strategy Box Windows repository owns a separate application/client implementation; its analytical core lives in a different repository classified under Business.

The Strategy Box product has current and prospective independently owned parts. Planned Web, Android, standalone host/application and other surface roles should be classified by verified responsibility **only after their physical repository exists and has a clear owner**. An architecturally accepted logical host is not automatically an independent repository, deployed implementation or separate observation stream.

**DEAEX — FUTURE ONLY.** DEAEX is intended as a platform/provider for market information and trading/investment activity: aggregation, standardization, controlled publication, presentation and access to upstream results and associated application events. It is **not present in the observed GitHub universe**. If its dedicated repository is created and its role is confirmed, its expected primary group is **Platforms**, with **ARMADA** as a candidate cross-cutting membership. DEAEX must **never** be included as a real repository, a zero-commit record or a counted platform before actual discovery. Earlier descriptions of Lepilot in a legacy trading architecture should not be taken as current definitive product semantics.

### 2.2 Intelligent Architecture & Infrastructure

PROTOS develops foundational intelligent-system architecture; CMemory develops a task-oriented access and composition standard for independently owned knowledge.

**Use of CMemory does not transfer ownership of the source knowledge or the repository into this sector.** A Trading or Business repository may have a CMemory-based knowledge-access surface while retaining its primary Trading or Business group.

### 2.3 Cognitive Engineering

Membership consists of MADAR, MADARAII, MADAR-supplements, CYBERSECLEX, the four distinct MADARAII pilot repositories and the six distinct mandat repositories (analytics, communication, evaluation-challenge, forecast, programming, strategy-decision).

These own engineering method, reusable instructions, work-management methods or defensive security engineering design and assurance. A method's application inside AppDock, Compass or LIN-Core does not make those entire repositories Cognitive Engineering. The presence of a programming-themed mandat does not establish that its file history is implementation code.

**Navigator is not primarily Cognitive Engineering.** Its financial markets, investing, portfolio/risk and capital-management methodology is classified as **Trading** for primary segmentation, although it is also explicitly a member of the cross-cutting Methodology activity cohort.

### 2.4 Data

LIN-Core owns market data acquisition, normalizing and computing source results. Tabularium owns source-faithful financial and institutional disclosures. Newsflow is a data gateway. The LIN-Core dock is a data/connector role, not a generic application platform.

**Important:** Tabularium can contain many financial reports as HTML, Markdown, JSON, XBRL or other data formats. The physical format or documentation volume does not change its primary Data responsibility.

### 2.5 Business

The current Strategy Box core library owns domain analytics, calculation and domain/business logic. This puts **stratbox** in Business, even though it also contains reusable infrastructure and research/knowledge material. Its **stratbox-windows** surface stays in Platforms.

Other members are fin-business, COTRA and Finance-Board. Finance-Board's archived state is a separate lifecycle fact and does not make it Others. COTRA is placed by its business/financial analytical function rather than by generic data transport.

**Compass is not Business in this target taxonomy; it belongs to Trading.**

### 2.6 Trading and Others

**Trading:** Compass owns declarative strategy formulation, compilation, testing/execution and outcomes; Navigator owns investment/trading/financial-methodology knowledge and evaluation; LEPILOT_old represents a historical trading and trade-management application. LEPILOT_old is **not Platforms**, even though current Lepilot is.

**Others:** github-observatory and analytics. New projects of unknown role remain pending until reviewed, not automatically relegated to Others.

## 3. Exhaustive 32-repository reference mapping

Use stable GitHub repository IDs, not spelling alone. The mapping belongs to the derived reporting layer and does not limit discovery.

| Sector | Repository | Stable repository ID |
| --- | --- | ---: |
| Platforms | AppDock | 1252551768 |
| Platforms | Lepilot | 1169689333 |
| Platforms | stratbox-windows | 1279514466 |
| Intelligent Architecture & Infrastructure | PROTOS | 1370061357 |
| Intelligent Architecture & Infrastructure | CMemory | 1419934225 |
| Cognitive Engineering | MADAR | 1341646865 |
| Cognitive Engineering | MADARAII | 1353779596 |
| Cognitive Engineering | MADAR-supplements | 1400540520 |
| Cognitive Engineering | CYBERSECLEX | 1414868554 |
| Cognitive Engineering | madaraii-pilot | 1364938978 |
| Cognitive Engineering | madaraii-pilot-2 | 1365000063 |
| Cognitive Engineering | madaraii-pilot-3 | 1365033294 |
| Cognitive Engineering | madaraii-pilot-4 | 1374262898 |
| Cognitive Engineering | mandat-analytics | 1368735394 |
| Cognitive Engineering | mandat-communication | 1382410031 |
| Cognitive Engineering | mandat-evaluation-challenge | 1391332301 |
| Cognitive Engineering | mandat-forecast | 1380517906 |
| Cognitive Engineering | mandat-programming | 1384350423 |
| Cognitive Engineering | mandat-strategy-decision | 1391331793 |
| Data | LIN-Core | 1124795931 |
| Data | Tabularium | 1375017353 |
| Data | Newsflow | 1382422717 |
| Data | lincore-dock-private | 1169024420 |
| Business | stratbox | 1144531837 |
| Business | fin-business | 1016958961 |
| Business | COTRA | 344921764 |
| Business | Finance-Board | 347684425 |
| Trading | Compass | 1169689579 |
| Trading | Navigator | 1423739485 |
| Trading | LEPILOT_old | 990158962 |
| Others | github-observatory | 1381835317 |
| Others | analytics | 1371796532 |

**Control:** 3 + 2 + 14 + 4 + 4 + 3 + 2 = 32. None is assigned twice. The future platform **DEAEX is outside this table because it has no observed repository ID**. The registry's private/public and archived flags remain independent filter dimensions.

## 4. Overlapping cohort taxonomy

Primary sector answers **what responsibility the repository owns**. An activity cohort answers **which broader subject, program or kind of production it participates in**. A repository may appear in many cohorts; their totals **must not be added to infer a portfolio total**.

| Cohort | Initial membership / coverage | Meaning and boundary |
| --- | --- | --- |
| **ARMADA** | **LIN-Core, Navigator, Compass, Lepilot, LEPILOT_old** | Complete market-information, methodology/research, strategy and investment/capital-management activity chain |
| **Methodology** | **MADAR, MADARAII, CYBERSECLEX, Navigator** | Named owners of systematic engineering, security or financial methodology and organized domain knowledge |
| **Methodology Extended** | Methodology + explicitly selected MADAR-supplements, six mandat repositories and four MADARAII pilots | Optional broader methodology-family analysis; the added projects must be visible in the chart definition |
| **Cognitive Knowledge Bases** | Qualifying knowledge material from Methodology owners **plus qualifying file subsets in AppDock, Compass, LIN-Core, stratbox** and later admitted projects | Cross-sector knowledge activity, not an automatic classification of entire repositories or all Markdown files |
| **Documentation / Knowledge Production** | All repositories, filtered to verified documentation and knowledge-related changes | File-work dimension, not a sector or claim that all documents are cognitively qualified |
| **Programming** | All repositories, filtered to implementation and qualifying executable code | File-work dimension that can be divided by language, repository and primary sector |

### 4.1 ARMADA scope and planned DEAEX

**ARMADA has five current members:** LIN-Core (Data), Navigator (Trading), Compass (Trading), Lepilot (Platforms), LEPILOT_old (Trading).

The broader market-to-usage cycle includes upstream normalized information, computational results, research/evaluation, strategy formulation and execution, and final application/publication/consumption. These roles are analytically linked without collapsing their independent ownership.

**DEAEX is a conditional future ARMADA member, not a sixth current observed member.** A future actual DEAEX platform may aggregate and publish results/data, offer controlled user/provider interfaces and visualize activity, but no claim about present implementation is made. Historical depictions of Lepilot should not overwrite the current repository role or the primary sector.

**Do not add AppDock, Tabularium or any other ecosystem dependency to ARMADA solely because another member uses it.** Membership requires the portfolio owner's explicit semantic decision.

ARMADA reporting should show additive whole-cohort commits and file-touch counts by members, split by their distinct sectors, with a switch for the documentation/code mix and code languages. Legacy vs active application roles are additional filters.

### 4.2 Methodology and Cognitive Knowledge Bases are related but not equal

Methodology focuses on **ownership of methodological knowledge products** and retains four named current members. The related supplemental and pilot projects form a separately named extended option to avoid changing the definition silently.

Cognitive Knowledge Bases is a different **cross-sector analytical view**. It can incorporate structured research, maintained scientific knowledge, engineering knowledge products and source-native domain material, provided qualification exists. In AppDock, Compass, LIN-Core and stratbox, the scope must be a **qualified document or knowledge-file subset**, not every commit of the entire repository.

**CMemory is a method of access to source-native knowledge, not a container that appropriates all source knowledge.** Its presence in one repository does not make every Markdown or JSON file compliant or cognitively indexed.

### 4.3 Knowledge qualification should be staged

| Status | Evidence required | Safe conclusion |
| --- | --- | --- |
| Document candidate | Extension, type or documented prose role | A document exists; may be a note, research, README or generated material |
| Knowledge material | Verified domain/engineering semantic purpose and owner | Substantive knowledge is being maintained or developed |
| Structured knowledge | Stable identity, established relations/structure or source-native semantic format | The material is eligible for qualified navigation and formalization |
| Qualified cognitive access | Verified task-specific access/composition model, source bindings, operations, recipes and checked behavior | Declared CMemory-compatible access for a bounded scope, **not** universal semantic correctness |

A Markdown file is not automatically a knowledge base. An example written in Python inside Markdown is not a changed Python implementation file. An XBRL schema has explicit native semantic relationships but does not automatically constitute a CMemory installation. Preserve unknown and unqualified status rather than guessing positive conformity.

## 5. File-work classification: physical kind versus semantic role

### 5.1 Exclusive physical-kind categories for additive accounting

| File-work kind | Concept | Notable exceptions |
| --- | --- | --- |
| Documentation / knowledge | Readable research, articles, maintained manuals and knowledge documents | Markdown may carry code examples or generated notes; not all docs are qualified cognitive knowledge |
| Implementation code | Executable source, libraries, scripts and qualified tests | Executable test code is code with a test-role facet |
| Structured data | CSV, JSON, XBRL, XML and other records **when used as data** | JSON may instead be configuration, schema, access model or implementation resource |
| Configuration / automation | CI declarations, build packaging, manifests, environment descriptions | Some scripts here are executable code; classify by actual role |
| Assets / binary | Images, office documents, PDFs, archives and other non-source artifacts | PDF/XLSX can contain domain knowledge; keep semantic knowledge and physical format separate |
| Other / unknown | Unrecognized, ambiguous, incomplete | Must remain explicit; a missing classification is not an observed zero |

This primary kind must be **mutually exclusive for each file occurrence** to support sums. Additional facets may overlap: language, implementation-vs-test, research-vs-maintained knowledge, schema vs data, generated/vendor status, CMemory access qualification, scientific/domain roles.

**Physical format is not semantic role**. The same extension can be code, data, documentation or configuration in different contexts. A file touched repeatedly counts as repeated file-change occurrences; it is not a distinct file for each touch.

### 5.2 Existing GitHub language bytes are not historical code-vs-doc activity

The currently stored language snapshots are **GitHub Linguist language-byte observations**, not per-commit changes, documentation lines, code LOC or language-specific commit counts. GitHub Linguist's default treatment filters out many documentation, prose, generated and vendored sources from language statistics and supports classification overrides. Therefore a repository containing hundreds of knowledge documents can report little or no programming-language bytes without implying absence of documentation activity.

**The current Observatory cannot correctly infer daily documentation updates from its activity or languages series alone.** It stores no file paths, diffs, source contents or commit-level file inventory. Inferring activity kind from repository names or total file count would create false evidence.

### 5.3 Accurate aggregation and mixed-commit handling

Example: one canonical commit changes three documentation files and two Python source files.

- File-change occurrence partition: documentation = **3**, code = **2**, total = **5**. This is additive when the classifier and file list are complete.
- Commits touching documentation = **1**, commits touching code = **1**. These categories **overlap** and **must not be added to claim two commits**.
- A mutually exclusive commit-type series can place the single commit in a **mixed code + documentation** bucket, preserving exactly one counted commit.

Suggested metrics and safe usage:

| Metric | Chart unit | Across kinds | Additional notes |
| --- | --- | --- | --- |
| Existing daily commits | Count of canonical commits | Additive **only** after mutually exclusive commit bucketing | Mixed commits must be one bucket |
| Changed-file occurrences by primary kind | File-change occurrences | **Additive** with complete, exclusive categorization | Repeated changes to the same file count repeatedly |
| Commits touching kind | Count of commits that touch at least one file of kind | **Non-additive** across kinds | Useful to describe involvement, not to stack into total commits |
| Current files by kind | Complete Git tree blob count | Additive if snapshot complete | Snapshot stock; not new files per day |
| Programming-language bytes | Language bytes at observed snapshot | Conditional on detection policy | Not LOC, new code lines or documentation work |
| Verified cognitive knowledge units | Units meeting a semantic qualification contract | Depends on unit identity and duplication rules | Not estimable from file extensions alone |
| Daily unique viewers/cloners | Repository/day uniques | **Not additive** across repositories or days | This existing Observatory rule is unchanged |

## 6. Future visual design: hues for sectors, gentle patterns for material

The user's explicitly desired graphical enhancement is **two-dimensional coding without visual overload**:

- **Base hue:** stable seven-sector color. 
- **Project shade:** fixed shade within the corresponding sector hue, consistent between monthly, ISO-weekly, daily and ranking charts.
- **Pattern:** soft fine diagonal lines or sparse dots for documentation/knowledge activity; code as solid fill or a faint alternate texture; mixed as a clearly explained blended pattern; unknown as neutral unfilled/outlined.
- **Labels/tooltips:** full group, project, measured kind, unit, source cut, missing status and classifier version. Patterns should remain legible for color-vision deficiencies and not flicker or form visual moiré.

Do **not** use aggressive contrasting stripes across a 40-week × 32-project dense chart. On high-level charts limit patterns to documentation versus code with mixed/unknown separately disclosed; on a detailed panel, allow data/configuration distinctions. Provide a chart/table toggle and hover detail.

### 6.1 Three honest rendering variants

**Variant A — file-touch chart (preferred when measured):** X = UTC day, ISO week or calendar month; Y = exclusive changed-file occurrences. Stacked colors = sectors/projects; patterns = documentation, code, data/config and unknown. Additive if the source is complete.

**Variant B — mutually exclusive commit-type chart:** X = period; Y = canonical commits. Buckets = documentation-only, code-only, mixed, other-only, unknown; colors = sector/project; patterns = buckets. Never add overlapping doc-touch and code-touch commit counts.

**Variant C — preserve the already available commit count chart, plus a separate synchronized document/code composition strip.** This avoids inventing file-work splits for today's data and retains an uncluttered portfolio overview.

**Forbidden:** draw a patterned documentation share on top of currently recorded total commits using present-day language bytes or guessed Markdown fractions. An aesthetic convention cannot justify fabricated statistics.

### 6.2 Required drill-down sequence

1. **Portfolio:** year-to-date monthly grouped bars, weekly grouped bars, recent daily activity; seven base colors.
2. **Sector and project:** monthly/weekly repository shades, project ranking and repository × week heatmap.
3. **Cross-sector activity:** ARMADA and Methodology as independent cohorts; also Cognitive Knowledge Bases and Programming where qualified.
4. **Material:** documentation/code/data/config/unknown by sector and project using hatches once measured.
5. **Language and knowledge depth:** code languages, research/maintained knowledge distinction, qualified cognitive access, corpus change and completeness.
6. **Evidence:** observation coverage, classification version, unknown/ambiguous files and Git history revision semantics.

The same fixed hierarchy applies to a README graphic overview, an interactive dashboard and any downloadable rendered report. The visual rendering layer must be reproducible from authorized observations.

## 7. Implementation proposal without premature collector changes

**Immediate presentation-only step:** adopt an owner-reviewed versioned sector/cohort mapping keyed by stable repository IDs, and use it to rebuild existing charts. No source-file inspection or new collection is required for repository-level and whole-cohort classification.

**New file-work metric step, if separately authorized:** run a bounded classification of changed file types or complete tree contents with tested exactness. Observe file identities transiently under access controls and retain only explicitly permitted aggregate facts, coverage and provenance. Decide first whether this belongs in a new source family or a separate private derived analytic job. Preserve the current prohibition on persisting repository contents, paths, authors, raw changes and patches. Handle Git API pagination, truncated results, merges, rebases and uncertain classification. Historical data is not guaranteed to be reconstructible.

**Qualified knowledge step, if separately authorized:** distinguish source-native documents and forms from semantic knowledge roles and verified cognitive-access contracts. Do not conflate CMemory-compatible task routing with ownership, full corpus coverage or domain validity.

**Rendering step:** deterministic SVG and/or static dashboard views use one tested metric layer; evidence collection must complete and remain safe even if rendering fails.

### 7.1 Proposed configuration concept

Each repository assignment should record stable repository ID, assigned primary sector, effective-from date, taxonomy edition, review status and stable project color-shade token. Secondary cohorts use explicit repository ID sets and optional qualified file-subset predicates. A future-project record may contain **DEAEX** with planned status but **no repository ID or observed metrics**.

New discoveries cause a classification review request rather than an undocumented new sector or a missing data point. Group names are frozen by design, assignments change only under clear ownership evidence and a versioned decision.

### 7.2 Acceptance checks

| Test | Expected result |
| --- | --- |
| Complete owner census | 32 observed IDs, exactly 32 primary assignments |
| Sector counts | Platforms 3; Intelligent A&I 2; Cognitive Engineering 14; Data 4; Business 4; Trading 3; Others 2 |
| Critical corrections | Lepilot in Platforms; LEPILOT_old, Navigator and Compass in Trading |
| Strategy Box split | Core in Business, actual Windows surface in Platforms, proposed uncreated surfaces not counted |
| ARMADA | Exactly five present repositories; future DEAEX is not included in observed totals |
| Methodology | Four named core method owners, with explicit extended-family option |
| CMemory | Cross-repository compliant-knowledge claims only with independently checked qualification |
| Financial and technical cohorts | No duplication when adding overlapping ARMADA and Methodology graphs |
| File-kind source readiness | Present unavailable state, not inferred historic documentation shares |
| Mixed commits | One commit touching docs and code is not counted twice in a stacked commit chart |
| Taxonomy color | Seven distinguishable hues; stable repository shades across time resolutions |
| Documentation style | Readable low-contrast stripes/dots; never used without measured evidence |
| GitHub privacy | No persisted raw file paths/contents/diffs; private aggregate publishing policy enforced |
| Missingness | Unknown does not become zero, and planned repositories cannot acquire synthetic metrics |

## 8. Decisions, limits and next implementation gates

**Settled target vocabulary:** seven primary sectors with the exact short name **Trading**. **Compass, Navigator and LEPILOT_old are Trading; current Lepilot is Platforms.** This resolves the initial ambiguous assignments. DEAEX is a planned future Platforms and potentially ARMADA project but not yet observed. The seven-sector map is exhaustive for the 32-repository evaluated universe.

**Independent activity grouping:** ARMADA has five currently named members; Methodology has four named core members, plus a separately disclosed wider family; Cognitive Knowledge Bases is a qualified cross-sector file/knowledge view; Programming is a cross-sector file/code view. These are not competing primary group memberships.

**Future desirable measurement:** differentiate documentation and code on charts using calm patterns and a stable color hierarchy. An aggregate-only measurement and its reporting semantics must be designed and authorized before actual doc/code shares are graphed.

**Open before implementation:** decide classification registry ownership/editions, treatment of future repositories and renames, completeness and privacy of any file-role observation, historical backfill limits, mixed-commit accounting, knowledge qualification and an accessibility-tested texture palette. None of these decisions alters the current collector merely by appearing in this research.

**Research conclusion:** the durable Observatory classification is **one primary sector × many optional activity cohorts × measured file-kind/semantic facets**. This supports progressively detailed, consistent automated reports without confusing repository identity, software implementation, documentation, native knowledge and CMemory-qualified cognitive access.

## External references

- GitHub Linguist, *How Linguist works* — describes why documentation, prose and generated/vendor files may be excluded from language-byte statistics; supports the warning that languages snapshots cannot recover documentation activity: https://github.com/github-linguist/linguist/blob/main/docs/how-linguist-works.md
- GitHub Linguist, *Overrides* — describes how language detectability and documentation/generated/vendor overrides alter the repository language statistics; supports keeping raw language bytes separate from file-work semantics: https://github.com/github-linguist/linguist/blob/main/docs/overrides.md
