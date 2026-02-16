#!/usr/bin/env python3
"""
validate-postgresql-code.py — Валидация SQL-кода на соответствие standard-postgresql.md.

Использование:
    python validate-postgresql-code.py <файл или папка>
    python validate-postgresql-code.py <файл или папка> --verbose

Проверяет автоматизируемые правила из validation-postgresql.md:
    - PG001: Таблицы snake_case, множественное число (CREATE TABLE)
    - PG002: Колонки snake_case (определения колонок)
    - PG003: FK без индекса (FOREIGN KEY без CREATE INDEX)
    - PG004: TIMESTAMP вместо TIMESTAMPTZ
    - PG005: SELECT * в запросах
    - PG007: Формат имени файла миграций ({NNN}_{description}.sql)
    - PG009: SQL keywords не в UPPER CASE

SSOT:
    - specs/technologies/standard-postgresql.md
    - specs/technologies/validation-postgresql.md

Примеры:
    python validate-postgresql-code.py src/notification/database/
    python validate-postgresql-code.py src/notification/database/migrations/001_create_tables.sql --verbose

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
    "PG001": "Таблица не в snake_case",
    "PG002": "Колонка не в snake_case",
    "PG003": "Foreign key без индекса",
    "PG004": "TIMESTAMP вместо TIMESTAMPTZ",
    "PG005": "SELECT * в запросе",
    "PG007": "Имя файла миграции не соответствует формату",
    "PG009": "SQL keyword не в UPPER CASE",
}

SNAKE_CASE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$")
MIGRATION_NAME = re.compile(r"^\d{3}_[a-z0-9_]+\.sql$")

# SQL keywords, которые должны быть UPPER CASE
SQL_KEYWORDS = [
    "SELECT", "INSERT", "UPDATE", "DELETE", "FROM", "WHERE",
    "JOIN", "LEFT", "RIGHT", "INNER", "OUTER", "FULL",
    "CREATE", "ALTER", "DROP", "TABLE", "INDEX", "VIEW",
    "INTO", "VALUES", "SET", "ORDER", "GROUP", "HAVING",
    "LIMIT", "OFFSET", "ON", "AND", "OR", "NOT", "IN",
    "EXISTS", "BETWEEN", "LIKE", "IS", "NULL", "AS",
    "PRIMARY", "FOREIGN", "KEY", "REFERENCES", "CONSTRAINT",
    "UNIQUE", "DEFAULT", "CHECK", "CASCADE", "RESTRICT",
    "BEGIN", "COMMIT", "ROLLBACK", "GRANT", "REVOKE",
    "UNION", "EXCEPT", "INTERSECT", "RETURNING", "WITH",
    "CASE", "WHEN", "THEN", "ELSE", "END",
    "TYPE", "ENUM", "FUNCTION", "TRIGGER", "PROCEDURE",
    "ADD", "COLUMN",
]

# Слова, которые часто являются идентификаторами, а не ключевыми словами
KEYWORD_EXCEPTIONS = {"id", "name", "type", "key", "set", "index", "view", "end",
                       "column", "add", "check", "in", "on", "as", "is", "not",
                       "or", "and", "null", "between", "like", "exists", "case",
                       "when", "then", "else", "with"}


def is_comment_or_empty(line: str) -> bool:
    """Проверить, является ли строка комментарием или пустой."""
    stripped = line.strip()
    return not stripped or stripped.startswith("--")


def is_in_string(line: str, pos: int) -> bool:
    """Примитивная проверка: находится ли позиция внутри строкового литерала."""
    in_string = False
    quote_char = None
    for i, ch in enumerate(line):
        if i == pos and not in_string:
            return False
        if i == pos and in_string:
            return True
        if ch in ("'", '"') and not in_string:
            in_string = True
            quote_char = ch
        elif ch == quote_char and in_string:
            in_string = False
    return False


def check_pg001(content: str, rel_path: str) -> list[str]:
    """PG001: Таблицы должны быть snake_case."""
    errors = []
    for i, line in enumerate(content.split("\n"), 1):
        if is_comment_or_empty(line):
            continue
        match = re.search(
            r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\S+)",
            line, re.IGNORECASE,
        )
        if match:
            table_name = match.group(1).strip('"').strip("`").split(".")[-1]
            if not SNAKE_CASE.match(table_name):
                errors.append(
                    f"[PG001] {rel_path}:{i}: таблица '{table_name}' не в snake_case"
                )
    return errors


def check_pg002(content: str, rel_path: str) -> list[str]:
    """PG002: Колонки должны быть snake_case."""
    errors = []
    in_create_table = False
    paren_depth = 0

    for i, line in enumerate(content.split("\n"), 1):
        if is_comment_or_empty(line):
            continue
        upper_line = line.upper().strip()

        if re.search(r"CREATE\s+TABLE", line, re.IGNORECASE):
            in_create_table = True
            paren_depth = 0

        if in_create_table:
            paren_depth += line.count("(") - line.count(")")

            # Определение колонки: начинается с имени, затем тип
            col_match = re.match(
                r"^\s+(\w+)\s+"
                r"(BIGSERIAL|BIGINT|INTEGER|INT|SERIAL|SMALLINT|BOOLEAN|BOOL"
                r"|TEXT|VARCHAR|CHAR|UUID|TIMESTAMPTZ|TIMESTAMP|DATE|TIME"
                r"|NUMERIC|DECIMAL|FLOAT|DOUBLE|REAL|JSONB|JSON|BYTEA"
                r"|INET|CIDR|MACADDR)",
                line, re.IGNORECASE,
            )
            if col_match:
                col_name = col_match.group(1)
                # Пропускать ключевые слова SQL
                if col_name.upper() in ("PRIMARY", "FOREIGN", "CONSTRAINT",
                                         "UNIQUE", "CHECK", "CREATE", "INDEX"):
                    continue
                if not SNAKE_CASE.match(col_name):
                    errors.append(
                        f"[PG002] {rel_path}:{i}: колонка '{col_name}' не в snake_case"
                    )

            if paren_depth <= 0 and ")" in line:
                in_create_table = False

    return errors


def check_pg003(content: str, rel_path: str) -> list[str]:
    """PG003: FK без индекса."""
    errors = []
    # Собрать все FK-колонки
    fk_columns = []
    for i, line in enumerate(content.split("\n"), 1):
        if is_comment_or_empty(line):
            continue
        match = re.search(
            r"FOREIGN\s+KEY\s*\(([^)]+)\)",
            line, re.IGNORECASE,
        )
        if match:
            cols = [c.strip().strip('"') for c in match.group(1).split(",")]
            for col in cols:
                fk_columns.append((col, i))

    # Собрать все индексированные колонки
    indexed_columns = set()
    for line in content.split("\n"):
        if is_comment_or_empty(line):
            continue
        idx_match = re.search(
            r"CREATE\s+(?:UNIQUE\s+)?INDEX\s+\S+\s+ON\s+\S+\s*\(([^)]+)\)",
            line, re.IGNORECASE,
        )
        if idx_match:
            cols = [c.strip().strip('"').split()[0] for c in idx_match.group(1).split(",")]
            indexed_columns.update(cols)

    for col, line_num in fk_columns:
        if col not in indexed_columns:
            errors.append(
                f"[PG003] {rel_path}:{line_num}: FK на '{col}' без индекса"
            )

    return errors


def check_pg004(content: str, rel_path: str) -> list[str]:
    """PG004: TIMESTAMP вместо TIMESTAMPTZ."""
    errors = []
    for i, line in enumerate(content.split("\n"), 1):
        if is_comment_or_empty(line):
            continue
        # Найти TIMESTAMP, но не TIMESTAMPTZ
        matches = list(re.finditer(r"\bTIMESTAMP\b", line, re.IGNORECASE))
        for m in matches:
            end_pos = m.end()
            # Проверить, что за TIMESTAMP не идёт TZ
            rest = line[end_pos:]
            if not rest.upper().startswith("TZ"):
                # Исключить TIMESTAMP WITH TIME ZONE
                if not re.match(r"\s+WITH\s+TIME\s+ZONE", rest, re.IGNORECASE):
                    errors.append(
                        f"[PG004] {rel_path}:{i}: TIMESTAMP без timezone "
                        f"(используй TIMESTAMPTZ)"
                    )
    return errors


def check_pg005(content: str, rel_path: str) -> list[str]:
    """PG005: SELECT * в запросе."""
    errors = []
    for i, line in enumerate(content.split("\n"), 1):
        if is_comment_or_empty(line):
            continue
        if re.search(r"\bSELECT\s+\*\s+FROM\b", line, re.IGNORECASE):
            errors.append(
                f"[PG005] {rel_path}:{i}: SELECT * (перечисли нужные колонки)"
            )
    return errors


def check_pg007(file_path: Path, rel_path: str) -> list[str]:
    """PG007: Формат имени файла миграции."""
    errors = []
    # Только файлы в папке migrations/
    if "migrations" in file_path.parts or "migration" in file_path.parts:
        if not MIGRATION_NAME.match(file_path.name):
            errors.append(
                f"[PG007] {rel_path}: имя миграции '{file_path.name}' "
                f"не соответствует формату NNN_description.sql"
            )
    return errors


def check_pg009(content: str, rel_path: str) -> list[str]:
    """PG009: SQL keywords должны быть UPPER CASE."""
    errors = []
    # Строим set из lowercase keywords для быстрой проверки
    kw_lower = {kw.lower() for kw in SQL_KEYWORDS} - KEYWORD_EXCEPTIONS

    for i, line in enumerate(content.split("\n"), 1):
        if is_comment_or_empty(line):
            continue

        # Разбиваем строку на слова
        words = re.findall(r"\b([a-zA-Z_]+)\b", line)
        for word in words:
            lower_word = word.lower()
            if lower_word in kw_lower and word != word.upper():
                # Дополнительная проверка: не часть идентификатора
                # (слово после точки = имя колонки/таблицы, пропускаем)
                if is_in_string(line, line.find(word)):
                    continue
                errors.append(
                    f"[PG009] {rel_path}:{i}: '{word}' → '{word.upper()}'"
                )
                break  # Одна ошибка на строку достаточно

    return errors


def validate_file(file_path: Path, repo_root: Path, verbose: bool = False) -> list[str]:
    """Валидация одного SQL-файла."""
    errors = []
    try:
        rel = str(file_path.relative_to(repo_root))
    except ValueError:
        rel = str(file_path)
    content = file_path.read_text(encoding="utf-8")

    if verbose:
        print(f"\n📄 {rel}")

    # PG007: формат имени миграции
    file_errors = check_pg007(file_path, rel)
    errors.extend(file_errors)
    if verbose and not file_errors:
        if "migrations" in file_path.parts or "migration" in file_path.parts:
            print(f"    PG007: формат имени ✓")

    # PG001: таблицы snake_case
    pg001 = check_pg001(content, rel)
    errors.extend(pg001)
    if verbose and not pg001:
        print(f"    PG001: таблицы ✓")

    # PG002: колонки snake_case
    pg002 = check_pg002(content, rel)
    errors.extend(pg002)
    if verbose and not pg002:
        print(f"    PG002: колонки ✓")

    # PG003: FK без индекса
    pg003 = check_pg003(content, rel)
    errors.extend(pg003)
    if verbose and not pg003:
        print(f"    PG003: FK индексы ✓")

    # PG004: TIMESTAMP → TIMESTAMPTZ
    pg004 = check_pg004(content, rel)
    errors.extend(pg004)
    if verbose and not pg004:
        print(f"    PG004: TIMESTAMPTZ ✓")

    # PG005: SELECT *
    pg005 = check_pg005(content, rel)
    errors.extend(pg005)
    if verbose and not pg005:
        print(f"    PG005: SELECT * ✓")

    # PG009: keywords UPPER CASE
    pg009 = check_pg009(content, rel)
    errors.extend(pg009)
    if verbose and not pg009:
        print(f"    PG009: keywords UPPER CASE ✓")

    return errors


def main():
    """Точка входа: парсинг аргументов и запуск валидации."""
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация SQL-кода на соответствие standard-postgresql.md"
    )
    parser.add_argument("path", nargs="*", help="Файлы .sql или папки")
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    parser.add_argument("--repo", default=".", help="Корень репозитория")

    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    if not (repo_root / ".git").exists():
        # Попробовать подняться
        current = repo_root
        while current != current.parent:
            if (current / ".git").exists():
                repo_root = current
                break
            current = current.parent

    # Собрать файлы
    files = []
    for p in args.path:
        target = Path(p)
        if not target.is_absolute():
            target = repo_root / target

        if target.is_dir():
            files.extend(sorted(target.rglob("*.sql")))
        elif target.is_file() and target.suffix == ".sql":
            files.append(target)

    if not files:
        if args.path:
            print("⚠ Нет .sql файлов для валидации")
        sys.exit(0)

    print(f"🔍 Валидация PostgreSQL-кода ({len(files)} файлов)...")

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
        print("✅ PostgreSQL-код соответствует стандарту")
        sys.exit(0)


if __name__ == "__main__":
    main()
