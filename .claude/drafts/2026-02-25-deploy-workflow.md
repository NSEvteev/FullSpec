# Deploy Workflow — стандарт и шаблон deploy.yml

Определение стандарта деплоя через GitHub Actions: триггер `on: release: published`, шаблон workflow, связь с инфраструктурой.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** `.github/workflows/deploy.yml` не существует. standard-release.md § 11 описывает триггер и шаги деплоя, но файла нет.
**Почему создан:** Без deploy.yml Release не триггерит деплой. validate-post-release.py обходит проверку деплоя через `--skip-deploy`.
**Связанные файлы:**
- `/.github/.instructions/releases/standard-release.md` — § 11 Публикация на production
- `/.github/.instructions/actions/standard-action.md` — стандарт GitHub Actions
- `/.github/workflows/ci.yml` — текущий CI (только pre-commit)
- `/.github/workflows/README.md` — реестр workflows

## Содержание

### Что нужно

1. **Файл `.github/workflows/deploy.yml`** — workflow деплоя
2. **Обновить `.github/workflows/README.md`** — зарегистрировать workflow
3. **Определить инфраструктуру** — Docker Compose (dev) vs Kubernetes (prod) vs SSH

### Шаблон из standard-release.md § 11

```yaml
on:
  release:
    types: [published]
```

Workflow выполняет:
1. Checkout кода на тег релиза
2. Build Docker образов
3. Push образов в Registry
4. Деплой на production сервер
5. Health check

### Зависимости

- Тип инфраструктуры не определён (Docker Compose / K8s / SSH)
- Docker-образы не описаны (нет Dockerfile для сервисов)
- Registry не выбран (Docker Hub / GitHub Container Registry / самохостинг)
- Health check эндпоинты не определены

## Решения

*Нет решений — требуется определить инфраструктуру.*

## Открытые вопросы

- Какой тип деплоя? Docker Compose (простой) / Kubernetes (масштабируемый) / SSH (базовый)?
- Какой container registry использовать?
- Нужен ли staging environment перед production?
- Как организован health check? (HTTP endpoint `/health`?)
- Нужен ли rollback в deploy.yml (automatic rollback on health check failure)?
