---
description: Инструкции для безопасности GitHub — Dependabot, Secret Scanning, security policies. Индекс документов.
standard: .structure/.instructions/standard-readme.md
standard-version: v1.2
index: .github/.instructions/actions/security/README.md
---

# Инструкции /.github/.instructions/actions/security/

Безопасность и сканирование.

**Полезные ссылки:**
- [Инструкции actions](../README.md)
- [Инструкции .github](../../README.md)
- [SSOT .github](../../../README.md)

**Содержание:** Dependabot, CodeQL, Secret Scanning, SECURITY.md.

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Стандарты](#1-стандарты) | — | Форматы и правила |
| [2. Воркфлоу](#2-воркфлоу) | — | Создание и изменение |
| [3. Валидация](#3-валидация) | — | Проверка согласованности |
| [4. Скрипты](#4-скрипты) | — | Автоматизация |
| [5. Скиллы](#5-скиллы) | — | Скиллы для этой области |

```
/.github/.instructions/actions/security/
├── README.md                           # Этот файл (индекс)
├── standard-secrets.md                 # Стандарт GitHub Secrets
├── standard-security.md                # Стандарт безопасности
└── validation-security.md              # Валидация файлов безопасности
```

---

# 1. Стандарты

## 1.1. Стандарт безопасности

Dependabot, Code Scanning (CodeQL), Secret Scanning и политика безопасности.

**Оглавление:**
- [Dependabot](./standard-security.md#3-dependabot)
- [Code Scanning](./standard-security.md#4-code-scanning-codeql)
- [Secret Scanning](./standard-security.md#5-secret-scanning)
- [SECURITY.md](./standard-security.md#6-securitymd)

**Инструкция:** [standard-security.md](./standard-security.md)

## 1.2. Стандарт GitHub Secrets

Именование, уровни хранения, ротация и категоризация секретов.

**Оглавление:**
- [Именование](./standard-secrets.md#2-именование)
- [Уровни хранения](./standard-secrets.md#3-уровни-хранения)
- [Категории](./standard-secrets.md#4-категории-секретов)
- [Ротация](./standard-secrets.md#5-ротация)

**Инструкция:** [standard-secrets.md](./standard-secrets.md)

---

# 2. Воркфлоу

*Нет воркфлоу.*

---

# 3. Валидация

| Документ | Описание |
|----------|----------|
| [validation-security.md](./validation-security.md) | Валидация файлов безопасности (SEC001-SEC010) |

---

# 4. Скрипты

| Скрипт | Назначение | Инструкция |
|--------|------------|------------|
| [validate-security.py](../../.scripts/validate-security.py) | Валидация файлов безопасности (SEC001-SEC010) | [validation-security.md](./validation-security.md) |

---

# 5. Скиллы

*Нет скиллов.*
