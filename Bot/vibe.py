"""Execution of the !vibe command."""

import random

from history import record_command
from responses import VIBES


def run_vibe(text, chatter_id, username, clean_argument, swap_perspective):
    """Run the command using the router's existing argument helpers."""
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        return "Whose vibe am I judging?"

    raw_subject = clean_argument(parts[1])

    if not raw_subject:
        return "Whose vibe am I judging?"

    subject = swap_perspective(raw_subject)
    record_command(
        chatter_id,
        username,
        "vibe",
        subject,
    )
    vibe = random.choice(VIBES)

    return vibe.format(subject=subject)
