"""Execution of the !praise command."""

import random

from history import record_command
from responses import PRAISES


def run_praise(text, chatter_id, username, clean_argument, swap_perspective):
    """Run the command using the router's existing argument helpers."""
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        return "Who am I praising?"

    raw_subject = clean_argument(parts[1])

    if not raw_subject:
        return "Who am I praising?"

    subject = swap_perspective(raw_subject)
    record_command(
        chatter_id,
        username,
        "praise",
        subject,
    )
    praise = random.choice(PRAISES)

    return praise.format(subject=subject)
