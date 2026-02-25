# Security Scan — трёхуровневая модель безопасности кода

Расширение стандарта безопасности: per-tech security файлы (`security-{tech}.md`), pre-release security gate, AI-assisted сканирование (Claude Code Security). Трёхуровневая модель: Automated → Gated → AI-assisted.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
  - [§ 1. AS IS — что уже есть](#-1-as-is--что-уже-есть)
  - [§ 2. Трёхуровневая модель безопасности](#-2-трёхуровневая-модель-безопасности)
  - [§ 3. Расширение standard-security.md — три новых секции](#-3-расширение-standard-securitymd--три-новых-секции)
  - [§ 4. Формат security-{tech}.md](#-4-формат-security-techmd)
  - [§ 5. Шаблон security-{tech}.md](#-5-шаблон-security-techmd)
  - [§ 6. Пример: security-python.md](#-6-пример-security-pythonmd)
  - [§ 7. Расширение create-technology.md — шаг 10](#-7-расширение-create-technologymd--шаг-10)
  - [§ 8. Расширение standard-technology.md](#-8-расширение-standard-technologymd)
  - [§ 9. Pre-release security gate (E009, E010)](#-9-pre-release-security-gate-e009-e010)
  - [§ 10. Pre-commit: gitleaks](#-10-pre-commit-gitleaks)
  - [§ 11. CI security job template](#-11-ci-security-job-template)
  - [§ 12. Claude Code Security (AI-assisted)](#-12-claude-code-security-ai-assisted)
  - [§ 13. Интеграция в процесс](#-13-интеграция-в-процесс)
- [Решения](#решения)
- [Закрытые вопросы](#закрытые-вопросы)
- [Задачи](#задачи)

---

## Контекст

**Задача:** Закрыть пробелы безопасности: нет per-tech security-инструментов (LLM не знает ЧЕМ сканировать), нет pre-release security gate (`validate-pre-release.py` → E001-E008 без security), нет локального secrets detection (только серверный GitHub Secret Scanning).

**Почему создан:** Release workflow не проверяет безопасность перед созданием релиза. Per-tech security-инструменты (Bandit, pip audit, npm audit) не описаны нигде — LLM-разработчик не знает какие инструменты использовать для конкретной технологии. Существующий `standard-security.md` покрывает только GitHub-платформу.

**Связанные файлы:**
- `.github/.instructions/actions/security/standard-security.md` — существующий стандарт (§§ 1-10: Dependabot, CodeQL, Secret Scanning, SECURITY.md)
- `.github/.instructions/actions/security/validation-security.md` — SEC001-SEC010
- `.github/.instructions/.scripts/validate-pre-release.py` — E001-E008 (нет security check)
- `.github/.instructions/.scripts/validate-security.py` — pre-commit хук для файлов безопасности
- `specs/.instructions/docs/technology/standard-technology.md` — формат per-tech стандартов (8 секций)
- `specs/.instructions/docs/technology/create-technology.md` — воркфлоу создания per-tech (9 шагов)
- `.pre-commit-config.yaml` — 26 хуков, нет secrets detection

---

## Содержание

### § 1. AS IS — что уже есть

| Компонент | Файл | Покрывает | НЕ покрывает |
|-----------|------|-----------|-------------|
| standard-security.md | `.github/.instructions/actions/security/` | Dependabot, CodeQL, Secret Scanning, SECURITY.md | Per-tech инструменты, pre-release gate, AI-scanning |
| validate-security.py | `.github/.instructions/.scripts/` | SEC001-SEC010 (формат конфиг-файлов) | Проверка alerts, runtime сканирование |
| validate-pre-release.py | `.github/.instructions/.scripts/` | E001-E008 (main sync, tests, milestone) | Security alerts, уязвимости зависимостей |
| codeql.yml | `.github/workflows/` | SAST на уровне GitHub (push + PR + weekly) | Локальные per-tech SAST-линтеры |
| dependabot.yml | `.github/` | Автообновление зависимостей, алерты | Локальный `pip audit` / `npm audit` |
| .pre-commit-config.yaml | корень | 26 хуков валидации документов | Secrets detection (gitleaks/detect-secrets) |
| Secret Scanning | GitHub Settings | Серверное обнаружение секретов при push | Локальное обнаружение ДО коммита |

**Пробелы:**
1. Нет per-tech security-файлов — LLM не знает ЧЕМ сканировать конкретную технологию
2. Нет pre-release security gate — `validate-pre-release.py` не проверяет Dependabot alerts
3. Нет локального secrets detection — только серверный GitHub Secret Scanning
4. Нет AI-assisted уровня — Claude Code Security не документирован

---

### § 2. Трёхуровневая модель безопасности

```
┌─────────────────────────────────────────────────────────┐
│ Level 1: AUTOMATED (каждый commit/push/PR)              │
│  ├── Pre-commit: gitleaks (секреты в diff)              │
│  ├── CI: CodeQL (SAST — GitHub-native)                  │
│  ├── CI: per-tech security jobs (из security-{tech}.md) │
│  └── GitHub: Dependabot alerts + Secret Scanning        │
├─────────────────────────────────────────────────────────┤
│ Level 2: GATED (перед релизом, блокирующий)             │
│  ├── validate-pre-release.py E009: Dependabot alerts    │
│  ├── validate-pre-release.py E010: open security issues │
│  └── Per-tech: dependency audit (pip audit / npm audit) │
├─────────────────────────────────────────────────────────┤
│ Level 3: AI-ASSISTED (рекомендуемый, по решению)        │
│  ├── Claude Code Security (семантический анализ)        │
│  └── Ручной security review (OWASP Top 10 чек-лист)    │
└─────────────────────────────────────────────────────────┘
```

| Уровень | Когда запускается | Что блокирует | Кто запускает |
|---------|-------------------|---------------|---------------|
| Level 1: Automated | Каждый commit (pre-commit), push/PR (CI) | Merge (CI failure) | Автоматически |
| Level 2: Gated | Перед созданием Release | Release creation | `/release-create` → `validate-pre-release.py` |
| Level 3: AI-assisted | Перед релизом, при аудите, при добавлении auth/payment | Ничего (рекомендация) | Разработчик вручную |

**Принцип:** Level 1 + Level 2 обязательны и автоматизированы. Level 3 — рекомендация, не блокирует процесс.

---

### § 3. Расширение standard-security.md — три новых секции

Добавить в существующий `.github/.instructions/actions/security/standard-security.md` (после текущего § 10) три новых секции.

#### Новый § 11. Per-tech Security Scanning

Содержание секции:

```markdown
## 11. Per-tech Security Scanning

Для каждой технологии из Tech Stack, у которой есть package manager или SAST-инструменты,
создаётся файл `security-{tech}.md` с описанием инструментов безопасности.

**Расположение:**

    specs/docs/.technologies/security-{tech}.md

**Формат:** 5 обязательных секций (см. standard-technology.md).

**Создание:** Файл создаётся вместе с `standard-{tech}.md` при выполнении
create-technology.md (шаг 10).

**Когда создавать:**

| Условие | Пример | security-{tech}.md |
|---------|--------|-------------------|
| Язык/runtime с package manager | Python, JavaScript, Go | Да |
| Контейнерная технология | Docker | Да |
| СУБД, кэш, очередь | PostgreSQL, Redis, RabbitMQ | Нет |
| CSS/UI framework | Tailwind CSS | Нет |
| Инфраструктурная утилита | Nginx, Terraform | По ситуации |

**Связь с GitHub Security (§§ 3-5):**

| GitHub Security (платформа) | Per-tech Security (локально + CI) |
|-----------------------------|-----------------------------------|
| CodeQL — SAST на уровне GitHub | Per-tech SAST дополняет (глубже, специфичнее) |
| Dependabot — автообновление зависимостей | dependency audit проверяет уязвимости локально |
| Secret Scanning — серверное обнаружение | gitleaks — локальное обнаружение до push |

Per-tech НЕ заменяет GitHub Security — они дополняют друг друга.
GitHub Security = базовый слой (всегда включён).
Per-tech = глубокий слой (специфичный для стека).
```

#### Новый § 12. Pre-release Security Gate

Содержание секции:

```markdown
## 12. Pre-release Security Gate

Перед созданием Release обязательна проверка безопасности в validate-pre-release.py:

| Код | Проверка | Severity | Блокирует |
|-----|----------|----------|-----------|
| E009 | Нет open Dependabot alerts с severity critical/high | critical, high | Да |
| E010 | Нет open Issues с меткой `security` | any | Да |

**Допустимые исключения:**

| Ситуация | Как пропустить |
|----------|---------------|
| Alert помечен `dismissed` с причиной `tolerable_risk` | Не считается open |
| Issue помечен `security` + `wont-fix` | Не считается open |
| Medium/low severity alerts | НЕ блокируют (только warning) |

**Команды проверки:**

    # E009: Critical/High Dependabot alerts
    gh api repos/{owner}/{repo}/dependabot/alerts \
      --jq '[.[] | select(.state=="open")
        | select(.security_advisory.severity=="critical"
          or .security_advisory.severity=="high")] | length'

    # E010: Open security issues
    gh issue list --label security --state open --json number --jq 'length'
```

#### Новый § 13. AI-assisted Security Scanning

Содержание секции:

```markdown
## 13. AI-assisted Security Scanning

Claude Code Security — встроенная функция Claude Code для семантического
анализа кода на уязвимости (research preview, Enterprise/Team).

**Когда использовать (рекомендация):**
- Перед релизом (особенно major)
- При security аудите
- После добавления auth / payment / PII модулей
- При изменении модели авторизации

**Что даёт сверх CodeQL (§ 4):**
- Анализ бизнес-логики (authorization bypass, IDOR)
- Контекстный анализ потоков данных между сервисами
- Мульти-этапная верификация (снижает false positives)
- Предложение конкретных патчей для ревью

**Ограничения:**
- Research preview — API и возможности могут измениться
- Только Enterprise/Team клиенты
- Не автоматизируется в CI — запуск вручную через Claude Code
- Ничего не применяет без одобрения человека

**Альтернатива без Enterprise/Team:**
Ручной security review по OWASP Top 10 чек-листу перед релизом.
```

---

### § 4. Формат security-{tech}.md

Файл `security-{tech}.md` — companion к `standard-{tech}.md`. Описывает инструменты и конфигурацию безопасности для конкретной технологии.

**Расположение:**
```
specs/docs/.technologies/security-{tech}.md
```

**Именование:** `{tech}` совпадает с `{tech}` в `standard-{tech}.md` (kebab-case).

**Frontmatter:**
```yaml
---
description: Security scanning {Technology} — dependency audit, SAST, конфигурация.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: {tech}
type: security
---
```

Поле `type: security` отличает от `standard-{tech}.md` (у которого нет поля `type`).

**5 обязательных h2-секций:**

| # | Секция | Содержание | Формат |
|---|--------|-----------|--------|
| 1 | Инструменты | Список security-инструментов для технологии | Таблица: инструмент, версия, категория (dependency/SAST/secrets), назначение |
| 2 | Dependency Audit | Команда запуска, severity-модель, формат вывода | Code-блок с командой + таблица severity |
| 3 | SAST | Инструмент, конфигурация, ключевые правила | Code-блок с конфигом + таблица правил |
| 4 | CI Integration | Фрагмент job для CI workflow | YAML code-блок (steps для GitHub Actions) |
| 5 | Known Exceptions | Suppressed правила с обоснованием | Таблица: rule ID, причина, дата review |

**Когда секция не применима:** stub-текст в курсиве: `*{Секция} не применимо — {причина}.*`

Пример: для Docker нет dependency audit → `*Dependency Audit не применимо — Docker images не имеют package manager. Уязвимости образов проверяются через Trivy (см. SAST).*`

---

### § 5. Шаблон security-{tech}.md

`````markdown
---
description: Security scanning {Technology} — dependency audit, SAST, конфигурация.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: {tech}
type: security
---

# Security {Technology}

## Инструменты

| Инструмент | Версия | Категория | Назначение |
|-----------|--------|-----------|-----------|
| {tool1} | {ver} | dependency audit | {что проверяет} |
| {tool2} | {ver} | SAST | {что проверяет} |

## Dependency Audit

<!-- Если применимо: -->

**Команда:**
```bash
{команда dependency audit}
```

**Severity-модель:**

| Severity | Действие | Блокирует CI | Блокирует Release |
|----------|----------|-------------|------------------|
| critical | Исправить немедленно | Да | Да |
| high | Исправить до релиза | Да | Да |
| medium | Исправить в следующем спринте | Нет (warning) | Нет |
| low | Backlog | Нет | Нет |

<!-- Если не применимо: -->
<!-- *Dependency Audit не применимо — {причина}.* -->

## SAST

<!-- Если применимо: -->

**Инструмент:** {tool} {version}

**Конфигурация:**
```{format}
{содержимое конфига}
```

**Ключевые правила:**

| Rule ID | Что проверяет | Severity |
|---------|--------------|----------|
| {id} | {описание} | {high/medium/low} |

<!-- Если не применимо: -->
<!-- *SAST не применимо — {причина}.* -->

## CI Integration

```yaml
# Фрагмент для .github/workflows/ci.yml
{tech}-security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: {step description}
      run: {command}
```

## Known Exceptions

<!-- Если есть suppressed правила: -->

| Rule ID | Причина suppression | Дата review |
|---------|-------------------|-------------|
| {id} | {обоснование} | {YYYY-MM-DD} |

<!-- Если нет исключений: -->
<!-- *Нет suppressed правил.* -->
`````

---

### § 6. Пример: security-python.md

`````markdown
---
description: Security scanning Python — pip audit, Bandit, safety. Dependency audit и SAST.
standard: specs/.instructions/docs/technology/standard-technology.md
technology: python
type: security
---

# Security Python

## Инструменты

| Инструмент | Версия | Категория | Назначение |
|-----------|--------|-----------|-----------|
| pip-audit | 2.7+ | dependency audit | Проверка PyPI-зависимостей по OSV database |
| Bandit | 1.7+ | SAST | Статический анализ Python-кода на уязвимости |
| safety | 3.0+ | dependency audit | Альтернативная проверка (Safety DB, шире чем OSV) |

## Dependency Audit

**Команда:**
```bash
# Основной инструмент (OSV database — открытая, бесплатная)
pip-audit -r src/{svc}/requirements.txt --format json

# Альтернатива (Safety DB — требует API key для commercial)
safety check -r src/{svc}/requirements.txt --json
```

**Severity-модель:**

| Severity | Действие | Блокирует CI | Блокирует Release |
|----------|----------|-------------|------------------|
| critical | Исправить немедленно | Да | Да (E009) |
| high | Исправить до релиза | Да | Да (E009) |
| medium | Исправить в следующем спринте | Нет (warning) | Нет |
| low | Backlog | Нет | Нет |

**Вывод:** При обнаружении critical/high — CI job падает. Вывод содержит: package, installed version, fixed version, CVE ID.

## SAST

**Инструмент:** Bandit 1.7+

**Конфигурация** (`pyproject.toml`):
```toml
[tool.bandit]
exclude_dirs = ["tests", "migrations"]
skips = []
# severity: LOW, MEDIUM, HIGH
# confidence: LOW, MEDIUM, HIGH
```

**Ключевые правила:**

| Rule ID | Что проверяет | Severity |
|---------|--------------|----------|
| B101 | assert в production коде | low |
| B103 | set_bad_file_permissions (chmod 777) | high |
| B105 | Hardcoded password в коде | high |
| B108 | Hardcoded /tmp path | medium |
| B301 | Использование pickle (deserialization attack) | high |
| B303 | Использование MD5/SHA1 для security | high |
| B608 | SQL injection через string formatting | high |
| B602 | subprocess с shell=True | high |

**Команда:**
```bash
bandit -r src/{svc}/ -f json --severity-level medium
```

## CI Integration

```yaml
# Фрагмент для .github/workflows/ci.yml
python-security:
  runs-on: ubuntu-latest
  needs: [test]
  steps:
    - uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"

    - name: Install security tools
      run: pip install pip-audit bandit

    - name: Dependency Audit
      run: |
        for req in src/*/requirements.txt; do
          echo "=== Checking $req ==="
          pip-audit -r "$req" --format json --desc || exit 1
        done

    - name: SAST (Bandit)
      run: bandit -r src/ -f json --severity-level medium --exit-zero
      # --exit-zero: не падать, результаты в SARIF для Code Scanning
```

## Known Exceptions

*Нет suppressed правил.*
`````

---

### § 7. Расширение create-technology.md — шаг 10

Добавить **Шаг 10** после текущего Шага 9 (Отчёт) в `create-technology.md`.

**Шаг 10: Создать security-{tech}.md (если применимо)**

```markdown
### Шаг 10: Создать security-{tech}.md (если применимо)

Определить, нужен ли security-файл для технологии:

| Условие | Пример | Создавать |
|---------|--------|-----------|
| Язык/runtime с package manager | Python, JavaScript, Go, Java | Да |
| Контейнерная технология | Docker | Да |
| СУБД, кэш, очередь | PostgreSQL, Redis, RabbitMQ | Нет |
| CSS/UI framework | Tailwind CSS, Bootstrap | Нет |
| Инфраструктурная утилита | Nginx | Нет |
| IaC с provider registry | Terraform | Да |

**Если Да:**
1. Скопировать шаблон security-{tech}.md (см. standard-technology.md)
2. Заполнить frontmatter (`type: security`)
3. Заполнить 5 секций:

| Секция | Источник данных |
|--------|----------------|
| Инструменты | Официальные security-инструменты технологии |
| Dependency Audit | Package manager audit command |
| SAST | Официальный или de-facto SAST для языка |
| CI Integration | GitHub Actions steps для инструментов выше |
| Known Exceptions | Пусто при создании |

4. Зарегистрировать в `specs/docs/README.md` (таблица + дерево)

**Если Нет:** Шаг пропускается. В отчёте указать: `📎 security-{tech}.md: не создан — {причина}`.
```

**Обновление чек-листа create-technology.md:**

Добавить в конец чек-листа:
```markdown
- [ ] security-{tech}.md создан (если технология имеет package manager / SAST)
- [ ] security-{tech}.md: frontmatter содержит `type: security`
- [ ] security-{tech}.md: 5 секций заполнены / stub
- [ ] security-{tech}.md зарегистрирован в docs/README.md
```

**Обновление отчёта (Шаг 9):**

Добавить в шаблон отчёта:
```markdown
### Security
- 📎 `security-{tech}.md`: {создан / не создан — причина}
- Инструменты: {список}
```

---

### § 8. Расширение standard-technology.md

Добавить в `standard-technology.md` новую секцию после текущего § 10 (Пример):

```markdown
## 11. Companion: security-{tech}.md

Для технологий с package manager или SAST-инструментами создаётся companion-файл
`security-{tech}.md` — описание инструментов безопасности.

**Расположение:**

    specs/docs/.technologies/security-{tech}.md

**Формат:** 5 обязательных h2-секций:

| # | Секция | Содержание |
|---|--------|-----------|
| 1 | Инструменты | Таблица инструментов |
| 2 | Dependency Audit | Команда + severity-модель |
| 3 | SAST | Конфигурация + правила |
| 4 | CI Integration | GitHub Actions job fragment |
| 5 | Known Exceptions | Suppressed правила |

**Frontmatter:** Содержит `type: security` (отличает от `standard-{tech}.md`).

**Шаблон:** См. [standard-security.md § 11](/.github/.instructions/actions/security/standard-security.md#11-per-tech-security-scanning).

**Когда создавать:** Вместе с `standard-{tech}.md` при /technology-create.
Критерий: технология имеет package manager (pip, npm, go mod) или SAST-инструмент.
```

---

### § 9. Pre-release security gate (E009, E010)

Расширить `validate-pre-release.py` двумя новыми проверками.

**Текущие коды:** E001-E008 (main sync, critical PR, tests, milestone, working tree, branch).

**Новые коды:**

| Код | Проверка | Команда | Блокирует |
|-----|----------|---------|-----------|
| E009 | Нет open Dependabot alerts severity critical/high | `gh api repos/{o}/{r}/dependabot/alerts` | Да |
| E010 | Нет open Issues с меткой `security` | `gh issue list --label security` | Да |

**Добавить в `ERROR_CODES`:**
```python
ERROR_CODES = {
    # ... E001-E008 ...
    "E009": "Есть open Dependabot alerts (critical/high)",
    "E010": "Есть open Issues с меткой security",
}
```

**Функция E009:**
```python
def check_dependabot_alerts() -> list[str]:
    """E009: Проверить Dependabot alerts (critical/high)."""
    result = run_cmd([
        "gh", "api", f"repos/:owner/:repo/dependabot/alerts",
        "--jq", '[.[] | select(.state=="open") | select(.security_advisory.severity=="critical" or .security_advisory.severity=="high")] | length'
    ])
    if result.returncode != 0:
        # API недоступен (нет прав, не настроен) — warning, не ошибка
        return []
    count = int(result.stdout.strip() or "0")
    if count > 0:
        return [f"E009: {count} open Dependabot alert(s) с severity critical/high"]
    return []
```

**Функция E010:**
```python
def check_security_issues() -> list[str]:
    """E010: Проверить open Issues с меткой security."""
    result = run_cmd([
        "gh", "issue", "list", "--label", "security",
        "--state", "open", "--json", "number", "--jq", "length"
    ])
    if result.returncode != 0:
        return []
    count = int(result.stdout.strip() or "0")
    if count > 0:
        return [f"E010: {count} open Issue(s) с меткой security"]
    return []
```

**Graceful degradation:** Если `gh api` возвращает ошибку (нет прав, Dependabot не настроен) — warning, не блокировка. Это критично для шаблона, где Dependabot может быть не включён.

---

### § 10. Pre-commit: gitleaks

Добавить gitleaks в `.pre-commit-config.yaml` как хук #27.

**Почему gitleaks:**

| Критерий | gitleaks | detect-secrets (Yelp) |
|----------|----------|----------------------|
| Установка | Single binary (Go) | pip install |
| Скорость | Быстрый (Go, скан diff) | Медленнее (Python) |
| Patterns | 700+ встроенных | Требует baseline файл |
| Pre-commit | Нативная поддержка | Требует wrapper |
| Поддержка | Активная (2025+) | Редкие обновления |
| CI Integration | GitHub Action есть | Нет официального Action |

**Конфигурация в `.pre-commit-config.yaml`:**
```yaml
  # 27. Обнаружение секретов (gitleaks)
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
        name: Detect secrets (gitleaks)
        stages: [pre-commit]
```

**Что проверяет:** Только staged diff (не всю историю). Ищет:
- API keys (AWS, GCP, Azure, Stripe, etc.)
- Tokens (GitHub, GitLab, Slack, etc.)
- Private keys (RSA, SSH, PGP)
- Passwords в конфигах
- Connection strings с credentials

**Suppression (false positives):**

Файл `.gitleaks.toml` в корне проекта:
```toml
[allowlist]
description = "Project-level allowlist"

# Пример: тестовые/фиктивные значения
[[allowlist.regexTarget]]
target = "match"
regexes = [
  '''EXAMPLE_KEY_[A-Z]+''',
]

# Пример: конкретный файл
[[allowlist.paths]]
paths = [
  '''\.env\.example''',
  '''.*test.*\.py''',
]
```

---

### § 11. CI security job template

Шаблон security job для CI workflow. Читает `security-{tech}.md` — конкретные шаги зависят от tech stack проекта.

**Подход:** Вместо одного монолитного security job — отдельный job на каждую технологию (параллельное выполнение).

**Шаблон в `platform/.github/templates/`:**
```yaml
# Template: security job per technology
# Генерируется /init-project на основе security-{tech}.md

security-{tech}:
  runs-on: ubuntu-latest
  needs: [build]
  steps:
    - uses: actions/checkout@v4
    # Steps из security-{tech}.md § CI Integration
```

**Пример итогового ci.yml (для Python + JS проекта):**
```yaml
jobs:
  # ... build, test ...

  security-python:
    runs-on: ubuntu-latest
    needs: [test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install pip-audit bandit
      - run: |
          for req in src/*/requirements.txt; do
            pip-audit -r "$req" || exit 1
          done
      - run: bandit -r src/ --severity-level medium

  security-javascript:
    runs-on: ubuntu-latest
    needs: [test]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: |
          for pkg in src/*/package.json; do
            cd "$(dirname "$pkg")"
            npm audit --audit-level=high
            cd -
          done

  # gitleaks (universal, не зависит от tech stack)
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

### § 12. Claude Code Security (AI-assisted)

**Что это:** Встроенная функция Claude Code (research preview, Enterprise/Team) для семантического анализа кода на уязвимости. Не rule-based SAST, а контекстный анализ — понимает бизнес-логику, потоки данных, взаимодействие компонентов.

**Чем отличается от CodeQL (Level 1):**

| Аспект | CodeQL (Level 1) | Claude Code Security (Level 3) |
|--------|-----------------|-------------------------------|
| Подход | Rule-based, pattern matching | Семантический, контекстный |
| Что находит | Известные паттерны (SQLi, XSS, path traversal) | Бизнес-логика (authz bypass, IDOR, race conditions) |
| False positives | Много (нет понимания контекста) | Мало (мульти-этапная верификация) |
| Автоматизация | Полная (CI workflow) | Нет (ручной запуск) |
| Результат | Alert list | Alert + предложенный патч |

**Когда запускать (рекомендация):**
- Перед major-релизом
- После добавления auth / payment / PII модулей
- При изменении модели авторизации (RBAC, ownership checks)
- При security аудите (по расписанию или по запросу)

**Документирование в процессе:**

В `standard-security.md § 13` зафиксировать как рекомендуемый шаг. В `/release-create` добавить напоминание: "Рекомендуется запустить Claude Code Security перед major-релизом".

Не блокирует процесс — это осознанное решение: tool в preview, не у всех есть доступ, не автоматизируется.

---

### § 13. Интеграция в процесс

**Где security встраивается в standard-process.md:**

| Фаза процесса | Security action | Level |
|----------------|----------------|-------|
| Phase 0: Init | Настроить GitHub Security (standard-security.md §§ 3-5, 7) | Setup |
| Phase 0: Init | Создать security-{tech}.md вместе с standard-{tech}.md | Setup |
| Development | Pre-commit: gitleaks (каждый коммит) | 1 |
| Development | CI: CodeQL + per-tech security jobs (каждый PR) | 1 |
| Pre-release | validate-pre-release.py E009, E010 | 2 |
| Pre-release | Claude Code Security (рекомендация) | 3 |
| Post-release | Dependabot alerts мониторинг | 1 |

**Обновление standard-process.md:**

В § 8 (Tool summary) добавить строку:
```
| Security scanning | standard-security.md + security-{tech}.md | Level 1-3 security model |
```

В § 10 (Gaps) — этот gap будет закрыт при реализации данного черновика.

---

## Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| R1 | Расширить existing `standard-security.md` (§§ 11-13), а не создавать новый стандарт | Единая точка входа для всего security. Избегаем дублирования — GitHub Security и per-tech в одном документе. |
| R2 | `security-{tech}.md` как отдельный companion-файл, а не секция внутри `standard-{tech}.md` | Разделение ответственности: coding conventions ≠ security scanning. CI может glob-ить `security-*.md` без парсинга `standard-*.md`. |
| R3 | Трёхуровневая модель: Automated → Gated → AI-assisted | Level 1 ловит 90% проблем автоматически. Level 2 — last gate перед релизом. Level 3 — deep analysis по решению человека. |
| R4 | gitleaks для pre-commit secrets detection (не detect-secrets) | Быстрее (Go binary), 700+ patterns из коробки, нативная поддержка pre-commit, активная поддержка, GitHub Action для CI. |
| R5 | 5 секций в security-{tech}.md (не 8 как в standard-{tech}.md) | Security scanning проще чем coding conventions. 5 секций покрывают: что (инструменты), зачем (dependency + SAST), как (CI), исключения. |
| R6 | security-{tech}.md только для технологий с package manager и/или SAST | PostgreSQL, Redis, Tailwind не имеют собственных security-инструментов — security покрывается через язык (Python → Bandit проверяет SQL injection). |
| R7 | Claude Code Security как Level 3 (рекомендуемый, не обязательный) | Research preview, только Enterprise/Team, не автоматизируется в CI. Нельзя строить обязательный процесс на preview-фиче. |
| R8 | E009/E010 блокируют только critical/high (medium/low — warning) | Medium/low уязвимости не должны блокировать релиз — это парализует процесс. Critical/high = реальный риск. |
| R9 | security-{tech}.md создаётся при `/technology-create` (шаг 10), не при `/init-project` | Следует существующему паттерну: per-tech файлы создаются при добавлении технологии, не при инициализации проекта. |
| R10 | Не создавать отдельный скилл `/security-scan` | Security встроен в существующие шаги: pre-commit (gitleaks), CI (jobs), pre-release (validate-pre-release.py). Отдельный скилл = лишняя абстракция. |

---

## Закрытые вопросы

| # | Вопрос | Ответ |
|---|--------|-------|
| Q1 | Отдельный стандарт или расширение existing? | Расширение existing `standard-security.md` тремя секциями (R1). Один документ = одна точка входа для security. |
| Q2 | Какой инструмент для secrets detection? | gitleaks (R4). Go binary, 700+ patterns, нативный pre-commit, активная поддержка. |
| Q3 | Блокировать ли merge/release при security issues? | Level 1 (CI) блокирует merge. Level 2 (pre-release) блокирует release. Только critical/high (R8). |
| Q4 | Нужен ли отдельный скилл `/security-scan`? | Нет (R10). Security встроен в существующие шаги процесса. |
| Q5 | Как обрабатывать false positives? | Known Exceptions секция в `security-{tech}.md` + `.gitleaks.toml` для pre-commit + `dismissed` с причиной для Dependabot. |

---

## Tasklist

Задачи для исполнения через TaskCreate. Порядок строгий — зависимости указаны в blockedBy.

```
TASK 1: Расширить standard-security.md
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (секция "§ 3")
    Добавить §§ 11-13 в .github/.instructions/actions/security/standard-security.md:
    § 11 Per-tech security scanning (security-{tech}.md формат, 5 секций,
    companion к standard-{tech}.md),
    § 12 Pre-release security gate (E009 Dependabot alerts, E010 security Issues),
    § 13 AI-assisted security (Claude Code Security, рекомендация не обязательство).
  activeForm: Расширяю standard-security.md

TASK 2: Расширить standard-technology.md
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (секция "§ 8")
    Добавить § 11 (companion security-{tech}.md) в
    specs/.instructions/docs/technology/standard-technology.md.
    Расположение: specs/docs/.technologies/security-{tech}.md.
    Формат: 5 h2-секций (Инструменты, Dependency Audit, SAST, CI Integration, Known Exceptions).
    Frontmatter: type: security. Шаблон включить в секцию.
    Когда создавать: вместе с standard-{tech}.md при /technology-create.
  activeForm: Расширяю standard-technology.md

TASK 3: Расширить create-technology.md
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (секция "§ 7")
    Добавить Шаг 10 (создание security-{tech}.md) в
    specs/.instructions/docs/technology/create-technology.md.
    Условие: технология имеет package manager (pip, npm, go mod) или SAST-инструмент.
    Если нет — шаг пропускается, в отчёте указать причину.
    Обновить чек-лист (4 пункта) и шаблон отчёта (секция Security).
  activeForm: Расширяю create-technology.md

TASK 4: Обновить validation-security.md
  blockedBy: [1]
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (задача 4)
    Добавить коды SEC011-SEC013 в
    .github/.instructions/actions/security/validation-security.md:
    SEC011: security-{tech}.md существует для каждой технологии с package manager,
    SEC012: security-{tech}.md содержит 5 обязательных h2-секций,
    SEC013: security-{tech}.md frontmatter содержит type: security.
  activeForm: Обновляю validation-security.md

TASK 5: Обновить validate-pre-release.py
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (секция "§ 9")
    Добавить E009 и E010 в .github/.instructions/.scripts/validate-pre-release.py.
    E009: gh api repos/:owner/:repo/dependabot/alerts — нет open critical/high.
    E010: gh issue list --label security --state open — нет open Issues.
    Graceful degradation: если gh api возвращает ошибку (нет прав, Dependabot не настроен)
    — warning, не блокировка. Критично для шаблона без настроенного Dependabot.
  activeForm: Обновляю validate-pre-release.py

TASK 6: Добавить gitleaks в .pre-commit-config.yaml
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (секция "§ 10")
    Добавить хук #27 в .pre-commit-config.yaml:
    repo: https://github.com/gitleaks/gitleaks, rev: v8.21.2, id: gitleaks,
    stages: [pre-commit].
    Создать .gitleaks.toml в корне проекта с базовым allowlist
    (EXAMPLE_KEY, .env.example, *test*.py).
  activeForm: Добавляю gitleaks

TASK 7: Обновить validation-technology.md
  blockedBy: [2]
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (задача 7)
    Добавить валидацию security-{tech}.md в
    specs/.instructions/docs/technology/validation-technology.md.
    Новые коды: TECH-SEC001 (frontmatter type: security),
    TECH-SEC002 (5 обязательных h2-секций), TECH-SEC003 (naming security-{tech}.md).
  activeForm: Обновляю validation-technology.md

TASK 8: Обновить validate-docs-technology.py
  blockedBy: [7]
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (задача 8)
    Реализовать проверки TECH-SEC001-003 в
    specs/.instructions/.scripts/validate-docs-technology.py.
    Скрипт уже валидирует standard-{tech}.md — расширить для security-{tech}.md.
    TECH-SEC001: frontmatter type == security.
    TECH-SEC002: 5 h2-секций (Инструменты, Dependency Audit, SAST, CI Integration, Known Exceptions).
    TECH-SEC003: файл называется security-{tech}.md (не standard-).
  activeForm: Обновляю validate-docs-technology.py

TASK 9: Обновить docs/README.md
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (задача 9)
    Добавить секцию security-{tech}.md в specs/docs/README.md:
    - Таблица: security-{tech}.md как companion к standard-{tech}.md
    - Дерево: .technologies/security-{tech}.md
  activeForm: Обновляю docs/README.md

TASK 10: Обновить standard-process.md
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (секция "§ 13")
    Обновить specs/.instructions/standard-process.md:
    - § 8 (Tool summary): добавить строку Security scanning
      (standard-security.md + security-{tech}.md, Level 1-3 security model)
    - § 10 (Gaps): закрыть соответствующий gap
  activeForm: Обновляю standard-process.md

TASK 11: Добавить pre-commit хук для security-{tech}.md
  blockedBy: [8]
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (задача 11)
    Добавить хук в .pre-commit-config.yaml:
    - Триггер: ^specs/docs/\.technologies/security-.*\.md$
    - Entry: validate-docs-technology.py (расширенный в задаче 8)
  activeForm: Добавляю pre-commit хук security-tech

TASK 12: Обновить .structure/pre-commit.md
  blockedBy: [6, 11]
  description: >
    Драфт: .claude/drafts/2026-02-25-security-scan.md (задача 12)
    Синхронизировать таблицу "Активные хуки" в .structure/pre-commit.md:
    - Добавить строку #27: gitleaks — "Обнаружение секретов в staged diff"
    - Добавить строку #28: security-technology-validate — "Формат security-{tech}.md"
  activeForm: Обновляю pre-commit.md
```
