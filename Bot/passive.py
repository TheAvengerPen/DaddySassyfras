"""Low-noise reactions to ordinary chat that do not require a !command."""

import random
import re


# Directed social responses. These only fire when chat addresses Sassy/Daddy.
THANKS_DADDY_RESPONSES = [
    "You're welcome, {user}.",
    "Anytime, {user}.",
    "Of course, {user}.",
    "You got it, {user}.",
    "Happy to help, {user}.",
    "Don't mention it, {user}.",
    "Daddy's got you, {user}.",
    "You're very welcome, {user}.",
]

HELLO_RESPONSES = [
    "Hey, {user}.",
    "Hello there, {user}.",
    "Hi hi, {user}.",
    "Well hello, {user}.",
    "Hey yourself, {user}.",
    "Howdy, {user}.",
    "There you are, {user}.",
]

GOODBYE_RESPONSES = [
    "Later, {user}.",
    "Bye, {user}. Behave yourself.",
    "See you around, {user}.",
    "Take care, {user}.",
    "Later, {user}. Try not to miss me too much.",
    "Bye bye, {user}.",
    "Until next time, {user}.",
    "See ya, {user}.",
    "Go on, get outta here, {user}.",
    "Farewell, {user}. I'll try to carry on.",
]

# Opportunistic trigger words. A matching message gets only one 5% roll,
# even if it contains more than one word from this list.
DEEZ_NUTZ_TRIGGERS = [
    "pound",
    "polish",
    "grind",
    "squeeze",
    "grab",
    "hold",
    "lick",
    "suck",
    "rub",
    "stroke",
    "smack",
    "beat",
]


def handle_passive(text, username):
    """Return one passive response when the message creates an opportunity."""
    # Directed social reactions are checked first.
    if re.search(r"\bthanks\s*,?\s+daddy\b", text, re.IGNORECASE):
        response = random.choice(THANKS_DADDY_RESPONSES)
        return response.format(user=username)

    if re.search(
        r"\b(hello|hi|hey)\s+(daddy|@daddysassyfras)\b",
        text,
        re.IGNORECASE,
    ):
        response = random.choice(HELLO_RESPONSES)
        return response.format(user=username)

    if re.search(
        r"\b(bye|goodbye|later|cya|see ya|see you)\s+(daddy|@daddysassyfras)\b",
        text,
        re.IGNORECASE,
    ):
        response = random.choice(GOODBYE_RESPONSES)
        return response.format(user=username)

    # Opportunistic Deez Nutz check. Match complete words so a trigger such
    # as "rub" does not match "grubby"
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    for trigger in DEEZ_NUTZ_TRIGGERS:
        if trigger in words:
            if random.random() < 0.05:
                return f"{trigger.upper()} DEEZ NUTZ"

            # Stop after the first matching trigger so there is one roll/message.
            break

    return None