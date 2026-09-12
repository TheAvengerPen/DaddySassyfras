"""Parsing and execution of local % terminal/admin commands."""

from profiles import list_nicknames, release_nickname


def handle_admin_command(text, runtime):
    """Handle % input using bot.py's live globals mapping for runtime switches."""
    #Nickname admin tools
    if text.lower() == "%nicknames":
        entries = list_nicknames()

        if not entries:
            print("No nicknames are currently assigned.")
            return

        print()
        print("Assigned nicknames:")
        print("-" * 50)

        for entry in entries:
            print(
                f"{entry['twitch_name']:<20} -> {entry['nickname']}"
            )

        print("-" * 50)
        return

    if text.lower().startswith("%releasenickname"):
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            print("Usage: %releasenickname <nickname>")
            return

        success, message = release_nickname(parts[1].strip())
        print(message)
        return

    #Runtime on/off switches
    if text.lower().startswith("%commands"):
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            state = "ON" if runtime["COMMANDS_ENABLED"] else "OFF"
            print(f"Public commands are currently {state}.")
            return

        setting = parts[1].strip().lower()

        if setting == "on":
            runtime["COMMANDS_ENABLED"] = True
            print("Public commands enabled.")
            return

        if setting == "off":
            runtime["COMMANDS_ENABLED"] = False
            print("Public commands disabled.")
            return

        print("Usage: %commands on | off")
        return

    if text.lower().startswith("%debug"):
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            state = "ON" if runtime["DEBUG_ENABLED"] else "OFF"
            print(f"Debug logging is currently {state}.")
            return

        setting = parts[1].strip().lower()

        if setting == "on":
            runtime["DEBUG_ENABLED"] = True
            print("Debug logging enabled.")
            return

        if setting == "off":
            runtime["DEBUG_ENABLED"] = False
            print("Debug logging disabled.")
            return

        print("Usage: %debug on | off")
        return

    if text.lower().startswith("%passive"):
        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            state = "ON" if runtime["PASSIVES_ENABLED"] else "OFF"
            print(f"Passive responses are currently {state}.")
            return

        setting = parts[1].strip().lower()

        if setting == "on":
            runtime["PASSIVES_ENABLED"] = True
            print("Passive responses enabled.")
            return

        if setting == "off":
            runtime["PASSIVES_ENABLED"] = False
            print("Passive responses disabled.")
            return

        print("Usage: %passive on | off")
        return

    # Any remaining % input is an unrecognized terminal/admin command.
    # Keep it local so a typo such as %pasive never gets sent to Twitch.
    if text.startswith("%"):
        print(f"Unknown admin command: {text}")
        return
