---
type: standard
description: Алертинг — severity levels, routing, связь с runbooks, уведомления
related:
  - platform/observability/overview.md
  - platform/observability/metrics.md
  - platform/operations.md
---

# Алертинг

Правила алертинга: severity levels, маршрутизация, runbooks, noise reduction.

## Оглавление

- [Правила](#правила)
  - [Severity Levels](#severity-levels)
  - [Alert Design](#alert-design)
  - [Routing и Escalation](#routing-и-escalation)
  - [Связь с Runbooks](#связь-с-runbooks)
  - [Noise Reduction](#noise-reduction)
  - [Alertmanager конфигурация](#alertmanager-конфигурация)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

> **Шаблон:** [/.claude/templates/platform/prometheus-rules.template](/.claude/templates/platform/prometheus-rules.template)

### Severity Levels

**Правило:** Чёткая классификация severity.

| Severity | Описание | Response Time | Канал | Пример |
|----------|----------|---------------|-------|--------|
| `critical` | Полный outage, потеря данных | 5 минут | Phone + SMS | Сайт недоступен |
| `high` | Значительная деградация | 15 минут | Slack + Push | Error rate > 10% |
| `warning` | Потенциальная проблема | 1 час | Slack | Disk usage > 80% |
| `info` | Информация | — | Dashboard | Deploy completed |

**Правило:** Severity определяет автоматически, не вручную.

```yaml
# prometheus-rules.yml
groups:
  - name: api-alerts
    rules:
      # Critical: полный outage
      - alert: APIDown
        expr: up{job="api-server"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "API server is down"
          runbook: "https://runbooks.example.com/api-down"

      # High: высокий error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.10
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "Error rate > 10%"
          runbook: "https://runbooks.example.com/high-error-rate"

      # Warning: повышенный error rate
      - alert: ElevatedErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.05
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Error rate > 5%"
```

### Alert Design

**Правило:** Alert должен быть actionable — требовать конкретного действия.

| Хороший alert | Плохой alert |
|---------------|--------------|
| "Error rate > 5%, требуется диагностика" | "Были ошибки" |
| "Disk usage > 80%, очистить логи" | "Disk usage изменился" |
| "Pod CrashLoopBackOff, проверить логи" | "Pod перезапустился" |

**Правило:** Структура alert rule.

```yaml
- alert: AlertName                    # PascalCase
  expr: metric_query > threshold      # Условие
  for: 5m                             # Сколько должно держаться
  labels:
    severity: high                    # Severity
    service: api-server               # Сервис
    team: backend                     # Команда-владелец
  annotations:
    summary: "Краткое описание"       # 1 строка
    description: "Детальное описание" # Подробности
    runbook: "URL runbook"            # Ссылка на runbook
    dashboard: "URL dashboard"        # Ссылка на dashboard
```

**Правило:** `for` duration предотвращает flapping.

| Ситуация | `for` duration |
|----------|----------------|
| Мгновенная проблема (down) | 1m |
| Метрика колеблется | 5-10m |
| Тренд (disk usage) | 15-30m |

**Правило:** Использовать absent() для пропавших метрик.

```yaml
- alert: MetricMissing
  expr: absent(up{job="api-server"})
  for: 5m
  labels:
    severity: high
  annotations:
    summary: "API server metrics missing"
```

### Routing и Escalation

**Правило:** Routing по severity и команде.

```yaml
# alertmanager.yml
route:
  receiver: 'default'
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    # Critical → все каналы
    - match:
        severity: critical
      receiver: 'critical-pagerduty'
      continue: true

    - match:
        severity: critical
      receiver: 'critical-slack'

    # High → Slack + on-call
    - match:
        severity: high
      receiver: 'high-slack'
      routes:
        - match:
            team: backend
          receiver: 'backend-oncall'
        - match:
            team: platform
          receiver: 'platform-oncall'

    # Warning → только Slack
    - match:
        severity: warning
      receiver: 'warning-slack'

receivers:
  - name: 'critical-pagerduty'
    pagerduty_configs:
      - service_key: 'xxx'
        severity: critical

  - name: 'critical-slack'
    slack_configs:
      - channel: '#incidents'
        title: ':rotating_light: CRITICAL: {{ .GroupLabels.alertname }}'

  - name: 'high-slack'
    slack_configs:
      - channel: '#alerts-high'
        title: ':warning: HIGH: {{ .GroupLabels.alertname }}'

  - name: 'warning-slack'
    slack_configs:
      - channel: '#alerts-warning'
        title: ':information_source: WARNING: {{ .GroupLabels.alertname }}'
```

**Правило:** Escalation при отсутствии реакции.

```yaml
# alertmanager.yml
route:
  routes:
    - match:
        severity: critical
      receiver: 'oncall-primary'
      routes:
        # Escalate после 15 минут
        - match:
            severity: critical
          receiver: 'oncall-secondary'
          group_wait: 15m
          routes:
            # Escalate после 30 минут
            - match:
                severity: critical
              receiver: 'engineering-manager'
              group_wait: 30m
```

### Связь с Runbooks

**Правило:** Каждый alert имеет runbook.

```yaml
annotations:
  runbook: "https://runbooks.example.com/{{ .Labels.alertname | toLower }}"
```

**Правило:** Формат URL runbook.

```
https://runbooks.example.com/{category}/{alert-name}

Примеры:
https://runbooks.example.com/api/high-error-rate
https://runbooks.example.com/database/connection-exhausted
https://runbooks.example.com/infrastructure/disk-full
```

**Правило:** Slack notification содержит ссылку на runbook.

```yaml
slack_configs:
  - channel: '#alerts'
    title: '{{ .Status | toUpper }}: {{ .GroupLabels.alertname }}'
    text: |
      *Service:* {{ .GroupLabels.service }}
      *Severity:* {{ .GroupLabels.severity }}
      *Summary:* {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}

      :book: *Runbook:* {{ range .Alerts }}{{ .Annotations.runbook }}{{ end }}
      :chart_with_upwards_trend: *Dashboard:* {{ range .Alerts }}{{ .Annotations.dashboard }}{{ end }}
    actions:
      - type: button
        text: 'Runbook'
        url: '{{ range .Alerts }}{{ .Annotations.runbook }}{{ end }}'
      - type: button
        text: 'Dashboard'
        url: '{{ range .Alerts }}{{ .Annotations.dashboard }}{{ end }}'
```

### Noise Reduction

**Правило:** Группировать связанные alerts.

```yaml
route:
  group_by: ['alertname', 'service', 'cluster']
  group_wait: 30s      # Ждать перед отправкой группы
  group_interval: 5m   # Интервал между группами
```

**Правило:** Inhibition rules для подавления child alerts.

```yaml
# alertmanager.yml
inhibit_rules:
  # Если сервис down, подавить alerts о latency и errors
  - source_match:
      alertname: 'ServiceDown'
    target_match_re:
      alertname: '(HighLatency|HighErrorRate)'
    equal: ['service']

  # Если cluster down, подавить alerts о nodes
  - source_match:
      alertname: 'ClusterDown'
    target_match_re:
      alertname: 'Node.*'
    equal: ['cluster']

  # Critical подавляет warning того же alert
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service']
```

**Правило:** Silences для плановых работ.

```bash
# Создать silence на 2 часа
amtool silence add \
  --alertmanager.url=http://alertmanager:9093 \
  --author="john@example.com" \
  --comment="Planned maintenance" \
  --duration=2h \
  service="api-server"

# Список silences
amtool silence query --alertmanager.url=http://alertmanager:9093

# Удалить silence
amtool silence expire <silence-id>
```

### Alertmanager конфигурация

**Правило:** Полная конфигурация Alertmanager.

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alerts@example.com'
  slack_api_url: 'https://hooks.slack.com/services/xxx'
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  receiver: 'default'
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    # Critical alerts
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true

    - match:
        severity: critical
      receiver: 'slack-critical'

    # High alerts
    - match:
        severity: high
      receiver: 'slack-high'
      group_wait: 1m

    # Warning alerts
    - match:
        severity: warning
      receiver: 'slack-warning'
      group_wait: 5m

    # Team routing
    - match:
        team: backend
      receiver: 'slack-backend'
    - match:
        team: platform
      receiver: 'slack-platform'

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts-default'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - routing_key: 'xxx'
        severity: critical
        description: '{{ .GroupLabels.alertname }}: {{ .Annotations.summary }}'
        details:
          service: '{{ .GroupLabels.service }}'
          runbook: '{{ .Annotations.runbook }}'

  - name: 'slack-critical'
    slack_configs:
      - channel: '#incidents'
        color: 'danger'
        title: ':rotating_light: CRITICAL: {{ .GroupLabels.alertname }}'
        text: |
          *Service:* {{ .GroupLabels.service }}
          *Summary:* {{ .Annotations.summary }}
          *Runbook:* {{ .Annotations.runbook }}
        send_resolved: true

  - name: 'slack-high'
    slack_configs:
      - channel: '#alerts-high'
        color: 'warning'
        title: ':warning: HIGH: {{ .GroupLabels.alertname }}'
        text: |
          *Service:* {{ .GroupLabels.service }}
          *Summary:* {{ .Annotations.summary }}
        send_resolved: true

  - name: 'slack-warning'
    slack_configs:
      - channel: '#alerts-warning'
        color: '#439FE0'
        title: ':information_source: WARNING: {{ .GroupLabels.alertname }}'

  - name: 'slack-backend'
    slack_configs:
      - channel: '#backend-alerts'

  - name: 'slack-platform'
    slack_configs:
      - channel: '#platform-alerts'

inhibit_rules:
  - source_match:
      alertname: 'ServiceDown'
    target_match_re:
      alertname: '(HighLatency|HighErrorRate|SlowQueries)'
    equal: ['service']

  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service']
```

---

## Примеры

### Пример 1: Стандартные alert rules

```yaml
# prometheus-rules/api-alerts.yml
groups:
  - name: api-availability
    rules:
      - alert: APIDown
        expr: up{job="api-server"} == 0
        for: 1m
        labels:
          severity: critical
          service: api
        annotations:
          summary: "API server is down"
          description: "Instance {{ $labels.instance }} is not responding"
          runbook: "https://runbooks.example.com/api/down"
          dashboard: "https://grafana.example.com/d/api-overview"

      - alert: APIHighErrorRate
        expr: |
          sum(rate(http_requests_total{job="api-server",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{job="api-server"}[5m])) > 0.05
        for: 5m
        labels:
          severity: high
          service: api
        annotations:
          summary: "API error rate > 5%"
          description: "Current error rate: {{ $value | humanizePercentage }}"
          runbook: "https://runbooks.example.com/api/high-error-rate"

      - alert: APIHighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket{job="api-server"}[5m]))
            by (le)
          ) > 1
        for: 5m
        labels:
          severity: high
          service: api
        annotations:
          summary: "API p99 latency > 1s"
          description: "Current p99: {{ $value | humanizeDuration }}"
          runbook: "https://runbooks.example.com/api/high-latency"

  - name: api-resources
    rules:
      - alert: APIHighMemory
        expr: |
          container_memory_usage_bytes{container="api-server"}
          /
          container_spec_memory_limit_bytes{container="api-server"} > 0.9
        for: 10m
        labels:
          severity: warning
          service: api
        annotations:
          summary: "API memory usage > 90%"
          description: "Pod {{ $labels.pod }} using {{ $value | humanizePercentage }} memory"

      - alert: APIHighCPU
        expr: |
          rate(container_cpu_usage_seconds_total{container="api-server"}[5m])
          /
          container_spec_cpu_quota{container="api-server"}
          * container_spec_cpu_period{container="api-server"} > 0.8
        for: 10m
        labels:
          severity: warning
          service: api
        annotations:
          summary: "API CPU usage > 80%"

  - name: api-sla
    rules:
      - alert: SLABreach
        expr: |
          (
            sum(rate(http_requests_total{job="api-server",status!~"5.."}[30d]))
            /
            sum(rate(http_requests_total{job="api-server"}[30d]))
          ) < 0.999
        for: 5m
        labels:
          severity: high
          service: api
        annotations:
          summary: "SLA breach: availability < 99.9%"
          description: "30-day availability: {{ $value | humanizePercentage }}"
          runbook: "https://runbooks.example.com/api/sla-breach"
```

### Пример 2: Database alerts

```yaml
# prometheus-rules/database-alerts.yml
groups:
  - name: database
    rules:
      - alert: DatabaseDown
        expr: pg_up == 0
        for: 1m
        labels:
          severity: critical
          service: database
        annotations:
          summary: "PostgreSQL is down"
          runbook: "https://runbooks.example.com/database/down"

      - alert: DatabaseConnectionsExhausted
        expr: |
          pg_stat_activity_count{datname!=""}
          /
          pg_settings_max_connections > 0.8
        for: 5m
        labels:
          severity: high
          service: database
        annotations:
          summary: "Database connections > 80%"
          description: "{{ $value | humanizePercentage }} of max connections used"
          runbook: "https://runbooks.example.com/database/connections"

      - alert: DatabaseReplicationLag
        expr: pg_replication_lag_seconds > 60
        for: 5m
        labels:
          severity: high
          service: database
        annotations:
          summary: "Replication lag > 60s"
          description: "Lag: {{ $value | humanizeDuration }}"
          runbook: "https://runbooks.example.com/database/replication-lag"

      - alert: DatabaseSlowQueries
        expr: |
          rate(pg_stat_statements_seconds_total[5m])
          /
          rate(pg_stat_statements_calls_total[5m]) > 1
        for: 10m
        labels:
          severity: warning
          service: database
        annotations:
          summary: "Average query time > 1s"

      - alert: DatabaseDiskSpace
        expr: |
          pg_database_size_bytes
          /
          node_filesystem_size_bytes{mountpoint="/var/lib/postgresql"} > 0.8
        for: 15m
        labels:
          severity: warning
          service: database
        annotations:
          summary: "Database disk usage > 80%"
          runbook: "https://runbooks.example.com/database/disk-space"
```

### Пример 3: Slack notification template

```yaml
# alertmanager-templates/slack.tmpl
{{ define "slack.default.title" -}}
{{ if eq .Status "firing" }}
{{- if eq (index .Alerts 0).Labels.severity "critical" }}:rotating_light:{{ end -}}
{{- if eq (index .Alerts 0).Labels.severity "high" }}:warning:{{ end -}}
{{- if eq (index .Alerts 0).Labels.severity "warning" }}:information_source:{{ end -}}
{{ else }}
:white_check_mark:
{{ end }}
{{ .Status | toUpper }}: {{ .GroupLabels.alertname }}
{{- end }}

{{ define "slack.default.text" -}}
*Service:* {{ .GroupLabels.service }}
*Severity:* {{ (index .Alerts 0).Labels.severity }}
*Alerts:* {{ len .Alerts }}

{{ range .Alerts -}}
*Instance:* {{ .Labels.instance }}
*Summary:* {{ .Annotations.summary }}
{{ if .Annotations.description }}*Description:* {{ .Annotations.description }}{{ end }}

{{ end }}

{{ if (index .Alerts 0).Annotations.runbook -}}
:book: <{{ (index .Alerts 0).Annotations.runbook }}|Runbook>
{{- end }}
{{ if (index .Alerts 0).Annotations.dashboard -}}
:chart_with_upwards_trend: <{{ (index .Alerts 0).Annotations.dashboard }}|Dashboard>
{{- end }}
{{- end }}
```

### Пример 4: Grafana alert rule (современный формат)

```yaml
# grafana-alerts.yml
apiVersion: 1

groups:
  - name: API Alerts
    folder: Alerts
    interval: 1m
    rules:
      - uid: api-error-rate
        title: High API Error Rate
        condition: C
        data:
          - refId: A
            datasourceUid: prometheus
            model:
              expr: |
                sum(rate(http_requests_total{job="api-server",status=~"5.."}[5m]))
                /
                sum(rate(http_requests_total{job="api-server"}[5m]))
              intervalMs: 1000
              maxDataPoints: 43200
          - refId: B
            datasourceUid: __expr__
            model:
              type: reduce
              reducer: last
              expression: A
          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              expression: B
              conditions:
                - evaluator:
                    params: [0.05]
                    type: gt
        for: 5m
        annotations:
          summary: API error rate exceeds 5%
          runbook_url: https://runbooks.example.com/api/high-error-rate
        labels:
          severity: high
          service: api
        noDataState: NoData
        execErrState: Error
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Alert не срабатывает — как отладить?

1. **Проверить expression в Prometheus:**
   ```promql
   # Скопировать expr из alert rule
   sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
   ```

2. **Проверить статус alert:**
   ```bash
   # Prometheus alerts endpoint
   curl http://prometheus:9090/api/v1/alerts

   # Alertmanager alerts
   curl http://alertmanager:9093/api/v2/alerts
   ```

3. **Проверить `for` duration:**
   - Alert в "pending" пока не прошло `for` время
   - Проверить в Prometheus UI → Alerts

4. **Проверить inhibitions:**
   - Другой alert может подавлять текущий

### Alert fatigue — как уменьшить шум?

1. **Audit alerts:**
   ```
   За последний месяц:
   - Сколько alerts сработало?
   - Сколько требовали действий?
   - Сколько были resolved автоматически?
   ```

2. **Удалить/объединить:**
   - Alerts с < 10% actionable rate
   - Дублирующие alerts
   - Info-level alerts → dashboard

3. **Настроить пороги:**
   - Увеличить `for` duration
   - Добавить hysteresis
   - Использовать percentiles вместо averages

4. **Группировка:**
   ```yaml
   group_by: ['alertname', 'service', 'cluster']
   group_wait: 5m
   ```

### Как настроить on-call rotation?

1. **PagerDuty:**
   ```yaml
   pagerduty_configs:
     - service_key: 'primary-oncall-key'
       severity: '{{ .Labels.severity }}'
   ```

2. **Opsgenie:**
   ```yaml
   opsgenie_configs:
     - api_key: 'xxx'
       responders:
         - name: 'Backend On-Call'
           type: schedule
   ```

3. **Slack escalation:**
   - Primary → @oncall-primary
   - 15 min → @oncall-secondary
   - 30 min → @engineering-manager

### Как тестировать alert rules?

```yaml
# Promtool unit tests
# test-alerts.yml
rule_files:
  - alerts.yml

tests:
  - interval: 1m
    input_series:
      - series: 'http_requests_total{status="500"}'
        values: '10+10x10'  # 10, 20, 30, ...
      - series: 'http_requests_total{status="200"}'
        values: '100+0x10'  # 100, 100, 100, ...

    alert_rule_test:
      - eval_time: 5m
        alertname: HighErrorRate
        exp_alerts:
          - exp_labels:
              severity: high
            exp_annotations:
              summary: "Error rate > 5%"
```

```bash
# Запуск тестов
promtool test rules test-alerts.yml
```

---

## Связанные инструкции

- [overview.md](overview.md) — Обзор observability
- [metrics.md](metrics.md) — Prometheus метрики
- [operations.md](../operations.md) — Runbooks и инциденты
