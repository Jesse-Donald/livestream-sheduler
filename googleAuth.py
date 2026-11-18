import fcntl
import json
import os
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from getConfig import *

os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/youtube.upload",
]

DATA_DIR = os.environ.get("DATA_DIR", "/app/data")
TOKEN_PATH = os.path.join(DATA_DIR, "token.json")


def _get_client_config():
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip().strip('"').strip("'")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "").strip().strip('"').strip("'")

    if not client_id or not client_secret:
        raise ValueError("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET environment variables.")

    return {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def _get_redirect_uri():
    return os.environ.get(
        "GOOGLE_REDIRECT_URI",
        "http://localhost:5000/auth_return"
    ).strip().strip('"').strip("'")


@contextmanager
def _token_lock():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, "token.lock"), "a+") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def _client_id_and_secret():
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "").strip().strip('"').strip("'")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "").strip().strip('"').strip("'")
    return client_id, client_secret


def _load_token_info():
    if not os.path.exists(TOKEN_PATH):
        return None
    with open(TOKEN_PATH, "r") as token:
        info = json.load(token)
    client_id, client_secret = _client_id_and_secret()
    if client_id:
        info["client_id"] = client_id
    if client_secret:
        info["client_secret"] = client_secret
    return info


def _save_credentials(creds, previous_refresh_token=None):
    os.makedirs(DATA_DIR, exist_ok=True)
    payload = json.loads(creds.to_json())
    refresh_token = payload.get("refresh_token") or previous_refresh_token
    if refresh_token:
        payload["refresh_token"] = refresh_token
    tmp_path = TOKEN_PATH + ".tmp"
    with open(tmp_path, "w") as token:
        json.dump(payload, token, indent=2)
        token.write("\n")
    os.replace(tmp_path, TOKEN_PATH)


def _needs_refresh(creds, force):
    if force or not creds.valid or creds.expiry is None:
        return True
    expiry = creds.expiry
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    return expiry <= datetime.now(timezone.utc) + timedelta(minutes=10)


def refresh_credentials(force=False):
    """Load token.json, refresh with Google if needed, and write back the new tokens."""
    with _token_lock():
        info = _load_token_info()
        if not info:
            return None

        creds = Credentials.from_authorized_user_info(info, SCOPES)
        previous_refresh_token = creds.refresh_token or info.get("refresh_token")
        if not previous_refresh_token:
            return None

        if not _needs_refresh(creds, force):
            return creds

        try:
            creds.refresh(Request())
        except RefreshError:
            return None

        _save_credentials(creds, previous_refresh_token=previous_refresh_token)
        return creds


def getAuthURL():
    """Generates the Google OAuth URL, state, and PKCE code_verifier."""
    flow = Flow.from_client_config(
        _get_client_config(),
        scopes=SCOPES,
        redirect_uri=_get_redirect_uri(),
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return auth_url, state, flow.code_verifier


def auth_creds_return(flask_request, state=None, code_verifier=None):
    """Handles Google's OAuth redirect, saves token.json, and schedules the stream."""
    redirect_uri = _get_redirect_uri()
    flow = Flow.from_client_config(
        _get_client_config(),
        scopes=SCOPES,
        state=state or flask_request.args.get("state"),
        redirect_uri=redirect_uri,
    )
    if code_verifier:
        flow.code_verifier = code_verifier

    query_string = flask_request.query_string.decode("utf-8")
    authorization_response = f"{redirect_uri}?{query_string}" if query_string else redirect_uri

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    with _token_lock():
        _save_credentials(credentials, previous_refresh_token=credentials.refresh_token)

    writeConfig("Status", "Ready")

    #localStartTime, utcStartTime, name, sermonTitle, theme = shedule.generateImage(credentials)
    #shedule.generateStream(localStartTime, utcStartTime, name, sermonTitle, theme, credentials)

    return credentials
