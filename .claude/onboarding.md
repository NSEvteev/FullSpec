# Onboarding

Руководство для новых участников проекта.

## 1. Философия проекта

### SSOT вместо дублирования
Каждый тип артефакта имеет один стандарт. Не копируй правила — ссылайся на стандарт.

### Скиллы вместо команд
Не используй `mkdir`, `rm -rf`, Write/Edit напрямую для структурных изменений. Используй скиллы: `/structure-create`, `/instruction-create`, `/skill-create`.

### Миграция вместо ручного обновления
При изменении стандарта не правь документы вручную. Используй `/migration-create` — это гарантирует обновление всех зависимых файлов.

### Версионирование как контроль качества
Каждый документ имеет `standard-version`. Расхождение версий = сигнал о необходимости миграции.

## 2. Первые шаги

0. Выполни `make setup` (или `/init-project` для полной настройки) — [initialization.md](/.structure/initialization.md)
1. Прочитай [/CLAUDE.md](/CLAUDE.md) — точка входа
2. Прочитай [quick-start.md](/.structure/quick-start.md) — минимальный контекст (SSOT, артефакты, скиллы, процесс)
3. Посмотри [/.structure/README.md](/.structure/README.md) — структура проекта
4. **Изменение поведения → `/chain`**, баги → `/hotfix`** — оркестратор создаёт TaskList. [SSOT: create-chain.md](/specs/.instructions/create-chain.md)

## 3. Типичные задачи

| Задача | Скилл | SSOT |
|--------|-------|------|
| Создать инструкцию | `/instruction-create` | `/.instructions/standard-instruction.md` |
| Создать скилл | `/skill-create` | `/.claude/.instructions/skills/standard-skill.md` |
| Создать rule | `/rule-create` | `/.claude/.instructions/rules/standard-rule.md` |
| Создать папку | `/structure-create` | `/.structure/.instructions/standard-readme.md` |
| Изменить стандарт | `/migration-create` | `/.instructions/migration/create-migration.md` |
| Проверить черновик | `/draft-validate` | `/.claude/.instructions/drafts/standard-draft.md` |

## 4. Чего НЕ делать

| Действие | Почему нельзя | Что делать вместо |
|----------|---------------|-------------------|
| `mkdir` для новой папки | Не создаст README, не обновит structure.json | `/structure-create` |
| `rm -rf` для удаления папки | Не обновит зависимости | `/structure-modify --delete` |
| Edit/Write для README | Может нарушить структуру | `/structure-modify` |
| Edit стандарта напрямую | Не обновит зависимые документы | `/migration-create` |
| Игнорировать `**SSOT:**` | Будешь работать по устаревшим правилам | Всегда читать SSOT |

## 5. Куда обращаться

| Вопрос | Где искать |
|--------|------------|
| Структура проекта | [/.structure/README.md](/.structure/README.md) |
| Список скиллов | [/.claude/skills/README.md](/.claude/skills/README.md) |
| Активные rules | [/.claude/rules/](/.claude/rules/) |
| Агенты | [/.claude/agents/README.md](/.claude/agents/README.md) |
| История изменений | [/.claude/CHANGELOG.md](/.claude/CHANGELOG.md) |
| Глоссарий | [/specs/glossary.md](/specs/glossary.md) |

## Связанные документы

- [Quick Start](/.structure/quick-start.md) — SSOT, артефакты, скиллы, процесс
