# Инструкция по служебным скриптам

**Связанные документы:**
- [llm_instructions.md](llm_instructions.md) — индекс инструкций
- [general_docs.md](general_docs.md) — правила документации
- [CLAUDE.md](../CLAUDE.md) — краткие инструкции для Claude

---

## Назначение

Папка `scripts/` содержит служебные скрипты для поддержания порядка в документации и коде проекта.

## Структура

```
scripts/
├── check_doc_health.py     # Комплексная проверка здоровья документации
├── check_gloss_health.py   # Проверка здоровья глоссария
├── check_doc_links.py      # [УСТАРЕЛ] Заменён на check_doc_health.py
│
├── task_new.py             # Создание задачи с автоинкрементом ID
├── task_complete.py        # Завершение задачи (перемещение + документирование)
├── task_move.py            # Перемещение задачи между current/future
│
├── discuss_new.py          # Создание дискуссии с автоинкрементом ID
├── discuss_delete.py       # Удаление дискуссии по ID
│
├── architecture_new.py     # Создание архитектуры из дискуссии
│
├── decision_new.py         # Создание ADR (Decision Record)
├── decision_delete.py      # Удаление ADR по ID
│
├── resource_new.py         # Создание ресурса (database/backend/frontend/infra)
├── resource_delete.py      # Удаление ресурса по ID
│
├── imp_plan_new.py         # Создание плана реализации
└── imp_plan_delete.py      # Удаление плана реализации
```

## Скрипты

### check_doc_health.py

**Назначение:** Комплексная проверка состояния документации проекта.

**Запуск:**
```bash
python scripts/check_doc_health.py                    # Полная проверка
python scripts/check_doc_health.py --verbose          # С подробным выводом
python scripts/check_doc_health.py --check links      # Только ссылки
python scripts/check_doc_health.py --check structure  # Только структура
python scripts/check_doc_health.py --check status     # Только статусы
python scripts/check_doc_health.py --check metadata   # Только метаданные
python scripts/check_doc_health.py --check markdown   # Только форматирование
```

**Команды Makefile:**
```bash
make docs-health              # Полная проверка документации
make docs-health-verbose      # С подробным выводом
make docs-links               # Только проверка ссылок
make docs-structure-check     # Только проверка структуры
make docs-status              # Только проверка статусов
make docs-metadata            # Только проверка метаданных
make docs-markdown            # Только проверка markdown
```

**Что проверяет:**
1. **Целостность ссылок:**
   - Ссылки на несуществующие файлы `[текст](путь/файл.md)`
   - Ссылки на несуществующие якоря `[текст](файл.md#несуществующий-раздел)`
   - Относительные ссылки в документации

2. **Структура документации:**
   - Наличие обязательных README.md в сервисах и пакетах
   - Обязательные разделы в дискуссиях (Исходный запрос, Принятое решение)
   - Обязательные разделы в архитектуре (Цель и контекст, Диаграммы, История изменений)
   - Обязательные разделы в планах реализации (Задачи, Зависимости)

3. **Статусы документов:**
   - Корректность статусов дискуссий: draft, in_progress, feedback, review, approved, final
   - Корректность статусов архитектуры: draft, in_progress, feedback, review, approved, final
   - Корректность статусов планов: draft, in_progress, review, test, approved, final
   - Корректность статусов диаграмм: in_progress, final

4. **Метаданные:**
   - Наличие даты последнего обновления в дискуссиях/архитектуре/планах
   - Наличие версии в архитектурных документах (формат: 1.0, 1.1, 2.0)

5. **Markdown форматирование:**
   - Заголовки с пробелом после # (например: `# Заголовок`)
   - Списки с пробелом после маркера (например: `- Элемент`)

**Когда запускать:**
- Перед коммитом изменений в документации
- После переименования или перемещения файлов
- При ревью pull request с изменениями документации
- Периодически (раз в неделю) для проверки актуальности

**Связанный скилл:** `/doc-health` — запускает проверку и предлагает исправления

---

### check_gloss_health.py

**Назначение:** Проверка здоровья глоссария проекта.

**Запуск:**
```bash
python scripts/check_gloss_health.py                  # Проверка глоссария
python scripts/check_gloss_health.py --verbose        # С подробным выводом
python scripts/check_gloss_health.py --warn-unused    # С предупреждениями о неиспользуемых терминах
```

**Команды Makefile:**
```bash
make gloss-health             # Проверка глоссария
make gloss-health-verbose     # С подробным выводом
make gloss-unused             # Найти неиспользуемые термины
make docs-check               # Полная проверка (документация + глоссарий)
```

**Что проверяет:**
1. **Ссылки на глоссарий:**
   - Все ли термины с иконкой 📖 существуют в `glossary.md`
   - Корректность ссылок на глоссарий `[📖 Термин](../general_docs/glossary.md#термин)`
   - Битые ссылки на якоря в глоссарии

2. **Неиспользуемые термины (с флагом --warn-unused):**
   - Термины в glossary.md, на которые нет ссылок в проекте
   - Помогает поддерживать глоссарий актуальным

3. **Структура определений терминов:**
   - Наличие обязательного поля "Определение"
   - Корректность форматирования определений

**Когда запускать:**
- После добавления новых терминов в глоссарий
- При изменении названий терминов
- Перед коммитом изменений в документации
- Периодически для проверки актуальности глоссария

**Связанные скиллы:**
- `/glossary-candidates` — анализирует документ и добавляет термины как кандидатов
- `/glossary-review` — интерактивно обрабатывает кандидатов в глоссарий
- `/glossary-link` — добавляет ссылки на глоссарий в .md файлы

---

### task_new.py

**Назначение:** Создание новой задачи с автоинкрементом ID.

**Запуск:**
```bash
python scripts/task_new.py -i                              # Интерактивный режим
python scripts/task_new.py -t "Название" -c feat -p high   # CLI режим
python scripts/task_new.py -t "Название" -c fix -f future  # В бэклог
```

**Команды Makefile:**
```bash
make task-new                   # Интерактивно
make task-new-feat TITLE="..." PRIORITY="high"
make task-new-fix TITLE="..." PRIORITY="medium"
make backlog-new                # Интерактивно в бэклог
```

**Параметры:**
- `-t, --title` — название задачи (обязательно)
- `-c, --category` — категория: `feat`, `fix`, `refactor`, `docs`, `test`, `infra`, `id`
- `-p, --priority` — приоритет: `high`, `medium`, `low` (по умолчанию: `medium`)
- `-a, --assignee` — исполнитель: `llm-main`, `amy-santiago`
- `-f, --folder` — папка: `current`, `future` (по умолчанию: `current`)
- `-i, --interactive` — интерактивный режим

**Формат ID:** `CATEGORY-NNNNN` (например: `FEAT-00001`, `FIX-00002`)

**Связанный документ:** [tasks.md](tasks.md)

---

### discuss_new.py

**Назначение:** Создание новой дискуссии с автоинкрементом ID.

**Запуск:**
```bash
python scripts/discuss_new.py "Тема дискуссии"
python scripts/discuss_new.py -t "Тема" -q "Полный запрос"
python scripts/discuss_new.py -i                           # Интерактивный режим
```

**Команды Makefile:**
```bash
make discuss-new                # Интерактивно
make discuss-new-topic TOPIC="Тема дискуссии"
make discuss-index              # Показать индекс
```

**Параметры:**
- `topic` — тема дискуссии (позиционный аргумент)
- `-t, --title` — тема дискуссии (альтернатива)
- `-d, --description` — краткое описание для индекса
- `-q, --request` — исходный запрос пользователя
- `-i, --interactive` — интерактивный режим

**Формат ID:** `NNN` (например: `001`, `002`)

**Что делает скрипт:**
1. Генерирует следующий ID из единого счётчика `general_docs/.doc_counter`
2. Создаёт файл `general_docs/01_discuss/NNN_slug.md`
3. Автоматически обновляет индекс `000_discuss.md`

**Связанный скилл:** `/discussion` — использует этот скрипт

---

### discuss_delete.py

**Назначение:** Удаление дискуссии по ID с обновлением индекса.

**Запуск:**
```bash
python scripts/discuss_delete.py 001              # С подтверждением
python scripts/discuss_delete.py 001 --force      # Без подтверждения
```

**Команды Makefile:**
```bash
make discuss-delete ID="001"   # Удалить дискуссию
```

**Параметры:**
- `discuss_id` — ID дискуссии (обязательно, например: `001`)
- `-f, --force` — удалить без подтверждения

**Что делает скрипт:**
1. Находит файл дискуссии по ID
2. Запрашивает подтверждение (если не указан `--force`)
3. Удаляет файл дискуссии
4. Обновляет индекс `000_discuss.md`:
   - Удаляет строку из таблицы
   - Уменьшает счётчик статуса
   - Обновляет секции "Быстрый поиск"

**Связанный скилл:** `/discussion` — включает команды удаления

---

### architecture_new.py

**Назначение:** Создание архитектурного документа из дискуссии.

**Запуск:**
```bash
python scripts/architecture_new.py -t "Название" -d "001"         # Из дискуссии 001
python scripts/architecture_new.py -i                              # Интерактивный режим
```

**Команды Makefile:**
```bash
make arch-new                              # Интерактивно
make arch-new-topic TITLE="..." DISCUSS="001"
make arch-index                            # Показать индекс
```

**Параметры:**
- `-t, --title` — название архитектуры (обязательно)
- `-d, --discuss` — ID связанной дискуссии
- `--domain` — область: UI/Frontend, Backend/API, Auth/Security, Database, Infrastructure, Architecture
- `-i, --interactive` — интерактивный режим

**Формат ID:** `NNN` (например: `001`, `002`)

**Что делает скрипт:**
1. Генерирует следующий ID из счётчика `general_docs/.doc_counter`
2. Создаёт файл `general_docs/02_architecture/NNN_slug.md`
3. Автоматически обновляет индекс `000_architecture.md`

**Связанный скилл:** `/architect` — использует этот скрипт

---

### decision_new.py

**Назначение:** Создание ADR (Architecture Decision Record) из архитектуры.

**Запуск:**
```bash
python scripts/decision_new.py -t "Название ADR" -a "001"         # Из архитектуры 001
python scripts/decision_new.py -i                                   # Интерактивный режим
```

**Команды Makefile:**
```bash
make decision-new                              # Интерактивно
make decision-new-topic TITLE="..." ARCH="001"
make decision-index                            # Показать индекс
```

**Параметры:**
- `-t, --title` — название ADR (обязательно)
- `-a, --architecture` — ID связанной архитектуры
- `--domain` — область: UI/Frontend, Backend/API, Auth/Security, Database, Infrastructure, Architecture
- `-i, --interactive` — интерактивный режим

**Формат ID:** `DEC-NNN` (например: `DEC-001`, `DEC-002`)

**Что делает скрипт:**
1. Генерирует следующий ID из счётчика `general_docs/.doc_counter`
2. Создаёт файл `general_docs/04_decisions/DEC-NNN_slug.md`
3. Автоматически обновляет индекс `000_decisions.md`

**Связанный скилл:** `/decision` — использует этот скрипт

---

### decision_delete.py

**Назначение:** Удаление ADR по ID с обновлением индекса.

**Запуск:**
```bash
python scripts/decision_delete.py DEC-001              # С подтверждением
python scripts/decision_delete.py DEC-001 --force      # Без подтверждения
python scripts/decision_delete.py 001                  # Можно указать только номер
```

**Команды Makefile:**
```bash
make decision-delete ID="DEC-001"   # Удалить ADR
```

**Параметры:**
- `decision_id` — ID решения (обязательно, например: `DEC-001` или `001`)
- `-f, --force` — удалить без подтверждения

**Что делает скрипт:**
1. Находит файл ADR по ID
2. Запрашивает подтверждение (если не указан `--force`)
3. Удаляет файл ADR
4. Обновляет индекс `000_decisions.md`

**Связанный скилл:** `/decision` — включает команды удаления

---

### resource_new.py

**Назначение:** Создание ресурса (database, backend, frontend, infra) из ADR.

**Запуск:**
```bash
python scripts/resource_new.py -n "Название" -t backend -a "DEC-001"
python scripts/resource_new.py -i                                    # Интерактивный режим
```

**Команды Makefile:**
```bash
make resource-new                                        # Интерактивно
make resource-new-backend NAME="..." ADR="DEC-001"
make resource-new-frontend NAME="..." ADR="DEC-001"
make resource-new-database NAME="..." ADR="DEC-001"
make resource-new-infra NAME="..." ADR="DEC-001"
make resource-index                                      # Показать индекс
```

**Параметры:**
- `-n, --name` — название ресурса (обязательно)
- `-t, --type` — тип: `database`, `backend`, `frontend`, `infra` (обязательно)
- `-a, --adr` — ID связанного ADR (например: `DEC-001`)
- `-i, --interactive` — интерактивный режим

**Формат ID:** `NNN` (например: `001`, `002`)

**Что делает скрипт:**
1. Генерирует следующий ID из счётчика (отдельный для каждого типа)
2. Создаёт файл в `general_docs/05_resources/{type}/NNN_slug.md`
3. Автоматически обновляет индекс `000_SUMMARY.md` в подпапке типа

**Связанный скилл:** `/resource` — использует этот скрипт

---

### resource_delete.py

**Назначение:** Удаление ресурса по ID и типу.

**Запуск:**
```bash
python scripts/resource_delete.py 001 -t backend              # С подтверждением
python scripts/resource_delete.py 001 -t frontend --force     # Без подтверждения
```

**Команды Makefile:**
```bash
make resource-delete ID="001" TYPE="backend"   # Удалить ресурс
```

**Параметры:**
- `resource_id` — ID ресурса (обязательно, например: `001`)
- `-t, --type` — тип: `database`, `backend`, `frontend`, `infra` (обязательно)
- `-f, --force` — удалить без подтверждения

**Что делает скрипт:**
1. Находит файл ресурса по ID и типу
2. Запрашивает подтверждение (если не указан `--force`)
3. Удаляет файл ресурса
4. Обновляет индекс `000_SUMMARY.md` в подпапке

**Связанный скилл:** `/resource` — включает команды удаления

---

### imp_plan_new.py

**Назначение:** Создание плана реализации из ADR.

**Запуск:**
```bash
python scripts/imp_plan_new.py -t "Название плана" -a "DEC-001"
python scripts/imp_plan_new.py -i                                  # Интерактивный режим
```

**Команды Makefile:**
```bash
make imp-plan-new                                        # Интерактивно
make imp-plan-new-topic TITLE="..." ADR="DEC-001"
make imp-plan-index                                      # Показать индекс
```

**Параметры:**
- `-t, --title` — название плана (обязательно)
- `-a, --adr` — ID связанного ADR (например: `DEC-001`)
- `--domain` — область: UI/Frontend, Backend/API, Auth/Security, Database, Infrastructure, Architecture
- `-i, --interactive` — интерактивный режим

**Формат ID:** `NNN` (например: `001`, `002`)

**Что делает скрипт:**
1. Генерирует следующий ID из счётчика `general_docs/.doc_counter`
2. Создаёт файл `general_docs/06_imp_plans/NNN_plan_slug.md`
3. Автоматически обновляет индекс `000_imp_plans.md`

**Связанный скилл:** `/imp-plan` — использует этот скрипт

---

### imp_plan_delete.py

**Назначение:** Удаление плана реализации по ID.

**Запуск:**
```bash
python scripts/imp_plan_delete.py 001              # С подтверждением
python scripts/imp_plan_delete.py 001 --force      # Без подтверждения
```

**Команды Makefile:**
```bash
make imp-plan-delete ID="001"   # Удалить план
```

**Параметры:**
- `plan_id` — ID плана (обязательно, например: `001`)
- `-f, --force` — удалить без подтверждения

**Что делает скрипт:**
1. Находит файл плана по ID
2. Запрашивает подтверждение (если не указан `--force`)
3. Удаляет файл плана
4. Обновляет индекс `000_imp_plans.md`

**Связанный скилл:** `/imp-plan` — включает команды удаления

---

### check_doc_links.py

**Статус:** УСТАРЕЛ. Заменён на `check_doc_health.py`.

**Миграция:**
```bash
# Старая команда:
python scripts/check_doc_links.py

# Новая команда (эквивалент):
python scripts/check_doc_health.py --check links
# или
make docs-links
```

## Добавление новых скриптов

При создании нового скрипта:
1. Разместить в папке `scripts/`
2. Добавить описание в этот файл
3. Добавить docstring с описанием в начало скрипта
4. Указать зависимости (если есть)
