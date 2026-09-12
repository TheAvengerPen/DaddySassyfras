"""Execution of the !sus command."""

import random

from history import record_command
from responses import SUS_RESPONSES


def run_sus(text, chatter_id, username, clean_argument, swap_perspective):
    """Run the command using the router's existing argument helpers."""
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        return "Who or what are we suspicious of?"

    raw_subject = clean_argument(parts[1])

    if not raw_subject:
        return "Who or what are we suspicious of?"

    subject = swap_perspective(raw_subject)
    record_command(
        chatter_id,
        username,
        "sus",
        subject,
    )
    response = random.choice(SUS_RESPONSES)

    return response.format(subject=subject)
