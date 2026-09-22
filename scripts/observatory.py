from __future__ import annotations

import csv
import datetime as dt
import json
import os
import pathlib
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable

from github_api import GitHubAPIError, GitHubClient


OWNER = os.environ.get("OBSERVATORY_OWNER", "ForestTiger-GH")
DATA_ROOT = pathlib.Path(os.environ.get("OBSERVATORY_DATA_ROOT", OWNER))
STATE_PATH = pathlib.Path(os.environ.get("OBSERVATORY_STATE_PATH", ".observatory/state.json"))
UTC = dt.timezone.utc

REPOSITORY_FIELDS = [
    "observation_date_utc", "observed_at", "repository_id", "name", "full_name",
    "visibility", "archived", "fork", "created_at", "updated_at", "pushed_at",
    "size_kb", "default_branch", "default_branch_commits", "stars", "forks", "subscribers",
]
ACTIVITY_FIELDS = [
    "activity_date_utc", "commits", "changed_file_occurrences",
    "commits_with_unknown_changed_files", "last_observed_at",
]
LANGUAGE_FIELDS = ["observation_date_utc", "observed_at", "language", "bytes"]
TRAFFIC_DAILY_FIELDS = ["traffic_date_utc", "count", "uniques", "last_observed_at"]
REFERRER_FIELDS = ["observation_date_utc", "observed_at", "referrer", "count", "uniques"]
PATH_FIELDS = ["observation_date_utc", "observed_at", "path", "title", "count", "uniques"]
REGISTRY_FIELDS = [
    "repository_id", "name", "full_name", "visibility", "archived", "default_branch",
    "first_seen_at", "last_seen_at", "present_on_last_scan",
]
STATUS_FIELDS = [
    "observation_date_utc", "observed_at", "repository_id", "repository_name",
    "metadata_status", "languages_status", "activity_status", "traffic_status",
]
RUN_FIELDS = [
    "observation_date_utc", "started_at", "finished_at", "mode",
    "repositories_seen", "repositories_succeeded", "repositories_with_errors",
]


@dataclass
class RepoRef:
    id: str
    name: str
    full_name: str
    visibility: str
    archived: bool
    default_branch: str | None


def utc_now() -> dt.datetime:
    return dt.datetime.now(UTC).replace(microsecond=0)


def iso_z(value: dt.datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def read_csv(path: pathlib.Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: pathlib.Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def upsert_rows(
    path: pathlib.Path,
    fieldnames: list[str],
    new_rows: Iterable[dict[str, Any]],
    key_fields: tuple[str, ...],
    sort_fields: tuple[str, ...] | None = None,
) -> None:
    combined: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in read_csv(path):
        combined[tuple(str(row.get(key, "")) for key in key_fields)] = row
    for row in new_rows:
        combined[tuple(str(row.get(key, "")) for key in key_fields)] = row
    rows = list(combined.values())
    sort_fields = sort_fields or key_fields
    rows.sort(key=lambda row: tuple(str(row.get(field, "")) for field in sort_fields))
    write_csv(path, fieldnames, rows)


def replace_partition(
    path: pathlib.Path,
    fieldnames: list[str],
    partition_field: str,
    partition_value: str,
    new_rows: Iterable[dict[str, Any]],
    sort_fields: tuple[str, ...],
) -> None:
    rows = [row for row in read_csv(path) if row.get(partition_field) != partition_value]
    rows.extend(new_rows)
    rows.sort(key=lambda row: tuple(str(row.get(field, "")) for field in sort_fields))
    write_csv(path, fieldnames, rows)


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"version": 1, "repositories": {}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def list_owned_repositories(client: GitHubClient) -> list[RepoRef]:
    repos = client.get_paginated(
        "/user/repos",
        {
            "affiliation": "owner",
            "visibility": "all",
            "sort": "full_name",
            "direction": "asc",
            "per_page": 100,
        },
    )
    result: list[RepoRef] = []
    for repo in repos:
        if str(repo.get("owner", {}).get("login", "")).casefold() != OWNER.casefold():
            continue
        visibility = repo.get("visibility") or ("private" if repo.get("private") else "public")
        result.append(
            RepoRef(
                id=str(repo["id"]),
                name=repo["name"],
                full_name=repo["full_name"],
                visibility=visibility,
                archived=bool(repo.get("archived")),
                default_branch=repo.get("default_branch"),
            )
        )
    return result


def repo_dir(repo: RepoRef) -> pathlib.Path:
    return DATA_ROOT / repo.name


def update_registry(repos: list[RepoRef], observed_at: str) -> None:
    path = DATA_ROOT / "repositories.csv"
    existing = {row["repository_id"]: row for row in read_csv(path)}
    for row in existing.values():
        row["present_on_last_scan"] = "false"

    for repo in repos:
        prior = existing.get(repo.id, {})
        old_name = prior.get("name")
        if old_name and old_name != repo.name:
            old_path = DATA_ROOT / old_name
            new_path = DATA_ROOT / repo.name
            if old_path.exists() and not new_path.exists():
                old_path.rename(new_path)
        existing[repo.id] = {
            "repository_id": repo.id,
            "name": repo.name,
            "full_name": repo.full_name,
            "visibility": repo.visibility,
            "archived": str(repo.archived).lower(),
            "default_branch": repo.default_branch or "",
            "first_seen_at": prior.get("first_seen_at") or observed_at,
            "last_seen_at": observed_at,
            "present_on_last_scan": "true",
        }

    rows = sorted(existing.values(), key=lambda row: (row.get("name", "").casefold(), row["repository_id"]))
    write_csv(path, REGISTRY_FIELDS, rows)


def repository_detail(client: GitHubClient, repo: RepoRef) -> dict[str, Any]:
    return client.get(f"/repos/{OWNER}/{repo.name}").data


GRAPHQL_REPO_HEAD = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef {
      name
      target {
        ... on Commit {
          oid
          history(first: 1) { totalCount }
        }
      }
    }
  }
}
"""

GRAPHQL_HISTORY_PAGE = """
query($owner: String!, $name: String!, $after: String, $since: GitTimestamp, $until: GitTimestamp) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 100, after: $after, since: $since, until: $until) {
            nodes {
              oid
              committedDate
              changedFilesIfAvailable
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }
  }
}
"""


def get_head_and_total(client: GitHubClient, repo: RepoRef) -> tuple[str | None, int | None]:
    data = client.graphql(GRAPHQL_REPO_HEAD, {"owner": OWNER, "name": repo.name})
    repository = data.get("repository")
    if not repository or not repository.get("defaultBranchRef"):
        return None, 0
    target = repository["defaultBranchRef"].get("target") or {}
    return target.get("oid"), (target.get("history") or {}).get("totalCount")


def iter_history(
    client: GitHubClient,
    repo: RepoRef,
    since: str | None = None,
    until: str | None = None,
):
    cursor = None
    while True:
        data = client.graphql(
            GRAPHQL_HISTORY_PAGE,
            {"owner": OWNER, "name": repo.name, "after": cursor, "since": since, "until": until},
        )
        repository = data.get("repository")
        if not repository or not repository.get("defaultBranchRef"):
            return
        target = repository["defaultBranchRef"].get("target") or {}
        history = target.get("history") or {"nodes": [], "pageInfo": {"hasNextPage": False}}
        for node in history.get("nodes") or []:
            yield node
        page_info = history.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")


def aggregate_commits(nodes: Iterable[dict[str, Any]]) -> dict[str, dict[str, int]]:
    aggregated: dict[str, dict[str, int]] = defaultdict(
        lambda: {"commits": 0, "changed_file_occurrences": 0, "commits_with_unknown_changed_files": 0}
    )
    for node in nodes:
        committed_date = node.get("committedDate")
        if not committed_date:
            continue
        row = aggregated[committed_date[:10]]
        row["commits"] += 1
        changed = node.get("changedFilesIfAvailable")
        if changed is None:
            row["commits_with_unknown_changed_files"] += 1
        else:
            row["changed_file_occurrences"] += int(changed)
    return aggregated


def write_full_activity(repo: RepoRef, aggregated: dict[str, dict[str, int]], observed_at: str) -> None:
    rows = [
        {"activity_date_utc": day, **values, "last_observed_at": observed_at}
        for day, values in sorted(aggregated.items())
    ]
    write_csv(repo_dir(repo) / "activity.csv", ACTIVITY_FIELDS, rows)


def add_incremental_activity(repo: RepoRef, aggregated: dict[str, dict[str, int]], observed_at: str) -> None:
    path = repo_dir(repo) / "activity.csv"
    existing = {row["activity_date_utc"]: row for row in read_csv(path)}
    for day, values in aggregated.items():
        prior = existing.get(
            day,
            {
                "activity_date_utc": day,
                "commits": "0",
                "changed_file_occurrences": "0",
                "commits_with_unknown_changed_files": "0",
                "last_observed_at": observed_at,
            },
        )
        prior["commits"] = str(int(prior.get("commits") or 0) + values["commits"])
        prior["changed_file_occurrences"] = str(
            int(prior.get("changed_file_occurrences") or 0) + values["changed_file_occurrences"]
        )
        prior["commits_with_unknown_changed_files"] = str(
            int(prior.get("commits_with_unknown_changed_files") or 0)
            + values["commits_with_unknown_changed_files"]
        )
        prior["last_observed_at"] = observed_at
        existing[day] = prior
    write_csv(path, ACTIVITY_FIELDS, sorted(existing.values(), key=lambda row: row["activity_date_utc"]))


def incremental_activity(
    client: GitHubClient,
    repo: RepoRef,
    old_head: str | None,
    new_head: str | None,
    observed_at: str,
) -> str:
    if new_head is None:
        return "no_default_branch"
    if old_head == new_head:
        return "unchanged"
    if old_head is None:
        yesterday = utc_now().date() - dt.timedelta(days=1)
        nodes = list(
            iter_history(
                client,
                repo,
                since=f"{yesterday.isoformat()}T00:00:00Z",
                until=f"{yesterday.isoformat()}T23:59:59Z",
            )
        )
        add_incremental_activity(repo, aggregate_commits(nodes), observed_at)
        return "bootstrap_previous_utc_day"

    new_nodes: list[dict[str, Any]] = []
    found_old_head = False
    for node in iter_history(client, repo):
        if node.get("oid") == old_head:
            found_old_head = True
            break
        new_nodes.append(node)

    if not found_old_head:
        write_full_activity(repo, aggregate_commits(new_nodes), observed_at)
        return "history_rebuilt_after_rewrite"

    add_incremental_activity(repo, aggregate_commits(new_nodes), observed_at)
    return "updated"


def collect_repository_snapshot(
    client: GitHubClient,
    repo: RepoRef,
    observed_at: str,
    observation_date: str,
    total_commits: int | None,
) -> None:
    detail = repository_detail(client, repo)
    row = {
        "observation_date_utc": observation_date,
        "observed_at": observed_at,
        "repository_id": str(detail["id"]),
        "name": detail["name"],
        "full_name": detail["full_name"],
        "visibility": detail.get("visibility") or ("private" if detail.get("private") else "public"),
        "archived": str(bool(detail.get("archived"))).lower(),
        "fork": str(bool(detail.get("fork"))).lower(),
        "created_at": detail.get("created_at") or "",
        "updated_at": detail.get("updated_at") or "",
        "pushed_at": detail.get("pushed_at") or "",
        "size_kb": detail.get("size", ""),
        "default_branch": detail.get("default_branch") or "",
        "default_branch_commits": "" if total_commits is None else total_commits,
        "stars": detail.get("stargazers_count", ""),
        "forks": detail.get("forks_count", ""),
        "subscribers": detail.get("subscribers_count", ""),
    }
    upsert_rows(repo_dir(repo) / "repository.csv", REPOSITORY_FIELDS, [row], ("observation_date_utc",))


def collect_languages(client: GitHubClient, repo: RepoRef, observed_at: str, observation_date: str) -> None:
    data = client.get(f"/repos/{OWNER}/{repo.name}/languages").data
    if not isinstance(data, dict):
        raise RuntimeError("Unexpected languages response")
    rows = [
        {
            "observation_date_utc": observation_date,
            "observed_at": observed_at,
            "language": language,
            "bytes": byte_count,
        }
        for language, byte_count in sorted(data.items(), key=lambda item: item[0].casefold())
    ]
    replace_partition(
        repo_dir(repo) / "languages.csv",
        LANGUAGE_FIELDS,
        "observation_date_utc",
        observation_date,
        rows,
        ("observation_date_utc", "language"),
    )


def collect_traffic(client: GitHubClient, repo: RepoRef, observed_at: str, observation_date: str) -> str:
    base = f"/repos/{OWNER}/{repo.name}/traffic"
    try:
        views = client.get(f"{base}/views", {"per": "day"}).data
        clones = client.get(f"{base}/clones", {"per": "day"}).data
    except GitHubAPIError as exc:
        if exc.status in {403, 404}:
            return f"unavailable_http_{exc.status}"
        raise

    view_rows = [
        {
            "traffic_date_utc": item["timestamp"][:10],
            "count": item["count"],
            "uniques": item["uniques"],
            "last_observed_at": observed_at,
        }
        for item in (views or {}).get("views", [])
    ]
    clone_rows = [
        {
            "traffic_date_utc": item["timestamp"][:10],
            "count": item["count"],
            "uniques": item["uniques"],
            "last_observed_at": observed_at,
        }
        for item in (clones or {}).get("clones", [])
    ]
    upsert_rows(repo_dir(repo) / "traffic" / "views.csv", TRAFFIC_DAILY_FIELDS, view_rows, ("traffic_date_utc",))
    upsert_rows(repo_dir(repo) / "traffic" / "clones.csv", TRAFFIC_DAILY_FIELDS, clone_rows, ("traffic_date_utc",))

    # Do not persist private navigation/referral details.
    if repo.visibility != "public":
        return "ok_aggregate_only_private"

    try:
        referrers = client.get(f"{base}/popular/referrers").data
        paths = client.get(f"{base}/popular/paths").data
    except GitHubAPIError as exc:
        if exc.status in {403, 404}:
            return f"aggregate_ok_detail_unavailable_http_{exc.status}"
        raise

    replace_partition(
        repo_dir(repo) / "traffic" / "referrers.csv",
        REFERRER_FIELDS,
        "observation_date_utc",
        observation_date,
        [
            {
                "observation_date_utc": observation_date,
                "observed_at": observed_at,
                "referrer": item.get("referrer", ""),
                "count": item.get("count", ""),
                "uniques": item.get("uniques", ""),
            }
            for item in referrers or []
        ],
        ("observation_date_utc", "referrer"),
    )
    replace_partition(
        repo_dir(repo) / "traffic" / "paths.csv",
        PATH_FIELDS,
        "observation_date_utc",
        observation_date,
        [
            {
                "observation_date_utc": observation_date,
                "observed_at": observed_at,
                "path": item.get("path", ""),
                "title": item.get("title", ""),
                "count": item.get("count", ""),
                "uniques": item.get("uniques", ""),
            }
            for item in paths or []
        ],
        ("observation_date_utc", "path"),
    )
    return "ok"


def backfill_activity(
    client: GitHubClient,
    repo: RepoRef,
    observed_at: str,
) -> tuple[str, str | None, int | None]:
    head, total = get_head_and_total(client, repo)
    if head is None:
        write_full_activity(repo, {}, observed_at)
        return "no_default_branch", None, total
    write_full_activity(repo, aggregate_commits(iter_history(client, repo)), observed_at)
    return "full_history", head, total


def status_for_error(exc: Exception) -> str:
    if isinstance(exc, GitHubAPIError):
        return f"error_http_{exc.status or 'unknown'}"
    return f"error_{type(exc).__name__}"


def collect(mode: str) -> int:
    token = os.environ.get("OBSERVATORY_TOKEN")
    if not token:
        print("OBSERVATORY_TOKEN is not set", file=sys.stderr)
        return 2

    client = GitHubClient(token)
    started = utc_now()
    observed_at = iso_z(started)
    observation_date = started.date().isoformat()
    state = load_state()
    repo_state: dict[str, Any] = state.setdefault("repositories", {})

    repos = list_owned_repositories(client)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    update_registry(repos, observed_at)

    status_rows: list[dict[str, Any]] = []
    succeeded = 0
    with_errors = 0

    for index, repo in enumerate(repos, start=1):
        print(f"[{index}/{len(repos)}] {repo.full_name}")
        repo_dir(repo).mkdir(parents=True, exist_ok=True)
        statuses = {
            "metadata_status": "not_run",
            "languages_status": "not_run",
            "activity_status": "not_run",
            "traffic_status": "not_run",
        }
        head: str | None = None
        total: int | None = None

        try:
            if mode == "backfill":
                statuses["activity_status"], head, total = backfill_activity(client, repo, observed_at)
            else:
                head, total = get_head_and_total(client, repo)
                old_head = (repo_state.get(repo.id) or {}).get("last_head_oid")
                statuses["activity_status"] = incremental_activity(client, repo, old_head, head, observed_at)
        except Exception as exc:
            statuses["activity_status"] = status_for_error(exc)
            print(f"  activity: {exc}", file=sys.stderr)

        try:
            collect_repository_snapshot(client, repo, observed_at, observation_date, total)
            statuses["metadata_status"] = "ok"
        except Exception as exc:
            statuses["metadata_status"] = status_for_error(exc)
            print(f"  metadata: {exc}", file=sys.stderr)

        try:
            collect_languages(client, repo, observed_at, observation_date)
            statuses["languages_status"] = "ok"
        except Exception as exc:
            statuses["languages_status"] = status_for_error(exc)
            print(f"  languages: {exc}", file=sys.stderr)

        try:
            statuses["traffic_status"] = collect_traffic(client, repo, observed_at, observation_date)
        except Exception as exc:
            statuses["traffic_status"] = status_for_error(exc)
            print(f"  traffic: {exc}", file=sys.stderr)

        if head is not None:
            repo_state[repo.id] = {
                "name": repo.name,
                "last_head_oid": head,
                "last_seen_at": observed_at,
            }

        if any(value.startswith("error_") for value in statuses.values()):
            with_errors += 1
        else:
            succeeded += 1

        status_rows.append(
            {
                "observation_date_utc": observation_date,
                "observed_at": observed_at,
                "repository_id": repo.id,
                "repository_name": repo.name,
                **statuses,
            }
        )

    state["last_run_at"] = observed_at
    state["last_mode"] = mode
    save_state(state)

    upsert_rows(
        DATA_ROOT / "_collection" / "repository-status.csv",
        STATUS_FIELDS,
        status_rows,
        ("observation_date_utc", "repository_id"),
        ("observation_date_utc", "repository_name"),
    )

    finished = utc_now()
    upsert_rows(
        DATA_ROOT / "_collection" / "runs.csv",
        RUN_FIELDS,
        [{
            "observation_date_utc": observation_date,
            "started_at": observed_at,
            "finished_at": iso_z(finished),
            "mode": mode,
            "repositories_seen": len(repos),
            "repositories_succeeded": succeeded,
            "repositories_with_errors": with_errors,
        }],
        ("observation_date_utc", "mode"),
        ("observation_date_utc", "mode"),
    )

    print(
        f"Completed {mode}: repos={len(repos)} succeeded={succeeded} with_errors={with_errors} "
        f"duration={(finished - started).total_seconds():.1f}s"
    )
    # Per-repository failures are availability observations; universe/auth failures still fail.
    return 0
