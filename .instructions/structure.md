# Структура инструкций

Правила расположения инструкций в проекте.

---

## Основная концепция

**Инструкции = ТОЛЬКО стандарты (КАК делать).**

Они НЕ описывают структуру папок — это делает README.

---

## Расположение инструкций

### Централизованные

| Область | Путь |
|---------|------|
| Как писать инструкции | `/.instructions/` |
| Как писать скиллы | `/.claude/.instructions/skills/` |
| Как писать specs | `/specs/.instructions/` |

### Локальные (будущие)

| Папка проекта | Локальные инструкции |
|---------------|---------------------|
| `/.structure/` | `/.structure/.instructions/` |
| `/src/` | `/src/.instructions/` |
| `/platform/` | `/platform/.instructions/` |
| `/tests/` | `/tests/.instructions/` |
| `/shared/` | `/shared/.instructions/` |
| `/config/` | `/config/.instructions/` |
| `/.github/` | `/.github/.instructions/` |

> **Покрытие:** [/.instructions/coverage.md](./coverage.md)

---

## Примеры

### Инструкция для API (будущее)

```
/src/.instructions/api/design.md
```

### Инструкция для скиллов

```
/.claude/.instructions/skills/workflow.md
```

### Инструкция для specs

```
/specs/.instructions/statuses.md
```

---

## Связанные инструкции

- [types.md](./types.md) — типы инструкций
- [validation.md](./validation.md) — валидация формата
