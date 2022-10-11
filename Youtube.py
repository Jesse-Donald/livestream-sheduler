
from google_auth_oauthlib.flow import InstalledAppFlow
def generate_authorized_user_file():
    """
    Run the authentication flow and save the token (refresh token) for future refreshes
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json",
        scopes=[
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.force-ssl",
            "https://www.googleapis.com/auth/youtube.upload",
        ],
    )
    credentials = flow.run_console()
    with open("token.json", "w", encoding="UTF-8") as token_file:
        token_file.write(credentials.to_json())
    return credentials

generate_authorized_user_file()