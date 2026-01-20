# Тесты: input-validate

> **Scope:** claude
> **Категория:** utility
> **Критичность:** 🟡 Medium (переиспользуемый компонент)

---

## Smoke test

📋 **Smoke test: input-validate**

**Команда:** `/input-validate skill-name test-skill`
**Триггер:** "проверь ввод skill-name test-skill"

**Ожидание:**
- [ ] Скилл запускается без ошибок
- [ ] Выводит результат валидации
- [ ] Формат вывода соответствует спецификации

**Результат:** ⬜ Не выполнен

---

## Functional tests

### FT-1: Валидация skill-name (успех)

**Команда:**
```
/input-validate skill-name my-awesome-skill
```

**Ожидание:**
```
✅ Валидация пройдена

Тип: skill-name
Значение: my-awesome-skill
```

**Результат:** ⬜ Не выполнен

---

### FT-2: Валидация skill-name (ошибка — без дефиса)

**Команда:**
```
/input-validate skill-name myskill --required
```

**Ожидание:**
```
❌ Валидация не пройдена

Тип: skill-name
Значение: myskill
Ошибка: Формат не соответствует паттерну

Ожидаемый формат: ^[a-z]+(-[a-z]+)+$
Примеры: skill-create, doc-update, test-review
```

**Результат:** ⬜ Не выполнен

---

### FT-3: Валидация skill-name (ошибка — заглавные буквы)

**Команда:**
```
/input-validate skill-name MySkill
```

**Ожидание:**
- Ошибка валидации
- Показан ожидаемый формат

**Результат:** ⬜ Не выполнен

---

### FT-4: Валидация file-path (файл существует)

**Команда:**
```
/input-validate file-path /.claude/skills/skill-create/SKILL.md
```

**Ожидание:**
```
✅ Валидация пройдена

Тип: file-path
Значение: /.claude/skills/skill-create/SKILL.md
```

**Результат:** ⬜ Не выполнен

---

### FT-5: Валидация file-path (файл не существует)

**Команда:**
```
/input-validate file-path /.claude/skills/nonexistent/SKILL.md
```

**Ожидание:**
- Ошибка "Файл не найден"
- Показаны похожие файлы (если есть)

**Результат:** ⬜ Не выполнен

---

### FT-6: Валидация dir-path (папка существует)

**Команда:**
```
/input-validate dir-path /.claude/skills/
```

**Ожидание:**
```
✅ Валидация пройдена

Тип: dir-path
Значение: /.claude/skills/
```

**Результат:** ⬜ Не выполнен

---

### FT-7: Валидация issue-number

**Команда:**
```
/input-validate issue-number #123
```

**Ожидание:**
```
✅ Валидация пройдена

Тип: issue-number
Значение: #123
```

**Результат:** ⬜ Не выполнен

---

### FT-8: Валидация issue-number (без #)

**Команда:**
```
/input-validate issue-number 456
```

**Ожидание:**
- Валидация пройдена (оба формата допустимы)

**Результат:** ⬜ Не выполнен

---

### FT-9: Флаг --required с пустым значением

**Команда:**
```
/input-validate skill-name "" --required
```

**Ожидание:**
```
❌ Валидация не пройдена

Тип: skill-name
Ошибка: Значение обязательно (--required)
```

**Результат:** ⬜ Не выполнен

---

### FT-10: Флаг --silent

**Команда:**
```
/input-validate skill-name test-skill --silent
```

**Ожидание:**
- Нет вывода в консоль
- Код возврата 0 (успех)

**Результат:** ⬜ Не выполнен

---

### FT-11: Неизвестный тип валидации

**Команда:**
```
/input-validate unknown-type value
```

**Ожидание:**
```
❌ Ошибка: Неизвестный тип валидации

Тип: unknown-type

Доступные типы:
- skill-name
- file-path
- dir-path
- md-file
- issue-number
- branch-name
- url
- email
- semver
- json
- yaml-frontmatter
- not-empty
```

**Результат:** ⬜ Не выполнен

---

### FT-12: Валидация yaml-frontmatter

**Команда:**
```
/input-validate yaml-frontmatter /.claude/skills/skill-create/SKILL.md
```

**Ожидание:**
- Показаны поля frontmatter
- Статус: пройдена

**Результат:** ⬜ Не выполнен

---

## Integration test

### IT-1: Интеграция с skill-create

**Сценарий:** Использование input-validate в workflow skill-create

**Шаги:**
1. Вызвать `/skill-create invalid_name`
2. Ожидать вызов `/input-validate skill-name invalid_name`
3. Ожидать ошибку валидации

**Ожидание:**
- skill-create вызывает input-validate
- При ошибке валидации — запрос корректного имени

**Результат:** ⬜ Не выполнен

---

### IT-2: Batch-валидация

**Команда:**
```
/input-validate skill-name test-skill --required
/input-validate dir-path /.claude/skills/ --required
/input-validate md-file /.claude/instructions/README.md
```

**Ожидание:**
- Все три валидации выполнены последовательно
- Результат каждой показан

**Результат:** ⬜ Не выполнен

---

## Чек-лист smoke test

- [ ] Скилл распознаёт команду `/input-validate`
- [ ] Скилл распознаёт триггер "проверь ввод"
- [ ] Валидация skill-name работает
- [ ] Валидация file-path работает
- [ ] Валидация dir-path работает
- [ ] Флаг --required работает
- [ ] Флаг --silent работает
- [ ] Ошибки выводятся в правильном формате
- [ ] Успех выводится в правильном формате

---

## История запусков

| Дата | Версия | Smoke | Functional | Integration | Комментарий |
|------|--------|-------|------------|-------------|-------------|
| — | — | ⬜ | ⬜ | ⬜ | Тесты не выполнялись |
