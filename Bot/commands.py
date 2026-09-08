"""Public Twitch command parsing, cooldowns, mini-games, and command logic."""

import random
import re
import time
import unicodedata

from history import record_command
from profiles import (
    set_nickname,
    get_sassy_name,
    clear_nickname,
    update_escape_best,
    get_escape_leaderboard,
)
from responses import (
    WOULD_YOU_RATHER,
    PRAISES,
    VIBES,
    SASSES,
    SUS_RESPONSES,
    ESCAPE_FAIL_0,
    ESCAPE_FAIL_LOW,
    ESCAPE_FAIL_MID,
    ESCAPE_FAIL_HIGH,
    ESCAPE_FAIL_INSANE,
    ESCAPE_SUCCESS,
)

# Cooldowns are in seconds. USER_COOLDOWN is currently shortened for testing.
USER_COOLDOWN = 5
OWNER_COOLDOWN = 5
GLOBAL_COOLDOWN = 2

OWNER_LOGIN = "LanUnlimited"

# Cooldown state is intentionally runtime-only; restarting Sassy clears it.
user_cooldowns = {}
global_cooldowns = {}
cooldown_warnings = {}

# Short-term memory keeps escape responses from feeling like raw RNG.
# Avoid recently used templates, but still allow them back naturally later.
recent_escape_responses = []
ESCAPE_RECENT_MEMORY = 4

# Only real user-facing actions consume command cooldowns.
# Diagnostic/help commands such as !ping and !sassys are intentionally excluded.
COOLDOWN_COMMANDS = {
    "!wyr",
    "!rate",
    "!praise",
    "!vibe",
    "!sass",
    "!sus",
    "!nickname",
    "!escape",
    "!escapeboard",
}

# Per-gate pass chances. A player must pass every earlier gate to reach later ones.
ESCAPE_CHANCES = [
    0.98,  # Gate 1
    0.95,  # Gate 2
    0.90,  # Gate 3
    0.82,  # Gate 4
    0.72,  # Gate 5
    0.60,  # Gate 6
    0.48,  # Gate 7
    0.35,  # Gate 8
    0.23,  # Gate 9
    0.14,  # Gate 10
    0.08,  # Gate 11
    0.04,  # Gate 12
]


# ---------------------------------------------------------------------------
# Input cleanup
# ---------------------------------------------------------------------------


def clean_command(text):
    """Extract only the leading !command token and normalize it to lowercase."""
    match = re.match(r"^![a-zA-Z0-9_]+", text)

    if not match:
        return ""

    return match.group(0).lower()

def clean_argument(text):
    """Remove invisible formatting characters that can sneak in from Twitch chat."""
    text = "".join(
        char for char in text
        if char != "\u034f" and unicodedata.category(char) != "Cf"
    )

    return text.strip()

def swap_perspective(text):
    """Swap simple first/second-person words so Sassy replies naturally."""
    words = text.split()

    swaps = {
        "my": "your",
        "your": "my",
        "me": "you",
        "you": "me",
    }

    result = []

    for word in words:
        lower = word.lower()

        if lower in swaps:
            replacement = swaps[lower]

            if word[0].isupper():
                replacement = replacement.capitalize()

            result.append(replacement)
        else:
            result.append(word)

    return " ".join(result)


# ---------------------------------------------------------------------------
# Escape mini-game
# ---------------------------------------------------------------------------


def run_escape():
    """Roll the escape gates in order and return how many were cleared."""
    gates_passed = 0

    for chance in ESCAPE_CHANCES:
        if random.random() <= chance:
            gates_passed += 1
        else:
            break

    return gates_passed

def choose_escape_response(responses):
    """Choose an escape line while avoiding very recent repeats when possible."""
    # Prefer lines that have not been used recently.
    available = [
        response for response in responses
        if response not in recent_escape_responses
    ]

    # If a small pool has been exhausted, allow the full pool again.
    if not available:
        available = responses

    chosen = random.choice(available)

    recent_escape_responses.append(chosen)

    if len(recent_escape_responses) > ESCAPE_RECENT_MEMORY:
        recent_escape_responses.pop(0)

    return chosen


# ---------------------------------------------------------------------------
# Cooldowns
# ---------------------------------------------------------------------------


def check_cooldown(command, chatter_id, username):
    """Apply per-user and channel-wide cooldowns for one command."""
    now = time.monotonic()

    # Lan gets a much shorter cooldown while we're developing.
    if username.lower() == OWNER_LOGIN.lower():
        user_limit = OWNER_COOLDOWN
    else:
        user_limit = USER_COOLDOWN

    user_key = (chatter_id, command)
    last_user_use = user_cooldowns.get(user_key)

    if last_user_use is not None:
        elapsed = now - last_user_use

        if elapsed < user_limit:
            # Warn only once during this cooldown period.
            if not cooldown_warnings.get(user_key, False):
                cooldown_warnings[user_key] = True
                return False, "That command is still cooling off. Try again later."

            return False, None

    # Tiny channel-wide protection for this particular command.
    last_global_use = global_cooldowns.get(command)

    if last_global_use is not None:
        if now - last_global_use < GLOBAL_COOLDOWN:
            return False, None

    # Command is allowed.
    user_cooldowns[user_key] = now
    global_cooldowns[command] = now
    cooldown_warnings[user_key] = False

    return True, None


# ---------------------------------------------------------------------------
# Command router
# ---------------------------------------------------------------------------


def handle_command(text, chatter_id, username):
    """Handle one chat message and return Sassy's response, or None."""
    # Commands are checked from top to bottom. A matching branch returns
    # immediately; unknown !commands eventually fall through to None.
    command = clean_command(text)
    sassy_name = get_sassy_name(chatter_id, username)

    if command in COOLDOWN_COMMANDS:
        allowed, cooldown_message = check_cooldown(
            command,
            chatter_id,
            username,
        )

        if not allowed:
            return cooldown_message

    # ---- Identity / nickname ---------------------------------------------
    if command == "!nickname":
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            return f"I'm calling you {sassy_name}."

        nickname = clean_argument(parts[1])

        if nickname.lower() == "clear":
            _success, message = clear_nickname(
                chatter_id,
                username,
            )
            return message

        _success, message = set_nickname(
            chatter_id,
            username,
            nickname,
        )

        return message

    # ---- Simple commands -------------------------------------------------
    if command == "!ping":
        return "pong"

    if command == "!wyr":
        record_command(
            chatter_id,
            username,
            "wyr",
        )
        return random.choice(WOULD_YOU_RATHER)

    # ---- Commands that operate on a subject ------------------------------
    if command == "!rate":
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

    if command == "!praise":
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

    if command == "!vibe":
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

    if command == "!sass":
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

    if command == "!sus":
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

    # ---- Escape mini-game ------------------------------------------------
    if command == "!escape":
        record_command(
            chatter_id,
            username,
            "escape",
        )
        gates = run_escape()

        new_record, _old_best = update_escape_best(
            chatter_id,
            username,
            gates,
        )

        if gates == len(ESCAPE_CHANCES):
            template = choose_escape_response(ESCAPE_SUCCESS)

        elif gates == 0:
            template = choose_escape_response(ESCAPE_FAIL_0)

        elif gates <= 3:
            template = choose_escape_response(ESCAPE_FAIL_LOW)

        elif gates <= 6:
            template = choose_escape_response(ESCAPE_FAIL_MID)

        elif gates <= 9:
            template = choose_escape_response(ESCAPE_FAIL_HIGH)

        else:
            template = choose_escape_response(ESCAPE_FAIL_INSANE)

        gate_word = "gate" if gates == 1 else "gates"

        result = template.format(
            name=sassy_name,
            gates=gates,
            gate_word=gate_word,
        )

        if new_record:
            result += " NEW RECORD!"

        return result

    if command == "!escapeboard":
        leaderboard = get_escape_leaderboard()

        if not leaderboard:
            return "Nobody has escaped anything yet."

        top = leaderboard[:5]

        entries = []

        for position, player in enumerate(top, start=1):
            entries.append(
                f"{position}. {player['name']} - {player['score']}"
            )

        return "🚪 ESCAPE RECORDS 🚪 " + " | ".join(entries)

    # ---- Help ------------------------------------------------------------
    if command == "!sassys":
        return (
            "Sassy commands: "
            "!wyr | "
            "!rate <thing> | "
            "!praise <thing> | "
            "!vibe <thing> | "
            "!sass <thing> | "
            "!sus <thing> | "
            "!nickname <name/clear> | "
            "!escape | "
            "!escapeboard"
        )

    return None