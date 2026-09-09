"""Public Twitch command parsing, cooldowns, mini-games, and command logic."""

import re
import time
import unicodedata

from escape import run_escape
from praise import run_praise
from rate import run_rate
from sass import run_sass
from sus import run_sus
from vibe import run_vibe
from wyr import run_wyr
from profiles import (
    set_nickname,
    get_sassy_name,
    clear_nickname,
    get_escape_leaderboard,
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
        return run_wyr(chatter_id, username)

    # ---- Commands that operate on a subject ------------------------------
    if command == "!rate":
        return run_rate(
            text, chatter_id, username, clean_argument, swap_perspective,
        )

    if command == "!praise":
        return run_praise(
            text, chatter_id, username, clean_argument, swap_perspective,
        )

    if command == "!vibe":
        return run_vibe(
            text, chatter_id, username, clean_argument, swap_perspective,
        )

    if command == "!sass":
        return run_sass(
            text, chatter_id, username, clean_argument, swap_perspective,
        )

    if command == "!sus":
        return run_sus(
            text, chatter_id, username, clean_argument, swap_perspective,
        )

    # ---- Escape mini-game ------------------------------------------------
    if command == "!escape":
        return run_escape(chatter_id, username, sassy_name)

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