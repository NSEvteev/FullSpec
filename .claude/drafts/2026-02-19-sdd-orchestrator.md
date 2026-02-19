# Оркестратор: реализация SDD v2

Последовательность реализации новой модели SDD, таблица драфтов, зависимости, чеклист миграции.

## Контекст

**Задача:** Координация реализации всех объектных драфтов — от создания стандартов в specs/.instructions/ до заполнения первых docs/ документов.

**Источник:** `.claude/drafts/2026-02-19-sdd-chain-rethink.md` (декомпозирован на 8 объектных драфтов)

**Связанные файлы:**
- `2026-02-19-sdd-structure.md` — архитектурные решения и открытые вопросы
- `encapsulated-jumping-ocean.md` — план декомпозиции (исходный)

---

## Содержание

### Таблица драфтов

| # | Драфт | Прообраз | Статус | Зависит от |
|---|-------|---------|--------|-----------|
| 1 | [sdd-structure.md](2026-02-19-sdd-structure.md) | Архитектурные решения SDD v2 | done | — |
| 2 | [sdd-docs-readme.md](2026-02-19-sdd-docs-readme.md) | `specs/docs/README.md` | done | — |
| 3 | [sdd-docs-overview.md](2026-02-19-sdd-docs-overview.md) | `specs/docs/.system/overview.md` | done | — |
| 4 | [sdd-docs-conventions.md](2026-02-19-sdd-docs-conventions.md) | `specs/docs/.system/conventions.md` | done | — |
| 5 | [sdd-docs-infrastructure.md](2026-02-19-sdd-docs-infrastructure.md) | `specs/docs/.system/infrastructure.md` | done | — |
| 6 | [sdd-docs-testing.md](2026-02-19-sdd-docs-testing.md) | `specs/docs/.system/testing.md` | done | — |
| 7 | [sdd-docs-service.md](2026-02-19-sdd-docs-service.md) | `specs/docs/{svc}.md` | done | — |
| 8 | [sdd-docs-technology.md](2026-02-19-sdd-docs-technology.md) | `specs/docs/.technologies/standard-{tech}.md` | done | — |
| 9 | **sdd-orchestrator.md** (этот файл) | Координация | done | #1-#8 |

### Последовательность реализации

Из каждого драфта создаётся набор артефактов в `specs/.instructions/`:

| Фаза | Что делать | Входные драфты | Выходные артефакты | Статус |
|------|-----------|---------------|-------------------|--------|
| **0. Миграция** | Переместить старые specs/ в _old/ | — | `specs/_old/`, новая структура specs/ | **done** |
| **1. Мета-стандарт** | Написать верхнеуровневый стандарт docs/ + валидацию + стартовый набор | sdd-structure | `standard-docs.md`, `validation-docs.md`, `validate-docs.py`, pre-commit hook, `specs/docs/` (7 файлов) | **done** |
| **2. docs/README.md** | Стандарт + шаблон docs/README.md | sdd-docs-readme | `standard-readme.md`, `validation-readme.md`, `validate-docs-readme.py`, pre-commit hook | **done** |
| **3. overview.md** | Стандарт + шаблон overview.md | sdd-docs-overview | `standard-overview.md` (captain-holt: 16 рекомендаций), `validation-overview.md` (OVW001-OVW008), `validate-docs-overview.py`, `modify-overview.md` (6 сценариев), pre-commit hook | **done** |
| **4. conventions.md** | Стандарт + шаблон conventions.md | sdd-docs-conventions | `standard-conventions.md` (captain-holt: 10 рекомендаций), `validation-conventions.md` (CNV001-CNV007), `validate-docs-conventions.py`, `modify-conventions.md` (6 сценариев), pre-commit hook | **done** |
| **5. infrastructure.md** | Стандарт + шаблон infrastructure.md | sdd-docs-infrastructure | `standard-infrastructure.md` (captain-holt: 11 рекомендаций), `validation-infrastructure.md` (INF001-INF007), `validate-docs-infrastructure.py`, `modify-infrastructure.md` (6 сценариев), pre-commit hook | **done** |
| **6. testing.md** | Стандарт + шаблон testing.md | sdd-docs-testing | standard + validation | — |
| **7. {svc}.md** | Стандарт + шаблон сервисного документа | sdd-docs-service | standard + validation + create + modify | — |
| **8. standard-{tech}.md** | Стандарт + шаблон per-tech | sdd-docs-technology | standard + validation + create + modify | — |
| **9. analysis/** | Определить контур аналитики | **ОТЛОЖЕНО** | TBD | — |

**Зависимости:**
- Фазы 2-8 независимы друг от друга (можно параллельно)
- Фаза 1 (мета-стандарт) блокирует фазы 2-8
- Фаза 0 (миграция) блокирует фазы 1-8
- Фаза 9 (analysis/) отложена — открытые вопросы в sdd-structure.md

### Чеклист миграции specs/ → _old/

- [x] `specs/_old/` создана
- [x] `specs/discussion/` → `specs/_old/discussion/`
- [x] `specs/impact/` → `specs/_old/impact/`
- [x] `specs/design/` → `specs/_old/design/`
- [x] `specs/services/` → `specs/_old/services/`
- [x] `specs/architecture/` → `specs/_old/architecture/`
- [x] `specs/tests/` → `specs/_old/tests/`
- [x] `specs/technologies/` → `specs/_old/technologies/`
- [x] `specs/glossary/` → `specs/_old/glossary/`
- [x] `specs/.instructions/` → `specs/_old/.instructions/`
- [x] `specs/README.md` → `specs/_old/README.md`
- [x] Новые пустые папки: `specs/analysis/`, `specs/docs/`, `specs/.instructions/`
- [x] Новый `specs/README.md` — индекс с двумя контурами + ссылка на _old
- [x] `.claude/rules/` обновлены — нет ссылок на старые пути
- [x] Удалены устаревшие pre-commit хуки (service-labels, architecture, postgresql-code, redis-code)
- [x] Удалены устаревшие rules (postgresql.md, redis.md)
- [x] Стартовый набор `specs/docs/` создан (README, 4 системных, 2 примера)
- [x] Pre-commit хук `docs-validate` добавлен и работает

### Контур analysis/ — ОТЛОЖЕН

Будет создан после обсуждения. Открытые вопросы зафиксированы в [sdd-structure.md](2026-02-19-sdd-structure.md#открытые-вопросы):

1. Какие документы внутри `analysis/0001-.../`?
2. Аналитика — хранить или удалять после завершения?
3. Минимальная единица изменения для цепочки?
