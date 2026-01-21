# Инструкции /doc/

Индекс инструкций для работы с документацией проекта.

**Содержание:** структура `/doc/`, документирование кода, шаблоны, workflow документации.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Structure](#1-structure) | [structure.md](./structure.md) | Структура /doc/, документирование кода |
| [2. Templates](#2-templates) | [templates.md](./templates.md) | Шаблоны документации |
| [3. Rules](#3-rules) | [rules.md](./rules.md) | Правила для doc-* скиллов |

---

# 1. Structure

Правила организации документации в `/doc/` и документирования кода в `/src/`.

**Содержание:** принцип зеркалирования (код → документация), типы документов (README, ADR, Runbooks, Specs), структура сервиса, шаблоны документации, workflow от идеи до документации, скиллы /doc-*.

### Принцип зеркалирования

| Код | Документация |
|-----|--------------|
| `/src/auth/backend/handlers.ts` | `/doc/src/auth/backend/handlers.md` |
| `/shared/libs/errors/` | `/doc/shared/libs/errors.md` |
| `/platform/gateway/` | `/doc/platform/gateway/README.md` |

### Что зеркалируется

| Папка | Зеркалируется | Причина |
|-------|:-------------:|---------|
| `/src/` | Да | Сервисы требуют документации |
| `/shared/` | Да | Библиотеки и контракты |
| `/platform/` | Да | Инфраструктура, runbooks |
| `/config/` | Нет | Самодокументируемы |
| `/tests/` | Нет | Код = спецификация |

### Типы документов

| Тип | Расположение | Назначение |
|-----|--------------|------------|
| README.md | Корень папки | Точка входа, обзор |
| ADR | `/doc/src/{service}/specs/adr/` | Архитектурные решения |
| Runbooks | `/doc/runbooks/`, `/doc/src/{service}/runbooks/` | Эксплуатация |
| Specs | `/doc/src/{service}/specs/` | Архитектура, планы |

### Workflow документации

```
Дискуссия → ADR → План → Код → Документация
```

| Событие | Скилл |
|---------|-------|
| Создан файл в `/src/` | `/doc-create` |
| Изменён файл в `/src/` | `/doc-update` |
| Удалён файл из `/src/` | `/doc-delete` |

**Инструкция:** [structure.md](./structure.md)

---

# 2. Templates

Шаблоны документации для различных типов файлов.

**Содержание:** шаблоны backend, database, frontend, minimal; правила выбора шаблона; ссылки на файлы шаблонов.

### Файлы шаблонов

| Шаблон | Файл | Назначение |
|--------|------|------------|
| Backend | [backend-template.md](/.claude/templates/doc/backend-template.md) | handlers, services, controllers |
| Database | [database-template.md](/.claude/templates/doc/database-template.md) | schema, migrations |
| Frontend | [frontend-template.md](/.claude/templates/doc/frontend-template.md) | components, pages |
| Minimal | [minimal-template.md](/.claude/templates/doc/minimal-template.md) | утилиты, константы |

### Выбор шаблона

| Тип файла | Шаблон |
|-----------|--------|
| `handlers.ts`, `services.py` | Backend |
| `schema.sql`, `migrations/*.sql` | Database |
| `*.tsx`, `*.vue`, `pages/*.ts` | Frontend |
| `utils.ts`, `constants.py` | Minimal |

**Инструкция:** [templates.md](./templates.md)

---

# 3. Rules

Правила документации для doc-* скиллов (doc-create, doc-update, doc-delete).

**Содержание:** маппинг путей, валидация, поддерживаемые языки, шаблон документации, формат пометки.

### Маппинг путей

```
/{any-path}/{file}.{ext} → /doc/{any-path}/{file}.md
```

### Исключённые пути

| Путь | Причина |
|------|---------|
| `/doc/**` | Целевая папка документации |
| `/.claude/**` | Уже содержит документацию |
| `/.git/**` | Служебные файлы |
| `/tests/**` | Описываются в инструкциях |

### Связанные скиллы

| Событие | Скилл |
|---------|-------|
| Создан файл | `/doc-create` |
| Изменён файл | `/doc-update` |
| Удалён файл | `/doc-delete` |

**Инструкция:** [rules.md](./rules.md)

