---
title: CI/CD интеграция Captain Holt с GitHub Actions
type: feature
status: draft
created: 2026-02-01
related:
  - /.claude/agents/captain-holt/AGENT.md
---

# CI/CD интеграция Captain Holt

## Проблема

Анализ запускается вручную. Нет автоматической проверки при PR или коммите. Новые документы могут содержать неясные формулировки, которые попадут в main без проверки.

## Предлагаемое решение

### 1. GitHub Actions Workflow

```yaml
# .github/workflows/documentation-clarity.yml
name: Documentation Clarity Check

on:
  pull_request:
    paths:
      - '**/*.md'
      - '!.claude/drafts/**'  # Исключить черновики

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Для diff с main

      - name: Get changed markdown files
        id: changed
        run: |
          FILES=$(git diff --name-only origin/main...HEAD | grep '\.md$' | grep -v '.claude/drafts/' || true)
          echo "files=$FILES" >> $GITHUB_OUTPUT
          echo "count=$(echo "$FILES" | wc -w)" >> $GITHUB_OUTPUT

      - name: Setup Claude CLI
        if: steps.changed.outputs.count != '0'
        run: |
          # Установка Claude CLI (уточнить актуальный способ)
          npm install -g @anthropic-ai/claude-code

      - name: Run Captain Holt analysis
        if: steps.changed.outputs.count != '0'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          mkdir -p .claude/ci-reports
          for file in ${{ steps.changed.outputs.files }}; do
            echo "Analyzing: $file"
            claude --agent captain-holt "Проанализируй $file" > ".claude/ci-reports/$(basename $file .md)-analysis.md" || true
          done

      - name: Check for P1 issues
        if: steps.changed.outputs.count != '0'
        run: |
          P1_COUNT=$(grep -r "| P1 |" .claude/ci-reports/ | wc -l || echo "0")
          if [ "$P1_COUNT" -gt "0" ]; then
            echo "::error::Found $P1_COUNT critical (P1) documentation issues"
            cat .claude/ci-reports/*
            exit 1
          fi

      - name: Upload analysis reports
        if: always() && steps.changed.outputs.count != '0'
        uses: actions/upload-artifact@v4
        with:
          name: holt-analysis-reports
          path: .claude/ci-reports/
          retention-days: 30

      - name: Comment on PR
        if: steps.changed.outputs.count != '0'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const reports = fs.readdirSync('.claude/ci-reports/');
            let comment = '## Captain Holt Documentation Analysis\n\n';

            for (const report of reports) {
              const content = fs.readFileSync(`.claude/ci-reports/${report}`, 'utf8');
              // Извлечь только резюме
              const summary = content.match(/## Резюме[\s\S]*?(?=---)/);
              if (summary) {
                comment += `### ${report}\n${summary[0]}\n`;
              }
            }

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### 2. Конфигурация

**Secrets необходимые:**
- `ANTHROPIC_API_KEY` — API ключ для Claude

**Поведение:**
| Результат анализа | Действие |
|-------------------|----------|
| Нет P1 проблем | PR проходит, комментарий с резюме |
| Есть P1 проблемы | PR блокируется, требуется исправление |
| P2/P3 проблемы | PR проходит, комментарий с рекомендациями |

### 3. Исключения

Файлы, которые **не анализируются**:
- `.claude/drafts/**` — черновики
- `CHANGELOG.md` — автогенерируемый
- `node_modules/**` — зависимости

### 4. Интеграция с архивом анализов

После успешного мержа PR:
1. Анализы из `.claude/ci-reports/` копируются в архив
2. Обновляется статистика в `common-issues.json`

## Открытые вопросы

1. **Стоимость:** Сколько стоит анализ в CI? Нужен ли кэш?

2. **Скорость:** Как ускорить? Параллельный анализ нескольких файлов?

3. **Ложные срабатывания:** Как обрабатывать случаи, когда P1 проблема — false positive?

4. **Self-hosted runner:** Нужен ли для безопасности API ключа?

## Следующие шаги

- [ ] Создать `.github/workflows/documentation-clarity.yml`
- [ ] Добавить `ANTHROPIC_API_KEY` в secrets репозитория
- [ ] Протестировать на тестовом PR
- [ ] Настроить branch protection rule (require passing checks)
