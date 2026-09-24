# GitHub Observatory — Workspace Passport

## Engineering Subject

The Engineering Subject is the bounded development of **GitHub Observatory** as a compact, recoverable system for observing GitHub repositories and preserving evidence about their state and activity.

This workspace is the Work plane. It does not replace the repository's current Product, collection, or data-semantics owners. Repository operating rules remain in `AGENTS.md`; stored-field semantics remain in `SCHEMA.md`; canonical collected observations remain under `ForestTiger-GH/`.

## Bootstrap Work Architecture

**Architecture identity:** GO-WA-001  
**Status:** ACCEPTED BOOTSTRAP ARCHITECTURE  
**Formed under:** MADARAII-01 — Engineering Work Architecture Formation  
**Instruction baseline:** ForestTiger-GH/MADARAII main@37d4115d715554625da3123a186f44218fb1f8bc  
**Pre-realization baseline:** ForestTiger-GH/github-observatory main@32cdb7d02bdf2ac5c18f6597319fa62832bb6ab8

This passport owns the bootstrap Engineering Work Architecture. No separate Work Architecture artifact is justified at bootstrap.

### Purpose

Establish one cold-recoverable Development Epoch for bounded Research and development of GitHub Observatory without prematurely creating a larger process, Knowledge, Product, Task, or interaction system.

### Current architecture

Committed now:

- one explicit workspace front door;
- one active Development Epoch;
- one epoch-bound `research/` route;
- one nested `research/results/` route;
- explicit separation between Work/Research material and the repository's current Product/data owners.

No current need justifies a dedicated Work State, Task registry, inbox/outbox, maintained Scientific Knowledge, Target WHAT/HOW, new schema layer, or other speculative workspace structure.

## Current Development Epoch

Exactly one epoch is active:

`_mw/epochs/001-observatory-development/`

Purpose: research and develop GitHub Observatory while preserving the current repository contracts unless a separately commissioned and authorized Work changes them.

Status: **ACTIVE / RESEARCH AND DEVELOPMENT**.

## Current owner routes

| Concern | Current owner / route |
| --- | --- |
| Repository orientation | `README.md` |
| Repository development rules | `AGENTS.md` |
| Stored data semantics | `SCHEMA.md` |
| Collected observations | `ForestTiger-GH/` |
| Repository profiles | `profiles/` |
| Collector implementation | `scripts/` and `.github/workflows/` |
| Workspace passport / Work Architecture | `_mw/AGENTS.md` |
| Active epoch | `_mw/epochs/001-observatory-development/README.md` |
| Research | active epoch `research/` |
| Research / development Results | active epoch `research/results/` |

A Research Result, directory listing, search result, generated view, or actor memory is not a replacement owner for current repository semantics.

## Authority boundaries

- The maintainer/user holds project Authority for repository direction, architecture revision, epoch opening/closure, and admission of changes to current Product or data semantics.
- Actors may inspect, research, draft, or mutate repository state only within commissioned bounded Work.
- Write capability is not Decision Authority.
- Research conclusions and development Results remain candidate inputs until the appropriate owner is explicitly changed.

## Cold-entry route

For material development Work:

1. read repository `AGENTS.md` and the relevant current owner such as `README.md` or `SCHEMA.md`;
2. open this file explicitly;
3. read the active epoch `README.md`;
4. bind the exact Work kind, Subject, Baseline, Authority, expected Result, allowed effects, completion, and stop conditions;
5. when a MADARAII is selected, read its current FOUNDATION, instruction, and matching EXAMPLE;
6. widen into Research or Results only as required.

Do not hydrate or reorganize the whole repository by default.

## Directory map

```text
_mw/
├── AGENTS.md
└── epochs/
    └── 001-observatory-development/
        ├── README.md
        └── research/
            ├── README.md
            └── results/
                └── README.md
```

No additional workspace surface is required at bootstrap.

## Research and Results policy

Research material belongs under the active epoch `research/` route unless a later accepted architecture establishes another owner.

Durable Results of commissioned Research or related development Work belong in `research/results/` unless their Commission binds another owner.

Research and Results may inform later changes, but neither route silently changes `AGENTS.md`, `SCHEMA.md`, collector behavior, stored observations, or other current repository truth.

## Interaction capabilities

Repository-backed human interaction channels are not enabled.

```text
file_backed_inbox = false
file_backed_outbox = false
may_emit_human_message = true through external conversation
may_block_waiting_for_human = false unless explicitly commissioned
```

## Recovery and re-evaluation

Cold recovery route:

`AGENTS.md → _mw/AGENTS.md → active epoch README`.

Selectively revise this architecture when a material new owner, lifecycle, coordination need, interaction channel, persistent Knowledge/Product surface, epoch transition, or routing ambiguity actually appears. Do not design those structures in advance.
