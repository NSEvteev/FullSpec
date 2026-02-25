# Feature Freeze — технический блок через Branch Protection

Реализация Release Freeze как технического ограничения (не организационной меры): блокировка merge в main через GitHub API / Branch Protection Rules.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** standard-release.md § 9 описывает Release Freeze как организационную меру: "НЕ мержить PR". create-release.md Шаг 2: "LLM не может заблокировать merge технически. Freeze — организационная мера."
**Почему создан:** Организационный freeze ненадёжен — PR может быть смержен случайно. Технический блок через branch protection гарантирует freeze.
**Связанные файлы:**
- `/.github/.instructions/releases/standard-release.md` — § 9 Release Freeze
- `/.github/.instructions/releases/create-release.md` — Шаг 2 Release Freeze
- `/.github/.instructions/branches/standard-branching.md` — стандарт ветвления

## Содержание

### Текущее описание

```
Шаг 2: Release Freeze
LLM не может заблокировать merge технически.
Freeze — организационная мера. Ответственность на пользователе.
```

### Варианты технического блока

**Вариант A: GitHub Branch Protection Rules (API)**

```bash
# Включить freeze: required reviewers = 99 (практически блокирует merge)
gh api repos/{owner}/{repo}/branches/main/protection -X PUT \
  -f required_pull_request_reviews.required_approving_review_count=99

# Снять freeze: вернуть нормальное значение
gh api repos/{owner}/{repo}/branches/main/protection -X PUT \
  -f required_pull_request_reviews.required_approving_review_count=1
```

**Ограничение:** Требует GitHub Pro/Team/Enterprise для branch protection rules.

**Вариант B: GitHub Rulesets (современный подход)**

```bash
# Создать ruleset "release-freeze"
gh api repos/{owner}/{repo}/rulesets -X POST \
  --input ruleset-freeze.json

# Удалить после Release
gh api repos/{owner}/{repo}/rulesets/{id} -X DELETE
```

**Ограничение:** Rulesets доступны начиная с GitHub Free (с ограничениями) и GitHub Pro.

**Вариант C: Label-based блок**

- Добавить метку `release-freeze` на все открытые PR
- CI проверяет: если PR имеет метку `release-freeze` → fail (не merge)
- Исключение: PR с меткой `critical` проходит

```yaml
# В ci.yml
- name: Check release freeze
  if: contains(github.event.pull_request.labels.*.name, 'release-freeze')
  run: |
    echo "Release freeze active. Only critical PRs allowed."
    exit 1
```

**Преимущество:** Работает на GitHub Free. Не требует branch protection.

**Вариант D: Environment protection rules**

- Создать environment "production" с required reviewers
- deploy.yml использует environment → reviewer должен одобрить
- Не блокирует merge, но блокирует деплой

### Сравнение

| Вариант | GitHub Free | Блокирует merge | Исключения | Сложность |
|---------|------------|-----------------|------------|-----------|
| A: Branch Protection | Нет (Pro+) | Да | Через bypass | Средняя |
| B: Rulesets | Частично | Да | Через bypass | Средняя |
| C: Label + CI | Да | Да (через CI) | `critical` label | Низкая |
| D: Environment | Да | Нет (только деплой) | Через approval | Низкая |

## Решения

*Нет решений — нужно выбрать вариант.*

## Открытые вопросы

- Какой план GitHub используется? (Free / Pro / Team / Enterprise)
- Нужен ли настоящий merge-блок или достаточно CI-предупреждения?
- Должен ли freeze быть автоматическим (вызывается из /release-create) или ручным?
- Как обрабатывать hotfix во время freeze? (метка `critical` обходит блок?)
- Где описать: в standard-release.md § 9 или в отдельной инструкции?
