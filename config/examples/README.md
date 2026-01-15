# Примеры конфигурационных файлов

Эта директория содержит примеры конфигурационных файлов для различных окружений и компонентов проекта.

## Структура

```
config/examples/
├── .env.development.example       # Переменные окружения для разработки
├── .env.production.example        # Переменные окружения для продакшена
├── .env.test.example              # Переменные окружения для тестов
├── database.config.example.json   # Конфигурация базы данных
├── logging.config.example.yaml    # Конфигурация логирования
└── README.md                      # Этот файл
```

## Использование

### Переменные окружения (.env файлы)

**Базовая настройка (для всех окружений):**
```bash
# Скопировать базовый шаблон
cp .env.example .env

# Отредактировать под свои нужды
nano .env
```

**Для конкретного окружения:**

**Development:**
```bash
cp config/examples/.env.development.example .env.development
```

**Production:**
```bash
cp config/examples/.env.production.example .env.production

# ВАЖНО: Заполните РЕАЛЬНЫЕ пароли и секреты!
# НИКОГДА не коммитьте .env.production в Git!
```

**Test:**
```bash
cp config/examples/.env.test.example .env.test
```

### Конфигурационные файлы

**База данных:**
```bash
cp config/examples/database.config.example.json config/database.json
```

**Логирование:**
```bash
cp config/examples/logging.config.example.yaml config/logging.yaml
```

## Приоритет загрузки переменных окружения

В большинстве фреймворков и библиотек используется следующий приоритет:

1. **Переменные окружения системы** (самый высокий приоритет)
2. **`.env.local`** (локальные переопределения, в `.gitignore`)
3. **`.env.[NODE_ENV]`** (специфичные для окружения)
4. **`.env`** (базовые настройки)

### Пример для Node.js

```javascript
// Загрузить .env файл в зависимости от окружения
const dotenv = require('dotenv');
const path = require('path');

// Загрузить базовые настройки
dotenv.config();

// Загрузить настройки для текущего окружения
const envFile = `.env.${process.env.NODE_ENV || 'development'}`;
dotenv.config({ path: path.resolve(process.cwd(), envFile) });

// Загрузить локальные переопределения (если есть)
dotenv.config({ path: path.resolve(process.cwd(), '.env.local') });
```

### Пример для Python

```python
# Загрузить .env файл
from dotenv import load_dotenv
import os

# Загрузить базовые настройки
load_dotenv()

# Загрузить настройки для текущего окружения
env = os.getenv('ENV', 'development')
load_dotenv(dotenv_path=f'.env.{env}')

# Загрузить локальные переопределения (если есть)
load_dotenv(dotenv_path='.env.local', override=True)
```

## Безопасность

### ⚠️ ВАЖНО: Что НЕ нужно коммитить в Git

Добавлено в `.gitignore`:
- `.env`
- `.env.local`
- `.env.*.local`
- `config/*.json` (кроме примеров)
- `config/*.yaml` (кроме примеров)

### ✅ Что можно коммитить

- `.env.example` — шаблоны БЕЗ секретов
- `config/examples/*` — примеры конфигураций
- Документация

### Генерация секретных ключей

**Node.js:**
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**Python:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**OpenSSL:**
```bash
openssl rand -hex 32
```

## Управление секретами в Production

Для продакшена рекомендуется использовать системы управления секретами:

- **AWS Secrets Manager** — для AWS инфраструктуры
- **HashiCorp Vault** — универсальное решение
- **Azure Key Vault** — для Azure
- **Google Secret Manager** — для GCP
- **Docker Secrets** — для Docker Swarm
- **Kubernetes Secrets** — для Kubernetes

Не храните секреты в `.env` файлах на продакшене!

## Дополнительные ресурсы

- [dotenv документация](https://github.com/motdotla/dotenv)
- [Twelve-Factor App: Config](https://12factor.net/config)
- [OWASP: Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
