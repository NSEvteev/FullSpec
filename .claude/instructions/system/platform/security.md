---
type: standard
description: Безопасность инфраструктуры — Dependabot, GitLeaks, Semgrep, scanning в CI
related:
  - platform/docker.md
  - platform/deployment.md
  - git/ci.md
  - src/security/auth.md
---

# Безопасность инфраструктуры

Правила безопасности: сканирование уязвимостей, секреты, статический анализ.

## Оглавление

- [Правила](#правила)
  - [Управление зависимостями](#управление-зависимостями)
  - [Сканирование секретов](#сканирование-секретов)
  - [Статический анализ безопасности](#статический-анализ-безопасности)
  - [Сканирование контейнеров](#сканирование-контейнеров)
  - [CI/CD Security Gates](#cicd-security-gates)
  - [Управление секретами](#управление-секретами)
- [Примеры](#примеры)
- [Скиллы](#скиллы)
- [FAQ / Troubleshooting](#faq--troubleshooting)
- [Связанные инструкции](#связанные-инструкции)

---

## Правила

### Управление зависимостями

**Правило:** Включить Dependabot для автоматического обновления зависимостей.

```yaml
# .github/dependabot.yml
version: 2
updates:
  # npm
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    groups:
      dev-dependencies:
        dependency-type: "development"
      production-dependencies:
        dependency-type: "production"
        update-types:
          - "minor"
          - "patch"

  # Docker
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"

  # Python
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

  # Go
  - package-ecosystem: "gomod"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Правило:** Автоматически мержить патч-обновления безопасности.

```yaml
# .github/workflows/dependabot-auto-merge.yml
name: Dependabot Auto-merge

on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: "${{ secrets.GITHUB_TOKEN }}"

      - name: Auto-merge patch updates
        if: steps.metadata.outputs.update-type == 'version-update:semver-patch'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Правило:** Блокировать PR с критическими уязвимостями.

| Severity | Действие | SLA |
|----------|----------|-----|
| Critical | Блокировать merge | 24 часа |
| High | Блокировать merge | 7 дней |
| Medium | Warning | 30 дней |
| Low | Info | Плановое обновление |

### Сканирование секретов

**Правило:** Использовать GitLeaks для обнаружения секретов в коде.

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:

jobs:
  gitleaks:
    name: Scan for secrets
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Правило:** Настроить .gitleaks.toml для исключений.

```toml
# .gitleaks.toml
title = "Gitleaks Config"

[allowlist]
description = "Allowlisted patterns"
paths = [
    '''\.gitleaks\.toml$''',
    '''(.*)?test(.*)?\.py$''',
    '''fixtures/''',
]
regexes = [
    '''EXAMPLE_''',
    '''PLACEHOLDER_''',
]

[[rules]]
id = "aws-access-key"
description = "AWS Access Key"
regex = '''AKIA[0-9A-Z]{16}'''
tags = ["aws", "credentials"]

[[rules]]
id = "private-key"
description = "Private Key"
regex = '''-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----'''
tags = ["key", "private"]

[[rules]]
id = "jwt"
description = "JWT Token"
regex = '''eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*'''
tags = ["jwt", "token"]
```

**Правило:** Pre-commit hook для проверки локально.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

### Статический анализ безопасности

**Правило:** Использовать Semgrep для SAST.

```yaml
# .github/workflows/semgrep.yml
name: Semgrep

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * 0'  # Еженедельно

jobs:
  semgrep:
    name: SAST Scan
    runs-on: ubuntu-latest
    container:
      image: returntocorp/semgrep

    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        run: |
          semgrep ci \
            --config auto \
            --config p/security-audit \
            --config p/secrets \
            --sarif --output semgrep.sarif

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
        if: always()
```

**Правило:** Настроить правила для технологического стека.

```yaml
# .semgrep.yml
rules:
  - id: hardcoded-password
    patterns:
      - pattern-either:
          - pattern: password = "..."
          - pattern: PASSWORD = "..."
          - pattern: secret = "..."
    message: "Hardcoded password detected"
    severity: ERROR
    languages: [python, javascript, go]

  - id: sql-injection
    patterns:
      - pattern: |
          $QUERY = "... " + $VAR + " ..."
          $DB.execute($QUERY)
    message: "Possible SQL injection"
    severity: ERROR
    languages: [python]

  - id: insecure-random
    pattern: Math.random()
    message: "Use crypto.randomBytes() for security-sensitive operations"
    severity: WARNING
    languages: [javascript, typescript]
```

### Сканирование контейнеров

**Правило:** Сканировать образы на уязвимости перед деплоем.

```yaml
# В CI workflow
- name: Build Docker image
  run: docker build -t $IMAGE:$TAG .

- name: Scan with Trivy
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE }}:${{ env.TAG }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'  # Fail на CRITICAL/HIGH

- name: Upload scan results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```

**Правило:** Пороги блокировки для контейнеров.

| Severity | Production | Staging | Dev |
|----------|------------|---------|-----|
| Critical | Block | Block | Warn |
| High | Block | Warn | — |
| Medium | Warn | — | — |

**Правило:** Регулярное сканирование запущенных образов.

```yaml
# .github/workflows/container-scan.yml
name: Scan Running Images

on:
  schedule:
    - cron: '0 6 * * *'  # Ежедневно в 6:00

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - name: Get deployed images
        run: |
          kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}' \
            | tr ' ' '\n' | sort -u > images.txt

      - name: Scan each image
        run: |
          while read image; do
            trivy image --severity CRITICAL,HIGH "$image"
          done < images.txt
```

### CI/CD Security Gates

**Правило:** Обязательные проверки безопасности перед merge.

```yaml
# Branch protection settings
required_status_checks:
  - gitleaks
  - semgrep
  - trivy-scan
  - dependency-check
```

**Правило:** Pipeline структура с security gates.

```
┌─────────────────────────────────────────────────────┐
│                    PR Pipeline                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Lint   │→ │  Test   │→ │  Build  │→ │ Security│ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
│                                              │       │
│                                              ▼       │
│                              ┌───────────────────┐  │
│                              │ Security Gates:   │  │
│                              │ • Gitleaks ✓      │  │
│                              │ • Semgrep ✓       │  │
│                              │ • Trivy ✓         │  │
│                              │ • Dependabot ✓    │  │
│                              └───────────────────┘  │
│                                              │       │
│                                              ▼       │
│                              ┌───────────────────┐  │
│                              │   Ready to Merge  │  │
│                              └───────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Управление секретами

**Правило:** Секреты хранятся только в защищённых хранилищах.

| Хранилище | Назначение | Примеры |
|-----------|------------|---------|
| GitHub Secrets | CI/CD | API keys, tokens |
| HashiCorp Vault | Runtime | DB passwords, certs |
| AWS Secrets Manager | Cloud | AWS-specific secrets |
| Kubernetes Secrets | K8s workloads | Service credentials |

**Правило:** Ротация секретов по расписанию.

| Тип секрета | Частота ротации |
|-------------|-----------------|
| API keys | 90 дней |
| Database passwords | 30 дней |
| Service tokens | 7 дней |
| Encryption keys | 365 дней |

**Правило:** Никогда не логировать секреты.

```python
# Неправильно
logger.info(f"Connecting with password: {password}")

# Правильно
logger.info("Connecting to database", extra={"host": host})
```

**Правило:** Использовать External Secrets Operator для K8s.

```yaml
# ExternalSecret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: db-credentials
    creationPolicy: Owner
  data:
    - secretKey: password
      remoteRef:
        key: secret/data/db
        property: password
```

---

## Примеры

### Пример 1: Полный security workflow

```yaml
name: Security

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 6 * * 1'  # Понедельник 6:00

jobs:
  secrets-scan:
    name: Secrets Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  sast:
    name: SAST
    runs-on: ubuntu-latest
    container:
      image: returntocorp/semgrep
    steps:
      - uses: actions/checkout@v4
      - run: semgrep ci --config auto --sarif -o semgrep.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep.sarif
        if: always()

  dependency-check:
    name: Dependency Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run npm audit
        run: npm audit --audit-level=high
        continue-on-error: true
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

  container-scan:
    name: Container Scan
    runs-on: ubuntu-latest
    needs: [secrets-scan, sast]
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t app:${{ github.sha }} .
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: app:${{ github.sha }}
          format: 'sarif'
          output: 'trivy.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy.sarif'
        if: always()

  security-gate:
    name: Security Gate
    runs-on: ubuntu-latest
    needs: [secrets-scan, sast, dependency-check, container-scan]
    steps:
      - name: All security checks passed
        run: echo "Security gate passed"
```

### Пример 2: Vault интеграция

```python
# vault_client.py
import hvac
from functools import lru_cache

class VaultClient:
    def __init__(self, url: str, token: str):
        self.client = hvac.Client(url=url, token=token)

    @lru_cache(maxsize=100)
    def get_secret(self, path: str, key: str) -> str:
        """Получить секрет из Vault."""
        response = self.client.secrets.kv.v2.read_secret_version(
            path=path
        )
        return response['data']['data'][key]

    def get_database_url(self, db_name: str) -> str:
        """Получить динамические credentials для БД."""
        creds = self.client.secrets.database.generate_credentials(
            name=db_name
        )
        return (
            f"postgresql://{creds['data']['username']}:"
            f"{creds['data']['password']}@db:5432/{db_name}"
        )

# Использование
vault = VaultClient(
    url=os.environ["VAULT_ADDR"],
    token=os.environ["VAULT_TOKEN"]
)
api_key = vault.get_secret("api-keys", "stripe")
db_url = vault.get_database_url("myapp")
```

### Пример 3: Pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  # Secrets detection
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # Security linting
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]

  # Dockerfile linting
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint

  # YAML security
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.33.0
    hooks:
      - id: yamllint

  # Terraform security
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_tfsec
```

### Пример 4: Security alerts notification

```yaml
# .github/workflows/security-alerts.yml
name: Security Alerts

on:
  schedule:
    - cron: '0 9 * * *'  # Ежедневно в 9:00

jobs:
  check-alerts:
    runs-on: ubuntu-latest
    steps:
      - name: Check Dependabot alerts
        uses: actions/github-script@v7
        with:
          script: |
            const alerts = await github.rest.dependabot.listAlertsForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              severity: 'critical,high'
            });

            if (alerts.data.length > 0) {
              const message = alerts.data.map(a =>
                `- ${a.security_advisory.summary} (${a.security_advisory.severity})`
              ).join('\n');

              // Отправить в Slack
              await fetch(process.env.SLACK_WEBHOOK, {
                method: 'POST',
                body: JSON.stringify({
                  text: `⚠️ Security Alerts:\n${message}`
                })
              });
            }
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_SECURITY_WEBHOOK }}
```

---

## Скиллы

Скиллы для работы с этой инструкцией:

| Скилл | Описание |
|-------|----------|
| — | Пока нет специализированных скиллов |

---

## FAQ / Troubleshooting

### Gitleaks нашёл ложный позитив — как исключить?

1. **Добавить в allowlist:**
   ```toml
   # .gitleaks.toml
   [allowlist]
   commits = ["abc123..."]  # конкретный коммит
   paths = ["test/fixtures/"]  # путь
   regexes = ["EXAMPLE_KEY"]  # паттерн
   ```

2. **Inline исключение:**
   ```python
   API_KEY = "test_key_12345"  # gitleaks:allow
   ```

3. **Для файла целиком:**
   ```toml
   [allowlist]
   paths = [".*test.*\\.py"]
   ```

### Semgrep слишком много findings — как приоритизировать?

1. **Фильтровать по severity:**
   ```bash
   semgrep --severity ERROR --config auto
   ```

2. **Использовать baseline:**
   ```bash
   # Создать baseline
   semgrep --config auto --json > baseline.json

   # Проверять только новые
   semgrep --config auto --baseline-commit HEAD~10
   ```

3. **Настроить правила проекта:**
   ```yaml
   # .semgrep.yml
   rules:
     - id: custom-rule
       severity: ERROR  # только критичные
   ```

### Как обновить зависимость с уязвимостью срочно?

```bash
# 1. Проверить уязвимость
npm audit
# или
pip-audit

# 2. Обновить конкретный пакет
npm update vulnerable-package
# или
pip install --upgrade vulnerable-package

# 3. Проверить совместимость
npm test
# или
pytest

# 4. Создать PR напрямую (bypass Dependabot)
git checkout -b security/fix-lodash-prototype-pollution
git add package-lock.json
git commit -m "security: fix CVE-2021-23337 in lodash (prototype pollution)"
git push origin security/fix-lodash-prototype-pollution
```

### Container scan блокирует билд — что делать?

1. **Проверить конкретную уязвимость:**
   ```bash
   trivy image --severity CRITICAL app:latest
   ```

2. **Обновить базовый образ:**
   ```dockerfile
   # Было
   FROM node:18-alpine

   # Стало (новая версия)
   FROM node:20-alpine
   ```

3. **Если fix недоступен — создать исключение:**
   ```yaml
   # .trivyignore
   # CVE-2023-44487: HTTP/2 Rapid Reset (no upstream fix yet)
   CVE-2023-44487
   ```

4. **Документировать риск:**
   ```
   ## Accepted Vulnerabilities

   | CVE | Package | Reason | Expiry |
   |-----|---------|--------|--------|
   | CVE-2023-44487 | nghttp2 | HTTP/2 Rapid Reset, mitigated by rate limiting | 2024-03-01 |
   | CVE-2024-21626 | runc | Container escape, no fix in alpine yet | 2024-04-15 |
   ```

### Как настроить security alerts в Slack?

```yaml
# .github/workflows/security-notify.yml
name: Security Notifications

on:
  # При создании security advisory
  repository_vulnerability_alert:
    types: [created]

  # При fail security checks
  workflow_run:
    workflows: ["Security"]
    types: [completed]

jobs:
  notify:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - name: Send Slack notification
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: ${{ secrets.SLACK_SECURITY_CHANNEL }}
          slack-message: |
            :warning: Security check failed
            Repo: ${{ github.repository }}
            Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

---

## Связанные инструкции

- [docker.md](docker.md) — Безопасность Docker образов
- [deployment.md](deployment.md) — Безопасный деплой
- [ci.md](../git/ci.md) — Security gates в CI
- [auth.md](../src/security/auth.md) — Аутентификация
