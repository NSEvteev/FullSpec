# План миграции инструкций

План перехода от текущей структуры `/.claude/instructions/` к новой.

**Связанные документы:**
- [new_structure_of_project.md](./new_structure_of_project.md) — целевая структура
- [refactoting-claude-and-instructions.md](./refactoting-claude-and-instructions.md) — история рефакторинга
- [workflow-refactoring.md](./workflow-refactoring.md) — воркфлоу рефакторинга

---

## 0. Таблица миграции

> Все пути относительно `/.claude/instructions/`

| Новая папка | Старая папка | Рефакторинг | Миграция | Верификация 1 | Верификация 2 |
|-------------|--------------|:-----------:|:--------:|:-------------:|:-------------:|
| **service/** | | | | | |
| `service/*.md` | `services/*.md` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/api/` | `src/api/` + `src/runtime/realtime.md` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/data/` | `src/data/` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/database/` | `src/runtime/database.md` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/dev/` | `src/dev/` (local.md, performance.md) | ⬜ | ✅ | ⬜ | ⬜ |
| `service/health/` | `src/runtime/health.md` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/resilience/` | `src/runtime/resilience.md` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/security/` | `src/security/` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/testing/` | `src/dev/testing.md` + `tests/unit.md` | ⬜ | ✅ | ⬜ | ⬜ |
| `service/frontend/` | — (новая) | — | ✅ | ⬜ | ⬜ |
| **system/** | | | | | |
| `system/platform/` | `platform/` | ⬜ | ✅ | ⬜ | ⬜ |
| `system/platform/observability/` | `platform/observability/` | ⬜ | ✅ | ⬜ | ⬜ |
| `system/tests/` | `tests/` (без unit.md, claude-*.md) | ⬜ | ✅ | ⬜ | ⬜ |
| `system/shared/` | `shared/` (без scope.md) | ⬜ | ✅ | ⬜ | ⬜ |
| `system/config/` | `config/` | ⬜ | ✅ | ⬜ | ⬜ |
| **workflow/** | | | | | |
| `workflow/git/` | `git/` (без ci.md) | ⬜ | ✅ | ⬜ | ⬜ |
| `workflow/github/` | — (новая, + git/ci.md) | — | ✅ | ⬜ | ⬜ |
| `workflow/github/issues/` | `issues/` | ⬜ | ✅ | ⬜ | ⬜ |
| `workflow/specs/` | `specs/` | ✅ | ✅ | ⬜ | ⬜ |
| `workflow/docs/` | `docs/` | ⬜ | ✅ | ⬜ | ⬜ |
| **meta/** | | | | | |
| `meta/instructions/` | `instructions/` | ✅ | ✅ | ⬜ | ⬜ |
| `meta/links/` | `links/` | ✅ | ✅ | ⬜ | ⬜ |
| `meta/skills/` | `skills/` | 🔄 | ✅ | ⬜ | ⬜ |
| `meta/agents/` | — (новая) | — | ✅ | ⬜ | ⬜ |
| `meta/scripts/` | — (новая) | — | ✅ | ⬜ | ⬜ |
| `meta/state/` | — (новая) | — | ✅ | ⬜ | ⬜ |
| `meta/templates/` | — (новая) | — | ✅ | ⬜ | ⬜ |

**Легенда:**
- ⬜ Не начато
- 🔄 В процессе
- ✅ Готово
- — Не применимо (новая папка)

**Колонки:**
- **Рефакторинг:** Внутренняя переработка содержимого (SSOT, README, скиллы)
- **Миграция:** Перемещение в новую структуру папок
- **Верификация 1:** Проверка файлов без кросс-верификации
- **Верификация 2:** Кросс-верификация ссылок в новой структуре

---

## 1. Что меняется

### Переименования папок

| Было | Стало | Причина |
|------|-------|---------|
| `services/` | `service/` | Единственное число, scope = один сервис |
| `src/` | `service/` (merge) | Объединение с services/ |
| `platform/` | `system/platform/` | Группировка system scope |
| `tests/` | `system/tests/` | Группировка system scope |
| `shared/` | `system/shared/` | Группировка system scope |
| `config/` | `system/config/` | Группировка system scope |
| `git/` | `workflow/git/` | Группировка workflow |
| `issues/` | `workflow/github/issues/` | GitHub-специфика внутри github/ |
| `specs/` | `workflow/specs/` | Группировка workflow |
| `docs/` | `workflow/docs/` | Группировка workflow |
| `instructions/` | `meta/instructions/` | Группировка meta |
| `links/` | `meta/links/` | Группировка meta |
| `skills/` | `meta/skills/` | Группировка meta |

### Новые папки

| Папка | Описание |
|-------|----------|
| `service/database/` | База данных (из runtime/) |
| `service/dev/` | Локальная разработка (из src/dev/, без testing.md) |
| `service/health/` | Health checks (из runtime/) |
| `service/resilience/` | Устойчивость (из runtime/) |
| `service/frontend/` | Клиентский код (опционально) |
| `workflow/github/` | GitHub платформа (actions, templates, CODEOWNERS) |
| `meta/agents/` | Правила агентов |
| `meta/scripts/` | Правила скриптов |
| `meta/state/` | Правила состояний |
| `meta/templates/` | Правила шаблонов |

### Удаляемые папки

| Папка | Причина |
|-------|---------|
| `src/runtime/` | Разбита на `service/database/`, `service/health/`, `service/resilience/`, + realtime.md → `service/api/` |
| `src/dev/` | Разбита на `service/dev/` (local, performance) и `service/testing/` (testing) |

### Удаляемые файлы (не мигрируют)

| Файл | Причина |
|------|---------|
| `shared/scope.md` | Избыточен, правила определения scope не нужны |
| `tests/claude-testing.md` | Тестирование Claude удаляется из проекта |
| `tests/claude-functional.md` | Тестирование Claude удаляется из проекта |

### Перемещение файлов

| Файл | Было | Стало |
|------|------|-------|
| `src/api/*.md` | `src/api/` | `service/api/` |
| `src/data/*.md` | `src/data/` | `service/data/` |
| `src/runtime/database.md` | `src/runtime/` | `service/database/` |
| `src/runtime/health.md` | `src/runtime/` | `service/health/` |
| `src/runtime/resilience.md` | `src/runtime/` | `service/resilience/` |
| `src/runtime/realtime.md` | `src/runtime/` | `service/api/realtime.md` |
| `src/security/*.md` | `src/security/` | `service/security/` |
| `src/dev/testing.md` | `src/dev/` | `service/testing/testing.md` |
| `src/dev/local.md` | `src/dev/` | `service/dev/local.md` |
| `src/dev/performance.md` | `src/dev/` | `service/dev/performance.md` |
| `services/lifecycle.md` | `services/` | `service/lifecycle.md` |
| `services/structure.md` | `services/` | `service/structure.md` |
| `services/dependencies.md` | `services/` | `service/dependencies.md` |
| `git/ci.md` | `git/` | `workflow/github/actions.md` |
| `issues/*.md` | `issues/` | `workflow/github/issues/` |
| `tests/unit.md` | `tests/` | `service/testing/unit.md` |

---

## 2. План миграции

### Фаза 1: Подготовка

- [ ] Создать backup текущей структуры
- [ ] Создать новые корневые папки: `service/`, `system/`, `workflow/`, `meta/`
- [ ] Обновить CLAUDE.md с временным указанием на обе структуры

### Фаза 2: Миграция service/

- [ ] Создать `service/` с подпапками: `api/`, `data/`, `database/`, `dev/`, `health/`, `resilience/`, `security/`, `testing/`, `frontend/`
- [ ] Переместить `services/*.md` → `service/*.md` (lifecycle, structure, dependencies)
- [ ] Переместить `src/api/` → `service/api/`
- [ ] Переместить `src/runtime/realtime.md` → `service/api/realtime.md`
- [ ] Переместить `src/data/` → `service/data/`
- [ ] Переместить `src/runtime/database.md` → `service/database/`
- [ ] Переместить `src/dev/local.md` → `service/dev/local.md`
- [ ] Переместить `src/dev/performance.md` → `service/dev/performance.md`
- [ ] Переместить `src/runtime/health.md` → `service/health/`
- [ ] Переместить `src/runtime/resilience.md` → `service/resilience/`
- [ ] Переместить `src/security/` → `service/security/`
- [ ] Переместить `src/dev/testing.md` → `service/testing/`
- [ ] Создать `service/frontend/` (пустая, опционально)
- [ ] Обновить ссылки в перемещённых файлах
- [ ] Удалить старые папки `src/`, `services/`

### Фаза 3: Миграция system/

- [ ] Создать `system/` с подпапками: `platform/`, `tests/`, `shared/`, `config/`
- [ ] Переместить `platform/` → `system/platform/`
- [ ] Переместить `tests/` → `system/tests/`
- [ ] Переместить `shared/` → `system/shared/`
- [ ] Переместить `config/` → `system/config/`
- [ ] Обновить ссылки

### Фаза 4: Миграция workflow/

- [ ] Создать `workflow/` с подпапками: `git/`, `github/`, `specs/`, `docs/`
- [ ] Переместить `git/` → `workflow/git/` (без ci.md)
- [ ] Создать `workflow/github/` и `workflow/github/issues/`
- [ ] Переместить `git/ci.md` → `workflow/github/actions.md`
- [ ] Переместить `issues/` → `workflow/github/issues/`
- [ ] Переместить `specs/` → `workflow/specs/`
- [ ] Переместить `docs/` → `workflow/docs/`
- [ ] Обновить ссылки

### Фаза 5: Миграция meta/

- [ ] Создать `meta/` с подпапками: `instructions/`, `links/`, `skills/`, `agents/`, `scripts/`, `state/`, `templates/`
- [ ] Переместить `instructions/` → `meta/instructions/`
- [ ] Переместить `links/` → `meta/links/`
- [ ] Переместить `skills/` → `meta/skills/`
- [ ] Создать новые: `meta/agents/`, `meta/scripts/`, `meta/state/`, `meta/templates/`
- [ ] Обновить ссылки

### Фаза 6: Финализация

- [ ] Обновить `/.claude/instructions/README.md`
- [ ] Обновить `CLAUDE.md`
- [ ] Запустить `/links-validate` для проверки всех ссылок
- [ ] Удалить backup после проверки

---

## 3. Риски и митигация

| Риск | Митигация |
|------|-----------|
| Битые ссылки после миграции | Запустить `/links-validate` после каждой фазы |
| Скиллы ссылаются на старые пути | Обновить SKILL.md в каждом скилле |
| CLAUDE.md устареет | Обновить в последнюю очередь |

---

## 4. Чек-лист готовности

- [ ] Все файлы перемещены
- [ ] Все ссылки обновлены
- [ ] `/links-validate` проходит без ошибок
- [ ] CLAUDE.md обновлён
- [ ] README.md в instructions/ обновлён
- [ ] Скиллы работают корректно

---

## 5. Миграция templates/

Шаблоны должны отражать структуру инструкций (4 scope).

> Все пути относительно `/.claude/templates/`

### Таблица миграции templates/

| Новая папка | Старая папка | Миграция |
|-------------|--------------|:--------:|
| **service/** | | |
| `service/` | `services/` | ✅ |
| **system/** | | |
| `system/platform/` | `platform/` | ✅ |
| `system/tests/` | `tests/` | ✅ |
| **workflow/** | | |
| `workflow/docs/` | `docs/` | ✅ |
| `workflow/git/` | `git/` | ✅ |
| `workflow/specs/` | `specs/` | ✅ |
| **meta/** | | |
| `meta/instructions/` | `instructions/` | ✅ |
| `meta/skills/` | `skills/` | ✅ |

### Перемещение файлов templates/

| Файл | Было | Стало |
|------|------|-------|
| `backend-template.md` | `docs/` | `workflow/docs/` |
| `database-template.md` | `docs/` | `workflow/docs/` |
| `frontend-template.md` | `docs/` | `workflow/docs/` |
| `minimal-template.md` | `docs/` | `workflow/docs/` |
| `codeowners.md` | `git/` | `workflow/git/` |
| `commit-message.md` | `git/` | `workflow/git/` |
| `pr-template.md` | `git/` | `workflow/git/` |
| `instruction.md` | `instructions/` | `meta/instructions/` |
| `readme.md` | `instructions/` | `meta/instructions/` |
| `runbook-template.md` | `platform/` | `system/platform/` |
| `skill.md` | `skills/` | `meta/skills/` |
| `adr.md` | `specs/` | `workflow/specs/` |
| `architecture.md` | `specs/` | `workflow/specs/` |
| `discussion.md` | `specs/` | `workflow/specs/` |
| `impact.md` | `specs/` | `workflow/specs/` |
| `plan.md` | `specs/` | `workflow/specs/` |
| `smoke-test.md` | `tests/` | `system/tests/` |

### Фаза миграции templates/

- [x] Создать `templates/service/`
- [x] Создать `templates/system/` с подпапками: `platform/`, `tests/`
- [x] Создать `templates/workflow/` с подпапками: `docs/`, `git/`, `specs/`
- [x] Создать `templates/meta/` с подпапками: `instructions/`, `skills/`
- [x] Переместить `templates/services/` → `templates/service/`
- [x] Переместить `templates/platform/` → `templates/system/platform/`
- [x] Переместить `templates/tests/` → `templates/system/tests/`
- [x] Переместить `templates/docs/` → `templates/workflow/docs/`
- [x] Переместить `templates/git/` → `templates/workflow/git/`
- [x] Переместить `templates/specs/` → `templates/workflow/specs/`
- [x] Переместить `templates/instructions/` → `templates/meta/instructions/`
- [x] Переместить `templates/skills/` → `templates/meta/skills/`
- [ ] Обновить README.md в templates/
- [ ] Обновить ссылки на шаблоны в скиллах
