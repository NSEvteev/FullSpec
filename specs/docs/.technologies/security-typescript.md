---
description: Security-инструменты TypeScript — npm audit, ESLint security plugin, SAST.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: typescript
type: security
---

# Security TypeScript v1.0

## Инструменты

| Инструмент | Тип | Пакет / Команда | Назначение |
|------------|-----|----------------|-----------|
| npm audit | Dependency audit | встроен в npm | Проверка уязвимостей в зависимостях |
| eslint-plugin-security | SAST | `eslint-plugin-security` | Статический анализ: SQL-инъекции, ReDoS, небезопасный eval |
| eslint-plugin-no-secrets | SAST | `eslint-plugin-no-secrets` | Обнаружение секретов в коде |
| gitleaks | Pre-commit | `gitleaks` (binary) | Обнаружение секретов до push |

## Dependency Audit

Команда для проверки уязвимостей в зависимостях:

```bash
# Проверить уязвимости — все уровни
npm audit

# Только high и critical
npm audit --audit-level=high

# Вывод в JSON (для CI)
npm audit --json

# Исправить автоматически (только minor/patch обновления)
npm audit fix

# Показать только production-зависимости
npm audit --omit=dev
```

**Severity-модель:**

| Уровень | Действие |
|---------|----------|
| critical | Блокирует сборку/деплой, исправить немедленно |
| high | Исправить до следующего релиза |
| moderate | Исправить в плановом порядке |
| low, info | Оценить, исправить при наличии возможности |

Допустимые исключения — задокументировать через `npm audit --json` + `npm audit fix --force` (только если breaking change приемлем).

## SAST

Конфигурация ESLint с security-плагинами (`.eslintrc.cjs` или `eslint.config.mjs`):

```javascript
// eslint.config.mjs — flat config (ESLint 9.x)
import securityPlugin from "eslint-plugin-security";
import noSecretsPlugin from "eslint-plugin-no-secrets";

export default [
  {
    plugins: {
      security: securityPlugin,
      "no-secrets": noSecretsPlugin,
    },
    rules: {
      // Небезопасное использование регулярных выражений (ReDoS)
      "security/detect-unsafe-regex": "error",
      // Небезопасное использование eval, Function()
      "security/detect-eval-with-expression": "error",
      // Небезопасный доступ к свойствам через переменные
      "security/detect-object-injection": "warn",
      // Небезопасное создание дочерних процессов
      "security/detect-child-process": "error",
      // Чтение файлов с переменным путём
      "security/detect-non-literal-fs-filename": "warn",
      // Обнаружение секретов в строках
      "no-secrets/no-secrets": ["error", { tolerance: 4.5 }],
    },
  },
];
```

**Запуск SAST:**

```bash
npx eslint src --ext .ts,.tsx --rule "security/detect-unsafe-regex: error"
# Или полный прогон всех правил:
npx eslint src --ext .ts,.tsx
```

## CI Integration

GitHub Actions job fragment для security-проверок TypeScript:

```yaml
# .github/workflows/security-typescript.yml (или добавить job в основной CI)
name: Security TypeScript

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 8 * * 1"  # Каждый понедельник в 08:00 UTC

jobs:
  security-typescript:
    name: TypeScript Security Scan
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: npm audit (high+critical)
        run: npm audit --audit-level=high
        # Допустимо: continue-on-error: true если есть known exceptions

      - name: ESLint security rules
        run: npx eslint src --ext .ts,.tsx --max-warnings 0

      - name: TypeScript strict check
        run: npx tsc --noEmit
```

## Known Exceptions

*Нет известных исключений при создании стандарта. При появлении задокументировать:*

| CVE / Rule | Пакет | Причина исключения | Дата ревизии |
|-----------|-------|-------------------|-------------|
| — | — | — | — |
