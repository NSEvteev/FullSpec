---
description: Артефакты тестового прогона цепочки 0001-task-dashboard — список файлов для удаления после теста.
status: active
---

# Артефакты тестового прогона 0001

Тестовый прогон `/chain` на цепочке `0001-task-dashboard`. Все артефакты ниже созданы агентами и подлежат удалению после завершения теста.

## Per-service docs

| Файл | Создан |
|------|--------|
| `specs/docs/task.md` | service-agent (SVC-1) |
| `specs/docs/auth.md` | service-agent (SVC-2) |
| `specs/docs/frontend.md` | service-agent (SVC-3) |

## Per-tech стандарты

| Файл | Создан |
|------|--------|
| `specs/docs/.technologies/standard-react.md` | technology-agent |
| `specs/docs/.technologies/standard-typescript.md` | technology-agent |
| `specs/docs/.technologies/standard-postgresql.md` | technology-agent |
| `specs/docs/.technologies/standard-prisma.md` | technology-agent |
| `specs/docs/.technologies/standard-express.md` | technology-agent |
| `specs/docs/.technologies/standard-jose.md` | technology-agent |

## Security стандарты

| Файл | Создан |
|------|--------|
| `specs/docs/.technologies/security-typescript.md` | technology-agent |

## Rules

| Файл | Создан |
|------|--------|
| `.claude/rules/react.md` | technology-agent |
| `.claude/rules/typescript.md` | technology-agent |
| `.claude/rules/postgresql.md` | technology-agent |
| `.claude/rules/prisma.md` | technology-agent |
| `.claude/rules/express.md` | technology-agent |
| `.claude/rules/jose.md` | technology-agent |

## GitHub Issues

| TASK | Issue | Сервис |
|------|-------|--------|
| TASK-1 | #42 | INFRA |
| TASK-2 | #43 | task |
| TASK-3 | #44 | task |
| TASK-4 | #45 | task |
| TASK-5 | #46 | task |
| TASK-6 | #47 | task |
| TASK-7 | #48 | task |
| TASK-8 | #49 | auth |
| TASK-9 | #50 | auth |
| TASK-10 | #51 | auth |
| TASK-11 | #52 | auth |
| TASK-12 | #53 | auth |
| TASK-13 | #54 | frontend |
| TASK-14 | #55 | frontend |
| TASK-15 | #56 | frontend |
| TASK-16 | #57 | frontend |
| TASK-17 | #58 | frontend |
| TASK-18 | #59 | frontend |
| TASK-19 | #60 | system |
| TASK-20 | #61 | system |

## GitHub Milestone

| Milestone | Номер |
|-----------|-------|
| v0.1.0 | #1 |

## Branch

| Ветка | Base |
|-------|------|
| `0001-task-dashboard` | main |

## Обновлённые файлы (восстановить из git)

| Файл | Что изменилось |
|------|---------------|
| `specs/docs/.system/overview.md` | system-agent mode=sync |
| `specs/docs/README.md` | Строки сервисов + таблица технологий + дерево |
