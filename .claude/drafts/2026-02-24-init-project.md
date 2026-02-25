---
description: Инструкция create-initialization.md + скилл /init-project — оркестратор Фазы 0 + консолидация quick-start/ssot/artifacts
type: feature
status: draft
created: 2026-02-24
---

# Инициализация проекта — инструкция + скилл

Единая точка входа для Фазы 0: оркестрация 6 существующих инструментов, интерактивная настройка, структурированный отчёт. Консолидация `quick-start.md` + `ssot.md` + `artifacts.md` → единый документ.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [1. Архитектура](#1-архитектура)
  - [2. Артефакт 1: create-initialization.md](#2-артефакт-1-create-initializationmd)
  - [3. Артефакт 2: /init-project SKILL.md](#3-артефакт-2-init-project-skillmd)
  - [4. Артефакт 3: Консолидация quick-start.md](#4-артефакт-3-консолидация-quick-startmd)
  - [5. Обновления существующих файлов](#5-обновления-существующих-файлов)
  - [6. Порядок создания](#6-порядок-создания)
- [Решения](#решения)
- [Закрытые вопросы](#закрытые-вопросы)
- [Tasklist](#tasklist)

---

## Контекст

**Задача:** G1 из standard-process.md — Фаза 0 разрозненна, три процесса без оркестратора
**Почему создан:** Фаза 0 состоит из трёх независимых шагов (GitHub, docs/, среда), каждый со своим SSOT. Нет единой точки входа. Инструменты существуют (`sync-labels.py`, `validate-docs.py`, `validate-architecture.py`, `validate-type-templates.py`, `make setup`), но вызываются вручную и разрозненно.
**Связанные файлы:**
- `specs/.instructions/standard-process.md` — § 4 Фаза 0 (3 подшага), § 10 G1
- `/.github/.instructions/standard-github-workflow.md` — § 2 (9 пунктов подготовки)
- `specs/.instructions/docs/standard-docs.md` — § 7 (минимальный стартовый набор)
- `/.structure/initialization.md` — human-readable гайд (8 секций, `make setup`)
- `/Makefile` — `make setup` (работает), `make init` (TODO placeholder)
- `/.github/.instructions/.scripts/sync-labels.py` — синхронизация labels (312 строк)
- `/specs/.instructions/.scripts/validate-docs.py` — проверка docs/
- `/specs/.instructions/.scripts/validate-architecture.py` — проверка 4 обязательных файлов
- `/.github/.instructions/.scripts/validate-type-templates.py` — Issue Templates vs labels.yml

---

## Содержание

### 1. Архитектура

**Три уровня инициализации:**

| Уровень | Инструмент | Аудитория | Что делает |
|---------|-----------|-----------|------------|
| Минимум | `make setup` | Человек/CI | Python + pre-commit + gh check (уже работает) |
| Автоматизация | `make init` | Человек/CI | setup + labels sync + verify (раскрыть TODO) |
| Полный | `/init-project` | Claude + человек | Интерактивная оркестрация всех шагов + customization + отчёт |

```
initialization.md                 (для человека — читает и следует)
       ↓ операционные детали
create-initialization.md          (для Claude — исполняемые шаги)
       ↓ SSOT для
/init-project (SKILL.md)          (точка входа — оркестрирует)
```

**Почему скилл, не агент:**

| Критерий | Скилл | Агент |
|----------|-------|-------|
| Частота | Однократно (при создании проекта) | — |
| Интерактивность | Высокая (AskUserQuestion: milestone? branch protection? customization?) | Агенту сложнее |
| Тяжёлая работа | Нет — скрипты делают всё | — |
| Нужен ли основной контекст | Да — AskUserQuestion | — |

Релиз — редкая операция, init — одноразовая. Скилл допустим для обоих.

### 2. Артефакт 1: create-initialization.md

**Путь:** `.structure/.instructions/create-initialization.md`
**Действие:** Создать через `/instruction-create`.
**Тип:** воркфлоу (create-*)

Содержание инструкции — 10 шагов с паттерном **Check → Act → Status** для каждого.

#### Блок 1: Prerequisites (gate)

**Шаг 1: Проверить prerequisites**

```bash
python --version      # Python 3.8+
pre-commit --version  # pre-commit 3.x+
git --version         # git 2.x+
```

Если любой не найден → **СТОП** с инструкцией установки (ссылка на initialization.md § 3).
При успехе → `make setup` (pre-commit install).

**Шаг 2: Проверить GitHub CLI**

```bash
gh --version          # gh 2.x+
gh auth status        # авторизован?
```

| Результат | Действие |
|-----------|----------|
| `gh` не найден | SKIP все GitHub-шаги (4-7), предупреждение с инструкцией |
| `gh` найден, не авторизован | Инструкция `gh auth login`, повторная проверка |
| `gh` авторизован, но нет remote | `gh repo view` fails → SKIP GitHub-шаги |
| Всё ок | Продолжить |

**Шаг 3: Проверить Docker (опционально)**

```bash
docker compose version   # Docker Compose 2.x+
```

Если Docker не найден → **WARN** (не gate, не блокирует). Предупреждение: "Docker Desktop необходим для `make dev/test`. Установите: initialization.md → Docker Desktop."

#### Блок 2: GitHub Setup (требует gh auth)

**Шаг 4: Синхронизировать Labels**

Check: `python .github/.instructions/.scripts/sync-labels.py` (dry-run по умолчанию — показывает diff).
Act: `python .github/.instructions/.scripts/sync-labels.py --apply --force`.

Предупредить пользователя через AskUserQuestion перед `--force`: "Будут удалены N default GitHub labels (bug, documentation, enhancement, ...). Это нормально — проект использует свою систему меток. Продолжить?"

**Шаг 5: Проверить файлы GitHub**

Check-before-act для 7 файлов:

| Файл | Проверка | Если отсутствует |
|------|----------|-----------------|
| `.github/ISSUE_TEMPLATE/*.yml` | `validate-type-templates.py` | WARN: создать через standard-issue-template.md |
| `.github/PULL_REQUEST_TEMPLATE.md` | `test -f` | WARN: создать через standard-pr-template.md |
| `.github/CODEOWNERS` | `test -f` | WARN: создать через standard-codeowners.md |
| `.github/workflows/ci.yml` | `test -f` | WARN: CI не настроен |
| `.github/workflows/codeql.yml` | `test -f` | WARN: CodeQL не настроен |
| `.github/dependabot.yml` | `test -f` | WARN: Dependabot не настроен |
| `.github/SECURITY.md` | `test -f` | WARN: SECURITY.md отсутствует |

Все файлы — из template, должны быть при клонировании. Если нет — значит repo создан не из template.

**Шаг 6: Security Settings (MANUAL)**

Невозможно проверить/настроить программно (GitHub Settings API ограничен). Вывести пошаговую инструкцию:

```
MANUAL: Настройте Security Settings в GitHub UI:
  Settings → Code security and analysis →
    ✅ Dependabot alerts → Enable
    ✅ Dependabot security updates → Enable
    ✅ Secret scanning → Enable
    ✅ Push protection → Enable

  ⚠️ НЕ включать Code Scanning → Default Setup (используется codeql.yml)

SSOT: standard-security.md § 7
```

**Шаг 7: Branch Protection (опционально)**

Check: `gh api repos/{owner}/{repo}/branches/main/protection` (может вернуть 404 — не настроено).

AskUserQuestion: "Настроить Branch Protection для main? (PR required, CI required, 1 approval)"

| Ответ | Действие |
|-------|----------|
| Да | `gh api repos/{owner}/{repo}/branches/main/protection --method PUT ...` |
| Нет | SKIP — вывести команду для ручной настройки |

#### Блок 3: Project Setup

**Шаг 8: Проверить docs/**

Check:
```bash
python specs/.instructions/.scripts/validate-docs.py
python specs/.instructions/.scripts/validate-architecture.py --verbose
```

Отчёт о найденных/отсутствующих файлах. Не создавать — docs/ создаются в Фазе 1 (Design → WAITING) через `/service-create`.

**Шаг 9: Customization (интерактивно)**

Detect placeholders/defaults в файлах из template и предложить заменить:

| Файл | Placeholder | AskUserQuestion |
|------|------------|----------------|
| `.github/SECURITY.md` | Email для отчётов об уязвимостях | "Укажите email для security-отчётов" |
| `.github/dependabot.yml` | Директории сервисов | "Проверьте директории в dependabot.yml" |
| `.github/workflows/codeql.yml` | `matrix.language` | "Какие языки используете? (python, javascript, go)" |
| `.github/CODEOWNERS` | Reviewers | "Обновить CODEOWNERS? Текущий: @NSEvteev" |

Для каждого: если placeholder обнаружен → AskUserQuestion. Если уже кастомизирован → SKIP.

#### Блок 4: Verification + Report

**Шаг 10: Верификация и отчёт**

```bash
pre-commit run --all-files
```

Финальный отчёт:

```
=== /init-project Report ===

| # | Step                | Status | Details                              |
|---|---------------------|--------|--------------------------------------|
| 1 | Prerequisites       | DONE   | Python 3.12, pre-commit 4.x, git 2.x |
| 2 | GitHub CLI          | DONE   | Authenticated as @user               |
| 3 | Docker              | WARN   | Not found — install for make dev     |
| 4 | Labels              | DONE   | Synced 27/27 (created 27, deleted 9) |
| 5 | GitHub Files        | DONE   | 7/7 present                          |
| 6 | Security Settings   | MANUAL | Enable Dependabot + Secret Scanning  |
| 7 | Branch Protection   | DONE   | main: PR required, CI required       |
| 8 | docs/               | DONE   | 7/7 files, architecture 4/4          |
| 9 | Customization       | DONE   | SECURITY.md email updated            |
| 10| Verification        | DONE   | pre-commit: 25/25 passed             |

Next: /chain — начать первый analysis chain
```

**Опциональный шаг после отчёта:**

AskUserQuestion: "Создать первый Milestone?" → Если да → `/milestone-create v0.1.0`

#### Идемпотентность

Все шаги реализуют паттерн check-before-act:
- Labels: `sync-labels.py` использует diff — не пересоздаёт существующие
- Файлы: `test -f` — не перезаписывает
- Customization: проверяет placeholder — если уже заменён → SKIP
- `make setup`: `pre-commit install` идемпотентен

Повторный запуск `/init-project` безопасен и работает как healthcheck.

#### Режим --check

`/init-project --check` — все проверки БЕЗ мутаций. Только отчёт. Полезно для:
- Проверка после ручной настройки
- CI healthcheck
- Аудит проекта

### 3. Артефакт 2: /init-project SKILL.md

**Путь:** `.claude/skills/init-project/SKILL.md`
**Действие:** Создать через `/skill-create`.

**Конфигурация:**

```yaml
---
name: init-project
description: Инициализация проекта — GitHub Labels, Security, docs/, pre-commit, customization.
standard: .claude/.instructions/skills/standard-skill.md
standard-version: v1.0
index: .claude/.instructions/skills/README.md
ssot: .structure/.instructions/create-initialization.md
version: v1.0
argument-hint: "[--check] [--skip-github] [--skip-docs] [--skip-setup]"
---
```

**Формат вызова:**

```
/init-project                — полная инициализация (интерактивная)
/init-project --check        — только проверка, без мутаций (healthcheck)
/init-project --skip-github  — пропустить GitHub-шаги (4-7)
/init-project --skip-docs    — пропустить проверку docs/ (8)
/init-project --skip-setup   — пропустить make setup (1)
```

### 4. Артефакт 3: Консолидация quick-start.md

**Проблема:** Claude при onboarding читает 3 концептуальных файла с пересекающимся содержанием:

| Файл | Строк | Суть |
|------|-------|------|
| `quick-start.md` | 64 | Таблица артефактов + "скиллы вместо команд" + ссылки |
| `ssot.md` | 96 | Что такое SSOT, иерархия документов, исключения |
| `artifacts.md` | 163 | 7 типов артефактов детально, иерархия слоёв |

**Итого:** 323 строки в 3 файлах. quick-start.md уже дублирует ssot.md и artifacts.md в сжатой форме. Claude загружает 3 файла, чтобы получить одну картину.

**Действие:** Объединить в обогащённый `quick-start.md` (~250 строк).

**Целевая структура quick-start.md:**

```markdown
# Quick Start для Claude

## 1. SSOT — единый источник истины
  (из ssot.md: определение, иерархия Стандарт → Workflows → Экземпляры,
   таблица уровней, исключения, версионирование + миграция)

## 2. Артефакты системы
  (из artifacts.md: таблица 7 типов с SSOT/расположение/скиллы,
   иерархия слоёв, краткие описания каждого типа)

## 3. Скиллы вместо команд
  (уже есть в quick-start.md: таблица ЗАПРЕЩЕНО/ОБЯЗАТЕЛЬНО)

## 4. Версионирование
  (уже есть: standard-version, /migration-create)

## 5. Инициализация
  (NEW: /init-project, make setup, make init)

## 6. Процесс поставки ценности
  (уже есть: ссылка на standard-process.md)

## Навигация
  (уже есть: ссылки на ключевые документы)
```

**Файлы `ssot.md` и `artifacts.md` удаляются.** Все внешние ссылки обновляются → `quick-start.md#секция`.

**Затрагиваемые ссылки (обновить):**

| Файл | Ссылка | Обновить на |
|------|--------|-------------|
| `CLAUDE.md` | `[SSOT](/.structure/ssot.md) \| [Артефакты](/.structure/artifacts.md)` | `[Quick Start](/.structure/quick-start.md)` |
| `.structure/README.md` | Ссылки на ssot.md и artifacts.md в секции "Концептуальные документы" | Ссылки на quick-start.md#секции |
| `.claude/onboarding.md` | Шаг 3 "Изучи artifacts.md" | `quick-start.md#артефакты-системы` |
| `.claude/onboarding.md` | Ссылка на ssot.md | `quick-start.md#ssot--единый-источник-истины` |

### 5. Обновления существующих файлов

#### 5.1 initialization.md

| Секция | Изменение |
|--------|-----------|
| § 2 Зависимости | Добавить Docker Desktop в таблицу: `Docker Desktop` / `Docker, docker-compose для сервисов` / `https://www.docker.com/products/docker-desktop/`. Примечание: WSL2 обязателен на Windows |
| § 8 Labels | Исправить ссылку: `setup-labels.py` (не существует) → `sync-labels.py --apply` |
| Новая секция (после § 8) | **§ 9 Claude-assisted инициализация:** "Для полной интерактивной настройки с Claude: `/init-project`. Скилл оркестрирует все шаги из этого документа, проверяет состояние и генерирует отчёт." |

#### 5.2 Makefile `make init`

Раскрыть TODO placeholder:

```makefile
init:  ## Полная инициализация проекта
	@$(MAKE) setup
	@echo ""
	@echo "📋 Синхронизация Labels..."
	@python .github/.instructions/.scripts/sync-labels.py --apply --force 2>/dev/null || echo "⚠️ Labels: gh CLI не доступен или не авторизован"
	@echo ""
	@echo "✅ Верификация..."
	@pre-commit run --all-files || true
	@echo ""
	@echo "════════════════════════════════════════"
	@echo "  Для полной интерактивной настройки:"
	@echo "  Claude Code → /init-project"
	@echo "════════════════════════════════════════"
```

#### 5.3 CLAUDE.md

Добавить секцию "Инициализация" (перед "Архитектура", после блока "Первый шаг"):

```markdown
## Инициализация

**Новый проект?** Выполни `/init-project` — полная настройка GitHub, docs/, среда, customization.

| Команда | Когда |
|---------|-------|
| `make setup` | Минимум — pre-commit хуки |
| `make init` | Автоматизация — setup + labels + verify |
| `/init-project` | Полная настройка с Claude (интерактивно) |
| `/init-project --check` | Healthcheck — проверка без изменений |
```

#### 5.4 standard-process.md

| Секция | Изменение |
|--------|-----------|
| § 4 Фаза 0, строка "Скиллы" | Добавить `/init-project` |
| § 8 строка Фаза 0 | Добавить: create-initialization.md в "Инструкция", /init-project в "Скилл" |
| § 9 Quick Reference | Добавить перед "Фаза 1": `Фаза 0 — Инициализация:\n  /init-project` |
| § 10 G1 | Закрыть: "/init-project — оркестратор Фазы 0" |

#### 5.5 onboarding.md

| Секция | Изменение |
|--------|-----------|
| § 2 Первые шаги | Добавить шаг 0 (перед "Прочитай CLAUDE.md"): "0. Выполни `make setup` (или `/init-project` для полной настройки)" |

#### 5.6 quick-start.md (переписка — консолидация)

Это основная работа Артефакта 3. См. секцию "Артефакт 3: Консолидация quick-start.md".

Переписать quick-start.md, включив содержание ssot.md и artifacts.md. Удалить ssot.md и artifacts.md. Обновить все входящие ссылки.

#### 5.7 .structure/.instructions/README.md

Зарегистрировать `create-initialization.md` в таблице инструкций.

### 6. Порядок создания

| # | Артефакт | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | Консолидация `quick-start.md` | Ручное (переписка) | — |
| 2 | Удалить `ssot.md` и `artifacts.md` | `/structure-modify` | ← 1 |
| 3 | Обновить ссылки (CLAUDE.md, README.md, onboarding.md) | Ручное | ← 2 |
| 4 | Инструкция `create-initialization.md` | `/instruction-create` | — |
| 5 | Скилл `/init-project` | `/skill-create` | ← 4 |
| 6 | Обновить `initialization.md` | Ручное | — |
| 7 | Обновить `Makefile make init` | Ручное | — |
| 8 | Обновить `CLAUDE.md` — секция "Инициализация" | Ручное | ← 5 |
| 9 | Обновить `standard-process.md` §4/§8/§9/§10 | Ручное | ← 5 |
| 10 | Обновить `onboarding.md` | Ручное | ← 5 |
| 11 | Обновить `.structure/.instructions/README.md` | Автоматически (шаг 4) | ← 4 |
| 12 | Миграция `standard-process.md` | `/migration-create` | ← 9 |
| 13 | Валидация миграции | `/migration-validate` | ← 12 |

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| R1 | Скилл, не агент | Однократная интерактивная операция. Нужен AskUserQuestion (milestone, branch protection, customization). Контекст допустим |
| R2 | Три уровня (setup/init/init-project) | `make setup` — минимум для CI. `make init` — автоматизация без Claude. `/init-project` — полная интерактивная настройка |
| R3 | check-before-act для каждого шага | Идемпотентность. Повторный запуск безопасен и работает как healthcheck |
| R4 | `--check` режим | Только проверки, без мутаций. Для CI, аудита, проверки после ручной настройки |
| R5 | GitHub-шаги → SKIP если нет gh/auth/remote | Graceful degradation. Не блокировать настройку среды из-за отсутствия GitHub CLI |
| R6 | Docker → WARN, не gate | Docker нужен для `make dev/test`, но не для инициализации. Предупредить, не блокировать |
| R7 | Security Settings → MANUAL | GitHub Settings API не позволяет настраивать Dependabot/Secret Scanning программно. Вывести инструкцию |
| R8 | Customization через AskUserQuestion | Detect placeholders → спросить. Не молча перезаписывать, не пропускать. Каждый файл опрашивается один раз |
| R9 | CLAUDE.md — секция "Инициализация" | Claude должен знать о `/init-project` при первом входе в проект. CLAUDE.md — первый файл, который читает Claude |
| R10 | `make init` — мост между setup и /init-project | Раскрыть TODO. Labels sync + verify. Без Claude — для CI и manual workflow |
| R11 | Milestone опционален | Не все проекты начинают с milestone. AskUserQuestion после основных шагов |
| R12 | Инструкция в `.structure/.instructions/` | Инициализация — про структуру проекта, не GitHub и не specs |
| R13 | Консолидация quick-start + ssot + artifacts → один quick-start.md | 3 файла (323 строки) с пересекающимся содержанием → 1 файл (~250 строк). Claude загружает 1 страницу вместо 3 при onboarding. ssot.md и artifacts.md не используются нигде кроме onboarding |

---

## Закрытые вопросы

### Q1. Нужно ли создавать первый Milestone в рамках инициализации?

**Ответ: опционально.** AskUserQuestion после основных шагов: "Создать первый Milestone?" → `/milestone-create v0.1.0`. Не все проекты начинают с milestone — зависит от workflow команды.

→ R11

### Q2. Как обрабатывать случай когда GitHub repo ещё не создан?

**Ответ: graceful degradation.** `gh repo view` возвращает ошибку → все GitHub-шаги (4-7) получают статус SKIP с сообщением "No remote repository configured. GitHub steps skipped." Остальные шаги (prerequisites, docs/, make setup) выполняются нормально.

→ R5

### Q3. Нужен ли `--interactive` режим с пошаговым подтверждением?

**Ответ: нет.** Скилл интерактивен по природе — AskUserQuestion используется в точках решения (labels force, branch protection, customization, milestone). Per-step confirmation избыточен. `--check` покрывает потребность в неинтерактивном режиме.

### Q4. Нужен ли новый скрипт init-project.py?

**Ответ: нет.** Все проверки покрыты существующими скриптами (`sync-labels.py`, `validate-docs.py`, `validate-architecture.py`, `validate-type-templates.py`). Оркестрация — ответственность скилла, не скрипта. `make init` покрывает автоматизируемый subset для CI.

### Q5. Куда поместить create-initialization.md?

**Ответ: `.structure/.instructions/`.** Инициализация — про структуру и настройку проекта. Не про GitHub (не `.github/.instructions/`), не про анализ (не `specs/.instructions/`). Рядом с `standard-readme.md` и другими стандартами структуры.

### Q6. Можно ли объединить quick-start.md, ssot.md и artifacts.md?

**Ответ: да.** Три концептуальных файла (323 строки суммарно) с пересекающимся содержанием. quick-start.md уже дублирует ssot.md и artifacts.md в сжатой форме. ssot.md и artifacts.md не используются нигде за пределами onboarding. Объединение в обогащённый quick-start.md (~250 строк) уменьшает файлы на 2, упрощает навигацию и снижает контекст для Claude.

initialization.md и pre-commit.md остаются раздельно: pre-commit.md — ongoing reference (добавление хуков, отладка), не только setup. Разные жизненные циклы. .instructions/ (9 файлов) — формальная система стандартов, не трогаем.

→ R13

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Консолидировать quick-start.md (поглотить ssot.md + artifacts.md)
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "Артефакт 3")
    Переписать .structure/quick-start.md, включив содержание ssot.md и artifacts.md:
    - § 1 SSOT (из ssot.md: определение, иерархия, исключения, версионирование)
    - § 2 Артефакты системы (из artifacts.md: таблица 7 типов, иерархия слоёв, описания)
    - § 3 Скиллы вместо команд (уже есть)
    - § 4 Версионирование (уже есть)
    - § 5 Инициализация (NEW: /init-project, make setup, make init)
    - § 6 Процесс поставки (уже есть)
    - Навигация (уже есть)
    Целевой размер: ~250 строк.
  activeForm: Консолидирую quick-start.md

TASK 2: Удалить ssot.md и artifacts.md
  blockedBy: [1]
  description: >
    Удалить .structure/ssot.md и .structure/artifacts.md.
    Содержание перенесено в quick-start.md (TASK 1).
  activeForm: Удаляю ssot.md и artifacts.md

TASK 3: Обновить ссылки после консолидации
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "Артефакт 3", таблица ссылок)
    Обновить все входящие ссылки на ssot.md и artifacts.md:
    - CLAUDE.md: заменить "[SSOT](ssot.md) | [Артефакты](artifacts.md)" → "[Quick Start](quick-start.md)"
    - .structure/README.md: обновить секцию "Концептуальные документы"
    - .claude/onboarding.md § 2: шаг 3 → quick-start.md#артефакты-системы
    - .claude/onboarding.md: ссылка на ssot → quick-start.md#ssot--единый-источник-истины
    Поиск по всем .md файлам: grep "ssot\.md\|artifacts\.md" для полного покрытия.
  activeForm: Обновляю ссылки после консолидации

TASK 4: Создать инструкцию create-initialization.md
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "Артефакт 1")
    /instruction-create для .structure/.instructions/create-initialization.md.
    10 шагов с паттерном Check → Act → Status:
    - Блок 1: Prerequisites (python, pre-commit, git), GitHub CLI (gh auth), Docker (optional warn)
    - Блок 2: Labels (sync-labels.py), файлы GitHub (7 файлов), Security (MANUAL), Branch Protection (AskUserQuestion)
    - Блок 3: docs/ (validate-docs.py, validate-architecture.py), Customization (SECURITY.md email, dependabot dirs, codeql langs, CODEOWNERS)
    - Блок 4: Verification (pre-commit run --all-files) + Report (таблица)
    Включить: идемпотентность, graceful degradation, --check режим, опциональный Milestone.
  activeForm: Создаю create-initialization.md

TASK 5: Создать скилл /init-project
  blockedBy: [4]
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "Артефакт 2")
    /skill-create для .claude/skills/init-project/SKILL.md.
    SSOT: .structure/.instructions/create-initialization.md.
    Параметры: --check, --skip-github, --skip-docs, --skip-setup.
    Воркфлоу: прочитать create-initialization.md → выполнить 10 шагов.
  activeForm: Создаю /init-project

TASK 6: Обновить initialization.md
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "§ 5.1")
    Обновить .structure/initialization.md:
    - § 2 Зависимости: добавить Docker Desktop (WSL2 на Windows)
    - § 8 Labels: заменить setup-labels.py → sync-labels.py --apply
    - Новая § 9: "Claude-assisted инициализация" → ссылка на /init-project
  activeForm: Обновляю initialization.md

TASK 7: Обновить Makefile make init
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "§ 5.2")
    Раскрыть TODO placeholder в Makefile make init:
    - make setup (уже есть)
    - sync-labels.py --apply --force (с fallback если gh недоступен)
    - pre-commit run --all-files (с || true)
    - Вывод: "Для полной настройки: /init-project"
  activeForm: Обновляю Makefile

TASK 8: Обновить CLAUDE.md — секция "Инициализация"
  blockedBy: [3, 5]
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "§ 5.3")
    Добавить секцию "Инициализация" в CLAUDE.md (после "Первый шаг", перед "Архитектура"):
    - /init-project как точка входа для нового проекта
    - Таблица: make setup / make init / /init-project / /init-project --check
    Примечание: TASK 3 уже обновляет CLAUDE.md (ссылки ssot/artifacts → quick-start).
    Этот таск добавляет секцию "Инициализация" — другое изменение, blockedBy [3] чтобы не конфликтовать.
  activeForm: Обновляю CLAUDE.md — инициализация

TASK 9: Обновить standard-process.md §4/§8/§9/§10
  blockedBy: [5]
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "§ 5.4")
    Обновить specs/.instructions/standard-process.md:
    - § 4 Фаза 0 "Скиллы": добавить /init-project
    - § 8 строка Фаза 0: create-initialization.md + /init-project
    - § 9 Quick Reference: добавить "Фаза 0: /init-project"
    - § 10 G1: отметить как закрытый gap
  activeForm: Обновляю standard-process.md

TASK 10: Обновить onboarding.md
  blockedBy: [3, 5]
  description: >
    Драфт: .claude/drafts/2026-02-24-init-project.md (секция "§ 5.5")
    onboarding.md § 2: добавить шаг 0 "make setup или /init-project".
    Примечание: TASK 3 уже обновляет onboarding.md (ссылки ssot/artifacts).
    Этот таск добавляет шаг 0 — другое изменение, blockedBy [3] чтобы не конфликтовать.
  activeForm: Обновляю onboarding.md

TASK 11: Обновить .structure/.instructions/README.md
  blockedBy: [4]
  description: >
    Зарегистрировать create-initialization.md в таблице инструкций.
    README обновляется автоматически при создании артефактов, но проверить полноту.
  activeForm: Обновляю .structure README

TASK 12: Обновить .structure/README.md — секция "Концептуальные документы"
  blockedBy: [2]
  description: >
    Обновить .structure/README.md: удалить ssot.md и artifacts.md из секции
    "Концептуальные документы", обновить ссылки на quick-start.md.
  activeForm: Обновляю .structure/README.md

TASK 13: Миграция standard-process.md
  blockedBy: [9]
  description: >
    /migration-create для standard-process.md.
    Синхронизировать зависимые файлы после обновления §4/§8/§9/§10.
  activeForm: Мигрирую зависимости

TASK 14: Валидация миграции
  blockedBy: [13]
  description: >
    /migration-validate для standard-process.md.
    Убедиться что все зависимые файлы синхронизированы.
  activeForm: Валидирую миграцию

TASK 15: Обновить CLAUDE.md — отметка выполнения
  blockedBy: [11]
  description: >
    В CLAUDE.md отметить init-project (G1) как [x] выполненный.
  activeForm: Обновляю CLAUDE.md
```
