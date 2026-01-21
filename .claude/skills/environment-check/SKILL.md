---
name: environment-check
description: Проверка окружения (gh, git, python) перед выполнением скилла
allowed-tools: Bash
category: utility
triggers:
  commands:
    - /environment-check
  phrases:
    ru:
      - проверь окружение
      - проверь зависимости
    en:
      - check environment
      - check dependencies
---

# Проверка окружения

Микро-скилл для проверки доступности инструментов и зависимостей. Предназначен для переиспользования в других скиллах.

**Связанные скиллы:**
- [input-validate](/.claude/skills/input-validate/SKILL.md) — валидация входных данных

**Используется в:**
- [issue-create](/.claude/skills/issue-create/SKILL.md) — проверка gh перед созданием Issue
- [issue-update](/.claude/skills/issue-update/SKILL.md) — проверка gh перед обновлением Issue
- [issue-execute](/.claude/skills/issue-execute/SKILL.md) — проверка gh/git перед выполнением
- [issue-review](/.claude/skills/issue-review/SKILL.md) — проверка gh перед ревью
- [issue-complete](/.claude/skills/issue-complete/SKILL.md) — проверка gh перед закрытием
- [issue-delete](/.claude/skills/issue-delete/SKILL.md) — проверка gh перед закрытием

**Шаблоны:**
- [output-formats.md](/.claude/instructions/skills/output.md) — форматы вывода (SSOT)

## Оглавление

- [Формат вызова](#формат-вызова)
- [Проверки](#проверки)
- [Воркфлоу](#воркфлоу)
- [Интеграция в скиллы](#интеграция-в-скиллы)
- [Обработка ошибок](#обработка-ошибок)
- [Примеры использования](#примеры-использования)

---

## Формат вызова

```
/environment-check [инструменты...] [--silent] [--fix]
```

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `инструменты` | Список инструментов через пробел | Все основные |
| `--silent` | Не выводить сообщения, только код возврата | false |
| `--fix` | Показать команды установки при ошибке | false |

**Примеры:**
```
/environment-check                    # Проверить все основные
/environment-check gh git             # Только gh и git
/environment-check python --fix       # Python с инструкциями по установке
```

---

## Проверки

### Основные инструменты

| Инструмент | Команда проверки | Описание |
|------------|------------------|----------|
| `gh` | `gh --version` | GitHub CLI |
| `gh-auth` | `gh auth status` | Авторизация GitHub CLI |
| `git` | `git --version` | Git |
| `git-repo` | `git rev-parse --git-dir` | В репозитории Git |
| `python` | `python --version` | Python 3 |
| `node` | `node --version` | Node.js |
| `npm` | `npm --version` | NPM |

### Группы проверок

| Группа | Инструменты | Когда использовать |
|--------|-------------|-------------------|
| `github` | gh, gh-auth | issue-* скиллы |
| `git-ops` | git, git-repo | Любые git операции |
| `scripts` | python | Скиллы с Python скриптами |
| `frontend` | node, npm | Frontend разработка |
| `all` | Все инструменты | Полная проверка |

---

## Воркфлоу

### Шаг 1: Определить список проверок

1. Из аргументов: `/environment-check gh git`
2. Из группы: `/environment-check github`
3. По умолчанию: `gh`, `gh-auth`, `git`, `git-repo`

### Шаг 2: Выполнить проверки

Для каждого инструмента:

**gh:**
```bash
gh --version 2>/dev/null
# Ожидается: gh version X.Y.Z (...)
```

**gh-auth:**
```bash
gh auth status 2>&1
# Ожидается: Logged in to github.com as {username}
```

**git:**
```bash
git --version 2>/dev/null
# Ожидается: git version X.Y.Z
```

**git-repo:**
```bash
git rev-parse --git-dir 2>/dev/null
# Ожидается: .git или путь к .git
```

**python:**
```bash
python --version 2>/dev/null || python3 --version 2>/dev/null
# Ожидается: Python 3.X.Y
```

### Шаг 3: Собрать результаты

Для каждой проверки:
- `✅` — успешно
- `❌` — ошибка (с описанием)
- `⚠️` — предупреждение (работает, но не оптимально)

### Шаг 4: Вернуть результат

**Все проверки пройдены:**
```
✅ Окружение готово

Проверено:
- gh: 2.40.0
- gh-auth: Logged in as username
- git: 2.43.0
- git-repo: .git
```

**Есть ошибки:**
```
❌ Окружение не готово

✅ git: 2.43.0
✅ git-repo: .git
❌ gh: не установлен
❌ gh-auth: не проверено (gh не установлен)

Установка:
- gh: https://cli.github.com/
```

**Следующие шаги:**
- При успехе — продолжить выполнение основного скилла
- При ошибке — установить недостающие инструменты (см. команды с `--fix`)
- После установки — повторить `/environment-check` для подтверждения

---

## Интеграция в скиллы

### Как использовать в других скиллах

В начале воркфлоу добавить проверку окружения:

```markdown
### Шаг 0: Проверка окружения

Вызвать [/environment-check](/.claude/skills/environment-check/SKILL.md):

```
/environment-check github --fix
```

Если окружение не готово — остановить выполнение.
```

### Примеры интеграции

**issue-create (требует gh):**
```markdown
### Шаг 0: Проверка окружения

/environment-check gh gh-auth --fix

Если ошибка — показать инструкцию по установке и остановить.
```

**skill-create (требует git для отката):**
```markdown
### Шаг 0b: Fail-fast проверки

/environment-check git git-repo
```

---

## Обработка ошибок

> **SSOT:** [error-handling.md](/.claude/instructions/skills/errors.md)

| Ошибка | Код | Действие |
|--------|-----|----------|
| Инструмент не установлен | `ERR_NOT_INSTALLED` | Показать ссылку на установку |
| gh не авторизован | `ERR_NOT_AUTHORIZED` | Показать команду `gh auth login` |
| Не в git репозитории | `ERR_NOT_REPO` | Показать `git init` |
| Python 2 вместо 3 | `WARN_PYTHON2` | Предупредить, показать установку Python 3 |
| Неизвестный инструмент | `ERR_UNKNOWN` | Показать список доступных |

### Команды установки (--fix)

| Инструмент | macOS | Linux | Windows |
|------------|-------|-------|---------|
| gh | `brew install gh` | `sudo apt install gh` | `winget install GitHub.cli` |
| git | `brew install git` | `sudo apt install git` | `winget install Git.Git` |
| python | `brew install python` | `sudo apt install python3` | `winget install Python.Python.3` |
| node | `brew install node` | `sudo apt install nodejs` | `winget install OpenJS.NodeJS` |

---

## Чек-лист

- [ ] **Шаг 1:** Определил список проверок
- [ ] **Шаг 2:** Выполнил проверку каждого инструмента
- [ ] **Шаг 3:** Собрал результаты (✅/❌/⚠️)
- [ ] **Шаг 4:** Вернул результат с деталями

---

## Примеры использования

### Пример 1: Проверка GitHub окружения

**Вызов:**
```
/environment-check github
```

**Результат (успех):**
```
✅ Окружение готово

Проверено:
- gh: 2.40.0
- gh-auth: Logged in as myusername
```

### Пример 2: gh не установлен

**Вызов:**
```
/environment-check gh --fix
```

**Результат:**
```
❌ Окружение не готово

❌ gh: не установлен

Установка:
- macOS: brew install gh
- Linux: sudo apt install gh
- Windows: winget install GitHub.cli

Документация: https://cli.github.com/
```

### Пример 3: gh не авторизован

**Вызов:**
```
/environment-check gh-auth
```

**Результат:**
```
❌ Окружение не готово

✅ gh: 2.40.0
❌ gh-auth: You are not logged into any GitHub hosts

Авторизация:
gh auth login
```

### Пример 4: Полная проверка

**Вызов:**
```
/environment-check all
```

**Результат:**
```
✅ Окружение готово

Проверено:
- gh: 2.40.0
- gh-auth: Logged in as myusername
- git: 2.43.0
- git-repo: .git
- python: 3.11.5
- node: 20.10.0
- npm: 10.2.3
```

### Пример 5: Тихий режим

**Вызов:**
```
/environment-check git --silent
```

**Результат:**
*(нет вывода, код возврата 0 = успех, 1 = ошибка)*

---

## FAQ / Troubleshooting

### Как установить gh CLI?

**macOS:**
```bash
brew install gh
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install gh
```

**Windows:**
```powershell
winget install GitHub.cli
```

После установки выполните авторизацию: `gh auth login`

### Что делать если gh не авторизован?

Выполните команду авторизации:
```bash
gh auth login
```

Следуйте интерактивным инструкциям:
1. Выберите GitHub.com или Enterprise
2. Выберите протокол (HTTPS рекомендуется)
3. Авторизуйтесь через браузер или токен

### Как проверить конкретный инструмент?

Укажите инструмент или группу:
```
/environment-check gh              # только gh
/environment-check gh git          # gh и git
/environment-check github          # группа: gh + gh-auth
/environment-check all             # все инструменты
```

### Можно ли пропустить проверку?

Технически да — не вызывать `/environment-check`. Но это **не рекомендуется**, так как:
- Ошибки проявятся позже (сложнее диагностировать)
- Пользователь не получит инструкции по установке
- Скилл может выполниться частично

Используйте `--silent` если нужен только код возврата без вывода.

### Как добавить проверку нового инструмента?

1. Добавить в таблицу "Основные инструменты"
2. Описать команду проверки
3. Добавить команды установки для всех ОС (macOS, Linux, Windows)

### Почему gh-auth отдельно от gh?

`gh` может быть установлен, но не авторизован. Скиллы, работающие с GitHub API (issue-*), требуют обе проверки. Группа `github` включает обе.

### Можно ли кэшировать результаты проверок?

Нет. Окружение может измениться между вызовами (например, `gh auth logout`). Проверка выполняется каждый раз для актуальности результата.

### Что делать если Python 2 и Python 3 оба установлены?

Скилл проверяет сначала `python`, потом `python3`. Если `python` указывает на Python 2, будет предупреждение `WARN_PYTHON2`.

Решение: создать alias или использовать виртуальное окружение с Python 3.
