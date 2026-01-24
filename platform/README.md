# /platform/ — Общая инфраструктура

## Зона ответственности

Инфраструктурные конфигурации, скрипты, мониторинг.

**IN:** docker/, gateway/, monitoring/, k8s/, scripts/, docs/, runbooks/

**Границы:**
- инфраструктура системы → здесь
- бизнес-код сервисов → /src/
- скрипты Claude → /.claude/scripts/

> [Разделение ответственности всех папок проекта](/.structure/README.md)

---

## Структура

```
platform/
├── docker/           # Docker конфиги
├── gateway/          # API Gateway (Traefik/Nginx)
├── monitoring/       # Prometheus, Grafana, Loki
│   ├── prometheus/   # Метрики и алерты
│   ├── grafana/      # Дашборды
│   └── loki/         # Логи
├── k8s/              # Kubernetes манифесты
├── scripts/          # Инфра-скрипты (deploy, backup)
├── docs/             # Документация инфраструктуры
└── runbooks/         # Операционные runbooks
```

---

## Связи

- **Инструкции:** [/.claude/.instructions/platform/](/.claude/.instructions/platform/)
