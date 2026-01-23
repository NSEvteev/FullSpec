# Структура папок проекта

---

## Корневые файлы

```
/
├── .gitignore                       # Git ignore
├── CLAUDE.md                        # Точка входа для Claude
├── Makefile                         # Команды (make help)
└── README.md                        # Главный README
```

---

## Дерево папок

```
/
├── .claude/                             # Инструменты Claude
│   ├── .instructions/
│   │   └── skills/                      #   Как писать скиллы
│   ├── agents/                          #   Агенты
│   ├── drafts/                          #   Черновики (в git)
│   ├── skills/                          #   Скиллы (14)
│   └── settings.json                    #   Настройки
│
├── .github/                             # GitHub платформа
│   ├── .instructions/                   #   Стандарты GitHub (TODO)
│   ├── ISSUE_TEMPLATE/                  #   Шаблоны Issues
│   └── workflows/                       #   CI/CD pipelines
│
├── .instructions/                       # Мета: как писать инструкции
│
├── .structure/                          # SSOT структуры проекта
│   └── project.md                       #   Этот файл
│
├── config/                              # Конфигурации окружений
│   ├── .instructions/                   #   Стандарты конфигураций (TODO)
│   ├── *.yaml                           #   development, staging, production
│   └── feature-flags/                   #   Feature flags
│
├── platform/                            # Общая инфраструктура
│   ├── .instructions/                   #   Стандарты инфраструктуры (TODO)
│   ├── docker/                          #   Docker конфигурации
│   ├── gateway/                         #   API Gateway
│   ├── k8s/                             #   Kubernetes манифесты
│   ├── monitoring/                      #   Мониторинг
│   │   ├── grafana/
│   │   ├── loki/
│   │   └── prometheus/
│   ├── runbooks/                        #   Runbooks
│   └── scripts/                         #   Инфраструктурные скрипты
│
├── shared/                              # Общий код между сервисами
│   ├── .instructions/                   #   Стандарты общего кода (TODO)
│   ├── assets/                          #   Статические ресурсы
│   ├── contracts/                       #   API контракты
│   │   ├── openapi/                     #     REST контракты
│   │   └── protobuf/                    #     gRPC контракты
│   ├── events/                          #   Схемы событий
│   ├── i18n/                            #   Локализация
│   └── libs/                            #   Общие библиотеки
│
├── specs/                               # Спецификации проекта
│   ├── .instructions/                   #   Как писать specs
│   ├── discussions/                     #   Дискуссии: DISC-*.md
│   ├── glossary.md                      #   Глоссарий терминов
│   ├── impact/                          #   Импакт-анализ: IMPACT-*.md
│   └── services/                        #   Спецификации сервисов
│       └── {service}/
│           ├── adr/                     #     ADR-*.md
│           └── plans/                   #     PLAN-*.md
│
├── src/                                 # Исходный код сервисов
│   ├── .instructions/                   #   Стандарты разработки (TODO)
│   └── {service}/                       #   Сервисы
│       ├── backend/
│       │   ├── health/
│       │   ├── shared/
│       │   └── v*/
│       ├── database/
│       │   └── migrations/
│       ├── docs/
│       ├── frontend/
│       └── tests/
│           ├── integration/
│           └── unit/
│
└── tests/                               # Системные тесты
    ├── .instructions/                   #   Стандарты тестирования (TODO)
    ├── e2e/                             #   End-to-end сценарии
    ├── fixtures/                        #   Общие тестовые данные
    ├── integration/                     #   Интеграция между сервисами
    ├── load/                            #   Нагрузочные тесты (k6)
    └── smoke/                           #   Smoke тесты
```
