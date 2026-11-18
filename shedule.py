'''--------------IMPORT SECTION-------------'''
#External Modules
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

#Internal Modues

from planningCenter import getNames
from getThumb import generateThumb
from getConfig import getConfig, writeConfig
from googleAuth import refresh_credentials
import errorManager

'''--------------Script Start-------------'''
def createStream():
	global livestream_details
#	name, sermonTitle, theme = getNames()
	theme = ''

#Call to generate a thumbnail for the stream

	imgpath = generateThumb()

#Generate the time string

	writeConfig('Status', 'Scheduling')
	config = getConfig()

	localStartTime = datetime.strptime(datetime.strftime(datetime.now(), "%Y-%W") + '-6 10:45:00', "%Y-%W-%w %H:%M:%S")
	utcStartTime = pytz.timezone("Australia/Sydney").localize(localStartTime, is_dst=None).astimezone(pytz.utc)
	print("Sheduling Livestream for: " + localStartTime.strftime("%d %B %Y"))

# Build Livestream Object
	try:
		livestream_details = {
			 "snippet": {
				"title": '"' + config['SermonTitle'] + '" - ' + config['Preacher'],
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
				"privacyStatus": "public",
				"selfDeclaredMadeForKids": False,
			 },
			 "contentDetails": {
			 	"latencyPreference": "low"
			 }
		}
	        #Create stream entity using the youtube data API
	
		print("Building Stream...")
		creds = refresh_credentials()
		if creds is None:
			raise RuntimeError(
				"Google credentials are missing or expired. Use Get Auth URL to sign in again."
			)
		api = build("youtube", "v3", credentials=creds)

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

		writeConfig('Status', 'Done')

	#Error Handling

	except Exception as err:
		print(err)
		errorManager.save(str(err))
 
