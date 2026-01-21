# Runbook Template

> **Источник:** [/.claude/instructions/platform/operations.md](/.claude/instructions/platform/operations.md)

## Шаблон

```markdown
# Runbook: [Alert Name]

## Metadata
- **Alert:** alert_name
- **Severity:** P1 | P2 | P3 | P4
- **Service:** service-name
- **Last Updated:** YYYY-MM-DD

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

### Step 4: Determine pattern
| Паттерн | Вероятная причина |
|---------|-------------------|
| Все эндпоинты | Инфраструктура (DB, Redis) |
| Один эндпоинт | Баг в коде |
| Один под | Проблема с подом |

## Resolution

### Scenario A: [Описание сценария]
```bash
# Шаги решения
```

### Scenario B: [Описание сценария]
```bash
# Шаги решения
```

### Rollback (если нужен)
```bash
kubectl rollout undo deployment/service-name
```

## Escalation
| Условие | Эскалация |
|---------|-----------|
| > 15 минут без прогресса | @team-lead |
| > 30 минут без прогресса | @platform-team |
| P1 > 1 час | @engineering-manager |

## Related Runbooks
- [Related runbook 1](./related-1.md)
- [Related runbook 2](./related-2.md)

## History
| Дата | Изменение |
|------|-----------|
| YYYY-MM-DD | Создан |
```

## Severity Levels

| Severity | Описание | Response SLA | Resolution SLA |
|----------|----------|--------------|----------------|
| P1/Critical | Полный outage | 5 минут | 1 час |
| P2/High | Значительная деградация | 15 минут | 4 часа |
| P3/Medium | Частичная деградация | 1 час | 24 часа |
| P4/Low | Минимальное влияние | 4 часа | 1 неделя |

## Правила

- Runbook должен быть выполним за < 15 минут для P1
- Каждый алерт имеет связанный runbook
- Runbooks хранятся в `/doc/runbooks/`
- Обновлять runbook после каждого инцидента

<!-- Пример заполнения

# Runbook: High Error Rate

## Metadata
- **Alert:** HighErrorRate
- **Severity:** P1
- **Service:** api-server
- **Last Updated:** 2024-01-15

## Description
Error rate превысил порог 5% для сервиса API.
Это означает, что более 5% запросов завершаются с ошибками 5xx.

## Impact
- Пользователи получают ошибки при использовании API
- Деградация функциональности приложения
- Потенциальная потеря транзакций

## Prerequisites
- Доступ к Kubernetes cluster (kubectl configured)
- Доступ к Grafana: https://grafana.example.com
- Доступ к Loki: https://loki.example.com

## Diagnosis

### Step 1: Check current state
```bash
kubectl get pods -l app=api-server
kubectl top pods -l app=api-server
```

### Step 2: Review logs
```bash
kubectl logs -l app=api-server --tail=100 | grep ERROR
kubectl logs -l app=api-server --since=5m | grep -i exception
```

### Step 3: Check metrics
- Dashboard: [API Errors](https://grafana.example.com/d/api-errors)
- Key metrics:
  - `rate(http_requests_total{status=~"5.."}[5m])`
  - `rate(http_requests_total{status=~"2.."}[5m])`

### Step 4: Determine pattern
| Паттерн | Вероятная причина |
|---------|-------------------|
| Все эндпоинты затронуты | Инфраструктура (DB, Redis, Memory) |
| Один эндпоинт затронут | Баг в коде этого эндпоинта |
| Один под затронут | Проблема с конкретным подом |
| После деплоя | Регрессия в новой версии |

## Resolution

### Scenario A: Проблема с подом
```bash
# Перезапустить проблемный под
kubectl delete pod <pod-name>

# Проверить, что новый под поднялся
kubectl get pods -l app=api-server -w
```

### Scenario B: Регрессия после деплоя
```bash
# Откатить деплой
kubectl rollout undo deployment/api-server

# Проверить статус отката
kubectl rollout status deployment/api-server

# Проверить error rate
curl -s https://prometheus.example.com/api/v1/query?query=rate(http_requests_total{status=~"5.."}[5m])
```

### Scenario C: Проблема с БД
```bash
# Проверить подключения к БД
kubectl exec -it <api-pod> -- psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity"

# Если connection pool исчерпан - перезапуск
kubectl rollout restart deployment/api-server
```

## Escalation
| Условие | Эскалация |
|---------|-----------|
| > 15 минут без прогресса | @backend-team в Slack |
| > 30 минут без прогресса | @platform-team |
| P1 > 1 час | @engineering-lead (телефон) |

## Related Runbooks
- [Database Connection Issues](./db-connection.md)
- [High Latency](./high-latency.md)
- [Pod CrashLoop](./pod-crash-loop.md)

## History
| Дата | Изменение |
|------|-----------|
| 2024-01-15 | Создан |
| 2024-01-20 | Добавлен Scenario C для DB issues |
| 2024-02-01 | Обновлены ссылки на dashboards |
-->
