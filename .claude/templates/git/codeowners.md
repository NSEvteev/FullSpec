# CODEOWNERS Template

> **Источник:** [/.claude/instructions/git/review.md](/.claude/instructions/git/review.md)

## Шаблон

```
# .github/CODEOWNERS

# По умолчанию - вся команда
*                       @org/team

# Сервисы
/src/auth/              @org/auth-team
/src/notification/      @org/notify-team
/src/payment/           @org/payment-team
/src/users/             @org/users-team
/src/gateway/           @org/platform-team

# Инфраструктура
/platform/              @org/devops
/config/                @org/devops
/.github/workflows/     @org/devops

# Общий код - требует 2 approve
/shared/contracts/      @org/architects
/shared/libs/           @org/architects @org/backend-team

# Документация
/doc/                   @org/docs-team
/.claude/               @org/ai-team
/CLAUDE.md              @org/ai-team

# Конфигурации безопасности
/src/*/security/        @org/security-team
```

## Правила

| Правило | Описание |
|---------|----------|
| Один владелец | Каждый путь имеет чёткого владельца |
| Приоритет | Последнее совпадение имеет приоритет |
| Команды | Используйте `@org/team-name` для команд |
| Множественные владельцы | Можно указывать несколько через пробел |
| Wildcards | `*` для файлов, `**` для директорий |

## Требования approve

| Тип изменений | Требуется approve | От кого |
|---------------|-------------------|---------|
| Обычные изменения | 1 | Любой член команды |
| Изменения в shared/ | 2 | CODEOWNERS |
| Изменения в platform/ | 1 | DevOps |
| Breaking changes | 2 | Tech lead + CODEOWNERS |

<!-- Пример заполнения

# .github/CODEOWNERS

# Глобальные владельцы
*                           @company/backend-team

# Сервисы (каждая команда владеет своим)
/src/auth/                  @company/auth-team @john
/src/notification/          @company/notify-team
/src/payment/               @company/payment-team @jane
/src/users/                 @company/users-team
/src/gateway/               @company/platform-team

# Инфраструктура
/platform/                  @company/devops
/config/                    @company/devops
/.github/workflows/         @company/devops

# Общий код - требует внимания архитекторов
/shared/contracts/          @company/architects
/shared/libs/               @company/architects @company/backend-team

# Документация
/doc/                       @company/tech-writers
/.claude/                   @company/ai-team
/CLAUDE.md                  @company/ai-team

# Конфигурации безопасности
/src/*/security/            @company/security-team
-->
