---
description: Инициализация проекта — установка зависимостей и настройка окружения
standard: .structure/.instructions/standard-readme.md
standard-version: v1.1
---

# Инициализация проекта

После клонирования репозитория необходимо выполнить инициализацию для настройки локального окружения.

**Полезные ссылки:**
- [Структура проекта](./README.md)
- [Pre-commit хуки](./pre-commit.md)

---

## Оглавление

- [1. Быстрый старт](#1-быстрый-старт)
- [2. Зависимости](#2-зависимости)
- [3. Установка вручную](#3-установка-вручную)
- [4. Проверка установки](#4-проверка-установки)
- [5. Решение проблем](#5-решение-проблем)
- [CI (автоматически)](#ci-автоматически)
- [6. Настройка GitHub Security](#6-настройка-github-security)
- [Настройка GitHub Labels (опционально)](#настройка-github-labels-опционально)

---

## 1. Быстрый старт

```bash
# После клонирования репозитория
make setup
```

Эта команда автоматически:
- Установит pre-commit хуки
- Проверит наличие необходимых зависимостей

---

## 2. Зависимости

### Обязательные

| Инструмент | Назначение | Установка |
|------------|------------|-----------|
| **Python 3.8+** | Скрипты валидации | [python.org](https://www.python.org/downloads/) |
| **pre-commit** | Хуки перед коммитом | `pip install pre-commit` |
| **Git** | Контроль версий | [git-scm.com](https://git-scm.com/) |
| **GitHub CLI (gh)** | Работа с Issues, PR, Releases | `winget install GitHub.cli` |

---

## 3. Установка вручную

### Windows

```powershell
# 1. Pre-commit
pip install pre-commit

# 2. GitHub CLI
winget install GitHub.cli

# 3. Авторизация в GitHub (один раз)
gh auth login

# 4. Установка хуков
pre-commit install
```

### macOS

```bash
# 1. Pre-commit
pip install pre-commit

# 2. GitHub CLI
brew install gh

# 3. Авторизация в GitHub (один раз)
gh auth login

# 4. Установка хуков
pre-commit install
```

### Linux

```bash
# 1. Pre-commit
pip install pre-commit

# 2. GitHub CLI (Ubuntu/Debian)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# 3. Авторизация в GitHub (один раз)
gh auth login

# 4. Установка хуков
pre-commit install
```

---

## 4. Проверка установки

```bash
# Проверить версии
python --version      # Python 3.8+
pre-commit --version  # pre-commit 3.x
gh --version          # gh 2.x
git --version         # git 2.x

# Проверить авторизацию GitHub
gh auth status

# Проверить pre-commit хуки
pre-commit run --all-files
```

**Ожидаемый результат:**
```
Check README structure sync..........................Passed
Validate rules format................................Passed (или Skipped)
Validate scripts format..............................Passed (или Skipped)
Validate skills format...............................Passed (или Skipped)
Validate branch name.................................Passed
```

---

## 5. Решение проблем

### Pre-commit не запускается

```bash
# Переустановить хуки
pre-commit install -f
```

### gh: command not found

После установки gh CLI нужно перезапустить терминал или добавить в PATH:

**Windows:** `C:\Program Files\GitHub CLI`

### gh auth: not logged in

```bash
gh auth login
# Выбрать: GitHub.com → HTTPS → Login with browser
```

### Python не найден

Убедитесь что Python добавлен в PATH при установке.

---

## Что происходит при `make setup`

```
make setup
    │
    ├── pip install pre-commit     # Установка pre-commit
    │
    ├── pre-commit install         # Установка git hooks
    │
    └── Готово!
        │
        └── При каждом git commit
            автоматически запускаются
            проверки из .pre-commit-config.yaml
```

---

## CI (автоматически)

CI workflow уже настроен в репозитории — действий не требуется.

**Файл:** [`.github/workflows/ci.yml`](/.github/workflows/ci.yml)

**Что проверяет:** При каждом push в `main` и pull request запускаются те же pre-commit хуки на **всех** файлах. Если хуки были обойдены локально (`--no-verify`), CI поймает ошибку.

**Где смотреть результаты:** Вкладка Actions в GitHub → последний run, или:

```bash
gh run list --limit 5
gh run view <run-id> --log
```

---

## 6. Настройка GitHub Security

Файлы безопасности (`dependabot.yml`, `codeql.yml`, `SECURITY.md`) уже в репозитории из шаблона. Но **Settings не копируются** из template — их нужно настроить для каждого нового репозитория.

**SSOT:** [standard-security.md](/.github/.instructions/actions/security/standard-security.md)

### Шаг 1: Включить Dependabot

```
Settings → Code security and analysis →
  ✅ Dependabot alerts → Enable
  ✅ Dependabot security updates → Enable
```

### Шаг 2: Включить Secret Scanning

```
Settings → Code security and analysis →
  ✅ Secret scanning → Enable
  ✅ Push protection → Enable
```

### Шаг 3: Проверить файлы из шаблона

```bash
# Обновить контактный email в SECURITY.md
# Обновить директории сервисов в dependabot.yml
# Обновить matrix.language в codeql.yml
```

> **ВАЖНО:** НЕ включать Code Scanning → Default Setup в Settings. Используется Advanced Setup через `codeql.yml` (уже в репозитории). См. [standard-security.md § 4](/.github/.instructions/actions/security/standard-security.md#4-code-scanning-codeql).

---

## Настройка GitHub Labels (опционально)

После первоначальной настройки рекомендуется настроить систему меток GitHub:

```bash
# Запустить скрипт настройки меток
python .github/.instructions/.scripts/setup-labels.py
```

Скрипт:
- Удалит стандартные метки GitHub
- Создаст систему меток проекта (type:, priority:, area:, status:)

> **Примечание:** Скрипт будет создан при проработке `.github/.instructions/labels/`.

---

## Связанные документы

- [Pre-commit хуки](./pre-commit.md) — детали работы pre-commit
- [Makefile](/Makefile) — все команды проекта
- [CLAUDE.md](/CLAUDE.md) — инструкции для Claude Code
