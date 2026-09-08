"""Persistent behavioral telemetry used as Sassy's long-term observation log."""

import json
from datetime import datetime, timezone
from pathlib import Path


HISTORY_FILE = Path("sassy_history.json")
RECENT_LIMIT = 20


def load_history():
    """Load telemetry and ensure the two top-level collections exist."""
    if not HISTORY_FILE.exists():
        return {
            "users": {},
            "subjects": {},
        }

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        history = json.load(file)

    history.setdefault("users", {})
    history.setdefault("subjects", {})
    return history


def save_history(history):
    """Write the current telemetry snapshot to disk."""
    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)


def _now():
    """Return an explicit UTC timestamp suitable for JSON storage."""
    return datetime.now(timezone.utc).isoformat()


def _get_user_command(user, command):
    """Return the current user-command record, upgrading old integer data if needed."""
    existing = user["commands"].get(command)

    # Older sassy_history.json files stored command counts as plain integers.
    if isinstance(existing, int):
        existing = {
            "total": existing,
            "recent": [],
        }
        user["commands"][command] = existing

    if existing is None:
        existing = {
            "total": 0,
            "recent": [],
        }
        user["commands"][command] = existing

    # Keep this tolerant of partially-upgraded history files, may purge later.
    existing.setdefault("total", 0)
    existing.setdefault("recent", [])
    return existing


def record_command(user_id, username, command, subject=None):
    """Record a command use, optionally including the command's subject."""
    history = load_history()
    timestamp = _now()

    users = history.setdefault("users", {})
    user = users.setdefault(
        user_id,
        {
            "name": username,
            "total_commands": 0,
            "commands": {},
            "last_used": None,
        },
    )

    user.setdefault("commands", {})
    user.setdefault("total_commands", 0)
    user["name"] = username
    user["total_commands"] += 1

    user_command = _get_user_command(user, command)
    user_command["total"] += 1
    user_command["recent"].append(timestamp)
    user_command["recent"] = user_command["recent"][-RECENT_LIMIT:]
    user["last_used"] = timestamp

    # Subject tracking lets us later distinguish broad community trends from
    # one user repeatedly targeting the same person or thing.
    if subject:
        clean_subject = subject.strip()
        subject_key = clean_subject.lower()

        subjects = history.setdefault("subjects", {})
        subject_data = subjects.setdefault(
            subject_key,
            {
                "display_name": clean_subject,
                "commands": {},
                "last_used": None,
            },
        )

        subject_data.setdefault("display_name", clean_subject)
        subject_data.setdefault("commands", {})
        subject_data["last_used"] = timestamp

        command_data = subject_data["commands"].setdefault(
            command,
            {
                "total": 0,
                "users": {},
                "recent": [],
            },
        )

        command_data.setdefault("total", 0)
        command_data.setdefault("users", {})
        command_data.setdefault("recent", [])

        command_data["total"] += 1
        command_data["recent"].append(timestamp)
        command_data["recent"] = command_data["recent"][-RECENT_LIMIT:]
        command_data["users"][user_id] = (
            command_data["users"].get(user_id, 0) + 1
        )

    save_history(history)
