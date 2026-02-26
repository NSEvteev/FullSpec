---
description: Pre-commit хуки проекта — автоматические проверки перед коммитом, конфигурация, описание проверок и обход.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
---

# Pre-commit хуки

Проект использует [pre-commit](https://pre-commit.com/) для автоматической проверки кода перед каждым коммитом.

---

## Быстрый старт

```bash
# После клонирования репозитория
make setup
```

Это установит pre-commit и активирует хуки. Теперь при каждом `git commit` будут автоматически запускаться проверки.

---

## Активные хуки

| Хук | Что проверяет | Файлы |
|-----|---------------|-------|
| `structure-sync` | README деревья соответствуют файловой системе | Все |
| `rules-validate` | Формат rule-файлов | `.claude/rules/*.md` |
| `scripts-validate` | Формат Python-скриптов | `**/.scripts/*.py` |
| `skills-validate` | Формат SKILL.md | `.claude/skills/*/SKILL.md` |
| `pr-template-validate` | Структура PR template | `.github/PULL_REQUEST_TEMPLATE.md` |
| `codeowners-validate` | Синтаксис CODEOWNERS | `.github/CODEOWNERS` |
| `type-templates-validate` | Соответствие type:* ↔ Issue Templates | `labels.yml`, `ISSUE_TEMPLATE/*.yml` |
| `actions-validate` | Формат GitHub Actions workflow | `.github/workflows/*.yml` |
| `security-validate` | Файлы безопасности GitHub | `dependabot.yml`, `SECURITY.md`, `codeql.yml` |
| `branch-validate` | Формат имени ветки (naming convention) | Все (always_run) |
| `github-required` | Наличие обязательных файлов GitHub | Все (always_run) |
| `docs-validate` | Наличие обязательных документов docs/ | Все (always_run) |
| `docs-readme-validate` | Дерево и таблицы docs/README.md соответствуют файловой системе | `specs/docs/` |
| `overview-validate` | Секции, таблицы, mermaid, консистентность overview.md | `specs/docs/.system/overview.md` |
| `conventions-validate` | Секции, таблицы, code-блоки, shared-пакеты conventions.md | `specs/docs/.system/conventions.md` |
| `infrastructure-validate` | Секции, таблицы, хранилища, окружения infrastructure.md | `specs/docs/.system/infrastructure.md` |
| `testing-validate` | Секции, таблицы, фреймворки, матрица покрытия testing.md | `specs/docs/.system/testing.md` |
| `service-validate` | Frontmatter, 10 секций, таблицы, подсекции API/Data Model в {svc}.md | `specs/docs/*.md` (кроме README) |
| `service-readme-validate` | Синхронизация docs/README.md с деревом сервисов | `specs/docs/` |
| `technology-validate` | Frontmatter, 8 секций, таблицы, версия standard-{tech}.md | `specs/docs/.technologies/standard-*.md` |
| `design-validate` | Frontmatter, SVC-N (9 подсекций), INT-N, STS-N, маркеры, зона ответственности design.md | `specs/analysis/*/design.md` |
| `plan-test-validate` | Frontmatter, TC-N формат, покрытие REQ-N/STS-N, маркеры, зона ответственности plan-test.md | `specs/analysis/*/plan-test.md` |
| `plan-dev-validate` | Frontmatter, TASK-N (5 полей), подзадачи, зависимости, TC трассируемость, маркеры plan-dev.md | `specs/analysis/*/plan-dev.md` |
| `discussion-validate` | Frontmatter, секции, нумерация, маркеры discussion.md | `specs/analysis/*/discussion.md` |
| `review-validate` | Наличие review.md, status=RESOLVED, вердикт READY, хотя бы одна итерация | `specs/analysis/*/review.md` (always_run) |
| `validate-commit-msg` | Формат commit message по Conventional Commits (stage: commit-msg) | Все (always_run) |
| `security-technology-validate` | Frontmatter `type: security`, 5 h2-секций, именование security-{tech}.md | `specs/docs/.technologies/security-*.md` |
| `deploy-validate` | Триггер, discover, matrix, environments, rollback, permissions deploy.yml | `.github/workflows/deploy.yml` |
| `gitleaks` | Обнаружение секретов (API keys, tokens, passwords) в staged diff | Все (pre-commit) |

---

## Как это работает

```
git add file.py          # Добавить файл в staging
git commit -m "..."      # Pre-commit запускается автоматически
                         │
                         ▼
┌─────────────────────────────────────────────┐
│  Pre-commit проверяет ТОЛЬКО staged файлы   │
│                                             │
│  ✅ Passed → коммит создаётся               │
│  ❌ Failed → коммит блокируется             │
└─────────────────────────────────────────────┘
```

---

## Конфигурация

Файл: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: local
    hooks:
      - id: structure-sync
        name: Check README structure sync
        entry: python .structure/.instructions/.scripts/pre-commit-structure.py
        # ...
```

---

## Добавление нового хука

1. Создать скрипт валидации в соответствующей папке `.scripts/`
2. Добавить хук в `.pre-commit-config.yaml`:

```yaml
- id: my-validate
  name: Validate my files
  entry: python path/to/validate.py
  language: system
  files: \.my$              # Регулярное выражение для файлов
  pass_filenames: true      # Передавать пути к файлам
  stages: [pre-commit]
```

3. Переустановить хуки: `pre-commit install -f`

---

## Временное отключение

```bash
# Пропустить все хуки локально (CI всё равно проверит при push)
git commit --no-verify -m "WIP"

# Пропустить конкретный хук
SKIP=scripts-validate git commit -m "..."
```

---

## Ручной запуск

```bash
# Проверить все файлы
pre-commit run --all-files

# Проверить конкретный хук
pre-commit run structure-sync --all-files

# Проверить staged файлы
pre-commit run
```

---

## Решение проблем

### Хук не запускается

```bash
pre-commit install -f
```

### Ошибка "файл не найден"

Проверьте что скрипт существует и путь в `entry` корректен.

### Хук падает на нескольких файлах

Скрипт должен принимать несколько путей: `nargs="*"` в argparse.

---

## Связанные документы

- [Инициализация проекта](./initialization.md) — установка pre-commit (`make setup`)
- [Процесс поставки ценности](/specs/.instructions/standard-process.md) — pre-commit хуки в контексте процесса (шаги 3.2–3.3)
- [CI workflow](/.github/workflows/ci.yml) — те же хуки запускаются на GitHub при push/PR
- [Makefile](/Makefile) — команда `make setup`
- [.pre-commit-config.yaml](/.pre-commit-config.yaml) — конфигурация хуков
