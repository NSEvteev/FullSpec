# План: Поддержка вложенных папок в README инструкций

**SSOT драфт:** [nested-instructions-folders.md](./nested-instructions-folders.md)

---

## Проблема

`.claude/.instructions/README.md` игнорирует подпапку `rules/`, описывая только `skills/`. Стандарт не поддерживает вложенные папки инструкций.

---

## Решение

Добавить раздел "Вложенные области" в README папок инструкций, который описывает подпапки.

**Структура:**
1. Вложенные области (подпапки) — если есть
2. Секции 1-5 (файлы текущей папки) — всегда

---

## Файлы для изменения

### Инструкции (4 файла)

| Файл | Изменение |
|------|-----------|
| `.structure/.instructions/standard-readme.md` | Добавить описание раздела "Вложенные области" в § 3 |
| `.structure/.instructions/create-structure.md` | Обновить Шаг 5 — обновление родительского README |
| `.structure/.instructions/modify-structure.md` | Добавить шаги для вложенных папок |
| `.structure/.instructions/validation-structure.md` | Добавить проверку секции "Вложенные области" (коды S010-S012) |

### Скрипты (2 файла)

| Файл | Изменение |
|------|-----------|
| `.structure/.instructions/.scripts/mirror-instructions.py` | Добавить шаблон с вложенными областями, обновить логику |
| `.structure/.instructions/.scripts/validate-structure.py` | Добавить проверку вложенных областей |

### README для исправления (1 файл)

| Файл | Изменение |
|------|-----------|
| `.claude/.instructions/README.md` | Переписать — добавить skills/ и rules/ |

---

## Порядок выполнения

### Фаза 1: Обновить стандарт

**1.1. standard-readme.md**

Добавить в § 3 "README папок инструкций":

```markdown
### Раздел "Вложенные области" (опционально)

**Условие:** Присутствует если в папке `.instructions/` есть подпапки (кроме `.scripts/`).

**Расположение:** После оглавления, ПЕРЕД секцией "1. Стандарты".

**Формат:**

| Область | Описание | Индекс |
|---------|----------|--------|
| [{папка}/](./{папка}/) | {Описание} | [README](./{папка}/README.md) |

**Если секции 1-5 пустые:**
*Нет ... в корне — см. вложенные области.*
```

### Фаза 2: Обновить воркфлоу

**2.1. create-structure.md**

В Шаг 5 добавить:
- При создании подпапки в `.instructions/` — обновить родительский README (секция "Вложенные области")

**2.2. modify-structure.md**

Добавить шаги:
- Переименование: обновить "Вложенные области" в родителе
- Деактивация: удалить из "Вложенные области"

**2.3. validation-structure.md**

Добавить Шаг 4.1 и коды ошибок:
- S010: Подпапка не указана в "Вложенные области"
- S011: Битая ссылка на README подпапки
- S012: Секция "Вложенные области" отсутствует при наличии подпапок

### Фаза 3: Обновить скрипты

**3.1. mirror-instructions.py**

Текущее состояние:
- Есть `update_parent_instructions_readme()` — добавляет в TOC и tree
- НЕТ добавления в секцию "Вложенные области"

Изменения:
1. Добавить `README_TEMPLATE_WITH_NESTED` — шаблон с секцией "Вложенные области"
2. Добавить `add_to_nested_areas()` — функция добавления в таблицу вложенных областей
3. Обновить `update_parent_instructions_readme()` — вызывать `add_to_nested_areas()`
4. Обновить `cmd_create()` — определять нужен ли шаблон с вложенными областями

**3.2. validate-structure.py**

Текущее состояние:
- Проверяет только наличие `.instructions/README.md` (T005)
- НЕ проверяет содержимое

Изменения:
1. Добавить коды S010, S011, S012 в ERROR_CODES
2. Добавить `check_nested_areas()` — проверка секции "Вложенные области"
3. Вызывать `check_nested_areas()` в основной валидации

### Фаза 4: Исправить существующий README

**4.1. .claude/.instructions/README.md**

Переписать с:
- Секция "Вложенные области" (skills/, rules/)
- Секции 1-5 с текстом "*Нет ... — см. вложенные области.*"

---

## Валидация

После каждой фазы:
```bash
python .instructions/.scripts/validate-instruction.py <путь>
```

После Фазы 3:
```bash
python .structure/.instructions/.scripts/validate-structure.py
```

После Фазы 4:
```bash
python .structure/.instructions/.scripts/validate.py --path .claude
```

---

## Чек-лист

### Фаза 1: Стандарт
- [ ] standard-readme.md — добавить раздел "Вложенные области"

### Фаза 2: Воркфлоу
- [ ] create-structure.md — обновить Шаг 5
- [ ] modify-structure.md — добавить шаги для вложенных папок
- [ ] validation-structure.md — добавить Шаг 4.1 и коды S010-S012

### Фаза 3: Скрипты
- [ ] mirror-instructions.py — шаблон + функция add_to_nested_areas
- [ ] validate-structure.py — функция check_nested_areas + коды ошибок

### Фаза 4: README
- [ ] .claude/.instructions/README.md — переписать
