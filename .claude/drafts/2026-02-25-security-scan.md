# Security Scan / Dependency Audit — отдельный стандарт

Определение стандарта безопасности: dependency audit, SAST, секреты, интеграция в CI и Release workflow.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** В Release workflow отсутствует проверка безопасности. Черновик release-create отметил это как пробел по сравнению с best practices.
**Почему создан:** Security scan — отдельный quality gate, не часть Release workflow. Нужен собственный стандарт.
**Связанные файлы:**
- `/.github/.instructions/releases/standard-release.md` — § 9 Подготовка релиза (нет security check)
- `/.github/.instructions/.scripts/validate-pre-release.py` — нет проверки зависимостей
- `/.github/workflows/ci.yml` — нет security job

## Содержание

### Что нужно

1. **Стандарт security** — `standard-security.md` или секция в standard-action.md
2. **GitHub Action** — job в CI или отдельный workflow
3. **Интеграция с Release** — pre-release gate или отдельный шаг

### Области security

| Область | Инструмент | Интеграция |
|---------|-----------|------------|
| Dependency audit | `pip audit`, `npm audit`, Dependabot | CI job + pre-release check |
| SAST (Static Analysis) | Bandit (Python), ESLint security plugin | CI job |
| Secrets detection | Gitleaks, truffleHog | Pre-commit hook + CI |
| Container scanning | Trivy, Snyk | Deploy workflow |
| Dependabot alerts | GitHub native | Проверка в pre-release |

### Варианты интеграции

**Вариант A: Job в ci.yml**
```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v6
    - run: pip audit
    - run: bandit -r src/
```

**Вариант B: Отдельный workflow `security.yml`**
- Запуск по расписанию (weekly) + при PR
- Не блокирует merge, но создаёт Issues

**Вариант C: Pre-release gate**
- Добавить в validate-pre-release.py проверку Dependabot alerts
- `gh api repos/{o}/{r}/dependabot/alerts --jq '.[].state' | grep open`

## Решения

*Нет решений — требуется выбрать инструменты и уровень интеграции.*

## Открытые вопросы

- Какой уровень security нужен на старте? (минимум: dependency audit / полный: SAST + secrets + containers)
- Блокировать ли merge при обнаружении уязвимостей или только предупреждать?
- Нужен ли отдельный стандарт `standard-security.md` или достаточно секции в `standard-action.md`?
- Как обрабатывать false positives?
- Нужен ли Dependabot или достаточно ручного `pip audit`?
