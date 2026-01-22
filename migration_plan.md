# План миграции инструкций

План перехода от текущей структуры `/.claude/instructions/` к новой.

**Связанные документы:**
- [new_structure_of_project.md](./new_structure_of_project.md) — целевая структура

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
| `service/health/` | Health checks (из runtime/) |
| `service/resilience/` | Устойчивость (из runtime/) |
| `service/frontend/` | Клиентский код (опционально) |
| `workflow/github/` | GitHub платформа (actions, templates, CODEOWNERS) |
| `meta/agents/` | Правила агентов |
| `meta/scripts/` | Правила скриптов |
| `meta/state/` | Правила состояний |

### Удаляемые папки

| Папка | Причина |
|-------|---------|
| `src/runtime/` | Разбита на `service/database/`, `service/health/`, `service/resilience/` |

### Перемещение файлов

| Файл | Было | Стало |
|------|------|-------|
| `src/api/*.md` | `src/api/` | `service/api/` |
| `src/data/*.md` | `src/data/` | `service/data/` |
| `src/runtime/database.md` | `src/runtime/` | `service/database/` |
| `src/runtime/health.md` | `src/runtime/` | `service/health/` |
| `src/runtime/resilience.md` | `src/runtime/` | `service/resilience/` |
| `src/security/*.md` | `src/security/` | `service/security/` |
| `src/dev/testing.md` | `src/dev/` | `service/testing/` |
| `services/lifecycle.md` | `services/` | `service/lifecycle.md` |
| `services/structure.md` | `services/` | `service/structure.md` |
| `services/dependencies.md` | `services/` | `service/dependencies.md` |
| `git/ci.md` | `git/` | `workflow/github/actions.md` |
| `issues/*.md` | `issues/` | `workflow/github/issues/` |

---

## 2. План миграции

### Фаза 1: Подготовка

- [ ] Создать backup текущей структуры
- [ ] Создать новые корневые папки: `service/`, `system/`, `workflow/`, `meta/`
- [ ] Обновить CLAUDE.md с временным указанием на обе структуры

### Фаза 2: Миграция service/

- [ ] Создать `service/` с подпапками: `api/`, `data/`, `runtime/`, `security/`, `testing/`
- [ ] Переместить файлы из `src/` в `service/`
- [ ] Переместить файлы из `services/` в `service/`
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

- [ ] Создать `meta/` с подпапками: `instructions/`, `links/`, `skills/`, `agents/`, `scripts/`, `state/`
- [ ] Переместить `instructions/` → `meta/instructions/`
- [ ] Переместить `links/` → `meta/links/`
- [ ] Переместить `skills/` → `meta/skills/`
- [ ] Создать новые: `meta/agents/`, `meta/scripts/`, `meta/state/`
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
