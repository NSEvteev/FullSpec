# Драфт-план тестирования: oh-my-techno + Design + Impact + Service

## Scope

Тестирование изменений из нескольких сессий (5 коммитов + текущие unstaged). Затронуто 27 modified + 31 untracked файлов.

---

## 1. Скрипты валидации

### 1.1 validate-technology.py
- [ ] Запуск без аргументов (нет per-tech стандартов) — ожидание: "Нет per-tech стандартов"
- [ ] Запуск на несуществующем файле — ожидание: ошибка
- [ ] Запуск на папке `specs/.instructions/technologies/` — не должен подхватить `standard-technology.md` (мета-стандарт)
- [ ] Запуск с `--json` флагом — корректный JSON-вывод

### 1.2 validate-design.py
- [ ] Запуск на `design-0001-realtime-notifications.md` — ожидание: OK
- [ ] Запуск с `--all` — ожидание: валидация всех Design-документов
- [ ] Проверка frontmatter `standard-version: v1.1` — скрипт принимает

### 1.3 validate-impact.py
- [ ] Запуск на `impact-0001-realtime-notifications.md` — ожидание: OK
- [ ] Запуск с `--all` — валидация всех Impact-документов

### 1.4 validate-service.py
- [ ] Запуск на пустом сервисе — режим заглушки
- [ ] Проверка: секции 2, 3, 5 с маркером Planned — валидны
- [ ] Проверка: секции 4, 6 с placeholder — валидны

### 1.5 create-service-file.py
- [ ] `--help` — корректный вывод
- [ ] `--svc auth --design specs/design/design-0001-realtime-notifications.md` — создаёт файл
- [ ] Проверить: frontmatter (description, service) заполнены
- [ ] Проверить: Planned Changes ссылаются на правильные Discussion/Design
- [ ] Проверить: секции 2, 3, 5 — маркер Planned; секции 4, 6 — placeholder
- [ ] Повторный запуск — FileExistsError
- [ ] Невалидное имя сервиса (CamelCase) — ошибка
- [ ] Design не в WAITING — ошибка

### 1.6 create-design-file.py
- [ ] Проверить: шаблон содержит `standard-version: v1.1`
- [ ] Создание файла — `standard-version: v1.1` в результате

### 1.7 create-impact-file.py
- [ ] Базовая проверка: создание файла из parent Discussion

---

## 2. Инструкции — консистентность

### 2.1 standard-design.md (v1.0 → v1.1)
- [ ] § 1: Deep Scan таблица — 6 строк (5 + технологии)
- [ ] § 1: "6 источников" в тексте
- [ ] § 1: "5 артефактов" в описании WAITING
- [ ] § 4: таблица артефактов — 5 строк (Planned Changes × 2, заглушки, per-tech, ADR)
- [ ] § 3: шаблон frontmatter — `standard-version: v1.1`
- [ ] § 6: "6 источников" в описании Clarify
- [ ] § 7: шаблон документа — `standard-version: v1.1`
- [ ] Все ссылки валидны (`/links-validate`)

### 2.2 create-design.md
- [ ] Архитектура процесса: "6 источников"
- [ ] Принципы: "5 типов артефактов"
- [ ] Шаг 4: таблица — "6 источников"
- [ ] Шаг 9: таблица — 5 строк (артефакт 4 = per-tech, артефакт 5 = ADR)
- [ ] Шаг 9: порядок "1-4 перед ADR (артефакт 5)"
- [ ] Чек-лист: "6 источников", "Per-tech стандарты"
- [ ] Frontmatter: `standard-version: v1.1`

### 2.3 standard-technology.md (v1.1)
- [ ] § 4: двухфазная модель (Design → WAITING заглушка, ADR → DONE заполнение)
- [ ] § 7: шаблоны заглушки и полного стандарта
- [ ] § 8: описание отката (Design/ADR уровни)
- [ ] Все ссылки валидны

### 2.4 Technologies workflows
- [ ] `create-technology.md` — ссылки, чек-лист, примеры
- [ ] `modify-technology.md` — 5 сценариев (A-E), чек-лист
- [ ] `validation-technology.md` — коды ошибок, чек-лист

### 2.5 standard-specs.md
- [ ] Решение #36 — двухфазная модель
- [ ] § 7: строка "Технологический реестр"
- [ ] § 7.1: Design → WAITING создаёт per-tech заглушки
- [ ] § 7.3: ADR → DONE заполняет per-tech стандарты
- [ ] Откат Design: удаление per-tech заглушек
- [ ] Откат ADR: возврат к заглушкам

### 2.6 create-service.md
- [ ] Шаг 1: извлечение API-N, DATA-N, Dependencies
- [ ] Шаг 2: вызов скрипта `create-service-file.py`
- [ ] Шаг 3: маппинг данных (таблица)
- [ ] Чек-лист: секции 2, 3, 5 — предварительные данные ИЛИ placeholder
- [ ] Таблица скриптов: `create-service-file.py` в списке

### 2.7 standard-service.md
- [ ] § 9.1 шаблон заглушки: маркер Planned в секциях 2, 3, 5
- [ ] § 9.1 шаблон заглушки: placeholder в секциях 4, 6
- [ ] Маппинг данных: Impact API-N, DATA-N → секции; Design Dependencies, INT-N → секции

---

## 3. Агенты

### 3.1 design-agent
- [ ] Deep Scan таблица — 6 строк (5 + технологии)
- [ ] "6 источников" в описании
- [ ] Fallback: "Если `specs/technologies/` не существует — пропустить источник 6"

### 3.2 design-reviewer
- [ ] AGENT.md существует и валиден

### 3.3 impact-reviewer
- [ ] AGENT.md существует и валиден

### 3.4 technology-agent
- [ ] 3 режима: stub, fill, update
- [ ] Globs таблица для разных технологий
- [ ] Anti-hallucination правила
- [ ] Ограничения (только свои файлы)

### 3.5 Валидация всех агентов
- [ ] `python .claude/.instructions/.scripts/validate-agent.py .claude/agents/design-agent`
- [ ] `python .claude/.instructions/.scripts/validate-agent.py .claude/agents/design-reviewer`
- [ ] `python .claude/.instructions/.scripts/validate-agent.py .claude/agents/impact-reviewer`
- [ ] `python .claude/.instructions/.scripts/validate-agent.py .claude/agents/technology-agent`

---

## 4. Скиллы

### 4.1 Новые скиллы
- [ ] `design-create/SKILL.md` — SSOT ссылка, параметры, примеры
- [ ] `design-modify/SKILL.md` — SSOT ссылка, параметры
- [ ] `design-validate/SKILL.md` — SSOT ссылка, параметры
- [ ] `technology-create/SKILL.md` — SSOT ссылка, параллельный запуск
- [ ] `technology-modify/SKILL.md` — SSOT ссылка, 5 сценариев
- [ ] `technology-validate/SKILL.md` — SSOT ссылка

### 4.2 Изменённые скиллы
- [ ] `service-create/SKILL.md` — параметры `--design`, `--impact`
- [ ] `service-modify/SKILL.md` — проверить актуальность

### 4.3 skills/README.md
- [ ] Категория specs: 3 technology скилла в списке
- [ ] Категория specs: 3 design скилла в списке

### 4.4 Валидация всех новых скиллов
- [ ] `python .claude/.instructions/.scripts/validate-skill.py .claude/skills/design-create`
- [ ] `python .claude/.instructions/.scripts/validate-skill.py .claude/skills/design-modify`
- [ ] `python .claude/.instructions/.scripts/validate-skill.py .claude/skills/design-validate`
- [ ] `python .claude/.instructions/.scripts/validate-skill.py .claude/skills/technology-create`
- [ ] `python .claude/.instructions/.scripts/validate-skill.py .claude/skills/technology-modify`
- [ ] `python .claude/.instructions/.scripts/validate-skill.py .claude/skills/technology-validate`

---

## 5. README и индексы

- [ ] `specs/.instructions/design/README.md` — все 4 файла в таблице
- [ ] `specs/.instructions/technologies/README.md` — все файлы (standard, create, modify, validation)
- [ ] `specs/design/README.md` — design-0001 в таблице
- [ ] `specs/discussion/README.md` — disc-0001 в таблице
- [ ] `specs/impact/README.md` — impact-0001 в таблице
- [ ] `.claude/.instructions/agents/README.md` — 4 агента в таблице
- [ ] `.claude/skills/README.md` — все скиллы

---

## 6. Кросс-ссылки

- [ ] `/links-validate` на изменённых файлах — все ссылки резолвятся
- [ ] Grep: нет битых ссылок на `standard-design.md#` (якоря после переименования секций)
- [ ] Grep: нет ссылок на `v1.0` в контексте Design (должно быть `v1.1`)

---

## 7. SDD-цепочка (интеграционный тест)

- [ ] disc-0001 → impact-0001 → design-0001: parent/children ссылки согласованы
- [ ] Все 3 документа проходят валидацию своими скриптами
- [ ] README всех трёх папок содержат записи

---

## 8. Принципы кода

- [ ] `validate-principles.py` на всех новых/изменённых Python-скриптах:
  - `create-service-file.py`
  - `create-design-file.py`
  - `validate-design.py`
  - `validate-technology.py`
  - `validate-impact.py`
  - `validate-service.py`
