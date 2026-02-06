---
description: Стандарт формата YAML-шаблонов для GitHub Issues
standard: .instructions/standard-instruction.md
standard-version: v1.2
index: .github/.instructions/issues/issue-templates/README.md
---

# Стандарт YAML-шаблонов Issues

Версия стандарта: 1.3

Формат и правила создания шаблонов для GitHub Issues в `.github/ISSUE_TEMPLATE/`.

**Полезные ссылки:**
- [Инструкции issue-templates](./README.md)
- [Стандарт меток](../../labels/standard-labels.md)
- [Справочник меток](../../../labels.yml)

**Связанные документы:**

| Тип | Документ |
|-----|----------|
| Стандарт | Этот документ |
| Валидация | [validation-type-templates.md](./validation-type-templates.md) |
| Создание | *Не требуется (кросс-валидация)* |
| Модификация | *Не требуется (кросс-валидация)* |

## Оглавление

- [1. Назначение](#1-назначение)
- [2. Расположение и именование](#2-расположение-и-именование)
- [3. Формат YAML](#3-формат-yaml)
- [4. Обязательные поля верхнего уровня](#4-обязательные-поля-верхнего-уровня)
- [5. Поле body](#5-поле-body)
  - [Тип markdown](#тип-markdown)
  - [Тип input](#тип-input)
  - [Тип textarea](#тип-textarea)
  - [Тип dropdown](#тип-dropdown)
  - [Тип checkboxes](#тип-checkboxes)
- [6. Validations](#6-validations)
- [7. Предустановленные метки](#7-предустановленные-метки)
- [8. Файл config.yml](#8-файл-configyml)
- [9. Проверка валидности YAML](#9-проверка-валидности-yaml)
- [10. Тестирование шаблона](#10-тестирование-шаблона)
- [11. Примеры шаблонов](#11-примеры-шаблонов)

---

## 1. Назначение

**Что это:** YAML-шаблон для структурированного создания Issues через форму в GitHub UI.

**Применяется к:**
- GitHub Issues (не Pull Requests!)
- Формы создания задач в `.github/ISSUE_TEMPLATE/*.yml`

**Когда создавать шаблон (хотя бы одно условие):**
- Тип задачи используется регулярно (≥3 Issues в месяц) ИЛИ
- Задача требует структурированного ввода (например: шаги воспроизведения для баг-репорта) ИЛИ
- Требуются обязательные поля (например: версия окружения)

**Когда НЕ создавать:**
- Разовый тип задачи
- Задача не требует структуры (достаточно Blank Issue)
- Форма слишком сложная (>8 полей) — рассмотреть упрощение

**Цель:**
- Обеспечить структурированный ввод информации
- Автоматически добавлять метки к Issues
- Предоставить подсказки пользователю (placeholders, descriptions)
- Валидировать обязательные поля

**Принципы:**
- Один шаблон = один тип задачи
- Обязательные поля минимальны (≤ 3)
- Метки (labels) соответствуют системе меток проекта
- Описания полей помогают пользователю

---

## 2. Расположение и именование

**Путь:**
```
.github/ISSUE_TEMPLATE/{template-name}.yml
```

**Именование файла:**

| Правило | Пример ✅ | Пример ❌ |
|---------|----------|----------|
| Kebab-case | `bug-report.yml` | `bug_report.yml` |
| Латиница | `feature-request.yml` | `фича-запрос.yml` |
| Нижний регистр | `task.yml` | `Task.yml` |
| Расширение `.yml` | `bug-report.yml` | `bug-report.yaml` |

**Рекомендуемые имена для базовых шаблонов:**
- `bug-report.yml` — баг-репорт
- `feature-request.yml` — запрос новой функциональности
- `task.yml` — техническая задача

**Важно:** GitHub распознаёт файлы ТОЛЬКО в папке `.github/ISSUE_TEMPLATE/`. Вложенные папки игнорируются.

---

## 3. Формат YAML

**Структура файла:**
```yaml
name: {Название шаблона}
description: {Краткое описание}
title: {Префикс заголовка Issue}
labels: [{метка1}, {метка2}]
assignees: [{username1}]
body:
  - type: {тип поля}
    attributes:
      {атрибуты}
    validations:
      {правила валидации}
```

**Правила:**
- Отступы: 2 пробела (YAML standard)
- Кодировка: UTF-8
- Обязательные поля верхнего уровня: `name`, `description`, `body`
- Опциональные поля: `title`, `labels`, `assignees`

**Пример минимального шаблона:**
```yaml
name: Bug Report
description: Report a bug
body:
  - type: textarea
    attributes:
      label: Describe the bug
```

---

## 4. Обязательные поля верхнего уровня

### name (ОБЯЗАТЕЛЬНО)

**Тип:** string
**Назначение:** Название шаблона в UI выбора шаблонов.

**Правила:**
- Не более 60 символов
- Описательное название
- Без префиксов типа "Template:" или "Issue:"

**Примеры:**
```yaml
name: Bug Report  # ✅
name: Feature Request  # ✅
name: Template: Bug  # ❌ (префикс)
name: B  # ❌ (слишком короткое)
```

---

### description (ОБЯЗАТЕЛЬНО)

**Тип:** string
**Назначение:** Краткое описание назначения шаблона (показывается под названием в UI).

**Правила:**
- 1-2 предложения
- Объясняет когда использовать шаблон
- Не более 200 символов

**Примеры:**
```yaml
description: Report a bug or unexpected behavior  # ✅
description: Suggest a new feature or enhancement  # ✅
description: Bug  # ❌ (не описательно)
```

---

### title (ОПЦИОНАЛЬНО)

**Тип:** string
**Назначение:** Префикс или шаблон заголовка Issue.

**Правила:**
- Используется как placeholder в поле заголовка
- Может содержать placeholders для подстановки
- Пользователь может изменить

**Примеры:**
```yaml
title: "[Bug]: "  # ✅ Префикс
title: "[Feature Request]: "  # ✅
title: "Bug in module X"  # ❌ (слишком специфично)
```

---

### labels (ОПЦИОНАЛЬНО)

**Тип:** array[string]
**Назначение:** Автоматически добавляемые метки к Issue.

**Правила:**
- Метки ДОЛЖНЫ существовать в `.github/labels.yml`
- Список меток — см. [labels.yml](../../../labels.yml)
- Используется формат `{category}:{value}` (см. [standard-labels.md](../../labels/standard-labels.md))
- Количество меток не ограничено (но избегать дублирования категорий)

**Примеры:**
```yaml
labels:
  - type:bug  # ✅
  - priority:medium  # ✅

labels:
  - type:bug
  - type:feature  # ❌ (конфликт: несколько type:*)
```

**Важно:** Метки из шаблона ДОЛЖНЫ существовать в GitHub до создания шаблона. Проверить командой:
```bash
gh label list --search "type:bug"
```
Если метка отсутствует — создать через `gh label create` (см. [standard-labels.md](../../labels/standard-labels.md)). Без этой проверки Issue будет создан, но метка НЕ применится.

---

### assignees (ОПЦИОНАЛЬНО)

**Тип:** array[string]
**Назначение:** Автоматическое назначение исполнителей.

**Правила:**
- Username без `@` (например: `username`, не `@username`)
- Пользователи должны иметь доступ к репозиторию
- Используется редко (обычно назначается вручную)

**Примеры:**
```yaml
assignees:
  - owner  # ✅
  - @owner  # ❌ (не добавлять @)
```

---

### body (ОБЯЗАТЕЛЬНО)

**Тип:** array[object]
**Назначение:** Массив полей формы.

**Правила:**
- Минимум 1 поле
- Максимум 10 полей (рекомендация)
- Каждое поле имеет тип (type)

**Типы полей:**
- `markdown` — статичный текст (инструкции, примечания)
- `input` — однострочное поле ввода
- `textarea` — многострочное поле ввода
- `dropdown` — выбор из списка
- `checkboxes` — список чекбоксов

**Рекомендуемый порядок полей в body:**
1. `markdown` с инструкциями (в начале формы)
2. Основные поля ввода (`textarea` для описания, `input` для версии)
3. `textarea` для связанной документации (`related-docs`) — **обязательное**, см. ниже
4. `input` для зависимостей (`dependencies`) — **обязательное**, см. ниже
5. Дополнительные поля (`dropdown`, `textarea` для логов)
6. `checkboxes` с чек-листом (в конце формы)

**Принцип:** Обязательные поля — в начале, чек-листы и подтверждения — в конце.

**Поле Related Docs (обязательное):**

Каждый шаблон ДОЛЖЕН содержать поле связанной документации. Конвенция формата — [standard-issue.md § 4 Body](../standard-issue.md#body-структура-описания).

```yaml
- type: textarea
  id: related-docs
  attributes:
    label: Related Documentation
    description: "Project files that help understand the task context. Format: description — path. Write 'Связанной документации нет' if none"
    placeholder: |
      - Стандарт меток — .github/.instructions/labels/standard-labels.md
      - Справочник меток — .github/labels.yml
  validations:
    required: true
```

Поле обязательное (`required: true`): создатель Issue вынужден осознанно указать релевантные документы или явно написать "Связанной документации нет".

**Поле Dependencies (обязательное):**

Каждый шаблон ДОЛЖЕН содержать поле зависимостей. Конвенция формата — [standard-issue.md § 8](../standard-issue.md#8-декомпозиция-и-зависимости).

```yaml
- type: input
  id: dependencies
  attributes:
    label: Dependencies
    description: "Issues this depends on (e.g. #123, #124). Write 'None' if no dependencies"
    placeholder: "#123, #124 or None"
  validations:
    required: true
```

Поле обязательное (`required: true`): автор Issue вынужден осознанно оценить зависимости перед созданием. Если зависимостей нет — указать "None".

**Контекст для LLM:**

При создании или модификации Issue Template через LLM-агента, исполнитель должен получить контекстное окружение — список документов для понимания правил и структуры.

Формат: `{описание} - {путь}`

```
Стандарт YAML-шаблонов Issues - .github/.instructions/issues/issue-templates/standard-issue-template.md
Валидация Issue template - .github/.instructions/issues/issue-templates/validation-type-templates.md
Стандарт меток - .github/.instructions/labels/standard-labels.md
Справочник меток проекта - .github/labels.yml
```

LLM перед выполнением задачи читает документы из контекста для:
- Понимания формата и правил
- Проверки существующих меток
- Соблюдения naming conventions
- Валидации результата

---

## 5. Поле body

Каждый элемент `body` содержит:
- `type` — тип поля (ОБЯЗАТЕЛЬНО)
- `id` — уникальный идентификатор (ОПЦИОНАЛЬНО, но рекомендуется для не-markdown)
- `attributes` — атрибуты поля (ОБЯЗАТЕЛЬНО для всех типов кроме markdown)
- `validations` — правила валидации (ОПЦИОНАЛЬНО)

### Поле id

**Назначение:** Уникальный идентификатор поля для программного доступа.

**Зачем нужен:**
- Значения полей с `id` доступны через GitHub API в структурированном виде
- Позволяет автоматизировать обработку Issues (парсинг, триаж)
- `id` появляется в JSON при запросе Issue через API

**Правила:**
- Формат: kebab-case (`bug-description`, `steps-to-reproduce`)
- Уникальный в пределах одного шаблона
- Не использовать для `type: markdown` (игнорируется)

**Пример использования через API:**
```bash
# Получить Issue с полями
gh api repos/:owner/:repo/issues/123 --jq '.body'
# Поля с id доступны в структурированном формате
```

---

### Тип markdown

**Назначение:** Статичный текст (инструкции, предупреждения, форматирование).

**Атрибуты:**
- `value` (string, ОБЯЗАТЕЛЬНО) — markdown-содержимое

**Не имеет:**
- `id` (игнорируется)
- `validations` (игнорируется)

**Примеры:**
```yaml
- type: markdown
  attributes:
    value: |
      ## Instructions

      Please provide as much detail as possible.
```

**Использование:**
- Инструкции в начале формы
- Разделители между секциями
- Предупреждения (например: "Do not share sensitive data")

---

### Тип input

**Назначение:** Однострочное текстовое поле.

**Атрибуты:**
- `label` (string, ОБЯЗАТЕЛЬНО) — название поля
- `description` (string, ОПЦИОНАЛЬНО) — описание под полем
- `placeholder` (string, ОПЦИОНАЛЬНО) — placeholder в поле
- `value` (string, ОПЦИОНАЛЬНО) — значение по умолчанию

**Validations:**
- `required` (bool, по умолчанию `false`) — обязательность заполнения

**Примеры:**
```yaml
- type: input
  id: version
  attributes:
    label: Version
    description: Which version are you using?
    placeholder: "1.0.0"
  validations:
    required: true
```

**Применение:**
- Версия продукта
- URL
- Короткие идентификаторы

---

### Тип textarea

**Назначение:** Многострочное текстовое поле.

**Атрибуты:**
- `label` (string, ОБЯЗАТЕЛЬНО) — название поля
- `description` (string, ОПЦИОНАЛЬНО) — описание
- `placeholder` (string, ОПЦИОНАЛЬНО) — placeholder
- `value` (string, ОПЦИОНАЛЬНО) — значение по умолчанию
- `render` (string, ОПЦИОНАЛЬНО) — язык для подсветки синтаксиса (например: `bash`, `python`, `json`)

**Validations:**
- `required` (bool, по умолчанию `false`) — обязательность

**Примеры:**
```yaml
- type: textarea
  id: description
  attributes:
    label: Bug Description
    description: A clear description of the bug
    placeholder: "When I click X, Y happens instead of Z"
  validations:
    required: true
```

**С подсветкой синтаксиса:**
```yaml
- type: textarea
  id: logs
  attributes:
    label: Logs
    render: bash
```

**Поддерживаемые языки для `render`:**

| Язык | Значение `render` | Применение |
|------|-------------------|------------|
| Bash/Shell | `bash` | Логи, команды терминала |
| Python | `python` | Код, трейсбеки Python |
| JavaScript | `javascript` | Код JS/Node.js |
| TypeScript | `typescript` | Код TypeScript |
| JSON | `json` | Конфигурации, API ответы |
| YAML | `yaml` | Конфигурации |
| SQL | `sql` | Запросы к БД |
| Markdown | `markdown` | Форматированный текст |

**Применение:**
- Описание проблемы
- Шаги воспроизведения
- Логи (с `render: bash`)
- Ожидаемое поведение

---

### Тип dropdown

**Назначение:** Выбор одного значения из списка.

**Атрибуты:**
- `label` (string, ОБЯЗАТЕЛЬНО) — название поля
- `description` (string, ОПЦИОНАЛЬНО) — описание
- `multiple` (bool, по умолчанию `false`) — множественный выбор
- `options` (array[string], ОБЯЗАТЕЛЬНО) — список опций

**Validations:**
- `required` (bool, по умолчанию `false`) — обязательность

**Примеры:**
```yaml
- type: dropdown
  id: priority
  attributes:
    label: Priority
    description: How critical is this issue?
    options:
      - Critical
      - High
      - Medium
      - Low
  validations:
    required: true
```

**С множественным выбором:**
```yaml
- type: dropdown
  id: areas
  attributes:
    label: Affected Areas
    multiple: true
    options:
      - Backend
      - Frontend
      - Database
```

**Применение:**
- Приоритет
- Окружение (production, staging, local)
- Область кода (backend, frontend)

---

### Тип checkboxes

**Назначение:** Список чекбоксов (обычно для подтверждений).

**Атрибуты:**
- `label` (string, ОБЯЗАТЕЛЬНО) — название секции
- `description` (string, ОПЦИОНАЛЬНО) — описание
- `options` (array[object], ОБЯЗАТЕЛЬНО) — список чекбоксов

**Формат опции:**
```yaml
- label: {текст чекбокса}
  required: {true/false}
```

**Примеры:**
```yaml
- type: checkboxes
  id: checklist
  attributes:
    label: Checklist
    options:
      - label: I have searched for similar issues
        required: true
      - label: I have provided all required information
        required: true
      - label: I am willing to submit a PR
        required: false
```

**Применение:**
- Подтверждение прочтения инструкций
- Предварительные проверки (поиск дубликатов)
- Согласие с политиками

---

## 6. Validations

Правила валидации для полей `input`, `textarea`, `dropdown`, `checkboxes`.

**Доступные правила:**

| Правило | Тип | Применяется к | Описание |
|---------|-----|---------------|----------|
| `required` | bool | Все типы | Обязательность заполнения |

**Примеры:**
```yaml
validations:
  required: true  # Поле обязательно

validations:
  required: false  # Поле опционально (по умолчанию)
```

**Важно:**
- Если `required: true` — пользователь не сможет создать Issue без заполнения поля
- Для `checkboxes` — `required` применяется к каждому чекбоксу отдельно

---

## 7. Предустановленные метки

**SSOT:** [standard-labels.md](../../labels/standard-labels.md)

Метки автоматически применяются к Issue при создании через шаблон.

**Правила:**
- Метки ДОЛЖНЫ существовать в GitHub (создать перед использованием)
- Избегать конфликтов: не указывать несколько меток одной категории (например, два `type:*`)

Формат, категории и правила применения — см. SSOT.

### Соответствие type:* и шаблонов

**Для каждой метки `type:*` из [labels.yml](../../../labels.yml) ДОЛЖЕН существовать Issue Template.**

**Правила:**
- Шаблон ДОЛЖЕН содержать `labels: [type:{value}]`
- Именование файла: `{value}.yml`, `{value}-report.yml` или `{value}-request.yml`
- При добавлении метки `type:*` — создать шаблон (→ [standard-labels.md § 4](../../labels/standard-labels.md#4-связь-type-меток-с-issue-templates))
- При удалении метки `type:*` — удалить шаблон
- При создании шаблона — убедиться, что метка `type:*` существует в [labels.yml](../../../labels.yml)

**Валидация:**
```bash
python .github/.instructions/.scripts/validate-type-templates.py
```

> **Для LLM:** При создании/удалении Issue Template проверить соответствие с метками `type:*` в labels.yml.

---

## 8. Файл config.yml

**Путь:** `.github/ISSUE_TEMPLATE/config.yml`

**Назначение:** Конфигурация chooser (экран выбора шаблона).

**Структура:**
```yaml
blank_issues_enabled: {true/false}
contact_links:
  - name: {Название ссылки}
    url: {URL}
    about: {Описание}
```

**Поля:**

| Поле | Тип | Назначение |
|------|-----|------------|
| `blank_issues_enabled` | bool | Разрешить создание Blank Issue (без шаблона) |
| `contact_links` | array | Дополнительные ссылки в chooser (например: документация, чат) |

**Примеры:**
```yaml
blank_issues_enabled: false
contact_links:
  - name: Documentation
    url: https://docs.example.com
    about: Please check the documentation before opening an issue
  - name: Discord Community
    url: https://discord.gg/example
    about: Ask questions in our community
```

**Файл config.yml — ОПЦИОНАЛЕН.** Если его нет:
- Шаблоны работают как обычно
- Blank Issue доступен (как будто `blank_issues_enabled: true`)
- Contact links отсутствуют

Создавать `config.yml` если:
- Нужно отключить Blank Issue (`blank_issues_enabled: false`)
- Нужно добавить ссылки на документацию/чат (`contact_links`)

**Когда использовать `blank_issues_enabled: false`:**
- Все Issues должны проходить через шаблоны
- Требуется структурированный ввод

**Когда использовать `blank_issues_enabled: true`:**
- Нужна гибкость для нестандартных Issues
- Команда опытная и не требует подсказок

---

## 9. Проверка валидности YAML

GitHub тихо игнорирует невалидные YAML-шаблоны (ошибка не показывается).

**Типичные ошибки:**
- Неправильные отступы (должны быть 2 пробела)
- Табы вместо пробелов
- Опечатка в ключе (например: `lables` вместо `labels`)
- Отсутствие обязательного поля (например: `name`)

**Валидация перед коммитом:**
```bash
# Проверить синтаксис YAML
yamllint .github/ISSUE_TEMPLATE/bug-report.yml

# Или через скрипт валидации
python .github/.instructions/.scripts/validate-issue-template.py bug-report.yml
```

**После создания шаблона — ОБЯЗАТЕЛЬНО выполнить валидацию:**
См. [validation-type-templates.md](./validation-type-templates.md)

---

## 10. Тестирование шаблона

GitHub не поддерживает preview шаблонов без коммита. Процедура тестирования:

**Процесс:**

1. **Создать feature-ветку:**
   ```bash
   git checkout -b feat/add-issue-template
   ```

2. **Добавить шаблон:**
   ```bash
   # Создать/изменить файл
   git add .github/ISSUE_TEMPLATE/new-template.yml
   git commit -m "feat: add new issue template"
   git push -u origin feat/add-issue-template
   ```

3. **Протестировать в GitHub UI:**
   - Перейти в репозиторий → Issues → New Issue
   - GitHub покажет шаблоны из текущей ветки (если PR открыт)
   - Проверить: форма отображается корректно, поля работают

4. **Исправить и повторить** (если нужно):
   ```bash
   # Внести правки
   git add . && git commit -m "fix: adjust template fields"
   git push
   ```

5. **Создать PR и смержить** после успешного тестирования

**Чек-лист тестирования:**
- [ ] Шаблон появляется в списке выбора
- [ ] Название и описание корректны
- [ ] Все поля отображаются
- [ ] Обязательные поля помечены звёздочкой (*)
- [ ] Placeholders и descriptions понятны
- [ ] Метки применяются при создании Issue

---

## 11. Примеры шаблонов

**Перед использованием примеров:** Убедиться, что метки из `labels:` существуют в вашем репозитории (см. [standard-labels.md](../../labels/standard-labels.md) и [labels.yml](../../../labels.yml)).

### Пример: bug-report.yml

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels:
  - type:bug
  - priority:medium
body:
  - type: markdown
    attributes:
      value: |
        ## Thank you for reporting a bug!

        Please provide as much detail as possible.

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of the bug
      placeholder: "When I click X, Y happens instead of Z"
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this issue?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: input
    id: version
    attributes:
      label: Version
      description: Which version are you using?
      placeholder: "v1.0.0"
    validations:
      required: true

  - type: textarea
    id: related-docs
    attributes:
      label: Related Documentation
      description: "Project files that help understand the task context. Format: description — path. Write 'Связанной документации нет' if none"
      placeholder: |
        - Стандарт меток — .github/.instructions/labels/standard-labels.md
    validations:
      required: true

  - type: input
    id: dependencies
    attributes:
      label: Dependencies
      description: "Issues this depends on (e.g. #123, #124). Write 'None' if no dependencies"
      placeholder: "#123, #124 or None"
    validations:
      required: true

  - type: dropdown
    id: environment
    attributes:
      label: Environment
      description: Where did the bug occur?
      options:
        - Production
        - Staging
        - Local
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Logs
      description: Paste any relevant logs
      render: bash

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have searched for similar issues
          required: true
        - label: I have provided all required information
          required: true
```

---

### Пример: feature-request.yml

```yaml
name: Feature Request
description: Suggest a new feature or enhancement
title: "[Feature]: "
labels:
  - type:feature
  - priority:low
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this feature solve?
      placeholder: "I'm frustrated when..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this feature work?
      placeholder: "It should..."
    validations:
      required: true

  - type: textarea
    id: related-docs
    attributes:
      label: Related Documentation
      description: "Project files that help understand the task context. Format: description — path. Write 'Связанной документации нет' if none"
      placeholder: |
        - Стандарт меток — .github/.instructions/labels/standard-labels.md
    validations:
      required: true

  - type: input
    id: dependencies
    attributes:
      label: Dependencies
      description: "Issues this depends on (e.g. #123, #124). Write 'None' if no dependencies"
      placeholder: "#123, #124 or None"
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: What other solutions have you considered?

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have searched for similar feature requests
          required: true
        - label: I am willing to help implement this feature
          required: false
```

---

### Пример: task.yml

```yaml
name: Task
description: Technical task or improvement
title: "[Task]: "
labels:
  - type:task
body:
  - type: textarea
    id: description
    attributes:
      label: Task Description
      description: What needs to be done?
    validations:
      required: true

  - type: textarea
    id: related-docs
    attributes:
      label: Related Documentation
      description: "Project files that help understand the task context. Format: description — path. Write 'Связанной документации нет' if none"
      placeholder: |
        - Стандарт меток — .github/.instructions/labels/standard-labels.md
    validations:
      required: true

  - type: input
    id: dependencies
    attributes:
      label: Dependencies
      description: "Issues this depends on (e.g. #123, #124). Write 'None' if no dependencies"
      placeholder: "#123, #124 or None"
    validations:
      required: true

  - type: dropdown
    id: area
    attributes:
      label: Area
      description: Which part of the codebase?
      multiple: true
      options:
        - Backend
        - Frontend
        - Database
        - Infrastructure
    validations:
      required: true

  - type: checkboxes
    id: subtasks
    attributes:
      label: Subtasks
      description: Break down the task if possible
      options:
        - label: Subtask 1
        - label: Subtask 2
```

---

### Пример: question.yml

```yaml
name: Question
description: Ask a question about the project
title: "[Question]: "
labels:
  - type:question
body:
  - type: markdown
    attributes:
      value: |
        ## Before asking

        Please check the documentation and existing issues first.

  - type: textarea
    id: question
    attributes:
      label: Your Question
      description: What would you like to know?
      placeholder: "How do I configure..."
    validations:
      required: true

  - type: textarea
    id: related-docs
    attributes:
      label: Related Documentation
      description: "Project files that help understand the question context. Format: description — path. Write 'Связанной документации нет' if none"
      placeholder: |
        - Стандарт меток — .github/.instructions/labels/standard-labels.md
    validations:
      required: true

  - type: input
    id: dependencies
    attributes:
      label: Dependencies
      description: "Related issues (e.g. #123, #124). Write 'None' if no related issues"
      placeholder: "#123, #124 or None"
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Context
      description: What are you trying to achieve? This helps us give a better answer.

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have checked the documentation
          required: true
        - label: I have searched existing issues
          required: true
```

---

### Пример: config.yml

```yaml
blank_issues_enabled: false
contact_links:
  - name: Documentation
    url: https://github.com/owner/repo/wiki
    about: Check the documentation first
  - name: Discussions
    url: https://github.com/owner/repo/discussions
    about: Ask questions in Discussions
```

---

## Скиллы

*Нет скиллов.*
