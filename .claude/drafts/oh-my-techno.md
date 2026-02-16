# План: Технологии + скрипт-генератор заглушек + интеграция в Design

## Контекст

После реализации обогащения заглушек (Design → WAITING заполняет секции 2, 3, 5 предварительными данными) выявлены три связанных улучшения:

1. **Скрипт-генератор заглушек** — автоматизация создания `services/{svc}.md` (сейчас всё на LLM)
2. **Технологии** — `standard-technology.md` проработан хорошо (10 секций, шаблоны, примеры), но: нет create/modify/validation воркфлоу, скиллов; триггер создания устаревший (ADR → DONE вместо Design → WAITING)
3. **Интеграция технологий в Design** — Design выбирает Tech Stack, но не учитывает уже используемые технологии и не создаёт per-tech стандарты при WAITING

## Разрешённые вопросы

### Насколько проработан standard-technology.md?

**Проработан хорошо** — 10 секций, шаблоны (standard-{tech}.md, validation-{tech}.md, rule), примеры, чек-лист. Существенная доработка не нужна. Нужно:
- Обновить § 4 (триггер): Design → WAITING (заглушка) вместо ADR → DONE
- Добавить двухфазную модель: заглушка при Design → WAITING, заполнение при ADR → DONE

### Формат: один файл на технологию или группами?

**Один файл на технологию** — уже определено в standard-technology.md § 2 (`standard-{tech}.md`). Отдельные "описания технологий" (`specs/technologies/{tech}.md`) НЕ нужны — per-tech стандарт выполняет двойную роль:

| Роль | Когда | Пример (Tailwind CSS) |
|------|-------|-----------------------|
| **Декларация выбора** | Design → WAITING (заглушка) | "Проект использует Tailwind CSS 3.4 для стилизации frontend" |
| **Конвенции кодирования** | ADR → DONE (заполнение) | "Использовать utility-классы, избегать @apply, именование кастомных классов" |

Реестр технологий (`specs/technologies/README.md`) — сводная таблица для Quick/Deep Scan.

### Нужен ли technology-agent?

**Да, нужен.** При Design → WAITING может добавляться несколько технологий одновременно (например, Python + FastAPI + PostgreSQL + Redis). Каждая технология обрабатывается отдельным агентом параллельно — 5 технологий = 5 агентов. Агент получает на вход одну технологию и создаёт/обновляет: `standard-{tech}.md` (заглушка или заполнение), `validation-{tech}.md`, rule в `.claude/rules/`, строку реестра.

---

## Часть 1: Скрипт create-service-file.py

### Зачем
Создание заглушки — шаблонная операция. При 4+ сервисах LLM тратит контекст на повторяющийся маппинг. Скрипт делает это за один вызов.

### Что сделать
- `/script-create` → `specs/.instructions/.scripts/create-service-file.py`
- Паттерн: как `create-design-file.py` и `create-impact-file.py` (argparse, шаблон, извлечение данных)
- Параметры: `--design <path>`, `--impact <path>`, `--svc <name>`, `[--topic <description>]`
- Логика:
  1. Прочитать Design → найти SVC-N для указанного сервиса → извлечь назначение, Dependencies
  2. Прочитать Impact → найти SVC-N → извлечь API-N, DATA-N
  3. Прочитать Design INT-N → извлечь контракты для дополнительных зависимостей
  4. Сгенерировать `services/{svc}.md` по шаблону заглушки из standard-service.md § 9.1
- `/instruction-modify` → обновить create-service.md (шаг 2: вызов скрипта вместо ручного создания)
- `/skill-modify` → обновить SKILL.md service-create (вызов скрипта)

## Часть 2: Технологии — воркфлоу и инструменты

### Зачем
Design принимает решения о Tech Stack (Python, FastAPI, PostgreSQL и т.д.). Per-tech стандарт нужно объявить ДО начала написания кода — сначала стандарт, потом его использование. Но:
- Текущий триггер в standard-technology.md § 4 — ADR → DONE (устаревший, по аналогии со старым триггером для сервисов)
- Нет воркфлоу создания/модификации per-tech стандартов
- Нет скиллов

### Что сделать

#### 2.1 Обновить standard-technology.md

**§ 4 Триггер создания:** Перенести с ADR → DONE на двухфазную модель:

| Фаза | Триггер | Что создаётся |
|------|---------|---------------|
| **Заглушка** | Design → WAITING | `standard-{tech}.md` (§ 1 Версия и источники заполнен, § 2-6 placeholder), `validation-{tech}.md` (заглушка), rule в `.claude/rules/`, строка в реестре |
| **Заполнение** | ADR → DONE | `standard-{tech}.md` заполняется конвенциями (§ 2-6), `validation-{tech}.md` заполняется кодами ошибок |

**Шаблон заглушки:** Добавить § 7.4 — шаблон заглушки per-tech стандарта (по аналогии с standard-service.md § 9.1). Секция § 1 (Версия и источники) заполняется сразу. Секции § 2-6 — placeholder `*Заполняется при ADR → DONE.*`.

**Каскад:** Обновить дерево каскада (§ 4) — Design → WAITING вместо ADR → DONE.

**Откат:** Добавить описание отката:
- Design → ROLLING_BACK: удалить заглушки стандартов + rule + строку реестра
- ADR → ROLLING_BACK: вернуть стандарт к состоянию заглушки

#### 2.2 Создать воркфлоу (через `/instruction-create`)

- `/instruction-create` → `create-technology.md` — создание per-tech стандарта (заглушка при Design → WAITING + заполнение при ADR → DONE)
- `/instruction-create` → `modify-technology.md` — обновление при: новый сервис использует технологию, изменение версии, обновление конвенций
- `/instruction-create` → `validation-technology.md` — валидация per-tech стандарта (frontmatter, секции, rule, реестр)

#### 2.3 Создать скрипт (через `/script-create`)

- `/script-create` → `validate-technology.py` — автоматическая валидация per-tech стандартов

#### 2.4 Создать technology-agent (через `/agent-create`)

- `/agent-create` → `AGENT.md` в `.claude/agents/technology-agent/`
- Вход: одна технология (имя, версия, назначение, сервисы)
- Выход: `standard-{tech}.md` + `validation-{tech}.md` + rule + строка реестра
- Режимы: создание заглушки (Design → WAITING), заполнение конвенциями (ADR → DONE), обновление (новый сервис)
- Параллельный запуск: оркестратор запускает N агентов для N технологий

#### 2.5 Создать скиллы (через `/skill-create`)

- `/skill-create` → `/technology-create` — создание per-tech стандартов (запускает N technology-agent параллельно, по одному на технологию)
- `/skill-create` → `/technology-modify` — обновление per-tech стандартов (запускает N technology-agent параллельно)
- `/skill-create` → `/technology-validate` — валидация

#### 2.6 Обновить README

- `specs/.instructions/technologies/README.md` — добавить ссылки на воркфлоу и скиллы
- `specs/technologies/README.md` — формат реестра (если менялся)

## Часть 3: Интеграция технологий в Design

### Зачем
Design-agent при Deep Scan должен учитывать уже выбранные технологии (реестр + per-tech стандарты). А при WAITING — создавать заглушки per-tech стандартов для новых технологий.

### Что сделать

#### 3.1 Deep Scan: 6-й источник

- Обновить `standard-design.md § 1` — Deep Scan: добавить 6-й источник `specs/technologies/`
- Обновить таблицу "Что читать" — `specs/technologies/README.md` (реестр) + per-tech стандарты
- Обновить `create-design.md` — шаг 4 (design-agent читает технологии)
- Обновить AGENT.md design-agent — промпт включает чтение технологий

#### 3.2 Артефакт "per-tech стандарты" при Design → WAITING

- Обновить `standard-design.md § 4` — артефакт 5: per-tech стандарты (заглушки)
- Обновить `create-design.md` шаг 9 — артефакт 5: для каждой новой технологии вызвать `/technology-create`
- Обновить `create-design.md` шаг 9 — для существующей технологии + новый сервис → `/technology-modify` (обновить колонку "Сервисы" в реестре)
- Обновить таблицу артефактов Design → WAITING (было 4 типа, станет 5)

#### 3.3 Code Map → Tech Stack ссылки

- В standard-service.md § 5.4 уже есть: "При наличии standard-{tech}.md — таблица Tech Stack дополняется ссылками"
- Убедиться что при ADR → DONE (заполнение Code Map) ссылки на per-tech стандарты добавляются

#### 3.4 Обновить standard-specs.md

- **Решение #36:** Обновить — двухфазная модель (Design → WAITING заглушка, ADR → DONE заполнение)
- **§ 7 таблица живых документов:** Добавить строку "Технологический реестр" (`specs/technologies/README.md`)
- **§ 7.1:** Добавить Design → WAITING создаёт заглушки per-tech стандартов + обновляет реестр
- **§ 7.3:** Добавить ADR → DONE заполняет per-tech стандарты конвенциями
- **Откат (строка 721-722):** Design-уровень: удалить заглушки per-tech стандартов. ADR-уровень: вернуть к заглушкам (уже частично есть)

## Порядок реализации

1. **Часть 2** (технологии) — обновить standard-technology.md § 4 → воркфлоу → скрипт → скиллы
2. **Часть 3** (интеграция) — Deep Scan + артефакт при WAITING + standard-specs.md
3. **Часть 1** (скрипт заглушек) — create-service-file.py
4. **Миграция** — standard-technology.md, standard-design.md (если менялся)
5. **Верификация** — проверить, что в `specs/.instructions/standard-specs.md` работа с технологиями описана корректно (решение #36, § 7, § 7.1, § 7.3, откат Design/ADR)
