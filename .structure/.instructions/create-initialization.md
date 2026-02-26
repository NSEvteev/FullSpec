---
description: Воркфлоу инициализации проекта — оркестрация Фазы 0, GitHub Labels, Security, docs/, pre-commit, customization, отчёт.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .structure/.instructions/README.md
---

# Воркфлоу инициализации проекта

Пошаговый процесс настройки нового проекта. 10 шагов с паттерном **Check → Act → Status**.

**Полезные ссылки:**
- [Инструкции .structure/](./README.md)
- [Инициализация (для человека)](../initialization.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Reference | [initialization.md](../initialization.md) |
| Создание | Этот документ |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить prerequisites](#шаг-1-проверить-prerequisites)
  - [Шаг 2: Проверить GitHub CLI](#шаг-2-проверить-github-cli)
  - [Шаг 3: Проверить Docker](#шаг-3-проверить-docker)
  - [Шаг 4: Синхронизировать Labels](#шаг-4-синхронизировать-labels)
  - [Шаг 5: Проверить файлы GitHub](#шаг-5-проверить-файлы-github)
  - [Шаг 6: Security Settings](#шаг-6-security-settings)
  - [Шаг 7: Branch Protection](#шаг-7-branch-protection)
  - [Шаг 8: Проверить docs](#шаг-8-проверить-docs)
  - [Шаг 9: Customization](#шаг-9-customization)
  - [Шаг 10: Верификация и отчёт](#шаг-10-верификация-и-отчёт)
- [Режимы запуска](#режимы-запуска)
- [Идемпотентность](#идемпотентность)
- [Чек-лист](#чек-лист)
- [Скиллы](#скиллы)

---

## Принципы

> **Check-before-act.** Каждый шаг сначала проверяет текущее состояние, затем действует. Повторный запуск безопасен.

> **Graceful degradation.** Отсутствие `gh` или Docker не блокирует инициализацию — шаги переходят в SKIP.

> **Не дублировать SSOT.** Инструкция ссылается на существующие стандарты, не копирует их содержание.

---

## Шаги

> Блок 1: Prerequisites (шаги 1–3) — gate-проверки.

### Шаг 1: Проверить prerequisites

**Check:**

```bash
python --version      # Python 3.8+
pre-commit --version  # pre-commit 3.x+
git --version         # git 2.x+
```

| Результат | Действие |
|-----------|----------|
| Всё найдено | `make setup` (pre-commit install) → продолжить |
| Любой не найден | **СТОП** — вывести инструкцию установки (ссылка: [initialization.md § 3](../initialization.md#3-установка-вручную)) |

### Шаг 2: Проверить GitHub CLI

**Check:**

```bash
gh --version          # gh 2.x+
gh auth status        # авторизован?
```

| Результат | Действие |
|-----------|----------|
| `gh` не найден | **SKIP** все GitHub-шаги (4–7), предупреждение с инструкцией установки |
| `gh` найден, не авторизован | Инструкция `gh auth login`, повторная проверка |
| `gh` авторизован, но нет remote | `gh repo view` fails → **SKIP** GitHub-шаги |
| Всё ок | Продолжить |

### Шаг 3: Проверить Docker

**Check:**

```bash
docker compose version   # Docker Compose 2.x+
```

| Результат | Действие |
|-----------|----------|
| Docker найден | Продолжить |
| Docker не найден | **WARN** (не gate, не блокирует). Сообщение: "Docker Desktop необходим для `make dev/test`. Установите: [initialization.md § 3](../initialization.md#3-установка-вручную)" |

---

> Блок 2: GitHub Setup (шаги 4–7) — пропускается если Шаг 2 вернул SKIP.

### Шаг 4: Синхронизировать Labels

**Check:**

```bash
python .github/.instructions/.scripts/sync-labels.py
```

Dry-run показывает diff: какие метки создать, какие удалить.

**Act:** Перед применением — `AskUserQuestion`:

> "Будут удалены N default GitHub labels (bug, documentation, enhancement, ...). Это нормально — проект использует свою систему меток. Продолжить?"

При подтверждении:

```bash
python .github/.instructions/.scripts/sync-labels.py --apply --force
```

### Шаг 5: Проверить файлы GitHub

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

### Шаг 6: Security Settings

Невозможно проверить/настроить программно (GitHub Settings API ограничен). Вывести пошаговую инструкцию:

```
MANUAL: Настройте Security Settings в GitHub UI:
  Settings → Code security and analysis →
    Enable: Dependabot alerts
    Enable: Dependabot security updates
    Enable: Secret scanning
    Enable: Push protection

  НЕ включать Code Scanning → Default Setup (используется codeql.yml)

SSOT: standard-security.md
```

**SSOT:** [standard-security.md](/.github/.instructions/actions/security/standard-security.md)

### Шаг 7: Branch Protection

**Check:**

```bash
gh api repos/{owner}/{repo}/branches/main/protection --method GET
```

Может вернуть 404 — не настроено.

**Act:** `AskUserQuestion`:

> "Настроить Branch Protection для main? (PR required, CI required, 1 approval)"

| Ответ | Действие |
|-------|----------|
| Да | Настроить через `gh api` (см. [initialization.md § 7](../initialization.md#7-настройка-branch-protection-rules)) |
| Нет | SKIP — вывести команду для ручной настройки |

---

> Блок 3: Project Setup (шаги 8–9).

### Шаг 8: Проверить docs

**Check:**

```bash
python specs/.instructions/.scripts/validate-docs.py
python specs/.instructions/.scripts/validate-architecture.py --verbose
```

Отчёт о найденных/отсутствующих файлах. Не создавать — docs/ создаются в Фазе 1 (Design → WAITING) через `/service-create`.

**SSOT:** [standard-docs.md](../../specs/.instructions/docs/standard-docs.md)

### Шаг 9: Customization

Detect placeholders/defaults и предложить заменить через `AskUserQuestion`:

| Файл | Placeholder | Вопрос |
|------|------------|--------|
| `.github/SECURITY.md` | Email для отчётов об уязвимостях | "Укажите email для security-отчётов" |
| `.github/dependabot.yml` | Директории сервисов | "Проверьте директории в dependabot.yml" |
| `.github/workflows/codeql.yml` | `matrix.language` | "Какие языки используете? (python, javascript, go)" |
| `.github/CODEOWNERS` | Reviewers | "Обновить CODEOWNERS? Текущий: ..." |

Для каждого: если placeholder обнаружен → `AskUserQuestion`. Если уже кастомизирован → SKIP.

---

> Блок 4: Verification + Report (шаг 10).

### Шаг 10: Верификация и отчёт

**Act:**

```bash
pre-commit run --all-files
```

**Финальный отчёт:**

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

`AskUserQuestion`: "Создать первый Milestone?" → Если да → `/milestone-create v0.1.0`

---

## Режимы запуска

| Режим | Описание |
|-------|----------|
| По умолчанию | Полная инициализация (интерактивная) |
| `--check` | Все проверки БЕЗ мутаций. Только отчёт. Полезно для CI, аудита, проверки после ручной настройки |
| `--skip-github` | Пропустить шаги 4–7 (GitHub Setup) |
| `--skip-docs` | Пропустить шаг 8 (проверка docs/) |
| `--skip-setup` | Пропустить шаг 1 (make setup) |

---

## Идемпотентность

Все шаги реализуют паттерн check-before-act:
- Labels: `sync-labels.py` использует diff — не пересоздаёт существующие
- Файлы: `test -f` — не перезаписывает
- Customization: проверяет placeholder — если уже заменён → SKIP
- `make setup`: `pre-commit install` идемпотентен

Повторный запуск `/init-project` безопасен и работает как healthcheck.

---

## Чек-лист

### Prerequisites
- [ ] Python 3.8+ установлен
- [ ] pre-commit установлен
- [ ] Git установлен
- [ ] `make setup` выполнен

### GitHub Setup
- [ ] GitHub CLI установлен и авторизован (или SKIP)
- [ ] Labels синхронизированы
- [ ] Файлы GitHub проверены (7/7)
- [ ] Security Settings — ручная инструкция выведена
- [ ] Branch Protection — настроен или SKIP

### Project Setup
- [ ] docs/ проверен
- [ ] Customization — placeholders обработаны

### Verification
- [ ] `pre-commit run --all-files` пройден
- [ ] Финальный отчёт выведен
- [ ] Milestone (опционально) предложен

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/init-project](/.claude/skills/init-project/SKILL.md) | Инициализация проекта | Этот документ |
