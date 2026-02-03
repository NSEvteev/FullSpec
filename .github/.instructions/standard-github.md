---
description: Общие правила работы с GitHub: naming, review, merge, git flow
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/README.md
---

# Стандарт GitHub

Версия стандарта: 1.0

Общие принципы работы с GitHub. Детали регламентируются специализированными стандартами.

**Полезные ссылки:**
- [Инструкции .github](./README.md)
- [Черновик GitHub Platform Research](/.claude/drafts/2026-02-03-github-platform-research.md) — исследование возможностей GitHub

---

## 1. Зона ответственности

Этот документ — **индекс** для навигации по специализированным стандартам.

**НЕ содержит:**
- Детальных правил (они в специализированных стандартах)
- Дублирования контента

---

## 2. SSOT-ссылки

| Область | SSOT-документ |
|---------|---------------|
| Issues | [standard-issue.md](./issues/standard-issue.md) |
| Pull Requests | [standard-pull-request.md](./pull-requests/standard-pull-request.md) |
| Labels | [standard-labels.md](./labels/standard-labels.md) |
| Milestones | [standard-milestone.md](./milestones/standard-milestone.md) |
| Releases | [standard-release.md](./releases/standard-release.md) |
| Issue Templates | [standard-issue-template.md](./issue-templates/standard-issue-template.md) |
| PR Template | [standard-pr-template.md](./pr-template/standard-pr-template.md) |
| Workflows | [standard-workflow-file.md](./workflows-files/standard-workflow-file.md) |
| CODEOWNERS | [standard-codeowners.md](./codeowners/standard-codeowners.md) |
| Development Workflow | [standard-development-workflow.md](./standard-development-workflow.md) |
| Release Workflow | [standard-release-workflow.md](./standard-release-workflow.md) |

---

## 3. Принципы

> **CLI-first.** Все операции через `gh` CLI.

> **Merge в main ≠ деплой.** Production — только через Release.

> **Прямые коммиты в main запрещены.** Только через PR.

> **Одна задача — один Issue — одна ветка — один PR.**

> **Squash Merge по умолчанию.** История main линейная.

---

## 4. CLI как основной инструмент

**SSOT команд:** см. специализированные стандарты выше.

**Основные команды:**

| Операция | Команда |
|----------|---------|
| **Issues** | `gh issue create`, `gh issue list`, `gh issue view`, `gh issue close` |
| **Pull Requests** | `gh pr create`, `gh pr list`, `gh pr view`, `gh pr merge` |
| **Releases** | `gh release create`, `gh release list`, `gh release view` |
| **Reviews** | `gh pr review --approve`, `gh pr review --request-changes` |
| **Labels** | `gh label create`, `gh label list`, `gh label edit` |
| **Workflows** | `gh workflow run`, `gh run list`, `gh run view` |

**Исключения (Web UI допустим):**
- Branch Protection Rules (сложная структура JSON)
- Первичная настройка репозитория (создание репо, секреты)

---

## 5. Branch Protection Rules

**Настройка:** через Web UI (Settings → Branches)

**Рекомендуемые правила для main:**

| Правило | Когда включать |
|---------|----------------|
| **Require PR before merge** | С первого дня (обязательно) |
| **Require status checks** | Когда настроен CI workflow |
| **Require approvals** | При росте команды (2+ разработчика) |

**Проверка через API:**
```bash
gh api repos/{owner}/{repo}/branches/main/protection
```

---

## 6. Типичные ошибки

| Ошибка | Решение |
|--------|---------|
| `error: failed to push some refs` | `git pull origin main` → разрешить конфликты → `git push` |
| `remote: error: GH006: Protected branch update failed` | Создать PR через `gh pr create` |
| `fatal: Not a valid object name: 'main'` | `git checkout main` |
