#!/usr/bin/env python3
"""
chain_status.py — SSOT модуль управления статусами analysis chain.

Консолидирует: parse_frontmatter, find_repo_root, CHAIN_DOCS,
VALID_STATUSES, TRANSITION_MATRIX, README sync, prerequisites,
cross-chain awareness.

Заменяет дублированный код в: analysis-status.py, check-chain-readiness.py,
dev-next-issue.py, create-review-file.py.

Использование:
    from chain_status import ChainManager

    mgr = ChainManager("0001")
    mgr.status()                                    # → dict {doc: status}
    mgr.check_prerequisites(to="WAITING", doc="design")  # → list[PrerequisiteError]
    mgr.transition(to="WAITING", document="design") # → TransitionResult
    mgr.check_cross_chain()                         # → list[CrossChainAlert]
    mgr.classify_feedback(level="conflict")         # → dict

Спецификация:
    .claude/drafts/2026-02-24-status-manager.md §3
"""
from __future__ import annotations

import functools
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# Windows cp1251 → UTF-8 для корректного вывода Unicode (→, ✅, ❌)
if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8")


# =============================================================================
# Типы
# =============================================================================

DocType = Literal["discussion", "design", "plan-test", "plan-dev"]
Status = Literal[
    "DRAFT", "WAITING", "RUNNING", "REVIEW",
    "DONE", "CONFLICT", "ROLLING_BACK", "REJECTED",
]
FeedbackLevel = Literal["free", "flag", "conflict"]


# =============================================================================
# Константы
# =============================================================================

CHAIN_DOCS: list[str] = ["discussion", "design", "plan-test", "plan-dev"]
"""4 основных документа цепочки в иерархическом порядке (parent → child)."""

DOC_ORDER: dict[str, int] = {d: i for i, d in enumerate(CHAIN_DOCS)}
"""Порядковый номер документа в иерархии: discussion=0, plan-dev=3."""

VALID_STATUSES: set[str] = {
    "DRAFT", "WAITING", "RUNNING", "REVIEW",
    "DONE", "CONFLICT", "ROLLING_BACK", "REJECTED",
}
"""8 допустимых статусов analysis chain (standard-analysis.md §5)."""

# Матрица допустимых переходов: (from, to) → transition ID
TRANSITION_MATRIX: dict[tuple[str, str], str] = {
    ("DRAFT", "WAITING"):         "T1",   # per-document
    ("WAITING", "DRAFT"):         "T2",   # per-document (каскад дочерних)
    ("WAITING", "RUNNING"):       "T3",   # tree-level
    ("RUNNING", "CONFLICT"):      "T4",   # tree-level
    ("CONFLICT", "WAITING"):      "T5",   # per-document (top-down)
    ("RUNNING", "REVIEW"):        "T6",   # tree-level
    ("REVIEW", "DONE"):           "T7",   # per-document (bottom-up каскад)
    ("REVIEW", "CONFLICT"):       "T8",   # tree-level
    # T9: любой¹ → ROLLING_BACK (tree-level), ¹ = кроме DONE и REJECTED
    ("DRAFT", "ROLLING_BACK"):    "T9",
    ("WAITING", "ROLLING_BACK"):  "T9",
    ("RUNNING", "ROLLING_BACK"):  "T9",
    ("REVIEW", "ROLLING_BACK"):   "T9",
    ("CONFLICT", "ROLLING_BACK"): "T9",
    ("ROLLING_BACK", "REJECTED"): "T10",  # tree-level
}

TREE_LEVEL_TRANSITIONS: set[str] = {"T3", "T4", "T6", "T8", "T9", "T10"}
"""Переходы, затрагивающие ВСЕ документы цепочки."""

PER_DOC_TRANSITIONS: set[str] = {"T1", "T2", "T5", "T7"}
"""Переходы для одного документа (или bottom-up каскад для T7)."""

DONE_CASCADE_ORDER: list[str] = ["plan-dev", "plan-test", "design", "discussion"]
"""Bottom-up порядок для T7 (REVIEW → DONE)."""

# Иерархия документов: parent → children
DOC_CHILDREN: dict[str, list[str]] = {
    "discussion": ["design", "plan-test", "plan-dev"],
    "design": ["plan-test", "plan-dev"],
    "plan-test": ["plan-dev"],
    "plan-dev": [],
}

# Side effects по переходам (§1.3)
SIDE_EFFECTS: dict[tuple[str, str], list[str]] = {
    # Design → WAITING (артефакты specs/docs/ перенесены на /docs-sync)
    ("design", "WAITING"): [
        "Создать метки svc:{svc} для новых сервисов → /labels-modify",
    ],
    # Plan Dev → WAITING
    ("plan-dev", "WAITING"): [
        "Создать review.md → /review-create",
    ],
    # → RUNNING (tree-level, через create-development)
    ("*", "RUNNING"): [
        "Создать Issues для TASK-N → /issue-create",
        "Создать/привязать Milestone → /milestone-create",
        "Создать Branch → /branch-create",
    ],
    # Design → DONE (через T7 bottom-up каскад)
    ("design", "DONE"): [
        "Planned Changes → AS IS: specs/docs/{svc}.md §§1-8 (дельты → основной контент)",
        "Обновить specs/docs/{svc}.md §10 → Changelog",
        "Обновить specs/docs/.system/overview.md → AS IS + Changelog",
        "Кросс-цепочечная проверка: все другие цепочки с Planned Changes",
    ],
    # Plan Tests → DONE
    ("plan-test", "DONE"): [
        "Обновить specs/docs/.system/testing.md (если стратегия изменилась)",
    ],
    # Design CONFLICT → WAITING
    ("design", "WAITING_FROM_CONFLICT"): [
        "Пересчитать Planned Changes в specs/docs/",
    ],
    # Plan Dev CONFLICT → WAITING
    ("plan-dev", "WAITING_FROM_CONFLICT"): [
        "Синхронизировать Issues: changed→/issue-modify, deleted→close, new→/issue-create",
    ],
    # → ROLLING_BACK (tree-level)
    ("*", "ROLLING_BACK"): [
        "Откатить артефакты Design: удалить Planned Changes по chain-маркеру",
        "Откатить артефакты Design: удалить заглушки {svc}.md (если уникальны)",
        "Откатить артефакты Plan Dev: закрыть Issues --reason 'not planned'",
        "Откатить артефакты Plan Dev: удалить feature-ветку",
    ],
}

# Auto-propose после DRAFT → WAITING (§1.5)
# plan-dev — двухступенчатый: сначала /docs-sync, потом /dev-create
AUTO_PROPOSE: dict[str, str] = {
    "discussion": "/design-create {chain_id}",
    "design": "/plan-test-create {chain_id}",
    "plan-test": "/plan-dev-create {chain_id}",
    "plan-dev": "/docs-sync {chain_id}",  # после docs-sync → /dev-create
}

# Auto-propose после /docs-sync (docs-synced: true)
AUTO_PROPOSE_AFTER_DOCS_SYNC: str = "/dev-create {chain_id}"

# Regex patterns
MARKER_PATTERN = re.compile(r'\[ТРЕБУЕТ УТОЧНЕНИЯ')
BARRIER_PATTERN = re.compile(r'⛔\s*DEPENDENCY BARRIER')
FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
STATUS_LINE_PATTERN = re.compile(r'^(status:\s+)\S+', re.MULTILINE)
CHAIN_FOLDER_PATTERN = re.compile(r'^\d{4}-.+$')


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class FileChange:
    """Одно изменение файла."""
    file: str          # относительный путь от repo root
    field: str         # "status"
    old: str
    new: str


@dataclass
class CrossChainAlert:
    """Сигнал о затронутой параллельной цепочке."""
    chain: str         # "0002-payment-service"
    status: str        # текущий статус затронутой цепочки
    severity: str      # "info" | "warning" | "critical"
    message: str       # что рекомендовано сделать


@dataclass
class TransitionResult:
    """Результат перехода — возвращается из transition()."""
    chain: str                                # "0001-oauth2-authorization"
    transition_id: str                        # "T1"
    scope: str                                # "per-document" | "tree-level"
    from_statuses: dict[str, str]             # {"design": "DRAFT"} или все 4 документа
    to_status: str                            # "WAITING"
    document: str | None                      # "design" или None (tree-level)
    changes: list[FileChange] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    auto_propose: str | None = None           # "/plan-test-create 0001"
    cross_chain_alerts: list[CrossChainAlert] = field(default_factory=list)


@dataclass
class PrerequisiteError:
    """Одна ошибка prerequisites."""
    code: str          # "PRE001"
    message: str       # "Документ не в статусе DRAFT"


# =============================================================================
# Exceptions
# =============================================================================

class ChainError(Exception):
    """Базовый класс ошибок модуля."""


class ChainNotFoundError(ChainError):
    """Цепочка NNNN не найдена в specs/analysis/."""


class InvalidTransitionError(ChainError):
    """Переход недопустим по TRANSITION_MATRIX."""

    def __init__(
        self,
        from_status: str,
        to_status: str,
        document: str | None = None,
    ):
        self.from_status = from_status
        self.to_status = to_status
        self.document = document
        msg = f"Invalid transition: {from_status} → {to_status}"
        if document:
            msg += f" (document={document})"
        super().__init__(msg)


class DoneIsFinalError(InvalidTransitionError):
    """Попытка перехода из DONE — финальный статус."""

    def __init__(self, document: str | None = None):
        super().__init__("DONE", "any", document)


class PrerequisitesNotMetError(ChainError):
    """Prerequisites не выполнены — переход заблокирован."""

    def __init__(self, errors: list[PrerequisiteError]):
        self.errors = errors
        messages = "; ".join(f"[{e.code}] {e.message}" for e in errors)
        super().__init__(f"Prerequisites not met: {messages}")


# =============================================================================
# Класс ChainManager
# =============================================================================

class ChainManager:
    """
    Управление статусами одной analysis chain.

    Параметры:
        chain_id: номер или полное имя цепочки ("0001" или "0001-oauth2-authorization")
        repo_root: корень репозитория (автоопределение если None)

    Raises:
        ChainNotFoundError: если папка цепочки не существует или >1 совпадение
    """

    def __init__(self, chain_id: str, repo_root: Path | None = None) -> None:
        self._repo_root = repo_root or self.find_repo_root()
        self._analysis_dir = self._repo_root / "specs" / "analysis"
        self._chain_dir = self._resolve_chain_dir(chain_id)
        self._chain_name = self._chain_dir.name
        self._chain_id = self._chain_name[:4]

    def _resolve_chain_dir(self, chain_id: str) -> Path:
        """Найти папку цепочки по ID или полному имени."""
        # Полное имя — прямой путь
        direct = self._analysis_dir / chain_id
        if direct.is_dir():
            return direct

        # Short id (4 цифры) — поиск по префиксу
        candidates = [
            d for d in self._analysis_dir.iterdir()
            if d.is_dir() and d.name.startswith(chain_id)
            and CHAIN_FOLDER_PATTERN.match(d.name)
        ]
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) == 0:
            raise ChainNotFoundError(
                f"Chain '{chain_id}' not found in {self._analysis_dir}"
            )
        names = ", ".join(c.name for c in candidates)
        raise ChainNotFoundError(
            f"Multiple matches for '{chain_id}': {names}"
        )

    # ─── Свойства ─────────────────────────────────────────────────

    def chain_dir(self) -> Path:
        """Абсолютный путь к папке цепочки."""
        return self._chain_dir

    def chain_name(self) -> str:
        """Полное имя цепочки: '0001-oauth2-authorization'."""
        return self._chain_name

    def chain_id(self) -> str:
        """Short ID: '0001'."""
        return self._chain_id

    # ─── Чтение ────────────────────────────────────────────────────

    def _doc_path(self, doc: str) -> Path:
        """Путь к файлу документа: discussion.md, design.md, etc."""
        return self._chain_dir / f"{doc}.md"

    def status(self) -> dict[str, str]:
        """
        Текущий статус всех документов цепочки (включая review.md).

        Returns:
            {"discussion": "WAITING", "design": "DRAFT", "plan-test": "DRAFT",
             "plan-dev": "DRAFT", "review": "OPEN"}
            Если документ не существует — статус "—".

        Raises:
            ChainNotFoundError: если папка цепочки не существует
        """
        result: dict[str, str] = {}
        for doc in CHAIN_DOCS:
            fm = self.parse_frontmatter(doc)
            result[doc] = fm.get("status", "—")
        # review.md — отдельная 2-статусная модель (OPEN/RESOLVED)
        fm_review = self.parse_frontmatter("review")
        result["review"] = fm_review.get("status", "—")
        return result

    def parse_frontmatter(self, doc: str) -> dict[str, str]:
        """
        Frontmatter одного документа как dict.

        Параметры:
            doc: "discussion" | "design" | "plan-test" | "plan-dev" | "review"

        Returns:
            dict с полями frontmatter. Пустой dict если файл не существует.
        """
        return self.parse_frontmatter_file(self._doc_path(doc))

    # ─── Prerequisites ──────────────────────────────────────────────

    def check_prerequisites(
        self,
        to: str,
        document: str | None = None,
        skip: bool = False,
    ) -> list[PrerequisiteError]:
        """
        Проверить prerequisites для перехода.

        Только файловые проверки (§3.8): status, маркеры, barriers, чекбоксы.
        НЕ вызывает validate-*.py и gh CLI.

        Returns:
            [] — prerequisites выполнены
            [PrerequisiteError, ...] — список ошибок
        """
        if skip:
            return []

        errors: list[PrerequisiteError] = []
        statuses = self.status()

        if document:
            current = statuses.get(document, "—")
        else:
            # tree-level — берём "общий" статус (все должны быть одинаковы)
            doc_statuses = {d: statuses[d] for d in CHAIN_DOCS}
            current = next(iter(doc_statuses.values()), "—")

        tid = TRANSITION_MATRIX.get((current, to))

        # T1: DRAFT → WAITING (per-document)
        if tid == "T1" and document:
            errors.extend(self._check_t1(document))

        # T3: WAITING → RUNNING (tree-level)
        elif tid == "T3":
            errors.extend(self._check_t3(statuses))

        # T6: RUNNING → REVIEW (tree-level)
        elif tid == "T6":
            errors.extend(self._check_t6())

        # T7: REVIEW → DONE (bottom-up)
        elif tid == "T7":
            errors.extend(self._check_t7())

        # T10: ROLLING_BACK → REJECTED (tree-level)
        elif tid == "T10":
            errors.extend(self._check_t10(statuses))

        return errors

    def _check_t1(self, document: str) -> list[PrerequisiteError]:
        """T1 prerequisites: DRAFT, 0 маркеров, 0 barriers, cross-chain docs-sync."""
        errors: list[PrerequisiteError] = []
        doc_path = self._doc_path(document)
        fm = self.parse_frontmatter(document)

        if fm.get("status") != "DRAFT":
            errors.append(PrerequisiteError(
                "PRE001", f"{document}.md не в статусе DRAFT (текущий: {fm.get('status', '—')})"
            ))

        markers = self.count_markers(doc_path)
        if markers > 0:
            errors.append(PrerequisiteError(
                "PRE002", f"{document}.md содержит {markers} маркеров [ТРЕБУЕТ УТОЧНЕНИЯ]"
            ))

        barriers = self.count_barriers(doc_path)
        if barriers > 0:
            errors.append(PrerequisiteError(
                "PRE003", f"{document}.md содержит {barriers} ⛔ DEPENDENCY BARRIER"
            ))

        # Cross-chain guard: при Design → WAITING проверяем pending /docs-sync
        if document == "design":
            pending = self.check_pending_docs_sync()
            if pending:
                errors.append(PrerequisiteError(
                    "PRE011",
                    f"Завершите /docs-sync для цепочки {pending}. "
                    f"Design+ WAITING без docs-synced блокирует новые Design → WAITING"
                ))

        return errors

    def _check_t3(self, statuses: dict[str, str]) -> list[PrerequisiteError]:
        """T3 prerequisites: все 4 документа WAITING, 0 маркеров."""
        errors: list[PrerequisiteError] = []

        for doc in CHAIN_DOCS:
            if statuses.get(doc) != "WAITING":
                errors.append(PrerequisiteError(
                    "PRE004", f"{doc}.md не в статусе WAITING (текущий: {statuses.get(doc, '—')})"
                ))
            markers = self.count_markers(self._doc_path(doc))
            if markers > 0:
                errors.append(PrerequisiteError(
                    "PRE005", f"{doc}.md содержит {markers} маркеров [ТРЕБУЕТ УТОЧНЕНИЯ]"
                ))

        return errors

    def _check_t6(self) -> list[PrerequisiteError]:
        """T6 prerequisites: все чекбоксы [x] в plan-dev.md."""
        errors: list[PrerequisiteError] = []
        pd_path = self._doc_path("plan-dev")

        if not pd_path.exists():
            errors.append(PrerequisiteError("PRE006", "plan-dev.md не существует"))
            return errors

        text = pd_path.read_text(encoding="utf-8")
        unchecked = len(re.findall(r'^\s*- \[ \]', text, re.MULTILINE))
        if unchecked > 0:
            errors.append(PrerequisiteError(
                "PRE007", f"plan-dev.md содержит {unchecked} невыполненных подзадач ([ ])"
            ))

        return errors

    def _check_t7(self) -> list[PrerequisiteError]:
        """T7 prerequisites: review.md status==RESOLVED."""
        errors: list[PrerequisiteError] = []
        review_path = self._doc_path("review")

        if not review_path.exists():
            errors.append(PrerequisiteError("PRE008", "review.md не существует"))
            return errors

        fm = self.parse_frontmatter("review")
        if fm.get("status") != "RESOLVED":
            errors.append(PrerequisiteError(
                "PRE009", f"review.md не в статусе RESOLVED (текущий: {fm.get('status', '—')})"
            ))

        return errors

    def _check_t10(self, statuses: dict[str, str]) -> list[PrerequisiteError]:
        """T10 prerequisites: все документы в ROLLING_BACK."""
        errors: list[PrerequisiteError] = []

        for doc in CHAIN_DOCS:
            if statuses.get(doc) != "ROLLING_BACK":
                errors.append(PrerequisiteError(
                    "PRE010", f"{doc}.md не в статусе ROLLING_BACK (текущий: {statuses.get(doc, '—')})"
                ))

        return errors

    # ─── Переходы ────────────────────────────────────────────────────

    def _update_status(self, doc_path: Path, new_status: str) -> FileChange:
        """Regex-замена status в frontmatter. Не трогает другие поля."""
        text = doc_path.read_text(encoding="utf-8")
        old_match = STATUS_LINE_PATTERN.search(text)
        old_status = old_match.group(0).split()[-1] if old_match else "UNKNOWN"
        new_text = STATUS_LINE_PATTERN.sub(
            rf'\g<1>{new_status}', text, count=1,
        )
        doc_path.write_text(new_text, encoding="utf-8")
        rel = str(doc_path.relative_to(self._repo_root))
        return FileChange(file=rel, field="status", old=old_status, new=new_status)

    def _update_readme_dashboard(self) -> None:
        """Полная перегенерация таблицы 2 (dashboard) между BEGIN/END маркерами."""
        readme_path = self._repo_root / "specs" / "analysis" / "README.md"
        if not readme_path.exists():
            return

        text = readme_path.read_text(encoding="utf-8")
        begin = "<!-- BEGIN:analysis-status -->"
        end = "<!-- END:analysis-status -->"
        if begin not in text or end not in text:
            return

        status_short = {
            "DRAFT": "D", "WAITING": "W", "RUNNING": "R", "REVIEW": "RV",
            "DONE": "DN", "CONFLICT": "C", "ROLLING_BACK": "RB",
            "REJECTED": "RJ", "OPEN": "OP", "RESOLVED": "RS",
        }

        chain_names = self.find_all_chains(self._repo_root)
        lines = []
        lines.append("| NNNN | Тема | Disc | Design | P.Test | P.Dev | Review | Branch | Milestone |")
        lines.append("|------|------|------|--------|--------|-------|--------|--------|-----------|")

        for name in chain_names:
            chain_dir = self._analysis_dir / name
            nnnn = name[:4]
            topic = name[5:] if len(name) > 5 else name
            statuses: dict[str, str] = {}
            for doc in CHAIN_DOCS + ["review"]:
                fm = self.parse_frontmatter_file(chain_dir / f"{doc}.md")
                statuses[doc] = fm.get("status", "—")
            disc_fm = self.parse_frontmatter_file(chain_dir / "discussion.md")
            milestone = disc_fm.get("milestone", "—")

            d = status_short.get(statuses.get("discussion", "—"), "—")
            de = status_short.get(statuses.get("design", "—"), "—")
            pt = status_short.get(statuses.get("plan-test", "—"), "—")
            pd = status_short.get(statuses.get("plan-dev", "—"), "—")
            rev = status_short.get(statuses.get("review", "—"), "—")
            lines.append(f"| {nnnn} | {topic} | {d} | {de} | {pt} | {pd} | {rev} | {name} | {milestone} |")

        table = "\n".join(lines)
        new_block = f"{begin}\n{table}\n{end}"
        pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
        new_text = pattern.sub(new_block, text)
        readme_path.write_text(new_text, encoding="utf-8")

    def _collect_side_effects(
        self, tid: str, to: str, document: str | None,
        from_status: str | None = None,
    ) -> list[str]:
        """Собрать side_effects для перехода."""
        effects: list[str] = []

        if document and tid == "T5" and from_status == "CONFLICT":
            # CONFLICT → WAITING per-document
            key = (document, "WAITING_FROM_CONFLICT")
            effects.extend(SIDE_EFFECTS.get(key, []))
        elif document:
            key = (document, to)
            effects.extend(SIDE_EFFECTS.get(key, []))

        # tree-level side effects
        wildcard_key = ("*", to)
        if wildcard_key in SIDE_EFFECTS and tid in TREE_LEVEL_TRANSITIONS:
            effects.extend(SIDE_EFFECTS[wildcard_key])

        # T7 bottom-up: собрать side effects для каждого уровня
        if tid == "T7":
            for doc in DONE_CASCADE_ORDER:
                key = (doc, "DONE")
                effects.extend(SIDE_EFFECTS.get(key, []))

        return effects

    def _collect_auto_propose(self, tid: str, document: str | None) -> str | None:
        """Определить auto_propose после T1 (DRAFT → WAITING).

        Для plan-dev — двухступенчатый:
        - docs-synced отсутствует/false → /docs-sync
        - docs-synced: true → /dev-create
        """
        if tid == "T1" and document and document in AUTO_PROPOSE:
            if document == "plan-dev":
                fm = self.parse_frontmatter("design")
                if fm.get("docs-synced") == "true":
                    return AUTO_PROPOSE_AFTER_DOCS_SYNC.format(chain_id=self._chain_id)
            return AUTO_PROPOSE[document].format(chain_id=self._chain_id)
        return None

    def transition(
        self,
        to: str,
        document: str | None = None,
        dry_run: bool = False,
        skip_prerequisites: bool = False,
    ) -> TransitionResult:
        """
        Выполнить переход статуса.

        Логика:
        1. Определить текущий статус
        2. Вычислить transition_id по TRANSITION_MATRIX
        3. Scope: per-doc / tree-level / bottom-up (T7)
        4. check_prerequisites (если не skip)
        5. Обновить frontmatter + README
        6. T2: автокаскад дочерних → DRAFT
        7. DONE-документы не затрагиваются tree-level (T4, T8, T9)
        8. Собрать side_effects, auto_propose
        9. Return TransitionResult
        """
        statuses = self.status()
        changes: list[FileChange] = []

        # --- Определить текущий статус и transition_id ---
        if document:
            current = statuses.get(document, "—")
        else:
            # tree-level: берём первый не-DONE статус для определения перехода
            current = None
            for doc in CHAIN_DOCS:
                s = statuses.get(doc, "—")
                if s != "DONE" and s != "REJECTED":
                    current = s
                    break
            if current is None:
                current = statuses.get(CHAIN_DOCS[0], "—")

        # Проверка DONE — финальный статус
        if document and statuses.get(document) == "DONE":
            raise DoneIsFinalError(document)

        tid = TRANSITION_MATRIX.get((current, to))
        if tid is None:
            raise InvalidTransitionError(current, to, document)

        # --- Scope ---
        if tid in PER_DOC_TRANSITIONS and tid != "T7":
            scope = "per-document"
        else:
            scope = "tree-level"

        from_statuses: dict[str, str] = {}

        # --- Prerequisites ---
        if not skip_prerequisites:
            errors = self.check_prerequisites(to=to, document=document)
            if errors:
                raise PrerequisitesNotMetError(errors)

        if dry_run:
            # Собрать from_statuses без записи
            if document:
                from_statuses[document] = current
            else:
                from_statuses = {d: statuses[d] for d in CHAIN_DOCS}
            return TransitionResult(
                chain=self._chain_name,
                transition_id=tid,
                scope=scope,
                from_statuses=from_statuses,
                to_status=to,
                document=document,
                changes=[],
                side_effects=self._collect_side_effects(tid, to, document, current),
                auto_propose=self._collect_auto_propose(tid, document),
            )

        # --- Выполнить переход ---

        if tid == "T7":
            # Bottom-up каскад: plan-dev → plan-test → design → discussion
            for doc in DONE_CASCADE_ORDER:
                doc_status = statuses.get(doc, "—")
                if doc_status == "DONE":
                    continue  # уже DONE
                from_statuses[doc] = doc_status
                change = self._update_status(self._doc_path(doc), "DONE")
                changes.append(change)

        elif document and tid in PER_DOC_TRANSITIONS:
            # Per-document переход
            from_statuses[document] = current
            change = self._update_status(self._doc_path(document), to)
            changes.append(change)

            # T2: автокаскад дочерних → DRAFT
            if tid == "T2" and document in DOC_CHILDREN:
                for child in DOC_CHILDREN[document]:
                    child_status = statuses.get(child, "—")
                    if child_status not in ("DRAFT", "—", "DONE", "REJECTED"):
                        from_statuses[child] = child_status
                        child_change = self._update_status(
                            self._doc_path(child), "DRAFT",
                        )
                        changes.append(child_change)

        else:
            # Tree-level переход (T3, T4, T6, T8, T9, T10)
            for doc in CHAIN_DOCS:
                doc_status = statuses.get(doc, "—")
                # DONE и REJECTED не затрагиваются tree-level (T4, T8, T9)
                if doc_status in ("DONE", "REJECTED"):
                    continue
                from_statuses[doc] = doc_status
                change = self._update_status(self._doc_path(doc), to)
                changes.append(change)

        # --- Обновить README dashboard ---
        self._update_readme_dashboard()

        # --- Собрать результат ---
        return TransitionResult(
            chain=self._chain_name,
            transition_id=tid,
            scope=scope,
            from_statuses=from_statuses,
            to_status=to,
            document=document,
            changes=changes,
            side_effects=self._collect_side_effects(tid, to, document, current),
            auto_propose=self._collect_auto_propose(tid, document),
        )

    # ─── Cross-chain ──────────────────────────────────────────────

    # Regex для маркера Planned Changes: <!-- chain: NNNN-{topic} -->
    _CHAIN_MARKER_PATTERN = re.compile(
        r'<!--\s*chain:\s*(\d{4}-[^\s]+)\s*-->'
    )

    def check_cross_chain(self) -> list[CrossChainAlert]:
        """
        Проверить влияние текущей цепочки на параллельные (Q5: сигнализация).

        Сканирует specs/docs/ для <!-- chain: NNNN-{topic} --> маркеров.
        Находит пересечения: какие другие цепочки затрагивают те же файлы.
        НЕ выполняет переходы автоматически — только возвращает alerts.

        Реакция по статусу другой цепочки (§1.6):
        - DRAFT: info — "Перегенерировать затронутые документы"
        - WAITING: warning — "Обновить контекст"
        - RUNNING: critical — "CASCADE CONFLICT"
        - DONE: info — "Предложить новую Discussion"
        - REJECTED: не обрабатывается
        """
        docs_dir = self._repo_root / "specs" / "docs"
        if not docs_dir.exists():
            return []

        # 1. Собрать маркеры: file → set of chain_names
        file_chains: dict[str, set[str]] = {}
        for md_file in docs_dir.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            markers = self._CHAIN_MARKER_PATTERN.findall(text)
            if markers:
                rel = str(md_file.relative_to(self._repo_root))
                file_chains[rel] = set(markers)

        # 2. Найти файлы текущей цепочки
        my_files: set[str] = set()
        for rel, chains in file_chains.items():
            if self._chain_name in chains:
                my_files.add(rel)

        if not my_files:
            return []

        # 3. Найти пересекающиеся цепочки
        overlapping: set[str] = set()
        for rel in my_files:
            for chain_name in file_chains.get(rel, set()):
                if chain_name != self._chain_name:
                    overlapping.add(chain_name)

        if not overlapping:
            return []

        # 4. Определить статус каждой пересекающейся цепочки и сгенерировать alerts
        alerts: list[CrossChainAlert] = []
        for other_chain in sorted(overlapping):
            other_id = other_chain[:4]
            try:
                other_mgr = ChainManager(other_id, repo_root=self._repo_root)
                other_statuses = other_mgr.status()
            except ChainNotFoundError:
                continue

            # Определить "главный" статус другой цепочки (первый не-DONE/REJECTED)
            main_status = "—"
            for doc in CHAIN_DOCS:
                s = other_statuses.get(doc, "—")
                if s not in ("DONE", "REJECTED", "—"):
                    main_status = s
                    break
            # Если все DONE — считаем DONE
            if main_status == "—":
                if all(other_statuses.get(d) == "DONE" for d in CHAIN_DOCS):
                    main_status = "DONE"
                elif all(other_statuses.get(d) == "REJECTED" for d in CHAIN_DOCS):
                    continue  # REJECTED — не обрабатывается

            # Матрица реакции (§1.6)
            severity_map: dict[str, tuple[str, str]] = {
                "DRAFT": ("info", "Перегенерировать затронутые документы другой цепочки"),
                "WAITING": ("warning", "Обновить контекст затронутых документов (Planned Changes изменились)"),
                "RUNNING": ("critical", "CASCADE CONFLICT — другая цепочка тоже → CONFLICT (tree-level)"),
                "REVIEW": ("critical", "CASCADE CONFLICT — другая цепочка в REVIEW → CONFLICT"),
                "CONFLICT": ("warning", "Цепочка уже в CONFLICT — проверить что учтены изменения"),
                "DONE": ("info", "Предложить новую Discussion со ссылкой на DONE-цепочку"),
            }

            if main_status in severity_map:
                sev, msg = severity_map[main_status]
                alerts.append(CrossChainAlert(
                    chain=other_chain,
                    status=main_status,
                    severity=sev,
                    message=msg,
                ))

        return alerts

    # ─── Docs-sync guard ─────────────────────────────────────────

    def check_pending_docs_sync(self) -> str | None:
        """
        Cross-chain guard (D-12): при Design → WAITING проверить,
        есть ли цепочка M < N с Design+ в WAITING без docs-synced: true.

        Discussion создаётся свободно (не читает specs/docs/).
        Блокировка только при Design → WAITING.

        Returns:
            None — блокировки нет
            str — имя цепочки M, для которой не завершён /docs-sync
        """
        my_id = int(self._chain_id)
        all_chains = self.find_all_chains(self._repo_root)

        for chain_name in all_chains:
            other_id = int(chain_name[:4])
            if other_id >= my_id:
                continue  # проверяем только M < N

            other_dir = self._analysis_dir / chain_name
            # Проверяем: design+ (Design или дочерние) в WAITING
            design_fm = self.parse_frontmatter_file(other_dir / "design.md")
            design_status = design_fm.get("status", "—")

            if design_status not in ("WAITING", "RUNNING", "REVIEW"):
                continue  # Design не в активном статусе

            # Проверяем docs-synced
            if design_fm.get("docs-synced") != "true":
                return chain_name  # блокируем — /docs-sync не завершён

        return None

    # ─── Feedback guard ───────────────────────────────────────────

    def classify_feedback(self, level: FeedbackLevel) -> dict:
        """
        Guard для обратной связи Code → Specs (Q8).

        Определяет, допустим ли данный уровень обратной связи
        для текущего статуса цепочки (§1.7).

        Параметры:
            level: "free" | "flag" | "conflict"

        Returns:
            {"allowed": bool, "current_status": str,
             "action": str, "reason": str}

        Правила:
        - "free": всегда allowed, action="no_action"
        - "flag": allowed для RUNNING, action="log_only"
        - "conflict": allowed для RUNNING/REVIEW, action="transition_to_conflict"
        """
        statuses = self.status()

        # Определить "главный" статус цепочки
        current = "—"
        for doc in CHAIN_DOCS:
            s = statuses.get(doc, "—")
            if s not in ("DONE", "REJECTED", "—"):
                current = s
                break

        if level == "free":
            return {
                "allowed": True,
                "current_status": current,
                "action": "no_action",
                "reason": "Свободный уровень — реализация внутри пакета, без обратной связи",
            }

        if level == "flag":
            allowed = current == "RUNNING"
            return {
                "allowed": allowed,
                "current_status": current,
                "action": "log_only" if allowed else "rejected",
                "reason": (
                    "Work edits: LLM авто-правит plan-dev/plan-test, продолжает"
                    if allowed
                    else f"flag недопустим для статуса {current} (только RUNNING)"
                ),
            }

        # level == "conflict"
        allowed = current in ("RUNNING", "REVIEW")
        return {
            "allowed": allowed,
            "current_status": current,
            "action": "transition_to_conflict" if allowed else "rejected",
            "reason": (
                f"Design+ уровень — вся цепочка → CONFLICT ({current} → CONFLICT)"
                if allowed
                else f"conflict недопустим для статуса {current} (только RUNNING/REVIEW)"
            ),
        }

    # ─── Утилиты (статические) ────────────────────────────────────

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def find_repo_root(start_path: Path | None = None) -> Path:
        """Найти корень репозитория (папка с .git). Кэшируется."""
        current = (start_path or Path(__file__)).resolve()
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        raise ChainError("Git repository root not found")

    @staticmethod
    def parse_frontmatter_file(file_path: Path) -> dict[str, str]:
        """
        Извлечь frontmatter из markdown-файла.

        Заменяет дублированную функцию из analysis-status.py,
        check-chain-readiness.py, validate-analysis-*.py.
        """
        if not file_path.exists():
            return {}
        text = file_path.read_text(encoding="utf-8")
        match = FRONTMATTER_PATTERN.match(text)
        if not match:
            return {}
        result = {}
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith("  "):
                key, _, value = line.partition(":")
                result[key.strip()] = value.strip()
        return result

    @staticmethod
    def count_markers(file_path: Path) -> int:
        """Посчитать маркеры [ТРЕБУЕТ УТОЧНЕНИЯ в файле."""
        if not file_path.exists():
            return 0
        text = file_path.read_text(encoding="utf-8")
        return len(MARKER_PATTERN.findall(text))

    @staticmethod
    def count_barriers(file_path: Path) -> int:
        """Посчитать ⛔ DEPENDENCY BARRIER в файле."""
        if not file_path.exists():
            return 0
        text = file_path.read_text(encoding="utf-8")
        return len(BARRIER_PATTERN.findall(text))

    @staticmethod
    def count_iterations(file_path: Path) -> int:
        """Посчитать ## Итерация N в review.md."""
        if not file_path.exists():
            return 0
        text = file_path.read_text(encoding="utf-8")
        return len(re.findall(r"^## Итерация \d+", text, re.MULTILINE))

    @staticmethod
    def find_all_chains(repo_root: Path | None = None) -> list[str]:
        """
        Найти все цепочки NNNN-{topic} в specs/analysis/.

        Returns:
            Имена папок: ["0001-oauth2-authorization", ...]
        """
        root = repo_root or ChainManager.find_repo_root()
        analysis_dir = root / "specs" / "analysis"
        if not analysis_dir.exists():
            return []
        return sorted(
            d.name for d in analysis_dir.iterdir()
            if d.is_dir() and CHAIN_FOLDER_PATTERN.match(d.name)
        )
