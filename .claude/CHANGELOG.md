# Changelog системы инструкций

Все значимые изменения в системе инструкций, скиллов и rules.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/).

## Как читать этот файл

- **Добавлено** — новые функции
- **Изменено** — изменения в существующих функциях
- **Устарело** — функции, которые будут удалены
- **Удалено** — удалённые функции
- **Исправлено** — исправления багов
- **Критичные изменения** — изменения, требующие действий от пользователя

---

## [Unreleased]

## [2026-02] - Февраль 2026

### Добавлено
- Onboarding-документы: `ssot.md`, `objects.md`, `quick-start.md`
- Версионирование всех стандартов (`standard-version` в frontmatter)
- Скрипты валидации версий: `bump-standard-version.py`, `check-version-drift.py`
- Агент meta-reviewer для семантического анализа документов
- Скиллы `review-branch` и `review-pr` для ревью кода
- Инструкции `validation-release.md`, `create-release.md` (releases)
- Скрипты `validate-pre-release.py`, `validate-post-release.py`
- Корневой `CHANGELOG.md` (Keep a Changelog)
- Поле `argument-hint` в frontmatter скиллов (подсказка при автокомплите)

### Изменено
- Валидация всех 18 стандартов `.github/.instructions/` (Этапы 1 и 2 — 18/18)
- Объединение `standard-release.md` и `release-workflow.md` в один документ (v1.1)
- Миграция frontmatter 34 скиллов: `triggers` → `argument-hint`
- Обновлены 5 стандартов/инструкций скиллов для поддержки `argument-hint`
- Скрипты `validate-skill.py` и `list-skills.py` — поддержка `argument-hint`
- Актуализация README: `.structure/`, `.claude/`, `.github/`, `.claude/skills/`
- CI: fallback для `git branch --show-current` в detached HEAD (GitHub Actions)
- `validate-security.py`: проверка `codeql.yml` сделана опциональной (SEC008)

### Удалено
- Поле `triggers` из frontmatter всех 34 скиллов (заменено на `argument-hint`)
- Проверки K005/K006 из `validate-skill.py` (были для triggers)
- `codeql.yml` — Code Scanning требует GitHub Team/Enterprise или public repo
- Пустые папки-заглушки `.github/milestones/` и `.github/releases/`
- Несуществующие `hooks/` и `state/` из документации `.claude/`
- Фантомные скиллы и графы зависимостей из `.claude/README.md`

### Исправлено
- `validate-branch-name.py`: пустой результат `git branch --show-current` в GitHub Actions
- Колонка «Триггеры» убрана из 9 таблиц в `.claude/skills/README.md`

### Критичные изменения (breaking)
- Обязательный frontmatter с `standard-version` для Workflows и Экземпляров
- Миграция стандартов теперь требует 9 шагов (ранее — произвольно)
- Поле `triggers` больше не поддерживается в SKILL.md — используется `argument-hint`

### Как обновить
1. Запустить `/migration-validate` для проверки расхождений
2. Для каждого расхождения — выполнить `/migration-create`
3. В SKILL.md: заменить блок `triggers:` на `argument-hint:` в frontmatter

---

## [2026-01] - Январь 2026

### Добавлено
- Система скиллов (`/.claude/skills/`)
- Система rules (`/.claude/rules/`)
- Агенты meta-agent и meta-reviewer
- Черновики (`/.claude/drafts/`)

### Изменено
- Реструктуризация `/.claude/` — выделены отдельные папки для скиллов, rules, агентов
