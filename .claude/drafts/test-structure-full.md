# Полный план тестирования структуры с зеркалированием

**Дата:** 2026-01-27
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
- [ ] `test/` создана
- [ ] `test/README.md` существует и заполнен

**SSOT (`/.structure/README.md`):**
- [ ] Оглавление содержит `[test/]`
- [ ] Секция `### 🔗 [test/]` добавлена
- [ ] Дерево содержит `├── test/`

**Зеркало `.instructions`:**
- [ ] `test/.instructions/` создана
- [ ] `test/.instructions/README.md` существует

**Валидация:**
- [ ] `/structure-validate` проходит
- [ ] `/structure-validate --check-instructions` проходит
- [ ] `/links-validate` проходит

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
- [ ] `test/subtest/` создана
- [ ] `test/subtest/README.md` существует

**Родительский README (`test/README.md`):**
- [ ] Секция "Папки" содержит `subtest/`
- [ ] Дерево содержит `└── subtest/`

**SSOT (`/.structure/README.md`):**
- [ ] Оглавление содержит `[test/subtest/]` (вложенный)
- [ ] Секция `### 🔗 [test/subtest/]` добавлена после `test/`
- [ ] Дерево: `test/` содержит `└── subtest/`

**Зеркало `.instructions`:**
- [ ] `test/.instructions/subtest/` создана
- [ ] `test/.instructions/subtest/README.md` существует

**Валидация:**
- [ ] `/structure-validate --check-instructions` проходит
- [ ] `/links-validate` проходит

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

# 4. Обновить SSOT
python .structure/.instructions/.scripts/ssot.py rename test/subtest test/demo -d "Демо подпапка"

# 5. Обновить README папки (заголовок)
# → Edit test/demo/README.md: заголовок subtest → demo

# 6. Обновить ссылки в файлах
python .structure/.instructions/.scripts/find-references.py test/subtest
# → Edit найденные файлы

# 7. Валидация
python .structure/.instructions/.scripts/validate.py --path test
```

### Чек-лист

**Папка проекта:**
- [ ] `test/demo/` существует
- [ ] `test/subtest/` НЕ существует
- [ ] `test/demo/README.md` — заголовок обновлён

**Родительский README (`test/README.md`):**
- [ ] Секция "Папки": `subtest/` → `demo/`
- [ ] Дерево: `subtest/` → `demo/`

**SSOT (`/.structure/README.md`):**
- [ ] Оглавление: `test/subtest/` → `test/demo/`
- [ ] Секция переименована
- [ ] Дерево обновлено

**Зеркало `.instructions`:**
- [ ] `test/.instructions/demo/` существует
- [ ] `test/.instructions/subtest/` НЕ существует
- [ ] `test/.instructions/demo/README.md` — ссылки обновлены

**Скиллы:**
- [ ] SSOT-ссылки обновлены (если были)

**Валидация:**
- [ ] `/structure-validate --check-instructions` проходит
- [ ] `/links-validate` проходит

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

# 7. Обновить ссылки
python .structure/.instructions/.scripts/find-references.py test/demo
# → Edit найденные файлы

# 8. Валидация
python .structure/.instructions/.scripts/validate.py
```

### Чек-лист

**Папка проекта:**
- [ ] `test-demo/` существует в корне
- [ ] `test/demo/` НЕ существует
- [ ] `test-demo/README.md`:
  - [ ] Заголовок с новым путём
  - [ ] frontmatter (`index`) обновлён
  - [ ] "Полезные ссылки" обновлены

**Родительский README (`test/README.md`):**
- [ ] `demo/` удалена из секции "Папки"
- [ ] `demo/` удалена из дерева

**SSOT (`/.structure/README.md`):**
- [ ] `test/demo/` удалена
- [ ] `test-demo/` добавлена (корневая)
- [ ] Оглавление обновлено
- [ ] Дерево обновлено

**Зеркало `.instructions`:**
- [ ] `test-demo/.instructions/` существует
- [ ] `test/.instructions/demo/` НЕ существует
- [ ] `test-demo/.instructions/README.md` создан

**Валидация:**
- [ ] `/structure-validate --check-instructions` проходит
- [ ] `/links-validate` проходит

---

## Тест 5: Удаление папки

**Действие:** Удалить `test-demo/`

### Команды

```bash
# 1. Пометить DELETE_ (зеркало + скиллы)
python .structure/.instructions/.scripts/mark-deleted.py test-demo

# 2. Удалить из SSOT
python .structure/.instructions/.scripts/ssot.py delete test-demo

# 3. Обновить ссылки
python .structure/.instructions/.scripts/find-references.py test-demo
# → Edit/удалить найденные ссылки

# 4. Удалить папку
rm -rf test-demo

# 5. Валидация
python .structure/.instructions/.scripts/validate.py
```

### Чек-лист

**Папка проекта:**
- [ ] `test-demo/` НЕ существует

**SSOT (`/.structure/README.md`):**
- [ ] Секция `test-demo/` удалена
- [ ] Оглавление обновлено
- [ ] Дерево обновлено

**Зеркало `.instructions` (DELETE_):**
- [ ] `DELETE_test-demo/` существует (или `test-demo/.instructions/` → `DELETE_...`)
- [ ] Файлы внутри: `DELETE_*.md`

**Скиллы:**
- [ ] Связанные скиллы помечены `DELETE_` (если были)

**Валидация:**
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит
- [ ] Нет битых ссылок на `test-demo/`

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

- [ ] `test/` НЕ существует
- [ ] SSOT не содержит `test/`
- [ ] `DELETE_test/` или `test/.instructions/` → `DELETE_...`
- [ ] Нет битых ссылок
- [ ] Проект в исходном состоянии (кроме `DELETE_*`)

---

## Тест 7: Валидация `--check-instructions`

**Действие:** Проверить работу флага `--check-instructions`

### Команды

```bash
# Запустить валидацию
python .structure/.instructions/.scripts/validate-structure.py --check-instructions

# С JSON-выводом
python .structure/.instructions/.scripts/validate-structure.py --check-instructions --json
```

### Чек-лист

- [ ] Скрипт запускается без ошибок
- [ ] Находит папки без зеркал `.instructions` (если есть)
- [ ] Выводит команды для создания недостающих зеркал
- [ ] JSON-вывод корректен

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

- [ ] Нет `DELETE_*` папок в проекте
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит

---

## Результаты тестирования

### Базовый воркфлоу (ssot.py)

| Тест | Статус | Замечания |
|------|--------|-----------|
| 1. Создание корневой | ✅ | Работает |
| 2. Создание подпапки | ✅ | Работает (баги #1-4 исправлены) |
| 3. Переименование | ✅ | Работает (баги #5, #7 исправлены) |
| 4. Перемещение | ✅ | Работает (баг #6 исправлен) |
| 5. Удаление | ✅ | Работает |
| 6. Удаление родителя | ✅ | Работает |

### Зеркалирование `.instructions`

| Тест | Статус | Замечания |
|------|--------|-----------|
| 1. Создание + зеркало | ✅ | test/ + test/.instructions/ |
| 2. Подпапка + зеркало | ✅ | test/subtest/ + test/.instructions/subtest/ |
| 3. Rename + зеркало | ✅ | subtest→demo, зеркало переименовано |
| 4. Move + зеркало | ✅ | test/demo→test-demo, зеркало перемещено |
| 5. Delete + DELETE_ | ✅ | test-demo удалён, DELETE_.instructions помечен |
| 6. Delete родителя | ✅ | test/ удалён с DELETE_.instructions |
| 7. --check-instructions | ✅ | Находит папки без зеркал, JSON работает |
| 8. Очистка | ✅ | DELETE_* удалены вместе с папками |

---

## Исправленные баги

| # | Проблема | Файл | Решение |
|---|----------|------|---------|
| 1 | `ssot.py add` неправильно выравнивает комментарии | ssot.py | ✅ COMMENT_COLUMN |
| 2 | Инструкция не указывает про подпапки в SSOT | create-structure.md | ✅ Обновлено |
| 3 | `ssot.py add` не поддерживает вложенные пути | ssot.py | ✅ parse_folder_path() |
| 4 | `├──` вместо `└──` для последнего элемента | ssot.py | ✅ fix_tree_connectors() |
| 5 | rename теряет `│` разделитель | ssot.py | ✅ fix_tree_connectors() |
| 6 | delete не управляет `│` корректно | ssot.py | ✅ fix_tree_connectors() |
| 7 | rename/delete не удаляли детей | ssot.py | ✅ skip_children |

---

## Готовность

| Компонент | Статус |
|-----------|--------|
| Инструкции (Фаза 1) | ✅ |
| Скрипты (Фаза 2) | ✅ |
| Баги ssot.py | ✅ |
| Тестирование (Фаза 3) | ✅ Все 8 тестов пройдены |

**Дата тестирования:** 2026-01-27
**Все скрипты работают корректно.**
