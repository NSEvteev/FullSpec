---
description: Воркфлоу создания документа импакт-анализа SDD — Quick Scan, Clarify, генерация, валидация, перевод DRAFT → WAITING.
standard: .instructions/standard-instruction.md
standard-version: v1.3
index: specs/.instructions/impact/README.md
---

# Воркфлоу создания импакт-анализа

Рабочая версия стандарта: 1.0

Пошаговый процесс создания нового документа импакт-анализа (`specs/impact/impact-*.md`).

**Полезные ссылки:**
- [Стандарт импакт-анализа](./standard-impact.md)
- [Стандарт SDD](../standard-specs.md) — статусы, Clarify, маркеры, общий паттерн объекта
- [Инструкции impact/](./README.md)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | [standard-impact.md](./standard-impact.md) |
| Валидация | [validation-impact.md](./validation-impact.md) |
| Создание | Этот документ |
| Модификация | [modify-impact.md](./modify-impact.md) |

## Оглавление

- [Принципы](#принципы)
- [Шаги](#шаги)
  - [Шаг 1: Проверить parent Discussion](#шаг-1-проверить-parent-discussion)
  - [Шаг 2: Quick Scan архитектуры](#шаг-2-quick-scan-архитектуры)
  - [Шаг 3–4: Определить номер и создать файл из шаблона](#шаг-34-определить-номер-и-создать-файл-из-шаблона)
  - [Шаг 5: Заполнить frontmatter](#шаг-5-заполнить-frontmatter)
  - [Шаг 6: Clarify](#шаг-6-clarify)
  - [Шаг 7: Заполнить разделы](#шаг-7-заполнить-разделы)
  - [Шаг 8: Регистрация в README](#шаг-8-регистрация-в-readme)
  - [Шаг 8.5: Обновить parent Discussion](#шаг-85-обновить-parent-discussion)
  - [Шаг 9: Валидация](#шаг-9-валидация)
  - [Шаг 10: Ревью пользователем](#шаг-10-ревью-пользователем)
  - [Шаг 11: Отчёт о выполнении](#шаг-11-отчёт-о-выполнении)
- [Чек-лист](#чек-лист)
- [Примеры](#примеры)
- [Скрипты](#скрипты)
- [Скиллы](#скиллы)

---

## Принципы

> **Impact создаётся только после Discussion в WAITING.** Parent Discussion обязателен. Без одобренной Discussion — нет Impact.

> **Роль — ПРЕДЛАГАТЕЛЬ.** Impact ПРЕДЛАГАЕТ варианты затронутых сервисов и характер влияния. Окончательные решения — на уровне Design.

> **Quick Scan до Clarify.** LLM сначала читает архитектурные документы (2 файла), затем формирует предложения. LLM НЕ спрашивает пользователя "какие сервисы затронуты?" — это работа LLM.

> **Файл до Clarify.** Сначала создать файл из шаблона и заполнить базовые поля — затем уточнять содержание. Это обеспечивает resumability при прерывании LLM.

> **Clarify до генерации.** LLM предлагает свои выводы через AskUserQuestion перед генерацией контента разделов. Пропуск — только по `--auto-clarify`.

> **DRAFT → WAITING — единственный переход этого документа.** Все последующие переходы управляются на уровне цепочки.

> **Документ без маркеров.** Воркфлоу создания завершается переводом в WAITING. Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` должны быть разрешены до ревью. LLM разрешает маркеры через AskUserQuestion — не ставит маркер и не идёт дальше.

---

## Шаги

### Шаг 1: Проверить parent Discussion

**SSOT:** [standard-impact.md § 1](./standard-impact.md#1-назначение)

1. Определить parent Discussion (из запроса пользователя или контекста)
2. Прочитать parent Discussion целиком — все разделы (проблема, фичи, требования, критерии успеха)
3. Проверить `status` в frontmatter parent Discussion:
   - `WAITING` → продолжить
   - Любой другой → **СТОП**: "Discussion должна быть в статусе WAITING для создания Impact"
4. Извлечь `milestone` из parent Discussion (будет скопирован в Impact)

### Шаг 2: Quick Scan архитектуры

**SSOT:** [standard-impact.md § 1](./standard-impact.md#1-назначение)

Прочитать **2 файла** (строго в указанном порядке):

| # | Файл | Зачем |
|---|------|-------|
| 1 | `specs/architecture/services/README.md` | Таблица сервисов, технологии, ключевые API |
| 2 | `specs/architecture/system/overview.md` | Общая картина, потоки между сервисами |

**Если файлы не существуют или содержат только шаблоны/заглушки** (новый проект): Quick Scan считается выполненным. LLM опирается на Discussion + Clarify и предлагает все сервисы как "Новый (план создания)" с уверенностью "Предположительно".

**Запрещено:** читать детальные файлы сервисов (`specs/architecture/services/{svc}.md`) — это задача Design-агента.

### Шаг 3–4: Определить номер и создать файл из шаблона

**SSOT:** [standard-impact.md § 2](./standard-impact.md#2-расположение-и-именование), [§ 7](./standard-impact.md#7-шаблон)

```bash
python specs/.instructions/.scripts/create-impact-file.py --parent specs/discussion/disc-NNNN-topic.md [topic]
```

Скрипт извлекает NNNN из parent Discussion и создаёт `specs/impact/impact-NNNN-topic.md` из шаблона. Topic извлекается из parent filename если не указан явно.

**Если `specs/impact/` не существует:** вызвать `/structure-create specs/impact`.

**Вручную (если скрипт недоступен):**
1. Проверить существующие файлы в `specs/impact/`
2. Номер = NNNN из parent Discussion (disc-0002 → impact-0002)
3. Сформировать имя: `impact-NNNN-topic.md` (topic — kebab-case, латиница)
4. Скопировать шаблон из [standard-impact.md § 7](./standard-impact.md#7-шаблон) и создать файл

### Шаг 5: Заполнить frontmatter

**SSOT:** [standard-impact.md § 3](./standard-impact.md#3-frontmatter)

Заполнить поля, известные до Clarify:

| Поле | Значение |
|------|----------|
| `description` | Краткое описание из запроса пользователя (до 1024 символов) |
| `standard` | `specs/.instructions/impact/standard-impact.md` |
| `standard-version` | `v1.0` |
| `index` | `specs/impact/README.md` |
| `parent` | Путь к parent Discussion (из шага 1). Если скрипт использован с `--parent` — заполняется автоматически. Иначе: заменить placeholder `discussion/disc-NNNN-topic.md` на реальный путь |
| `children` | `[]` (Design ещё не создан) |
| `status` | `DRAFT` |
| `milestone` | Значение из parent Discussion (скопировать, не спрашивать) |

### Шаг 6: Clarify

**SSOT:** [standard-impact.md § 6](./standard-impact.md#6-clarify), [Стандарт SDD § 8](../standard-specs.md#8-clarify-и-блокирующие-правила)

**Если `--auto-clarify` НЕ указан:**

LLM **сам анализирует** Quick Scan + Discussion и **предлагает** свои выводы. Пользователь подтверждает или корректирует. LLM **НЕ спрашивает** пользователя "какие сервисы затронуты?" — LLM предлагает свои выводы.

Уточнения через AskUserQuestion по таблице из [standard-impact.md § 6](./standard-impact.md#6-clarify):

| Что предлагает LLM | Пример |
|---------------------|--------|
| Затронутые сервисы | "По Discussion и architecture, затронуты auth (основной) и gateway (вторичный). Верно? Есть ли другие?" |
| Компоненты | "В auth предположительно затронуты: Token Generator, Auth Middleware. Подтверждаете?" |
| Данные | "Потребуется новая таблица refresh_tokens в PostgreSQL. Есть ли другие изменения данных?" |
| API | "Предлагается новый эндпоинт POST /auth/token. Есть ли другие API-изменения?" |
| Зависимости | "Появляется зависимость gateway → auth (sync REST). Верно?" |
| Риски | "Основной риск — даунтайм при миграции. Есть ли требования к zero-downtime?" |

**Если `--auto-clarify` указан:**

LLM пропускает Clarify, генерирует документ на основе своего понимания Discussion + Quick Scan и ставит маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` на все неясности.

**После Clarify:** Обновить frontmatter — `description` (уточнённое, если изменилось).

### Шаг 7: Заполнить разделы

**SSOT:** [standard-impact.md § 5](./standard-impact.md#5-разделы-документа)

На основе результатов Quick Scan (шаг 2), Discussion (шаг 1) и Clarify (шаг 6) заполнить **все 7 разделов**:

1. **Резюме** — scope влияния, характер изменений, ключевые risk areas (контент обязателен)
2. **Затронутые сервисы** — таблица SVC-N с типом влияния и уверенностью (минимум 1 элемент)
3. **Компоненты** — таблица CMP-N или заглушка: _Компоненты не идентифицированы._
4. **Данные и хранение** — таблица DATA-N или заглушка: _Изменений в данных нет._
5. **API** — таблица API-N или заглушка: _Изменений в API нет._
6. **Зависимости** — таблица DEP-N или заглушка: _Зависимостей нет._
7. **Риски** — таблица RISK-N (минимум 1 элемент)

**Маркеры:** Если информации недостаточно — ставить `[ТРЕБУЕТ УТОЧНЕНИЯ: вопрос]`. Не угадывать.

**Заглушки vs маркеры:**
- **Заглушка** — LLM **уверен**, что секция не применима (на основе Discussion + Clarify)
- **Маркер** — LLM **не имеет** достаточной информации для решения
- При `--auto-clarify`: если Discussion не даёт ясности — маркер, **не заглушка**

**Dependency Barrier:** Если генерация следующей секции зависит от неразрешённого маркера — остановить генерацию контента и перейти к перечислению оставшихся секций ([Стандарт SDD § 8](../standard-specs.md#dependency-barrier)).

**Upward feedback:** Если при анализе обнаружена информация, затрагивающая Discussion ([standard-impact.md § 5](./standard-impact.md#5-разделы-документа)):
1. Приостановить работу с Impact
2. Дополнить Discussion (статус остаётся WAITING)
3. AskUserQuestion: подтвердить изменения в Discussion
4. Возобновить работу с Impact

**Разрешение маркеров (обязательно перед продолжением):**

После заполнения всех разделов:

1. Проверить документ на наличие `[ТРЕБУЕТ УТОЧНЕНИЯ]` маркеров
2. Если маркеры есть — для каждого маркера уточнить через AskUserQuestion
3. Заменить маркеры на ответы пользователя
4. Если был Dependency Barrier — продолжить генерацию оставшихся секций
5. Повторять пока маркеров = 0

**Запрещено:** переводить документ в WAITING с неразрешёнными маркерами.

**Зона ответственности ([standard-impact.md § 1](./standard-impact.md#1-назначение)):**

При генерации контента убедиться, что документ НЕ содержит:
- Окончательное распределение ответственностей между сервисами (→ Design)
- Полные request/response контракты API (→ Design)
- Архитектурные решения (→ ADR)
- Тестовые сценарии (→ План тестов)
- Задачи на реализацию (→ План разработки)

### Шаг 8: Регистрация в README

Добавить запись в `specs/impact/README.md`:

```markdown
| NNNN | impact-NNNN-topic.md | DRAFT | disc-NNNN | — | vX.Y.Z | {Описание} |
```

### Шаг 8.5: Обновить parent Discussion

Обновить frontmatter parent Discussion — добавить Impact в `children`:

```yaml
children:
  - impact/impact-NNNN-topic.md
```

Обновить колонку Impact в `specs/discussion/README.md`: `—` → `impact-NNNN`.

### Шаг 9: Валидация

```bash
python specs/.instructions/.scripts/validate-impact.py specs/impact/impact-NNNN-topic.md
```

**Если скрипт недоступен:** пройти чек-лист из [validation-impact.md](./validation-impact.md).

Исправить ошибки до продолжения.

### Шаг 10: Ревью пользователем

**Перед вопросом:** проверить что маркеров = 0 и валидация пройдена. Если нет — вернуться к шагу 7.

**БЛОКИРУЮЩЕЕ.** AskUserQuestion: "Документ импакт-анализа готов. Всё корректно?"

| Ответ | Действие |
|-------|----------|
| Да, всё корректно | Перевести DRAFT → WAITING: обновить frontmatter (`status: WAITING`), обновить README → шаг 11 |
| Нет, нужны правки | Внести изменения → продолжить с шага 9 |

### Шаг 11: Отчёт о выполнении

Вывести отчёт:

```
## 📋 Отчёт о создании импакт-анализа

✅ **Создан импакт-анализ:** `specs/impact/impact-NNNN-topic.md`
📄 **Parent Discussion:** `disc-NNNN-topic.md`

📝 **Описание:** {description}

🏷️ **Milestone:** {vX.Y.Z}

📂 **Разделы:**
- {список заполненных разделов}

🏗️ **Затронутые сервисы:** {список SVC-N}

⚠️ **Риски:** {количество рисков}

🔄 **Статус:** DRAFT → WAITING

⏭️ **Следующий шаг:** Создать Design

✅ **Валидация:** пройдена
```

---

## Чек-лист

### Подготовка
- [ ] Parent Discussion в статусе WAITING
- [ ] Parent Discussion прочитана целиком
- [ ] Quick Scan выполнен (2 файла)
- [ ] Milestone извлечён из parent Discussion
- [ ] Определён номер NNNN
- [ ] Файл создан из шаблона

### Frontmatter
- [ ] `description` — до 1024 символов
- [ ] `standard` = `specs/.instructions/impact/standard-impact.md`
- [ ] `standard-version` = `v1.0`
- [ ] `index` = `specs/impact/README.md`
- [ ] `parent` — путь к Discussion-документу (обязателен)
- [ ] `children` = `[]`
- [ ] `status` — `DRAFT` → `WAITING`
- [ ] `milestone` — совпадает с milestone parent Discussion

### Clarify
- [ ] Clarify проведён (или `--auto-clarify`)
- [ ] LLM предложил свои выводы (не спрашивал пользователя)
- [ ] Frontmatter обновлён (description, если изменилось)

### Содержание
- [ ] Все 7 разделов присутствуют
- [ ] "Резюме" заполнено контентом
- [ ] "Затронутые сервисы" — минимум 1 элемент (SVC-N)
- [ ] "Затронутые сервисы" — каждый SVC-N имеет колонку "Уверенность"
- [ ] Новые сервисы помечены "Новый (план создания)"
- [ ] Shared-компоненты маркированы в колонке "Scope"
- [ ] "Риски" — минимум 1 элемент (RISK-N)
- [ ] Остальные разделы: контент или заглушка
- [ ] Нумерация без дублей (SVC-N, CMP-N, DATA-N, API-N, DEP-N, RISK-N)
- [ ] Все маркеры `[ТРЕБУЕТ УТОЧНЕНИЯ]` разрешены (0 неразрешённых)

### Зона ответственности
- [ ] Нет распределения ответственностей между сервисами (→ Design)
- [ ] Нет полных request/response контрактов API (→ Design)
- [ ] Нет архитектурных решений (→ ADR)
- [ ] Нет тестовых сценариев (→ План тестов)
- [ ] Нет задач на реализацию (→ План разработки)

### Проверка
- [ ] Валидация пройдена (скрипт или чек-лист)
- [ ] Запись добавлена в README
- [ ] `children` обновлён в parent Discussion
- [ ] Колонка Impact обновлена в Discussion README
- [ ] Ревью пользователем пройдено
- [ ] Статус переведён в WAITING
- [ ] README обновлён (статус WAITING)
- [ ] Отчёт выведен

---

## Примеры

### Создание импакта для новой функциональности

```
Пользователь: "Создай импакт для disc-0001-oauth2-authorization.md"

1. Parent Discussion: disc-0001, status=WAITING, milestone=v1.2.0
2. Quick Scan: services/README.md (auth, gateway, users), overview.md
3. Номер: impact-0001-oauth2-authorization.md
4. Файл создан из шаблона
5. Frontmatter: parent=disc-0001, milestone=v1.2.0, status=DRAFT
6. Clarify: LLM предлагает "auth (основной), gateway (вторичный), users (вторичный)"
   → Пользователь: "Верно, ещё notification-service (новый)"
7. Разделы: Резюме, SVC-1..SVC-4, CMP-1..CMP-4, DATA-1..DATA-2, API-1..API-3, DEP-1..DEP-2, RISK-1..RISK-2
   → Проверка маркеров: 0 → OK
8-9. README + Валидация
10. Ревью: "Да, всё корректно" → DRAFT → WAITING
11. Отчёт
```

### Создание импакта для группы багфиксов

```
Пользователь: "Создай импакт для disc-0005-cache-race-conditions.md"

1. Parent Discussion: disc-0005, status=WAITING, milestone=v1.1.1
2. Quick Scan: services/README.md (cache-service), overview.md
3. Номер: impact-0005-cache-race-conditions.md
4. Файл создан из шаблона
5. Frontmatter: parent=disc-0005, milestone=v1.1.1, status=DRAFT
6. Clarify: LLM предлагает "cache-service (основной, единственный затронутый)"
   → Пользователь: "Верно"
7. Разделы: Резюме, SVC-1, CMP-1..CMP-2, заглушки (данные, API, зависимости), RISK-1
   → Проверка маркеров: 0 → OK
8-9. README + Валидация
10. Ревью: "Да, всё корректно" → DRAFT → WAITING
11. Отчёт
```

### Создание с --auto-clarify

```
Пользователь: "Создай импакт для disc-0008-api-latency.md --auto-clarify"

1. Parent Discussion: disc-0008, status=WAITING, milestone=v2.0.0
2. Quick Scan: services/README.md, overview.md
3. Номер: impact-0008-api-latency-reduction.md
4. Файл создан из шаблона
5. Frontmatter: parent=disc-0008, milestone=v2.0.0, status=DRAFT
6. Clarify пропущен — маркеры на неясности
7. Разделы: генерация с маркерами [ТРЕБУЕТ УТОЧНЕНИЯ]
   → Разрешение маркеров: AskUserQuestion по каждому → замена → 0 маркеров
8-9. README + Валидация
10. Ревью: "Да, всё корректно" → DRAFT → WAITING
11. Отчёт
```

### Создание с upward feedback

```
Пользователь: "Создай импакт для disc-0010-payment-integration.md"

1. Parent Discussion: disc-0010, status=WAITING, milestone=v1.3.0
2. Quick Scan: services/README.md, overview.md
3-5. Файл создан, frontmatter заполнен
6. Clarify: LLM обнаружил зависимость от external payment provider (не указана в Discussion)
   → Upward feedback: приостановка Impact
   → Дополнить Discussion: добавить зависимость в scope
   → AskUserQuestion: "Обнаружена зависимость от payment provider. Добавлено в Discussion. Подтверждаете?"
   → Пользователь: "Да"
   → Возобновление Impact
7-11. Стандартный поток
```

---

## Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [create-impact-file.py](../.scripts/create-impact-file.py) | Создание файла импакт-анализа из шаблона (шаг 3–4) | Этот документ |
| [validate-impact.py](../.scripts/validate-impact.py) | Валидация созданного документа (шаг 9) | [validation-impact.md](./validation-impact.md) |

---

## Скиллы

| Скилл | Назначение | Инструкция |
|-------|------------|------------|
| [/impact-create](/.claude/skills/impact-create/SKILL.md) | Создание документа импакт-анализа | Этот документ |
