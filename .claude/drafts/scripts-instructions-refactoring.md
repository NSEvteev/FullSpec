# Draft: Рефакторинг инструкций скриптов

**Статус:** DONE
**Дата:** 2026-01-28

## Цель

Обновить инструкции скриптов для:
1. Автоматизации шагов в инструкциях через скрипты
2. Добавления принципов программирования (вынесены в отдельный стандарт)
3. Интеграции скриптов с инструкциями create/modify/validation

## Выполненные задачи

### 1. standard-principles.md ✅ (НОВЫЙ)
- [x] Вынесены принципы программирования в отдельный стандарт
- [x] Структура по standard-instruction.md
- [x] 8 принципов с примерами кода:
  - KISS, DRY, YAGNI
  - Принцип наименьшего удивления
  - SOLID
  - Читаемость и документация
  - Обработка ошибок
  - Минимизация зависимостей

### 2. validation-principles.md ✅ (НОВЫЙ)
- [x] Валидация соблюдения принципов
- [x] Шаги проверки для каждого принципа
- [x] Команды поиска нарушений
- [x] Коды ошибок P001-P008

### 3. standard-script.md ✅
- [x] Секция 2 заменена на ссылку: `SSOT: standard-principles.md`
- [x] Добавлено: скрипты автоматизируют шаги в инструкциях (§ 1)
- [x] Паттерны именования: parse-{object}.py, find-{criteria}.py
- [x] Пример скрипта find-by-frontmatter.py

### 4. create-script.md ✅
- [x] Ссылки на принципы → standard-principles.md
- [x] Вызывается при создании/модификации инструкций
- [x] Скрипты только для validation/create/modify
- [x] Шаг 1: проверка существующих через parse-docstrings.py

### 5. modify-script.md ✅
- [x] Ссылка на принципы → standard-principles.md
- [x] Шаг 4: обновление инструкций
- [x] Вызов /instruction-modify после изменений

### 6. validation-script.md ✅
- [x] Ссылка на принципы → standard-principles.md
- [x] Ссылка на валидацию → validation-principles.md
- [x] Шаг 4: проверка принципов

### 7. create-instruction.md ✅
- [x] Шаг 5: создать скрипты (если нужно)
- [x] Шаг 6: обновить README области

### 8. parse-docstrings.py ✅
- [x] Создан скрипт поиска по docstring

## Созданные файлы

| Файл | Тип |
|------|-----|
| `.instructions/standard-principles.md` | Новый стандарт |
| `.instructions/validation-principles.md` | Новая валидация |
| `.instructions/.scripts/parse-docstrings.py` | Новый скрипт |

## Изменённые файлы

| Файл | Изменения |
|------|-----------|
| `.instructions/standard-script.md` | Ссылка на standard-principles.md |
| `.instructions/create-script.md` | Ссылки на standard-principles.md |
| `.instructions/modify-script.md` | Ссылки на standard-principles.md |
| `.instructions/validation-script.md` | Ссылки на standard/validation-principles.md |
| `.instructions/create-instruction.md` | Шаг создания скриптов |

## Структура инструкций принципов

```
standard-principles.md      ← SSOT принципов
    ↓
validation-principles.md    ← Как проверять
```

Ссылаются из:
- standard-script.md § 2
- create-script.md (принципы)
- modify-script.md (соблюдение)
- validation-script.md (проверка)
