---
type: standard
description: Стратегии деплоя — rolling update, blue-green, canary, автооткат
related:
  - platform/docker.md
  - platform/observability/overview.md
  - platform/operations.md
  - git/ci.md
---

# Деплой

Правила деплоя: стратегии развёртывания, откат, health checks.

## Оглавление

- [Правила](#правила)
  - [Стратегии деплоя](#стратегии-деплоя)
  - [Rolling Update](#rolling-update)
  - [Blue-Green Deployment](#blue-green-deployment)
  - [Canary Deployment](#canary-deployment)
  - [Health Checks](#health-checks)
  - [Автооткат](#автооткат)
  - [Pre/Post Deploy Hooks](#prepost-deploy-hooks)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Стратегии деплоя

**Правило:** Выбирать стратегию в зависимости от требований.

| Стратегия | Downtime | Rollback | Ресурсы | Когда использовать |
|-----------|----------|----------|---------|-------------------|
| Rolling Update | Нет | Медленный | 1.25x | Стандартный деплой |
| Blue-Green | Нет | Мгновенный | 2x | Критичные сервисы |
| Canary | Нет | Быстрый | 1.1x | Рискованные изменения |
| Recreate | Да | Быстрый | 1x | Dev/staging |

**Правило:** Production всегда использует zero-downtime стратегии.

### Rolling Update

**Правило:** Постепенная замена инстансов новой версией.

```yaml
# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # +1 инстанс во время деплоя
      maxUnavailable: 0  # всегда минимум 4 доступны
  template:
    spec:
      containers:
        - name: api
          image: api:v1.2.3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
```

**Правило:** `maxUnavailable: 0` для zero-downtime.

**Правило:** Readiness probe должен пройти перед приёмом трафика.

```
Процесс Rolling Update:

Начало:  [v1] [v1] [v1] [v1]
Шаг 1:   [v1] [v1] [v1] [v1] [v2*]  # создаётся новый
Шаг 2:   [v1] [v1] [v1] [v2] [v2*]  # v2 ready, старый удаляется
Шаг 3:   [v1] [v1] [v2] [v2] [v2*]
Шаг 4:   [v1] [v2] [v2] [v2] [v2*]
Конец:   [v2] [v2] [v2] [v2]
```

### Blue-Green Deployment

**Правило:** Две идентичные среды, мгновенное переключение трафика.

```
┌─────────────────────────────────────────┐
│              Load Balancer              │
│                   │                     │
│         ┌────────┴────────┐             │
│         ▼                 ▼             │
│   ┌───────────┐     ┌───────────┐       │
│   │   Blue    │     │   Green   │       │
│   │ (v1.2.2)  │     │ (v1.2.3)  │       │
│   │  active   │     │  standby  │       │
│   └───────────┘     └───────────┘       │
└─────────────────────────────────────────┘
```

**Правило:** Обе среды должны быть идентичны по ресурсам.

```yaml
# Kubernetes с Istio
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routing
spec:
  hosts:
    - api.example.com
  http:
    - route:
        - destination:
            host: api-blue
            port:
              number: 80
          weight: 100  # весь трафик на blue
        - destination:
            host: api-green
            port:
              number: 80
          weight: 0    # green в standby
```

**Переключение:**

```bash
# Переключить трафик на green
kubectl patch virtualservice api-routing --type='json' \
  -p='[
    {"op": "replace", "path": "/spec/http/0/route/0/weight", "value": 0},
    {"op": "replace", "path": "/spec/http/0/route/1/weight", "value": 100}
  ]'
```

### Canary Deployment

**Правило:** Постепенное увеличение трафика на новую версию.

```
Этапы Canary:

Этап 1: 5% трафика на canary, мониторинг 15 минут
Этап 2: 25% трафика, мониторинг 30 минут
Этап 3: 50% трафика, мониторинг 30 минут
Этап 4: 100% трафика, canary становится stable
```

```yaml
# Flagger (автоматический canary)
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api-server
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  service:
    port: 80
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        thresholdRange:
          min: 99
        interval: 1m
      - name: request-duration
        thresholdRange:
          max: 500
        interval: 1m
  webhooks:
    - name: load-test
      url: http://flagger-loadtester/
      metadata:
        cmd: "hey -z 1m -q 10 -c 2 http://api-server-canary/"
```

**Правило:** Автоматический rollback при ухудшении метрик.

| Метрика | Порог для rollback |
|---------|-------------------|
| Success rate | < 99% |
| P99 latency | > 500ms |
| Error rate | > 1% |

### Health Checks

**Правило:** Каждый сервис имеет три эндпоинта.

| Эндпоинт | Назначение | Что проверяет |
|----------|------------|---------------|
| `/health/live` | Liveness | Процесс жив |
| `/health/ready` | Readiness | Готов принимать трафик |
| `/health/startup` | Startup | Инициализация завершена |

```go
// Пример реализации
func (s *Server) healthLive(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("OK"))
}

func (s *Server) healthReady(w http.ResponseWriter, r *http.Request) {
    // Проверить зависимости
    if err := s.db.Ping(r.Context()); err != nil {
        w.WriteHeader(http.StatusServiceUnavailable)
        json.NewEncoder(w).Encode(map[string]string{
            "status": "not ready",
            "reason": "database unavailable",
        })
        return
    }

    if err := s.redis.Ping(r.Context()).Err(); err != nil {
        w.WriteHeader(http.StatusServiceUnavailable)
        json.NewEncoder(w).Encode(map[string]string{
            "status": "not ready",
            "reason": "cache unavailable",
        })
        return
    }

    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "ready"})
}
```

**Правило:** Readiness probe определяет приём трафика.

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  successThreshold: 1
  failureThreshold: 3

livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
  successThreshold: 1
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  initialDelaySeconds: 0
  periodSeconds: 5
  failureThreshold: 30  # 150 секунд на старт
```

### Автооткат

**Правило:** Автоматический откат при падении метрик качества.

```yaml
# Kubernetes rollback
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  annotations:
    kubernetes.io/change-cause: "Deploy v1.2.3"
spec:
  revisionHistoryLimit: 5  # хранить 5 предыдущих версий
```

```bash
# Ручной откат
kubectl rollout undo deployment/api-server

# Откат к конкретной версии
kubectl rollout history deployment/api-server
kubectl rollout undo deployment/api-server --to-revision=3

# Статус отката
kubectl rollout status deployment/api-server
```

**Правило:** Откат должен завершиться за < 5 минут.

| Триггер отката | Автоматический | Ручной |
|----------------|----------------|--------|
| Health check failed | Да (K8s) | — |
| Error rate > 5% | Да (с Flagger) | — |
| Latency p99 > 1s | Да (с Flagger) | — |
| Бизнес-метрики | — | Да |
| Обнаружен баг | — | Да |

### Pre/Post Deploy Hooks

**Правило:** Использовать hooks для миграций и валидации.

```yaml
# Kubernetes Job для миграций
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    helm.sh/hook: pre-upgrade
    helm.sh/hook-weight: "0"
    helm.sh/hook-delete-policy: hook-succeeded
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: api:v1.2.3
          command: ["./migrate", "up"]
      restartPolicy: Never
  backoffLimit: 3
```

**Правило:** Миграции должны быть обратно совместимы.

```
Pre-deploy:
1. Запустить миграции БД (добавить новые колонки, NOT NULL → NULL)
2. Проверить миграции успешны
3. Начать деплой

Post-deploy:
1. Smoke tests
2. Удалить старые колонки (если нужно)
3. Уведомление о завершении
```

---

## Примеры

### Пример 1: GitHub Actions деплой

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Build and push Docker image
        run: |
          docker build -t ${{ vars.REGISTRY }}/api:${{ github.sha }} .
          docker push ${{ vars.REGISTRY }}/api:${{ github.sha }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/api-server \
            api=${{ vars.REGISTRY }}/api:${{ github.sha }}
          kubectl rollout status deployment/api-server --timeout=5m

      - name: Smoke tests
        run: |
          curl -f https://api.example.com/health/ready
          ./scripts/smoke-tests.sh

      - name: Rollback on failure
        if: failure()
        run: |
          kubectl rollout undo deployment/api-server
          kubectl rollout status deployment/api-server
```

### Пример 2: Helm chart с blue-green

```yaml
# values.yaml
deployment:
  blue:
    enabled: true
    image: api:v1.2.2
    replicas: 3

  green:
    enabled: true
    image: api:v1.2.3
    replicas: 3

routing:
  active: blue  # или green

# templates/virtualservice.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: {{ .Release.Name }}
spec:
  hosts:
    - {{ .Values.host }}
  http:
    - route:
        - destination:
            host: {{ .Release.Name }}-blue
          weight: {{ if eq .Values.routing.active "blue" }}100{{ else }}0{{ end }}
        - destination:
            host: {{ .Release.Name }}-green
          weight: {{ if eq .Values.routing.active "green" }}100{{ else }}0{{ end }}
```

### Пример 3: Canary с Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api-server
spec:
  replicas: 5
  strategy:
    canary:
      steps:
        - setWeight: 5
        - pause: { duration: 5m }
        - setWeight: 20
        - pause: { duration: 10m }
        - setWeight: 50
        - pause: { duration: 10m }
        - setWeight: 80
        - pause: { duration: 5m }
      canaryService: api-server-canary
      stableService: api-server-stable
      trafficRouting:
        istio:
          virtualService:
            name: api-server-vsvc
            routes:
              - primary
      analysis:
        templates:
          - templateName: success-rate
        startingStep: 2
        args:
          - name: service-name
            value: api-server-canary

---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.99
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{
              service="{{args.service-name}}",
              status=~"2.."
            }[5m])) /
            sum(rate(http_requests_total{
              service="{{args.service-name}}"
            }[5m]))
```

### Пример 4: Graceful shutdown

```go
package main

import (
    "context"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    server := &http.Server{
        Addr:    ":8080",
        Handler: setupRoutes(),
    }

    // Канал для graceful shutdown
    done := make(chan bool)
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

    go func() {
        <-quit
        log.Println("Server is shutting down...")

        // Перестать принимать новые запросы
        // (readiness probe вернёт 503)
        setNotReady()

        // Дать время для удаления из load balancer
        time.Sleep(5 * time.Second)

        // Graceful shutdown с таймаутом
        ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()

        if err := server.Shutdown(ctx); err != nil {
            log.Fatalf("Server forced to shutdown: %v", err)
        }

        close(done)
    }()

    log.Println("Server is starting...")
    if err := server.ListenAndServe(); err != http.ErrServerClosed {
        log.Fatalf("Server error: %v", err)
    }

    <-done
    log.Println("Server stopped gracefully")
}
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Деплой зависает — что делать?

1. **Проверить статус rollout:**
   ```bash
   kubectl rollout status deployment/api-server
   kubectl describe deployment api-server
   ```

2. **Проверить pods:**
   ```bash
   kubectl get pods -l app=api-server
   kubectl describe pod <pod-name>
   kubectl logs <pod-name>
   ```

3. **Частые причины:**
   | Симптом | Причина | Решение |
   |---------|---------|---------|
   | `ImagePullBackOff` | Нет доступа к registry | Проверить credentials |
   | `CrashLoopBackOff` | Приложение падает | Проверить логи |
   | `Pending` | Нет ресурсов | Увеличить node pool |
   | Readiness failed | Приложение не отвечает | Проверить health endpoint |

### Как откатиться на предыдущую версию?

```bash
# Посмотреть историю
kubectl rollout history deployment/api-server

# Откат на предыдущую версию
kubectl rollout undo deployment/api-server

# Откат на конкретную ревизию
kubectl rollout undo deployment/api-server --to-revision=2

# Проверить статус
kubectl rollout status deployment/api-server
```

### Миграции ломают откат — что делать?

**Правило:** Миграции должны быть обратно совместимы.

| Операция | Безопасно для отката | Небезопасно |
|----------|---------------------|-------------|
| Добавить колонку | Да | — |
| Удалить колонку | — | Да |
| Переименовать | — | Да |
| Изменить тип | — | Да |
| Добавить NOT NULL | — | Да (если нет default) |

**Паттерн expand-contract:**

```
Версия 1.0: колонка "name"
Версия 1.1: добавить "full_name", копировать данные, писать в обе
Версия 1.2: читать из "full_name", писать в обе
Версия 1.3: удалить "name"
```

### Canary показывает ошибки — автооткат или ждать?

**Правило:** Автооткат при:
- Error rate > 5%
- P99 latency > 2x baseline
- Критические бизнес-метрики упали

**Продолжить, если:**
- Ошибки в пределах нормы (< 1%)
- Ошибки только для edge cases
- Метрики стабилизируются

```bash
# Ручной откат canary
kubectl argo rollouts abort api-server

# Продолжить canary
kubectl argo rollouts promote api-server
```

### Как деплоить без простоя при миграции схемы БД?

1. **Двухфазный деплой:**
   ```
   Фаза 1: Деплой новой версии с поддержкой старой схемы
   Фаза 2: Миграция схемы
   Фаза 3: Деплой версии без поддержки старой схемы
   ```

2. **Использовать feature flags:**
   ```python
   if feature_flag("use_new_schema"):
       return query_new_schema()
   return query_old_schema()
   ```

3. **Online schema migration** (для больших таблиц):
   - gh-ost (GitHub)
   - pt-online-schema-change (Percona)

---

## Связанные инструкции

- [docker.md](docker.md) — Docker образы
- [observability/overview.md](observability/overview.md) — Мониторинг деплоя
- [operations.md](operations.md) — Runbooks для инцидентов
- [ci.md](../git/ci.md) — CI/CD pipeline
