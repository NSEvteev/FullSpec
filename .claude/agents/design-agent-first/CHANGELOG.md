# CHANGELOG — design-agent-first

## v3.0 (2026-02-27)

### Изменено
- Переименование: design-agent → design-agent-first (миграция)
- Разделение на два агента: design-agent-first (технологии + архитектура) + design-agent-second (контент SVC-N)
- Убраны фазы Generate SVC-N подсекций, INT-N, STS-N (перенесены в design-agent-second)
- Generate теперь создаёт: Резюме + Выбор технологий + заголовки SVC-N (h2, без подсекций)
- Добавлена секция "Выбор технологий" (7 критериев, AskUserQuestion пачками по 4)
- Добавлена честность оценок технологий (критерии 5-6 LLM)
- Добавлена поддержка --auto-clarify с маркерами в "Выбрано"
- max_turns: 50 → 60
- Валидация теперь частичная (полная — после design-agent-second)
- Обновлён формат вывода (partial design.md)

## v1.0 (2026-02-16)

### Добавлено
- Первая версия агента
- Deep Scan (6 источников архитектуры)
- CLARIFY → GENERATE → VALIDATE в изолированном контексте
- Генерация секций SVC/INT/STS, контрактов API, sequence-диаграмм
