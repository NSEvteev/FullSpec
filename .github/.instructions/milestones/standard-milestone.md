---
description: Стандарт работы с GitHub Milestones — формат версии, описание, дата завершения, привязка Issue.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/milestones/README.md
---

# Стандарт управления GitHub Milestones

Версия стандарта: 1.1

Правила жизненного цикла, создания и управления вехами (Milestones) для организации работы по релизам.

**Полезные ссылки:**
- [Инструкции Milestones](./README.md)
- [Issues](../issues/standard-issue.md) — связь Issues с Milestones
- [Releases](../releases/standard-release.md) — связь Milestones с Releases

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-milestone.md](./validation-milestone.md) |
| Создание | [create-milestone.md](./create-milestone.md) |
| Модификация | [modify-milestone.md](./modify-milestone.md) |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Свойства Milestone](#2-свойства-milestone)
- [3. Жизненный цикл](#3-жизненный-цикл)
- [4. Версионирование (SemVer)](#4-версионирование-semver)
  - [Правила инкремента версий](#правила-инкремента-версий)
  - [Автоматическое определение версии](#автоматическое-определение-версии)
  - [Pre-release версии](#pre-release-версии)
  - [Специальные случаи](#специальные-случаи)
- [5. Правила создания](#5-правила-создания)
  - [Title](#title)
  - [Description](#description)
  - [Due Date](#due-date)
- [6. Связь с Issues](#6-связь-с-issues)
- [7. Связь с Releases](#7-связь-с-releases)
- [8. Закрытие Milestone](#8-закрытие-milestone)
- [9. CLI команды](#9-cli-команды)
- [10. Метрики и отчётность](#10-метрики-и-отчётность)

---

## 1. Назначение

GitHub Milestones — система группировки задач (Issues) по целям и релизам.

> **Почему без спринтов?** При разработке с LLM ключевую роль играют целевые точки (milestones) — конкретные версии и цели, а не временные итерации. Работа ведётся до достижения результата, а не до окончания двухнедельного окна. Спринты допустимы, но этот стандарт их не предполагает.

> **Почему без Roadmap Milestones?** При автоматизации с LLM каждый Milestone напрямую связан с версией продукта и GitHub Release. Закрытие Milestone → автоматическая сборка Release с участием LLM. Roadmap-цели (MVP, Public Beta) управляются через GitHub Projects или Issues с labels, а не через Milestones. Roadmap Milestones допустимы, но этот стандарт их не предполагает.

**Применяется к:**
- Релизы (версии продукта)

**Цель:**
- Группировка Issues по целевой версии
- Визуализация прогресса (% выполнения)
- Связь задач с релизами через автоматическую сборку Release

**Принципы:**
- Каждый Milestone = одна версия продукта (vX.Y.Z)
- Issue может принадлежать ТОЛЬКО одному Milestone
- Milestone закрывается только когда все Issues завершены
- Закрытие Milestone → создание GitHub Release

---

## 2. Свойства Milestone

**Базовые свойства:**

| Свойство | Тип | Обязательно | Описание | Как установить |
|----------|-----|-------------|----------|----------------|
| `number` | int | авто | Уникальный номер (генерируется автоматически) | — |
| `title` | string | да | Название (релиз/цель) | `--title` |
| `description` | markdown | да | Описание цели, критерии готовности | `--description` |
| `state` | enum | авто | `open` / `closed` | `gh api` |
| `due_on` | datetime | да | Дедлайн (срок завершения) | `--due-date` |
| `created_at` | datetime | авто | Дата создания | — |
| `updated_at` | datetime | авто | Дата последнего обновления | — |
| `closed_at` | datetime | авто | Дата закрытия | — |

**Метрики (авто-рассчитываются):**

| Метрика | Описание | Как получить |
|---------|----------|--------------|
| `open_issues` | Количество открытых Issues | `gh api repos/{owner}/{repo}/milestones/{number}` |
| `closed_issues` | Количество закрытых Issues | `gh api repos/{owner}/{repo}/milestones/{number}` |
| `progress` | Процент выполнения (%) | `(closed / total) * 100` |

**Примеры:**

```json
{
  "number": 3,
  "title": "v1.0.0",
  "state": "open",
  "description": "Первый стабильный релиз\n\n## Критерии готовности\n- [ ] MVP реализован\n- [ ] Тесты >80%\n",
  "due_on": "2025-03-15T23:59:59Z",
  "open_issues": 7,
  "closed_issues": 3,
  "progress": 30
}
```

---

## 3. Жизненный цикл

```
┌─────────────┐
│   СОЗДАНИЕ  │  gh api POST /repos/{owner}/{repo}/milestones
└──────┬──────┘
       │
       ├─ Установка: title, description, due_on
       │
       v
┌─────────────┐
│  ОТКРЫТ     │  state: open
│  (ACTIVE)   │
└──────┬──────┘
       │
       ├─ Добавление Issues: gh issue edit {number} --milestone "{title}"
       │
       v
┌─────────────┐
│  В РАБОТЕ   │  Прогресс: closed_issues / total_issues
└──────┬──────┘
       │
       ├─ Issues закрываются по мере завершения
       │
       v
┌─────────────┐
│  ЗАВЕРШЁН   │  Все Issues закрыты (100%)
└──────┬──────┘
       │
       ├─ Закрытие milestone: gh api PATCH /repos/{owner}/{repo}/milestones/{number} -f state=closed
       │
       v
┌─────────────┐
│  ЗАКРЫТ     │  state: closed
└─────────────┘
       │
       ├─ Создание Release: gh release create v1.0.0
       │
       v
┌─────────────┐
│  RELEASE    │  GitHub Release создан
└─────────────┘
```

**Ключевые этапы:**

1. **СОЗДАНИЕ** — Milestone создаётся через `gh api`
2. **ОТКРЫТ (ACTIVE)** — Issues добавляются, работа ведётся
3. **В РАБОТЕ** — Issues закрываются по мере выполнения
4. **ЗАВЕРШЁН** — Все Issues закрыты (100%)
5. **ЗАКРЫТ** — Milestone закрывается через API
6. **RELEASE** — Создаётся GitHub Release с тегом

**Переходы:**

- `open` → `closed` — вручную, когда все Issues завершены
- `closed` → `open` — вручную, если требуется переоткрыть

---

## 4. Версионирование (SemVer)

Milestone следует [Semantic Versioning 2.0.0](https://semver.org/). Версия определяется при создании Milestone и наследуется GitHub Release.

**Формат:** `vMAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

| Элемент | Правило | Пример |
|---------|---------|--------|
| `v` | Префикс (ОБЯЗАТЕЛЬНО) | `v` |
| `MAJOR` | Версия с breaking changes | `1` |
| `MINOR` | Версия с новой функциональностью (обратно совместимо) | `2` |
| `PATCH` | Версия с исправлениями (обратно совместимо) | `3` |
| `PRERELEASE` | Опциональный суффикс для pre-release | `-alpha`, `-beta.1`, `-rc.2` |
| `BUILD` | Опциональный build metadata | `+20250315` |

**Примеры:**
- `v1.0.0` — первый стабильный релиз
- `v1.1.0` — добавлена новая функциональность
- `v1.1.1` — исправлен баг
- `v2.0.0` — breaking changes (несовместимо с v1.x.x)
- `v1.0.0-alpha` — alpha-версия перед v1.0.0
- `v1.0.0-beta.2` — вторая beta-версия
- `v1.0.0-rc.1` — первый release candidate

### Правила инкремента версий

**MAJOR (X.0.0):** Увеличивается при breaking changes.

**Breaking changes — изменения, которые:**
- Нарушают обратную совместимость API (изменился формат запроса/ответа)
- Требуют изменений от пользователей/клиентов API
- Удаляют публичные методы/эндпоинты
- Меняют поведение существующих методов несовместимым образом

**Примеры:**
- Удаление эндпоинта `DELETE /api/v1/users`
- Изменение формата ответа `{ "user": {} }` → `{ "data": {} }`
- Переименование обязательного поля в запросе

**MINOR (x.Y.0):** Увеличивается при добавлении новой функциональности (обратно совместимо).

**Новая функциональность — изменения, которые:**
- Добавляют новые эндпоинты/методы
- Добавляют опциональные параметры
- Добавляют новые поля в ответ (не удаляя старые)
- Улучшают существующую функциональность без нарушения совместимости

**Примеры:**
- Добавление эндпоинта `POST /api/v1/auth/refresh`
- Добавление опционального параметра `?page_size=20`
- Добавление поля `created_at` в ответ (старые поля остаются)

**PATCH (x.y.Z):** Увеличивается при исправлении багов (обратно совместимо).

**Багфиксы — изменения, которые:**
- Исправляют некорректное поведение
- Не добавляют новой функциональности
- Не меняют публичный API

**Примеры:**
- Исправление ошибки 500 при загрузке файлов
- Исправление опечатки в тексте ошибки
- Исправление утечки памяти

**Когда сбрасывать младшие версии:**
- При инкременте MAJOR — MINOR и PATCH сбрасываются в 0: `v1.5.3` → `v2.0.0`
- При инкременте MINOR — PATCH сбрасывается в 0: `v1.5.3` → `v1.6.0`

### Автоматическое определение версии

Версия может быть определена автоматически по conventional commits в составе Milestone:

| Commit prefix | Инкремент | Пример |
|---------------|-----------|--------|
| `feat:` | MINOR | `feat: добавить OAuth2` |
| `fix:` | PATCH | `fix: исправить утечку памяти` |
| `BREAKING CHANGE:` в footer | MAJOR | Любой коммит с `BREAKING CHANGE:` в теле |
| `feat!:` / `fix!:` | MAJOR | `feat!: изменить формат API ответа` |

**Правило:** Итоговая версия определяется по НАИБОЛЬШЕМУ инкременту среди всех коммитов Milestone. Если есть хотя бы один `BREAKING CHANGE` — MAJOR, иначе если есть `feat:` — MINOR, иначе PATCH.

### Pre-release версии

**Формат:** `vX.Y.Z-{identifier}.{number}`

| Тип | Формат | Когда использовать | Пример |
|-----|--------|-------------------|--------|
| **alpha** | `vX.Y.Z-alpha` или `vX.Y.Z-alpha.N` | Ранняя версия для внутреннего тестирования | `v1.0.0-alpha`, `v1.0.0-alpha.1` |
| **beta** | `vX.Y.Z-beta` или `vX.Y.Z-beta.N` | Версия для публичного тестирования | `v1.0.0-beta`, `v1.0.0-beta.2` |
| **rc** | `vX.Y.Z-rc.N` | Release Candidate (финальное тестирование перед релизом) | `v1.0.0-rc.1` |

**Правила:**
- Pre-release идёт ПЕРЕД стабильным релизом: `v1.0.0-alpha` → `v1.0.0-beta` → `v1.0.0-rc.1` → `v1.0.0`
- Нумерация начинается с 1: `v1.0.0-alpha.1`, `v1.0.0-beta.1`
- Pre-release помечается флагом `--prerelease` при создании Release

**Сортировка версий (по возрастанию):**
```
v1.0.0-alpha
v1.0.0-alpha.1
v1.0.0-beta
v1.0.0-beta.1
v1.0.0-rc.1
v1.0.0
v1.0.1
v1.1.0
v2.0.0
```

### Специальные случаи

**Версия 0.x.x (начальная разработка):**
- До первого стабильного релиза используются версии `v0.x.x`
- Версия `v0.x.x` НЕ гарантирует обратную совместимость
- Первый стабильный релиз — `v1.0.0`

**Примеры:**
- `v0.1.0` — первая рабочая версия (MVP)
- `v0.2.0` — добавлена авторизация
- `v0.2.1` — исправлен баг в авторизации
- `v1.0.0` — первый стабильный релиз

**Build metadata (+):**
- Опционален для GitHub Releases. НЕ используется в стандартной практике проекта.
- Примеры применения (если потребуется в будущем): `v1.0.0+20250315`, `v1.0.0+sha.abc123`
- По умолчанию: тег Release содержит ТОЛЬКО `vX.Y.Z` без build metadata.

**Примеры:**
- `v1.0.0+20250315` — build от 15 марта 2025
- `v1.0.0+sha.abc123` — build с коммитом abc123

**Важно:** Build metadata НЕ используется для определения старшинства версий. `v1.0.0+build1` == `v1.0.0+build2`.

---

## 5. Правила создания

### Title

**Формат:** см. [§ 4. Версионирование (SemVer)](#4-версионирование-semver)

**Правила:**
- Уникальное в рамках репозитория
- Краткое (до 50 символов)
- Следует SemVer naming convention

### Description

**Минимальная структура:**

```markdown
## Цель

{Зачем создаётся этот Milestone, какая проблема решается}

## Критерии готовности

- [ ] {Критерий 1}
- [ ] {Критерий 2}

## Фокус

{Основные направления работы (опционально)}
```

**Пример:**

```markdown
## Цель

Релиз версии 1.0.0 — первый стабильный релиз проекта.

## Критерии готовности

- [ ] Все фичи MVP реализованы
- [ ] Тесты покрывают основную функциональность (>80%)
- [ ] Документация обновлена
- [ ] Нет критических багов

## Состав релиза

См. связанный [Release v1.0.0](../releases/v1.0.0.md)
```

### Due Date

**Формат:** ISO 8601 — `YYYY-MM-DDTHH:MM:SSZ`

**Правила:**

| Срок | Пример |
|------|--------|
| Планируемая дата релиза | `2025-03-15T23:59:59Z` |

> **Почему `23:59:59Z`?** Время `23:59:59` означает "конец дня" — весь указанный день включён в срок. GitHub UI отображает только дату, время используется для сортировки и API-фильтрации. Альтернатива: `00:00:00` следующего дня (эквивалентно по смыслу).

**Установка при создании:**

```bash
# Через gh api
gh api POST /repos/{owner}/{repo}/milestones \
  -f title="v1.0.0" \
  -f due_on="2025-03-15T23:59:59Z" \
  -f description="..."
```

**Изменение:**

```bash
# Через gh api
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f due_on="2025-04-01T23:59:59Z"
```

---

## 6. Связь с Issues

**SSOT:** [standard-issue.md § 9](../issues/standard-issue.md#9-связь-с-milestones)

Добавление, удаление и группировка Issues в Milestone — см. SSOT.

---

## 7. Связь с Releases

**SSOT:** [standard-release.md § 9–10](../releases/standard-release.md#9-подготовка-релиза)

Последовательность: создать Milestone → добавить Issues → закрыть Milestone → создать Release. Процесс, проверки и шаблон Release Notes — см. SSOT.

**Правила:**
- Каждый Milestone ДОЛЖЕН завершиться GitHub Release
- Milestone ДОЛЖЕН быть закрыт ПЕРЕД созданием Release
- В Release Notes ОБЯЗАТЕЛЬНА ссылка на Milestone

---

## 8. Закрытие Milestone

### Критерии закрытия

**Milestone готов к закрытию если:**

1. **Все Issues закрыты** — `open_issues = 0` (проверяется через API)
2. **Критерии готовности выполнены** (из Description, секция "Критерии готовности")
3. **Due date наступил ИЛИ до него осталось не более 2 дней** (проверка: `due_on - now() <= 2 days`)

**Проверка:**

```bash
# 1. Получить число открытых Issues
OPEN_COUNT=$(gh api repos/{owner}/{repo}/milestones/{number} -q '.open_issues')

# 2. Если OPEN_COUNT = 0 → Milestone готов к закрытию
if [ "$OPEN_COUNT" -eq 0 ]; then
  echo "Milestone готов к закрытию"
else
  echo "Есть открытые Issues: $OPEN_COUNT"
  # См. "Что делать с незавершёнными Issues"
fi
```

### Закрытие Milestone

**Через API:**

```bash
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f state=closed
```

**Переоткрытие (если нужно):**

```bash
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f state=open
```

### Что делать с незавершёнными Issues

**Если Milestone закрывается, но есть открытые Issues:**

1. **Оценить критичность:** Сравнить title/body Issues с секцией "Критерии готовности" в Description Milestone. Issue критичен, если он ПРЯМО упомянут в критериях готовности.
2. **Если НЕ критичные (не упомянуты в критериях готовности):**
   - Определить целевой Milestone:
     ```bash
     # Список открытых Milestones
     gh api repos/{owner}/{repo}/milestones -f state=open -q '.[].title'
     ```
   - Перенести Issue в выбранный Milestone:
     ```bash
     gh issue edit 123 --milestone "v1.1.0"
     ```
3. **Если критичные:**
   - НЕ закрывать Milestone
   - Продлить `due_on`:
     ```bash
     gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
       -f due_on="2025-04-01T23:59:59Z"
     ```

**Правило:** НЕ закрывать Milestone с открытыми Issues без переноса их в другой Milestone.

### Ретроспектива Milestone

После закрытия Milestone — анализ запланированного vs выполненного:

1. **Подсчёт:** сколько Issues было изначально vs сколько перенесено в другой Milestone
2. **Порог:** если >30% Issues перенесено — пересмотреть подход к планированию:
   - Scope следующего Milestone слишком большой?
   - Оценки сложности задач были занижены?
   - Были ли внешние блокеры?
3. **Действие:** скорректировать scope следующего Milestone на основе фактической пропускной способности

---

## 9. CLI команды

### Создание Milestone

**Через gh api:**

```bash
gh api POST /repos/{owner}/{repo}/milestones \
  -f title="v1.0.0" \
  -f description="## Цель\n\nПервый стабильный релиз\n\n## Критерии\n- [ ] MVP готов" \
  -f due_on="2025-03-15T23:59:59Z"
```

**Проверка перед созданием:**

```bash
# Проверить существование Milestone с таким же title
EXISTING=$(gh api repos/{owner}/{repo}/milestones -q '.[] | select(.title == "v1.0.0") | .number')
if [ -n "$EXISTING" ]; then
  echo "ERROR: Milestone с таким title уже существует (number: $EXISTING)"
  exit 1
fi
```

**Обработка ошибок:**

| Код ошибки | Причина | Решение |
|------------|---------|---------|
| `422 Unprocessable Entity` | Milestone с таким title уже существует | Использовать существующий или выбрать другой title |
| `400 Bad Request` | Невалидный формат `due_on` | Использовать ISO 8601: `YYYY-MM-DDTHH:MM:SSZ` |
| `403 Forbidden` | Нет прав на создание Milestone | Проверить доступ к репозиторию |

**Ответ (успех):**

```json
{
  "number": 3,
  "title": "v1.0.0",
  "state": "open",
  "due_on": "2025-03-15T23:59:59Z",
  "html_url": "https://github.com/owner/repo/milestone/3"
}
```

### Просмотр Milestones

```bash
# Список всех Milestones
gh api repos/{owner}/{repo}/milestones

# Только открытые
gh api repos/{owner}/{repo}/milestones -f state=open

# Только закрытые
gh api repos/{owner}/{repo}/milestones -f state=closed

# Сортировка по due_date
gh api repos/{owner}/{repo}/milestones -f sort=due_on -f direction=asc

# Детали конкретного Milestone
gh api repos/{owner}/{repo}/milestones/{number}
```

### Редактирование Milestone

```bash
# Изменить title
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f title="v1.1.0"

# Изменить description
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f description="Обновлённое описание"

# Изменить due_date
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f due_on="2025-04-01T23:59:59Z"

# Закрыть Milestone
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f state=closed

# Переоткрыть Milestone
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f state=open
```

### Удаление Milestone

**Когда можно удалить:**
- Milestone создан по ошибке (без Issues)
- Milestone больше не актуален И все Issues перенесены

**Когда НЕЛЬЗЯ удалить:**
- Milestone связан с GitHub Release (проверить: есть ли Release с тегом, совпадающим с title Milestone)
- Milestone содержит Issues (`open_issues > 0` ИЛИ `closed_issues > 0`)

**Шаги перед удалением:**

```bash
# 1. Проверить наличие Issues
gh api repos/{owner}/{repo}/milestones/{number} -q '.open_issues, .closed_issues'

# 2. Если Issues есть → перенести в другой Milestone ИЛИ удалить Milestone из Issues
gh issue edit 123 --milestone ""

# 3. Удалить Milestone
gh api DELETE /repos/{owner}/{repo}/milestones/{number}
```

**Важно:**
- Удаление Milestone НЕ удаляет Issues
- Issues остаются без Milestone (`milestone: null`)

### Получение Issues в Milestone

```bash
# Через gh issue list
gh issue list --milestone "v1.0.0"

# Через gh api
gh api repos/{owner}/{repo}/milestones/{number} \
  -q '.open_issues, .closed_issues'
```

---

## 10. Метрики и отчётность

### Прогресс Milestone

**Формула:**

```
progress = (closed_issues / total_issues) * 100
```

**Получить через API:**

```bash
gh api repos/{owner}/{repo}/milestones/{number} \
  -q '{
    title: .title,
    progress: ((.closed_issues / (.open_issues + .closed_issues)) * 100),
    open: .open_issues,
    closed: .closed_issues
  }'
```

**Пример вывода:**

```json
{
  "title": "v1.0.0",
  "progress": 60,
  "open": 4,
  "closed": 6
}
```

### Просроченные Milestones

**Найти Milestones с `due_on` в прошлом:**

```bash
gh api repos/{owner}/{repo}/milestones -f state=open \
  -q '.[] | select(.due_on < now) | {title, due_on, open_issues}'
```

### Отчёт по Milestone

**Пример отчёта:**

```markdown
# 📋 Отчёт: v1.0.0

**Статус:** Завершён
**Прогресс:** 10/10 Issues (100%)
**Due Date:** 2025-03-15

## Завершённые Issues

- #123 Добавить OAuth2
- #124 Обновить API до v2
- #125 Исправить ошибку загрузки файлов

## Незавершённые Issues

*Нет*

## Следующий Milestone

[v1.1.0](https://github.com/owner/repo/milestone/4)
```

**Генерация через скрипт:**

```bash
# Будущий скрипт: .github/.instructions/.scripts/milestone-report.py
python .github/.instructions/.scripts/milestone-report.py --milestone 3
```

---

