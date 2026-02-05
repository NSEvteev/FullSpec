---
description: Стандарт безопасности GitHub — Dependabot, CodeQL, Secret Scanning
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/actions/security/README.md
---

# Стандарт безопасности GitHub

Версия стандарта: 1.0

Настройка инструментов безопасности GitHub: Dependabot, Code Scanning (CodeQL), Secret Scanning и политика SECURITY.md.

**Полезные ссылки:**
- [Инструкции security](./README.md)
- [GitHub Security Features (Docs)](https://docs.github.com/en/code-security)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Не создано* |
| Создание | *Не создано* |
| Модификация | *Не создано* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Файлы и расположение](#2-файлы-и-расположение)
- [3. Dependabot](#3-dependabot)
- [4. Code Scanning (CodeQL)](#4-code-scanning-codeql)
- [5. Secret Scanning](#5-secret-scanning)
- [6. SECURITY.md](#6-securitymd)
- [7. CLI команды](#7-cli-команды)
- [8. Не включено в стандарт](#8-не-включено-в-стандарт)

---

## 1. Назначение

Стандарт описывает настройку встроенных инструментов безопасности GitHub для репозитория.

**Что покрывает:**

| Инструмент | Назначение |
|------------|-----------|
| **Dependabot** | Автоматическое обновление зависимостей и алерты уязвимостей |
| **Code Scanning (CodeQL)** | Статический анализ кода (SAST) |
| **Secret Scanning** | Обнаружение секретов в коде |
| **SECURITY.md** | Политика безопасности и процесс disclosure |

**Когда настраивать:**
- При создании нового репозитория — сразу
- Dependabot Alerts — включить всегда (бесплатно для public и private)
- Code Scanning — включить при наличии поддерживаемого языка
- Secret Scanning — включить всегда

---

## 2. Файлы и расположение

```
.github/
├── dependabot.yml              # Конфигурация Dependabot
├── SECURITY.md                 # Политика безопасности
└── workflows/
    └── codeql.yml              # Workflow для Code Scanning
```

| Файл | Обязательный | Описание |
|------|-------------|----------|
| `dependabot.yml` | Да | Конфигурация обновлений зависимостей |
| `SECURITY.md` | Да | Политика безопасности и контакты |
| `workflows/codeql.yml` | Рекомендуется | Workflow Code Scanning |

---

## 3. Dependabot

### Dependabot Alerts

Автоматические уведомления об уязвимостях в зависимостях.

**Включение:** Settings → Code security and analysis → Dependabot alerts → Enable.

**Поведение:** GitHub сканирует lock-файлы и манифесты зависимостей, создаёт Security Alerts при обнаружении CVE.

### Dependabot Security Updates

Автоматические PR для исправления уязвимых зависимостей.

**Включение:** Settings → Code security and analysis → Dependabot security updates → Enable.

**Поведение:** При обнаружении уязвимости Dependabot создаёт PR с обновлением до безопасной версии.

### Dependabot Version Updates

Автоматические PR для поддержания актуальных версий зависимостей.

**Конфигурация:** `.github/dependabot.yml`

```yaml
version: 2
updates:
  # Python (pip)
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
    commit-message:
      prefix: "deps"

  # Docker
  - package-ecosystem: "docker"
    directory: "/platform/docker/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
    commit-message:
      prefix: "deps"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
    commit-message:
      prefix: "ci"
```

**Параметры конфигурации:**

| Параметр | Обязательный | Описание |
|----------|-------------|----------|
| `package-ecosystem` | Да | Тип менеджера пакетов (`pip`, `npm`, `docker`, `github-actions` и др.) |
| `directory` | Да | Путь к манифесту зависимостей относительно корня |
| `schedule.interval` | Да | Частота проверки (`daily`, `weekly`, `monthly`) |
| `schedule.day` | Нет | День недели для `weekly` |
| `open-pull-requests-limit` | Нет | Макс. открытых PR (по умолчанию 5) |
| `labels` | Нет | Метки для PR |
| `commit-message.prefix` | Нет | Префикс коммит-сообщения |
| `reviewers` | Нет | Ревьюеры для PR |
| `ignore` | Нет | Исключения (зависимости или версии) |

**Исключение зависимостей:**

```yaml
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    ignore:
      - dependency-name: "some-legacy-package"
        # Не обновлять major-версии
        update-types: ["version-update:semver-major"]
```

---

## 4. Code Scanning (CodeQL)

### Назначение

CodeQL — движок статического анализа кода от GitHub. Выявляет уязвимости (SQL injection, XSS, path traversal и др.) без запуска кода.

**Поддерживаемые языки:** Python, JavaScript/TypeScript, Go, Java, C/C++, C#, Ruby, Swift, Kotlin.

### Настройка

**Вариант 1: Default Setup** (рекомендуется для начала)

Settings → Code security and analysis → Code scanning → Enable → Default setup.

GitHub автоматически создаёт workflow, определяет языки, запускает анализ на push и PR.

**Вариант 2: Advanced Setup** (кастомный workflow)

```yaml
# .github/workflows/codeql.yml
name: "CodeQL"

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 6 * * 1"  # Еженедельно, понедельник 06:00 UTC

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
      actions: read

    strategy:
      fail-fast: false
      matrix:
        language: ["python"]

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          # queries: +security-and-quality  # Расширенный набор запросов

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
```

### Правила

| Правило | Описание |
|---------|----------|
| Триггеры | Push в main, PR в main, еженедельный cron |
| Языки | Указывать только используемые в проекте |
| `fail-fast: false` | Анализ каждого языка независим |
| `security-events: write` | Обязательное разрешение для записи результатов |
| Schedule | Еженедельный запуск для обнаружения новых уязвимостей в существующем коде |

---

## 5. Secret Scanning

### Назначение

Автоматическое обнаружение секретов (API-ключи, токены, пароли), случайно закоммиченных в репозиторий.

**Включение:** Settings → Code security and analysis → Secret scanning → Enable.

### Push Protection

**Push Protection** блокирует push, содержащий обнаруженный секрет.

**Включение:** Settings → Code security and analysis → Push protection → Enable.

**Поведение:**
- При `git push` GitHub сканирует diff
- Если обнаружен секрет — push отклоняется с описанием найденного секрета
- Автор может: исправить коммит, пометить как false positive, или bypass (если разрешено)

### Правила

| Правило | Описание |
|---------|----------|
| Включить Secret Scanning | Всегда (бесплатно для public, для private требуется GHAS) |
| Включить Push Protection | Всегда (предотвращает утечку) |
| При обнаружении секрета | Немедленно ротировать (отозвать старый, выпустить новый) |
| `.env` файлы | НИКОГДА не коммитить. Использовать `.env.example` без значений |
| Bypass Push Protection | Только с обоснованием (false positive, тестовый токен) |

### Действия при срабатывании

1. **НЕ игнорировать алерт** — даже если секрет "тестовый"
2. **Ротировать секрет** — отозвать скомпрометированный, выпустить новый
3. **Очистить историю** — если секрет в коммитах (git filter-branch или BFG Repo-Cleaner)
4. **Закрыть алерт** — указать причину (revoked, false positive, used in tests)

---

## 6. SECURITY.md

### Назначение

Файл политики безопасности. Описывает, как сообщать об уязвимостях.

**Расположение:** `.github/SECURITY.md`

### Формат

```markdown
# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **DO NOT** create a public GitHub Issue
2. Use [GitHub Private Vulnerability Reporting](https://github.com/{owner}/{repo}/security/advisories/new)
3. Or email: security@example.com

### What to include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response timeline

- **Acknowledgment:** within 48 hours
- **Initial assessment:** within 1 week
- **Fix timeline:** depends on severity

## Security Updates

Security updates are released as patch versions. Subscribe to GitHub Security Advisories for notifications.
```

### Правила

| Правило | Описание |
|---------|----------|
| Файл обязателен | Каждый репозиторий ДОЛЖЕН иметь SECURITY.md |
| Расположение | `.github/SECURITY.md` |
| Язык | Английский (стандарт для open-source и GitHub UI) |
| Контакт | Указать способ связи для responsible disclosure |
| Private reporting | Использовать GitHub Private Vulnerability Reporting (если включено) |

---

## 7. CLI команды

### Dependabot

```bash
# Посмотреть алерты Dependabot
gh api repos/:owner/:repo/dependabot/alerts --jq '.[].security_advisory.summary'

# Закрыть алерт
gh api repos/:owner/:repo/dependabot/alerts/{alert_number} \
  -X PATCH -f state="dismissed" -f dismissed_reason="tolerable_risk"
```

### Code Scanning

```bash
# Посмотреть алерты Code Scanning
gh api repos/:owner/:repo/code-scanning/alerts --jq '.[] | "\(.rule.id): \(.most_recent_instance.location.path)"'

# Закрыть алерт (false positive)
gh api repos/:owner/:repo/code-scanning/alerts/{alert_number} \
  -X PATCH -f state="dismissed" -f dismissed_reason="false positive"
```

### Secret Scanning

```bash
# Посмотреть алерты Secret Scanning
gh api repos/:owner/:repo/secret-scanning/alerts --jq '.[] | "\(.secret_type): \(.state)"'

# Закрыть алерт (секрет отозван)
gh api repos/:owner/:repo/secret-scanning/alerts/{alert_number} \
  -X PATCH -f state="resolved" -f resolution="revoked"
```

### Общий статус безопасности

```bash
# Проверить включённые функции безопасности
gh api repos/:owner/:repo --jq '{
  dependabot_alerts: .security_and_analysis.dependabot_security_updates.status,
  secret_scanning: .security_and_analysis.secret_scanning.status,
  secret_scanning_push_protection: .security_and_analysis.secret_scanning_push_protection.status
}'
```

---

## 8. Не включено в стандарт

| Тема | Причина исключения | Где описано |
|------|-------------------|-------------|
| **GitHub Advanced Security (GHAS) лицензирование** | Вопрос администрирования организации | [GitHub Docs: GHAS](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security) |
| **Custom CodeQL queries** | Требуют глубокой экспертизы, редко нужны для стандартных проектов | [CodeQL Docs](https://codeql.github.com/docs/) |
| **Third-party security tools** | Вне зоны ответственности (Snyk, SonarQube и др.) | Документация инструмента |
| **Security workflow files (.yml)** | Формат workflow файлов — зона `standard-workflow-file.md` | [standard-workflow-file.md](../../workflows-files/standard-workflow-file.md) |
