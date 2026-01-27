# Драфт: Сессия валидации ссылок

**Дата:** 2026-01-27
**Статус:** DONE

---

## Резюме

Рефакторинг инструкций `.structure/.instructions/` и создание системы валидации ссылок.

---

## 1. Выполненные задачи

### 1.1. Выравнивание инструкций по эталону

**Эталон:** `standard-readme.md`

**Изменённые файлы:**

| Файл | Изменения |
|------|-----------|
| `standard-frontmatter.md` | Добавлены: "Связанные инструкции", "Оглавление", нумерация секций (## 1., ## 2.), "Скиллы и скрипты" |
| `standard-links.md` | Добавлены: `---` после Оглавления, "Скиллы и скрипты" |

**Структурные изменения:**
- Двухуровневое оглавление (подсекции)
- Секция "Скиллы и скрипты" разделена на "Создаёт" / "Использует"

### 1.2. Создание validation-links.md

**Причина:** Разделение "Стандарт" (что должно быть) и "Валидация" (как проверить).

**Источник:** Секция 8 из `standard-links.md` (удалена).

**Содержание:**
- 6 шагов валидации
- Коды ошибок E001-E009
- Коды предупреждений W001-W003
- Чек-лист
- Типичные ошибки

| Шаг | Проверка | Коды |
|-----|----------|------|
| 1 | Существование цели | E001, E002 |
| 2 | Формат пути | W001, W002 |
| 3 | Якорные ссылки | E003, W003 |
| 4 | Ссылки на папки | E004 |
| 5 | Ссылки в frontmatter | E005, E006, E007 |
| 6 | Ссылки в SSOT | E008, E009 |

### 1.3. Удаление устаревших скиллов

**Удалены папки:**
- `.claude/skills/links-create/`
- `.claude/skills/links-update/`
- `.claude/skills/links-delete/`
- `.claude/skills/links-validate/` (старый)

**Обновлены файлы** (удалены ссылки на links-*):
- `CLAUDE.md`
- `.claude/skills/README.md`
- `.structure/.instructions/README.md`
- `.structure/.instructions/standard-readme.md`
- `.structure/.instructions/standard-links.md`
- `.structure/.instructions/validation-links.md`
- `.structure/.instructions/validation-structure.md`
- `.structure/.instructions/workflow-modify.md`

**Не обновлены** (помечены как неактуальные):
- 16 файлов с упоминаниями links-* остались без изменений

### 1.4. Создание скрипта validate-links.py

**Путь:** `.structure/.instructions/.scripts/validate-links.py`

**Функционал:**
- Проверка всех 6 шагов из `validation-links.md`
- Поддержка `--path` для выборочной проверки
- Поддержка `--json` для автоматизации
- Человекочитаемый вывод с группировкой по файлам

**Использование:**
```bash
# Весь проект
python .structure/.instructions/.scripts/validate-links.py

# Конкретный путь
python .structure/.instructions/.scripts/validate-links.py --path .structure/

# JSON
python .structure/.instructions/.scripts/validate-links.py --json
```

### 1.5. Создание скилла /links-validate

**Путь:** `.claude/skills/links-validate/SKILL.md`

**Воркфлоу:**
1. Запустить скрипт валидации
2. Проанализировать результаты
3. Предложить исправления
4. Проверить чек-лист
5. Вывести результат

**Особенности:**
- SSOT-ссылки ведут на конкретные разделы (с якорями)
- Шаг 4 — возврат на первый невыполненный шаг

---

## 2. Изменённые файлы

### Созданы

| Файл | Описание |
|------|----------|
| `.structure/.instructions/validation-links.md` | Процедура валидации ссылок |
| `.structure/.instructions/.scripts/validate-links.py` | Скрипт валидации |
| `.claude/skills/links-validate/SKILL.md` | Скилл валидации ссылок |

### Обновлены

| Файл | Изменения |
|------|-----------|
| `CLAUDE.md` | Счётчик скиллов 14→11, добавлен /links-validate |
| `.claude/skills/README.md` | Добавлена категория "documentation" |
| `.claude/README.md` | Удалены упоминания links-* |
| `.structure/.instructions/README.md` | Добавлен validation-links.md, убраны links-* |
| `.structure/.instructions/standard-frontmatter.md` | Выравнивание по эталону |
| `.structure/.instructions/standard-links.md` | Удалена секция 8, перенумерована 9→8 |
| `.structure/.instructions/workflow-modify.md` | Заменены /links-* на ручные процессы |

### Удалены

| Путь | Причина |
|------|---------|
| `.claude/skills/links-create/` | Устаревший скилл |
| `.claude/skills/links-update/` | Устаревший скилл |
| `.claude/skills/links-delete/` | Устаревший скилл |

---

## 3. Текущее состояние

### Скиллы (11)

| Категория | Скиллы |
|-----------|--------|
| skill-* | create, delete, migrate, update |
| spec-* | create, status, update |
| instruction-* | create, deactivate, update |
| links-* | validate |

### Инструкции .structure/.instructions/

| Файл | Статус |
|------|--------|
| README.md | ✅ |
| standard-frontmatter.md | ✅ |
| standard-links.md | ✅ |
| standard-readme.md | ✅ (эталон) |
| validation-links.md | ✅ (новый) |
| validation-structure.md | ✅ |
| workflow-create.md | ⚠️ требует проверки |
| workflow-modify.md | ✅ |

### Скрипты

| Скрипт | Статус |
|--------|--------|
| generate-readme.py | ✅ |
| validate-structure.py | ✅ |
| validate-links.py | ✅ (новый) |

---

## 4. Известные проблемы

### 4.1. ~~Ложные срабатывания в validate-links.py~~ ✅ ИСПРАВЛЕНО

Скрипт игнорирует ссылки внутри блоков кода (``` и `).

### 4.2. Битые якоря в документации

Реальные ошибки, найденные скриптом:

| Файл | Ошибка |
|------|--------|
| README.md | `#обязательные-поля` → должен быть `#1-обязательные-поля` |
| README.md | `#правила-заполнения` → нужно проверить |
| README.md | `#шаги` → должен быть `#шаги-валидации` |
| standard-readme.md | `#раздел-заголовок-1` → должен быть `#раздел-заголовок` |

### 4.3. Устаревшие ссылки на links-*

16 файлов содержат упоминания удалённых скиллов:
- Помечены как "неактуальные"
- Требуют ручной проверки при необходимости

---

## 5. Следующие шаги

- [x] ~~Исправить ложные срабатывания в validate-links.py~~ ✅
- [ ] Исправить битые якоря в README.md и standard-readme.md
- [ ] Проверить workflow-create.md на соответствие эталону
- [ ] Обновить 16 файлов с устаревшими ссылками (опционально)
- [ ] Создать /structure-create, /structure-modify, /structure-validate (см. предыдущий драфт)
