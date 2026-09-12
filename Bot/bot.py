"""Main Twitch connection and runtime loop for Sassy."""


import asyncio
import json
import os
import time
from datetime import datetime
from time import perf_counter

import requests
import websockets
from dotenv import load_dotenv

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from admin_commands import handle_admin_command
from commands import handle_command
from passive import handle_passive
from profiles import get_sassy_name

# .env stores app credentials; .tokens stores the current bot-account tokens.
# override=True makes the dedicated token file win over any stale environment value.
load_dotenv()
load_dotenv(".tokens", override=True)

OWNER_LOGIN = "LanUnlimited"
SEND_CHAT_URL = "https://api.twitch.tv/helix/chat/messages"

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")

TARGET_CHANNEL = "LanUnlimited"

# Runtime switches. These can be changed from Sassy's terminal with % commands.
COMMANDS_ENABLED = True
PASSIVES_ENABLED = True
DEBUG_ENABLED = True

EVENTSUB_URL = "wss://eventsub.wss.twitch.tv/ws"
EVENTSUB_SUB_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"

# At most one passive reply may be sent during this many seconds.
PASSIVE_COOLDOWN = 5
last_passive_time = 0.0


#
# Twitch HTTP helpers
#


def twitch_headers():
    """Return the headers required by Twitch Helix API calls."""
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Client-Id": CLIENT_ID,
        "Content-Type": "application/json",
    }


def get_user_by_login(login):
    """Look up one Twitch user record by login name."""
    response = requests.get(
        "https://api.twitch.tv/helix/users",
        headers=twitch_headers(),
        params={"login": login},
    )

    response.raise_for_status()

    data = response.json()["data"]

    if not data:
        raise RuntimeError(f"Could not find Twitch user: {login}")

    return data[0]


def create_chat_subscription(session_id, broadcaster_id, bot_user_id):
    """Subscribe the current EventSub WebSocket session to chat messages."""
    payload = {
        "type": "channel.chat.message",
        "version": "1",
        "condition": {
            "broadcaster_user_id": broadcaster_id,
            "user_id": bot_user_id,
        },
        "transport": {
            "method": "websocket",
            "session_id": session_id,
        },
    }

    response = requests.post(
        EVENTSUB_SUB_URL,
        headers=twitch_headers(),
        json=payload,
    )

    if response.status_code != 202:
        print("Subscription failed:")
        print(response.status_code)
        print(response.text)
        response.raise_for_status()

    print(f"Now monitoring chat in: {TARGET_CHANNEL}")


def send_chat_message(broadcaster_id, bot_user_id, text):
    """Send one message as DaddySassyfras and report whether Twitch accepted it."""
    payload = {
        "broadcaster_id": broadcaster_id,
        "sender_id": bot_user_id,
        "message": text,
    }

    send_start = perf_counter()

    response = requests.post(
        SEND_CHAT_URL,
        headers=twitch_headers(),
        json=payload,
    )

    send_elapsed = perf_counter() - send_start
    if DEBUG_ENABLED:
        print(f"[DEBUG] Twitch send API: {send_elapsed:.3f}s")

    if response.status_code != 200:
        print("Failed to send chat message:")
        print(response.status_code)
        print(response.text)
        return False

    return True


#
# Local terminal controls
# 


async def terminal_chat(broadcaster_id, bot_user_id):
    """Read local terminal input for admin controls or manual bot messages."""
    session = PromptSession("> ")

    # Admin input stays local; only plain text reaches Twitch.
    with patch_stdout():
        while True:
            try:
                text = await session.prompt_async()
            except (EOFError, KeyboardInterrupt):
                return

            text = text.strip()

            if not text:
                continue

            if text.lower() == "/quit":
                return

            # The % prefix is reserved for local admin input, including typos.
            if text.startswith("%"):
                handle_admin_command(text, globals())
                continue

            # Plain text that did not match an admin command is spoken by Sassy.
            send_chat_message(broadcaster_id, bot_user_id, text)


#
# EventSub / chat runtime
#


async def main():
    """Connect to Twitch, log chat, and route messages to Sassy's behaviors."""
    global last_passive_time

    bot_user = get_user_by_login("daddysassyfras")
    broadcaster = get_user_by_login(TARGET_CHANNEL)
    owner = get_user_by_login(OWNER_LOGIN)

    print(f"Bot account: {bot_user['login']}")
    print(f"Target channel: {broadcaster['login']}")
    print()
    print("Connecting to Twitch...")

    try:
        async with websockets.connect(EVENTSUB_URL) as websocket:
            while True:
                raw_message = await websocket.recv()
                message = json.loads(raw_message)

                message_type = message["metadata"]["message_type"]

                # Twitch first welcomes the WebSocket session; only then can
                # Create the chat subscription tied to that session ID.
                if message_type == "session_welcome":
                    session_id = message["payload"]["session"]["id"]

                    print("Connected.")
                    print("Creating chat subscription...")

                    create_chat_subscription(
                        session_id,
                        broadcaster["id"],
                        bot_user["id"],
                    )

                    print()
                    print("Chat log:")
                    print("-" * 50)
                    print("Type a message and press Enter to speak as daddysassyfras.")

                    terminal_task = asyncio.create_task(
                        terminal_chat(
                            broadcaster["id"],
                            bot_user["id"],
                        )
                    )

                # Notifications are the actual incoming chat messages.
                elif message_type == "notification":
                    event = message["payload"]["event"]

                    username = event["chatter_user_name"]
                    chatter_id = event["chatter_user_id"]
                    text = event["message"]["text"]

                    timestamp = datetime.now().strftime("%H:%M:%S")

                    print(f"[{timestamp}] {username}: {text}")

                    # Passives are evaluated before commands. Sassy's own messages
                    # are excluded here to prevent passive-response loops.
                    if PASSIVES_ENABLED and chatter_id != bot_user["id"]:
                        passive_name = get_sassy_name(
                            chatter_id,
                            username,
                        )

                        now = time.monotonic()

                        passive_response = handle_passive(
                            text,
                            passive_name,
                        )

                        if passive_response and now - last_passive_time >= PASSIVE_COOLDOWN:
                            send_chat_message(
                                broadcaster["id"],
                                bot_user["id"],
                                passive_response,
                            )

                            last_passive_time = now

                    # I can always test commands. Everyone else depends
                    # on the runtime %commands switch.
                    if chatter_id == owner["id"] or COMMANDS_ENABLED:
                        command_start = perf_counter()

                        response = handle_command(
                            text,
                            chatter_id,
                            username,
                        )

                        command_elapsed = perf_counter() - command_start

                        if response:
                            if DEBUG_ENABLED:
                                print(
                                    f"[DEBUG] Command logic: {command_elapsed:.3f}s"
                                )

                            total_start = perf_counter()

                            send_chat_message(
                                broadcaster["id"],
                                bot_user["id"],
                                response,
                            )

                            total_elapsed = command_elapsed + (
                                perf_counter() - total_start
                            )
                            if DEBUG_ENABLED:
                                print(
                                    f"[DEBUG] Command + send: {total_elapsed:.3f}s"
                                )

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped.")
