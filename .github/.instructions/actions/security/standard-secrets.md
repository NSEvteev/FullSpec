---
description: Стандарт управления GitHub Secrets — именование, уровни, ротация, категории
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/actions/security/README.md
---

# Стандарт GitHub Secrets

Версия стандарта: 1.0

Управление секретами в GitHub: именование, уровни хранения, ротация и категоризация.

**Полезные ссылки:**
- [Инструкции security](./README.md)
- [GitHub Docs: Encrypted Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | *Не создано* |
| Создание | *Не создано* |
| Модификация | *Не создано* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Именование](#2-именование)
- [3. Уровни хранения](#3-уровни-хранения)
- [4. Категории секретов](#4-категории-секретов)
- [5. Ротация](#5-ротация)
- [6. Доступ и права](#6-доступ-и-права)
- [7. CLI команды](#7-cli-команды)
- [8. Не включено в стандарт](#8-не-включено-в-стандарт)

---

## 1. Назначение

Стандарт описывает **управление** GitHub Secrets: как называть, где хранить, когда ротировать.

**Что покрывает:**

| Аспект | Описание |
|--------|----------|
| **Именование** | Конвенция имён для единообразия |
| **Уровни** | Repository, Environment, Organization — когда какой |
| **Категории** | Типы секретов и их особенности |
| **Ротация** | Периодичность обновления |
| **Доступ** | Кто может управлять секретами |

**Что НЕ покрывает (другие зоны):**

| Тема | Где описано |
|------|-------------|
| Использование секретов в workflows (`${{ secrets.X }}`) | [standard-action.md § 7](../standard-action.md#7-secrets-и-variables) |
| Обнаружение утёкших секретов (Secret Scanning) | [standard-security.md § 5](./standard-security.md#5-secret-scanning) |
| Локальные `.env` файлы | [standard-security.md § 5](./standard-security.md#5-secret-scanning) |

---

## 2. Именование

### Формат

```
{КАТЕГОРИЯ}_{СЕРВИС}_{НАЗНАЧЕНИЕ}
```

| Часть | Описание | Примеры |
|-------|----------|---------|
| `КАТЕГОРИЯ` | Тип секрета (см. [§ 4](#4-категории-секретов)) | `DB`, `API`, `DEPLOY`, `NOTIFY` |
| `СЕРВИС` | Сервис или провайдер | `POSTGRES`, `STRIPE`, `AWS`, `SLACK` |
| `НАЗНАЧЕНИЕ` | Конкретная роль | `URL`, `TOKEN`, `KEY`, `PASSWORD` |

### Правила

| Правило | Описание |
|---------|----------|
| Регистр | UPPER_SNAKE_CASE |
| Разделитель | Только `_` (underscore) |
| Длина | Максимум 48 символов |
| Язык | Английский |
| Префикс среды | НЕ добавлять (`PROD_`, `DEV_`) — использовать Environment Secrets |

### Примеры

| Секрет | Категория | Описание |
|--------|-----------|----------|
| `DB_POSTGRES_URL` | Database | Connection string |
| `DB_POSTGRES_PASSWORD` | Database | Пароль базы данных |
| `API_STRIPE_SECRET_KEY` | API | Stripe API key |
| `API_OPENAI_TOKEN` | API | OpenAI API token |
| `DEPLOY_AWS_ACCESS_KEY_ID` | Deploy | AWS credentials |
| `DEPLOY_AWS_SECRET_ACCESS_KEY` | Deploy | AWS credentials |
| `NOTIFY_SLACK_WEBHOOK` | Notification | Slack webhook URL |
| `REGISTRY_DOCKER_TOKEN` | Registry | Docker Hub token |

---

## 3. Уровни хранения

GitHub предоставляет три уровня хранения секретов. Каждый уровень имеет свою область видимости.

### Сравнение уровней

| Уровень | Область видимости | Когда использовать |
|---------|------------------|--------------------|
| **Repository** | Один репозиторий | Секреты, уникальные для проекта |
| **Environment** | Один репозиторий + конкретная среда | Разные значения для dev/staging/prod |
| **Organization** | Все (или выбранные) репозитории организации | Общие секреты (Docker Hub, npm, Slack) |

### Repository Secrets

```bash
# Создание
gh secret set DB_POSTGRES_URL --body "postgresql://user:pass@host:5432/db"

# Просмотр списка
gh secret list
```

Доступны во всех workflows репозитория. Подходят для большинства случаев.

### Environment Secrets

```bash
# Создание для среды "production"
gh secret set DB_POSTGRES_URL --env production --body "postgresql://prod-host/db"

# Создание для среды "staging"
gh secret set DB_POSTGRES_URL --env staging --body "postgresql://staging-host/db"
```

**Одно имя — разные значения** для каждой среды. Workflow указывает среду:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # ← выбор среды
    steps:
      - run: echo "DB=${{ secrets.DB_POSTGRES_URL }}"
      # Получит значение из environment "production"
```

**Правила Protection Rules** (настраиваются в Settings → Environments):

| Правило | Описание |
|---------|----------|
| Required reviewers | Ручное подтверждение перед деплоем |
| Wait timer | Задержка перед запуском (минуты) |
| Deployment branches | Только определённые ветки (например, `main`) |

### Organization Secrets

```bash
# Для всех репозиториев организации
gh secret set --org {org} REGISTRY_DOCKER_TOKEN --visibility all --body "..."

# Для выбранных репозиториев
gh secret set --org {org} REGISTRY_DOCKER_TOKEN --visibility selected \
  --repos "repo1,repo2" --body "..."
```

| Visibility | Описание |
|-----------|----------|
| `all` | Все репозитории организации |
| `private` | Только private-репозитории |
| `selected` | Конкретный список репозиториев |

---

## 4. Категории секретов

| Категория | Префикс | Примеры | Ротация |
|-----------|---------|---------|---------|
| **Database** | `DB_` | Connection strings, passwords | 90 дней |
| **API** | `API_` | Ключи внешних сервисов | По требованию провайдера |
| **Deploy** | `DEPLOY_` | Cloud credentials (AWS, GCP) | 90 дней |
| **Registry** | `REGISTRY_` | Docker Hub, npm, PyPI tokens | 180 дней |
| **Notification** | `NOTIFY_` | Slack, email webhooks | При смене интеграции |
| **Signing** | `SIGN_` | GPG, code signing keys | 365 дней |
| **Auth** | `AUTH_` | OAuth secrets, JWT signing keys | 90 дней |

---

## 5. Ротация

### Периодичность

| Приоритет | Периодичность | Категории |
|-----------|---------------|-----------|
| Высокий | 90 дней | DB, Deploy, Auth |
| Средний | 180 дней | Registry, API |
| Низкий | 365 дней | Signing, Notify |

### Процедура ротации

1. **Создать новый секрет** в провайдере (новый ключ/пароль)
2. **Обновить секрет в GitHub** (`gh secret set ...`)
3. **Проверить** — запустить workflow с новым секретом
4. **Отозвать старый** секрет в провайдере
5. **Документировать** дату ротации

### При утечке секрета

1. **Немедленно** отозвать секрет в провайдере
2. Создать новый секрет
3. Обновить в GitHub
4. Проверить логи доступа в провайдере
5. См. [standard-security.md § 5](./standard-security.md#5-secret-scanning)

---

## 6. Доступ и права

### Кто может управлять секретами

| Уровень | Кто имеет доступ |
|---------|------------------|
| Repository | Repository Admin, Owner |
| Environment | Repository Admin, Owner |
| Organization | Organization Owner, Admin |

### Правила доступа

| Правило | Описание |
|---------|----------|
| Минимум привилегий | Давать доступ только тем workflows, которым секрет нужен |
| Environment Protection | Для production — включить Required Reviewers |
| Fork-репозитории | Секреты НЕ передаются в fork (по умолчанию) |
| Pull Request из fork | Секреты НЕ доступны в `pull_request` из fork |

---

## 7. CLI команды

### Управление секретами

```bash
# Список секретов репозитория
gh secret list

# Создать/обновить секрет
gh secret set {NAME} --body "{value}"

# Создать секрет из файла
gh secret set {NAME} < path/to/file.txt

# Создать секрет для среды
gh secret set {NAME} --env {environment} --body "{value}"

# Удалить секрет
gh secret delete {NAME}
```

### Управление variables (для справки)

```bash
# Список переменных
gh variable list

# Создать/обновить переменную
gh variable set {NAME} --body "{value}"

# Удалить переменную
gh variable delete {NAME}
```

---

## 8. Не включено в стандарт

| Тема | Причина исключения | Где описано |
|------|-------------------|-------------|
| Синтаксис `${{ secrets.X }}` | Зона standard-action.md | [standard-action.md § 7](../standard-action.md#7-secrets-и-variables) |
| Secret Scanning / Push Protection | Зона standard-security.md | [standard-security.md § 5](./standard-security.md#5-secret-scanning) |
| `.env` файлы и `.env.example` | Зона standard-security.md | [standard-security.md § 5](./standard-security.md#5-secret-scanning) |
| HashiCorp Vault / AWS Secrets Manager | External tools, вне GitHub Secrets | Документация инструмента |
