# CS-12 — Security, Privacy and Access Boundary

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Consumer:** security/privacy review, future development and research-only Current HOW fan-in.

## Question

What security, privacy and access boundary is actually implemented for public and private repositories, from authenticated GitHub access through persistence into the public Observatory repository?

## Evidence boundary

Inspected:

- root `AGENTS.md`, `README.md`, `SCHEMA.md`;
- workflow permissions and secret injection;
- repository-discovery and Traffic visibility code;
- current public/private registry;
- complete generated file topology;
- current GitHub repository metadata for `github-observatory`.

Not inspected or available:

- value of `OBSERVATORY_TOKEN`;
- token type, scopes or account-side permissions;
- organization policy outside this repository;
- GitHub secret-store configuration;
- private repository contents.

Those remain intentionally outside Product evidence.

## Public Product boundary

The Observatory repository itself is **public**.

Its generated corpus intentionally includes high-level observations about the full discovered owner-repository universe, including repositories whose GitHub visibility is private.

This is explicit in current Product contracts:

- `AGENTS.md` says repository profiles cover the discovered universe regardless of visibility;
- names, descriptions, visibility and other stored high-level observations are intended Observatory surface;
- `SCHEMA.md` defines visibility as normal registry/snapshot metadata.

Therefore the public exposure of private-repository **existence and high-level metadata** is an intentional current behavior, not an accidental leak discovered only by implementation inspection.

## Current private-repository exposure

The public generated registry currently contains private repository records including:

- repository ID;
- name and full name;
- description;
- visibility;
- archived flag;
- first/last seen timestamps;
- present-on-last-scan status.

Per-repository public observation directories for private repositories additionally persist allowed high-level metrics such as:

- repository metadata and timestamps;
- GitHub size;
- exact file count when supportable;
- current canonical commit total;
- stars/forks/subscribers;
- daily canonical activity aggregates;
- language byte snapshots;
- aggregate daily views/clones when authorized.

The corpus does **not** mark these records as secret; their public persistence is the current Product policy.

## Content minimization boundary

Current Product rules explicitly prohibit persistence of:

- repository contents or source files;
- commit messages;
- authors or email addresses;
- diffs/patches;
- changed file paths or directory trees;
- issue/PR bodies;
- workflow logs/artifacts;
- secrets;
- security findings.

Implementation matches this boundary.

The collector may transiently access structures required for permitted aggregates:

- recursive Git tree entries are traversed to count blobs;
- canonical commit history is traversed to aggregate daily commit/change counts.

But the sensitive fine-grained elements are not written to the generated corpus.

This is a clear **data-minimization design**, not merely absence by accident.

## Private navigation/referral boundary

A stricter rule applies to GitHub Traffic detail.

For private repositories:

```text
views/clones aggregate daily metrics
→ may be persisted when authorized

popular referrers / popular paths
→ are not queried for persistence after aggregate success
→ no referrers.csv / paths.csv are stored
```

Complete Product-baseline tree inspection confirms:

- 16 private repositories;
- zero private `traffic/referrers.csv`;
- zero private `traffic/paths.csv`;
- all private repositories do have aggregate views/clones files.

This is a successfully enforced current privacy boundary.

## Public repository Traffic detail

For public repositories, the current Product does persist rolling top-referrer and popular-path snapshots.

Those are public-repository navigation observations, not private repository internals.

Even here the Product stores only the GitHub-returned top-table fields and does not store visitor identities.

## Authentication boundary

Collector API access uses:

```text
OBSERVATORY_TOKEN
```

injected from a GitHub Actions secret.

The token is not stored in the repository or generated corpus.

`GitHubClient` sends it in:

```text
Authorization: Bearer <token>
```

and uses it for both REST and GraphQL.

The exact token value and permission set are intentionally unavailable to repository readers.

Therefore current Product can establish:

> authenticated API access exists and is sufficient to enumerate/observe the current private repository universe.

It cannot establish:

> the token has only the minimum possible scopes.

Least-privilege assessment of the actual secret is **UNKNOWN** from repository evidence.

## Workflow-token vs Observatory-token distinction

The workflows use two different authority channels:

### GitHub workflow token / job permissions

Workflow declares:

```yaml
permissions:
  contents: write
```

This authorizes the workflow to commit/push generated changes to the Observatory repository.

### `OBSERVATORY_TOKEN`

Separate secret passed only to the collector process for source observation.

This separates:

```text
authority to read observed repositories
from
authority to write Observatory output
```

at the configuration surface.

The actual backing credentials may still belong to the same user/account context; repository evidence does not establish their identity relation.

## Secret propagation surface

The secret is injected only into the collector/backfill execution step:

```yaml
env:
  OBSERVATORY_TOKEN: ${{ secrets.OBSERVATORY_TOKEN }}
```

It is not set globally for the whole job in current workflow files.

The Python client does not log the Authorization header.

Errors include URL and message/status, but not the token string by construction.

No current generated file contains an obvious token/secret field.

This reduces accidental secret propagation, though no formal secret-scanning result is part of current Product assurance.

## Public generated-data commit boundary

Workflow stages only:

```text
git add ForestTiger-GH
```

for collector output.

Thus normal automated persistence is constrained to the generated corpus rather than arbitrary working-tree changes.

This is a useful write-boundary property.

However, the job itself has `contents: write` permission to the repository; staging discipline is enforced by the shell script, not by a GitHub path-scoped permission model.

## Access dependency for private Traffic

Current `SCHEMA.md` explicitly states private Traffic availability depends on GitHub access/plan and token authorization.

Unavailable is represented as unavailable, not zero.

Therefore lack of private Traffic can be an authorization/source-availability condition without implying the private repository itself disappeared.

## Public observability vs confidentiality

The current architecture makes a deliberate tradeoff:

```text
private repository contents and navigation detail
→ withheld

private repository existence + high-level operational metadata
→ publicly observable through github-observatory
```

This tradeoff may be acceptable or unacceptable under a future governance decision, but the present Study does not decide that policy question.

The important Current HOW fact is that the boundary is **intentional and encoded in owner documents**.

## Potentially sensitive inference surface

Even without source contents, public high-level metadata can reveal:

- that a private repository exists;
- its project name and description;
- periods of commit activity;
- language composition;
- approximate repository size/file count;
- aggregate Traffic volume;
- creation/push/update timing.

These are permitted current Product observations.

A downstream consumer must not infer hidden source contents from them.

Whether these metadata classes themselves should be considered confidential is a future policy/governance question, not resolved by current Product contracts.

## Failure and leakage boundaries

### Source-family errors

Errors are normalized into status strings and do not intentionally persist API response bodies.

### GitHub API exception messages

`GitHubAPIError` stores:

- status;
- message;
- URL;
- headers.

Exceptions are printed to workflow stderr for family failures.

Current code does not explicitly redact API-provided error messages or response headers before logging.

No current evidence shows a secret-bearing GitHub error response, and GitHub normally does not echo bearer tokens. Still:

> log confidentiality depends partly on upstream error content.

Because workflow logs themselves are not persisted by Observatory, this remains an operational platform/logging boundary rather than generated-corpus exposure.

### GitHub Actions logs

Root Product rules prohibit persisting workflow logs into Observatory.

GitHub Actions itself retains workflow execution logs under platform policy; that external retention is not controlled by generated CSV semantics.

## Current observed topology check

At the baseline:

- Observatory repository: public;
- discovered repositories: 28;
- private: 16;
- public: 12;
- private names/descriptions/high-level metrics: present in public generated corpus by design;
- private referrer/path detail files: none;
- public referrer/path detail files: present for all public repositories;
- no source-content datasets exist in Product tree.

## Negative findings

Within the inspected current Product:

- no repository contents are copied;
- no commit messages/authors/emails are stored;
- no changed paths/directories are stored;
- no issue/PR content is stored;
- no workflow log/artifact corpus is stored;
- no private popular-path/referrer files are present;
- no token value is present in workflow source or generated schema;
- no allow-list of private repositories exists;
- no per-field encryption/access-control layer exists inside the public generated corpus.

## UNKNOWN / limits

- exact `OBSERVATORY_TOKEN` type/scopes are UNKNOWN;
- whether all current public high-level private-repository metadata is acceptable under external confidentiality policy is UNKNOWN;
- GitHub Actions secret/log retention and organization policy are external;
- no formal secret scan or adversarial privacy review was performed;
- no claim is made that aggregated metadata is non-sensitive in every context.

## Current HOW contribution

```text
private/public source repositories
→ authenticated API observation using secret token
→ strict content minimization
→ allowed high-level repository/activity/language/aggregate-Traffic facts
→ extra suppression of private navigation/referral detail
→ public Observatory generated corpus
```

The current security/privacy model is therefore not “private repos are hidden”. It is:

> **private contents are hidden, selected high-level private-repository evidence is intentionally public, and private navigation/referral detail is additionally suppressed.**

## Residue and routes

- consumer-facing clarity about this exposure → CS-13;
- any change to what private metadata is public requires a separate Product/governance decision;
- token least-privilege verification would require account-side evidence outside this repository.

## Reopen / invalidation triggers

Reopen if:

- Observatory repository visibility changes;
- private metadata exposure policy changes;
- `OBSERVATORY_TOKEN` or workflow permission architecture changes;
- private referrer/path data begins to persist;
- new source families are added;
- content-level data is admitted;
- a security/privacy incident supplies materially new evidence.
