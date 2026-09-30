# CS-02 — Repository Discovery, Identity and Registry Lifecycle

**Work kind:** `CURRENT_STATE_BOUNDED_STUDY` (MADARAII-06)  
**Status:** COMPLETE  
**Product baseline:** `ForestTiger-GH/github-observatory@d0119ec73c79bfd2376b9a197edea8a15b38c811`  
**Consumer:** generated-corpus consumers, later collection/reliability studies and research-only Current HOW fan-in.

## Question

How are repositories discovered, identified, renamed, retained and represented in the current Observatory registry?

## Boundary and evidence

Inspected:

- `list_owned_repositories()`, `repo_dir()`, `update_registry()`;
- `ForestTiger-GH/repositories.csv`;
- current recursive repository tree;
- `SCHEMA.md` registry contract;
- latest collection status showing the current discovered universe.

No historical rename event is present in the inspected generated evidence, so rename behavior below is implementation-established rather than operation-observed.

## Current discovery mechanism

Each collector execution performs discovery before repository-specific collection:

```text
authenticated GET /user/repos
  affiliation=owner
  visibility=all
  sort=full_name
  direction=asc
  per_page=100
  paginated until final short page
→ defensive owner.login == OBSERVATORY_OWNER filter
→ RepoRef(id, name, full_name, description, visibility, archived)
→ registry reconciliation
```

This is **automatic discovery**. There is no repository allow-list in current Product realization.

The owner boundary defaults to `ForestTiger-GH` and may be overridden by `OBSERVATORY_OWNER`.

## Identity model

The stable registry identity is GitHub repository ID:

```text
repository_id = stable registry key
name          = mutable current locator/display component
full_name     = current GitHub full name
```

`repositories.csv` is read into a map keyed by `repository_id`, so a name change does not create a new registry identity by itself.

This implements the useful distinction:

```text
repository identity
≠ repository name
≠ local directory locator
```

## Registry transition on each scan

Before applying newly discovered repositories, every existing registry row is set:

```text
present_on_last_scan = false
```

For each repository returned by the current scan:

- current name/full name/description/visibility/archived are written;
- `first_seen_at` is preserved if the ID already existed, otherwise set to current `observed_at`;
- `last_seen_at` becomes current `observed_at`;
- `present_on_last_scan=true`.

Rows not returned remain in the registry with their prior identity and metadata, but `present_on_last_scan=false`.

Therefore disappearance does **not** delete registry history.

## Rename behavior

If an existing ID has a different prior name:

```text
old_path = ForestTiger-GH/<old_name>
new_path = ForestTiger-GH/<new_name>

if old_path exists and new_path does not exist:
    rename old_path → new_path
```

This preserves the existing per-repository observation directory across ordinary repository renames.

### Collision limit

If both old and new paths already exist, the automatic filesystem rename is not performed. The registry still changes to the new name, and subsequent collection writes to the new-name directory.

No such collision is evidenced in the current corpus. Its behavior beyond the code path is therefore a **code-derived edge condition**, not an observed defect.

## Current registry state at the baseline

`repositories.csv` contains:

| Property | Current observed state |
| --- | ---: |
| registry rows | 28 |
| present on latest scan | 28 |
| public | 12 |
| private | 16 |
| archived | 1 |
| absent on latest scan | 0 |

The archived repository is `Finance-Board`; archived repositories remain in the discovered universe.

First-seen distribution in the durable registry:

- 23 repositories first observed on 2026-09-22;
- 2 on 2026-09-23;
- 1 on 2026-09-24;
- 2 on 2026-09-28.

This supports the current mechanism that new owner repositories enter automatically on later scans.

## Relationship between registry and per-repository observations

The registry is the current discoverability surface for the repository universe.

Per-repository data is physically stored under:

```text
ForestTiger-GH/<current-repository-name>/
```

Not every per-repository CSV repeats `repository_id`; many inherit repository context from their directory. Therefore the rename migration performed by `update_registry()` is materially important to maintaining continuity between stable GitHub identity and mutable physical locator.

The registry itself does not claim that every listed repository has every observation family. Availability is established separately by generated files and `_collection/repository-status.csv`.

## Failure and recovery behavior

Discovery and registry update happen **before** the per-repository try/catch loop.

Consequences:

- if repository discovery fails catastrophically, no per-repository collection begins;
- if registry writing fails, no per-repository collection begins;
- these failures do not receive a same-run `_collection/runs.csv` or per-repository status record because those are written only later in `collect()`;
- external GitHub Actions metadata can still evidence the failed workflow execution.

This is a current observability boundary, not proof that such a failure has occurred in the observed corpus.

## Accepted/documented vs implemented vs observed

### Accepted/documented

The Product contract says repository discovery is automatic, covers repositories owned by the configured owner and does not require a manually maintained allow-list.

### Implemented

The collector implements this with authenticated `/user/repos` pagination plus an owner-login filter and stable repository-ID registry reconciliation.

### Observed

The registry currently contains 28 live rows and shows repositories entering at multiple first-seen dates after Observatory started collecting.

No currently absent repository and no observed rename are available as empirical examples at this cutoff.

## Negative findings

- No manual allow-list was found.
- No separate current registry owner was found.
- No registry row is currently marked absent.
- No evidence of a current repository-ID duplicate exists in the registry.
- No cleanup path deleting historical directories for disappeared repositories was found.

## UNKNOWN / limits

- Behavior when the authenticated token cannot enumerate a private repository is indistinguishable from non-return at this mechanism boundary; the registry would mark a formerly known item absent on that scan.
- Whether GitHub repository IDs remain stable across every transfer/restore edge is a platform question outside this bounded current-mechanism Study.
- Rename-path collision behavior is not empirically exercised in the current corpus.
- Deleted/unreachable local observation directories from historical states were not found, but no broader filesystem history claim is made.

## Current HOW contribution

```text
configured owner account
→ authenticated owner-repository enumeration
→ stable repository_id reconciliation
→ mutable current metadata + presence status
→ name-based physical observation route
→ per-repository collection
```

Registry history is retained when a repository disappears; ordinary name changes attempt to move the physical observation directory while preserving the stable ID lineage.

## Residue and routes

- Date semantics of `first_seen_at`, `last_seen_at` and collection-day attribution → CS-03.
- Snapshot families created after discovery → CS-04.
- Status meaning when a repository source family is unavailable → CS-10.
- Access/privacy implications of enumerating private repositories → CS-12.

## Reopen / invalidation triggers

Reopen if:

- repository discovery endpoint, affiliation/visibility/filter semantics or pagination changes;
- `OBSERVATORY_OWNER` handling changes;
- registry schema/key changes;
- rename/disappearance handling changes;
- generated data moves away from name-based repository directories;
- an observed rename/collision/transfer provides materially new operational evidence.
