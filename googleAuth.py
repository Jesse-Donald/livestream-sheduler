import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from getConfig import *
import shedule

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


def refresh_credentials():
    """Loads saved token.json and refreshes it automatically if expired."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
        return creds

    return None


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

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(TOKEN_PATH, "w") as token:
        token.write(credentials.to_json())

    writeConfig("Status", "Ready")

    localStartTime, utcStartTime, name, sermonTitle, theme = shedule.generateImage(credentials)
    shedule.generateStream(localStartTime, utcStartTime, name, sermonTitle, theme, credentials)

    return credentials
