---
title: CI/CD интеграция валидаторов через Pre-commit
type: feature
status: draft
created: 2026-02-01
updated: 2026-02-03
related:
  - /.pre-commit-config.yaml
  - /.structure/.instructions/.scripts/pre-commit-structure.py
---

# CI/CD интеграция валидаторов

## Оглавление

- [Концепция](#концепция)
- [Архитектура](#архитектура)
- [Pre-commit хуки](#pre-commit-хуки)
- [Реализация](#реализация)
- [Следующие шаги](#следующие-шаги)

---

## Концепция

### Проблема

Валидация запускается вручную. Невалидные документы, скрипты и скиллы могут попасть в main без проверки.

### Решение: Pre-commit First

**Принцип:** Все проверки выполняются локально через pre-commit. CI/CD только дублирует их для внешних PR.

| Подход | API ключ | Где выполняется | Когда |
|--------|----------|-----------------|-------|
| Pre-commit | ❌ Не нужен | Локально | До коммита |
| Captain Holt | ✅ Нужен | Локально | Вручную (опционально) |

**Преимущества:**
- Быстрая обратная связь (до коммита)
- Нет затрат на API
- CI/CD — страховка, не основной механизм
- Работает оффлайн

---

## Архитектура

### Слои валидации

```
┌─────────────────────────────────────────────────────────────┐
│                    РАЗРАБОТЧИК                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   PRE-COMMIT ХУКИ                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │  structure  │ │   rules     │ │   scripts   │            │
│  │    sync     │ │  validate   │ │  validate   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐                                            │
│  │   skills    │                                            │
│  │  validate   │                                            │
│  └─────────────┘                                            │
│                                                              │
│  Результат: ✅ Passed → коммит разрешён                      │
│             ❌ Failed → коммит заблокирован                  │
└─────────────────────────────────────────────────────────────┘
```

**Captain Holt** (опционально) — семантический анализ документов, запускается вручную, требует API ключ.

### Матрица проверок

| Проверка | Скрипт | Что проверяет | Триггер |
|----------|--------|---------------|---------|
| structure-sync | `pre-commit-structure.py` | README деревья = файловая система | Любые файлы |
| rules-validate | `validate-rule.py` | Формат rule-файлов | `.claude/rules/*.md` |
| scripts-validate | `validate-script.py` | Формат Python-скриптов | `**/.scripts/*.py` |
| skills-validate | `validate-skill.py` | Формат SKILL.md | `.claude/skills/**/SKILL.md` |
| instructions-validate | `validate-instruction.py` | Формат инструкций | `**/.instructions/*.md` |
| links-validate | `validate-links.py` | Битые ссылки в markdown | `**/*.md` |

---

## Pre-commit хуки

### Текущее состояние

```yaml
# .pre-commit-config.yaml (текущий)
repos:
  - repo: local
    hooks:
      - id: structure-sync
        name: Check README structure sync
        entry: python .structure/.instructions/.scripts/pre-commit-structure.py
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-commit]
```

### Целевое состояние

```yaml
# .pre-commit-config.yaml (целевой)
repos:
  - repo: local
    hooks:
      # 1. Синхронизация README с файловой системой
      - id: structure-sync
        name: Check README structure sync
        entry: python .structure/.instructions/.scripts/pre-commit-structure.py
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-commit]

      # 2. Валидация rules
      - id: rules-validate
        name: Validate rules format
        entry: python .claude/.instructions/rules/.scripts/validate-rule.py
        language: system
        files: ^\.claude/rules/.*\.md$
        exclude: ^\.claude/rules/_old-.*\.md$
        pass_filenames: true
        stages: [pre-commit]

      # 3. Валидация скриптов
      - id: scripts-validate
        name: Validate scripts format
        entry: python .instructions/.scripts/validate-script.py
        language: system
        files: \.scripts/.*\.py$
        pass_filenames: true
        stages: [pre-commit]

      # 4. Валидация скиллов
      - id: skills-validate
        name: Validate skills format
        entry: python .claude/.instructions/skills/.scripts/validate-skill.py
        language: system
        files: ^\.claude/skills/.*/SKILL\.md$
        pass_filenames: true
        stages: [pre-commit]

      # 5. Валидация инструкций
      - id: instructions-validate
        name: Validate instructions format
        entry: python .instructions/.scripts/validate-instruction.py
        language: system
        files: \.instructions/.*\.md$
        exclude: README\.md$
        pass_filenames: true
        stages: [pre-commit]

      # 6. Валидация ссылок (опционально, может быть медленным)
      - id: links-validate
        name: Validate markdown links
        entry: python .structure/.instructions/.scripts/validate-links.py
        language: system
        files: \.md$
        pass_filenames: true
        stages: [pre-commit]
        verbose: true
```

### Описание хуков

#### 1. structure-sync (уже реализован ✅)

**Назначение:** Проверяет что деревья в README соответствуют реальной файловой системе.

**Скрипт:** `.structure/.instructions/.scripts/pre-commit-structure.py`

**Логика:**
1. Получает список staged файлов
2. Определяет затронутые папки
3. Запускает `validate-structure.py` для корневой структуры
4. Запускает `sync-readme.py --check` для README в затронутых папках

**Коды ошибок:**
- `T002`: Папка есть в ФС, нет в SSOT
- `T003`: Папка есть в SSOT, нет в ФС
- `R001`: Элемент в ФС, отсутствует в дереве README
- `R002`: Элемент в дереве README, отсутствует в ФС

#### 2. rules-validate

**Назначение:** Проверяет формат rule-файлов.

**Скрипт:** `.claude/.instructions/rules/.scripts/validate-rule.py`

**Что проверяет:**
- Наличие обязательного frontmatter (`description`, `globs`)
- Корректность формата globs
- Валидность markdown-структуры
- Отсутствие конфликтов paths

**Коды ошибок:** R001-R015 (см. validation-rule.md)

#### 3. scripts-validate

**Назначение:** Проверяет формат Python-скриптов автоматизации.

**Скрипт:** `.instructions/.scripts/validate-script.py`

**Что проверяет:**
- Наличие docstring с description
- Структура docstring (Args, Returns, Exit codes)
- Соответствие принципам (KISS, DRY, YAGNI)
- Обработка ошибок

**Коды ошибок:** S001-S032 (см. validation-script.md)

#### 4. skills-validate

**Назначение:** Проверяет формат SKILL.md файлов.

**Скрипт:** `.claude/.instructions/skills/.scripts/validate-skill.py`

**Что проверяет:**
- Наличие обязательного frontmatter
- Структура секций (Формат вызова, Воркфлоу, Чек-лист)
- Ссылка на SSOT инструкцию
- Корректность параметров

**Коды ошибок:** K001-K031 (см. validation-skill.md)

#### 5. instructions-validate

**Назначение:** Проверяет формат инструкций.

**Скрипт:** `.instructions/.scripts/validate-instruction.py`

**Что проверяет:**
- Наличие frontmatter (description, standard, standard-version)
- Структура документа (заголовки, оглавление)
- Ссылки на связанные документы

**Коды ошибок:** I001-I031 (см. validation-instruction.md)

#### 6. links-validate (опционально)

**Назначение:** Проверяет что все ссылки в markdown валидны.

**Скрипт:** `.structure/.instructions/.scripts/validate-links.py`

**Что проверяет:**
- Существование файлов по относительным путям
- Корректность якорей (#section)
- Отсутствие битых внутренних ссылок

**Примечание:** Может быть медленным на больших коммитах. Рекомендуется запускать только для .md файлов.

---

## Реализация

### Фаза 1: Адаптация скриптов (текущая)

Скрипты валидации должны поддерживать вызов с путём к файлу:

```bash
# Текущий вызов (по имени)
python validate-rule.py core

# Нужный вызов (по пути)
python validate-rule.py .claude/rules/core.md
```

**Статус скриптов:**

| Скрипт | Текущий вызов | Нужный вызов | Статус |
|--------|---------------|--------------|--------|
| `validate-rule.py` | `name` или `path` | `path` | ✅ Готов |
| `validate-script.py` | `path` | `path` | ✅ Готов |
| `validate-skill.py` | `name` или `path` | `path` | ✅ Готов |
| `validate-instruction.py` | `path` | `path` | ✅ Готов |
| `validate-links.py` | `path` | `path` | ✅ Готов |

### Фаза 2: Обновление pre-commit-config ✅

Обновлён `.pre-commit-config.yaml` с хуками:
- `structure-sync`
- `rules-validate`
- `scripts-validate`
- `skills-validate`

---

## Следующие шаги

### Приоритет 1: Pre-commit хуки ✅ ВЫПОЛНЕНО

- [x] Адаптировать `validate-rule.py` для приёма пути файла
- [x] Адаптировать `validate-skill.py` для приёма пути файла
- [x] Добавить хук `rules-validate` в `.pre-commit-config.yaml`
- [x] Добавить хук `scripts-validate` в `.pre-commit-config.yaml`
- [x] Добавить хук `skills-validate` в `.pre-commit-config.yaml`
- [x] Добавить `make setup` для установки pre-commit
- [ ] Протестировать все хуки локально с реальным коммитом

### Приоритет 2: GitHub Actions — НЕ ТРЕБУЕТСЯ

Для приватного репозитория pre-commit достаточно. GitHub Actions избыточны.

### Приоритет 3: Опциональные улучшения

- [ ] Добавить хук `instructions-validate`
- [ ] Добавить хук `links-validate`

> **Captain Holt** — запускается вручную (`/agent captain-holt`), не в pre-commit. Требует API ключ.

---

## FAQ

### Зачем дублировать проверки в CI, если есть pre-commit?

Pre-commit можно обойти (`git commit --no-verify`). CI — гарантия для main ветки.

### Почему не использовать только CI?

Обратная связь через 2-5 минут (CI) vs мгновенно (pre-commit). Разработчик узнаёт об ошибке до коммита.

### Нужен ли ANTHROPIC_API_KEY?

Нет, если не используете Captain Holt. Все структурные проверки работают локально.

### Как отключить pre-commit временно?

```bash
git commit --no-verify -m "WIP: временный коммит"
```

Но CI всё равно проверит при PR.
