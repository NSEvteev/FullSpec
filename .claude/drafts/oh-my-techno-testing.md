# Драфт-план тестирования: oh-my-techno + Design + Impact + Service

## Scope

Тестирование изменений из нескольких сессий (5 коммитов + текущие unstaged). Затронуто 27 modified + 31 untracked файлов.

---

## 1. Скрипты валидации

### 1.1 validate-technology.py
- [x] Запуск без аргументов (нет per-tech стандартов) — path обязателен, ожидание: usage error
- [x] Запуск на несуществующем файле — ожидание: ошибка "Путь не найден"
- [x] Запуск на папке `specs/.instructions/technologies/` — не подхватывает `standard-technology.md` → "Нет файлов для валидации"
- [ ] ~~Запуск с `--json` флагом~~ — флаг не реализован (нет `--json`)

### 1.2 validate-design.py
- [x] Запуск на `design-0001-realtime-notifications.md` — OK
- [x] Запуск с `--all` — OK
- [x] Проверка frontmatter `standard-version: v1.1` — скрипт принимает

### 1.3 validate-impact.py
- [x] Запуск на `impact-0001-realtime-notifications.md` — OK
- [x] Запуск с `--all` — OK

### 1.4 validate-service.py
- [x] Запуск на заглушке — режим заглушки, единственная ошибка SVC012 (не в README) — ожидаемо
- [x] ~~Проверка: секции 2, 3, 5 с маркером Planned~~ — проверено через создание test-svc
- [x] ~~Проверка: секции 4, 6 с placeholder~~ — проверено через создание test-svc

### 1.5 create-service-file.py
- [x] `--help` — корректный вывод
- [x] `--svc auth --design specs/design/design-0001-realtime-notifications.md` — создаёт файл
- [x] Frontmatter (description, service) заполнены
- [x] Planned Changes ссылаются на правильные Discussion/Design
- [x] Секции 2, 3, 5 — маркер Planned; секции 4, 6 — placeholder
- [x] Повторный запуск — FileExistsError
- [x] Невалидное имя сервиса (CamelCase) — ошибка
- [ ] ~~Design не в WAITING~~ — не тестировали (требует ручное изменение status)

### 1.6 create-design-file.py
- [x] Шаблон содержит `standard-version: v1.1`

### 1.7 create-impact-file.py
- [x] Базовая проверка (`--help`) — OK, корректный вывод

---

## 2. Инструкции — консистентность

### 2.1 standard-design.md (v1.0 → v1.1)
- [x] § 1: Deep Scan таблица — 6 строк
- [x] § 1: "6 источников" в тексте
- [x] § 1: "5 артефактов" в описании WAITING
- [x] § 4: таблица артефактов — 5 строк
- [x] § 3: шаблон frontmatter — `standard-version: v1.1`
- [x] § 6: "6 источников" в описании Clarify
- [x] § 7: шаблон документа — `standard-version: v1.1`
- [x] `/links-validate` — 2 E003 найдены и исправлены (двойные дефисы `--` в якорях, устаревший якорь `#4-триггеры-создания-и-обновления`)

### 2.2 create-design.md
- [x] Архитектура процесса: "6 источников"
- [x] Принципы: "5 типов артефактов"
- [x] Шаг 4: таблица — "6 источников"
- [x] Шаг 9: таблица — 5 строк (артефакт 4 = per-tech, артефакт 5 = ADR)
- [x] Шаг 9: порядок "1-4 перед ADR (артефакт 5)"
- [x] Чек-лист: "6 источников", "Per-tech стандарты"
- [x] Frontmatter: `standard-version: v1.1`

### 2.3 standard-technology.md (v1.1) — проверялось в предыдущих сессиях
### 2.4 Technologies workflows — проверялось в предыдущих сессиях

### 2.5 standard-specs.md
- [x] Решение #36 — двухфазная модель (строка 988)
- [x] § 7: строка "Технологический реестр" (строка 748)
- [x] § 7.1: Design → WAITING создаёт per-tech заглушки (строка 756)
- [x] § 7.3: ADR → DONE заполняет per-tech стандарты (строка 783)
- [x] Откат Design: удаление per-tech заглушек (строка 721)
- [x] Откат ADR: возврат к заглушкам (строка 722)

### 2.6 create-service.md
- [x] Шаг 1: извлечение API-N, DATA-N, Dependencies
- [x] Шаг 2: вызов скрипта `create-service-file.py`
- [x] Шаг 3: маппинг данных (таблица)
- [x] Чек-лист: секции 2, 3, 5 — предварительные данные ИЛИ placeholder
- [x] Таблица скриптов: `create-service-file.py` в списке

### 2.7 standard-service.md — проверялось в предыдущих сессиях

---

## 3. Агенты

### 3.1 design-agent
- [x] Deep Scan таблица — 6 строк
- [x] "6 источников" в описании
- [x] Fallback: "Если `specs/technologies/` не существует — пропустить источник 6"
- [x] CHANGELOG исправлен: 5 → 6 источников

### 3.2 design-reviewer
- [x] AGENT.md существует и валиден

### 3.3 impact-reviewer
- [x] AGENT.md существует и валиден

### 3.4 technology-agent
- [x] 3 режима: stub, fill, update — проверено при создании
- [x] Globs таблица — проверено при создании
- [x] Anti-hallucination правила — проверено при создании
- [x] Ограничения — проверено при создании

### 3.5 Валидация всех агентов
- [x] design-agent — OK
- [x] design-reviewer — OK
- [x] impact-reviewer — OK
- [x] technology-agent — OK

---

## 4. Скиллы

### 4.1-4.3 Контент скиллов — проверено при создании

### 4.4 Валидация всех новых скиллов
- [x] design-create — OK (42 строк)
- [x] design-modify — OK (42 строк)
- [x] design-validate — OK (43 строк)
- [x] technology-create — OK (47 строк)
- [x] technology-modify — OK (44 строк)
- [x] technology-validate — OK (41 строк)
- [x] service-create — OK (48 строк)
- [x] service-modify — OK (44 строк)

---

## 5. README и индексы

- [x] `specs/design/README.md` — design-0001 в таблице
- [x] `specs/discussion/README.md` — disc-0001 в таблице
- [x] `specs/impact/README.md` — impact-0001 в таблице
- [x] `.claude/.instructions/agents/README.md` — 4 агента (проверено при создании)
- [x] `.claude/skills/README.md` — все скиллы (проверено при создании)
- [x] `specs/.instructions/design/README.md` — OK (5 файлов, 2 скрипта, 3 скилла, дерево совпадает)
- [x] `specs/.instructions/technologies/README.md` — OK (5 файлов, 1 скрипт, 3 скилла, дерево совпадает)

---

## 6. Кросс-ссылки

- [x] Нет устаревших "5 источников" или "4 артефакта" в Design файлах
- [x] `v1.0` присутствует ТОЛЬКО в frontmatter standard-design.md (ссылка на standard-instruction.md)
- [x] `/links-validate` полный прогон — 36 ошибок найдено и исправлено (двойные дефисы, пути скриптов, относительные пути агентов, якоря скиллов). Остались 4 ожидаемых false positive: шаблонные пути `standard-{tech}.md`, `standard-python.md`, несуществующий `standard-adr.md`

---

## 7. SDD-цепочка (интеграционный тест)

- [x] disc-0001 → impact-0001 → design-0001: parent/children ссылки согласованы
- [x] Все 3 документа проходят валидацию скриптами
- [x] README всех трёх папок содержат записи

---

## 8. Принципы кода

- [x] create-service-file.py — OK
- [x] create-design-file.py — OK
- [x] validate-design.py — OK (после fix: extract_file_nnnn)
- [x] validate-technology.py — OK
- [x] validate-impact.py — OK
- [x] validate-service.py — OK (после fix: iter_lines_outside_code + docstring)

---

## Найденные и исправленные проблемы

| # | Проблема | Файл | Исправление |
|---|----------|------|-------------|
| 1 | P002: дублирование FILENAME_REGEX.match | validate-design.py | Хелпер `extract_file_nnnn()` |
| 2 | P002: дублирование code-block логики (8 строк) | validate-service.py | `iter_lines_outside_code()` + `extract_headings()` |
| 3 | P006: main() без docstring | validate-service.py | Добавлен docstring |
| 4 | "5 источников" в CHANGELOG | design-agent/CHANGELOG.md | Исправлено на "6 источников" |
| 5 | E003: двойные дефисы `--` в якорях (символ `→`) | 10 файлов (standard-specs, technologies/*, service/*, agents/*) | `--waiting` → `-waiting`, `--done` → `-done`, `--adr` → `-adr` и др. |
| 6 | E001: неверный путь `../../.scripts/` | technologies/{create,modify,validation,README} | `../../.scripts/` → `../.scripts/` |
| 7 | E001: относительные пути без `/` в агентах | agents/{design-agent,design-reviewer,impact-reviewer} | `(specs/` → `(/specs/` |
| 8 | E003: устаревшие якоря в оглавлении | service/create-service.md | Обновлены на актуальные заголовки |
| 9 | E003: устаревший якорь `#4-триггеры-создания-и-обновления` | design/standard-design.md | `#4-триггер-создания` |
| 10 | E003: устаревшие якоря `#5-чек-лист` | skills/instruction-{create,modify} | `#чек-лист` |
