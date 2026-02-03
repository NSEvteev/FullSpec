---
description: Pre-commit хуки — автоматическая валидация перед коммитом
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
# Пропустить все хуки (не рекомендуется)
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

- [Makefile](/Makefile) — команда `make setup`
- [.pre-commit-config.yaml](/.pre-commit-config.yaml) — конфигурация хуков
