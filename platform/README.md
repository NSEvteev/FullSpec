# /platform/ — Общая инфраструктура

Инфраструктурные конфигурации и скрипты.

## Содержимое

| IN | OUT |
|----|-----|
| docker, gateway, monitoring, k8s, scripts | Код сервисов (→ `/src/`) |

## Структура

```
platform/
├── docker/           # Docker конфиги
├── gateway/          # API Gateway (Traefik/Nginx)
├── monitoring/       # Prometheus, Grafana, Loki
├── k8s/              # Kubernetes манифесты
└── scripts/          # Инфра-скрипты (deploy, backup)
```

## Связанные ресурсы

- [Инструкции](/.claude/instructions/system/platform/) — правила инфраструктуры
- [Документация](/doc/platform/) — документация инфраструктуры
