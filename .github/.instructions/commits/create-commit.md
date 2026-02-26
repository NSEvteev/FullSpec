---
description: Воркфлоу создания коммита — анализ diff, формирование message, staging, обработка ошибок hooks, amend, signing.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: .github/.instructions/commits/README.md
---

# Воркфлоу создания коммита

Рабочая версия стандарта: 1.3

Процесс создания коммита по Conventional Commits: анализ diff, определение type/scope, формирование message, staging, обработка ошибок hooks, amend, signing.

**Полезные ссылки:**
- [Инструкции commits](./README.md)
- [Стандарт коммитов](./standard-commit.md) — SSOT формата

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-commit.md](./standard-commit.md) |
| Валидация | *Покрыта скриптом [validate-commit-msg.py](./.scripts/validate-commit-msg.py)* |
| Создание | Этот документ |
| Модификация | *Будет создан* |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Анализ staging](#шаг-1-анализ-staging)
  - [Шаг 2: Определение type из diff](#шаг-2-определение-type-из-diff)
  - [Шаг 3: Определение scope из путей](#шаг-3-определение-scope-из-путей)
  - [Шаг 4: Формирование commit message](#шаг-4-формирование-commit-message)
  - [Шаг 5: Выполнение git commit](#шаг-5-выполнение-git-commit)
  - [Шаг 6: Обработка ошибок pre-commit hooks](#шаг-6-обработка-ошибок-pre-commit-hooks)
  - [Шаг 7: Логика --amend](#шаг-7-логика---amend)
  - [Шаг 8: Commit signing](#шаг-8-commit-signing)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Один коммит = одна цель.** Не смешивать разные задачи в одном коммите.

> **Формат — из стандарта.** Все правила формата — в [standard-commit.md](./standard-commit.md). Эта инструкция описывает процесс, не формат.

> **Hooks не пропускать.** `--no-verify` запрещён. Если hook провалился — исправить причину.

> **Amend — только для незапушенных коммитов.** Запушенный в main коммит нельзя amend'ить.

> **Signing — не форсировать.** Уважать настройки git config пользователя.

---

## Шаги

### Шаг 1: Анализ staging

1. Выполнить `git status` — определить unstaged/staged файлы
2. Предложить группировку по логическому блоку (один коммит = одна цель)
3. Если unstaged файлы не относятся к текущему коммиту — предупредить
4. Если staged файлы из разных целей — предложить разделить на несколько коммитов
5. `.env`, credentials, секреты — НИКОГДА не добавлять в staging

### Шаг 2: Определение type из diff

Выполнить `git diff --cached` и определить type:

| Признак в diff | type |
|----------------|------|
| Новые файлы, exports, endpoints | `feat` |
| Исправления без новой функциональности | `fix` |
| Только `.md` файлы | `docs` |
| Только тесты | `test` |
| `package.json`, `go.mod`, зависимости | `chore` |
| CI файлы (`.github/workflows/`, `.pre-commit-config.yaml`) | `ci` |
| Удаление/переименование без изменения поведения | `refactor` |
| Оптимизация производительности | `perf` |

### Шаг 3: Определение scope из путей

Выполнить `git diff --cached --stat` и вычислить scope из путей (маппинг из [standard-commit.md § 3](./standard-commit.md#3-scope)):

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

### Шаг 4: Формирование commit message

1. Сформировать subject: `{type}({scope}): {description}` — до 70 символов
2. Description — нижний регистр, без точки в конце, начать с глагола, пробел после двоеточия
3. При необходимости добавить body (diff затрагивает >3 файлов или логика сложная)
4. Проверить на BREAKING CHANGE: удаление публичных API, изменение сигнатур, изменение data model → footer `BREAKING CHANGE: описание`
5. Добавить footer `Closes #N` из имени ветки — парсинг `git branch --show-current` (формат `NNNN-*`)

**Запрет:** `!` нотация не поддерживается. Только footer `BREAKING CHANGE:`.

### Шаг 5: Выполнение git commit

```bash
git commit -m "{subject}" -m "{body}" -m "{footer}"
```

Для многострочных сообщений использовать HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
{type}({scope}): {description}

{body}

{footer}
EOF
)"
```

### Шаг 6: Обработка ошибок pre-commit hooks

1. Выполнить `git commit`
2. При провале — прочитать вывод ошибки
3. Определить какой hook провалился и причину
4. Исправить автоматически если возможно (форматирование, мелкие lint ошибки)
5. Повторить `git add` + `git commit` (НЕ `--amend` — коммит не был создан)
6. Если автоматическое исправление невозможно — сообщить пользователю причину и рекомендацию

**Запреты:**
- `--no-verify` — пропуск hooks запрещён
- `--amend` после провала hooks — коммит не создан, нечего amend'ить

### Шаг 7: Логика --amend

Перед amend проверить push-статус:

```bash
git log --oneline -1 origin/{branch}..HEAD
```

| Результат | Действие |
|-----------|----------|
| Коммит не запушен (есть вывод) | amend безопасен |
| Коммит запушен в feature-ветку (пусто, только вы работаете) | допустимо, предупредить о `--force-with-lease` |
| Коммит запушен в main/shared ветку | запрет amend, предложить новый коммит |

### Шаг 8: Commit signing

- Если в git config настроена подпись (`commit.gpgsign = true`) → коммит подписывается автоматически
- Не форсировать подпись, если не настроена
- Не передавать `--no-gpg-sign` без явного запроса пользователя

---

## Чек-лист

### Staging
- [ ] `git status` проверен
- [ ] Файлы сгруппированы по логическому блоку
- [ ] Секреты не добавлены в staging

### Message
- [ ] type определён из diff
- [ ] scope определён из путей (или опущен обоснованно)
- [ ] Subject ≤ 70 символов
- [ ] Description — нижний регистр, без точки, пробел после `:`
- [ ] Body добавлен (если >3 файлов или сложная логика)
- [ ] BREAKING CHANGE проверен
- [ ] `Closes #N` добавлен (если есть Issue)

### Commit
- [ ] `git commit` выполнен
- [ ] Hooks пройдены
- [ ] amend проверен на push-статус (если используется)

---

## Примеры

### Простой коммит

```bash
git add src/auth/handlers/login.go
git commit -m "feat(auth): добавить валидацию JWT"
```

### Коммит с body и footer

```bash
git add src/api/
git commit -m "$(cat <<'EOF'
fix(api): обработать null response от внешнего сервиса

Внешний сервис иногда возвращает null вместо пустого массива.
Добавлена проверка на null перед итерацией.

Closes #42
EOF
)"
```

### Коммит с BREAKING CHANGE

```bash
git commit -m "$(cat <<'EOF'
feat(api): изменить формат ответа /users

Ответ теперь возвращает объект {data: [], meta: {}} вместо массива.

BREAKING CHANGE: ответ /users больше не массив, клиенты должны читать поле data
Closes #99
EOF
)"
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-commit-msg.py](./.scripts/validate-commit-msg.py) | Валидация формата commit message | [standard-commit.md](./standard-commit.md) |

---

## Скиллы

*Нет скиллов.*
