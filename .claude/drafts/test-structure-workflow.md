# Драфт: Тестирование воркфлоу структуры

**Дата:** 2026-01-27
**Статус:** IN_PROGRESS
**Цель:** Проверить работу `.structure/.instructions/` и скиллов `structure-*`

---

## План тестирования

| Шаг | Действие | Скилл | Что проверяем |
|-----|----------|-------|---------------|
| 1 | Создать папку `test/` в корне | `/structure-create` | README, SSOT, родитель |
| 2 | Создать подпапку `test/subtest/` | `/structure-create` | README, родитель `test/` |
| 3 | Переименовать `test/subtest/` → `test/demo/` | `/structure-modify` | Ссылки, README, SSOT |
| 4 | Переместить `test/demo/` → `test-demo/` (в корень) | `/structure-modify` | Пути, frontmatter, родители |
| 5 | Удалить `test-demo/` | `/structure-modify` | SSOT, родитель, ссылки |
| 6 | Удалить `test/` | `/structure-modify` | Финальная очистка |

---

## Шаг 1: Создать папку `test/` в корне

**Команда:** `/structure-create test --description "Тестовая папка"`

**Чек-лист после выполнения:**
- [ ] Папка `test/` создана
- [ ] `test/README.md` создан и заполнен
- [ ] `/.structure/README.md` содержит секцию `test/`
- [ ] Корневой README (если есть) обновлён
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит

---

## Шаг 2: Создать подпапку `test/subtest/`

**Команда:** `/structure-create test/subtest --description "Тестовая подпапка"`

**Чек-лист после выполнения:**
- [ ] Папка `test/subtest/` создана
- [ ] `test/subtest/README.md` создан
- [ ] `test/README.md` содержит описание `subtest/` в секции "Папки"
- [ ] `test/README.md` содержит `subtest/` в дереве
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит

---

## Шаг 3: Переименовать `test/subtest/` → `test/demo/`

**Команда:** `/structure-modify` (переименование)

**Чек-лист после выполнения:**
- [ ] Папка `test/demo/` существует
- [ ] Папка `test/subtest/` НЕ существует
- [ ] `test/demo/README.md` — заголовок обновлён
- [ ] `test/README.md` — секция "Папки" обновлена
- [ ] `test/README.md` — дерево обновлено
- [ ] `/.structure/README.md` — ссылки обновлены (если были)
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит

---

## Шаг 4: Переместить `test/demo/` → `test-demo/` (в корень)

**Команда:** `/structure-modify` (перемещение)

**Чек-лист после выполнения:**
- [ ] Папка `test-demo/` существует в корне
- [ ] Папка `test/demo/` НЕ существует
- [ ] `test-demo/README.md` — заголовок с новым путём
- [ ] `test-demo/README.md` — "Полезные ссылки" обновлены
- [ ] `test-demo/README.md` — frontmatter (`index`) обновлён
- [ ] `test/README.md` — `demo/` удалена из секции "Папки" и дерева
- [ ] `/.structure/README.md` — секция `test-demo/` добавлена
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит

---

## Шаг 5: Удалить `test-demo/`

**Команда:** `/structure-modify` (удаление)

**Чек-лист после выполнения:**
- [ ] Папка `test-demo/` НЕ существует
- [ ] `/.structure/README.md` — секция `test-demo/` удалена
- [ ] `/.structure/README.md` — оглавление обновлено
- [ ] `/.structure/README.md` — дерево обновлено
- [ ] Нет битых ссылок на `test-demo/`
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит

---

## Шаг 6: Удалить `test/`

**Команда:** `/structure-modify` (удаление)

**Чек-лист после выполнения:**
- [ ] Папка `test/` НЕ существует
- [ ] `/.structure/README.md` — секция `test/` удалена
- [ ] Нет битых ссылок на `test/`
- [ ] `/structure-validate` проходит
- [ ] `/links-validate` проходит
- [ ] Проект в исходном состоянии

---

## Результаты

| Шаг | Статус | Замечания |
|-----|--------|-----------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |

---

## Найденные проблемы

| # | Шаг | Проблема | Файл | Статус |
|---|-----|----------|------|--------|
| 1 | 1 | `ssot.py add` неправильно выравнивает комментарии в дереве | `.scripts/ssot.py` | ✅ исправлено |
| 2 | 2 | Инструкция не указывает явно, что ВСЕ папки (включая подпапки) добавляются в SSOT | `create-structure.md` | ✅ исправлено |
| 3 | 2 | `ssot.py add` не поддерживает вложенные пути (`test/subtest` → добавляет `subtest/` в корень) | `.scripts/ssot.py` | ✅ исправлено |

---

## Выводы

*(заполнить после тестирования)*
