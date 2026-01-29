# Фаза 3: Rules инфраструктура

Создание системы rules с автоматической загрузкой контекста.

---

## Статус: Готова к выполнению

**Дата:** 2026-01-29
**Зависит от:** Фаза 2 ✅

---

## Цель

Создать инфраструктуру для rules:
1. Инструкции (standard, create, modify, validation)
2. Скрипты (validate, list)
3. Скиллы (rule-create, rule-modify, rule-validate)
4. Базовый rule для rules

---

## Формат rule (ВАЖНО)

> **Frontmatter для rules отличается от инструкций!**

**Только поле `paths`** (опционально):

```yaml
---
paths:
  - "паттерн/**"
---

# Название

Содержимое rule.
```

**Типы применения:**

| Тип | Frontmatter | Когда загружается |
|-----|-------------|-------------------|
| Глобальный | Без `paths` | Всегда (при старте сессии) |
| Условный | С `paths` | При работе с файлами по паттерну |

**Паттерны paths:**
- Glob: `**/*.ts`, `src/**/*`
- Braces: `{a,b}/**`
- Относительные от корня проекта

---

## Структура

### Инструкции
```
/.claude/.instructions/rules/
├── README.md              # Индекс
├── standard-rule.md       # Стандарт формата rule
├── create-rule.md         # Создание rule
├── modify-rule.md         # Изменение rule
├── validation-rule.md     # Валидация rules
└── .scripts/
    ├── validate-rule.py   # Валидация формата
    └── list-rules.py      # Список всех rules
```

### Скиллы
```
/.claude/skills/
├── rule-create/SKILL.md   # → create-rule.md
├── rule-modify/SKILL.md   # → modify-rule.md
└── rule-validate/SKILL.md # → validation-rule.md
```

### Rules
```
/.claude/rules/
└── rules.md               # Rule для rules
```

---

## Порядок выполнения

```
[ ] 3.1. Создать standard-rule.md
[ ] 3.2. Создать validation-rule.md + validate-rule.py
[ ] 3.3. Создать create-rule.md + list-rules.py
[ ] 3.4. Создать modify-rule.md
[ ] 3.5. Создать README.md
[ ] 3.6. Создать скиллы rule-*
[ ] 3.7. Создать базовый rule (rules.md)
[ ] 3.8. Обновить CLAUDE.md и /.claude/skills/README.md
[ ] 3.9. Валидация всей фазы
```

---

## 3.1. standard-rule.md

**Секции:**
1. Назначение — что такое rule, когда создавать
2. Расположение — `/.claude/rules/{name}.md`
3. Frontmatter — только `paths` (опционально)
4. Структура — заголовок + содержимое
5. Типы применения — глобальный vs условный
6. Примеры

---

## 3.2. validation-rule.md + validate-rule.py

**Проверки:**
- Файл в `/.claude/rules/`
- Расширение `.md`
- Frontmatter валиден (если есть `paths` — массив строк)
- Есть заголовок H1
- Паттерны paths валидны

**Коды ошибок:** R0xx

| Код | Описание |
|-----|----------|
| R001 | Неверное расположение |
| R002 | Неверное расширение |
| R010 | Невалидный frontmatter |
| R011 | `paths` не массив |
| R020 | Нет заголовка H1 |

---

## 3.3. create-rule.md + list-rules.py

**Шаги:**
1. Проверить существующие rules (list-rules.py)
2. Выбрать тип применения (глобальный/условный)
3. Определить имя и паттерны paths
4. Создать файл
5. Валидация
6. Отчёт

**Обязательный шаг выбора типа:**
```
Шаг 2: Выбрать тип применения

> **ОБЯЗАТЕЛЬНО** — AskUserQuestion

Варианты:
1. Глобальный — rule нужен всегда (без paths)
2. Условный — rule при работе с файлами (с paths)
```

---

## 3.4. modify-rule.md

**Типы изменений:**
- Обновление — изменить содержимое, paths
- Деактивация — rule больше не нужен
- Миграция — переименование

---

## 3.5. README.md

**Формат:** стандартный README для папки инструкций

**Содержит:**
- Описание области
- Таблица инструкций
- Таблица скриптов

---

## 3.6. Скиллы rule-*

| Скилл | Назначение | SSOT |
|-------|------------|------|
| `/rule-create` | Создание rule | `create-rule.md` |
| `/rule-modify` | Изменение rule | `modify-rule.md` |
| `/rule-validate` | Валидация rule | `validation-rule.md` |

**Формат:** по стандарту из `standard-skill.md`

---

## 3.7. Базовый rule (rules.md)

**Файл:** `/.claude/rules/rules.md`

```markdown
---
paths:
  - ".claude/rules/**"
---

# Rules

При создании rule:
→ `/rule-create`

При изменении rule:
→ `/rule-modify`

При валидации rule:
→ `/rule-validate`
```

---

## 3.8. Обновить документацию

- [ ] `/.claude/skills/README.md` — добавить категорию rules
- [ ] `/CLAUDE.md` — обновить счётчик скиллов (13 → 16)

---

## 3.9. Валидация

- [ ] Все инструкции проходят validate-instruction.py
- [ ] Скрипты работают
- [ ] Скиллы проходят validate-skill.py
- [ ] Rule rules.md загружается при работе в `.claude/rules/`

---

## Результат Фазы 3

**Создано:**
- 5 инструкций (standard, create, modify, validation, README)
- 2 скрипта (validate-rule.py, list-rules.py)
- 3 скилла (rule-create, rule-modify, rule-validate)
- 1 rule (rules.md)

**Обновлено:**
- CLAUDE.md
- /.claude/skills/README.md

---

## После Фазы 3

→ Фаза 4: Rules для областей (instructions, scripts, skills, structure)
