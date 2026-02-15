# Проблема: README specs-папок не имеют процесса создания

## Оглавление

- [Контекст](#контекст)
- [Содержание](#содержание)

---

## Контекст

**Задача:** Закрыть пробел — README файлы specs-папок (`specs/discussion/README.md`, `specs/impact/README.md` и т.д.) имеют специфичный табличный формат, но ни один воркфлоу не отвечает за его создание.

**Почему:** При тестировании impact-инструкций обнаружено, что README Impact имел неправильный формат таблицы. Формат описан в стандарте, но нигде не применяется автоматически.

**Связанные файлы:**
- [standard-readme.md](/.structure/.instructions/standard-readme.md) — стандарт generic README
- [create-structure.md](/.structure/.instructions/create-structure.md) — воркфлоу создания папок
- [standard-specs.md](/specs/.instructions/standard-specs.md) § 9 — общий формат README-таблиц
- [standard-discussion.md](/specs/.instructions/discussion/standard-discussion.md) § 2 — формат Discussion README
- [standard-impact.md](/specs/.instructions/impact/standard-impact.md) § 2 — формат Impact README

---

## Содержание

### Суть проблемы

Каждый тип SDD-объекта определяет **свой формат README-таблицы** в стандарте (§ 2):

| Объект | Формат таблицы | Где описан |
|--------|---------------|------------|
| Discussion | `ID \| Документ \| Статус \| Impact \| Milestone \| Описание` | standard-discussion.md § 2 |
| Impact | `ID \| Документ \| Статус \| Parent Discussion \| Design \| Milestone \| Описание` | standard-impact.md § 2 |
| Design | *(будет определён)* | standard-design.md § 2 |
| ADR | *(будет определён)* | standard-adr.md § 2 |
| Plan Tests | *(будет определён)* | standard-plan-test.md § 2 |
| Plan Dev | *(будет определён)* | standard-plan-dev.md § 2 |

Но **ни один процесс не создаёт README с этим форматом:**

1. `/structure-create specs/discussion` → создаёт generic README из `standard-readme.md` (frontmatter + заголовок + дерево). **Не знает** про таблицу `ID | Документ | Статус | Impact | ...`.

2. `create-discussion.md` шаг 7 → "Добавить запись в README". Предполагает, что README **уже содержит** нужную таблицу. Не описывает что делать, если таблицы нет.

3. `standard-specs.md` § 9 → описывает общий формат (`# | Документ | Статус | Описание`) и говорит "стандарты объектов определяют конкретные колонки". Но не указывает **когда** и **кем** эти колонки создаются.

### Последствия

- При первом создании Discussion/Impact LLM получает README без таблицы или с таблицей неправильного формата.
- LLM должен "догадаться" какой формат нужен, прочитав стандарт. Это работает, но ненадёжно — в итерации 1 тестирования Impact README имел неправильный формат.
- Нет единого места, которое говорит: "при создании `specs/discussion/` — README должен содержать вот эту таблицу".

### Варианты решения

**Вариант A: Расширить `/structure-create`**
- `create-structure.md` получает маппинг: если путь = `specs/discussion/` → использовать шаблон README из `standard-discussion.md` § 2.
- Плюсы: одна точка входа.
- Минусы: `create-structure.md` начинает знать про specs-специфику.

**Вариант B: Шаг в create-воркфлоу каждого объекта**
- `create-discussion.md`, `create-impact.md` и т.д. получают шаг: "Если README не содержит нужной таблицы — создать таблицу по формату из стандарта § 2".
- Плюсы: каждый воркфлоу самодостаточен.
- Минусы: дублирование логики в 6 create-воркфлоу.

**Вариант C: Скрипт инициализации specs-папки**
- Отдельный скрипт `init-specs-folder.py` (или расширение `create-*-file.py`), который при создании первого объекта проверяет и инициализирует README.
- Плюсы: автоматизация.
- Минусы: ещё один скрипт.

**Вариант D: Шаблоны README в стандартах**
- Каждый `standard-*.md` содержит полный шаблон README (уже частично так — § 2 содержит формат таблицы). Скрипты `create-*-file.py` при создании первого файла проверяют README и дополняют таблицу если нужно.
- Плюсы: SSOT в стандарте + автоматизация в скрипте.
- Минусы: усложнение скриптов.
