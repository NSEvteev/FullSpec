---
description: Стандарт безопасности GitHub — Dependabot, CodeQL, Secret Scanning, security advisories, SECURITY.md.
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/actions/security/README.md
---

# Стандарт безопасности GitHub

Версия стандарта: 1.1

Настройка инструментов безопасности GitHub: Dependabot, Code Scanning (CodeQL), Secret Scanning и политика SECURITY.md.

**Полезные ссылки:**
- [Инструкции security](./README.md)
- [GitHub Security Features (Docs)](https://docs.github.com/en/code-security)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-security.md](./validation-security.md) |
| Создание | *Не планируется* |
| Модификация | *Не планируется* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Файлы и расположение](#2-файлы-и-расположение)
- [3. Dependabot](#3-dependabot)
- [4. Code Scanning (CodeQL)](#4-code-scanning-codeql)
- [5. Secret Scanning](#5-secret-scanning)
- [6. SECURITY.md](#6-securitymd)
- [7. Порядок настройки](#7-порядок-настройки)
- [8. CLI команды](#8-cli-команды)
- [9. Типичные ошибки](#9-типичные-ошибки)
- [10. Не включено в стандарт](#10-не-включено-в-стандарт)

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

**Контекст: template-репозиторий.**

Этот репозиторий — шаблон. При создании нового репозитория из шаблона:
- **Файлы** (`dependabot.yml`, `codeql.yml`, `SECURITY.md`) копируются автоматически
- **Settings** (Dependabot Alerts, Secret Scanning, Push Protection) **НЕ копируются** — настроить для каждого нового репозитория по [initialization.md](/.structure/initialization.md#настройка-github-security)

---

## 2. Файлы и расположение

```
.github/
├── dependabot.yml              # Конфигурация Dependabot
├── SECURITY.md                 # Политика безопасности
└── workflows/
    └── codeql.yml              # Workflow для Code Scanning (Advanced Setup)
```

| Файл | Обязательный | Условие | Описание |
|------|-------------|---------|----------|
| `dependabot.yml` | Да | Всегда | Конфигурация обновлений зависимостей |
| `SECURITY.md` | Да | Всегда | Политика безопасности и контакты |
| `workflows/codeql.yml` | Да | Всегда (Advanced Setup) | Workflow Code Scanning |

---

## 3. Dependabot

### Структура Dependabot

| Функция | Требуется ли dependabot.yml | Как включить |
|---------|----------------------------|--------------|
| **Dependabot Alerts** | Нет (работает без файла) | Settings → Dependabot alerts → Enable |
| **Dependabot Security Updates** | Нет (работает без файла) | Settings → Dependabot security updates → Enable |
| **Dependabot Version Updates** | **Да (файл обязателен)** | Создать `.github/dependabot.yml` |

**Создавать `dependabot.yml` ВСЕГДА** (даже если используются только Alerts), чтобы настроить расписание, группировку обновлений и префиксы коммитов.

### Dependabot Alerts

Автоматические уведомления об уязвимостях в зависимостях.

**Включение:** Settings → Code security and analysis → Dependabot alerts → Enable.

**Поведение:** GitHub сканирует lock-файлы и манифесты зависимостей автоматически:
- При включении Dependabot Alerts — немедленное первое сканирование
- Далее — при каждом push в default branch
- Дополнительно — при обновлении GitHub Advisory Database (несколько раз в день)

Security Alerts создаются при обнаружении CVE в используемых зависимостях.

### Dependabot Security Updates

Автоматические PR для исправления уязвимых зависимостей.

**Включение:** Settings → Code security and analysis → Dependabot security updates → Enable.

**Поведение:** При обнаружении уязвимости Dependabot создаёт PR с обновлением до безопасной версии.

### Dependabot Version Updates

Автоматические PR для поддержания актуальных версий зависимостей.

**Конфигурация:** `.github/dependabot.yml`

#### Пример для монорепо

```yaml
version: 2
updates:
  # Python (pip) — backend сервисы
  - package-ecosystem: "pip"
    directory: "/src/auth"
    schedule:
      interval: "weekly"
      day: "monday"
    groups:
      pip-minor-patch:
        patterns: ["*"]
        update-types: ["minor", "patch"]
    labels:
      - "dependencies"
    commit-message:
      prefix: "deps"

  - package-ecosystem: "pip"
    directory: "/src/api"
    schedule:
      interval: "weekly"
      day: "monday"
    groups:
      pip-minor-patch:
        patterns: ["*"]
        update-types: ["minor", "patch"]
    labels:
      - "dependencies"
    commit-message:
      prefix: "deps"

  # JavaScript/TypeScript (npm) — frontend
  - package-ecosystem: "npm"
    directory: "/src/frontend"
    schedule:
      interval: "weekly"
      day: "monday"
    groups:
      npm-minor-patch:
        patterns: ["*"]
        update-types: ["minor", "patch"]
    labels:
      - "dependencies"
    commit-message:
      prefix: "deps"

  # Docker — платформа
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

**Группировка:** Используйте `groups` для объединения minor/patch обновлений в один PR. Без группировки монорепо с 10+ сервисами создаёт 50+ PR в неделю.

**Параметры конфигурации:**

| Параметр | Обязательный | Описание |
|----------|-------------|----------|
| `package-ecosystem` | Да | Тип менеджера пакетов (`pip`, `npm`, `docker`, `github-actions` и др.) |
| `directory` | Да | Путь к манифесту зависимостей относительно корня |
| `schedule.interval` | Да | Частота проверки (`daily`, `weekly`, `monthly`) |
| `schedule.day` | Нет | День недели для `weekly` |
| `open-pull-requests-limit` | Нет | Макс. открытых PR (по умолчанию 5) |
| `groups` | Нет | Группировка обновлений (minor/patch → один PR) |
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

### Настройка (Advanced Setup)

Во всех проектах используется **Advanced Setup** (кастомный workflow). Default Setup не используется — проекты содержат несколько языков и требуют кастомизации.

> **ВАЖНО:** НЕ включать Default Setup через Settings. Он конфликтует с Advanced Setup (дублирование сканирования, двойной расход CI-минут).

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

permissions:
  security-events: write
  contents: read
  actions: read

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    timeout-minutes: 20

    strategy:
      fail-fast: false
      matrix:
        language: ["python", "javascript-typescript"]
        # Добавить используемые языки: "go", "java", "csharp", "ruby"

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: +security-and-quality  # Расширенный набор запросов

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
| Только Advanced Setup | НЕ включать Default Setup через Settings (конфликт) |
| Триггеры | Push в main, PR в main, еженедельный cron |
| Языки | Указывать ВСЕ используемые в проекте в `matrix.language` |
| `fail-fast: false` | Анализ каждого языка независим |
| `security-events: write` | Обязательное разрешение для записи результатов |
| `queries: +security-and-quality` | Расширенный набор запросов (рекомендуется) |
| Schedule | Еженедельный запуск для обнаружения новых уязвимостей в существующем коде |
| `timeout-minutes` | Указывать явно (рекомендуется 20 мин) |

---

## 5. Secret Scanning

### Назначение

Автоматическое обнаружение секретов (API-ключи, токены, пароли), случайно закоммиченных в репозиторий.

**Включение:** Settings → Code security and analysis → Secret scanning → Enable.

> **Private repos:** Secret Scanning требует лицензию GitHub Advanced Security (GHAS). Если GHAS недоступна — использовать альтернативу (pre-commit hook `detect-secrets`).

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
| Включить Secret Scanning | Всегда (для private repos требуется GHAS) |
| Включить Push Protection | Всегда (предотвращает утечку) |
| `.env` файлы | НИКОГДА не коммитить. Использовать `.env.example` без значений |
| Bypass Push Protection | Только с обоснованием (false positive, тестовый токен) |

### Действия при срабатывании

**Для ЛЮБОГО алерта (даже если кажется false positive):**

1. **Оценить риск:**
   - Это настоящий секрет? (production API key, токен, пароль)
   - Это тестовый/фиктивный секрет? (example.com, placeholder)
   - Это false positive? (строка, похожая на секрет, но не являющаяся им)

2. **Если настоящий секрет:**
   - Ротировать НЕМЕДЛЕННО — процедура ротации в [standard-secrets.md § 5](./standard-secrets.md#5-ротация)
   - Очистить историю Git (если секрет в коммитах) — `git filter-branch` или BFG Repo-Cleaner
   - Закрыть алерт с причиной `revoked`

3. **Если тестовый/false positive:**
   - Закрыть алерт с причиной `false positive` или `used in tests`
   - Добавить комментарий с обоснованием

---

## 6. SECURITY.md

### Назначение

Файл политики безопасности. Описывает, как сообщать об уязвимостях.

**Расположение:** `.github/SECURITY.md`

### Формат (для private/internal проектов)

```markdown
# Security Policy

## Reporting a Vulnerability

**INTERNAL PROJECT — Confidential disclosure only.**

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub Issue
2. **DO NOT** discuss in public channels (Slack, email lists)
3. Email: security@company.internal
4. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response timeline

- **Acknowledgment:** within 24 hours
- **Initial assessment:** within 3 business days
- **Fix timeline:** depends on severity (Critical: 7 days, High: 14 days, Medium: 30 days)

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | Yes       |

## Security Updates

Security updates are released as patch versions.
```

### Правила

| Правило | Описание |
|---------|----------|
| Файл обязателен | Каждый репозиторий ДОЛЖЕН иметь SECURITY.md |
| Расположение | `.github/SECURITY.md` |
| Язык | Английский |
| Контакт | Указать email для confidential disclosure |
| Private reporting | НЕ использовать публичный GitHub Issues |

---

## 7. Порядок настройки

При создании нового репозитория из шаблона файлы (`dependabot.yml`, `codeql.yml`, `SECURITY.md`) уже скопированы. Остаётся настроить Settings.

**Последовательность настройки Settings:**

1. **SECURITY.md** — проверить контактные данные в скопированном файле, обновить email
2. **Dependabot Alerts** — Settings → Enable
3. **Dependabot Security Updates** — Settings → Enable
4. **Secret Scanning** — Settings → Enable
5. **Push Protection** — Settings → Enable
6. **dependabot.yml** — проверить и обновить директории сервисов в скопированном файле
7. **codeql.yml** — проверить и обновить `matrix.language` для используемых языков

> **НЕ включать** Code Scanning → Default Setup в Settings. Используется Advanced Setup через `codeql.yml`.

Подробнее — [initialization.md](/.structure/initialization.md#настройка-github-security).

---

## 8. CLI команды

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

## 9. Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `Dependabot cannot parse manifest` | Некорректный синтаксис package.json, requirements.txt | Проверить файл через JSON/YAML linter |
| `CodeQL: language not supported` | Язык не входит в список поддерживаемых | Убрать язык из `matrix.language` |
| `Secret Scanning: 403 Forbidden` | Private repo без GHAS лицензии | Связаться с администратором организации |
| `Push Protection blocked commit` | Коммит содержит обнаруженный секрет | Удалить секрет из файлов, использовать [GitHub Secrets](./standard-secrets.md) |
| Двойное сканирование CodeQL | Включены И Default Setup, И codeql.yml | Отключить Default Setup в Settings |
| 50+ Dependabot PR в неделю | Нет группировки в dependabot.yml | Добавить `groups` для minor/patch |

---

## 10. Не включено в стандарт

| Тема | Причина исключения | Где описано |
|------|-------------------|-------------|
| **Custom CodeQL queries** | Требуют глубокой экспертизы, используются готовые query suites | [CodeQL Docs](https://codeql.github.com/docs/) |
| **Third-party security tools** | Вне зоны ответственности (Snyk, SonarQube и др.) | Документация инструмента |
| **YAML-синтаксис workflow файлов** | Синтаксис `.yml` описан в отдельном стандарте. Содержимое codeql.yml (конфигурация CodeQL) описано в этом документе (§ 4) | [standard-action.md](../standard-action.md) |
| **Управление секретами** | Именование, уровни хранения, ротация | [standard-secrets.md](./standard-secrets.md) |
