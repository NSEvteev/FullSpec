# Infrastructure (Инфраструктурный код)

Конфигурации для развертывания и управления инфраструктурой.

## Структура

```
infrastructure/
├── docker/               # Docker конфигурации
│   ├── nginx/
│   ├── postgres/
│   └── redis/
│
├── kubernetes/           # K8s манифесты
│   ├── deployments/
│   ├── services/
│   └── ingress/
│
└── terraform/            # IaC (Infrastructure as Code)
    ├── aws/
    └── gcp/
```

## Docker

Конфигурации для локальной разработки и production.

## Kubernetes

Манифесты для деплоя в K8s кластер.

## Terraform

Infrastructure as Code для облачных провайдеров.
