# Post-release workflow — оценка и план

Мониторинг и действия после публикации Release на production.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G8 из standard-process.md — нет post-release workflow
**Почему создан:** Определить что входит в post-release и когда реализовать
**Связанные файлы:**
- `/.github/.instructions/releases/standard-release.md` — § 11 Публикация на production
- `/.github/.instructions/releases/validation-release.md` — post-release валидация
- `specs/.instructions/standard-process.md` — §5 Фаза 6

## Содержание

### Что уже покрыто

- `standard-release.md § 11` — post-deploy verification: health check, smoke tests, мониторинг
- `validation-release.md` — post-release валидация (скрипт `validate-post-release.py`)
- `create-release.md` Шаг 7 — post-release валидация

### Что НЕ покрыто

| Функция | Описание | Зависит от |
|---------|----------|-----------|
| Health check | `curl /health` → проверка статуса | Инфраструктура (URL, формат ответа) |
| Smoke tests | Автоматические базовые сценарии | Тесты (e2e) |
| Мониторинг | Error rate за 15 мин после деплоя | Мониторинг (Grafana, Datadog, etc.) |
| Уведомления | Slack/Discord/Email о новом релизе | Интеграции |
| CHANGELOG.md sync | Синхронизация после Release | Уже описано в create-release.md Шаг 6 |

### Артефакты

| # | Артефакт | Путь | Статус |
|---|---------|------|--------|
| 1 | **Инструкция** (SSOT) | `/.github/.instructions/releases/create-post-release.md` | **Нужно создать** (когда инфраструктура будет) |
| 2 | **Скилл** (обёртка) | `/.claude/skills/post-release/SKILL.md` | **Нужно создать** |

### Почему отложено

Post-release зависит от инфраструктуры проекта (URL сервисов, мониторинг, CI/CD pipeline). В template-проекте эти вещи ещё не определены. Реализовать при первом реальном деплое.

## Решения

- Приоритет низкий — зависит от инфраструктуры
- Частично покрыто `validate-post-release.py`
- Реализовать при первом реальном деплое

## Открытые вопросы

- Какой формат health check endpoint будет использоваться?
- Какая система мониторинга будет?
- Нужны ли автоматические smoke tests в CI/CD или ручные?

---

## Что уже описано в проекте

### standard-release.md -- 11 Публикация на production

- **Триггер деплоя:** GitHub Actions workflow `deploy.yml` запускается по событию `on: release: types: [published]`. Workflow выполняет: checkout на тег, build Docker, push в Registry, деплой на production, health check.
- **Post-deploy verification** (таблица из 3 проверок):
  1. Health check: `curl https://example.com/health` -- ожидается `{"status": "ok"}`
  2. Smoke tests: основные сценарии (ручные или авто) -- критичные пути работают
  3. Мониторинг: error rate за 15 мин после деплоя -- не вырос
- **Если health check провалился:** проверить логи, если критично -- rollback (13), если не критично -- hotfix (12)
- **Таблица ошибок деплоя:** ошибка кода (hotfix), ошибка инфраструктуры (исправить + retry `gh workflow run deploy.yml --ref vX.Y.Z`), таймаут (проверить сервер + retry)
- **Просмотр запусков:** `gh run list --workflow=deploy.yml`, `gh run view {id}`, `gh run view {id} --log`

### validation-release.md -- Шаг 6: Проверить деплой (post-release)

- Автоматическая проверка через `validate-post-release.py --version vX.Y.Z`
- Проверяет статус workflow `deploy.yml` (completed+success / completed+failure / in_progress / нет запусков)
- Post-deploy verification: health check, smoke tests, error rate (15 мин) -- те же 3 пункта что в standard-release.md
- Критерий: деплой завершён успешно, health check пройден

### validate-post-release.py -- Скрипт post-release валидации

- 5 групп проверок: объект Release, Git-тег, Release Notes, CHANGELOG.md, деплой
- 15 кодов ошибок (E001-E015): от "Release не найден" до "Деплой не запущен"
- Проверяет: tag SemVer, title формат, body не пустой, не draft, target=main, Milestone ссылка, changelog наличие, placeholder-тексты, CHANGELOG.md формат, deploy.yml статус
- Флаги: `--skip-deploy` (пропустить проверку деплоя), `--json` (вывод JSON)
- **НЕ проверяет:** реальный health check сервисов, smoke tests, error rate, уведомления -- это за пределами скрипта

### create-release.md -- Шаг 7: Post-release валидация

- Вызов `validate-post-release.py --version $VERSION`
- Таблица исправлений: Release Notes без Milestone -- `gh release edit`, CHANGELOG.md не обновлен -- обновить и закоммитить, деплой провалился -- см. standard-release.md 11
- Снятие Release Freeze после валидации

### standard-process.md -- Фаза 6: Поставка

- Шаг 6.1: Release -- Milestone complete, changelog, tag, GitHub Release
- Инструменты: standard-release + create-release + validation-release, скилл `/milestone-validate`, скрипты validate-pre-release.py + validate-post-release.py
- G8 зафиксирован как пробел: "Нет post-release workflow -- Низкий приоритет -- Мониторинг зависит от инфраструктуры"

### standard-action.md -- Deploy workflow паттерн

- Рекомендуемый триггер для deploy: `on: release: types: [published]`
- Разделение CI и CD: `ci.yml` (тесты, линтинг) и `deploy.yml` (деплой) -- не смешивать
- Environments: `production` environment с required reviewers, своими секретами и deployment history
- Concurrency: `cancel-in-progress: false` для deploy (не отменять deploy посередине)
- Координация через `workflow_run`: deploy после успешного CI
- Уведомления при ошибке: `if: failure()` + curl к Slack webhook

### platform/ -- Инфраструктурная заготовка

- `platform/monitoring/` -- структура готова:
  - `prometheus/` -- метрики и алерты (prometheus.yml, alerts.yml, rules/)
  - `grafana/` -- дашборды (dashboards/*.json, provisioning/)
  - `loki/` -- логи (loki-config.yml, promtail.yml)
- `platform/k8s/` -- Kubernetes манифесты (deployments, services, ingress, secrets)
- `platform/scripts/` -- инфра-скрипты (deploy.sh, backup.sh, restore.sh)
- `platform/runbooks/` -- директория существует, но пуста (нет ни одного runbook)
- `platform/docker/` -- только .gitkeep, конфигов нет
- `platform/gateway/` -- только .gitkeep, конфигов нет
- **Реальный контент:** все подпапки содержат только .gitkeep и README -- конфигураций нет

### config/feature-flags/ -- Feature flags заготовка

- Директория существует, README описывает: `flags.yaml`, rollout rules -- но файлов нет
- Связь с post-release: feature flags позволяют safe rollouts и быстрый rollback без redeploy

### .github/workflows/ -- Текущее состояние CI/CD

- Существует `ci.yml` -- pre-commit checks при push в main и PR (Python 3.12, pre-commit run --all-files)
- `deploy.yml` -- **НЕ существует** (упоминается в стандартах как будущий)
- Нет workflow для post-deploy verification, smoke tests, уведомлений

### 2026-02-24-tests-and-platform.md -- Связанный драфт

- Smoke тесты: `tests/smoke/` -- "После deploy, НЕТ (связано с G8 post-release)"
- `standard-runbooks.md` -- формат runbook, шаблон инцидента, escalation -- приоритет низкий, "нужен при первом инциденте"
- `standard-monitoring.md` -- формат дашбордов, алерты, метрики -- приоритет низкий, "нужен при настройке мониторинга"
- `standard-scripts.md` -- формат инфра-скриптов (деплой, бэкап, rollback) -- приоритет средний, "нужен при первом деплое"

---

## Best practices

### Post-deployment verification -- многоуровневая стратегия

**Уровень 0: Инфраструктурная проверка (0-1 мин после деплоя)**
- Проверка что контейнеры/поды запустились: `docker ps`, `kubectl get pods -w`
- Readiness probe пройден (K8s автоматически не направляет трафик до ready)
- Нет CrashLoopBackOff, OOMKilled, ImagePullBackOff

**Уровень 1: Health check (1-2 мин)**
- Стандартный endpoint `/health` или `/healthz` возвращает 200 + JSON `{"status":"ok"}`
- Расширенный health check (`/health/ready`) проверяет зависимости: БД, кэш, очереди, внешние API
- Паттерн: shallow health (процесс жив) vs deep health (все зависимости доступны)
- Health check должен быть idempotent, быстрым (<500ms), не требовать аутентификации

**Уровень 2: Smoke tests (2-5 мин)**
- Минимальный набор end-to-end сценариев на production: авторизация, основной CRUD, критичный бизнес-путь
- Smoke != полный e2e -- только "система не сломана" (5-15 тестов, не 500)
- Должны использовать тестовые данные или sandbox, чтобы не загрязнять production
- Запуск: отдельный CI job после deploy, или скрипт `make smoke-test ENVIRONMENT=production`

**Уровень 3: Мониторинг error rate (5-15 мин)**
- Сравнение error rate до и после деплоя (baseline vs current)
- Пороги: >1% ошибок на критичных эндпоинтах -- alert, >5% -- auto-rollback
- Latency p50/p95/p99 не деградировала более чем на 20%
- Нет новых типов ошибок в логах (новые stack traces, неизвестные exception types)

### Canary deployments и progressive rollouts

**Canary deployment:**
- Направить 1-5% трафика на новую версию, остальные 95-99% на старую
- Мониторить error rate и latency canary vs baseline в течение 10-30 мин
- Если метрики ОК -- постепенно увеличить до 25%, 50%, 100%
- Если метрики деградируют -- автоматический rollback canary
- Инструменты: Kubernetes (Argo Rollouts, Flagger), Istio service mesh, AWS ALB weighted target groups

**Blue-green deployment:**
- Две идентичные среды: blue (текущая) и green (новая)
- Деплой на green, smoke tests, переключение трафика (DNS, load balancer)
- Мгновенный rollback -- переключение обратно на blue
- Проще canary, но требует двойных ресурсов

**Rolling update (K8s default):**
- Постепенная замена старых подов новыми (maxUnavailable, maxSurge)
- Rollback: `kubectl rollout undo deployment/{name}`
- Проще в настройке, но нет сравнения метрик canary vs baseline

### Observability -- три столпа

**1. Metrics (Prometheus + Grafana)**
- RED metrics для сервисов: Rate (запросы/сек), Errors (% ошибок), Duration (latency)
- USE metrics для инфраструктуры: Utilization, Saturation, Errors (CPU, RAM, disk, network)
- Custom business metrics: регистрации/мин, заказы/час, конверсия
- Дашборд post-release: side-by-side сравнение метрик "до" и "после" деплоя
- Алерты: Prometheus alertmanager rules, severity: critical/warning/info

**2. Logs (Loki + Promtail)**
- Структурированные логи (JSON): timestamp, level, service, trace_id, message
- Log aggregation: собирать логи всех сервисов в одном месте
- Post-release: фильтр по временному окну "после деплоя", поиск новых ERROR/FATAL
- Корреляция: trace_id позволяет проследить запрос через все сервисы

**3. Traces (OpenTelemetry / Jaeger / Zipkin)**
- Distributed tracing: визуализация пути запроса через микросервисы
- Post-release: сравнение latency spans до и после деплоя
- Обнаружение bottlenecks: какой сервис добавил задержку после обновления
- Sampling: в production обычно 1-10% запросов (не 100%, чтобы не перегружать)

### SLO/SLI мониторинг после релиза

**SLI (Service Level Indicators)** -- конкретные метрики:
- Availability: % успешных запросов (200-399) от общего числа
- Latency: p50, p95, p99 время ответа
- Error rate: % запросов с ошибками (5xx)
- Throughput: запросов/сек

**SLO (Service Level Objectives)** -- целевые значения SLI:
- Availability >= 99.9% (допустимый downtime: ~8.7 часов/год)
- Latency p99 < 500ms для API
- Error rate < 0.1% для критичных эндпоинтов

**Error budget:**
- Если SLO availability = 99.9%, error budget = 0.1% (43.2 мин/мес)
- Post-release: если деплой "съел" значительную часть error budget -- freeze на новые деплои до стабилизации
- Burn rate alert: если error budget расходуется быстрее нормы -- немедленная реакция

### Incident response и rollback procedures

**Incident severity levels:**
- **SEV1 (Critical):** Сервис полностью недоступен, потеря данных. Реакция: немедленно, rollback в течение 5 мин
- **SEV2 (High):** Основная функциональность деградирована. Реакция: 15 мин, hotfix или rollback
- **SEV3 (Medium):** Второстепенная функциональность сломана. Реакция: 1 час, hotfix
- **SEV4 (Low):** Косметические баги, minor degradation. Реакция: следующий рабочий день

**Runbook для post-release инцидента:**
1. Detect: алерт от мониторинга или пользователь сообщил
2. Assess: определить severity, затронутые компоненты, количество пользователей
3. Decide: rollback (SEV1-2) или hotfix (SEV3-4), см. standard-release.md 12-13 (30 мин SLA для hotfix)
4. Act: выполнить rollback/hotfix по процедуре
5. Verify: health check + smoke tests после действия
6. Communicate: уведомить команду и стейкхолдеров
7. Postmortem: разбор причин (для SEV1-2 обязательно)

**Rollback стратегии (от быстрых к медленным):**
- Feature flag off: мгновенный (~секунды), если фича за флагом
- Revert canary: перенаправить трафик обратно (~секунды-минуты)
- K8s rollout undo: `kubectl rollout undo` (~минуты)
- Redeploy previous version: `gh workflow run deploy.yml --ref vPREVIOUS` (~минуты)
- Revert commit + new release: полный цикл из standard-release.md 13 (~10-30 мин)

### Feature flags для safe rollouts

**Зачем feature flags при post-release:**
- Деплой кода != включение фичи -- код деплоится выключенным, включается постепенно
- Мгновенный rollback: выключить флаг, не нужен redeploy
- Постепенный rollout: 1% -> 10% -> 50% -> 100% пользователей
- A/B тестирование: метрики фичи на подмножестве пользователей

**Типы флагов:**
- Release flags: вкл/выкл новой фичи (убрать после полного rollout)
- Ops flags: kill switch для нагруженных фич (оставить навсегда)
- Experiment flags: A/B тесты (убрать после эксперимента)

**Процесс safe rollout с флагами:**
1. Deploy: код с feature flag (выключен по умолчанию)
2. Verify deploy: health check, smoke tests -- без новой фичи
3. Enable 1%: включить флаг для 1% пользователей
4. Monitor 15-30 мин: error rate, latency для группы с флагом
5. Ramp up: 10% -> 50% -> 100% с мониторингом на каждом шаге
6. Cleanup: убрать флаг из кода в следующем релизе

**Связь с проектом:** `config/feature-flags/` уже заложена в структуре (flags.yaml, rollout rules), но пуста

### Post-release уведомления

**Кому и когда:**
- Команда (Slack/Discord): автоматически при создании Release (GitHub webhook или Actions step)
- Стейкхолдеры: автоматически -- summary из Release Notes
- Пользователи: CHANGELOG.md или release page -- опционально, вручную

**GitHub Actions step для уведомлений:**
```yaml
- name: Notify team
  if: success()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -H 'Content-Type: application/json' \
      -d '{"text":"Release ${{ github.event.release.tag_name }} deployed successfully"}'

- name: Notify on failure
  if: failure()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -H 'Content-Type: application/json' \
      -d '{"text":"ALERT: Deploy ${{ github.event.release.tag_name }} FAILED"}'
```

### Post-release checklist (рекомендуемый порядок)

| # | Проверка | Время | Автоматизация | Кто |
|---|----------|-------|---------------|-----|
| 1 | deploy.yml завершён успешно | 0-5 мин | `gh run list --workflow=deploy.yml` | CI/CD |
| 2 | Контейнеры/поды запущены | 0-2 мин | K8s readiness probe / `docker ps` | Инфра |
| 3 | Health check `/health` | 1-2 мин | `curl /health` | Скрипт |
| 4 | Deep health `/health/ready` | 1-2 мин | `curl /health/ready` | Скрипт |
| 5 | Smoke tests | 2-5 мин | `make smoke-test` или CI job | Скрипт |
| 6 | Error rate baseline comparison | 5-15 мин | Grafana dashboard / Prometheus alert | Мониторинг |
| 7 | Latency p95/p99 check | 5-15 мин | Grafana dashboard | Мониторинг |
| 8 | Логи: нет новых ERROR/FATAL | 5-15 мин | Loki query | Мониторинг |
| 9 | validate-post-release.py | 1 мин | Скрипт уже есть | CI |
| 10 | Release Freeze снят | -- | Ручное | Человек |
| 11 | Команда уведомлена | -- | Slack webhook | CI/CD |
| 12 | CHANGELOG.md синхронизирован | -- | create-release.md Шаг 6 | Ручное/скрипт |

### Что реализовать первым (при наличии инфраструктуры)

| Приоритет | Что | Почему | Зависимость |
|-----------|-----|--------|-------------|
| P0 | `deploy.yml` workflow | Без него деплой ручной | Инфраструктура (Docker Registry, сервер) |
| P0 | Health check endpoint `/health` | Минимальная проверка "сервис жив" | Код сервисов |
| P1 | Smoke tests (`tests/smoke/`) | Проверка критичных путей | Тесты + инфраструктура |
| P1 | Slack/Discord уведомления | Команда знает о деплое | Webhook URL |
| P2 | Prometheus + Grafana дашборд | Error rate / latency мониторинг | platform/monitoring/ конфиги |
| P2 | Loki log aggregation | Поиск ошибок после деплоя | platform/monitoring/loki/ конфиги |
| P3 | Alertmanager rules | Автоматические алерты при деградации | Prometheus |
| P3 | Feature flags integration | Safe rollouts | config/feature-flags/ |
| P4 | Canary deployment | Постепенный rollout | K8s + service mesh |
| P4 | Runbooks | Операционные процедуры | platform/runbooks/ |
