# Скилл /commit — оценка и план

Удобный скилл для коммитов по Conventional Commits с автоматической генерацией сообщения.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G5 из standard-process.md — нет `/commit` скилла
**Почему создан:** Определить нужен ли скилл или достаточно standard-commit + pre-commit hooks
**Связанные файлы:**
- `/.github/.instructions/commits/standard-commit.md` — стандарт коммитов (Conventional Commits)
- `/.structure/pre-commit.md` — pre-commit хуки
- `specs/.instructions/standard-process.md` — §5 Фаза 3, шаг 3.3

## Содержание

### Что уже покрыто

- `standard-commit.md` — полный стандарт: формат, типы, scope, body, footer, breaking changes
- Pre-commit hooks — автоматическая валидация формата при `git commit`
- Claude Code — уже умеет формировать commit messages по стандарту (через rule `development.md`)

### Что даёт скилл

| Функция | Сейчас | С `/commit` |
|---------|--------|-------------|
| Формат сообщения | Claude знает из rule | Формальный вызов с гарантией |
| Выбор типа | Ручной | Автоопределение из `git diff` |
| Scope | Ручной | Автоопределение из изменённых файлов |
| Staging | `git add` вручную | Предложение файлов для staging |
| Breaking changes | Ручной footer | Автоопределение при изменении API |

### Артефакты

По архитектуре: **инструкция (SSOT) → скилл (обёртка)**.

| # | Артефакт | Путь | Статус |
|---|---------|------|--------|
| 1 | **Инструкция** (SSOT) | `/.github/.instructions/commits/create-commit.md` | **Нужно создать** |
| 2 | **Скилл** (обёртка) | `/.claude/skills/commit/SKILL.md` | **Нужно создать** |

### Формат вызова

```
/commit [--amend] [--no-verify]
```

### Порядок создания

1. `/instruction-create create-commit --path .github/.instructions/commits/`
2. `/skill-create commit`

## Решения

- Приоритет низкий — процесс работает без скилла
- Скилл добавляет удобство, не новую функциональность

## Открытые вопросы

- Достаточно ли rule + standard-commit.md или скилл реально нужен?
- Нужен ли скрипт для автоопределения type/scope из diff?

---

## Что уже описано в проекте

### standard-commit.md (`/.github/.instructions/commits/standard-commit.md`)

Полный стандарт Conventional Commits, покрывающий весь формат:

- **§ 1 Формат:** `{type}({scope}): {description}` + body + footer. Subject до 70 символов (жёсткое ограничение, отклоняется pre-commit hook)
- **§ 2 Типы:** 8 типов — `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf`
- **§ 3 Scope:** допустимые значения (имя модуля/сервиса/компонента/подсистемы), когда опустить scope (зависимости уровня проекта, инфраструктура, глобальные настройки)
- **§ 4 Body и Footer:** body 1-3 абзаца, строки до 72 символов; footer: `Closes`, `Fixes`, `Refs`, `BREAKING CHANGE`, `Reviewed-by`
- **§ 5 Правила:** нижний регистр, без точки, imperative mood, пробел после двоеточия, один логический блок = один коммит
- **§ 6 Процесс:** `git add` → `git commit` → pre-commit hooks (линтинг → форматирование → commitlint). При провале: коммит НЕ создан, запрещено `--no-verify` и `--amend`
- **§ 7 Исправление:** `--amend` допустим если коммит не запушен или запушен в feature-ветку (только ваша). Запушен в main или shared → новый коммит
- **§ 8 Язык:** type/scope — английский, description/body — русский, footer — английский

### commits/README.md (`/.github/.instructions/commits/README.md`)

Индекс секции commits. Секции "Воркфлоу", "Валидация", "Скрипты", "Скиллы" пусты — помечены `*Нет*`. Это подтверждает, что `create-commit.md` (инструкция-воркфлоу) и скилл `/commit` ещё не существуют.

### Pre-commit hooks (`/.structure/pre-commit.md`, `/.pre-commit-config.yaml`)

- 26 pre-commit хуков, ни один из них не валидирует формат commit message напрямую (нет commitlint/commit-msg hook)
- Все хуки привязаны к `stages: [pre-commit]` — проверяют файлы, не сообщение коммита
- Хуки: structure-sync, rules-validate, scripts-validate, skills-validate, pr-template-validate, codeowners-validate, type-templates-validate, actions-validate, security-validate, branch-validate, github-required, docs-validate и 14 других валидаторов specs/analysis
- **Важное открытие:** В `standard-commit.md § 6` упоминается commitlint как шаг 3 в pipeline hooks (линтинг → форматирование → **валидация сообщения коммита (commitlint)**), но в `.pre-commit-config.yaml` хук commitlint отсутствует. Это пробел — валидация формата сообщения коммита описана в стандарте, но не реализована

### Rule development.md (`/.claude/rules/development.md`)

Rule активируется при работе с git и GitHub. Содержит ссылки на все стандарты процесса разработки, включая `standard-commit.md`. Это механизм, через который Claude Code узнаёт стандарт при выполнении коммита.

### standard-process.md (`/specs/.instructions/standard-process.md`)

- **§ 5 Фаза 3, шаг 3.3 (строка 247):** `Commits | Conventional Commits, 25 pre-commit хуков | — | standard-commit.md`. Колонка скиллов — прочерк (`—`), подтверждает пробел G5
- **§ 8.1 Сводная таблица (строка 414):** Шаг 3.3 — инструкция `standard-commit`, скилл отсутствует, агент отсутствует, скрипт отсутствует
- **§ 8.2 Pre-commit хуки (строка 443):** Шаг 3.3 — "25 pre-commit хуков (все)"
- **§ 10 Пробелы (строка 515):** G5 — `Нет /commit скилла | Низкий | Процесс покрыт standard-commit + pre-commit hooks`

### standard-development.md (`/.github/.instructions/development/standard-development.md`)

- **§ 2 Процесс, шаг 5 (строка 194):** `КОММИТ → standard-commit.md` — коммит как финальный шаг цикла разработки
- **§ 5 (строка 280-284):** Pre-commit hooks запускаются автоматически при `git commit`, если не установлены — `make setup`

### validation-development.md (`/.github/.instructions/development/validation-development.md`)

Не содержит явных проверок формата коммита. Валидация: тесты → линтер → сборка → E2E → зависимости → полнота реализации. Формат коммита делегирован standard-commit.md и pre-commit hooks.

### standard-release.md (`/.github/.instructions/releases/standard-release.md`)

- **§ 3 (строка 155-166):** Автоопределение SemVer по типу коммита: `fix:` → PATCH, `feat:` → MINOR, `feat:` + `BREAKING CHANGE:` → MAJOR, `refactor:/docs:/chore:` → нет инкремента
- **§ 5 (строка 216-279):** CHANGELOG.md в формате Keep a Changelog 1.1.0, секции Added/Changed/Fixed/Removed, ссылки сравнения между тегами
- Прямая связь: правильные Conventional Commits → автоматическое определение версии → корректный changelog

### create-release.md (`/.github/.instructions/releases/create-release.md`)

- **Шаг 4:** Сборка Release Notes из PR (через `--generate-notes`). Conventional Commits в PR body → release notes
- Косвенная зависимость: качество commit messages → качество Release Notes

### Существующие скиллы — формат SKILL.md (`/.claude/skills/dev/SKILL.md`)

Формат скилла-обёртки: frontmatter (name, description, allowed-tools, ssot-version, argument-hint) → SSOT-ссылка → формат вызова → таблица параметров → воркфлоу → чек-лист → примеры. Скилл `/commit` должен следовать этому формату.

---

## Best practices

### Conventional Commits specification (v1.0.0)

- **Формат:** `<type>[optional scope]: <description>` с опциональным body и footer(s)
- **Связь с SemVer:** `fix` → PATCH, `feat` → MINOR, `BREAKING CHANGE` → MAJOR. Это ключевая причина стандартизации — автоматическое определение версии
- **`!` нотация:** `feat!: breaking API change` — альтернатива `BREAKING CHANGE:` в footer. Проект использует footer-вариант (standard-commit.md § 4), `!` нотация не описана — при создании скилла стоит решить, поддерживать ли оба варианта
- **Спецификация допускает кастомные типы** помимо `feat` и `fix`. Проект использует 8 типов (§ 2 стандарта) — расширенный набор, соответствующий Angular convention

### Автогенерация commit message из git diff

**Алгоритм для скилла `/commit`:**
1. `git diff --cached --stat` — определить какие файлы изменены, вычислить scope из путей
2. `git diff --cached` — получить полный diff для определения type (новые файлы → `feat`, исправления → `fix`, только .md → `docs`, только тесты → `test`)
3. Определить type по эвристике: наличие новых exports/endpoints → `feat`, удаление/изменение без новых → `fix`/`refactor`, package.json/go.mod → `chore`, CI файлы → `ci`
4. Проверить на BREAKING CHANGE: удаление публичных API, изменение сигнатур, изменение data model
5. Сформировать subject: `{type}({scope}): {description}` до 70 символов
6. При необходимости добавить body (если diff затрагивает >3 файлов или логика сложная)
7. Добавить footer: `Closes #N` из имени ветки (парсинг `git branch --show-current`)

**Определение scope из путей файлов:**
- `src/{service}/**` → scope = имя сервиса
- `shared/**` → scope = имя пакета или `shared`
- `platform/**` → scope = `infra` или имя компонента
- `.github/**` → scope = `ci` или `github`
- `.claude/**` → scope по типу артефакта (skill, rule, agent)
- `specs/**` → scope = `analysis` или `docs`
- Если файлы из разных областей → scope опустить

### Связь commit types с Semantic Versioning

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
| `BREAKING CHANGE` (любой type) | MAJOR | Breaking (отдельная секция) | Мажорная версия |

Эта таблица должна быть частью инструкции `create-commit.md` — чтобы при создании коммита Claude оценивал влияние на версию.

### Changelog generation из коммитов (Keep a Changelog)

- Проект уже использует Keep a Changelog 1.1.0 (standard-release.md § 5, `/CHANGELOG.md`)
- Секции: Added, Changed, Deprecated, Removed, Fixed, Security
- Маппинг commit type → секция: `feat` → Added, `fix` → Fixed, `perf`/`refactor` → Changed
- `--generate-notes` в `gh release create` генерирует Release Notes из PR titles — а PR titles формируются из commit messages (при squash merge)
- Качественные commit messages → качественные PR titles → качественные Release Notes → качественный CHANGELOG

### Инструменты экосистемы Conventional Commits

| Инструмент | Назначение | Релевантность для проекта |
|-----------|-----------|--------------------------|
| **commitlint** | Линтер commit messages (pre-commit/commit-msg hook) | Упомянут в standard-commit.md § 6, но НЕ установлен в .pre-commit-config.yaml — пробел |
| **commitizen** | Интерактивный wizard для формирования commit message | Не нужен — Claude Code заменяет wizard |
| **conventional-changelog** | Генерация CHANGELOG из git log | Может быть полезен для автоматизации create-release.md шаг 4 |
| **semantic-release** | Автоматический bump версии + release | Не подходит — проект использует ручные решения о версии (standard-release.md § 3: "Финальное решение о версии принимает человек") |
| **standard-version** | Автоматический CHANGELOG + tag + bump | Deprecated, заменён release-please |
| **release-please** | Автоматический release workflow от Google | Не подходит по той же причине, что semantic-release |

### Валидация commit message как pre-commit/commit-msg hook

**Текущий пробел:** standard-commit.md § 6 описывает commitlint как шаг 3 pipeline, но хук не реализован.

**Варианты реализации:**
1. **commitlint (Node.js)** — `@commitlint/config-conventional` + `commit-msg` hook через husky/pre-commit. Полная поддержка Conventional Commits, кастомные правила (допустимые scopes, русский язык description)
2. **Python-скрипт** — как остальные хуки проекта (все 26 хуков — Python). Плюс: единообразие с проектом (все `.scripts/*.py`). Минус: нужно самому реализовать парсер
3. **Через скилл `/commit`** — Claude формирует сообщение → гарантирует формат → хук не нужен. Минус: работает только при использовании скилла, ручные коммиты не валидируются

**Рекомендация:** Python-скрипт `.github/.instructions/commits/.scripts/validate-commit-msg.py` как `commit-msg` hook (stage: `commit-msg`, не `pre-commit`). Это закроет пробел в standard-commit.md § 6 И будет работать независимо от скилла.

### Атомарность коммитов — правила staging

**Best practice для скилла:**
1. Показать `git status` — unstaged/staged файлы
2. Предложить группировку файлов по логическому блоку (один коммит = одна цель)
3. Если unstaged файлы не относятся к текущему коммиту — предупредить
4. Если staged файлы относятся к разным целям — предложить разделить на несколько коммитов
5. Файлы `.env`, credentials — никогда не добавлять в staging (standard-development.md § 8)

### Обработка ошибок pre-commit hooks при коммите

Из standard-commit.md § 6:
- При провале hooks — коммит НЕ создан
- Запрещено `--no-verify` (пропуск hooks)
- Запрещено `--amend` (нечего amend'ить — коммит не создан)
- Нужно исправить причину и повторить `git commit`

Скилл `/commit` должен:
1. Выполнить `git commit`
2. При провале — прочитать вывод ошибки
3. Определить какой hook провалился и причину
4. Исправить (если возможно автоматически — форматирование, мелкие lint ошибки)
5. Повторить `git add` + `git commit` (НЕ `--amend`)
6. Если автоматическое исправление невозможно — сообщить пользователю причину и рекомендацию

### Commit signing и verification

- Git поддерживает GPG/SSH подпись коммитов (`git commit -S`)
- GitHub показывает "Verified" badge для подписанных коммитов
- В проекте не описан — ни в standard-commit.md, ни в standard-development.md
- Низкий приоритет для текущего проекта, но стоит учитывать при проектировании скилла: параметр `--sign` / `--no-sign` (по умолчанию — из git config)

### Связь с флагом `--amend` в скилле

Из standard-commit.md § 7:
- `--amend` допустим только для НЕ запушенных коммитов или feature-ветка только ваша
- При `--amend` на запушенном коммите — потребуется `git push --force-with-lease` (standard-sync.md)
- Скилл должен проверить: `git log --oneline -1 origin/{branch}..HEAD` — если пусто, коммит уже запушен → предупредить перед amend
