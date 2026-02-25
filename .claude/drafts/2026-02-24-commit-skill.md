---
description: Обогащение standard-commit.md + инструкция create-commit.md + commit-agent + validate-commit-msg.py
type: feature
status: done
created: 2026-02-24
---

# Коммиты — обогащение стандарта + инструкция + агент

Вместо скилла `/commit`: обогатить стандарт, создать инструкцию процесса и commit-agent для экономии контекста основного LLM.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G5 из standard-process.md — нет `/commit` скилла
**Почему создан:** Анализ показал, что скилл даёт минимальную пользу (Claude уже знает стандарт через rule `development.md`). Вместо этого: обогатить стандарт полезной информацией, вынести операционные детали в инструкцию, создать агента для экономии контекста.
**Связанные файлы:**
- `/.github/.instructions/commits/standard-commit.md` — стандарт коммитов (SSOT формата)
- `/.github/.instructions/commits/README.md` — индекс секции commits
- `/.structure/pre-commit.md` — pre-commit хуки
- `/.claude/rules/development.md` — rule, загружающий стандарт при git-операциях
- `/specs/.instructions/standard-process.md` — §5 Фаза 3, шаг 3.3; §10 G5

## Содержание

### Почему не скилл

| Критерий | Скилл `/commit` | Агент `commit-agent` |
|----------|-----------------|----------------------|
| Контекст основного LLM | Тратит (скилл = промпт в основном контексте) | Не тратит (subprocess) |
| Чтение стандарта | Каждый раз в основном контексте | Один раз в subprocess |
| Вызов | Явный `/commit` | Автоматический через Task tool |
| Поддержка | Скилл + инструкция | Агент + инструкция |

Агент решает главную проблему — **экономия контекста** — лучше, чем скилл.

### Архитектура

```
standard-commit.md          (правила формата — что)
       ↓ ссылается
create-commit.md            (инструкция процесса — как)
       ↓ SSOT для
commit-agent (AGENT.md)     (исполнитель — делает)
```

### Артефакт 1: Обогащение `standard-commit.md`

**Путь:** `/.github/.instructions/commits/standard-commit.md`
**Действие:** Добавить 3 блока в существующие секции.

#### 1.1. Таблица type → SemVer → CHANGELOG (→ новая § 9)

Мотивирует правильный выбор type — показывает влияние на версию и changelog.

| Commit type | SemVer bump | CHANGELOG секция | Влияние на Release |
|-------------|-------------|-----------------|-------------------|
| `feat` | MINOR | Added | Новая функциональность |
| `fix` | PATCH | Fixed | Исправление |
| `perf` | PATCH | Changed | Оптимизация |
| `refactor` | — (нет bump) | Changed (опционально) | Не влияет на версию |
| `docs` | — | — | Не влияет |
| `test` | — | — | Не влияет |
| `chore` | — | — | Не влияет |
| `ci` | — | — | Не влияет |
| любой type + `BREAKING CHANGE` | MAJOR | Breaking | Мажорная версия |

Ссылка на источник: `standard-release.md` §3.

#### 1.2. Маппинг scope из структуры проекта (→ расширение § 3)

Конкретизирует абстрактное "имя модуля" привязкой к реальным путям:

| Путь файла | scope |
|------------|-------|
| `src/{service}/**` | имя сервиса |
| `shared/**` | имя пакета или `shared` |
| `platform/**` | `infra` или имя компонента |
| `.github/**` | `ci` или `github` |
| `.claude/**` | по типу артефакта (`skill`, `rule`, `agent`) |
| `specs/**` | `analysis` или `docs` |
| `.instructions/**` | `docs` или имя секции |
| Файлы из разных областей | scope опустить |

#### 1.3. Решение по `!` нотации (→ дополнение § 4)

Conventional Commits допускает `feat!: breaking change` как альтернативу `BREAKING CHANGE:` в footer. Текущий стандарт описывает только footer-вариант.

**Решение:** Не поддерживать `!` нотацию. Причины:
- Footer-вариант (`BREAKING CHANGE: описание`) явнее — содержит описание того, что сломано
- `!` легко пропустить при чтении git log
- Один способ делать одно и то же — проще валидировать

Добавить в §4: явный запрет `!` нотации с объяснением.

### Артефакт 2: Инструкция `create-commit.md`

**Путь:** `/.github/.instructions/commits/create-commit.md`
**Действие:** Создать через `/instruction-create`.
**Тип:** воркфлоу (create-*)

Содержание инструкции — операционные детали процесса создания коммита:

#### 2.1. Алгоритм автогенерации commit message из diff

1. `git diff --cached --stat` — определить изменённые файлы, вычислить scope из путей (по маппингу из §3 стандарта)
2. `git diff --cached` — получить полный diff для определения type:
   - Новые файлы, exports, endpoints → `feat`
   - Исправления без новой функциональности → `fix`
   - Только `.md` файлы → `docs`
   - Только тесты → `test`
   - `package.json`, `go.mod`, зависимости → `chore`
   - CI файлы → `ci`
   - Удаление/переименование без изменения поведения → `refactor`
3. Проверить на BREAKING CHANGE: удаление публичных API, изменение сигнатур, изменение data model
4. Сформировать subject: `{type}({scope}): {description}` до 70 символов
5. При необходимости добавить body (diff затрагивает >3 файлов или логика сложная)
6. Добавить footer: `Closes #N` из имени ветки (парсинг `git branch --show-current` — формат `NNNN-*`)

#### 2.2. Правила staging и атомарность

1. Показать `git status` — unstaged/staged файлы
2. Предложить группировку по логическому блоку (один коммит = одна цель)
3. Если unstaged файлы не относятся к текущему коммиту — предупредить
4. Если staged файлы из разных целей — предложить разделить на несколько коммитов
5. `.env`, credentials, секреты — НИКОГДА не добавлять в staging

#### 2.3. Обработка ошибок pre-commit hooks

1. Выполнить `git commit`
2. При провале — прочитать вывод ошибки
3. Определить какой hook провалился и причину
4. Исправить автоматически если возможно (форматирование, мелкие lint ошибки)
5. Повторить `git add` + `git commit` (НЕ `--amend` — коммит не был создан)
6. Если автоматическое исправление невозможно — сообщить пользователю причину и рекомендацию

**Запреты:** `--no-verify`, `--amend` после провала hooks.

#### 2.4. Логика `--amend`

- Проверить: `git log --oneline -1 origin/{branch}..HEAD` — если пусто, коммит уже запушен
- Запушен в main/shared ветку → запрет amend, предложить новый коммит
- Запушен в feature-ветку (только ваша) → допустимо, предупредить о `--force-with-lease`
- Не запушен → amend безопасен

#### 2.5. Commit signing

- Если в git config настроена подпись (`commit.gpgsign = true`) → коммит подписывается автоматически
- Не форсировать подпись, если не настроена
- Не передавать `--no-gpg-sign` без явного запроса пользователя

### Артефакт 3: Агент `commit-agent`

**Путь:** `/.claude/agents/commit-agent/AGENT.md`
**Действие:** Создать через `/agent-create`.

**Конфигурация:**

| Поле | Значение |
|------|---------|
| name | commit-agent |
| description | Создание коммитов по Conventional Commits |
| model | haiku (экономия, задача шаблонная) |
| allowed-tools | Bash, Read, Glob, Grep |
| ssot | `/.github/.instructions/commits/create-commit.md` |

**Промпт агента (суть):**
- Прочитать SSOT-инструкцию `create-commit.md`
- Выполнить алгоритм: анализ diff → определение type/scope → формирование message → git commit
- При провале hooks — исправить и повторить
- Вернуть результат: коммит создан / ошибка + причина

**Вызов из основного LLM:**
```
Task tool → subagent_type: "general-purpose"
prompt: "Выполни коммит изменений. Прочитай инструкцию create-commit.md и следуй ей."
```

Rule `development.md` будет обновлён — добавить указание делегировать коммиты агенту `commit-agent`.

**Изменение в rule:**
```
- Коммиты: [standard-commit.md](/.github/.instructions/commits/standard-commit.md)
+ Коммиты: делегировать агенту `commit-agent` через Task tool (SSOT: [create-commit.md](/.github/.instructions/commits/create-commit.md))
```

### Порядок создания

| # | Артефакт | Инструмент | Зависимости |
|---|---------|------------|-------------|
| 1 | Обогащение `standard-commit.md` | Ручное редактирование | — |
| 2 | Миграция после обновления стандарта | `/migration-create` | ← 1 |
| 3 | Инструкция `create-commit.md` | `/instruction-create` | ← 1 |
| 4 | Агент `commit-agent` | `/agent-create` | ← 3 |
| 5 | Скрипт `validate-commit-msg.py` | `/script-create` | ← 1 |
| 6 | Хук в `.pre-commit-config.yaml` | Ручное | ← 5 |
| 7 | Документация хука в `pre-commit.md` | Ручное | ← 5 |
| 8 | Обновление `commits/README.md` | Автоматически (шаги 3, 4, 5) | ← 3, 4, 5 |
| 9 | Обновление rule `development.md` | Ручное | ← 4 |
| 10 | Обновление `standard-process.md` §8/§10 | Ручное | ← 4, 5 |

### Артефакт 4: Скрипт `validate-commit-msg.py` + commit-msg hook

**Проблема:** `standard-commit.md` §6 описывает commitlint как шаг 3 pipeline, но хук не реализован в `.pre-commit-config.yaml`.

**Скрипт:**
- **Путь:** `/.github/.instructions/commits/.scripts/validate-commit-msg.py`
- **Действие:** Создать через `/script-create`
- **Stage:** `commit-msg` (не `pre-commit` — проверяет сообщение, не файлы)

**Что валидирует:**
- Формат `{type}({scope}): {description}` (§1)
- Допустимые типы: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf` (§2)
- Subject ≤ 70 символов (§1)
- Нижний регистр в description (§5)
- Без точки в конце (§5)
- Пробел после двоеточия (§5)
- Запрет `!` нотации (§4, новое решение)
- Footer: допустимые ключевые слова `Closes`, `Fixes`, `Refs`, `BREAKING CHANGE`, `Reviewed-by` (§4)

**Обновление 2 файлов:**

1. `/.pre-commit-config.yaml` — добавить хук:
```yaml
- repo: local
  hooks:
    - id: validate-commit-msg
      name: validate-commit-msg
      entry: python .github/.instructions/commits/.scripts/validate-commit-msg.py
      language: python
      stages: [commit-msg]
      always_run: true
```

2. `/.structure/pre-commit.md` — добавить хук в документацию (таблица хуков)

## Решения

- **Скилл `/commit` не создаём** — агент решает задачу экономии контекста лучше
- **Стандарт обогащаем** тремя блоками: SemVer-таблица, scope-маппинг, запрет `!` нотации
- **Инструкция `create-commit.md`** — SSOT для операционных деталей (алгоритм, staging, ошибки, amend, signing)
- **Агент `commit-agent`** — subprocess, читает инструкцию, выполняет коммит, экономит контекст основного LLM
- **Модель агента: haiku** — задача шаблонная, не требует мощной модели
- **`!` нотацию не поддерживаем** — один способ для breaking changes (footer)
- **Rule `development.md` обновить** — заменить ссылку на `standard-commit.md` на делегирование агенту `commit-agent`
- **commitlint hook включён в scope** — скрипт `validate-commit-msg.py` + обновление `.pre-commit-config.yaml` и `pre-commit.md`

## Открытые вопросы

*Нет открытых вопросов.*

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Обогатить standard-commit.md
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Артефакт 1")
    Добавить 3 блока в .github/.instructions/commits/standard-commit.md:
    1.1. Новая §9 — таблица type → SemVer → CHANGELOG (влияние коммита на релиз)
    1.2. Расширение §3 — маппинг scope из структуры проекта (путь файла → scope)
    1.3. Дополнение §4 — явный запрет ! нотации с объяснением (только footer BREAKING CHANGE)
  activeForm: Обогащаю standard-commit.md

TASK 2: Миграция после обновления стандарта
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Порядок создания", шаг 2)
    /migration-create для standard-commit.md.
    Синхронизировать все зависимые файлы после обновления стандарта.
  activeForm: Мигрирую зависимости standard-commit

TASK 3: Создать инструкцию create-commit.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Артефакт 2")
    /instruction-create для .github/.instructions/commits/create-commit.md.
    Содержание:
    - 2.1. Алгоритм автогенерации commit message из diff (6 шагов)
    - 2.2. Правила staging и атомарность (5 пунктов)
    - 2.3. Обработка ошибок pre-commit hooks (6 шагов, запрет --no-verify/--amend)
    - 2.4. Логика --amend (проверка push-статуса)
    - 2.5. Commit signing (уважать git config, не форсировать)
  activeForm: Создаю create-commit.md

TASK 4: Создать агент commit-agent
  blockedBy: [3]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Артефакт 3")
    /agent-create для .claude/agents/commit-agent/AGENT.md.
    Конфигурация: model=haiku, tools=Bash/Read/Glob/Grep,
    ssot=create-commit.md.
    Промпт: прочитать SSOT → анализ diff → type/scope → message → git commit.
    При провале hooks — исправить и повторить.
  activeForm: Создаю commit-agent

TASK 5: Создать скрипт validate-commit-msg.py
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Артефакт 4")
    /script-create для .github/.instructions/commits/.scripts/validate-commit-msg.py.
    Валидация: формат type(scope): desc, допустимые типы, subject ≤70,
    нижний регистр, без точки, пробел после двоеточия, запрет ! нотации,
    допустимые footer keywords.
  activeForm: Создаю validate-commit-msg.py

TASK 6: Добавить commit-msg hook в .pre-commit-config.yaml
  blockedBy: [5]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Артефакт 4", блок yaml)
    Добавить в .pre-commit-config.yaml хук:
    repo=local, id=validate-commit-msg, stage=commit-msg,
    entry=python .github/.instructions/commits/.scripts/validate-commit-msg.py,
    always_run=true.
  activeForm: Добавляю commit-msg hook

TASK 7: Документировать хук в pre-commit.md
  blockedBy: [5]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Артефакт 4", пункт 2)
    Добавить validate-commit-msg в таблицу хуков в .structure/pre-commit.md.
    Stage: commit-msg, назначение: валидация формата commit message.
  activeForm: Документирую хук в pre-commit.md

TASK 8: Обновить commits/README.md
  blockedBy: [3, 4, 5]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Порядок создания", шаг 8)
    Обновить .github/.instructions/commits/README.md:
    - Добавить ссылку на create-commit.md (инструкция)
    - Добавить ссылку на commit-agent (агент)
    - Добавить ссылку на validate-commit-msg.py (скрипт)
    README обновляется автоматически при создании артефактов, но проверить полноту.
  activeForm: Обновляю commits/README.md

TASK 9: Обновить rule development.md
  blockedBy: [4]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Артефакт 3", блок "Изменение в rule")
    В .claude/rules/development.md заменить строку:
    - Было: Коммиты: [standard-commit.md](путь)
    - Стало: Коммиты: делегировать агенту commit-agent через Task tool
      (SSOT: [create-commit.md](путь))
  activeForm: Обновляю rule development.md

TASK 10: Обновить standard-process.md §8/§10
  blockedBy: [4, 5]
  description: >
    Драфт: .claude/drafts/2026-02-24-commit-skill.md (секция "Порядок создания", шаг 10)
    Обновить /specs/.instructions/standard-process.md:
    - §8: добавить ссылки на create-commit.md и commit-agent
    - §10 G5: отметить как закрытый gap
  activeForm: Обновляю standard-process.md
```
