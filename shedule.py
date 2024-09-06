'''--------------IMPORT SECTION-------------'''
#External Modules
import google
import google.auth.transport.requests
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime
import pytz
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

#Internal Modues

from planningCenter import getNames
from getThumb import generateThumb
from getConfig import getConfig
import errorManager

'''--------------Script Methods-------------'''

def refresh_credentials():
	request = google.auth.transport.requests.Request()
	SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube.upload']
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
				creds.refresh(google.auth.transport.requests.Request())
		else:
				flow = InstalledAppFlow.from_client_secrets_file(
					 'credentials.json', SCOPES)
				creds = flow.run_console(port=0)
				print(creds)
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
				token.write(creds.to_json())
	return creds

'''--------------Script Start-------------'''

#Get details for the stream

name, sermonTitle, theme = getNames()

#Call to generate a thumbnail for the stream

imgpath = generateThumb()

#Generate the time string

localStartTime = datetime.strptime(datetime.strftime(datetime.now(), "%Y-%W") + '-6 10:45:00', "%Y-%W-%w %H:%M:%S")
utcStartTime = pytz.timezone("Australia/Sydney").localize(localStartTime, is_dst=None).astimezone(pytz.utc)
print("Sheduling Livestream for: " + localStartTime.strftime("%d %B %Y"))

# Build Livestream Object
	 
livestream_details = {
	 "snippet": {
		"title": '"' + sermonTitle + '" - ' + name,
		"scheduledStartTime": utcStartTime.isoformat(),
		"categoryId": 44,
		"description": localStartTime.strftime("%d %B %Y"),
		"thumbnails": {
			"default": {
				"url": "https://content.api.news/v3/images/bin/07bf526aa6a349ec035ea815c2142944",
				"width": 712,
				"height": 400,
			}
		},
	 },
	 "status": {
		"privacyStatus": "unlisted",
		"selfDeclaredMadeForKids": False,
	 },
	 "contentDetails": {
	 	"latencyPreference": "low"
	 }
}

#Start Error Handling

try:
        #Create stream entity using the youtube data API
        
	print("Building Stream...")
	api = build("youtube", "v3", credentials=refresh_credentials())
	
	request = api.playlists().list(
			part="snippet,contentDetails",
			maxResults=25,
			mine=True
		 ).execute()
	
	response = api.liveBroadcasts().insert(
		 part="snippet,status,contentDetails",
		 body=livestream_details,
	).execute()

	#Update the stream category as this cannot be done during the initial stream creation
	
	response['snippet']['categoryId'] = '29'
	
	print("Updating Categories...")
	
	updated = api.videos().update(
		part="snippet",
		body={
		"id": response['id'],
		"snippet": response['snippet'],
		}
	).execute()

        #Update the stream entity to include the generated thumbnail
	
	print("Setting Thumbnail...")
	
	thumbnail = api.thumbnails().set(
		videoId = response['id'],
		media_body=MediaFileUpload('thumb.png')
	).execute()

	#Add the stream to the required playlists ("Church Services {year}","Church Services (Recent)" and Theme as in Planning Center
	
	print("Adding to Playlists...")
	
	for i in request['items']:
		if i['snippet']['title'].split(' — ')[0] == theme.split('\n')[0]:
		 	print(theme.split('\n')[0])
		 	addplaylist = api.playlistItems().insert(
		 		part = "snippet",
		 		body={
	          "snippet": {
	            "playlistId": i['id'],
	            "resourceId": {
	            "kind": "youtube#video",
	              "videoId": response['id']
	            }
	          }
	        }
			).execute()
		if i['snippet']['title'] == 'Church Services ' + datetime.now().strftime("%Y"):
			addplaylist = api.playlistItems().insert(
		 		part = "snippet",
		 		body={
	          "snippet": {
	            "playlistId": i['id'],
	            "resourceId": {
	            "kind": "youtube#video",
	              "videoId": response['id']
	            }
	          }
	        }
			).execute()
		if i['snippet']['title'] == 'Church Services (recent)':
			addplaylist = api.playlistItems().insert(
		 		part = "snippet",
		 		body={
	          "snippet": {
	            "playlistId": i['id'],
	            "resourceId": {
	            "kind": "youtube#video",
	              "videoId": response['id']
	            }
	          }
	        }
			).execute()
	
	print("Done!")

#Error Handling
	
except Exception as err:
	print(err)
	errorManager.send(config['ErrorEmailRecipients'], str(err))
 
