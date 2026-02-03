---
description: Процесс работы с GitHub Milestones
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/milestones/README.md
---

# Стандарт управления GitHub Milestones

Версия стандарта: 1.0

Правила жизненного цикла, создания и управления вехами (Milestones) для организации работы по спринтам и релизам.

**Полезные ссылки:**
- [Инструкции Milestones](./README.md)
- [Issues](../issues/standard-issue.md) — связь Issues с Milestones
- [Releases](../releases/standard-release.md) — связь Milestones с Releases

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Будет создан* |
| Создание | *Будет создан* |
| Модификация | *Будет создан* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Свойства Milestone](#2-свойства-milestone)
- [3. Типы Milestones](#3-типы-milestones)
- [4. Жизненный цикл](#4-жизненный-цикл)
- [5. Правила именования](#5-правила-именования)
  - [Sprint Milestones](#sprint-milestones)
  - [Release Milestones](#release-milestones)
  - [Roadmap Milestones](#roadmap-milestones)
- [6. Правила создания](#6-правила-создания)
  - [Title](#title)
  - [Description](#description)
  - [Due Date](#due-date)
- [7. Связь с Issues](#7-связь-с-issues)
- [8. Связь с Releases](#8-связь-с-releases)
- [9. Закрытие Milestone](#9-закрытие-milestone)
- [10. CLI команды](#10-cli-команды)
- [11. Метрики и отчётность](#11-метрики-и-отчётность)

---

## 1. Назначение

GitHub Milestones — система группировки задач (Issues) по целям, спринтам или релизам.

**Применяется к:**
- Спринты (итерации разработки)
- Релизы (версии продукта)
- Долгосрочные цели (roadmap)

**Цель:**
- Организация работы по временным отрезкам
- Группировка Issues по общей цели
- Визуализация прогресса (% выполнения)
- Связь задач с релизами

**Принципы:**
- Каждый Milestone имеет чёткую цель и срок
- Issue может принадлежать ТОЛЬКО одному Milestone
- Milestone закрывается только когда все Issues завершены
- Milestone связывается с Release при создании версии

---

## 2. Свойства Milestone

**Базовые свойства:**

| Свойство | Тип | Обязательно | Описание | Как установить |
|----------|-----|-------------|----------|----------------|
| `number` | int | авто | Уникальный номер (генерируется автоматически) | — |
| `title` | string | да | Название (спринт/релиз/цель) | `--title` |
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
  "number": 5,
  "title": "Sprint 2025-W05",
  "state": "open",
  "description": "Фокус: авторизация и API v2\n\n## Цели\n- [ ] Реализовать OAuth2\n- [ ] Обновить API до v2\n",
  "due_on": "2025-02-09T23:59:59Z",
  "open_issues": 7,
  "closed_issues": 3,
  "progress": 30
}
```

---

## 3. Типы Milestones

| Тип | Цель | Срок | Примеры |
|-----|------|------|---------|
| **Sprint** | Итерация разработки | 1-2 недели | `Sprint 2025-W05`, `Sprint 12` |
| **Release** | Релиз версии продукта | Зависит от roadmap | `v1.0.0`, `v2.0 Beta`, `Q1 2025 Release` |
| **Roadmap** | Долгосрочная цель | 1-3 месяца | `MVP`, `Public Beta`, `Q2 Refactoring` |

**Как определить тип:**

1. **Sprint** — если:
   - Фокус на итеративной разработке
   - Четкий временной интервал (1-2 недели)
   - Группировка задач для команды
   - **Naming:** `Sprint YYYY-WXX` (год-неделя) или `Sprint {N}`

2. **Release** — если:
   - Milestone связан с версией продукта
   - Завершение milestone → создание GitHub Release
   - **Naming:** следует [SemVer](https://semver.org/) — `vX.Y.Z`

3. **Roadmap** — если:
   - Долгосрочная цель (> 1 месяца)
   - Группировка фич для крупного этапа
   - **Naming:** описательное имя — `MVP`, `Public Beta`, `Q2 2025`

---

## 4. Жизненный цикл

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
       ├─ (Опционально) Создание Release: gh release create v1.0.0
       │
       v
┌─────────────┐
│  RELEASE    │  Связан с GitHub Release
└─────────────┘
```

**Ключевые этапы:**

1. **СОЗДАНИЕ** — Milestone создаётся через `gh api`
2. **ОТКРЫТ (ACTIVE)** — Issues добавляются, работа ведётся
3. **В РАБОТЕ** — Issues закрываются по мере выполнения
4. **ЗАВЕРШЁН** — Все Issues закрыты (100%)
5. **ЗАКРЫТ** — Milestone закрывается через API
6. **RELEASE** — (Опционально) Создаётся GitHub Release с тегом

**Переходы:**

- `open` → `closed` — вручную, когда все Issues завершены
- `closed` → `open` — вручную, если требуется переоткрыть

---

## 5. Правила именования

### Sprint Milestones

**Формат 1 (рекомендуется):** `Sprint YYYY-WXX`

| Элемент | Правило | Пример |
|---------|---------|--------|
| `YYYY` | Год (4 цифры) | `2025` |
| `-W` | Разделитель "Week" | `-W` |
| `XX` | Номер недели по ISO 8601 (01-53) | `05` (5-я неделя 2025 года) |

**Примеры:**
- `Sprint 2025-W05` — 5-я неделя 2025 года
- `Sprint 2025-W23` — 23-я неделя 2025 года

**Формат 2 (альтернатива):** `Sprint {N}`

| Элемент | Правило | Пример |
|---------|---------|--------|
| `Sprint` | Префикс | `Sprint` |
| `{N}` | Порядковый номер (с начала проекта) | `12` |

**Примеры:**
- `Sprint 12`
- `Sprint 45`

**Когда использовать:**
- Формат 1 — если спринты привязаны к календарным неделям
- Формат 2 — если спринты идут последовательно с начала проекта

### Release Milestones

**SSOT:** [standard-release.md § 3](../releases/standard-release.md#3-версионирование-semver)

**Формат:** `vX.Y.Z` — следует SemVer

Правила версионирования (MAJOR/MINOR/PATCH, pre-release) — см. SSOT.

**Примеры:**
- `v1.0.0` — первый стабильный релиз
- `v2.0.0-beta` — бета-версия
- `v1.5.0-rc.2` — release candidate

### Roadmap Milestones

**Формат:** Описательное имя

| Тип | Примеры |
|-----|---------|
| Этап проекта | `MVP`, `Public Beta`, `Production Ready` |
| Квартальные цели | `Q1 2025`, `Q2 Backend Refactoring` |
| Функциональные вехи | `Auth System`, `API v2`, `Mobile Support` |

**Правила:**
- Без префиксов `v` (отличие от Release)
- CamelCase или Title Case
- Краткость: до 50 символов

---

## 6. Правила создания

### Title

**Формат:** см. [§ 5. Правила именования](#5-правила-именования)

**Правила:**
- Уникальное в рамках репозитория
- Краткое (до 50 символов)
- Следует naming convention по типу Milestone

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

**Для Sprint Milestones:**

```markdown
## Цель

Реализовать базовую авторизацию и обновить API до v2.

## Критерии готовности

- [ ] OAuth2 интеграция завершена
- [ ] API v2 endpoints задокументированы
- [ ] Тесты покрывают новую функциональность

## Фокус

- Backend: авторизация
- API: миграция на v2
- Docs: обновление документации
```

**Для Release Milestones:**

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

**Для Roadmap Milestones:**

```markdown
## Цель

Достичь готовности MVP продукта для внутреннего тестирования.

## Критерии готовности

- [ ] Базовая авторизация
- [ ] CRUD операции для основных сущностей
- [ ] Интеграция с payment gateway
- [ ] Базовый UI (без дизайн-системы)

## Целевая дата

Конец Q1 2025
```

### Due Date

**Формат:** ISO 8601 — `YYYY-MM-DDTHH:MM:SSZ`

**Правила:**

| Тип | Срок | Пример |
|-----|------|--------|
| **Sprint** | Окончание спринта (обычно пятница) | `2025-02-09T23:59:59Z` |
| **Release** | Планируемая дата релиза | `2025-03-15T12:00:00Z` |
| **Roadmap** | Конец периода (квартал, месяц) | `2025-03-31T23:59:59Z` |

**Установка при создании:**

```bash
# Через gh api
gh api POST /repos/{owner}/{repo}/milestones \
  -f title="Sprint 2025-W05" \
  -f due_on="2025-02-09T23:59:59Z" \
  -f description="..."
```

**Изменение:**

```bash
# Через gh api
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f due_on="2025-02-16T23:59:59Z"
```

---

## 7. Связь с Issues

### Добавление Issue в Milestone

**При создании Issue:**

1. Проверить существование Milestone:
   ```bash
   gh api repos/{owner}/{repo}/milestones -q '.[] | select(.title == "Sprint 2025-W05") | .number'
   # Если пусто → Milestone не существует, создать или выбрать другой
   ```
2. Создать Issue с Milestone:
   ```bash
   gh issue create \
     --title "Добавить OAuth2" \
     --body "..." \
     --label type:feature \
     --label priority:high \
     --milestone "Sprint 2025-W05"
   ```

**Для существующего Issue:**

```bash
gh issue edit 123 --milestone "Sprint 2025-W05"
```

**Удаление Issue из Milestone:**

```bash
gh issue edit 123 --milestone ""
```

### Правила группировки Issues

**Принцип:**
- Issue принадлежит Milestone, если он запланирован на выполнение в рамках этого Milestone
- Один Issue — один Milestone (нельзя добавить в несколько Milestones)

**Рекомендации:**

| Тип Milestone | Критерий добавления Issue |
|---------------|---------------------------|
| **Sprint** | Issue запланирован на эту итерацию (1-2 недели) |
| **Release** | Issue ДОЛЖЕН быть завершён для релиза этой версии |
| **Roadmap** | Issue относится к долгосрочной цели |

**Ограничения:**
- Не перегружать Sprint Milestone (макс. 15-20 Issues)
- Если Issues > 20 → разбить на подзадачи или перенести в следующий Sprint

### Просмотр Issues в Milestone

```bash
# Список Issues
gh issue list --milestone "Sprint 2025-W05"

# Открытые Issues
gh issue list --milestone "Sprint 2025-W05" --state open

# Закрытые Issues
gh issue list --milestone "Sprint 2025-W05" --state closed
```

---

## 8. Связь с Releases

**Правило:** Release Milestone должен быть связан с GitHub Release.

### Процесс создания Release из Milestone

1. **Milestone создан:** `v1.0.0`
2. **Issues завершены:** Все Issues в Milestone закрыты
3. **Milestone закрыт:**
   ```bash
   gh api PATCH /repos/{owner}/{repo}/milestones/{number} -f state=closed
   ```
4. **Release создан:**
   ```bash
   gh release create v1.0.0 \
     --title "Release v1.0.0" \
     --notes "См. Milestone: [v1.0.0](https://github.com/{owner}/{repo}/milestone/{number})"
   ```

### Структура Release Notes с ссылкой на Milestone

```markdown
# Release v1.0.0

## Milestone

Этот релиз основан на [Milestone v1.0.0](https://github.com/{owner}/{repo}/milestone/5).

**Прогресс:** 15/15 Issues завершено (100%)

## Изменения

- Добавлена авторизация через OAuth2 (#123)
- API обновлён до v2 (#124)
- Исправлена ошибка загрузки файлов (#125)

## Критические изменения

*Нет*

## Обновление

См. [CHANGELOG.md](./CHANGELOG.md)
```

### Правила

- Release Milestone ДОЛЖЕН быть закрыт ПЕРЕД созданием Release. **Проверка:**
  ```bash
  STATE=$(gh api repos/{owner}/{repo}/milestones/{number} -q '.state')
  if [ "$STATE" != "closed" ]; then
    echo "ERROR: Milestone должен быть закрыт перед созданием Release"
    exit 1
  fi
  ```
- В Release Notes ОБЯЗАТЕЛЬНА ссылка на Milestone
- Milestone может НЕ иметь Release — это нормально для Sprint и Roadmap Milestones. Release создаётся ТОЛЬКО для типа "Release Milestone" (см. § 3).

---

## 9. Закрытие Milestone

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
     gh issue edit 123 --milestone "Sprint 2025-W06"
     ```
3. **Если критичные:**
   - НЕ закрывать Milestone
   - Продлить `due_on`:
     ```bash
     gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
       -f due_on="2025-02-16T23:59:59Z"
     ```

**Правило:** НЕ закрывать Milestone с открытыми Issues без переноса их в другой Milestone.

---

## 10. CLI команды

### Создание Milestone

**Через gh api:**

```bash
# Базовое создание
gh api POST /repos/{owner}/{repo}/milestones \
  -f title="Sprint 2025-W05" \
  -f description="## Цель\n\nРеализовать OAuth2\n\n## Критерии\n- [ ] OAuth2 готов" \
  -f due_on="2025-02-09T23:59:59Z"

# С переменными
REPO="owner/repo"
gh api POST /repos/$REPO/milestones \
  -f title="v1.0.0" \
  -f description="Первый релиз" \
  -f due_on="2025-03-15T12:00:00Z"
```

**Проверка перед созданием:**

```bash
# Проверить существование Milestone с таким же title
EXISTING=$(gh api repos/{owner}/{repo}/milestones -q '.[] | select(.title == "Sprint 2025-W05") | .number')
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
  "number": 5,
  "title": "Sprint 2025-W05",
  "state": "open",
  "due_on": "2025-02-09T23:59:59Z",
  "html_url": "https://github.com/owner/repo/milestone/5"
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
  -f title="Sprint 2025-W06"

# Изменить description
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f description="Обновлённое описание"

# Изменить due_date
gh api PATCH /repos/{owner}/{repo}/milestones/{number} \
  -f due_on="2025-02-16T23:59:59Z"

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
gh issue list --milestone "Sprint 2025-W05"

# Через gh api
gh api repos/{owner}/{repo}/milestones/{number} \
  -q '.open_issues, .closed_issues'
```

---

## 11. Метрики и отчётность

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
  "title": "Sprint 2025-W05",
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
# Отчёт: Sprint 2025-W05

**Статус:** Завершён ✅
**Прогресс:** 10/10 Issues (100%)
**Due Date:** 2025-02-09

## Завершённые Issues

- #123 Добавить OAuth2
- #124 Обновить API до v2
- #125 Исправить ошибку загрузки файлов

## Незавершённые Issues

*Нет*

## Следующий Milestone

[Sprint 2025-W06](https://github.com/owner/repo/milestone/6)
```

**Генерация через скрипт:**

```bash
# Будущий скрипт: .github/.instructions/.scripts/milestone-report.py
python .github/.instructions/.scripts/milestone-report.py --milestone 5
```

---

## Скиллы

*Нет скиллов.*
