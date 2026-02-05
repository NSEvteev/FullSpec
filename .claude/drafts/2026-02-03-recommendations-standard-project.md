# Рекомендации по дополнению standard-project.md

**Дата:** 2026-02-03
**Статус:** draft
**Проанализированный документ:** `.github/.instructions/projects/standard-project.md`

---

## Краткая оценка

Документ **практичный** с чётким позиционированием: Projects опциональны для маленьких команд.

**Сильные стороны:**
- Явные критерии "когда использовать / когда не использовать"
- Полный список CLI команд для Projects
- Таблица лимитов GitHub
- Последовательность создания проекта (пошаговая)

## Рекомендации по улучшению

### 1. Не описано: миграция с GitHub Projects Classic

**Проблема:** Стандарт описывает Projects v2, но многие проекты используют Classic.

**Рекомендация:** Добавить секцию "Миграция с Projects Classic":
- Projects Classic deprecated с 2024
- Автоматическая миграция GitHub
- Ручная миграция: экспорт → создание нового → импорт

### 2. Неясность: Draft items vs Issues

**Проблема:** Упоминаются Draft items, но не описано:
- Когда использовать Draft вместо Issue
- Как конвертировать Draft в Issue

**Рекомендация:** Добавить подсекцию "Draft Items":
- Использовать для быстрых идей без формализации
- Конвертация: открыть Draft → "Convert to Issue"
- Не использовать для задач, которые пойдут в работу

### 3. Не описано: множественные Projects

**Проблема:** Примеры для одного проекта, но не описано когда создавать несколько.

**Рекомендация:** Добавить рекомендации:
| Сценарий | Количество Projects |
|----------|---------------------|
| Один продукт | 1 Project |
| Монорепо с разными командами | 1 Project на команду |
| Публичный + внутренний backlog | 2 Projects (public + private) |

### 5. Не описано: архивация Projects

**Проблема:** Описано `gh project close`, но не описана архивация завершённых проектов.

**Рекомендация:** Добавить секцию "Архивация":
- Закрытый Project доступен для просмотра
- Для полной архивации: экспорт данных → delete
- GitHub не имеет "archive" функции — только close или delete

### 6. Неясность: item-edit для установки Status

**Проблема:** Пример `gh project item-edit` требует знания множества ID (item-id, field-id, option-id).

**Рекомендация:** Добавить полный скрипт:
```bash
# Получить все необходимые ID и установить Status = "In Progress"
PROJECT=1
OWNER="@me"
ISSUE=123

ITEM_ID=$(gh project item-list $PROJECT --owner $OWNER --format json | jq -r ".items[] | select(.content.number==$ISSUE) | .id")
FIELD_ID=$(gh project field-list $PROJECT --owner $OWNER --format json | jq -r '.fields[] | select(.name=="Status") | .id')
OPTION_ID=$(gh project field-list $PROJECT --owner $OWNER --format json | jq -r '.fields[] | select(.name=="Status") | .options[] | select(.name=="In Progress") | .id')

gh project item-edit --project-id $PROJECT --id $ITEM_ID --field-id $FIELD_ID --single-select-option-id $OPTION_ID
```

### 8. Мелкое: нет примера Roadmap View с Date полем

**Проблема:** Описано что Roadmap требует Date поле, но нет примера создания.

**Рекомендация:** Добавить:
```bash
# Создать поле Due Date
gh project field-create 1 --owner @me --name "Due Date" --data-type "DATE"
```

И пояснение: после создания поля — элементы появятся на Roadmap timeline.

---

## Проверка границ SSOT

| Что | В этом стандарте? | Где должно быть? |
|-----|-------------------|------------------|
| Свойства Project | ✅ Да | — |
| Views и Fields | ✅ Да | — |
| CLI команды | ✅ Да | — |
| Автоматизация | ✅ Да | — |
| Issues | ✅ Ссылка | standard-issue.md |
| Pull Requests | ✅ Ссылка | standard-pull-request.md |
| Milestones | ✅ Ссылка | standard-milestone.md |

**Вывод:** Границы SSOT соблюдены. Хорошее разделение между Project (визуализация) и Issues/Milestones (данные).

---

## Итог

- **Качество:** 8/10
- **Полнота:** 7/10
- **Необходимые доработки:** средние (Draft items, множественные Projects, скрипт item-edit)
