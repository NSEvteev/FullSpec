#!/usr/bin/env python3
"""
validate-redis-code.py — Валидация кода на соответствие standard-redis.md.

Использование:
    python validate-redis-code.py <файл или папка>
    python validate-redis-code.py <файл или папка> --verbose

Проверяет автоматизируемые правила из validation-redis.md:
    - RDS002: Inline-конструирование ключей (f-string/конкатенация в Redis-вызовах)
    - RDS004: Использование KEYS вместо SCAN
    - RDS008: Отсутствует сервис-префикс (ключ без двоеточия)

SSOT:
    - specs/technologies/standard-redis.md
    - specs/technologies/validation-redis.md

Примеры:
    python validate-redis-code.py src/notification/redis/
    python validate-redis-code.py src/notification/ --verbose

Возвращает:
    0 — все проверки пройдены
    1 — ошибки валидации
"""

import argparse
import re
import sys
from pathlib import Path


# Коды ошибок (автоматизируемые)
ERROR_CODES = {
    "RDS002": "Inline-конструирование ключей",
    "RDS004": "Использование KEYS вместо SCAN",
    "RDS008": "Ключ без сервис-префикса (нет двоеточия)",
}

# Redis-операции, принимающие ключ первым аргументом
REDIS_OPS = [
    "get", "set", "del", "delete", "exists", "expire", "ttl", "pttl",
    "hget", "hset", "hdel", "hgetall", "hmset", "hmget",
    "lpush", "rpush", "lpop", "rpop", "lrange", "llen",
    "sadd", "srem", "smembers", "sismember", "scard",
    "zadd", "zrem", "zrange", "zrangebyscore", "zscore", "zcard",
    "incr", "decr", "incrby", "decrby",
    "setex", "setnx", "psetex",
    "getset", "append", "mget", "mset",
    "publish", "subscribe",
]

# Паттерн: redis.operation(f"..." или "..." + ...)
REDIS_CALL_PATTERN = re.compile(
    r"\.(?:" + "|".join(REDIS_OPS) + r")\s*\(",
    re.IGNORECASE,
)

# Паттерн: redis.keys(...)
REDIS_KEYS_PATTERN = re.compile(
    r"\.keys\s*\(",
    re.IGNORECASE,
)

# Паттерн: команда KEYS в строковом литерале (для Redis CLI / raw commands)
KEYS_COMMAND_PATTERN = re.compile(
    r"""["']KEYS\s""",
)

# Файлы с Redis-импортами
REDIS_IMPORT_PATTERNS = [
    re.compile(r"(?:import|from)\s+.*redis", re.IGNORECASE),
    re.compile(r"(?:import|from)\s+.*ioredis", re.IGNORECASE),
    re.compile(r"require\s*\(\s*['\"](?:ioredis|redis)['\"]", re.IGNORECASE),
    re.compile(r"Redis\s*\(", re.IGNORECASE),
    re.compile(r"createClient\s*\(", re.IGNORECASE),
]


def is_comment(line: str, ext: str) -> bool:
    """Проверить, является ли строка комментарием."""
    stripped = line.strip()
    if not stripped:
        return True
    if ext in (".py",):
        return stripped.startswith("#")
    if ext in (".ts", ".js", ".tsx", ".jsx"):
        return stripped.startswith("//")
    return False


def has_redis_usage(content: str) -> bool:
    """Проверить, содержит ли файл Redis-импорты."""
    for pattern in REDIS_IMPORT_PATTERNS:
        if pattern.search(content):
            return True
    return False


def check_rds002(content: str, rel_path: str, ext: str) -> list[str]:
    """RDS002: Inline-конструирование ключей в Redis-вызовах."""
    errors = []
    for i, line in enumerate(content.split("\n"), 1):
        if is_comment(line, ext):
            continue
        # Найти Redis-вызов
        call_match = REDIS_CALL_PATTERN.search(line)
        if not call_match:
            continue

        # Посмотреть после вызова: f-string или конкатенация
        after_call = line[call_match.end():]

        # f-string: f"key:{var}" или f'key:{var}'
        if re.search(r'f["\']', after_call):
            errors.append(
                f"[RDS002] {rel_path}:{i}: inline f-string ключ в Redis-вызове "
                f"(вынеси в модуль keys)"
            )
            continue

        # Конкатенация: "key:" + var или `key:${var}`
        if re.search(r'["\'][^"\']*["\']\s*\+', after_call):
            errors.append(
                f"[RDS002] {rel_path}:{i}: inline конкатенация ключа в Redis-вызове "
                f"(вынеси в модуль keys)"
            )
            continue

        # Template literal: `key:${var}`
        if re.search(r'`[^`]*\$\{', after_call):
            errors.append(
                f"[RDS002] {rel_path}:{i}: inline template literal ключ в Redis-вызове "
                f"(вынеси в модуль keys)"
            )

    return errors


def check_rds004(content: str, rel_path: str, ext: str) -> list[str]:
    """RDS004: Использование KEYS вместо SCAN."""
    errors = []
    for i, line in enumerate(content.split("\n"), 1):
        if is_comment(line, ext):
            continue

        # .keys() вызов на Redis-клиенте
        if REDIS_KEYS_PATTERN.search(line):
            errors.append(
                f"[RDS004] {rel_path}:{i}: .keys() — используй SCAN вместо KEYS"
            )
            continue

        # Строковая команда "KEYS ..."
        if KEYS_COMMAND_PATTERN.search(line):
            errors.append(
                f"[RDS004] {rel_path}:{i}: команда KEYS — используй SCAN"
            )

    return errors


def check_rds008(content: str, rel_path: str, ext: str) -> list[str]:
    """RDS008: Ключ без сервис-префикса (нет двоеточия)."""
    errors = []
    for i, line in enumerate(content.split("\n"), 1):
        if is_comment(line, ext):
            continue
        # Найти Redis-вызов с строковым литералом-ключом
        call_match = REDIS_CALL_PATTERN.search(line)
        if not call_match:
            continue

        after_call = line[call_match.end():]
        # Строковый литерал сразу после (: "key" или 'key'
        str_match = re.match(r"""\s*["']([^"']+)["']""", after_call)
        if str_match:
            key_value = str_match.group(1)
            # Ключ должен содержать двоеточие (сервис-префикс)
            if ":" not in key_value and not key_value.startswith("*"):
                errors.append(
                    f"[RDS008] {rel_path}:{i}: ключ '{key_value}' без "
                    f"сервис-префикса (ожидается формат service:entity:id)"
                )

    return errors


def validate_file(file_path: Path, repo_root: Path, verbose: bool = False) -> list[str]:
    """Валидация одного файла."""
    errors = []
    try:
        rel = str(file_path.relative_to(repo_root))
    except ValueError:
        rel = str(file_path)
    content = file_path.read_text(encoding="utf-8")
    ext = file_path.suffix

    # Проверить, использует ли файл Redis
    if not has_redis_usage(content):
        if verbose:
            print(f"  ⏭ {rel}: нет Redis-операций, пропуск")
        return errors

    if verbose:
        print(f"\n📄 {rel}")

    # RDS002: inline ключи
    rds002 = check_rds002(content, rel, ext)
    errors.extend(rds002)
    if verbose and not rds002:
        print(f"    RDS002: inline ключи ✓")

    # RDS004: KEYS вместо SCAN
    rds004 = check_rds004(content, rel, ext)
    errors.extend(rds004)
    if verbose and not rds004:
        print(f"    RDS004: KEYS vs SCAN ✓")

    # RDS008: сервис-префикс
    rds008 = check_rds008(content, rel, ext)
    errors.extend(rds008)
    if verbose and not rds008:
        print(f"    RDS008: сервис-префикс ✓")

    return errors


def main():
    """Точка входа: парсинг аргументов и запуск валидации."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация кода на соответствие standard-redis.md"
    )
    parser.add_argument("path", nargs="*", help="Файлы .py/.ts/.js или папки")
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    if not (repo_root / ".git").exists():
        current = repo_root
        while current != current.parent:
            if (current / ".git").exists():
                repo_root = current
                break
            current = current.parent

    # Допустимые расширения
    valid_exts = {".py", ".ts", ".js", ".tsx", ".jsx"}

    # Собрать файлы
    files = []
    for p in args.path:
        target = Path(p)
        if not target.is_absolute():
            target = repo_root / target

        if target.is_dir():
            for ext in valid_exts:
                files.extend(sorted(target.rglob(f"*{ext}")))
        elif target.is_file() and target.suffix in valid_exts:
            files.append(target)

    if not files:
        if args.path:
            print("⚠ Нет файлов для валидации Redis-кода")
        sys.exit(0)

    print(f"🔍 Валидация Redis-кода ({len(files)} файлов)...")

    all_errors = []
    for f in files:
        file_errors = validate_file(f, repo_root, verbose=args.verbose)
        all_errors.extend(file_errors)

    if all_errors:
        print(f"\n❌ Найдено ошибок: {len(all_errors)}")
        for err in all_errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print("✅ Redis-код соответствует стандарту")
        sys.exit(0)


if __name__ == "__main__":
    main()
