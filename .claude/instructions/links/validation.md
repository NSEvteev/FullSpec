---
type: standard
description: Правила валидации ссылок в проекте
governed-by: links/README.md
related:
  - links/workflow.md
  - links/patterns.md
---

# Валидация ссылок

Правила проверки ссылок в markdown-документах.

**Индекс:** [/.claude/instructions/README.md](/.claude/instructions/README.md) | **Папка:** [links/README.md](./README.md)

## Оглавление

- [Типы ссылок](#типы-ссылок)
- [Правила проверки](#правила-проверки)
- [Режим --fix](#режим---fix)
- [Автоматизация](#автоматизация)
- [Скиллы](#скиллы)
- [Связанные инструкции](#связанные-инструкции)

---

## Типы ссылок

| Тип | Пример | Валидация |
|-----|--------|-----------|
| **Относительные** | `./file.md`, `../folder/` | Проверить от текущего файла |
| **Абсолютные** | `/path/to/file.md` | Проверить от корня проекта |
| **Якоря** | `#section`, `file.md#section` | Проверить заголовок |
| **Внешние** | `https://...` | Пропустить (не проверяем) |

---

## Правила проверки

### Относительные пути

```
./file.md     → текущая папка + file.md
../file.md    → родительская папка + file.md
```

**Проверка:** Разрешить путь относительно документа, проверить существование.

### Абсолютные пути

```
/path/to/file.md → корень проекта + path/to/file.md
```

**Проверка:** Путь от корня репозитория.

### Якоря

```
#section-name     → в текущем файле
file.md#section   → в другом файле
```

**Проверка:** Найти заголовок `## Section Name` (kebab-case slug).

### Внешние ссылки

```
https://example.com
http://localhost:3000
```

**Проверка:** Пропускаем. Требуют сетевых запросов, могут быть временно недоступны.

---

## Режим --fix

При вызове `/links-validate --fix`:

1. **Fuzzy match** — поиск похожих файлов
2. **Git history** — проверка переименований
3. **Предложения** — интерактивный выбор

**Пример:**
```
💡 Предложения по исправлению:

1. /.claude/skills/old-skill/SKILL.md:15
   Было: [test](./test.md)
   Предложение: [test](./tests.md)

Применить исправления? [Y/n/выборочно]
```

---

## Автоматизация

### CI-интеграция

```yaml
# .github/workflows/links.yml
jobs:
  validate-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate links
        run: claude /links-validate --json
```

### Pre-commit hook

```bash
# .git/hooks/pre-commit
claude /links-validate || exit 1
```

---

## Скиллы

| Скилл | Назначение |
|-------|------------|
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Валидация ссылок |
| [/health-check](/.claude/skills/health-check/SKILL.md) | Использует links-validate |

---

## Связанные инструкции

- [workflow.md](./workflow.md) — жизненный цикл ссылок
- [patterns.md](./patterns.md) — паттерны поиска
