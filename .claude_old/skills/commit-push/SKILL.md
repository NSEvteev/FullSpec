---
name: commit-push
description: Коммит и пуш изменений в GitHub с правильным форматированием сообщений
allowed-tools: Bash, Read
---

# Коммит и пуш

Команда для сохранения изменений и отправки в GitHub.

## Формат сообщения коммита

**Везде используются причастия (страдательный залог):**

### Заголовок (первая строка)

- ✅ "Добавлен скилл commit-push"
- ✅ "Обновлена структура документации"
- ✅ "Исправлены ошибки в конфигурации"
- ❌ "Добавили скилл" (неправильно)
- ❌ "Добавить скилл" (неправильно)

### Описание изменений (тело коммита)

- ✅ "- Добавлен скилл для генерации структуры"
- ✅ "- Обновлена таблица скиллов"
- ✅ "- Исправлена опечатка в документации"
- ❌ "- Добавить скилл" (неправильно)
- ❌ "- Добавили скилл" (неправильно)

### Примеры полных сообщений

```
Добавлена система документации

- Добавлена структура папок general_docs/
- Создан глоссарий терминов
- Обновлён README.md

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

```
Исправлены ошибки в конфигурации

- Исправлен путь к шаблонам
- Удалены дублирующиеся записи
- Обновлена документация

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Инструкции

### Шаг 1: Проверить статус

```bash
git status
git diff
git log --oneline -3
```

### Шаг 2: Добавить файлы

Добавить все изменённые файлы, кроме:
- `.claude/settings.local.json` — локальные настройки
- Файлы с секретами (.env, credentials)

```bash
git add [файлы]
```

### Шаг 3: Создать коммит

Использовать HEREDOC для сообщения:

```bash
git commit -m "$(cat <<'EOF'
[Заголовок — причастие]

- [Изменение 1 — причастие]
- [Изменение 2 — причастие]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Шаг 4: Отправить в GitHub

```bash
git push
```

### Шаг 5: Подтвердить результат

```bash
git status
```

Вывести хэш и заголовок коммита.

## Таблица причастий

| Действие | Муж. род | Жен. род | Мн. число |
|----------|----------|----------|-----------|
| add | Добавлен | Добавлена | Добавлены |
| update | Обновлён | Обновлена | Обновлены |
| fix | Исправлен | Исправлена | Исправлены |
| remove | Удалён | Удалена | Удалены |
| create | Создан | Создана | Созданы |
| refactor | Переработан | Переработана | Переработаны |
| improve | Улучшен | Улучшена | Улучшены |
| move | Перемещён | Перемещена | Перемещены |
| rename | Переименован | Переименована | Переименованы |

### Согласование с существительным

- **скилл** (м.р.) → Добавлен скилл, Обновлён скилл
- **команда** (ж.р.) → Добавлена команда, Обновлена команда
- **документация** (ж.р.) → Обновлена документация
- **файл** (м.р.) → Добавлен файл, Удалён файл
- **структура** (ж.р.) → Обновлена структура
- **ошибки** (мн.ч.) → Исправлены ошибки

## Примеры использования

### Пример 1: Коммит изменений в документации

**Сценарий:** Обновлены файлы документации скиллов (добавлены примеры использования в 7 SKILL.md файлов). Нужно закоммитить все изменения с правильным форматированием.

**Команда:**
```bash
/commit-push
```

**Ожидаемый результат:**
- Проверка статуса git
- Добавление изменённых файлов
- Коммит с причастиями в сообщении
- Пуш в GitHub
- Подтверждение успешной операции

**Вывод (пример):**
```bash
# Проверка статуса
$ git status
Changes not staged for commit:
  modified:   .claude/skills/doc-health/SKILL.md
  modified:   .claude/skills/glossary-link/SKILL.md
  modified:   .claude/skills/doc-claude/SKILL.md
  modified:   .claude/skills/glossary-candidates/SKILL.md
  modified:   .claude/skills/glossary-review/SKILL.md
  modified:   .claude/skills/doc-project-structure/SKILL.md
  modified:   .claude/skills/commit-push/SKILL.md

# Добавление файлов
$ git add .claude/skills/*/SKILL.md

# Коммит
$ git commit -m "$(cat <<'EOF'
Добавлены примеры использования в документацию скиллов

- Добавлены примеры для doc-health (3 сценария)
- Добавлены примеры для glossary-link (3 сценария)
- Обновлены примеры для doc-claude (3 улучшенных сценария)
- Добавлены примеры для glossary-candidates (3 сценария)
- Добавлены примеры для glossary-review (3 сценария)
- Добавлены примеры для doc-project-structure (3 сценария)
- Добавлены примеры для commit-push (3 сценария)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# Пуш
$ git push

✓ Коммит создан: a1b2c3d
✓ Изменения отправлены в GitHub
```

### Пример 2: Коммит с множественными файлами (код + документация)

**Сценарий:** Добавлен новый скрипт `scripts/check_dependency_chain.py` для проверки цепочки зависимостей и обновлена документация скилла doc-health. Нужно закоммитить изменения в обоих файлах.

**Команда:**
```bash
/commit-push
```

**Ожидаемый результат:**
- Добавление и скрипта, и документации
- Логическая группировка изменений в сообщении коммита
- Использование причастий для всех изменений

**Вывод (пример):**
```bash
# Проверка статуса
$ git status
Changes not staged for commit:
  modified:   scripts/check_doc_health.py
  new file:   scripts/check_dependency_chain.py
  modified:   .claude/skills/doc-health/SKILL.md

# Добавление файлов
$ git add scripts/check_doc_health.py scripts/check_dependency_chain.py .claude/skills/doc-health/SKILL.md

# Коммит
$ git commit -m "$(cat <<'EOF'
Добавлена проверка цепочки зависимостей в документации

- Добавлен скрипт check_dependency_chain.py
- Добавлена функция check_dependency_chain() в check_doc_health.py
- Обновлена документация скилла doc-health с новой проверкой
- Добавлены примеры использования для проверки цепочки

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# Пуш
$ git push

✓ Коммит создан: d4e5f6g
✓ Изменения отправлены в GitHub
```

### Пример 3: Исправление ошибок

**Сценарий:** Обнаружены опечатки в файлах CLAUDE.md и README.md. Нужно быстро исправить и закоммитить.

**Команда:**
```bash
/commit-push
```

**Ожидаемый результат:**
- Простое сообщение коммита (только исправление ошибок)
- Правильное согласование причастий

**Вывод (пример):**
```bash
# Проверка статуса
$ git status
Changes not staged for commit:
  modified:   CLAUDE.md
  modified:   README.md

# Добавление файлов
$ git add CLAUDE.md README.md

# Коммит
$ git commit -m "$(cat <<'EOF'
Исправлены опечатки в документации

- Исправлена опечатка в разделе "Быстрый старт LLM" (CLAUDE.md)
- Исправлено описание команды make docs-health (README.md)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# Пуш
$ git push

✓ Коммит создан: h7i8j9k
✓ Изменения отправлены в GitHub
```

### Пример 4: Откат коммита (дополнительный сценарий)

**Сценарий:** Случайно закоммитили файл `.claude/settings.local.json` с локальными настройками. Нужно откатить коммит.

**Команда:**
```bash
# Откат последнего коммита (сохраняя изменения)
git reset --soft HEAD~1

# Или полный откат (удаляя изменения)
git reset --hard HEAD~1
```

**Вывод (пример):**
```bash
$ git reset --soft HEAD~1
$ git status
Changes to be committed:
  modified:   .claude/skills/doc-health/SKILL.md
  modified:   .claude/settings.local.json  # Нужно убрать

$ git reset HEAD .claude/settings.local.json
$ git status
Changes to be committed:
  modified:   .claude/skills/doc-health/SKILL.md

Untracked files:
  .claude/settings.local.json

# Добавить .claude/settings.local.json в .gitignore
$ echo ".claude/settings.local.json" >> .gitignore
$ git add .gitignore

✓ Локальные настройки исключены из коммита
✓ Файл добавлен в .gitignore
```
