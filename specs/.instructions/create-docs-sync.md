---
description: Воркфлоу синхронизации specs/docs/ — оркестрация service-agent, technology-agent, system-agent с ревью. Вызывается после Plan Dev (все 4 документа в WAITING).
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/README.md
---

# Воркфлоу синхронизации docs/

Рабочая версия стандарта: 1.3

Оркестратор синхронизации specs/docs/ — запускает три пары агентов (service, technology, system) параллельными волнами с ревью и исправлениями.

**Полезные ссылки:**
- [Инструкции specs/](./README.md)

**SSOT-зависимости:**
- [standard-process.md](./standard-process.md) — фазы процесса (§ Docs Sync)
- [create-chain.md](./create-chain.md) — позиция /docs-sync в TaskList
- [chain_status.py](./.scripts/chain_status.py) — check_pending_docs_sync(), docs-synced

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Скилл | [/docs-sync](/.claude/skills/docs-sync/SKILL.md) |

## Оглавление

- [Принципы](#принципы)
- [Вход и выход](#вход-и-выход)
- [Шаги](#шаги)
  - [Шаг 1: Проверить prerequisites](#шаг-1-проверить-prerequisites)
  - [Шаг 2: Определить scope](#шаг-2-определить-scope)
  - [Шаг 3: Волна 1 создание](#шаг-3-волна-1-создание)
  - [Шаг 4: Обновить README](#шаг-4-обновить-readme)
  - [Шаг 5: Волна 2 ревью](#шаг-5-волна-2-ревью)
  - [Шаг 6: Волна 3 исправления](#шаг-6-волна-3-исправления)
  - [Шаг 7: Маркер docs-synced](#шаг-7-маркер-docs-synced)
  - [Шаг 8: Отчёт](#шаг-8-отчёт)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Агенты](#агенты)
- [Скиллы](#скиллы)

---

## Принципы

> **Параллельность.** Все агенты одной волны запускаются параллельно через Task tool.

> **Ревью обязательно.** Каждый агент имеет парный ревьюер. Ревьюер сверяет результат с Design и ЖЁСТКО пресекает расхождения (MISSING/INVENTED/DISTORTED).

> **Антигаллюцинации.** Агенты берут информацию ИСКЛЮЧИТЕЛЬНО из Design, Discussion, Plan Tests и реального кода. ЗАПРЕЩЕНО придумывать.

> **system-agent при /docs-sync обновляет ТОЛЬКО overview.md.** Остальные 3 файла .system/ (conventions, infrastructure, testing) обновляются при DONE (create-chain-done.md).

---

## Вход и выход

**Вход:**
- Все 4 документа analysis chain в WAITING (Discussion, Design, Plan Tests, Plan Dev)
- Путь к design.md

**Выход:**
- Per-service docs: `specs/docs/{svc}.md` — создан или обновлён (§ 9 Planned Changes)
- Per-tech стандарты: `specs/technologies/standard-{tech}.md` — создан или обновлён
- Системная архитектура: `specs/docs/.system/overview.md` — обновлён
- Все артефакты прошли ревью (ACCEPT)
- Маркер `docs-synced: true` в frontmatter design.md

---

## Шаги

### Шаг 1: Проверить prerequisites

1. Извлечь chain-id из пути design.md (например `0001-task-dashboard`)
2. Проверить статусы всех 4 документов:
   ```bash
   python specs/.instructions/.scripts/chain_status.py status {chain-id}
   ```
3. Все 4 документа ОБЯЗАНЫ быть в WAITING
4. **Cross-chain guard:** проверить нет ли pending /docs-sync для предыдущих цепочек:
   ```bash
   python specs/.instructions/.scripts/chain_status.py check-pending-docs-sync {chain-id}
   ```
   Если есть → СТОП: "Завершите /docs-sync для цепочки {M}"

### Шаг 2: Определить scope

1. Прочитать design.md — определить:
   - **Сервисы:** все SVC-N (имя сервиса, kebab-case)
   - **Технологии:** секция "Выбор технологий" — строки со статусом "Выбрано"
2. Для каждого сервиса определить mode:
   - `specs/docs/{svc}.md` существует? → `update`
   - Не существует? → `create`
3. Для каждой технологии определить mode:
   - `specs/technologies/standard-{tech}.md` существует? → `update`
   - Не существует? → `create`
4. **Для каждого нового сервиса** (mode=create):
   - Создать папку кода: `mkdir -p src/{svc}` (если не существует)
   - Создать GitHub label: `gh label create "svc:{svc}" --description "🔷 Сервис {svc}" --color "0ea5e9"` (если не существует)
   - Добавить label в `.github/labels.yml` секцию SVC
   - **Docker scaffolding** (по [standard-docker.md](/platform/.instructions/standard-docker.md)):

     **a) Dockerfile.{svc}** — создать `platform/docker/Dockerfile.{svc}` из шаблона по технологии (Design SVC-N § 3 Tech Stack):

     Python (FastAPI/Flask):
     ```dockerfile
     # === Base ===
     FROM python:3.12-slim AS base
     WORKDIR /app
     RUN addgroup --system app && adduser --system --group app

     # === Development ===
     FROM base AS development
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY . .
     USER app
     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{PORT}", "--reload"]

     # === Production ===
     FROM base AS production
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY . .
     USER app
     CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:{PORT}"]
     ```

     Node.js (Express):
     ```dockerfile
     # === Base ===
     FROM node:20-slim AS base
     WORKDIR /app
     RUN addgroup --system app && adduser --system --group app

     # === Development ===
     FROM base AS development
     COPY package*.json .
     RUN npm ci
     COPY . .
     USER app
     CMD ["npx", "nodemon", "index.js"]

     # === Production ===
     FROM base AS production
     COPY package*.json .
     RUN npm ci --production
     COPY . .
     USER app
     CMD ["node", "index.js"]
     ```

     > `{PORT}` — из [infrastructure.md](/specs/docs/.system/infrastructure.md).

     **b) docker-compose.yml блок** — добавить сервис в `platform/docker/docker-compose.yml`:

     ```yaml
       {svc}:
         build:
           context: ../../src/{svc}
           dockerfile: ../../platform/docker/Dockerfile.{svc}
           target: development
         restart: unless-stopped
         ports:
           - "{PORT}:{PORT}"
         depends_on:
           # из Design SVC-N § 6 Dependencies:
           # postgres → condition: service_healthy
           # redis → condition: service_healthy
           # rabbitmq → condition: service_healthy
           postgres:
             condition: service_healthy
         volumes:
           - ../../src/{svc}:/app
           # Node.js: добавить anonymous volume для node_modules
           # - /app/node_modules
         # healthcheck:
         #   test: ["CMD", "curl", "-f", "http://localhost:{PORT}/health"]
         #   interval: 10s
         #   timeout: 5s
         #   retries: 3
         env_file:
           - .env
         networks:
           - app-network
     ```

     > Health check закомментирован — dev-agent раскомментирует при реализации `/health` endpoint.
     > `depends_on` — генерировать из Design SVC-N § 6 Dependencies (маппинг: PostgreSQL → `postgres`, Redis → `redis`, RabbitMQ → `rabbitmq`, другой сервис → `{svc}`).

     **c) init-db.sql** — если сервис использует PostgreSQL (Design SVC-N § 4 Data Model), добавить в `platform/docker/init-db.sql`:

     ```sql
     CREATE DATABASE myapp_{svc};
     ```

     **d) .env файлы** — добавить per-service переменные:

     В `platform/docker/.env.example`:
     ```bash
     # --- {SVC} Service ---
     {SVC}_DB_NAME=myapp_{svc}                    # если PostgreSQL
     {SVC}_REDIS_DB={next_db_number}              # если Redis
     {SVC}_SERVICE_URL=http://{svc}:{PORT}        # URL для inter-service communication
     ```

     В `platform/docker/.env.test`:
     ```bash
     # --- {SVC} Service (test) ---
     {SVC}_DB_NAME=myapp_{svc}
     {SVC}_REDIS_DB={next_db_number}
     {SVC}_SERVICE_URL=http://localhost:{PORT}
     ```

     **e) .dockerignore** — создать `src/{svc}/.dockerignore` по технологии:

     ```
     # Общие
     .git/
     .env
     tests/

     # Python (если Python)
     __pycache__/
     *.pyc
     .venv/
     .pytest_cache/
     .mypy_cache/

     # Node.js (если Node.js)
     node_modules/
     dist/
     .next/
     ```

     > Docker ищет `.dockerignore` в build context (`src/{svc}/`), не в `platform/docker/`.

### Шаг 3: Волна 1 создание

Запустить ВСЕ агенты параллельно через Task tool (один message с N+M+1 tool calls):

**service-agent × N** (один на сервис):
```
Task tool:
  subagent_type: service-agent
  prompt: |
    service: {svc}
    design-path: {design-path}
    discussion-path: {discussion-path}
    svc-section: SVC-{N}
    mode: {create | update}
    chain-id: {chain-id}
```

**technology-agent × M** (один на технологию):
```
Task tool:
  subagent_type: technology-agent
  prompt: |
    tech: {tech}
    version: {version}
    services: {список сервисов}
    design-id: design-{NNNN}
    mode: {create | update}
```

**system-agent × 1** (mode=sync, ТОЛЬКО overview.md):
```
Task tool:
  subagent_type: system-agent
  prompt: |
    design-path: {design-path}
    mode: sync
```

Дождаться завершения ВСЕХ агентов Волны 1.

### Шаг 4: Обновить README

> **Оркестратор, НЕ агенты** — избежать конфликтов записи.

Если были созданы новые `specs/docs/{svc}.md`:
- Обновить `specs/docs/README.md` — добавить строки для новых сервисов

### Шаг 5: Волна 2 ревью

Запустить ВСЕ ревьюеры параллельно через Task tool:

**service-reviewer × N** (один на сервис):
```
Task tool:
  subagent_type: service-reviewer
  prompt: |
    service: {svc}
    svc-path: specs/docs/{svc}.md
    design-path: {design-path}
    svc-section: SVC-{N}
```

**technology-reviewer × 1** (все per-tech стандарты):
```
Task tool:
  subagent_type: technology-reviewer
  prompt: |
    Проверь per-tech стандарты, созданные/обновлённые в рамках Design {NNNN}.
    design-path: {design-path}
```

**system-reviewer × 1** (mode=sync, ТОЛЬКО overview.md):
```
Task tool:
  subagent_type: system-reviewer
  prompt: |
    design-path: {design-path}
    mode: sync
```

Дождаться завершения ВСЕХ ревьюеров Волны 2.

### Шаг 6: Волна 3 исправления

1. Собрать вердикты всех ревьюеров
2. Если ВСЕ ACCEPT → перейти к Шагу 7
3. Если есть REWORK:
   - Перезапустить ТОЛЬКО агентов с REWORK, передав список расхождений
   - После исправлений — повторный ревью для этих агентов
   - **Максимум 3 итерации** Волны 3
   - После 3-й итерации с REWORK → эскалация пользователю через AskUserQuestion

### Шаг 7: Маркер docs-synced

Записать `docs-synced: true` в frontmatter design.md:

```python
# Добавить поле docs-synced: true в frontmatter
```

Этот маркер проверяется:
- `check_pending_docs_sync()` — cross-chain guard (D-12)
- AUTO_PROPOSE в chain_status.py — двухступенчатый переход к Dev

### Шаг 8: Отчёт

```
## Отчёт /docs-sync

**Цепочка:** {chain-id}
**Design:** {design-path}

### Сервисы (service-agent → service-reviewer)
| Сервис | Mode | Ревью | Итераций |
|--------|------|-------|----------|
| {svc} | create/update | ACCEPT | 1 |

### Технологии (technology-agent → technology-reviewer)
| Технология | Mode | Ревью |
|-----------|------|-------|
| {tech} | create/update | ACCEPT |

### Система (system-agent mode=sync → system-reviewer mode=sync)
| Файл | Обновлён | Ревью |
|------|----------|-------|
| overview.md | Да/Нет | ACCEPT |

### Инфраструктура сервисов
| Сервис | src/ папка | svc: label |
|--------|-----------|------------|
| {svc} | создана/существовала | создан/существовал |

### Docker scaffolding (новые сервисы)
| Сервис | Dockerfile | compose блок | init-db | .env | .dockerignore |
|--------|-----------|-------------|---------|------|---------------|
| {svc} | создан | добавлен | добавлен/N/A | добавлены | создан |

**Маркер:** docs-synced: true записан в design.md

**Следующий шаг:** `/dev-create {chain-id}`
```

---

## Чек-лист

### Prerequisites
- [ ] Все 4 документа в WAITING
- [ ] Cross-chain guard пройден

### Scope (шаг 2)
- [ ] src/{svc}/ папки созданы для новых сервисов
- [ ] svc:{svc} labels созданы на GitHub для новых сервисов
- [ ] labels.yml обновлён (секция SVC)

### Docker scaffolding (шаг 2, для новых сервисов)
- [ ] Dockerfile.{svc} создан в platform/docker/
- [ ] Блок сервиса добавлен в docker-compose.yml (с закомментированным healthcheck)
- [ ] CREATE DATABASE добавлен в init-db.sql (если PostgreSQL)
- [ ] Per-service переменные добавлены в .env.example и .env.test
- [ ] .dockerignore создан в src/{svc}/

### Волна 1
- [ ] service-agent × N запущены параллельно
- [ ] technology-agent × M запущены параллельно
- [ ] system-agent mode=sync запущен
- [ ] Все агенты завершились

### Между волнами
- [ ] specs/docs/README.md обновлён (если новые сервисы)

### Волна 2
- [ ] service-reviewer × N запущены параллельно
- [ ] technology-reviewer × 1 запущен
- [ ] system-reviewer mode=sync запущен
- [ ] Все ревьюеры завершились

### Волна 3 (при REWORK)
- [ ] Агенты с REWORK перезапущены
- [ ] Повторный ревью пройден
- [ ] Итераций ≤ 3

### Завершение
- [ ] docs-synced: true записан в design.md
- [ ] Отчёт выведен

---

## Примеры

### /docs-sync для цепочки с 3 сервисами и 2 технологиями

```bash
# Шаг 1: prerequisites
python specs/.instructions/.scripts/chain_status.py status 0001-task-dashboard
python specs/.instructions/.scripts/chain_status.py check-pending-docs-sync 0001-task-dashboard

# Шаг 2: scope из design.md
# Сервисы: task (create), auth (create), frontend (create)
# Технологии: fastapi (create), react (create)

# Шаг 3: Волна 1 — 3 service-agent + 2 technology-agent + 1 system-agent (параллельно)
# Шаг 4: README — добавить 3 новых сервиса
# Шаг 5: Волна 2 — 3 service-reviewer + 1 technology-reviewer + 1 system-reviewer (параллельно)
# Шаг 6: Волна 3 — при REWORK перезапуск (макс. 3 итерации)

# Шаг 7: маркер
# docs-synced: true → design.md frontmatter

# Шаг 8: отчёт → предложить /dev-create 0001-task-dashboard
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [chain_status.py](./.scripts/chain_status.py) | check_pending_docs_sync(), docs-synced | Этот документ |
| [validate-docs-service.py](./.scripts/validate-docs-service.py) | Валидация {svc}.md (агенты) | [validation-service.md](./docs/service/validation-service.md) |
| [validate-docs-overview.py](./.scripts/validate-docs-overview.py) | Валидация overview.md (агенты) | [validation-overview.md](./docs/overview/validation-overview.md) |

---

## Агенты

| Агент | Роль | Запуск |
|-------|------|--------|
| [service-agent](/.claude/agents/service-agent/AGENT.md) | Создание/обновление {svc}.md | Волна 1 (× N, параллельно) |
| [service-reviewer](/.claude/agents/service-reviewer/AGENT.md) | Сверка {svc}.md с Design SVC-N | Волна 2 (× N, параллельно) |
| [technology-agent](/.claude/agents/technology-agent/AGENT.md) | Создание/обновление per-tech стандартов | Волна 1 (× M, параллельно) |
| [technology-reviewer](/.claude/agents/technology-reviewer/AGENT.md) | Ревью per-tech стандартов | Волна 2 (× 1) |
| [system-agent](/.claude/agents/system-agent/AGENT.md) | Обновление overview.md (mode=sync) | Волна 1 (× 1) |
| [system-reviewer](/.claude/agents/system-reviewer/AGENT.md) | Сверка overview.md с Design (mode=sync) | Волна 2 (× 1) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/docs-sync](/.claude/skills/docs-sync/SKILL.md) | Запуск синхронизации docs/ | Этот документ |
