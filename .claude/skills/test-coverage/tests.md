# Тесты: test-coverage

## TC-COVERAGE-001: Claude scope — все скиллы с тестами

**Предусловие:**
- Все скиллы имеют файл tests.md

**Шаги:**
1. Вызвать `/test-coverage claude`

**Ожидаемый результат:**
- Покрытие = 100%
- Список "Скиллы без тестов" пуст
- Подсчитаны тест-кейсы по статусам

**Статус:** pending

---

## TC-COVERAGE-002: Claude scope — скилл без тестов

**Предусловие:**
- Создан скилл `/.claude/skills/test-skill/SKILL.md`
- Файл tests.md отсутствует

**Шаги:**
1. Вызвать `/test-coverage claude`

**Ожидаемый результат:**
- Покрытие < 100%
- `test-skill` в списке "Скиллы без тестов"

**Статус:** pending

---

## TC-COVERAGE-003: JSON вывод

**Шаги:**
1. Вызвать `/test-coverage claude --json`

**Ожидаемый результат:**
- Валидный JSON
- Содержит поля: skills_total, skills_with_tests, skills_coverage, test_cases

**Статус:** pending

---

## TC-COVERAGE-004: Threshold — успех

**Шаги:**
1. Вызвать `/test-coverage claude --threshold 50`

**Ожидаемый результат:**
- При покрытии >= 50% — сообщение "✅ passed"
- Exit code 0

**Статус:** pending

---

## TC-COVERAGE-005: Threshold — провал

**Предусловие:**
- Реальное покрытие < 100%

**Шаги:**
1. Вызвать `/test-coverage claude --threshold 100`

**Ожидаемый результат:**
- Сообщение "❌ failed"
- Указано текущее покрытие и порог

**Статус:** pending

---

## TC-COVERAGE-006: Подсчёт тест-кейсов по статусам

**Шаги:**
1. Вызвать `/test-coverage claude --verbose`

**Ожидаемый результат:**
- Для каждого скилла показано количество тестов
- Разбивка по статусам: passed, failed, pending
- Итоговая сумма корректна

**Статус:** pending
