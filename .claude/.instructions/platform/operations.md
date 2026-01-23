---
type: standard
description: Операции — runbooks, incidents, postmortems, on-call
related:
  - platform/deployment.md
  - platform/observability/overview.md
  - platform/observability/alerting.md
---

# Операции

Правила операционной работы: runbooks, управление инцидентами, postmortems.

## Оглавление

- [Правила](#правила)
  - [Runbooks](#runbooks)
  - [Управление инцидентами](#управление-инцидентами)
  - [Severity Levels](#severity-levels)
  - [Incident Response](#incident-response)
  - [Postmortems](#postmortems)
  - [On-Call](#on-call)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Runbooks

> **Шаблон:** [/.claude/templates/platform/runbook-template.md](/.claude/templates/platform/runbook-template.md)

**Правило:** Каждый алерт имеет связанный runbook.

| Компонент runbook | Описание |
|-------------------|----------|
| Описание | Что произошло, почему это важно |
| Диагностика | Шаги для определения причины |
| Решение | Шаги для устранения |
| Эскалация | Когда и кому эскалировать |
| Связанные алерты | Другие алерты этой проблемы |

**Правило:** Runbook должен быть выполним за < 15 минут для P1.

```markdown
# Runbook: High Error Rate

## Описание
Error rate превысил порог 5% для сервиса API.

## Влияние
- Пользователи получают ошибки
- Деградация функциональности

## Диагностика

### 1. Проверить текущий статус
```bash
kubectl get pods -l app=api-server
kubectl logs -l app=api-server --tail=100 | grep ERROR
```

### 2. Проверить метрики
- Grafana: [Dashboard API Errors](https://grafana/d/api-errors)
- Prometheus: `rate(http_requests_total{status=~"5.."}[5m])`

### 3. Определить паттерн
| Паттерн | Вероятная причина |
|---------|-------------------|
| Все эндпоинты | Инфраструктура (DB, Redis) |
| Один эндпоинт | Баг в коде |
| Один под | Проблема с подом |

## Решение

### Если проблема с подом
```bash
kubectl delete pod <pod-name>
```

### Если проблема с деплоем
```bash
kubectl rollout undo deployment/api-server
```

### Если проблема с БД
См. runbook: [Database Connection Issues](./db-connection.md)

## Эскалация
- 15 минут без прогресса → @backend-team
- 30 минут без прогресса → @platform-team
- P1 не решён за 1 час → @engineering-lead
```

**Правило:** Runbooks хранятся в `/platform/runbooks/`.

```
/platform/runbooks/
  README.md             # Индекс всех runbooks
  api/
    high-error-rate.md
    high-latency.md
    pod-crash-loop.md
  database/
    connection-issues.md
    replication-lag.md
  infrastructure/
    kubernetes-node-down.md
    redis-memory-full.md
```

### Управление инцидентами

**Правило:** Инцидент = любое событие, нарушающее SLA.

```
┌─────────────────────────────────────────────────────┐
│              Lifecycle инцидента                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Detection → Triage → Response → Resolution → Review │
│      │          │         │           │          │   │
│      ▼          ▼         ▼           ▼          ▼   │
│  Алерт или   Severity   Работа    Восстано-  Postmortem│
│  сообщение   и роли     по runbook вление            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Правило:** Каждый инцидент имеет Incident Commander (IC).

| Роль | Ответственность |
|------|-----------------|
| Incident Commander | Координация, коммуникация, решения |
| Tech Lead | Техническая диагностика и решение |
| Communications | Обновления для stakeholders |
| Scribe | Документирование timeline |

**Правило:** Все коммуникации в выделенном канале.

```
#incident-2024-01-15-api-outage
├── Pinned: Статус, IC, severity, timeline
├── @incident-commander: координация
├── @tech-lead: техническая работа
└── Bot: автообновления из мониторинга
```

### Severity Levels

**Severity levels:** см. [alerting.md](./observability/alerting.md#severity-levels)

**Правило:** Severity устанавливается при triage и может меняться.

### Incident Response

**Правило:** Следовать структурированному процессу.

```
1. DETECT (0-5 мин)
   - Получить алерт
   - Подтвердить проблему
   - Создать incident channel

2. TRIAGE (5-15 мин)
   - Определить severity
   - Назначить IC
   - Начать runbook

3. RESPOND (ongoing)
   - Выполнять runbook
   - Обновлять статус каждые 15 мин
   - Эскалировать при необходимости

4. RESOLVE
   - Подтвердить восстановление
   - Мониторить стабильность 30 мин
   - Закрыть incident

5. REVIEW (24-48 часов)
   - Провести postmortem
   - Создать action items
   - Обновить runbooks
```

**Правило:** Обновления статуса каждые 15 минут для P1/P2.

```markdown
## Status Update - 14:30 UTC

**Status:** Investigating
**Impact:** 30% пользователей получают 500 ошибки
**Cause:** Расследуем, возможно связано с последним деплоем
**Next Update:** 14:45 UTC
**Actions:**
- Анализируем логи
- Готовим rollback
```

### Postmortems

**Правило:** Postmortem обязателен для P1/P2 в течение 48 часов.

```markdown
# Postmortem: API Outage 2024-01-15

## Метаданные
- **Дата:** 2024-01-15
- **Severity:** P1
- **Duration:** 45 минут (14:00-14:45 UTC)
- **Incident Commander:** @alice
- **Author:** @bob

## Summary
API был недоступен 45 минут из-за исчерпания connection pool к БД после деплоя.

## Impact
- 100% пользователей не могли использовать API
- ~5000 неудачных запросов
- Потенциальная потеря дохода: ~$X

## Timeline (UTC)
| Время | Событие |
|-------|---------|
| 13:45 | Деплой v2.3.4 |
| 14:00 | Алерт: High Error Rate |
| 14:02 | IC назначен, канал создан |
| 14:10 | Причина определена: DB connections exhausted |
| 14:15 | Решение: rollback |
| 14:20 | Rollback запущен |
| 14:35 | Сервис восстановлен |
| 14:45 | Стабильность подтверждена |

## Root Cause
Новая версия содержала утечку соединений к БД. При каждом запросе создавалось новое соединение без освобождения. Connection pool исчерпан через 15 минут.

## Contributing Factors
1. Отсутствие теста на утечку соединений
2. Canary deploy не обнаружил (слишком мало трафика)
3. Мониторинг DB connections не был в dashboard

## What Went Well
- Быстрое обнаружение (< 5 мин)
- Чёткая коммуникация
- Rollback сработал

## What Went Wrong
- Баг прошёл code review
- Canary был неэффективен
- Нет алерта на DB connections

## Action Items
| # | Задача | Владелец | Дедлайн |
|---|--------|----------|---------|
| 1 | Добавить тест на connection leaks | @bob | 2024-01-20 |
| 2 | Добавить метрику db_connections_active | @alice | 2024-01-18 |
| 3 | Увеличить время canary до 30 мин | @ops | 2024-01-17 |
| 4 | Review connection management в коде | @team | 2024-01-22 |

## Lessons Learned
- Connection management критичен
- Canary нужно больше времени для stateful проблем
- Нужен мониторинг ресурсов БД
```

**Правило:** Postmortem = blameless. Фокус на системе, не на людях.

| Blameless | Blame |
|-----------|-------|
| "Тест не покрывал этот случай" | "Разработчик не написал тест" |
| "Review process не обнаружил" | "Reviewer пропустил баг" |
| "Документация была неполной" | "Он не прочитал документацию" |

### On-Call

**Правило:** On-call ротация еженедельная.

```yaml
# PagerDuty / Opsgenie schedule
schedule:
  name: "Backend On-Call"
  rotation:
    type: weekly
    start_day: monday
    handoff_time: "10:00"
  layers:
    - primary:
        members: ["alice", "bob", "charlie", "david"]
    - secondary:
        members: ["eve", "frank"]  # backup
```

**Правило:** On-call engineer должен реагировать в рамках SLA.

| Severity | Response Time | Канал |
|----------|---------------|-------|
| P1 | 5 минут | Phone call + SMS |
| P2 | 15 минут | Push notification |
| P3 | 1 час | Email |
| P4 | Next business day | Email |

**Правило:** Компенсация за on-call.

- Доплата за on-call неделю
- Time-off после ночных инцидентов
- Максимум 1 неделя on-call в месяц

---

## Примеры

### Пример 1: Шаблон runbook

```markdown
# Runbook: [Alert Name]

## Metadata
- **Alert:** alert_name
- **Severity:** P2
- **Service:** service-name
- **Last Updated:** 2024-01-15

## Description
[Что означает этот алерт и почему он важен]

## Impact
- [Влияние на пользователей]
- [Влияние на бизнес]

## Prerequisites
- Доступ к Kubernetes cluster
- Доступ к Grafana/Prometheus
- Доступ к логам (Loki)

## Diagnosis

### Step 1: Check current state
```bash
# Команды для проверки состояния
kubectl get pods -l app=service-name
```

### Step 2: Review logs
```bash
# Команды для просмотра логов
kubectl logs -l app=service-name --tail=100
```

### Step 3: Check metrics
- Dashboard: [Link to Grafana]
- Key metrics:
  - `metric_name{label="value"}`

## Resolution

### Scenario A: [Описание сценария]
```bash
# Шаги решения
```

### Scenario B: [Описание сценария]
```bash
# Шаги решения
```

## Escalation
| Условие | Эскалация |
|---------|-----------|
| > 15 минут без прогресса | @team-lead |
| P1 > 30 минут | @engineering-manager |

## Related Runbooks
- [Related runbook 1](./related-1.md)
- [Related runbook 2](./related-2.md)

## History
| Дата | Изменение |
|------|-----------|
| 2024-01-15 | Создан |
| 2024-01-20 | Добавлен Scenario B |
```

### Пример 2: Incident bot commands

```python
# Slack bot для управления инцидентами
class IncidentBot:
    commands = {
        "/incident new": "Создать новый инцидент",
        "/incident severity P1|P2|P3|P4": "Установить severity",
        "/incident status update <message>": "Обновить статус",
        "/incident assign @user": "Назначить IC",
        "/incident resolve": "Закрыть инцидент",
        "/incident timeline": "Показать timeline",
    }

    async def create_incident(self, title: str, severity: str):
        # 1. Создать канал
        channel = await self.slack.create_channel(
            f"incident-{date.today()}-{slugify(title)}"
        )

        # 2. Пригласить on-call
        oncall = await self.pagerduty.get_oncall("backend")
        await self.slack.invite(channel, oncall)

        # 3. Создать incident record
        incident = await self.db.create_incident(
            title=title,
            severity=severity,
            channel=channel.id,
            created_at=datetime.utcnow()
        )

        # 4. Отправить сообщение
        await self.slack.post(channel, self.format_incident_header(incident))

        return incident
```

### Пример 3: Автоматизация postmortem

```yaml
# .github/workflows/postmortem.yml
name: Create Postmortem

on:
  workflow_dispatch:
    inputs:
      incident_id:
        description: 'Incident ID'
        required: true
      title:
        description: 'Incident title'
        required: true
      severity:
        description: 'Severity (P1/P2/P3/P4)'
        required: true
        type: choice
        options:
          - P1
          - P2
          - P3
          - P4

jobs:
  create-postmortem:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create postmortem from template
        run: |
          DATE=$(date +%Y-%m-%d)
          FILENAME="doc/postmortems/${DATE}-${{ inputs.incident_id }}.md"

          cat > "$FILENAME" << 'EOF'
          # Postmortem: ${{ inputs.title }}

          ## Метаданные
          - **ID:** ${{ inputs.incident_id }}
          - **Дата:** ${DATE}
          - **Severity:** ${{ inputs.severity }}
          - **IC:** @TODO
          - **Author:** @TODO

          ## Summary
          TODO: Краткое описание

          ## Impact
          TODO: Влияние на пользователей

          ## Timeline
          | Время | Событие |
          |-------|---------|
          | | |

          ## Root Cause
          TODO

          ## Action Items
          | # | Задача | Владелец | Дедлайн |
          |---|--------|----------|---------|
          | 1 | | | |

          EOF

      - name: Create PR
        run: |
          git checkout -b postmortem/${{ inputs.incident_id }}
          git add .
          git commit -m "docs: add postmortem for ${{ inputs.incident_id }}"
          gh pr create --title "Postmortem: ${{ inputs.title }}" \
            --body "Postmortem для инцидента ${{ inputs.incident_id }}"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Пример 4: On-call handoff checklist

```markdown
# On-Call Handoff Checklist

## Уходящий on-call (@alice → @bob)

### Перед handoff
- [ ] Все инциденты закрыты или переданы
- [ ] Action items из инцидентов созданы
- [ ] Postmortems написаны для P1/P2

### Во время handoff
- [ ] Передать context по открытым issues
- [ ] Рассказать о нестабильных компонентах
- [ ] Передать доступы (если временные)

### Документ handoff
```markdown
## On-Call Handoff: @alice → @bob
**Дата:** 2024-01-22

### Активные проблемы
- Issue #123: Flaky тесты в CI (низкий приоритет)
- Alert: Redis memory высокая, но стабильная

### Недавние инциденты
- 2024-01-20: API outage (P1), postmortem готов

### На что обратить внимание
- Деплой v2.4.0 запланирован на среду
- Нагрузочное тестирование в четверг

### Контакты
- Backup: @charlie
- Platform: @platform-team
```
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Как определить, нужен ли postmortem?

| Критерий | Postmortem обязателен |
|----------|----------------------|
| Severity P1/P2 | Да |
| Duration > 30 минут | Да |
| Повторяющийся инцидент | Да |
| Потеря данных | Да |
| P3/P4 < 30 минут | Нет (но можно) |

### Что делать, если runbook не помогает?

1. **Эскалировать** — не тратить время впустую
2. **Документировать** — записывать все попытки
3. **Искать паттерны** — проверить похожие инциденты
4. **Привлечь эксперта** — тот, кто писал код
5. **Обновить runbook** — после решения

### Как справиться с alert fatigue?

1. **Audit алертов:**
   ```
   За последний месяц:
   - Сколько алертов сработало?
   - Сколько требовали действий?
   - Сколько были ложными?
   ```

2. **Удалить/объединить:**
   - Алерты с < 10% actionable rate
   - Дублирующие алерты
   - Информационные (перевести в dashboard)

3. **Настроить пороги:**
   - Использовать динамические пороги
   - Учитывать время суток
   - Добавить hysteresis

### Как проводить эффективный postmortem?

1. **Подготовка:**
   - Собрать timeline
   - Пригласить участников
   - Подготовить данные

2. **Встреча (60 минут max):**
   ```
   5 мин: Обзор инцидента
   15 мин: Timeline review
   20 мин: Root cause analysis (5 Whys)
   15 мин: Action items
   5 мин: Wrap-up
   ```

3. **5 Whys пример:**
   ```
   1. Почему API упал? → Connection pool exhausted
   2. Почему exhausted? → Connections не освобождались
   3. Почему не освобождались? → Баг в новом коде
   4. Почему баг прошёл? → Нет теста на connection leak
   5. Почему нет теста? → Не было в checklist

   Root cause: Неполный checklist для code review
   ```

4. **Follow-up:**
   - Создать issues для action items
   - Отслеживать выполнение
   - Закрыть postmortem когда все items done

---

## Связанные инструкции

- [deployment.md](deployment.md) — Деплой и откат
- [observability/overview.md](observability/overview.md) — Мониторинг
- [observability/alerting.md](observability/alerting.md) — Настройка алертов
