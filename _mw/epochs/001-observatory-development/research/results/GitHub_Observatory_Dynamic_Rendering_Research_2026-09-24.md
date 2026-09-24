# GitHub Observatory: динамический рендеринг, README-dashboard и GitHub Pages

**Дата:** 2026-09-24  
**Контекст:** развитие `ForestTiger-GH/github-observatory`

## Краткий вывод

Да, GitHub позволяет реализовать оба интересующих сценария:

1. **Файл, который визуально рендерится прямо в интерфейсе репозитория** — через `README.md`, SVG, PNG, CSV/TSV, PDF, Jupyter Notebook, Mermaid и ряд других поддерживаемых форматов.
2. **Автоматически обновляемая визуализация**, которая перестраивается каждый день на основе новых данных внутри репозитория — через GitHub Actions, генерирующий новый SVG/PNG/HTML/JSON после ежедневного сбора данных.

Для `github-observatory` оптимальная архитектура — двухслойная:

- **README + автоматически генерируемый SVG-dashboard** как мгновенная обложка и executive summary репозитория;
- **GitHub Pages** как полноценный интерактивный аналитический интерфейс с фильтрами, hover, переключателями периодов и drill-down.

Эта архитектура полностью укладывается в инфраструктуру GitHub и не требует отдельного сервера.

---

# 1. Что означает «рендериться на GitHub»

Важно различать два режима.

## 1.1. Рендеринг внутри интерфейса github.com

GitHub умеет сам отображать определённые типы файлов в браузере. Наиболее важные для Observatory:

| Формат | Поведение GitHub | Пригодность для Observatory |
|---|---|---|
| `README.md` | автоматически отображается на главной странице репозитория | отлично |
| `.svg` | отображается как векторное изображение | отлично |
| `.png`, `.jpg`, `.gif` | отображаются как изображения | хорошо |
| `.csv`, `.tsv` | отображаются как таблицы | уже полезно для сырых данных |
| `.pdf` | встроенный просмотр | хорошо для статических отчётов |
| `.ipynb` | статический рендер notebook | можно использовать |
| Mermaid | GitHub строит диаграммы | полезно для архитектурных схем |
| GeoJSON | карта | если появятся геоданные |
| STL | 3D-объект | для Observatory почти неактуально |
| `.html` | не превращается в полноценную исполняемую страницу внутри репозитория | нужен GitHub Pages |

Главная особенность — `README.md`. Он фактически может служить встроенной главной страницей репозитория.

В README можно вставлять изображения относительными путями, например:

```markdown
![Dashboard](./assets/generated/dashboard.svg)
```

GitHub автоматически подхватит актуальную версию файла из репозитория.

## 1.2. Настоящая веб-страница

Если требуется исполняемый HTML/CSS/JavaScript, интерактивные графики, фильтры, hover tooltip, переключатели и т. п., нужен **GitHub Pages**.

GitHub Pages публикует статический сайт из содержимого репозитория или из артефакта GitHub Actions.

То есть можно получить адрес вида:

```text
https://foresttiger-gh.github.io/github-observatory/
```

и разместить там полноценный dashboard.

---

# 2. Можно ли сделать динамическую картинку

Да.

Правильная модель для GitHub выглядит не так:

```text
Пользователь открыл README
        ↓
SVG сам полез в CSV
        ↓
сам себя перестроил
```

а так:

```text
Новый день данных
        ↓
GitHub Actions
        ↓
сбор CSV
        ↓
пересчёт метрик
        ↓
генерация SVG / PNG
        ↓
commit + push
        ↓
README автоматически показывает новую версию
```

Это полноценная динамическая визуализация во времени, просто вычисление выполняется не при каждом просмотре страницы, а при обновлении данных.

Для Observatory это даже предпочтительнее: визуализация становится воспроизводимым производным артефактом конкретного состояния данных.

---

# 3. Почему SVG — лучший базовый формат

Для Observatory я бы выбрал **SVG как основной формат dashboard**.

## Преимущества SVG

### 3.1. Векторное качество

SVG масштабируется без потери качества. Текст, линии и графики остаются идеально чёткими.

### 3.2. Хорошая совместимость с Git

SVG — текстовый XML. Git способен хранить изменения гораздо эффективнее, чем ежедневные новые версии бинарного PNG.

### 3.3. Малый размер

Для типичного dashboard SVG будет сравнительно лёгким.

### 3.4. Хорош для статической аналитической инфографики

Можно рисовать:

- KPI-карточки;
- линии и бары;
- heatmap;
- подписи;
- таблицы;
- статусы;
- мини-графики;
- sparklines;
- сравнительные блоки.

## Ограничение

GitHub не следует рассматривать SVG внутри репозитория как среду для произвольного JavaScript.

Поэтому SVG должен быть **предварительно сгенерированным представлением данных**, а не самоисполняющимся приложением.

---

# 4. Предлагаемая структура репозитория

Для `github-observatory` можно сделать следующую структуру:

```text
github-observatory/
│
├── README.md
│
├── assets/
│   └── generated/
│       ├── dashboard-light.svg
│       └── dashboard-dark.svg
│
├── dashboard/
│   ├── dashboard.json
│   └── README.md
│
├── scripts/
│   ├── collect.py
│   ├── observatory.py
│   ├── build_dashboard_model.py
│   └── render_dashboard.py
│
└── ForestTiger-GH/
    └── ...
```

`ForestTiger-GH/` остаётся каноническим хранилищем наблюдений.

`dashboard.json` — производная модель для визуализации.

`dashboard-light.svg` и `dashboard-dark.svg` — производные представления.

---

# 5. README как динамическая обложка Observatory

README можно один раз настроить так, чтобы он всегда показывал актуальный dashboard.

Например:

```html
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="./assets/generated/dashboard-dark.svg">
  <source media="(prefers-color-scheme: light)"
          srcset="./assets/generated/dashboard-light.svg">
  <img
    alt="GitHub Observatory dashboard"
    src="./assets/generated/dashboard-light.svg">
</picture>
```

Тогда:

- пользователю не нужно ничего запускать;
- README не нужно ежедневно переписывать;
- Action заменяет содержимое SVG;
- GitHub автоматически показывает новую версию.

Такой README становится своего рода стартовым экраном Observatory.

---

# 6. Как встроить это в текущий `collect.yml`

Текущий Observatory уже почти готов к такой архитектуре.

Workflow сейчас делает примерно следующее:

```text
02:00 UTC
   ↓
checkout
   ↓
Python
   ↓
collect.py
   ↓
commit observations
   ↓
git push
```

Для dashboard достаточно добавить генерацию после сбора данных.

Например:

```yaml
- name: Build dashboard model
  run: python scripts/build_dashboard_model.py

- name: Render dashboard
  run: python scripts/render_dashboard.py
```

Текущий staging использует:

```bash
git add ForestTiger-GH
```

Если dashboard находится за пределами `ForestTiger-GH/`, нужно расширить staging:

```bash
git add ForestTiger-GH dashboard assets/generated
```

---

# 7. Важный архитектурный нюанс: сырые данные и производные артефакты

`github-observatory` по своей природе является evidence store.

Поэтому канонические наблюдения должны быть важнее dashboard.

Плохая архитектура:

```text
collect
   ↓
render
   ↓
что-то сломалось
   ↓
нет commit вообще
```

Если упал matplotlib, SVG renderer или шаблон, нельзя допускать потери уникального дневного наблюдения.

Лучше разделить процесс:

```text
COLLECT
   │
   ├── generate raw observations
   │
   ├── validate
   │
   └── commit raw observations
   │
   ▼
RENDER
   │
   ├── derive dashboard model
   ├── generate SVG
   └── commit derived artifacts
```

Тогда возможны два commit:

```text
Collect repository observations 2026-09-24
Update Observatory dashboard 2026-09-24
```

Если рендер сломается — сырые данные уже сохранены.

Для исследовательского хранилища это более надёжная архитектура.

---

# 8. Что должен показывать dashboard

Оптимально сделать dashboard компактным, но содержательным.

## 8.1. Верхний блок

```text
GITHUB OBSERVATORY
Data through 23 Sep 2026 UTC
```

## 8.2. KPI

Например:

- Repositories
- Views today
- Repo-level unique viewers
- Commits today
- Changed-file occurrences
- Clones
- Collection errors

## 8.3. График трафика

Например 14 или 30 дней:

```text
VIEWS — LAST 14 DAYS
```

Можно добавить:

- total views;
- moving average;
- top day;
- latest day;
- day-over-day change.

## 8.4. График активности

```text
COMMITS — LAST 14 DAYS
```

Отдельно можно показать:

- commits;
- changed-file occurrences;
- active repositories.

## 8.5. Топ активных репозиториев

Например:

```text
TOP ACTIVE REPOSITORIES

tabularium              14
MADAR                    8
mandat-analytics         6
mandat-forecast          5
```

## 8.6. Рост корпуса

Например:

- изменение количества файлов;
- изменение размера;
- новые репозитории;
- новые языки;
- изменение числа commits в canonical history.

## 8.7. Статус коллектора

```text
Latest collection: 26 / 26 repositories
Errors: 0
```

Это особенно полезно: пользователь сразу понимает, можно ли доверять дневному срезу.

---

# 9. Семантика метрик: dashboard не должен искажать данные

Это критично для Observatory.

Dashboard должен наследовать семантику `SCHEMA.md`, а не создавать удобные, но неверные интерпретации.

## 9.1. Unique visitors

GitHub Traffic считает `uniques` отдельно для каждого репозитория.

Например:

```text
repo A: uniques = 1
repo B: uniques = 1
repo C: uniques = 1
```

Это не означает трёх разных людей.

Один человек мог посетить все три репозитория.

Поэтому нельзя просто писать:

```text
Visitors: 3
```

если это сумма `uniques`.

Можно использовать более аккуратные показатели.

### Вариант A

```text
Repo-level unique viewer observations: 3
```

### Вариант B

Показывать диапазон:

```text
Account-wide unique viewers:
1 ≤ viewers ≤ 3
```

где:

```text
lower bound = max(repo uniques)
upper bound = sum(repo uniques)
```

Это гораздо честнее.

Если трафик был только у одного репозитория, как 23 сентября у `mandat-forecast`, можно фактически получить точное число уникальных посетителей всей наблюдаемой совокупности.

---

# 10. `changed_file_occurrences` нельзя называть «изменённые файлы»

`activity.csv` хранит:

```text
changed_file_occurrences
```

Это сумма количества изменённых файлов по коммитам.

Она не является количеством уникальных файлов.

Например:

- файл A менялся в трёх коммитах;
- он может быть учтён трижды.

Поэтому подпись dashboard должна быть вроде:

```text
Changed-file occurrences
```

а не:

```text
Files changed
```

без уточнения.

---

# 11. Исторические данные должны пересчитываться

Observatory специально допускает пересмотр старых данных.

Например:

- merge может сделать старые commits reachable;
- rebase может изменить canonical history;
- GitHub Traffic некоторое время обновляет недавние дни.

Поэтому dashboard нельзя строить по модели:

```text
вчерашний SVG
   +
одна новая точка
```

Нужно каждый день заново читать канонические CSV и пересчитывать используемое окно:

```text
canonical CSV
      ↓
recompute last 30 days
      ↓
new dashboard model
      ↓
new SVG
```

Так dashboard всегда остаётся согласован с текущим состоянием Observatory.

---

# 12. GitHub Pages как второй уровень

README-dashboard хорош как мгновенная обложка.

Но для полноценной аналитики лучше добавить GitHub Pages.

## Возможности Pages

На Pages можно реализовать:

- интерактивные line charts;
- bar charts;
- hover tooltips;
- переключение 7 / 14 / 30 / 90 дней;
- фильтр репозиториев;
- поиск;
- сортировку;
- drill-down по конкретному репозиторию;
- переключение Views / Clones / Commits / Files;
- heatmap активности;
- dark mode;
- карточки KPI;
- таблицу последних изменений.

Это уже полноценный Observatory Dashboard.

---

# 13. Два способа строить Pages

## 13.1. Build-time dashboard

Action ежедневно генерирует:

```text
index.html
summary.json
views.json
repos.json
```

и публикует их.

Плюсы:

- максимально воспроизводимо;
- минимум клиентской логики;
- простая отладка.

## 13.2. Client-side dashboard

На Pages лежат постоянные:

```text
index.html
app.js
```

а браузер читает опубликованный `dashboard.json` и динамически строит графики.

Плюсы:

- интерактивность;
- можно фильтровать данные;
- не требуется перестраивать весь HTML ради каждого представления.

## Предпочтительный гибрид

Для Observatory наиболее сильная схема:

```text
Python Action
   ↓
raw CSV
   ↓
derived dashboard.json
   ↓
GitHub Pages
   ↓
JavaScript visualization
```

Python отвечает за семантически корректную подготовку метрик.

JavaScript отвечает только за представление.

---

# 14. Не давать браузеру доступ к токену

Нельзя помещать `OBSERVATORY_TOKEN`, PAT или другой секрет в JavaScript Pages.

Клиентский JavaScript доступен любому посетителю.

Правильная схема:

```text
GitHub Action
   ↓
private API access
   ↓
aggregated safe JSON
   ↓
public/static Pages
```

То есть Pages получает только уже подготовленные безопасные данные.

---

# 15. Коварный момент с `GITHUB_TOKEN`

Есть важная особенность GitHub Actions.

События, созданные workflow через стандартный `GITHUB_TOKEN`, обычно не запускают новый workflow по `push`.

Это защита от бесконечных рекурсивных цепочек.

Поэтому схема:

```text
collect.yml
   ↓
git push by GITHUB_TOKEN
   ↓
pages.yml on: push
```

может не сработать так, как ожидается.

Надёжнее:

```text
collect.yml
   │
   ├── collect
   ├── commit observations
   ├── build dashboard
   └── deploy Pages
```

Либо использовать явно спроектированный chaining-механизм вроде `workflow_run`.

---

# 16. Стоит изменить время scheduled run

Сейчас Observatory запускается ровно:

```yaml
cron: "0 2 * * *"
```

То есть в 02:00 UTC.

Scheduled GitHub Actions могут задерживаться в периоды высокой нагрузки, особенно около начала часа.

Содержательно Observatory не нужен именно `02:00:00`.

Главное — запуск после завершения UTC-дня с достаточным буфером.

Поэтому можно использовать, например:

```yaml
cron: "17 2 * * *"
```

То есть 02:17 UTC.

Это сохраняет модель данных, но уменьшает вероятность попадания в типичный пик scheduled jobs.

Если время изменить, нужно синхронно обновить `SCHEMA.md`.

---

# 17. Предпочтительная итоговая архитектура

```text
                         GitHub APIs
                             │
                             ▼
                      scripts/collect.py
                             │
                             ▼
                   canonical CSV observations
                             │
                      COMMIT RAW DATA
                             │
                             ▼
               scripts/build_dashboard_model.py
                             │
                       dashboard.json
                             │
               ┌─────────────┴──────────────┐
               ▼                            ▼
     render_dashboard.py               Pages build
               │                            │
               ▼                            ▼
 dashboard-light.svg              interactive dashboard
 dashboard-dark.svg
               │
         COMMIT DERIVED
               │
               ▼
            README.md
               │
               ▼
     visible immediately on
        repository homepage
```

---

# 18. Возможный вид README-dashboard

```text
┌──────────────────────────────────────────────────────────────┐
│                     GITHUB OBSERVATORY                       │
│                 Data through 23 Sep 2026 UTC                │
│                                                              │
│  26              47              41              0           │
│  Repositories    Views           Commits         Errors      │
│                                                              │
│  ─────────────── VIEWS — LAST 14 DAYS ──────────────────    │
│                                                              │
│   719 ┤       ●                                               │
│       │       │      ●                                        │
│   547 ┤ ...                     ●                             │
│       │                                                       │
│    47 ┤                              ●                        │
│       └────────────────────────────────────────────────       │
│                                                              │
│  TOP ACTIVE REPOSITORIES                                     │
│                                                              │
│  tabularium                         14                        │
│  MADAR                               8                        │
│  mandat-analytics                    6                        │
│  mandat-forecast                     5                        │
│                                                              │
│  Latest collection: 26 / 26 repositories                    │
│  See SCHEMA.md for metric semantics                          │
└──────────────────────────────────────────────────────────────┘
```

README может стать фактически мгновенным аналитическим summary всей экосистемы.

---

# 19. Практическая рекомендация

Для `github-observatory` имеет смысл реализовывать систему в три этапа.

## Этап 1 — README-dashboard

Минимально жизнеспособная реализация:

- `build_dashboard_model.py`;
- `render_dashboard.py`;
- `dashboard-light.svg`;
- `dashboard-dark.svg`;
- вставка `<picture>` в README;
- ежедневный rebuild после сбора данных.

Это даст максимальный эффект при минимальной сложности.

## Этап 2 — semantic dashboard model

Создать канонический производный:

```text
dashboard/dashboard.json
```

В нём хранить уже интерпретированные метрики:

- latest closed day;
- collection completeness;
- views;
- unique viewer bounds;
- commits;
- changed-file occurrences;
- clones;
- active repository count;
- top repositories;
- repo growth;
- historical series.

SVG и Pages должны читать одну и ту же модель.

Это предотвращает расхождение логики между разными визуализациями.

## Этап 3 — GitHub Pages

Поверх `dashboard.json` построить интерактивный интерфейс.

README остаётся summary.

Pages становится рабочей аналитической панелью.

---

# 20. Итоговое решение

Для Observatory не нужно выбирать между «картинкой» и «сайтом».

Сильнее всего сделать оба уровня:

### Уровень 1 — README

```text
README.md
   ↓
latest generated SVG
```

Плюсы:

- моментально видно при открытии репозитория;
- нулевое действие со стороны пользователя;
- красиво;
- очень надёжно;
- полностью нативно для GitHub.

### Уровень 2 — GitHub Pages

```text
Full Observatory Dashboard
```

Плюсы:

- интерактивность;
- фильтры;
- детализация;
- исторические сравнения;
- drill-down;
- полноценное аналитическое использование.

В итоге `github-observatory` становится не просто репозиторием с CSV, а **самовизуализирующейся наблюдательной системой**:

```text
наблюдение
→ сохранение
→ интерпретация
→ визуализация
→ публикация
```

При этом канонические данные остаются отделены от производных артефактов, а визуализация полностью воспроизводима из сохранённого evidence layer.
