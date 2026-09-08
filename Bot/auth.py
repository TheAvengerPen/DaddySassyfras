"""One-time Twitch OAuth authorization for the DaddySassyfras bot account."""

import os
import secrets
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:3000"
SCOPES = "user:read:chat user:write:chat user:bot"

# Random state protects the local OAuth callback from being spoofed.
state = secrets.token_urlsafe(24)
auth_code = None


class CallbackHandler(BaseHTTPRequestHandler):
    """Receive the one-time OAuth redirect from Twitch on localhost."""

    def do_GET(self):
        global auth_code

        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if params.get("state", [None])[0] != state:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"State mismatch.")
            return

        auth_code = params.get("code", [None])[0]

        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            b"Authentication successful. You can close this browser tab."
        )

    def log_message(self, format, *args):
        pass


# Build the Twitch authorization URL and ask the user to approve the bot.
params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPES,
    "state": state,
    "force_verify": "true",
}

auth_url = "https://id.twitch.tv/oauth2/authorize?" + urllib.parse.urlencode(params)

print("Opening Twitch authorization page...")
webbrowser.open(auth_url)

server = HTTPServer(("localhost", 3000), CallbackHandler)

while auth_code is None:
    server.handle_request()

server.server_close()

# Exchange the temporary authorization code for real OAuth tokens.
response = requests.post(
    "https://id.twitch.tv/oauth2/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    },
)

response.raise_for_status()
token_data = response.json()
access_token = token_data["access_token"]

# Safety check: never overwrite .tokens with another account, will drive you crazy
user_response = requests.get(
    "https://api.twitch.tv/helix/users",
    headers={
        "Authorization": f"Bearer {access_token}",
        "Client-Id": CLIENT_ID,
    },
)

user_response.raise_for_status()
user_data = user_response.json()["data"]

if not user_data:
    raise RuntimeError("Could not determine which Twitch account was authorized.")

authorized_login = user_data[0]["login"]

if authorized_login.lower() != "daddysassyfras":
    raise RuntimeError(
        f"Wrong Twitch account authorized: {authorized_login}. "
        "Please authorize as daddysassyfras."
    )

# Only write tokens after the account identity has been verified.
with open(".tokens", "w", encoding="utf-8") as f:
    f.write(f"TWITCH_ACCESS_TOKEN={token_data['access_token']}\n")
    f.write(f"TWITCH_REFRESH_TOKEN={token_data['refresh_token']}\n")

print("Authentication complete.")
print("Tokens saved to .tokens")
