# Скилл /sync — оценка и план

Скилл для синхронизации локальной main после merge.

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)
- [Решения](#решения)
- [Открытые вопросы](#открытые-вопросы)

---

## Контекст

**Задача:** G7 из standard-process.md — нет `/sync` скилла
**Почему создан:** Определить нужен ли скилл или достаточно двух команд git
**Связанные файлы:**
- `/.github/.instructions/sync/standard-sync.md` — стандарт синхронизации
- `specs/.instructions/standard-process.md` — §5 Фаза 4, шаг 4.5

## Содержание

### Что уже покрыто

- `standard-sync.md` — полный стандарт
- Две команды: `git checkout main && git pull origin main`

### Что мог бы добавить скилл

| Функция | Сейчас | С `/sync` |
|---------|--------|----------|
| Sync команды | 2 команды вручную | Один вызов |
| Проверка stash | Ручная | Автоматический stash/unstash |
| Удаление merged ветки | Ручное | Автоматическое `git branch -d` |
| Обновление analysis chain | Ручное | Предложить `/analysis-status` если chain в RUNNING |

### Артефакты

| # | Артефакт | Путь | Статус |
|---|---------|------|--------|
| 1 | **Инструкция** (SSOT) | `/.github/.instructions/sync/create-sync.md` | **Нужно создать** |
| 2 | **Скилл** (обёртка) | `/.claude/skills/sync/SKILL.md` | **Нужно создать** |

### Формат вызова

```
/sync [--delete-branch]
```

### Порядок создания

1. `/instruction-create create-sync --path .github/.instructions/sync/`
2. `/skill-create sync`

## Решения

- Приоритет низкий — две команды git
- Ценность в автоматическом cleanup (ветка, stash)

## Открытые вопросы

- Объединить с `/merge` в один скилл?
- Нужно ли автоматически удалять merged ветку?

---

## Что уже описано в проекте

### standard-sync.md (полный стандарт синхронизации)

Полноценный документ в `/.github/.instructions/sync/standard-sync.md`, покрывающий:

1. **Обязательные триггеры синхронизации** (4 штуки):
   - Перед созданием ветки (main должна быть актуальной)
   - После merge PR в main (локальная main устарела)
   - При разработке > 2 дней (feature-ветку с main, rebase)
   - Перед финальным push / созданием PR (feature-ветку с main, проверка `git log HEAD..origin/main --oneline`)

2. **Процесс синхронизации main** — предусловия (`git status --porcelain`), проверка актуальности (`git fetch origin` + сравнение SHA `git rev-parse main` vs `git rev-parse origin/main`), сами команды (`git checkout main && git pull origin main`), таблица ошибок.

3. **Процесс синхронизации feature-ветки** — rebase (не merge): `git checkout main && git pull origin main && git checkout {branch} && git rebase main && git push --force-with-lease`. Объяснено почему rebase, а не merge (чистая линейная история, нет merge-коммитов, упрощает Squash Merge).

4. **Разрешение конфликтов** — конфликты только при rebase feature-ветки. Правила: приоритет main для конфигураций; если > 3 файлов или > 50 строк — `git rebase --abort` и сообщить пользователю.

5. **Запреты** — не `git pull` в feature-ветке для main, не `--force` в shared-ветках, force push только до создания PR, использовать `--force-with-lease`.

### standard-branching.md (жизненный цикл ветки)

В `/.github/.instructions/branches/standard-branching.md` section 3 описан lifecycle ветки:

- **Создание**: только от актуального main (обязательна синхронизация перед созданием).
- **Завершение** (после merge PR): ветка ДОЛЖНА быть удалена. Два способа:
  - Автоматически: Settings -> General -> "Automatically delete head branches" (рекомендуется).
  - Вручную: `git branch -d {branch-name} && git fetch --prune`.
- **Stash при переключении**: `git stash save "WIP: описание"` -> переключение -> `git stash pop`.

### standard-review.md section "После merge"

В `/.github/.instructions/review/standard-review.md` section 3 описано:

- **Автоматически на GitHub**: remote feature-ветка удаляется, Issues закрываются (через `Closes #N`), PR -> "Merged".
- **Локальная очистка**: ссылка на standard-branching.md section 3.
- **Синхронизация main**: ссылка на standard-sync.md.
- **CLI**: `gh pr merge 123 --squash --delete-branch` (удаляет remote-ветку при merge).

### standard-process.md (оркестратор, шаг 4.5)

В `specs/.instructions/standard-process.md` Фаза 4, шаг 4.5 "Sync main":
- Скилл: прочерк (нет скилла).
- SSOT: standard-sync.md.
- Quick Reference: `git checkout main && git pull`.
- G7 в таблице пробелов: приоритет "Низкий", описание "Две команды git".

### standard-github-workflow.md (Стадия 9)

Стадия 9 в `/.github/.instructions/standard-github-workflow.md` section 11:
- "Синхронизация локальной main с remote после merge."
- Выход: "Main синхронизирован -> готовность к релизу или новому циклу разработки."

### standard-development.md (SSOT-зависимость)

В `/.github/.instructions/development/standard-development.md` зависимость:
- `standard-sync.md` — синхронизация main при длительной разработке (> 2 дней).

### Драфт /merge (G6, пересечение)

В `.claude/drafts/2026-02-24-merge-skill.md` открытый вопрос: "Объединить с `/sync` в один скилл `/merge-and-sync`?" Драфт merge описывает post-merge sync как потенциальную добавленную ценность скилла. Оба драфта (G6 и G7) имеют зеркальные открытые вопросы об объединении.

### Скриптовая поддержка

- `sync-standard-version.py` (`.instructions/.scripts/`) — не связан с git sync, обновляет standard-version в файлах.
- `sync-labels.py` (`.github/.instructions/.scripts/`) — синхронизация GitHub labels, не связан.
- `sync-readme.py` (`.structure/.instructions/.scripts/`) — синхронизация README, не связан.
- `chain_status.py` (`specs/.instructions/.scripts/`) — управление статусами analysis chain. Связан: после sync main нужно обновить цепочку (RUNNING -> REVIEW) если все TASK-N выполнены.

### Что НЕ описано в проекте (пробелы)

- Нет инструкции `create-sync.md` (workflow создания sync).
- Нет скилла `/sync`.
- Нет скрипта автоматического cleanup локальных merged-веток.
- Нет скрипта обнаружения stale-веток (веток, у которых remote уже удалён).
- Нет post-merge hook (автоматический запуск sync после `gh pr merge`).
- Нет проверки "а нужно ли перейти к `/analysis-status`" после sync.

---

## Best practices

### 1. Branch cleanup automation

**`git fetch --prune`** — удаляет из локального кеша ссылки на remote-ветки, которых больше нет на origin. Проект уже упоминает это в standard-branching.md. Best practice: выполнять `git fetch --prune` каждый раз при sync main, а не отдельно.

**`git branch --merged main | grep -v main | xargs git branch -d`** — массовое удаление всех локальных веток, которые уже смержены в main. Полезно для cleanup после нескольких циклов разработки. Скилл `/sync` мог бы предлагать это при обнаружении > 0 merged-веток.

**GitHub "Automatically delete head branches"** — уже рекомендован в standard-branching.md. Удаляет remote-ветку автоматически после merge PR. Но локальная ветка остаётся — именно здесь `/sync` добавляет ценность.

### 2. Stale branch detection

**Stale branch** — ветка, remote-аналог которой удалён (после merge) или которая не обновлялась > N дней.

**Обнаружение orphaned (remote удалён):**
```bash
git fetch --prune
git branch -vv | grep ': gone]'
```
Показывает локальные ветки, чьи remote-tracking ветки больше не существуют. `/sync` мог бы автоматически предлагать удаление таких веток.

**Обнаружение inactive (давно без коммитов):**
```bash
git for-each-ref --sort=-committerdate --format='%(refname:short) %(committerdate:relative)' refs/heads/
```
Показывает ветки отсортированные по дате последнего коммита. Полезно для аудита.

**GitHub Actions stale branches:** GitHub имеет встроенный UI для просмотра stale-веток (Settings -> Branches). Также существуют Actions (например, `actions/stale`) для автоматической маркировки и удаления stale Issues/PRs, но не веток напрямую.

### 3. Safe sync strategies

**Pre-sync safety check:** Всегда проверять `git status --porcelain` перед sync. Если есть незакоммиченные изменения — auto-stash или ошибка. В проекте уже описано, но не автоматизировано.

**`git pull --ff-only`** — альтернатива `git pull` для main. Гарантирует, что pull выполнится только как fast-forward (без создания merge-коммита). Если fast-forward невозможен (локальные коммиты в main) — ошибка вместо молчаливого merge. Более безопасно, чем обычный `git pull`. Проект утверждает, что прямые коммиты в main запрещены, поэтому `--ff-only` всегда должен проходить. Если не проходит — явный сигнал нарушения workflow.

**`git config pull.ff only`** — глобальная настройка, чтобы `git pull` на main всегда был fast-forward only. Можно рекомендовать в initialization.md.

### 4. Post-merge hooks

**Git hook `post-merge`** (`.git/hooks/post-merge`) — выполняется автоматически после `git pull` (который внутри делает merge). Можно использовать для:
- Автоматического запуска `git fetch --prune`
- Уведомления об orphaned локальных ветках
- Обновления зависимостей (`make setup` если изменился lock-файл)

**Ограничение:** post-merge hook не вызывается после `gh pr merge` (это server-side операция). Он вызывается после локального `git pull`. Значит подходит для автоматизации именно sync-шага.

**Пример post-merge hook:**
```bash
#!/bin/bash
# Prune remote tracking branches
git fetch --prune
# Show orphaned local branches
orphaned=$(git branch -vv | grep ': gone]' | awk '{print $1}')
if [ -n "$orphaned" ]; then
  echo "Orphaned local branches (remote deleted):"
  echo "$orphaned"
  echo "Run 'git branch -d <branch>' to clean up"
fi
```

### 5. Monorepo vs polyrepo sync

Проект — monorepo (один репозиторий, микросервисная архитектура в `/src/{service}/`). Для monorepo:
- Sync main затрагивает все сервисы сразу — один `git pull` обновляет всё.
- Rebase feature-ветки может дать конфликты в файлах, не связанных с текущей задачей (другой сервис). Standard-sync.md уже покрывает это через правила конфликтов (> 3 файлов -> abort).
- Нет необходимости в selective sync или sparse checkout — проект относительно компактный (шаблон).

Для polyrepo (если проект масштабируется):
- Каждый сервис — отдельный репозиторий, sync каждого отдельно.
- Cross-repo зависимости через версионированные пакеты.
- Скилл `/sync` стал бы значительно полезнее: оркестрация sync нескольких репозиториев.

### 6. Sync + analysis chain transition

Ключевая неавтоматизированная связка: после sync main (шаг 4.5) следует Фаза 5 (5.1 RUNNING -> REVIEW). Скилл `/sync` мог бы:
1. Выполнить sync main.
2. Проверить, есть ли analysis chain в статусе RUNNING.
3. Если да — спросить пользователя: "Все TASK-N завершены? Перейти к `/analysis-status` для RUNNING -> REVIEW?"
4. Это создаёт мост между Фазой 4 и Фазой 5.

### 7. Идемпотентность sync

Best practice: `/sync` должен быть безопасен при повторном вызове. Если main уже актуален (SHA совпадают) — нет действий. Если ветка уже удалена — нет ошибки. Standard-sync.md уже описывает проверку актуальности через `git rev-parse`, но это не автоматизировано в скрипте.

### 8. Объединение /merge + /sync

Аргументы "за" объединение в `/merge-and-sync`:
- Шаги 4.4 (Merge) и 4.5 (Sync) всегда идут последовательно.
- Один вызов вместо двух.
- Post-merge cleanup (ветка) логически связан с sync.

Аргументы "против":
- Sync нужен не только после merge (триггеры: перед созданием ветки, начало рабочего дня).
- Принцип single responsibility — merge это GitHub-операция, sync это git-операция.
- Проект уже имеет отдельные стандарты (standard-review.md для merge, standard-sync.md для sync).

**Рекомендация:** Два отдельных скилла, но `/merge` автоматически вызывает `/sync` в конце (post-merge step). `/sync` остаётся самостоятельным для остальных триггеров.
