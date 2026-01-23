---
type: standard
description: Аудит-логи (кто/что/когда), PII, GDPR, data retention
related:
  - /.claude/.instructions/src/security/auth.md
  - /.claude/.instructions/src/data/logging.md
  - /.claude/.instructions/platform/observability/logging.md
---

# Аудит и соответствие требованиям

Правила ведения аудит-логов, защиты персональных данных и соответствия GDPR.

## Оглавление

- [Аудит-логи](#аудит-логи)
- [Персональные данные (PII)](#персональные-данные-pii)
- [GDPR соответствие](#gdpr-соответствие)
- [Data Retention](#data-retention)
- [Реализация](#реализация)
- [Мониторинг и алерты](#мониторинг-и-алерты)
- [Связанные инструкции](#связанные-инструкции)

---

## Аудит-логи

### Принцип: Кто / Что / Когда

Каждое значимое действие фиксируется с ответом на три вопроса:

| Вопрос | Поле | Пример |
|--------|------|--------|
| **Кто** | `actor` | `user:123`, `svc-payment`, `system` |
| **Что** | `action`, `resource` | `create`, `users/456` |
| **Когда** | `timestamp` | `2024-01-15T10:30:00.000Z` |

### Структура аудит-записи

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "event_id": "evt_abc123",
  "event_type": "audit",

  "actor": {
    "type": "user",
    "id": "user-123",
    "ip": "192.168.1.100",
    "user_agent": "Mozilla/5.0..."
  },

  "action": "update",
  "resource": {
    "type": "user",
    "id": "user-456"
  },

  "context": {
    "service": "users-service",
    "request_id": "req-xyz",
    "session_id": "sess-789"
  },

  "changes": {
    "before": { "email": "old@example.com" },
    "after": { "email": "new@example.com" }
  },

  "result": "success",
  "metadata": {
    "reason": "User requested email change"
  }
}
```

### Обязательные поля

| Поле | Тип | Обязательность |
|------|-----|----------------|
| `timestamp` | ISO 8601 | Всегда |
| `event_id` | UUID | Всегда |
| `actor.type` | string | Всегда |
| `actor.id` | string | Всегда |
| `action` | string | Всегда |
| `resource.type` | string | Всегда |
| `resource.id` | string | Всегда |
| `result` | success/failure | Всегда |
| `context.service` | string | Всегда |
| `context.request_id` | string | Всегда |

### Действия для аудита

| Категория | Действия | Пример |
|-----------|----------|--------|
| **Аутентификация** | login, logout, password_change, mfa_enable | Вход пользователя |
| **Авторизация** | permission_grant, permission_revoke, role_assign | Назначение роли |
| **Данные пользователя** | create, update, delete, export | Изменение профиля |
| **Платежи** | charge, refund, subscription_change | Списание средств |
| **Админ-действия** | user_block, config_change, feature_toggle | Блокировка пользователя |
| **Системные** | service_start, migration_run, backup_create | Запуск сервиса |

### Разделение логов

```
Обычные логи (Loki)          Аудит-логи (отдельное хранилище)
────────────────────         ──────────────────────────────────
- DEBUG уровень              - Только значимые действия
- Технические детали         - Бизнес-события
- Короткое хранение (30 дней) - Долгое хранение (1-7 лет)
- Для отладки                - Для compliance
```

---

## Персональные данные (PII)

### Что считается PII

| Категория | Примеры | Уровень защиты |
|-----------|---------|----------------|
| **Идентификаторы** | Email, телефон, паспорт | Высокий |
| **Финансовые** | Номер карты, счёт | Критический |
| **Медицинские** | Диагнозы, история | Критический |
| **Биометрия** | Отпечатки, фото | Критический |
| **Местоположение** | Адрес, GPS | Высокий |
| **Демография** | Возраст, пол, раса | Средний |

### Правила обработки PII

| Правило | Описание |
|---------|----------|
| **Не логировать** | PII не попадает в обычные логи |
| **Маскировать** | При необходимости показать: `jo***@example.com` |
| **Шифровать at rest** | В БД — шифрование на уровне поля или диска |
| **Шифровать in transit** | Только HTTPS/TLS |
| **Минимизировать** | Собирать только необходимые данные |
| **Ограничить доступ** | PII доступен только авторизованным сервисам |

### Маскирование PII

```typescript
// utils/masking.ts
export const maskEmail = (email: string): string => {
  const [local, domain] = email.split('@');
  const maskedLocal = local.slice(0, 2) + '***';
  return `${maskedLocal}@${domain}`;
};

export const maskPhone = (phone: string): string => {
  return phone.slice(0, 4) + '****' + phone.slice(-2);
};

export const maskCardNumber = (card: string): string => {
  return '****' + card.slice(-4);
};

// Использование в логах
logger.info('User action', {
  email: maskEmail(user.email),  // jo***@example.com
  phone: maskPhone(user.phone),  // +7 9****45
});
```

### Классификация данных

```yaml
# data-classification.yaml
fields:
  - name: email
    classification: pii
    mask_type: email
    retention: account_lifetime

  - name: password_hash
    classification: sensitive
    mask_type: full
    retention: account_lifetime

  - name: ip_address
    classification: pii
    mask_type: partial
    retention: 90_days

  - name: payment_card
    classification: pci
    mask_type: card
    retention: transaction_only
```

---

## GDPR соответствие

### Права субъекта данных

| Право | Статья GDPR | Реализация |
|-------|-------------|------------|
| **Доступ** (Access) | Art. 15 | GET /api/v1/users/me/data |
| **Исправление** (Rectification) | Art. 16 | PATCH /api/v1/users/me |
| **Удаление** (Erasure) | Art. 17 | DELETE /api/v1/users/me |
| **Ограничение** (Restriction) | Art. 18 | POST /api/v1/users/me/restrict |
| **Переносимость** (Portability) | Art. 20 | GET /api/v1/users/me/export |
| **Возражение** (Objection) | Art. 21 | POST /api/v1/users/me/object |

### Right to be Forgotten (Право на удаление)

**Процесс:**

```
1. Пользователь запрашивает удаление
2. Верификация личности (подтверждение через email)
3. Период ожидания (14 дней, отмена возможна)
4. Soft delete: деактивация аккаунта
5. Уведомление связанных сервисов
6. Hard delete: удаление данных через 30 дней
7. Аудит-запись о удалении (без PII)
```

**API:**

```typescript
// POST /api/v1/users/me/deletion-request
{
  "confirmation": "DELETE MY ACCOUNT",
  "reason": "optional feedback"
}

// Response
{
  "request_id": "del-123",
  "status": "pending_confirmation",
  "confirmation_expires": "2024-01-16T10:30:00Z",
  "deletion_scheduled": "2024-01-30T10:30:00Z"
}
```

### Data Export (Право на переносимость)

```typescript
// GET /api/v1/users/me/export

// Response: JSON с всеми данными пользователя
{
  "export_date": "2024-01-15T10:30:00Z",
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z"
  },
  "orders": [...],
  "preferences": {...},
  "activity_log": [...],
  "download_url": "https://secure-export.example.com/exports/exp-abc.zip",
  "expires_at": "2024-01-22T10:30:00Z"
}
```

### Согласие (Consent)

```typescript
// Модель согласия
interface Consent {
  user_id: string;
  purpose: string;           // 'marketing', 'analytics', 'personalization'
  granted: boolean;
  granted_at: Date | null;
  revoked_at: Date | null;
  version: string;           // версия политики
  ip_address: string;
  user_agent: string;
}

// API
POST /api/v1/users/me/consents
GET /api/v1/users/me/consents
DELETE /api/v1/users/me/consents/{purpose}
```

---

## Data Retention

### Политика хранения

| Тип данных | Срок хранения | После истечения |
|------------|---------------|-----------------|
| **Аккаунт пользователя** | Пока активен + 30 дней | Hard delete |
| **Аудит-логи** | 7 лет | Архивация |
| **Транзакции** | 7 лет (бухгалтерия) | Архивация |
| **Сессии** | 30 дней | Удаление |
| **Логи приложения** | 30 дней | Удаление |
| **Backup** | 90 дней | Удаление |
| **Analytics (анонимные)** | 2 года | Агрегация |

### Автоматическое удаление

```yaml
# config/data-retention.yaml
retention_policies:
  - name: sessions
    table: user_sessions
    retention_days: 30
    deletion_strategy: hard_delete
    schedule: "0 2 * * *"  # ежедневно в 2:00

  - name: audit_logs
    table: audit_events
    retention_days: 2555  # 7 лет
    deletion_strategy: archive_then_delete
    archive_bucket: s3://audit-archive/

  - name: application_logs
    storage: loki
    retention_days: 30
    deletion_strategy: auto  # управляется Loki
```

### Реализация retention job

```typescript
// jobs/data-retention.ts
import { CronJob } from 'cron';

export const retentionJob = new CronJob('0 2 * * *', async () => {
  const policies = await loadRetentionPolicies();

  for (const policy of policies) {
    const cutoffDate = subDays(new Date(), policy.retentionDays);

    logger.info('Running retention policy', {
      policy: policy.name,
      cutoff_date: cutoffDate.toISOString(),
    });

    if (policy.deletionStrategy === 'archive_then_delete') {
      await archiveOldRecords(policy, cutoffDate);
    }

    const deleted = await deleteOldRecords(policy, cutoffDate);

    // Аудит-запись о выполнении retention
    await auditLog({
      action: 'retention_executed',
      resource: { type: 'policy', id: policy.name },
      metadata: { records_deleted: deleted, cutoff_date: cutoffDate },
    });
  }
});
```

---

## Реализация

### Audit Logger

```typescript
// services/audit-logger.ts
import { v4 as uuid } from 'uuid';

interface AuditEvent {
  actor: {
    type: 'user' | 'service' | 'system';
    id: string;
    ip?: string;
    userAgent?: string;
  };
  action: string;
  resource: {
    type: string;
    id: string;
  };
  changes?: {
    before?: Record<string, unknown>;
    after?: Record<string, unknown>;
  };
  result: 'success' | 'failure';
  metadata?: Record<string, unknown>;
}

export class AuditLogger {
  constructor(
    private service: string,
    private storage: AuditStorage
  ) {}

  async log(event: AuditEvent, context: RequestContext): Promise<void> {
    const record = {
      timestamp: new Date().toISOString(),
      event_id: uuid(),
      event_type: 'audit',
      ...event,
      context: {
        service: this.service,
        request_id: context.requestId,
        session_id: context.sessionId,
      },
    };

    // Маскировать PII в changes
    if (record.changes) {
      record.changes = this.maskPII(record.changes);
    }

    await this.storage.write(record);
  }

  private maskPII(changes: object): object {
    // Реализация маскирования
    return maskSensitiveFields(changes, PII_FIELDS);
  }
}
```

### Middleware для аудита

```typescript
// middleware/audit.ts
export function auditMiddleware(auditLogger: AuditLogger) {
  return async (req, res, next) => {
    const startTime = Date.now();

    // Сохраняем оригинальный end
    const originalEnd = res.end;

    res.end = function (...args) {
      // Логируем после завершения запроса
      const shouldAudit = AUDITED_ROUTES.some(route =>
        req.method === route.method && req.path.match(route.pattern)
      );

      if (shouldAudit) {
        auditLogger.log({
          actor: {
            type: req.user ? 'user' : 'service',
            id: req.user?.id || req.serviceAccount || 'anonymous',
            ip: req.ip,
            userAgent: req.headers['user-agent'],
          },
          action: `${req.method.toLowerCase()}_${extractResourceType(req.path)}`,
          resource: {
            type: extractResourceType(req.path),
            id: extractResourceId(req.path),
          },
          result: res.statusCode < 400 ? 'success' : 'failure',
          metadata: {
            status_code: res.statusCode,
            duration_ms: Date.now() - startTime,
          },
        }, req.context);
      }

      return originalEnd.apply(this, args);
    };

    next();
  };
}
```

### Хранилище аудит-логов

```typescript
// storage/audit-storage.ts

// Вариант 1: Отдельная БД (PostgreSQL)
export class PostgresAuditStorage implements AuditStorage {
  async write(record: AuditRecord): Promise<void> {
    await this.db.query(
      `INSERT INTO audit_events (event_id, timestamp, data)
       VALUES ($1, $2, $3)`,
      [record.event_id, record.timestamp, JSON.stringify(record)]
    );
  }
}

// Вариант 2: Object Storage (S3)
export class S3AuditStorage implements AuditStorage {
  async write(record: AuditRecord): Promise<void> {
    const key = `${record.timestamp.slice(0, 10)}/${record.event_id}.json`;
    await this.s3.putObject({
      Bucket: 'audit-logs',
      Key: key,
      Body: JSON.stringify(record),
    });
  }
}

// Вариант 3: Специализированное решение (Elasticsearch)
export class ElasticsearchAuditStorage implements AuditStorage {
  async write(record: AuditRecord): Promise<void> {
    await this.es.index({
      index: `audit-${record.timestamp.slice(0, 7)}`,
      document: record,
    });
  }
}
```

---

## Мониторинг и алерты

### Метрики аудита

```
# Количество аудит-событий
audit_events_total{service="users", action="login", result="success"}
audit_events_total{service="users", action="login", result="failure"}

# Латентность записи аудита
audit_write_duration_seconds_bucket{service="users", le="0.01"}

# Ошибки записи
audit_write_errors_total{service="users", error_type="storage_unavailable"}
```

### Алерты безопасности

```yaml
# platform/monitoring/alerts/security.yml
groups:
  - name: security
    rules:
      - alert: HighFailedLoginRate
        expr: |
          rate(audit_events_total{action="login", result="failure"}[5m])
          / rate(audit_events_total{action="login"}[5m]) > 0.3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High failed login rate (>30%)"

      - alert: SuspiciousDataExport
        expr: |
          increase(audit_events_total{action="data_export"}[1h]) > 10
        labels:
          severity: warning
        annotations:
          summary: "Multiple data exports in 1 hour"

      - alert: BulkDeletion
        expr: |
          increase(audit_events_total{action=~"delete.*"}[5m]) > 100
        labels:
          severity: critical
        annotations:
          summary: "Bulk deletion detected (>100 in 5 min)"
```

### Dashboard аудита

| Панель | Метрики |
|--------|---------|
| События по типу | Pie chart: action distribution |
| Успех/Ошибки | Time series: result success/failure |
| Топ пользователей | Table: actor.id by event count |
| Подозрительная активность | Alerts: failed logins, bulk operations |

---

## Скиллы

| Скилл | Описание |
|-------|----------|
| [/doc-create](/.claude/skills/doc-create/SKILL.md) | Документирование политик аудита |
| [/doc-update](/.claude/skills/doc-update/SKILL.md) | Обновление при изменении retention |
| [/links-validate](/.claude/skills/links-validate/SKILL.md) | Проверка ссылок в документации |
| [/issue-create](/.claude/skills/issue-create/SKILL.md) | Задачи по GDPR compliance |

---

## Связанные инструкции

- [auth.md](./auth.md) — аутентификация между сервисами
- [logging.md](/.claude/.instructions/src/data/logging.md) — формат логов
- [logging.md](/.claude/.instructions/platform/observability/logging.md) — централизованные логи
