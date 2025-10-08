import os
import json
import webbrowser
import urllib.parse
from pathlib import Path
import requests

class AuthManager:
    """Handles WHOOP OAuth authentication and token management."""

    AUTH_URL = "https://api.prod.whoop.com/oauth/oauth2/auth"
    TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
    CONFIG_PATH = Path.home() / ".whoop_sdk" / "config.json"
    SETTINGS_PATH = Path.home() / ".whoop_sdk" / "settings.json"

    def __init__(self):
        self.settings = self._load_settings()

        # Prefer environment variables, then fallback to local settings file
        self.client_id = os.getenv("WHOOP_CLIENT_ID") or self.settings.get("client_id")
        self.client_secret = os.getenv("WHOOP_CLIENT_SECRET") or self.settings.get("client_secret")
        self.redirect_uri = self.settings.get("redirect_uri") or "https://www.google.com"

        # If nothing found, prompt the user interactively (first run)
        if not self.client_id or not self.client_secret:
            print("🔧 WHOOP SDK setup required.")
            self.client_id = input("Enter your WHOOP Client ID: ").strip()
            self.client_secret = input("Enter your WHOOP Client Secret: ").strip()
            self.redirect_uri = input("Redirect URI [https://www.google.com]: ").strip() or "https://www.google.com"
            self._save_settings({
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
            })
            print(f"✅ Credentials saved to {self.SETTINGS_PATH}")

        self.scopes = "offline read:profile read:recovery read:sleep read:workout"
        self.state = "whoop_sdk_state_12345"
        self.tokens = self._load_tokens()

    # ---------- Public Methods ----------

    def login(self):
        """Perform one-time OAuth login."""
        print("🌐 Opening WHOOP authorization page in your browser...")
        url = self._build_auth_url()
        webbrowser.open(url)

        print("\nOnce you approve access, you’ll be redirected to:")
        print("   → https://www.google.com/?code=XXXX&state=whoop_sdk_state_12345")
        code = input("\n🔑 Paste the code from that URL: ").strip()

        tokens = self._exchange_code_for_tokens(code)
        self._save_tokens(tokens)
        print("\n✅ WHOOP SDK is now authorized and ready to use!")
        return tokens

    def ensure_access_token(self):
        """Return valid access token (auto-refresh if needed)."""
        if not self.tokens:
            raise RuntimeError("No tokens found. Run Whoop(login=True) first.")
        return self.tokens.get("access_token") or self.refresh_access_token()

    def refresh_access_token(self):
        """Use the stored refresh token to get a new access token."""
        print("🔄 Refreshing access token...")
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.tokens["refresh_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        resp = requests.post(self.TOKEN_URL, data=data)
        resp.raise_for_status()
        new_tokens = resp.json()
        self.tokens.update(new_tokens)
        self._save_tokens(self.tokens)
        print("✅ Access token refreshed.")
        return self.tokens["access_token"]

    # ---------- Internal Helpers ----------

    def _build_auth_url(self):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scopes,
            "state": self.state,
        }
        return f"{self.AUTH_URL}?{urllib.parse.urlencode(params)}"

    def _exchange_code_for_tokens(self, code: str):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        resp = requests.post(self.TOKEN_URL, data=data)
        resp.raise_for_status()
        return resp.json()

    def _save_tokens(self, tokens):
        self.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_PATH, "w") as f:
            json.dump(tokens, f, indent=2)
        self.tokens = tokens

    def _load_tokens(self):
        if self.CONFIG_PATH.exists():
            with open(self.CONFIG_PATH) as f:
                return json.load(f)
        return {}

    def _load_settings(self):
        if self.SETTINGS_PATH.exists():
            with open(self.SETTINGS_PATH) as f:
                return json.load(f)
        return {}

    def _save_settings(self, data):
        self.SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(self.SETTINGS_PATH, "w") as f:
            json.dump(data, f, indent=2)
