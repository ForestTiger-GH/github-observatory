# GitHub Observatory: согласование временной семантики данных

**Дата:** 2026-09-24  
**Контекст:** уточнение временной модели `ForestTiger-GH/github-observatory`

## Краткий вывод

Если сбор Observatory выполняется утром **24 сентября**, то временная модель должна быть разделена на два основных слоя:

1. **T — текущая дата / момент наблюдения:** показатели состояния, которые GitHub возвращает «сейчас».
2. **T−1 — последний полностью завершённый календарный день:** дневные потоки активности и трафика.

Для сбора 24 сентября правильная семантика:

| Семейство | Дата в данных | Семантика |
|---|---:|---|
| `repository.csv` | **24.09** | состояние репозитория на момент наблюдения |
| `languages.csv` | **24.09** | языковой состав на момент наблюдения |
| `_collection/runs.csv` | **24.09** | запуск коллектора, произошедший 24.09 |
| `_collection/repository-status.csv` | **24.09** | статус этого запуска |
| `traffic/referrers.csv` | **24.09** | rolling snapshot, наблюдавшийся 24.09 |
| `traffic/paths.csv` | **24.09** | rolling snapshot, наблюдавшийся 24.09 |
| `activity.csv` | **23.09** | активность за последний завершённый день |
| `traffic/views.csv` | **23.09** | просмотры за последний завершённый день |
| `traffic/clones.csv` | **23.09** | клонирования за последний завершённый день |

Иными словами:

```text
SNAPSHOTS / OBSERVATIONS → T
DAILY FLOWS              → T−1
```

---

# 1. Почему `repository.csv` должен иметь дату текущего дня

`repository.csv` содержит показатели:

- `size_kb`;
- `files`;
- `commits`;
- `stars`;
- `forks`;
- `subscribers`;
- `updated_at`;
- `pushed_at`;
- другие метаданные состояния репозитория.

Эти значения не являются итогами «за предыдущий день».

Они означают:

> GitHub показал такое состояние репозитория в момент запроса.

Если запрос выполнен 24 сентября, логичная запись:

```text
data_date_utc = 2026-09-24
observed_at   = 2026-09-24T...
```

А не:

```text
data_date_utc = 2026-09-23
observed_at   = 2026-09-24T...
```

То есть для snapshot-метрик дата должна отражать **дату наблюдения**, а не последний закрытый день.

В перспективе поле `data_date_utc` для таких таблиц можно даже переименовать в:

```text
snapshot_date_utc
```

но это уже отдельное изменение схемы.

---

# 2. `languages.csv` — тоже текущий snapshot

Языковой состав также является состоянием репозитория на момент запроса.

Например:

```text
Python       100000 bytes
Markdown      40000 bytes
JavaScript    10000 bytes
```

если эти данные получены 24 сентября, они относятся к 24 сентября.

Это не показатель «за 23 сентября».

Поэтому:

```text
languages.csv → 24.09
```

---

# 3. `_collection/runs.csv` должен отражать фактическую дату запуска

`runs.csv` — это технический журнал выполнения коллектора.

Если запуск происходит 24 сентября, строка должна быть привязана к 24 сентября.

Логичная схема:

```text
run_date_utc = 2026-09-24
started_at   = 2026-09-24T...
finished_at  = 2026-09-24T...
```

Даже если поле пока называется `data_date_utc`, его значение в таком случае должно быть 24.09.

В дальнейшем можно рассмотреть переименование:

```text
data_date_utc
→ run_date_utc
```

но само поведение менять нужно уже на уровне значения даты.

---

# 4. `_collection/repository-status.csv` следует той же логике

`repository-status.csv` описывает состояние конкретного запуска:

- получилось ли собрать metadata;
- получилось ли собрать languages;
- получилось ли собрать activity;
- получилось ли собрать traffic;
- были ли ошибки.

Поэтому если сам запуск относится к 24 сентября, status-строки также должны быть датированы 24 сентября.

---

# 5. `activity.csv` остаётся на предыдущем дне

Здесь текущая логика правильная.

Если сбор выполняется утром 24 сентября, то последний полностью завершённый UTC-день — 23 сентября.

Поэтому:

```text
activity_date_utc = 2026-09-23
```

означает:

> активность, чей Git `committedDate` попадает в календарные сутки 23 сентября UTC.

То есть:

```text
2026-09-23 00:00 UTC
        ↓
2026-09-24 00:00 UTC
```

Это настоящий дневной поток.

Дополнительный лаг до 22 сентября не нужен.

---

# 6. `views.csv` и `clones.csv` также остаются на предыдущем дне

Трафик GitHub разбивается по календарным UTC-дням.

Поэтому при сборе 24 сентября:

```text
traffic_date_utc = 2026-09-23
```

для:

```text
views.csv
clones.csv
```

означает:

> итог за последний полностью завершённый день.

Это согласуется с `activity.csv`.

Таким образом эти три семейства становятся единым блоком:

```text
LATEST COMPLETE DAY — 23 Sep 2026
├── activity
├── views
└── clones
```

---

# 7. Итоговая модель T / T−1

Если сбор выполняется 24 сентября:

```text
24 Sep
│
├── CURRENT STATE / OBSERVATION
│   ├── repository.csv
│   ├── languages.csv
│   ├── runs.csv
│   ├── repository-status.csv
│   ├── referrers.csv
│   └── paths.csv
│
└── LAST COMPLETE DAY
    ├── activity.csv
    ├── views.csv
    └── clones.csv
```

То есть:

```text
T   = состояние, наблюдаемое сейчас
T−1 = завершённая дневная активность
```

Это значительно проще и интуитивнее, чем привязывать почти всё к последнему закрытому дню.

---

# 8. Что такое `referrers.csv`

`referrers.csv` отвечает на вопрос:

> откуда люди пришли в репозиторий?

Например:

```text
Google
reddit.com
stackoverflow.com
github.com
```

GitHub возвращает не дневную историю referrer'ов, а **текущую таблицу наиболее популярных источников переходов за rolling window последних дней**.

Поэтому это не показатель:

```text
Google за 23 сентября = 5
```

а скорее:

```text
На момент наблюдения 24 сентября:
Google входит в top referrers текущего rolling window
```

Следовательно, это snapshot.

Правильная дата:

```text
snapshot_date_utc = 2026-09-24
observed_at       = 2026-09-24T...
```

---

# 9. Что такое `paths.csv`

`paths.csv` отвечает на другой вопрос:

> какие страницы или файлы внутри репозитория люди смотрели чаще всего?

Например:

```text
/ForestTiger-GH/repo
/ForestTiger-GH/repo/blob/main/README.md
/ForestTiger-GH/repo/tree/main/docs
```

То есть:

```text
referrers = ОТКУДА пришли
paths     = КУДА внутри репозитория пошли
```

`paths.csv`, как и `referrers.csv`, является rolling snapshot, а не дневным потоком.

Следовательно, его также логично датировать днём наблюдения:

```text
24.09
```

---

# 10. Почему `referrers` и `paths` не надо смешивать с `views` и `clones`

Хотя все четыре семейства лежат внутри `traffic/`, у них разные временные смыслы.

## Daily traffic

```text
views.csv
clones.csv
```

Это календарные дневные ряды:

```text
23 Sep
24 Sep
25 Sep
...
```

## Rolling traffic snapshots

```text
referrers.csv
paths.csv
```

Это снимки текущего rolling window:

```text
observed 24 Sep
observed 25 Sep
observed 26 Sep
...
```

Поэтому в документации их полезно явно разделять.

Например:

```text
traffic/
├── daily/
│   ├── views.csv
│   └── clones.csv
│
└── rolling/
    ├── referrers.csv
    └── paths.csv
```

Физически менять директории необязательно, но семантическое разделение желательно закрепить в `SCHEMA.md`.

---

# 11. Возможное представление в dashboard

Будущий dashboard можно оформить очень просто:

```text
GITHUB OBSERVATORY
Observed 24 Sep 2026

CURRENT STATE
Repositories      26
Files           5,421
Size           84 MB
Canonical commits ...
Languages       ...

LATEST COMPLETE DAY — 23 Sep 2026
Views             47
Clones             3
Commits            41
Changed-file occurrences 699
```

Это сразу показывает пользователю две разные временные категории.

Не требуется объяснять сложную внутреннюю механику Observatory.

---

# 12. Изменения в коде

На уровне логики полезно разделить две даты.

Например:

```python
observation_date = started.astimezone(UTC).date()
latest_complete_day = observation_date - dt.timedelta(days=1)
```

Далее:

```text
observation_date
```

используется для:

```text
repository.csv
languages.csv
runs.csv
repository-status.csv
referrers.csv
paths.csv
```

А:

```text
latest_complete_day
```

используется для:

```text
activity.csv
views.csv
clones.csv
```

Это значительно яснее текущей перегруженной переменной `data_date`.

---

# 13. Рекомендуемые имена переменных

Вместо:

```python
cutoff_date
data_date
```

лучше использовать:

```python
observation_date
latest_complete_day
```

При необходимости:

```python
run_date = observation_date
snapshot_date = observation_date
daily_cutoff_date = latest_complete_day
```

Так код сам объясняет временную модель.

---

# 14. Возможное уточнение схемы полей

В перспективе можно разграничить сами поля:

## Snapshot tables

```text
snapshot_date_utc
observed_at
```

для:

- `repository.csv`;
- `languages.csv`;
- `referrers.csv`;
- `paths.csv`.

## Daily flow tables

```text
activity_date_utc
traffic_date_utc
```

для:

- `activity.csv`;
- `views.csv`;
- `clones.csv`.

## Collection metadata

```text
run_date_utc
started_at
finished_at
```

для:

- `runs.csv`;
- `repository-status.csv`.

Это было бы ещё чище, но не является обязательным условием для исправления текущей семантики.

---

# 15. Финальная временная классификация

Для утреннего сбора 24 сентября:

| Файл | Дата | Тип |
|---|---:|---|
| `repository.csv` | **24.09** | current snapshot |
| `languages.csv` | **24.09** | current snapshot |
| `_collection/runs.csv` | **24.09** | collection event |
| `_collection/repository-status.csv` | **24.09** | collection event/status |
| `traffic/referrers.csv` | **24.09** | rolling snapshot |
| `traffic/paths.csv` | **24.09** | rolling snapshot |
| `activity.csv` | **23.09** | daily flow |
| `traffic/views.csv` | **23.09** | daily flow |
| `traffic/clones.csv` | **23.09** | daily flow |

Главное правило:

```text
SNAPSHOTS / OBSERVATIONS → T
DAILY FLOWS              → T−1
```

Это и следует считать базовой временной семантикой GitHub Observatory.
