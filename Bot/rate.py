"""Execution of the !rate command."""

import random

from history import record_command


def run_rate(text, chatter_id, username, clean_argument, swap_perspective):
    """Run the command using the router's existing argument helpers."""
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        return "You have to give me something to rate."

    raw_subject = clean_argument(parts[1])

    if not raw_subject:
        return "You have to give me something to rate."

    subject = swap_perspective(raw_subject)
    record_command(
        chatter_id,
        username,
        "rate",
        subject,
    )
    rating = round(random.uniform(0, 10), 1)

    if rating < 2:
        comment = "Yikes."
    elif rating < 4:
        comment = "I've seen worse. Probably."
    elif rating < 6:
        comment = "Aggressively mediocre."
    elif rating < 8:
        comment = "Actually pretty solid."
    elif rating < 9.5:
        comment = "Ooh, that's good."
    else:
        comment = "Basically flawless."

    return f"I give {subject} a {rating}/10. {comment}"
