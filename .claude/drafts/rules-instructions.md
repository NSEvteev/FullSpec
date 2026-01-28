# Rules для инструкций

Автоматическая загрузка правил при работе с `.instructions/`.

---

## Статус: Отложено

Выделено из [instructions-workflow-refactoring.md](./instructions-workflow-refactoring.md) (Фаза 9).

---

## Концепция

```
Пользователь работает с .instructions/
         ↓
Rule автоматически загружается (paths match)
         ↓
Rule: "Используй /instruction-create или /instruction-modify"
         ↓
Skill читает SSOT-инструкцию и выполняет
```

---

## Файл

**Путь:** `/.claude/rules/instructions.md`

```markdown
---
paths:
  - ".instructions/**"
  - "**/.instructions/**"
---

# Инструкции

При создании инструкции:
→ `/instruction-create`

При изменении инструкции:
→ `/instruction-modify`
```

---

## Чек-лист

- [ ] Создать папку `/.claude/rules/`
- [ ] Создать `instructions.md`
- [ ] Протестировать автозагрузку

