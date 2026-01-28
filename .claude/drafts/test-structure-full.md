# Полный план тестирования структуры с зеркалированием

**Дата:** 2026-01-28 (повторное тестирование)
**Статус:** ✅ DONE — Все тесты пройдены
**Цель:** Проверить полный воркфлоу создания/изменения папок с зеркалированием `.instructions`

---

## Обзор

### Что тестируем

| Операция | Папка проекта | SSOT | Зеркало `.instructions` | Скиллы |
|----------|---------------|------|-------------------------|--------|
| Создание | `mkdir` + README | `ssot.py add` | `mirror-instructions.py create` | — |
| Переименование | `mv` + README | `ssot.py rename` | `mirror-instructions.py rename` | `update-skill-refs.py` |
| Перемещение | `mv` + README | delete + add | `mirror-instructions.py move` | `update-skill-refs.py` |
| Удаление | `rm -rf` | `ssot.py delete` | `mark-deleted.py` | `mark-deleted.py` |

### Скрипты

| Скрипт | Путь | Назначение |
|--------|------|------------|
| `generate-readme.py` | `.structure/.instructions/.scripts/` | Генерация README для папок |
| `ssot.py` | `.structure/.instructions/.scripts/` | Управление SSOT (add/rename/delete) |
| `mirror-instructions.py` | `.structure/.instructions/.scripts/` | Зеркалирование `.instructions` |
| `mark-deleted.py` | `.structure/.instructions/.scripts/` | Пометка DELETE_ при удалении |
| `update-skill-refs.py` | `.structure/.instructions/.scripts/` | Обновление ссылок в скиллах |
| `validate.py` | `.structure/.instructions/.scripts/` | Единая валидация |

### Принцип зеркалирования

```
test/                    → test/.instructions/README.md
test/subtest/            → test/.instructions/subtest/README.md
test/subtest/deep/       → test/.instructions/subtest/deep/README.md
```

---

## Тест 1: Создание корневой папки

**Действие:** Создать `test/` в корне проекта

### Команды

```bash
# 1. Создать папку и README
python .structure/.instructions/.scripts/generate-readme.py test --create
# → Заполнить плейсхолдеры в test/README.md

# 2. Создать зеркало .instructions
python .structure/.instructions/.scripts/mirror-instructions.py create test

# 3. Добавить в SSOT
python .structure/.instructions/.scripts/ssot.py add test -d "Тестовая папка" -e "Папка для тестирования воркфлоу структуры."

# 4. Валидация
python .structure/.instructions/.scripts/validate.py --path test
```

### Чек-лист

**Папка проекта:**
- [x] `test/` создана
- [x] `test/README.md` существует и заполнен

**SSOT (`/.structure/README.md`):**
- [x] Оглавление содержит `[test/]`
- [x] Секция `### 🔗 [test/]` добавлена
- [x] Дерево содержит `├── test/`

**Зеркало `.instructions`:**
- [x] `test/.instructions/` создана
- [x] `test/.instructions/README.md` существует

---

## Тест 2: Создание подпапки

**Действие:** Создать `test/subtest/` внутри `test/`

### Команды

```bash
# 1. Создать подпапку и README
python .structure/.instructions/.scripts/generate-readme.py test/subtest --create

# 2. Создать зеркало в .instructions
python .structure/.instructions/.scripts/mirror-instructions.py create test/subtest

# 3. Добавить в SSOT
python .structure/.instructions/.scripts/ssot.py add test/subtest -d "Тестовая подпапка" -e "Подпапка для тестирования вложенности."

# 4. Валидация
python .structure/.instructions/.scripts/validate.py --path test
```

### Чек-лист

**Папка проекта:**
- [x] `test/subtest/` создана
- [x] `test/subtest/README.md` существует

**Родительский README (`test/README.md`):**
- [x] Секция "Папки" содержит `subtest/`
- [x] Дерево содержит `subtest/`

**SSOT (`/.structure/README.md`):**
- [x] Дерево: `test/` содержит `subtest/`
- [x] Дерево: `.instructions/` содержит `subtest/`

**Зеркало `.instructions`:**
- [x] `test/.instructions/subtest/` создана
- [x] `test/.instructions/subtest/README.md` существует

---

## Тест 3: Переименование подпапки

**Действие:** Переименовать `test/subtest/` → `test/demo/`

### Команды

```bash
# 1. Переименовать папку
mv test/subtest test/demo

# 2. Переименовать зеркало
python .structure/.instructions/.scripts/mirror-instructions.py rename test/subtest test/demo

# 3. Обновить ссылки в скиллах (если есть)
python .structure/.instructions/.scripts/update-skill-refs.py test/subtest test/demo

# 4. Обновить SSOT (автоматически обновляет зеркало в дереве)
python .structure/.instructions/.scripts/ssot.py rename test/subtest test/demo -d "Демо подпапка"

# 5. Обновить README папки (заголовок)
# → Edit test/demo/README.md: заголовок subtest → demo

# 6. Обновить родительский README
# → Edit test/README.md: subtest → demo

# 7. Валидация
python .structure/.instructions/.scripts/validate.py --path test
```

### Чек-лист

**Папка проекта:**
- [x] `test/demo/` существует
- [x] `test/subtest/` НЕ существует
- [x] `test/demo/README.md` — заголовок обновлён

**Родительский README (`test/README.md`):**
- [x] Секция "Папки": `subtest/` → `demo/`
- [x] Дерево: `subtest/` → `demo/`

**SSOT (`/.structure/README.md`):**
- [x] Дерево: папка `demo/`
- [x] Дерево: зеркало `.instructions/demo/`

**Зеркало `.instructions`:**
- [x] `test/.instructions/demo/` существует
- [x] `test/.instructions/subtest/` НЕ существует

---

## Тест 4: Перемещение в корень

**Действие:** Переместить `test/demo/` → `test-demo/` (в корень)

### Команды

```bash
# 1. Переместить папку
mv test/demo test-demo

# 2. Переместить зеркало
python .structure/.instructions/.scripts/mirror-instructions.py move test/demo test-demo

# 3. Обновить ссылки в скиллах
python .structure/.instructions/.scripts/update-skill-refs.py test/demo test-demo

# 4. Обновить SSOT (удалить старое + добавить новое)
python .structure/.instructions/.scripts/ssot.py delete test/demo
python .structure/.instructions/.scripts/ssot.py add test-demo -d "Тест-демо" -e "Перемещённая папка."

# 5. Обновить README папки
# → Edit test-demo/README.md: заголовок, frontmatter, ссылки

# 6. Обновить родительский README
# → Edit test/README.md: удалить demo/ из секции "Папки" и дерева

# 7. Валидация
python .structure/.instructions/.scripts/validate.py
```

### Чек-лист

**Папка проекта:**
- [x] `test-demo/` существует в корне
- [x] `test/demo/` НЕ существует
- [x] `test-demo/README.md` — заголовок, index, ссылки обновлены

**Родительский README (`test/README.md`):**
- [x] `demo/` удалена из секции "Папки"
- [x] `demo/` удалена из дерева

**SSOT (`/.structure/README.md`):**
- [x] `test/demo/` удалена (включая зеркало)
- [x] `test-demo/` добавлена (корневая)
- [x] Оглавление обновлено
- [x] Дерево обновлено

**Зеркало `.instructions`:**
- [x] `test-demo/.instructions/` существует
- [x] `test/.instructions/demo/` НЕ существует

---

## Тест 5: Удаление папки

**Действие:** Удалить `test-demo/`

### Команды

```bash
# 1. Пометить DELETE_ (зеркало + скиллы)
python .structure/.instructions/.scripts/mark-deleted.py test-demo

# 2. Удалить из SSOT
python .structure/.instructions/.scripts/ssot.py delete test-demo

# 3. Удалить папку
rm -rf test-demo

# 4. Валидация
python .structure/.instructions/.scripts/validate.py
```

### Чек-лист

**Папка проекта:**
- [x] `test-demo/` НЕ существует

**SSOT (`/.structure/README.md`):**
- [x] Секция `test-demo/` удалена
- [x] Оглавление обновлено
- [x] Дерево обновлено

---

## Тест 6: Удаление родительской папки

**Действие:** Удалить `test/`

### Команды

```bash
# 1. Пометить DELETE_
python .structure/.instructions/.scripts/mark-deleted.py test

# 2. Удалить из SSOT
python .structure/.instructions/.scripts/ssot.py delete test

# 3. Удалить папку
rm -rf test

# 4. Валидация
python .structure/.instructions/.scripts/validate.py
```

### Чек-лист

- [x] `test/` НЕ существует
- [x] SSOT не содержит `test/`
- [x] Проект в исходном состоянии

---

## Тест 7: Валидация `--check-instructions`

**Действие:** Проверить работу флага `--check-instructions`

### Команды

```bash
# Запустить валидацию
python .structure/.instructions/.scripts/validate.py --check-instructions

# С JSON-выводом
python .structure/.instructions/.scripts/validate.py --check-instructions --json
```

### Чек-лист

- [x] Скрипт запускается без ошибок
- [x] Находит папки без зеркал `.instructions` (если есть)
- [x] Выводит команды для создания недостающих зеркал
- [x] JSON-вывод корректен

---

## Тест 8: Очистка

**Действие:** Удалить все `DELETE_*` папки

### Команды

```bash
# Найти DELETE_ папки
find . -name "DELETE_*" -type d

# Удалить
rm -rf DELETE_*
rm -rf */DELETE_*
rm -rf */.instructions/DELETE_*
```

### Чек-лист

- [x] Нет `DELETE_*` папок в проекте (удалены вместе с родительскими папками)

---

## Результаты тестирования

### Базовый воркфлоу (ssot.py)

| Тест | Статус | Замечания |
|------|--------|-----------|
| 1. Создание корневой | ✅ | Работает |
| 2. Создание подпапки | ✅ | Работает |
| 3. Переименование | ✅ | Работает (баг #8 исправлен) |
| 4. Перемещение | ✅ | Работает |
| 5. Удаление | ✅ | Работает (баг #9 исправлен) |
| 6. Удаление родителя | ✅ | Работает |

### Зеркалирование `.instructions`

| Тест | Статус | Замечания |
|------|--------|-----------|
| 1. Создание + зеркало | ✅ | test/ + test/.instructions/ |
| 2. Подпапка + зеркало | ✅ | test/subtest/ + test/.instructions/subtest/ |
| 3. Rename + зеркало | ✅ | subtest→demo, зеркало в SSOT обновлено |
| 4. Move + зеркало | ✅ | test/demo→test-demo, зеркало перемещено |
| 5. Delete + зеркало | ✅ | Зеркало удаляется из SSOT автоматически |
| 6. Delete родителя | ✅ | test/ удалён |
| 7. --check-instructions | ✅ | Находит папки без зеркал, JSON работает |
| 8. Очистка | ✅ | DELETE_* удалены вместе с папками |

---

## Исправленные баги

### Первое тестирование (2026-01-27)

| # | Проблема | Файл | Решение |
|---|----------|------|---------|
| 1 | `ssot.py add` неправильно выравнивает комментарии | ssot.py | ✅ COMMENT_COLUMN |
| 2 | Инструкция не указывает про подпапки в SSOT | create-structure.md | ✅ Обновлено |
| 3 | `ssot.py add` не поддерживает вложенные пути | ssot.py | ✅ parse_folder_path() |
| 4 | `├──` вместо `└──` для последнего элемента | ssot.py | ✅ fix_tree_connectors() |
| 5 | rename теряет `│` разделитель | ssot.py | ✅ fix_tree_connectors() |
| 6 | delete не управляет `│` корректно | ssot.py | ✅ fix_tree_connectors() |
| 7 | rename/delete не удаляли детей | ssot.py | ✅ skip_children |

### Повторное тестирование (2026-01-28)

| # | Проблема | Файл | Решение |
|---|----------|------|---------|
| 8 | `ssot.py rename` не обновлял зеркало `.instructions` в дереве | ssot.py | ✅ cmd_rename() + delete/add зеркала |
| 9 | `ssot.py delete` не удалял зеркало `.instructions` из дерева | ssot.py | ✅ cmd_delete() + delete_from_tree() для зеркала |
| 10 | `validate.py --check-instructions` не реализован | validate.py | ✅ check_instructions_mirrors() + --json |

---

## Готовность

| Компонент | Статус |
|-----------|--------|
| Инструкции (Фаза 1) | ✅ |
| Скрипты (Фаза 2) | ✅ |
| Баги ssot.py | ✅ Все исправлены |
| Баги validate.py | ✅ --check-instructions реализован |
| Тестирование (Фаза 3) | ✅ Все 8 тестов пройдены |

**Дата последнего тестирования:** 2026-01-28
**Коммит:** `a5bd1fd fix: Исправление ssot.py и добавление --check-instructions в validate.py`
**Все скрипты работают корректно.**
