import google
import google.auth.transport.requests

import os
import google.oauth2.credentials
from googleapiclient.discovery import build

# Set your API key or OAuth credentials file path
API_KEY = "YOUR_API_KEY"
CLIENT_SECRETS_FILE = "client_secrets.json"  # Path to your client secrets JSON file
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    credentials = None
    if os.path.exists("token.json"):
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file("token.json", SCOPES)

    if not credentials or not credentials.valid:
        if False: #credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google.auth.OAuth2WebServerFlow(
                client_secrets_file=CLIENT_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            )
            auth_url, _ = flow.authorization_url(access_type="offline")
            print("Please visit this URL to authorize the application:", auth_url)
            code = input("Enter the authorization code: ")
            credentials = flow.fetch_token(authorization_response=code)

            with open("token.json", "w") as token_file:
                token_file.write(credentials.to_json())

    return build("youtube", "v3", credentials=credentials)



def get_most_recent_unlisted_video_id(youtube, channel_id):
    with open('videoid.txt') as f:
        contents = f.read()
        f.close()
    return contents
#    response = youtube.search().list(
#         part="snippet",
#         forMine=True,
#         maxResults=1,
#         type="stream",
#        part="id",
#        channelId=channel_id,
#        maxResults=1,
#         order="date",
#        type="video",
#        forMine="true",
#        videoSyndicated="true",
#        videoType="unlisted",
#    ).execute()

    if "items" in response:
        print(response)
        return response["items"][0]["id"]["videoId"]
    else:
        return None


def update_video_privacy(youtube, video_id):
    youtube.videos().update(
        part="status",
        body={
            "id": video_id,
            "status": {
                "privacyStatus": "public"
            }
        }
    ).execute()

def main():
    youtube = get_authenticated_service()
    channel_id = "UCAPsJAqTs3y5a1sogz4BVdw"
    video_id = get_most_recent_unlisted_video_id(youtube, channel_id)
    update_video_privacy(youtube, video_id)
    print(video_id)
    print("Video privacy status updated to public.")

if __name__ == "__main__":
    main()
