#!/usr/bin/env python3
"""
Хук SubagentStop: обновляет статус агента и удаляет блокировки (fallback).

Входные данные (stdin JSON):
- agent_id: уникальный ID субагента
- agent_type: тип агента (Explore, Bash, кастомный)

Действия:
1. Обновляет статус в agents-status.json на completed
2. Удаляет оставшиеся блокировки агента из locks.json (fallback/страховка)

SSOT: /.claude/.instructions/state/standard-state.md
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    # Читаем JSON из stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    agent_id = input_data.get("agent_id")

    if not agent_id:
        print("Error: agent_id is required", file=sys.stderr)
        sys.exit(1)

    script_dir = Path(__file__).parent
    state_dir = script_dir.parent / "state"
    agents_file = state_dir / "agents-status.json"
    locks_file = state_dir / "locks.json"

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # 1. Обновляем статус агента
    if agents_file.exists():
        try:
            with open(agents_file, "r", encoding="utf-8") as f:
                agents_state = json.load(f)
        except json.JSONDecodeError:
            agents_state = {"agents": {}}

        if agent_id in agents_state.get("agents", {}):
            agents_state["agents"][agent_id]["status"] = "completed"
            agents_state["agents"][agent_id]["finished_at"] = now

            with open(agents_file, "w", encoding="utf-8") as f:
                json.dump(agents_state, f, indent=2, ensure_ascii=False)
                f.write("\n")

            print(f"Agent {agent_id} status updated to completed")
        else:
            print(f"Warning: Agent {agent_id} not found in agents-status.json")

    # 2. Удаляем блокировки агента (fallback)
    removed_locks = []
    if locks_file.exists():
        try:
            with open(locks_file, "r", encoding="utf-8") as f:
                locks_state = json.load(f)
        except json.JSONDecodeError:
            locks_state = {"locks": {}}

        locks = locks_state.get("locks", {})
        keys_to_remove = [
            path for path, lock in locks.items() if lock.get("agent") == agent_id
        ]

        for key in keys_to_remove:
            del locks[key]
            removed_locks.append(key)

        if keys_to_remove:
            with open(locks_file, "w", encoding="utf-8") as f:
                json.dump(locks_state, f, indent=2, ensure_ascii=False)
                f.write("\n")

    if removed_locks:
        print(f"Removed {len(removed_locks)} stale lock(s): {removed_locks}")
    else:
        print("No stale locks to remove")


if __name__ == "__main__":
    main()
