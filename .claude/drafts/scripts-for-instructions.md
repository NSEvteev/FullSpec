# Draft: Скрипты для инструкций

**Статус:** IN_PROGRESS
**Дата:** 2026-01-28

## Цель

Создать недостающие скрипты для автоматизации шагов в инструкциях `.instructions/`.

---

## Скрипты для создания

### 1. find-references.py

**Назначение:** Поиск всех ссылок на файл в проекте.

**Использование:**
```bash
python .instructions/.scripts/find-references.py path/to/file.md
python .instructions/.scripts/find-references.py --pattern "old-name.md"
```

**Используется в:**
- `modify-instruction.md` → Деактивация Шаг 1: Найти все ссылки
- `modify-instruction.md` → Миграция Шаг 1: Найти все ссылки на старый путь
- `modify-script.md` → Удаление Шаг 1: Найти зависимости

---

### 2. update-references.py

**Назначение:** Замена ссылок во всех файлах (старый путь → новый).

**Использование:**
```bash
python .instructions/.scripts/update-references.py old-path.md new-path.md
python .instructions/.scripts/update-references.py --dry-run old.md new.md
```

**Используется в:**
- `modify-instruction.md` → Миграция Шаг 4: Обновить все ссылки

---

### 3. create-script-file.py

**Назначение:** Создание файла скрипта по шаблону (аналог create-instruction-file.py).

**Использование:**
```bash
python .instructions/.scripts/create-script-file.py validate-api --area src/.instructions
python .instructions/.scripts/create-script-file.py parse-config --description "Парсинг конфигов"
```

**Используется в:**
- `create-script.md` → Шаг 4: Создать файл по шаблону

---

## Инструкции для обновления

### modify-instruction.md

| Секция | Шаг | Изменение |
|--------|-----|-----------|
| Деактивация | Шаг 1 | Добавить `find-references.py` |
| Миграция | Шаг 1 | Добавить `find-references.py` |
| Миграция | Шаг 4 | Добавить `update-references.py` |
| Скрипты | — | Добавить оба скрипта в таблицу |

### modify-script.md

| Секция | Шаг | Изменение |
|--------|-----|-----------|
| Удаление | Шаг 1 | Добавить `find-references.py` |
| Скрипты | — | Добавить скрипт в таблицу |

### create-script.md

| Секция | Шаг | Изменение |
|--------|-----|-----------|
| Шаги | Шаг 4 | Добавить `create-script-file.py` |
| Скрипты | — | Добавить скрипт в таблицу |

### README.md (.instructions/)

- Добавить все 3 скрипта в секцию "4. Скрипты"
- Обновить структуру папки

---

## Чек-лист

### Создание скриптов
- [x] find-references.py ✅
- [x] update-references.py ✅
- [ ] create-script-file.py

### Валидация скриптов
- [ ] validate-script.py --principles для каждого

### Обновление инструкций
- [ ] modify-instruction.md
- [ ] modify-script.md
- [ ] create-script.md
- [ ] README.md

### Финальная проверка
- [ ] validate-instruction.py --all
- [ ] Тестирование скриптов

---

## Существующие скрипты (справка)

| Скрипт | Назначение |
|--------|------------|
| list-instructions.py | Список инструкций с описаниями |
| create-instruction-file.py | Создание файла инструкции |
| validate-instruction.py | Валидация инструкций |
| validate-script.py | Валидация скриптов |
| parse-docstrings.py | Поиск скриптов по описанию |
