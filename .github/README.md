# /.github/ — GitHub платформа

## Зона ответственности

Конфигурации GitHub: CI/CD, шаблоны, владельцы кода.

**IN:** workflows/, ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md, CODEOWNERS

**Границы:**
- GitHub конфигурации → здесь
- код проекта → /src/
- скрипты деплоя → /platform/scripts/

> [Разделение ответственности всех папок проекта](/.structure/README.md)

---

## Структура

```
.github/
├── workflows/              # CI/CD pipelines
│   ├── ci.yml
│   ├── deploy.yml
│   └── release.yml
├── ISSUE_TEMPLATE/         # Шаблоны Issues
│   ├── bug.md
│   ├── feature.md
│   └── task.md
├── PULL_REQUEST_TEMPLATE.md
└── CODEOWNERS
```

---

## Связи

- **Инструкции:** [/.claude/.instructions/.github/](/.claude/.instructions/.github/)
