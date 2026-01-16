# Ресурсы: Правила работы

## О файлах в этой папке

**Этот файл (README.md) — КАК:**
- Статичные правила работы с [📖 ресурсами](../glossary.md#ресурс)
- Структура по категориям
- Требования к полноте описания
- **Для LLM:** Инструкции по ресурсам

**Файл 000_resources.md — ЧТО:**
- Динамический индекс всех ресурсов
- Статистика по категориям
- **Для LLM:** Обзор ресурсов

**Файл [000_SUMMARY.md](000_SUMMARY.md) — ЗАЧЕМ:**
- **Агрегация ресурсов** для обзора всех технических компонентов
- Содержит краткое описание всех ресурсов по категориям
- Обновляется вручную при создании или изменении ресурсов
- **Для LLM:** Контекст при работе с планами реализации

---

**Индекс:** См. [000_resources.md](000_resources.md)

**Полная инструкция:** [general_docs.md](../../llm_instructions/general_docs.md#ресурсы-resources)

---

## Назначение

Детальное описание всех ресурсов системы.

**[📖 Ресурс](../glossary.md#ресурс)** — компонент системы (БД, сервис, API), который:
- Описан детально (схема, API, конфигурация)
- Определен в ADR
- Используется в реализации

---

## Структура

**Принцип:** Ресурсы организованы по **типу**, затем по **сервису**. Имена файлов соответствуют именам файлов в `src/`.

```
05_resources/
├── 000_resources.md         # Общий индекс
├── README.md                # Общие правила
│
├── database/                # Ресурсы БД
│   ├── 000_database.md      # Индекс БД-ресурсов
│   ├── README.md
│   └── [service-name]/      # Папка сервиса
│       ├── 000_SUMMARY.md   # Агрегация БД-компонентов сервиса
│       ├── email_queue.md   # Описание таблицы (имя = имя таблицы)
│       └── email_templates.md
│
├── backend/                 # Бэкенд-ресурсы
│   ├── 000_backend.md
│   ├── README.md
│   └── [service-name]/
│       ├── 000_SUMMARY.md   # Агрегация бэкенд-компонентов сервиса
│       ├── notification.service.md  # (имя = имя файла в src/)
│       └── email.worker.md
│
├── frontend/                # Фронтенд-ресурсы
│   ├── 000_frontend.md
│   ├── README.md
│   └── [feature-name]/      # Папка фичи/компонента
│       ├── 000_SUMMARY.md
│       ├── NotificationSettingsPage.md
│       └── NotificationToggle.md
│
└── infra/                   # Инфраструктурные ресурсы
    ├── 000_infra.md
    ├── README.md
    └── [service-name]/
        ├── 000_SUMMARY.md
        └── redis_queue.md
```

### Связь с IT-сервисами

Каждая папка `[service-name]/` соответствует [📖 IT-сервису](../glossary.md#it-сервис) из `00_services/`:

```
00_services/notification-service/
        ↓
05_resources/backend/notification-service/
05_resources/database/notification-service/
05_resources/frontend/notification-settings/
05_resources/infra/notification-service/
```

---

## Именование

### Папки сервисов

- Формат: `[service-name]/` (kebab-case)
- Пример: `notification-service/`, `auth-service/`
- Имя соответствует сервису в `00_services/`

### Файлы ресурсов

- Формат: `[имя_как_в_src].md`
- Имя файла = имя файла в кодовой базе (с расширением `.md`)

**Примеры:**

| Тип | Файл в src/ | Файл в resources/ |
|-----|-------------|-------------------|
| backend | `notification.service.ts` | `notification.service.md` |
| database | таблица `email_queue` | `email_queue.md` |
| frontend | `NotificationSettingsPage.tsx` | `NotificationSettingsPage.md` |
| infra | конфиг Redis | `redis_queue.md` |

---

## Требования

См. README.md в каждой категории:
- [database/README.md](database/README.md)
- [backend/README.md](backend/README.md)
- [frontend/README.md](frontend/README.md)
- [infra/README.md](infra/README.md)

---

## Связь с документами

**Входящие:** Архитектура → Ресурс

**Исходящие:** Ресурс → План, Документация папок

**Цепочка:**
```
Дискуссия → Архитектура → [Ресурсы] → План → Документация папок
```

---

## Обратная связь

При изменении ресурса:
1. Обновить архитектуру (если существенно)
2. Обновить документацию папок
3. Обновить индекс

Чек-лист:
- [ ] Обновлен индекс категории
- [ ] Обновлена архитектура (если нужно)
- [ ] Обновлена документация папок

---

**Шаблон:** [templates/resource.md](../../llm_instructions/templates/resource.md)

**Связанные папки:**
- [02_architecture/](../02_architecture/)
- [06_imp_plans/](../06_imp_plans/)

---

**Последнее обновление:** 2026-01-15
**Версия:** 1.0
