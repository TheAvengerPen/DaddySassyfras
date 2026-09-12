"""Execution of the !wyr command."""

import random

from history import record_command
from responses import WOULD_YOU_RATHER


def run_wyr(chatter_id, username):
    """Record the command and choose a would-you-rather response."""
    record_command(
        chatter_id,
        username,
        "wyr",
    )
    return random.choice(WOULD_YOU_RATHER)
