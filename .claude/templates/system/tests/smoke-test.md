# Smoke Test Template

> **Источник:** [/.claude/instructions/tests/claude-testing.md](/.claude/instructions/tests/claude-testing.md)

Шаблон smoke-теста для проверки скиллов и инструкций Claude Code.

---

## Шаблон: Smoke test

```markdown
## Smoke test: {skill-name}

**Команда:** /{skill-name}
**Триггер:** "{фраза на русском}"

### Шаги

1. Ввести: `/{skill-name}`
2. Проверить, что скилл запрашивает параметры / выводит справку

### Ожидание

- Скилл распознаётся по команде
- Скилл не падает с ошибкой
- Скилл выводит ожидаемый формат ответа

### Результат

> /{skill-name}

{Вывод скилла}

### Статус

- [ ] Passed
- [ ] Failed

**Причина (если Failed):** {описание проблемы}
```

---

## Шаблон: Functional test

```markdown
## Functional test: {skill-name}

**Сценарий:** {Краткое описание что проверяем}

### Входные данные

- param1: {value1}
- param2: {value2}

### Шаги

1. {Первый шаг}
2. {Второй шаг}
3. Проверить результат

### Ожидаемый результат

- [ ] {Условие 1}
- [ ] {Условие 2}
- [ ] {Условие 3}

### Проверка

```bash
$ {команда проверки}
{ожидаемый вывод}
```

### Cleanup (если нужен)

```bash
$ {команда отката}
```

### Статус

- [ ] Passed
- [ ] Failed

**Причина (если Failed):** {описание проблемы}
```

---

## Шаблон: Integration test

```markdown
## Integration test: {workflow-name}

**Сценарий:** {Описание воркфлоу между скиллами}

### Участники

- {skill-1} - {роль}
- {skill-2} - {роль}

### Шаги

1. Выполнить: `/{skill-1} {params}`
2. Проверить промежуточный результат
3. Выполнить: `/{skill-2} {params}`
4. Проверить финальный результат

### Ожидаемый результат

- [ ] {skill-1} выполнился корректно
- [ ] Данные переданы в {skill-2}
- [ ] {skill-2} выполнился корректно
- [ ] Связи между артефактами установлены

### Статус

- [ ] Passed
- [ ] Failed

**Причина (если Failed):** {описание проблемы}
```

---

<!-- Пример заполнения: Smoke test

## Smoke test: issue-create

**Команда:** /issue-create
**Триггер:** "создай задачу"

### Шаги

1. Ввести: `/issue-create`
2. Проверить, что скилл запрашивает параметры

### Ожидание

- Скилл выводит список сервисов для выбора
- Запрашивает заголовок задачи
- Не падает с ошибкой

### Результат

> /issue-create

Для какого сервиса?
[1] auth
[2] notify
[3] payment

Выберите номер сервиса:

### Статус

- [x] Passed
- [ ] Failed

-->

<!-- Пример заполнения: Functional test

## Functional test: skill-create

**Сценарий:** Создание нового скилла test-example

### Входные данные

- name: test-example
- category: testing
- description: "Пример тестового скилла"

### Шаги

1. Выполнить: `/skill-create test-example`
2. Выбрать категорию: testing
3. Подтвердить метаданные
4. Проверить результат

### Ожидаемый результат

- [x] Создан файл `.claude/skills/test-example/SKILL.md`
- [x] Скилл добавлен в `skills/README.md`
- [x] Связанные скиллы обновлены

### Проверка

```bash
$ ls .claude/skills/test-example/
SKILL.md

$ grep "test-example" .claude/skills/README.md
| test-example | Пример тестового скилла | testing |
```

### Cleanup

```bash
$ rm -rf .claude/skills/test-example/
$ git checkout -- .claude/skills/README.md
```

### Статус

- [x] Passed
- [ ] Failed

-->

<!-- Пример заполнения: Integration test

## Integration test: instruction-create -> skill-create chain

**Сценарий:** Создание инструкции с автоматическим предложением создать скиллы

### Участники

- instruction-create - создаёт инструкцию
- skill-create - создаёт предложенные скиллы

### Шаги

1. Выполнить: `/instruction-create tests/example.md`
2. Заполнить инструкцию
3. Согласиться на создание предложенных скиллов
4. Проверить, что скиллы созданы через /skill-create

### Ожидаемый результат

- [x] Инструкция `.claude/instructions/tests/example.md` создана
- [x] Предложены релевантные скиллы для создания
- [x] Скиллы созданы через /skill-create
- [x] В скиллах есть ссылка на инструкцию
- [x] В инструкции есть раздел "Скиллы"

### Статус

- [x] Passed
- [ ] Failed

-->
