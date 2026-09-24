# GitHub Observatory: расширенная система ежедневных метрик

**Дата:** 2026-09-24  
**Объект:** `ForestTiger-GH/github-observatory`  
**Статус:** Research Result / предложение для последующего проектирования  
**Изменения текущего collector/schema:** не выполнялись

---

## 1. Резюме

Текущий GitHub Observatory уже хорошо наблюдает три слоя:

- текущее состояние репозитория;
- каноническую commit-активность;
- GitHub Traffic.

Следующий качественный шаг — наблюдать **жизненный цикл работы**, а не только stock репозитория и число commits. Наибольшую ценность дадут:

1. изменения содержимого: `additions`, `deletions`, churn, merge/non-merge, human/automation;
2. Pull Requests: opened/closed/merged, размер, cycle time, review latency;
3. Issues: поток, backlog, возраст backlog, close time;
4. GitHub Actions: runs, jobs, failures, runtime, queue time, reruns, cache/artifact usage и при возможности billing;
5. Releases и Deployments: поставка, release cadence, deployment flow, корректные delivery metrics;
6. Governance: branch protection, workflows, community profile и конфигурационный drift;
7. виды работ: code / tests / docs-spec / research / data / automation / configuration;
8. портфельные агрегаты: активные repositories, концентрация работы, распределение по ролям repositories и видам работ;
9. observability самого collector: API calls, retries, rate limit, completeness, freshness, duration.

Главная архитектурная идея:

```text
GitHub API / Git data
        ↓
transient processing
        ↓
CANONICAL OBSERVATIONS
        ↓
DERIVED ANALYTICS
        ↓
dashboard / README / Pages
```

Observatory стоит сохранить как **evidence system**. Производные показатели нужно отделить от канонического collection layer.

---

# 2. Текущий baseline

На текущем состоянии репозитория Observatory сохраняет:

- registry repositories;
- repository metadata snapshot;
- `size_kb`;
- точное число blob-файлов, когда Git tree не truncated;
- число canonical commits;
- stars / forks / subscribers;
- language bytes;
- commit activity по UTC-дням;
- changed-file occurrences;
- views / clones;
- rolling referrers / popular paths;
- статусы collection и runs.

В текущем `scripts/observatory.py` commit history перечитывается целиком для каждого repository на каждом запуске. Это обеспечивает сильную семантику после merge/rebase/history rewrite, но стоимость растёт вместе со всей историей.

Существующая архитектурная граница сильная и её стоит сохранить: Observatory не должен превращаться в копию repository contents. Текущие правила исключают сохранение source files, commit messages, author identities, diffs/patches, changed paths, issue/PR bodies, workflow logs, artifacts, secrets и security findings.

---

# 3. Временная модель: T / T−1

Предыдущее исследование Observatory уже сформулировало удобную модель:

```text
T   = current observation / snapshot
T−1 = latest fully completed UTC day
```

Её стоит распространить на новые семейства.

## Snapshots — T

- repository state;
- languages;
- workflow inventory;
- open PR backlog;
- open issue backlog;
- Actions cache usage;
- branch/protection state;
- community-profile state;
- governance configuration;
- current release/assets state;
- collection run/status.

## Daily flows — T−1

- commits;
- additions/deletions;
- PRs opened/merged/closed;
- issues opened/closed;
- Actions runs/jobs completed;
- releases published;
- deployments/status transitions;
- views/clones;
- work-type activity.

## Rolling snapshots — T

- referrers;
- popular paths.

Это разделение нужно закреплять в schema каждого семейства, а не пытаться применять одно поле даты ко всем данным.

---

# 4. Три слоя данных

## 4.1. Layer A — Source observations

Факты, максимально близкие к GitHub:

```text
repository state
commit facts
PR flow
issue flow
Actions flow
release flow
deployment flow
governance snapshots
traffic
collection telemetry
```

## 4.2. Layer B — Semantic daily facts

Детерминированные агрегаты:

```text
code churn
PR duration buckets
issue backlog delta
Actions outcomes and duration buckets
work-type composition
human/automation split
deployment duration
```

## 4.3. Layer C — Analytical views

Пересчитываемый слой:

```text
7d / 28d rolling windows
period-over-period deltas
portfolio concentration
activity breadth
repo-role aggregates
work-type aggregates
DORA-compatible metrics where valid
```

Layer C лучше хранить отдельно, например в `derived/`, а raw/normalized observations — под текущим data root.

---

# 5. Commit layer: самый дешёвый и сильный апгрейд

Текущий GraphQL history уже запрашивает для каждого commit `committedDate` и `changedFilesIfAvailable`. Объект GitHub GraphQL `Commit` также предоставляет `additions` и `deletions`. Это значит, что их можно получить почти без роста числа HTTP requests — расширяется уже существующий query.

## 5.1. Рекомендуемые primary fields

```text
activity_date_utc
commits
additions
deletions
changed_file_occurrences
commits_with_unknown_changed_files
merge_commits
non_merge_commits
last_observed_at
```

Опционально:

```text
human_commits
automation_commits
unknown_actor_commits
```

Actor identity хранить не требуется.

## 5.2. Производные

### Churn

```text
code_churn = additions + deletions
```

### Net line delta

```text
net_line_delta = additions - deletions
```

### Размер commit

```text
churn_per_commit = code_churn / commits
```

### Ширина commit

```text
changed_files_per_commit = changed_file_occurrences / commits
```

Эти показатели описывают характер изменений. Они не являются productivity или quality score.

---

# 6. Human vs automation

Для этой экосистемы важно отделять ручную работу от автогенерации. Daily collector, bots и другие Actions способны создавать регулярные commits и искусственно поддерживать видимость постоянной активности.

Предлагаемая transient classification:

```text
human
automation
unknown
```

В durable evidence сохранять только агрегаты:

```text
human_commits
automation_commits
unknown_actor_commits
```

Производная:

```text
automation_share =
    automation_commits /
    (human_commits + automation_commits + unknown_actor_commits)
```

Для dashboard полезно иметь одновременно:

```text
all canonical activity
human-associated activity
```

Это особенно важно для repositories с generated data или automated publication.

---

# 7. Work type: что именно делали

Сильнейший новый semantic layer — классификация изменяемых областей.

Вопрос меняется с:

> сколько commits?

на:

> какая работа велась?

## 7.1. Базовая таксономия

```text
product_code
tests_quality
documentation_specification
research_method
data_content
automation_ci
build_packaging
configuration
assets
unknown
```

На уровне commit возможен `mixed`, но для аналитики лучше multi-label агрегация по файлам.

## 7.2. Пример правил

```text
src/**                  → product_code
packages/**             → product_code

tests/**
test_*.py               → tests_quality

docs/**
README*
spec/**
specs/**
method/**               → documentation_specification

_mw/**
research/**
development-reports/**  → research_method

russia/**
data/**
*.csv
*.parquet               → data_content

.github/**              → automation_ci

scripts/**
tools/**
Dockerfile
pyproject.toml
BUILD.json              → build_packaging / configuration
```

Правила должны быть:

- детерминированными;
- versioned;
- упорядоченными;
- с repository-specific overrides.

## 7.3. Privacy boundary

Пути нужны только во время расчёта. Их можно читать transiently и сразу сворачивать в:

```text
activity_date_utc
work_type
changed_file_occurrences
additions
deletions
commits_contributing
classification_version
classification_status
```

Raw paths не сохраняются.

## 7.4. Coverage

Обязательно фиксировать:

```text
classified_file_occurrences
unclassified_file_occurrences
classification_coverage
classification_version
```

Без coverage классификация выглядит точнее, чем она есть.

## 7.5. Неаддитивность commits

Если один commit затронул code, tests и docs, `commits_contributing` попадёт во все три категории. Поэтому основной аддитивный слой — `changed_file_occurrences`, `additions`, `deletions`.

---

# 8. Pull Requests

PR отражает рабочий lifecycle, которого нет в commit count.

Observatory может собирать PR metadata и transiently анализировать changed files без сохранения title/body/author/filename.

## 8.1. Daily flow

```text
prs_opened
prs_closed
prs_merged
prs_reopened
draft_prs_opened
```

## 8.2. Snapshot

```text
open_prs
draft_open_prs
open_prs_age_p50_days
open_prs_age_p90_days
```

## 8.3. Размер PR

Для merged/closed PRs:

```text
pr_additions_sum
pr_deletions_sum
pr_changed_files_sum
pr_commits_sum
```

Распределения:

```text
pr_churn_p50
pr_churn_p90
pr_changed_files_p50
pr_changed_files_p90
```

## 8.4. Cycle time

```text
time_to_merge = merged_at - created_at
```

Хранить p50/p90 или histogram buckets.

Если review timeline доступен и стоит дополнительных запросов:

```text
time_to_first_review = first_review_at - created_at
```

## 8.5. Ошибка, которой стоит избежать

```text
prs_merged_today / prs_opened_today
```

не является корректным merge rate: числитель и знаменатель относятся к разным cohorts.

Если нужен share, лучше считать среди PRs, закрытых в одном cohort/window, либо строить cohort analysis.

---

# 9. Issues

Issues дают независимый поток задач/проблем.

GitHub Issues REST API может возвращать и pull requests; их надо отделять по `pull_request` marker или использовать отдельные PR endpoints.

## 9.1. Daily flow

```text
issues_opened
issues_closed
issues_reopened
```

## 9.2. Snapshot

```text
open_issues
open_issues_age_p50_days
open_issues_age_p90_days
open_issues_30d_plus
open_issues_90d_plus
```

## 9.3. Производные

```text
backlog_delta = issues_opened - issues_closed
```

```text
issue_close_time = closed_at - created_at
```

Для распределений предпочтительнее p50/p90 либо buckets.

## 9.4. Labels

Raw label names сохранять необязательно. При необходимости labels можно transiently mapped в безопасную taxonomy:

```text
bug
feature
maintenance
documentation
research
other
```

---

# 10. GitHub Actions — наиболее ценный новый operational layer

GitHub сам выделяет для Actions performance metrics run time, queue time и failure rate; usage metrics включают workflows, jobs, repositories, runtime OS и runner type.

Observatory может построить собственный долговременный ряд этих фактов.

## 10.1. Workflow inventory snapshot

```text
workflow_count
workflow_active_count
workflow_disabled_count
```

Имена/path workflows сохранять не обязательно.

## 10.2. Runs — daily flow

```text
runs_started
runs_completed
runs_success
runs_failure
runs_cancelled
runs_skipped
runs_timed_out
runs_action_required
```

По trigger event:

```text
runs_push
runs_pull_request
runs_schedule
runs_workflow_dispatch
runs_other_event
```

Event — полезная обезличенная характеристика причины запуска.

## 10.3. Reruns

Workflow runs имеют `run_attempt`.

Можно считать:

```text
rerun_attempts
logical_runs_with_rerun
rerun_rate = logical_runs_with_rerun / logical_runs
```

Это признак CI instability, но не DORA change fail rate.

## 10.4. Run duration

```text
run_duration = completed_at - run_started_at
```

Сохранять:

```text
run_duration_p50_seconds
run_duration_p95_seconds
```

или duration histogram.

## 10.5. Jobs

Jobs дают более точный pipeline view:

```text
jobs_completed
jobs_success
jobs_failure
jobs_cancelled
job_runtime_p50
job_runtime_p95
job_queue_p50
job_queue_p95
```

## 10.6. CI recovery

Можно считать:

```text
ci_recovery_time
```

как интервал от failed run до следующего successful run того же logical workflow context.

Его нужно называть именно **CI recovery**, а не DORA failed deployment recovery.

## 10.7. Actions per change

```text
runs_per_commit
jobs_per_commit
ci_seconds_per_commit
ci_seconds_per_1000_churn_lines
```

Это descriptors стоимости automation, а не универсальные efficiency scores.

---

# 11. Actions billing / фактическая стоимость

GitHub Billing Usage API для user account может отдавать usage items с:

```text
date
product
sku
quantity
unitType
pricePerUnit
grossAmount
discountAmount
netAmount
repositoryName
```

Для product `Actions` это позволяет получить repository/day факты:

```text
actions_billable_minutes
actions_gross_amount
actions_discount_amount
actions_net_amount
```

Это optional capability: зависит от billing platform и token permissions.

Цены лучше не hardcode. Если GitHub возвращает фактические quantity/amount, сохранять именно их.

---

# 12. Actions cache usage

GitHub имеет aggregate endpoint cache usage. Для repository можно получать:

```text
active_caches_count
active_caches_size_in_bytes
```

Это хороший snapshot T.

Опционально из списка cache entries transiently:

```text
cache_oldest_age_days
cache_p50_age_days
cache_p90_age_days
```

Не сохранять:

- cache key;
- ref;
- version.

Важное ограничение: cache inventory не даёт полноценный hit/miss stream, поэтому `cache hit rate` из этих данных выводить нельзя.

---

# 13. Actions artifacts

Workflow artifacts можно агрегировать без скачивания содержимого:

```text
artifact_count
artifact_total_bytes
expired_artifact_count
```

Опционально age buckets.

Не следует сохранять artifact names или contents.

---

# 14. Releases

GitHub Releases дают отдельную delivery surface.

Daily flow:

```text
releases_published
prereleases_published
```

Snapshot:

```text
published_release_count
draft_release_count
latest_release_published_at
days_since_latest_release
```

Release assets:

```text
release_asset_count
release_asset_bytes
release_asset_downloads_cumulative
```

При ежедневном snapshot cumulative download count можно строить:

```text
downloads_daily_delta = cumulative_today - cumulative_previous
```

Нужно учитывать удаление/recreation assets и сопровождать delta статусом полноты.

---

# 15. Deployments

Deployment API — ключевой слой для delivery metrics.

Deployment status может быть:

```text
queued
pending
in_progress
success
failure
error
inactive
```

GitHub хранит предыдущие deployment statuses только 90 дней. Поэтому ежедневное durable сохранение агрегированной deployment history особенно полезно.

## 15.1. Primary facts

```text
deployments_created
deployments_success
deployments_failure
deployments_error
deployments_inactive
```

При безопасной нормализации environment:

```text
production_deployments_success
nonproduction_deployments_success
```

Raw environment names хранить необязательно.

## 15.2. Deployment duration

```text
deployment_time_to_success =
    successful_status_at - deployment_created_at
```

Хранить p50/p90 или buckets.

---

# 16. DORA: строгая граница интерпретации

DORA software delivery performance включает deployment frequency, change lead time, failed deployment recovery time, change fail rate и deployment rework rate.

GitHub Observatory не должен автоматически объявлять любой CI/deployment signal DORA metric.

## 16.1. Deployment frequency

Корректно, если:

- repository deployable;
- production semantics определены;
- GitHub deployment records соответствуют реальным production deployments.

```text
deployment_frequency = successful production deployments / period
```

## 16.2. Change lead time

Более правильный алгоритм:

1. взять два последовательных successful production deployments;
2. определить commits, впервые вошедшие между предыдущим и новым deployed SHA;
3. для каждого commit:

```text
lead_time = deployment_success_at - commit.committedDate
```

4. агрегировать распределение.

## 16.3. Change fail rate

Нельзя механически считать:

```text
failed deployment status / all deployments
```

как DORA change fail rate. DORA описывает production change, который потребовал immediate intervention.

Failed deployment до фактического production impact может не соответствовать этому определению.

## 16.4. Failed deployment recovery

Тоже требует уверенной идентификации production failure и последующего восстановления. Иначе это только `deployment-status recovery proxy`.

## 16.5. Deployment rework rate

Из одного GitHub deployment stream обычно невозможно достоверно определить, что deployment был незапланированным remediation после production incident. Без дополнительной маркировки метрику лучше не публиковать.

---

# 17. Governance и repository configuration

Часть важных событий — это изменения правил repository, а не commits.

## 17.1. Branch inventory

GitHub list branches возвращает `protected`.

Можно сохранять:

```text
branch_count
protected_branch_count
```

без branch names. Это совместимо с текущей boundary Observatory, где refs не являются observation dimension.

## 17.2. Default-branch protection

Transiently прочитать protection settings и сохранить только агрегированное состояние:

```text
default_branch_protected
requires_status_checks
requires_pr_reviews
required_approvals
requires_code_owner_reviews
requires_last_push_approval
dismisses_stale_reviews
requires_linear_history
allows_force_push
allows_deletions
requires_conversation_resolution
```

User/team identities не сохраняются.

## 17.3. Configuration drift

Governance — snapshot T. Производный факт:

```text
governance_change_event
```

возникает при изменении snapshot относительно предыдущего наблюдения.

---

# 18. Community profile

GitHub Community Profile API возвращает наличие:

- README;
- license;
- CONTRIBUTING;
- issue template;
- PR template;
- code of conduct;
- documentation;
- GitHub `health_percentage`.

Лучше сохранять наблюдаемые booleans:

```text
has_readme
has_license
has_contributing
has_issue_template
has_pr_template
has_code_of_conduct
has_documentation
```

`health_percentage` допустим как GitHub-provided metric, но не как собственный рейтинг качества repository.

---

# 19. Dependency inventory / SBOM

GitHub Dependency Graph умеет генерировать SPDX-compatible SBOM.

В Observatory потенциально полезны только aggregates:

```text
dependency_count
dependency_ecosystem_count
```

при надёжной доступности:

```text
direct_dependency_count
transitive_dependency_count
```

## Почему не daily core

Dependencies меняются при изменении manifests/lockfiles. Практичнее:

- on relevant change;
- либо weekly.

На 24 сентября 2026 GitHub сообщает, что старый SBOM operation будет закрыт после **13 ноября 2026** и рекомендует asynchronous generate/fetch flow. Новую реализацию нужно сразу строить через новый flow.

Security findings сюда включать не следует.

---

# 20. Repository Statistics API

GitHub имеет готовые statistics endpoints: code frequency, commit activity, contributors.

Они полезны для validation или отдельных backfills, но не должны становиться главным источником Observatory:

- GitHub прямо описывает вычисление statistics как дорогую операцию;
- endpoint может сначала вернуть `202`;
- результат cache-ируется по SHA default branch;
- push в default branch инвалидирует cache;
- собственный GraphQL/REST collector даёт более контролируемую семантику.

Рекомендация:

```text
statistics API → validation / secondary evidence
GraphQL + targeted REST → primary collection
```

---

# 21. Traffic: производные из уже собранных данных

## 21.1. Rolling sums

```text
views_7d
views_14d
views_28d
clones_7d
clones_14d
clones_28d
```

28d становится возможным именно благодаря собственному архиву Observatory, хотя GitHub Traffic API даёт только недавнее окно.

## 21.2. Intensity descriptors

```text
views_per_active_day
views_per_commit
views_per_1000_churn_lines
```

Это descriptors, а не “эффективность”.

## 21.3. Views / clones

Можно показывать отношение `clones / views`, но нельзя называть его conversion rate пользователей.

## 21.4. Uniques нельзя дедуплицировать между repositories

```text
sum(repo.unique_viewers)
```

не равно числу уникальных людей портфеля. Один человек может попасть в uniques нескольких repositories.

Поэтому cross-repo sums uniques либо не считать, либо явно называть `sum_of_repository_unique_counts`.

---

# 22. Referrers и popular paths

Это rolling snapshots, а не дневные flows.

Допустимые snapshot analytics:

```text
top_referrer_share
referrer_concentration
top_path_share
path_concentration
```

Нельзя получать “daily referrer flow” простым вычитанием двух rolling snapshots: одновременно добавляется новый день и выпадает старый.

---

# 23. Portfolio layer

Именно этот слой превращает Observatory в систему наблюдения всей экосистемы.

## 23.1. Active repositories

```text
active_repositories_day =
    count(repositories with qualifying activity > 0)
```

Лучше отдельно:

```text
active_repositories_all_activity
active_repositories_human_activity
```

## 23.2. Breadth

```text
active_repositories_7d
active_repositories_28d
```

## 23.3. Concentration

Для commits или churn:

```text
share_i = activity_i / total_activity
HHI = Σ share_i²
```

Интерпретация: ближе к 1 — работа сильнее сосредоточена в одном repository. Это focus concentration, а не качество.

Альтернатива — normalized entropy:

```text
H = -Σ p_i * ln(p_i) / ln(N_active)
```

Для dashboard достаточно одного из этих показателей.

## 23.4. Portfolio totals

```text
portfolio_commits
portfolio_additions
portfolio_deletions
portfolio_churn
portfolio_changed_files
```

## 23.5. Work-type composition

```text
product_code_share
tests_quality_share
docs_spec_share
research_method_share
data_content_share
automation_share
```

Лучше по churn или changed-file occurrences, а не только по commits.

---

# 24. Repository role — отдельная dimension

Repository role и work type — разные сущности.

Пример:

```text
AppDock
repo_role = software_product
```

но сегодняшняя работа может быть `documentation_specification`.

И наоборот:

```text
tabularium
repo_role = data_registry
```

может иметь `data_content`, `automation_ci` и `documentation_specification` в один день.

## 24.1. Возможная taxonomy

```text
software_product
library_framework
data_registry
analytics_workspace
method_specification
research_experiment
pilot
infrastructure
gateway_integration
archive_legacy
other
```

## 24.2. Лучше curated, а не daily AI inference

Роль repository меняется редко и является смысловой классификацией. Лучше хранить её явно в version-controlled dimension, например:

```text
profiles/repository-dimensions.csv
```

или YAML.

---

# 25. Матрица repo role × work type

Две оси дают сильное представление:

```text
                  code  tests  docs  research  data  automation
software_product
library_framework
data_registry
method_spec
research_pilot
analytics_workspace
gateway
```

Это позволяет отвечать:

- где идёт продуктовая разработка;
- где исследование;
- где растут datasets;
- где изменения почти полностью automated;
- какие категории repositories активны;
- как меняется структура работы во времени.

---

# 26. Activity cadence

Derived metrics по repository:

```text
days_since_last_activity
active_days_7d
active_days_28d
current_active_streak
longest_active_streak_90d
```

Лучше разделить:

```text
days_since_last_human_activity
days_since_last_any_activity
```

---

# 27. Momentum без “магического score”

Не нужен единый proprietary activity score.

Лучше показывать прозрачные сравнения:

```text
commits_7d vs previous_7d
churn_7d vs previous_7d
active_days_7d vs previous_7d
PR_merges_7d vs previous_7d
Actions_runs_7d vs previous_7d
```

Это не смешивает несопоставимые величины.

---

# 28. Изменение размера и структуры repository

Из уже существующих snapshot fields:

```text
size_kb
files
commits
language bytes
```

можно считать:

```text
delta_files
delta_size_kb
delta_commits
delta_language_bytes
```

`files_T - files_T-1` — net stock change, а не число файлов, добавленных в commits.

## Language mix

```text
language_share = language_bytes / total_language_bytes
```

Производные:

```text
language_share_change
new_language_detected
language_removed
```

---

# 29. Stars, forks, subscribers

Текущие snapshots позволяют:

```text
stars_delta
forks_delta
subscribers_delta
```

Если когда-нибудь понадобится точный acquisition timing, stargazer/fork objects можно transiently читать и сохранять только aggregate by date. Usernames/owners не нужны.

Для небольших значений snapshot delta проще и дешевле.

---

# 30. Observability самого collector

Это очень ценный слой.

Уже есть started/finished/status counts. Стоит добавить:

```text
rest_requests
graphql_requests
http_304_count
retry_count
bytes_received

rate_limit_start
rate_limit_end
rate_limit_min_remaining

families_expected
families_collected
families_unavailable

repositories_skipped_unchanged
repositories_incrementally_scanned
repositories_full_reconciled
```

## Freshness

```text
latest_source_event_at
collection_lag_seconds
```

## Completeness

```text
collection_completeness =
    successful_expected_observations /
    expected_observations
```

Это техническая completeness Observatory, а не оценка repository.

---

# 31. Rate-limit architecture

Для authenticated personal access token типичный REST primary limit — 5,000 requests/hour. Есть и secondary rate limits.

Расширенный collector должен обрабатывать:

- `403` / `429`;
- `retry-after`;
- `x-ratelimit-reset`;
- exponential backoff;
- rate-limit telemetry;
- bounded expensive families.

Текущая логика retries для 502/503/504 недостаточна для более тяжёлого collector.

---

# 32. ETag / conditional GET

Для стабильных snapshot endpoints стоит добавить:

```text
If-None-Match / ETag
If-Modified-Since
```

Authenticated `304 Not Modified` не расходует primary REST quota.

Особенно полезно для:

- workflow inventory;
- governance snapshots;
- community profile;
- repository metadata;
- releases при низкой активности;
- branch inventory.

Локально достаточно metadata cache:

```text
endpoint_key
etag
last_modified
last_checked_at
```

Response content хранить отдельно не требуется.

---

# 33. Главный scalability issue текущего collector

Сейчас ежедневный run перечитывает всю canonical history каждого repository.

Это семантически надёжно, но растёт примерно как:

```text
O(all historical commits × every daily run)
```

Перед добавлением per-file classification эту архитектуру стоит изменить.

---

# 34. Incremental canonical history

## 34.1. Сохранять current canonical head OID

```text
canonical_head_oid
```

SHA не является branch name и не требует раскрывать ref dimension.

## 34.2. На следующем run сравнить previous/current head

### Head unchanged

History scan не нужен.

### Fast-forward

Обработать только новые commits и пересчитать затронутые days.

### Divergence / rewrite

Выполнить full reconciliation только для этого repository.

## 34.3. Периодический assurance pass

Например weekly full reconciliation.

Целевая стоимость:

```text
O(new commits)
```

с bounded fallback после rewrites.

---

# 35. Incremental PR / Issues / Actions

Event-like APIs лучше собирать через watermark:

```text
last_successful_observed_at
```

Следующий запрос:

```text
since = watermark - overlap
```

Overlap, например 24–48h, позволяет пережить поздние updates и повторные runs.

Далее:

- transient dedup по object ID;
- распределение по фактическим timestamps;
- upsert daily partitions.

---

# 36. Почему Events API не должен быть ядром

Общий GitHub Events stream удобен как диагностический источник, но Observatory нужен воспроизводимый domain evidence.

Предпочтительно использовать authoritative families:

```text
commits
pull requests
issues
actions
releases
deployments
traffic
```

---

# 37. Стоимость work-type classification

## GraphQL-only core

Дёшево:

```text
commit date
additions
deletions
changed files count
```

## Per-file REST

Для work type нужны filenames/per-file changes. REST commit endpoint возвращает stats + files, но это может потребовать запрос на каждый новый commit.

Правильная стратегия:

- только latest closed day/new commits;
- только repositories с activity;
- hard cap;
- explicit `classification_status`;
- raw paths не сохранять.

Если cap превышен:

```text
classification_status = partial_limit
```

Unknown не превращается в zero.

---

# 38. Merge commits и churn

Git topology включает regular commits, merge commits, squash merges и rebases.

Если суммировать diff каждого canonical commit, topology влияет на churn.

Поэтому нужно:

1. отдельно считать `merge_commits`;
2. документировать, что churn — сумма GitHub commit diffs;
3. при необходимости иметь `non_merge_commit_churn`;
4. не суммировать PR-level additions/deletions и commit-level churn как одну величину.

Это разные analytical lenses.

---

# 39. Предлагаемая файловая архитектура

Исследовательское предложение:

```text
ForestTiger-GH/
├── repositories.csv
├── _collection/
│   ├── runs.csv
│   ├── repository-status.csv
│   ├── api-telemetry.csv
│   └── source-freshness.csv
│
├── <repo>/
│   ├── repository.csv
│   ├── activity.csv
│   ├── languages.csv
│   │
│   ├── development/
│   │   ├── pull-requests.csv
│   │   └── issues.csv
│   │
│   ├── automation/
│   │   ├── actions.csv
│   │   ├── workflows.csv
│   │   ├── caches.csv
│   │   └── artifacts.csv
│   │
│   ├── delivery/
│   │   ├── releases.csv
│   │   └── deployments.csv
│   │
│   ├── governance/
│   │   └── repository-governance.csv
│   │
│   ├── work/
│   │   └── work-types.csv
│   │
│   └── traffic/
│       ├── views.csv
│       ├── clones.csv
│       ├── referrers.csv
│       └── paths.csv
```

Пересчитываемый слой:

```text
derived/
├── repository-daily.csv
├── portfolio-daily.csv
├── work-types-daily.csv
├── delivery-daily.csv
└── dashboard.json
```

Граница:

```text
ForestTiger-GH/ → canonical/normalized observations
derived/        → recalculable analytics
```

---

# 40. Минимальный schema expansion

Если расширяться постепенно, первый пакет можно ограничить четырьмя семействами.

## 40.1. Расширить `activity.csv`

```text
additions
deletions
merge_commits
human_commits
automation_commits
unknown_actor_commits
```

## 40.2. `development/pull-requests.csv`

```text
activity_date_utc
opened
closed
merged
reopened
open_snapshot
time_to_merge_p50_hours
time_to_merge_p90_hours
merged_additions
merged_deletions
merged_changed_files
observed_at
```

## 40.3. `development/issues.csv`

```text
activity_date_utc
opened
closed
reopened
open_snapshot
open_30d_plus_snapshot
open_90d_plus_snapshot
close_time_p50_hours
close_time_p90_hours
observed_at
```

## 40.4. `automation/actions.csv`

```text
activity_date_utc
runs
success
failure
cancelled
reruns
run_seconds_sum
run_seconds_p50
run_seconds_p95
queue_seconds_p50
queue_seconds_p95
jobs
job_failures
observed_at
```

---

# 41. Work-types schema

```text
activity_date_utc
work_type
changed_file_occurrences
additions
deletions
commits_contributing
classification_version
classification_status
observed_at
```

`work_type` — controlled vocabulary.

---

# 42. Delivery schema

## Releases

```text
activity_date_utc
published
prereleases
asset_count_published
asset_bytes_published
observed_at
```

## Deployments

```text
activity_date_utc
deployments
success
failure
error
production_success
deployment_duration_p50
deployment_duration_p90
observed_at
```

Если production semantics отсутствует:

```text
production_success = unknown
```

а не 0.

---

# 43. Governance schema

Snapshot T:

```text
snapshot_date_utc
branch_count
protected_branch_count

default_branch_protected
requires_status_checks
requires_pr_reviews
required_approvals
requires_code_owner_reviews
requires_linear_history
allows_force_push
allows_deletions
requires_conversation_resolution

workflow_count
active_workflow_count

has_readme
has_license
has_contributing
has_issue_template
has_pr_template
has_code_of_conduct

observed_at
```

---

# 44. Repository dimensions

Отдельная curated dimension:

```text
repository_id
repository_role
deployable
production_semantics_available
classification_profile
classification_profile_version
```

Это semantic configuration, а не ежедневное observation.

---

# 45. Derived metrics по repository

## Activity

```text
commits 1d / 7d / 28d
churn 1d / 7d / 28d
active days
days since last activity
human vs automation
```

## Development flow

```text
PR opened / merged
PR cycle time
issue opened / closed
issue backlog
```

## Automation

```text
runs
failure rate
runtime
queue time
reruns
Actions minutes/cost
```

## Delivery

```text
release cadence
deployment cadence
deployment duration
change lead time where valid
```

## Attention

```text
views
clones
stars delta
forks delta
```

## Composition

```text
language mix
work-type mix
```

---

# 46. Derived metrics по всей экосистеме

```text
repository_count
active_repository_count

portfolio_commits
portfolio_churn

human_activity_share
automation_activity_share

repo_activity_concentration

work_type_distribution
repo_role_distribution

PR_flow
issue_flow

Actions_runs
Actions_failures
Actions_runtime
Actions_minutes
Actions_spend

releases
deployments

views
clones

collection_completeness
```

---

# 47. Почему repo-role aggregates важнее простого рейтинга

Текущий ForestTiger-GH universe включает разные типы repositories: software/platform, data, analytics workspace, methodology/spec, pilots/research, gateway/integration, legacy/archive.

Поэтому сравнение всех по одному показателю `commits` или `churn` будет систематически искажать картину.

Сильнее модель:

```text
repository role
×
work type
×
time
×
development lifecycle
```

---

# 48. Histograms вместо event ledger

Если Observatory хранит только p50/p90 по каждому repository, точный portfolio p50 из них восстановить нельзя.

Чтобы не хранить event-level PR/run/issue ledger, можно сохранять duration histogram buckets.

## PR / issue buckets

```text
<1h
1-6h
6-24h
1-3d
3-7d
7-30d
30d+
```

## Actions runtime buckets

```text
<30s
30s-2m
2-5m
5-15m
15-30m
30-60m
60m+
```

## Queue buckets

```text
<10s
10-30s
30-60s
1-5m
5-15m
15m+
```

Buckets аддитивны между repositories и сохраняют распределение без identities и event records.

---

# 49. Additivity contract

## Обычно аддитивно между repositories

```text
commits
additions
deletions
workflow runs
PR opened
issues opened
releases
deployments
view count
clone count
histogram bucket counts
```

## Не аддитивно как “уникальные люди”

```text
unique viewers
unique cloners
```

## Нельзя просто суммировать

```text
p50 / p90
rates
shares
HHI
```

Portfolio-level значения таких метрик надо пересчитывать корректно.

---

# 50. Privacy classes

Полезно формализовать четыре класса.

## A. Safe aggregate

```text
counts
durations
churn
backlog
success/failure totals
```

## B. Public-detail only

Например текущие:

```text
popular paths
referrers
```

## C. Transient-only

```text
file paths
actor identities
workflow names
environment names
labels
```

## D. Never persist here

```text
secrets
workflow logs
artifact contents
security findings
commit messages
issue/PR bodies
review/comment text
```

Общая модель:

```text
rich input
→ narrow normalized evidence
```

---

# 51. Permission model

Нужно различать:

```text
GITHUB_TOKEN       → записывает результат в github-observatory
OBSERVATORY_TOKEN  → читает наблюдаемые repositories
```

Для новых families fine-grained token может потребовать:

```text
Contents: read
Pull requests: read
Issues: read
Actions: read
Deployments: read
Administration: read
Plan: read  # только если billing layer включён
```

Нужно выдавать только реально используемые permissions.

---

# 52. API cost / collection tiers

## Дешёвые

- additions/deletions в существующем GraphQL;
- repository snapshots;
- workflow inventory;
- cache aggregate usage;
- branch count;
- community profile;
- incremental PR/issues.

## Средние

- workflow runs;
- jobs;
- releases;
- deployments.

## Потенциально дорогие

- per-commit file details;
- full canonical history every day;
- exhaustive PR file history;
- repeated full stargazer/fork history;
- daily full SBOM.

Их нужно делать incremental/conditional.

---

# 53. Приоритет по ROI

| Family | Value | API cost | Complexity | Priority |
|---|---:|---:|---:|---:|
| Commit additions/deletions | very high | very low | low | P0 |
| Human/automation split | high | low | medium | P0 |
| Actions runs | very high | low/medium | medium | P0 |
| PR flow | very high | low/medium | medium | P0 |
| Issue flow | high | low/medium | medium | P0 |
| Collector telemetry | very high | very low | low | P0 |
| Incremental history | very high | saves cost | medium/high | P0 |
| Work types | very high | medium/high | high | P1 |
| Workflow jobs | high | medium | medium | P1 |
| Releases | medium/high | low | low | P1 |
| Deployments | high for deployable repos | low/medium | medium | P1 |
| Governance | medium | low | medium | P1 |
| Billing | medium/high | low | medium | P2 |
| Caches/artifacts | medium | low | low | P2 |
| SBOM aggregates | medium | medium | medium | P3 |

---

# 54. Первый implementation package

Если переходить от исследования к реализации, оптимальный bounded пакет:

```text
1. Внедрить T / T−1 temporal model из предыдущего исследования.
2. Добавить canonical head OID и incremental history.
3. Расширить GraphQL commits: additions/deletions + merge flag.
4. Добавить human/automation aggregate.
5. Добавить PR daily flow.
6. Добавить Issues daily flow.
7. Добавить Actions runs daily flow.
8. Добавить collector API telemetry и rate-aware retry.
9. Создать derived/repository-daily и derived/portfolio-daily.
10. После стабилизации добавить work-type classifier.
```

Следующий пакет:

```text
workflow jobs
releases
deployments
governance
billing/cache/artifact usage
```

---

# 55. Целевой daily execution

```text
02:xx UTC
│
├─ discover repositories
│
├─ current snapshots (T)
│   ├─ metadata
│   ├─ languages
│   ├─ workflows
│   ├─ caches
│   ├─ governance
│   └─ backlog stocks
│
├─ latest closed day (T−1)
│   ├─ commits
│   ├─ PR flow
│   ├─ issues flow
│   ├─ Actions
│   ├─ releases
│   ├─ deployments
│   ├─ views
│   └─ clones
│
├─ transient enrichment
│   ├─ actor class
│   └─ changed path → work type
│
├─ persist canonical observations
│
├─ build derived model
│   ├─ repository daily
│   ├─ portfolio daily
│   ├─ work mix
│   └─ rolling windows
│
└─ render dashboard
```

Это естественно продолжает два предыдущих исследования:

```text
WHEN  → Temporal semantics
WHAT  → Expanded evidence & metrics
VIEW  → Dynamic rendering
```

---

# 56. Сильнейшие метрики для первого dashboard

## Portfolio

```text
active repositories
commits
churn
human activity share
top-3 activity share
work mix
```

## Development

```text
merged PRs
PR cycle p50
issue backlog delta
```

## Automation

```text
Actions runs
Actions failure rate
runtime p50/p95
rerun rate
```

## Delivery

```text
releases
production deployments
change lead time where valid
```

## Attention

```text
views
clones
star delta
```

## Observatory health

```text
collection completeness
API errors
collection duration
rate remaining
```

---

# 57. Что считать ежедневно, а что реже

## Ежедневно

```text
repo metadata
languages
commits
PRs
issues
Actions runs/jobs
releases
deployments
traffic
cache aggregate
collector health
```

## Conditional / ETag

```text
governance
workflow inventory
community profile
```

## Еженедельно / on-change

```text
SBOM aggregate
full canonical reconciliation
expanded governance audit
```

## По необходимости

```text
historical backfill
expensive repository statistics
exact stargazer history
```

---

# 58. Что сознательно не делать первым

Не начинать с:

- AI productivity score;
- semantic analysis commit messages;
- PR/issue body classification;
- daily full dependency graph;
- full event ledger всех GitHub objects;
- security findings;
- универсального ranking repositories;
- DORA labels на любую CI activity.

Сначала нужен устойчивый evidence layer.

---

# 59. Output vs outcome

GitHub хорошо наблюдает:

```text
work output
development process
delivery process
repository reach
```

GitHub почти не измеряет напрямую:

```text
business value
software quality
user satisfaction
research correctness
profitability
strategic importance
```

Поэтому:

```text
more commits ≠ better
more churn ≠ better
more PRs ≠ better
more deployments ≠ better
more Actions ≠ better
```

Observatory должен измерять факты, а не подменять ими оценку результата.

---

# 60. Целевой semantic core

У каждого repository полезно иметь восемь независимых осей:

```text
STATE
  что существует сейчас

CHANGE
  что изменилось в canonical Git history

WORKFLOW
  как работа проходила через PR/issues

AUTOMATION
  как отработали Actions

DELIVERY
  что было released/deployed

ATTENTION
  что происходило с внешним интересом

WORK TYPE
  что это была за работа

OBSERVATORY HEALTH
  насколько надёжно всё это измерено
```

Один daily analytical record логически выглядит так:

```text
repo
date

STATE
files
size
languages
stars

CHANGE
commits
additions
deletions
changed_files
human_commits
automation_commits

WORKFLOW
prs_opened
prs_merged
issues_opened
issues_closed
backlog

AUTOMATION
runs
failures
runtime
queue_time
reruns

DELIVERY
releases
deployments

ATTENTION
views
clones

WORK TYPE
code
tests
docs
research
data
automation

QUALITY OF OBSERVATION
completeness
freshness
```

Это уже полноценная repository observability model.

---

# 61. Итоговая рекомендация

GitHub Observatory не стоит развивать по принципу «собирать всё, что отдаёт GitHub API».

Сильнее построить **компактную фактическую модель repository work system**.

Она должна отвечать на четыре уровня вопросов.

## 1. Что есть?

```text
repositories
files
languages
size
stars
workflows
governance
```

## 2. Что происходило?

```text
commits
churn
PRs
issues
Actions
releases
deployments
traffic
```

## 3. Какая это была работа?

```text
code
tests
docs/spec
research
data
automation
configuration
```

## 4. Что происходит со всей системой repositories?

```text
active-repo breadth
portfolio concentration
work composition
human vs automation
development flow
automation reliability
delivery flow
attention
```

При этом сохраняется текущая сильная граница:

```text
no repository-content copying
no identities
no message bodies
no workflow logs
no artifact contents
no security findings
no opaque productivity scores
```

---

# 62. Источники

Официальные источники, проверенные 24 сентября 2026:

1. GitHub REST — Repository statistics  
   https://docs.github.com/en/rest/metrics/statistics

2. GitHub REST — Repository traffic  
   https://docs.github.com/en/rest/metrics/traffic

3. GitHub GraphQL — Commits  
   https://docs.github.com/en/graphql/reference/commits

4. GitHub REST — Commits  
   https://docs.github.com/en/rest/commits/commits

5. GitHub REST — Pull requests  
   https://docs.github.com/en/rest/pulls/pulls

6. GitHub REST — Issues  
   https://docs.github.com/en/rest/issues/issues

7. GitHub REST — Workflow runs  
   https://docs.github.com/en/rest/actions/workflow-runs

8. GitHub REST — Workflow jobs  
   https://docs.github.com/en/rest/actions/workflow-jobs

9. GitHub REST — Workflows  
   https://docs.github.com/en/rest/actions/workflows

10. GitHub Actions — Metrics  
    https://docs.github.com/en/actions/concepts/metrics

11. GitHub Actions — Viewing metrics  
    https://docs.github.com/en/actions/how-tos/administer/view-metrics

12. GitHub REST — Actions artifacts  
    https://docs.github.com/en/rest/actions/artifacts

13. GitHub REST — Actions cache  
    https://docs.github.com/en/rest/actions/cache

14. GitHub REST — Billing usage  
    https://docs.github.com/en/rest/billing/usage

15. GitHub REST — Releases  
    https://docs.github.com/en/rest/releases/releases

16. GitHub REST — Deployments  
    https://docs.github.com/en/rest/deployments/deployments

17. GitHub REST — Deployment statuses  
    https://docs.github.com/en/rest/deployments/statuses

18. GitHub REST — Branches  
    https://docs.github.com/en/rest/branches/branches

19. GitHub REST — Branch protection  
    https://docs.github.com/en/rest/branches/branch-protection

20. GitHub REST — Community metrics  
    https://docs.github.com/en/rest/metrics/community

21. GitHub REST — SBOM  
    https://docs.github.com/en/rest/dependency-graph/sboms

22. GitHub REST — Rate limits  
    https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api

23. GitHub REST — Best practices  
    https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api

24. DORA — Software delivery performance metrics  
    https://dora.dev/guides/dora-metrics/

---

# 63. Связь с предыдущими Research Results

Это исследование следует читать совместно с:

```text
GitHub_Observatory_Temporal_Semantics_2026-09-24.md
GitHub_Observatory_Dynamic_Rendering_Research_2026-09-24.md
```

Вместе они формируют три слоя:

```text
WHEN
Temporal semantics
        ↓
WHAT
Expanded evidence & metrics
        ↓
HOW TO SEE
Dynamic rendering
```

Итоговая архитектурная цепочка:

```text
source evidence
→ temporally correct observations
→ semantic daily facts
→ derived portfolio analytics
→ reproducible visual presentation
```
