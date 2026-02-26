#!/usr/bin/env python3
"""
validate-commit-msg.py — Валидация формата commit message по Conventional Commits.

Использование:
    python validate-commit-msg.py <commit-msg-file>
    python validate-commit-msg.py .git/COMMIT_EDITMSG

Примеры:
    python validate-commit-msg.py .git/COMMIT_EDITMSG
    echo "feat(auth): добавить логин" | python validate-commit-msg.py -

Возвращает:
    0 — сообщение валидно
    1 — найдены ошибки
"""

import argparse
import re
import sys
from pathlib import Path

# =============================================================================
# Константы
# =============================================================================

VALID_TYPES = {"feat", "fix", "docs", "refactor", "test", "chore", "ci", "perf"}

VALID_FOOTER_KEYWORDS = {
    "Closes", "Fixes", "Refs", "BREAKING CHANGE", "Reviewed-by",
    "Co-Authored-By",
}

SUBJECT_MAX_LENGTH = 70

# Паттерн subject: type(scope): description или type: description
SUBJECT_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)"
    r"(?:\((?P<scope>[a-z0-9_-]+)\))?"
    r"(?P<bang>!)?"
    r":\s?"
    r"(?P<description>.*)$"
)

ERROR_CODES = {
    "CM001": "Subject не соответствует формату type(scope): description",
    "CM002": "Недопустимый тип коммита",
    "CM003": "Subject превышает 70 символов",
    "CM004": "Description начинается с заглавной буквы",
    "CM005": "Description заканчивается точкой",
    "CM006": "Отсутствует пробел после двоеточия",
    "CM007": "Запрещена ! нотация — используйте footer BREAKING CHANGE",
    "CM008": "Недопустимое ключевое слово в footer",
    "CM009": "Пустое сообщение коммита",
    "CM010": "Body должно отделяться от subject пустой строкой",
}


# =============================================================================
# Функции валидации
# =============================================================================


def add_error(result: dict, code: str, detail: str = "") -> None:
    """Добавить ошибку с кодом из ERROR_CODES."""
    message = ERROR_CODES.get(code, code)
    if detail:
        message = f"{code}: {message}: {detail}"
    else:
        message = f"{code}: {message}"
    result["errors"].append(message)


def parse_commit_message(text: str) -> dict:
    """Разобрать commit message на subject, body, footer."""
    lines = text.strip().split("\n")
    if not lines:
        return {"subject": "", "body": "", "footer_lines": []}

    subject = lines[0]
    body_lines = []
    footer_lines = []

    # Пропускаем строки, начинающиеся с # (комментарии git)
    remaining = [line for line in lines[1:] if not line.startswith("#")]

    # Находим разделитель subject/body (первая пустая строка)
    in_body = False
    in_footer = False

    for i, line in enumerate(remaining):
        if not in_body and line.strip() == "":
            in_body = True
            continue
        if in_body:
            # Footer начинается с известного keyword или после пустой строки в body
            if not in_footer and _is_footer_line(line):
                in_footer = True
            if in_footer:
                footer_lines.append(line)
            else:
                body_lines.append(line)

    return {
        "subject": subject,
        "body": "\n".join(body_lines).strip(),
        "footer_lines": footer_lines,
    }


def _is_footer_line(line: str) -> bool:
    """Проверить, является ли строка footer."""
    for keyword in VALID_FOOTER_KEYWORDS:
        if line.startswith(f"{keyword}:") or line.startswith(f"{keyword} #"):
            return True
    return False


def validate_subject(subject: str, result: dict) -> None:
    """Валидация subject строки."""
    if not subject.strip():
        add_error(result, "CM009")
        return

    match = SUBJECT_PATTERN.match(subject)

    if not match:
        add_error(result, "CM001", f"'{subject}'")
        return

    commit_type = match.group("type")
    bang = match.group("bang")
    description = match.group("description")

    # CM002: допустимый тип
    if commit_type not in VALID_TYPES:
        add_error(result, "CM002", f"'{commit_type}' не в {sorted(VALID_TYPES)}")

    # CM003: длина subject
    if len(subject) > SUBJECT_MAX_LENGTH:
        add_error(result, "CM003", f"{len(subject)} > {SUBJECT_MAX_LENGTH}")

    # CM006: пробел после двоеточия
    colon_pos = subject.find(":")
    if colon_pos >= 0 and colon_pos + 1 < len(subject):
        if subject[colon_pos + 1] != " ":
            add_error(result, "CM006")

    # CM007: запрет ! нотации
    if bang:
        add_error(result, "CM007")

    # CM004: нижний регистр description
    if description and description[0].isupper():
        add_error(result, "CM004", f"'{description}'")

    # CM005: точка в конце
    if description and description.rstrip().endswith("."):
        add_error(result, "CM005")


def validate_body_separator(text: str, result: dict) -> None:
    """Проверить пустую строку между subject и body."""
    lines = [line for line in text.strip().split("\n") if not line.startswith("#")]
    if len(lines) > 1 and lines[1].strip() != "":
        add_error(result, "CM010")


def validate_footer(footer_lines: list, result: dict) -> None:
    """Валидация footer строк."""
    for line in footer_lines:
        if not line.strip():
            continue
        is_valid = False
        for keyword in VALID_FOOTER_KEYWORDS:
            if line.startswith(f"{keyword}:") or line.startswith(f"{keyword} #"):
                is_valid = True
                break
        if not is_valid:
            add_error(result, "CM008", f"'{line}'")


def validate_commit_message(text: str) -> dict:
    """Валидировать commit message."""
    result = {"errors": [], "warnings": []}

    parsed = parse_commit_message(text)

    validate_subject(parsed["subject"], result)
    validate_body_separator(text, result)
    validate_footer(parsed["footer_lines"], result)

    return result


# =============================================================================
# Main
# =============================================================================


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Валидация формата commit message по Conventional Commits"
    )
    parser.add_argument(
        "commit_msg_file",
        help="Путь к файлу с commit message (обычно .git/COMMIT_EDITMSG)",
    )

    args = parser.parse_args()

    msg_path = Path(args.commit_msg_file)
    if not msg_path.exists():
        print(f"❌ Файл не найден: {msg_path}", file=sys.stderr)
        sys.exit(1)

    text = msg_path.read_text(encoding="utf-8")

    result = validate_commit_message(text)

    if result["errors"]:
        print(f"❌ Commit message — {len(result['errors'])} ошибок:")
        for error in result["errors"]:
            print(f"   {error}")
        sys.exit(1)

    print("✅ Commit message валиден")
    sys.exit(0)


if __name__ == "__main__":
    main()
