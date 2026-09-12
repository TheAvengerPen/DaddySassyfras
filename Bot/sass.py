"""Execution of the !sass command."""

import random

from history import record_command
from responses import SASSES


def run_sass(text, chatter_id, username, clean_argument, swap_perspective):
    """Run the command using the router's existing argument helpers."""
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        return "Who or what am I sassing?"

    raw_subject = clean_argument(parts[1])

    if not raw_subject:
        return "Who or what am I sassing?"

    subject = swap_perspective(raw_subject)
    record_command(
        chatter_id,
        username,
        "sass",
        subject,
    )
    sass = random.choice(SASSES)

    return sass.format(subject=subject)
