# Minimal Template

> **Источник:** [/.claude/instructions/docs/structure.md](/.claude/instructions/docs/structure.md#шаблон-минимальный)

Минимальный шаблон документации для простых файлов: утилиты, константы, хелперы.

---

## Шаблон

```markdown
# {Название}

> Исходный код: [{filename}](/{path})

{Описание}

## API

| Функция/Константа | Описание |
|-------------------|----------|
| `{name}` | {description} |
```

---

<!-- Пример заполнения

# String Utils

> Исходный код: [string-utils.ts](/src/shared/utils/string-utils.ts)

Утилиты для работы со строками: форматирование, валидация, преобразование.

## API

| Функция/Константа | Описание |
|-------------------|----------|
| `capitalize(str)` | Первая буква в верхний регистр |
| `truncate(str, length)` | Обрезать строку с добавлением "..." |
| `slugify(str)` | Преобразовать в URL-slug |
| `sanitizeHtml(str)` | Очистить HTML от опасных тегов |
| `MAX_TITLE_LENGTH` | Максимальная длина заголовка (100) |
| `EMAIL_REGEX` | Регулярное выражение для email |

-->
