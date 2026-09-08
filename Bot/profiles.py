"""Persistent Twitch-user profiles, nicknames, and escape-game records."""

import json
import os

PROFILE_FILE = "profiles.json"


def load_profiles():
    """Load profiles.json, creating an empty in-memory registry if absent."""
    if not os.path.exists(PROFILE_FILE):
        return {}

    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_profiles(profiles):
    """Persist the complete profile registry."""
    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(profiles, file, indent=4)


def validate_nickname(nickname):
    """Enforce Sassy's 1-10 character ASCII alphanumeric nickname rules."""
    if not nickname:
        return False, "Give me a nickname."

    if len(nickname) > 10:
        return False, "Nicknames are limited to 10 characters."

    if not nickname.isascii() or not nickname.isalnum():
        return False, "Nicknames can only contain letters and numbers."

    return True, None


def nickname_taken(profiles, nickname, user_id):
    """Return True when another Twitch ID already owns this nickname."""
    wanted = nickname.lower()

    for existing_user_id, profile in profiles.items():
        existing_nickname = profile.get("nickname")

        if (
            existing_nickname
            and existing_nickname.lower() == wanted
            and existing_user_id != user_id
        ):
            return True

    return False


def list_nicknames():
    """Return the currently assigned nickname registry for terminal display."""
    profiles = load_profiles()

    entries = []

    for user_id, profile in profiles.items():
        nickname = profile.get("nickname")
        twitch_name = profile.get("twitch_name")

        if nickname:
            entries.append(
                {
                    "user_id": user_id,
                    "twitch_name": twitch_name,
                    "nickname": nickname,
                }
            )

    return entries


def release_nickname(nickname):
    """Admin override that releases a nickname without deleting user stats."""
    profiles = load_profiles()
    wanted = nickname.lower()

    for user_id, profile in profiles.items():
        existing = profile.get("nickname")

        if existing and existing.lower() == wanted:
            twitch_name = profile.get("twitch_name", user_id)

            profile["nickname"] = None
            save_profiles(profiles)

            return True, f'Released nickname "{existing}" from {twitch_name}.'

    return False, f'Nickname "{nickname}" was not found.'


def set_nickname(user_id, twitch_name, nickname):
    """Assign a validated, globally unique nickname to a Twitch user ID."""
    profiles = load_profiles()

    valid, error = validate_nickname(nickname)

    if not valid:
        return False, error

    if nickname_taken(profiles, nickname, user_id):
        return False, "That nickname is already taken. Find your own identity."

    profile = profiles.setdefault(user_id, {})

    profile["twitch_name"] = twitch_name
    profile["nickname"] = nickname

    save_profiles(profiles)

    return True, f"Fine. You're {nickname} now."


def get_sassy_name(user_id, twitch_name):
    """Return the nickname Sassy should use, or the Twitch name as fallback."""
    profiles = load_profiles()

    profile = profiles.get(user_id)

    if profile and profile.get("nickname"):
        return profile["nickname"]

    return twitch_name


def update_escape_best(user_id, twitch_name, gates):
    """Store a new personal escape record and report whether it improved."""
    profiles = load_profiles()

    profile = profiles.setdefault(user_id, {})
    profile["twitch_name"] = twitch_name

    old_best = profile.get("escape_best", 0)

    if gates > old_best:
        profile["escape_best"] = gates
        save_profiles(profiles)
        return True, old_best

    return False, old_best


def get_escape_leaderboard():
    """Return all escape records sorted from highest to lowest."""
    profiles = load_profiles()
    leaderboard = []

    for user_id, profile in profiles.items():
        best = profile.get("escape_best")

        if best is None:
            continue

        name = profile.get("nickname") or profile.get("twitch_name", "Unknown")

        leaderboard.append({
            "name": name,
            "score": best,
        })

    leaderboard.sort(
        key=lambda entry: entry["score"],
        reverse=True,
    )

    return leaderboard


def clear_nickname(user_id, twitch_name):
    """Remove a user nickname while preserving the rest of their profile."""
    profiles = load_profiles()

    profile = profiles.get(user_id)

    if not profile or not profile.get("nickname"):
        return False, f"I'm already calling you {twitch_name}."

    old_nickname = profile["nickname"]

    profile["nickname"] = None
    profile["twitch_name"] = twitch_name

    save_profiles(profiles)

    return True, f"Fine. {old_nickname} is gone. You're {twitch_name} again."