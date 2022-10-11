import google
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
from Buletin2Youtube import getNames
from datetime import datetime
import pytz
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from unsplash.api import Api
from unsplash.auth import Auth

def adding_text(img, text, position, size, colour, font):
    font = ImageFont.truetype(font, size)
    W, H = position
    draw = ImageDraw.Draw(img)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=colour)
    return img
    
name, sermonTitle = getNames()

raw_image = requests.get('https://source.unsplash.com/1280x720/?landscape').content
img = Image.open(BytesIO(raw_image)).convert('RGBA')
template_image=Image.open('thumb-template.png').convert('RGBA')
generated = Image.alpha_composite(img, template_image)
generated = adding_text(generated, "CASTLE HILL SDA CHURCH", (1280, 500), 30, (255, 255, 255), 'Montserrat/static/Montserrat-Regular.ttf')
generated = adding_text(generated, '"' + sermonTitle + '"', (1280, 720), 65, (255, 255, 255), 'Aleo/Aleo-Regular.ttf')
generated = adding_text(generated, name, (1280, 900), 30, (255, 255, 255), 'Montserrat/static/Montserrat-Regular.ttf')
imgpath = generated.save('thumb.png')

localStartTime = datetime.strptime(datetime.strftime(datetime.now(), "%Y-%W") + '-6 10:45:00', "%Y-%W-%w %H:%M:%S")
utcStartTime = pytz.timezone("Australia/Sydney").localize(localStartTime, is_dst=None).astimezone(pytz.utc)
print("Sheduling Livestream for: " + localStartTime.strftime("%d %B %Y"))



def refresh_credentials():
    """
    Returns current credentials from saved refresh token
    """
    credentials = Credentials.from_authorized_user_file("token.json")
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials
    
from googleapiclient.discovery import build
livestream_details = {
    "snippet": {
        "title": '"' + sermonTitle + '" - ' + name,
        "scheduledStartTime": utcStartTime.isoformat(),
        "categoryId": 44,
        "description": localStartTime.strftime("%d %B %Y"),
        "thumbnails": {
        	"default": {
        		"url": "https://res-2.cloudinary.com/amn/image/upload/c_fill,h_400,w_712/v1646104307/adventistplace/thumbnail_image0_1_iogszh.jpg",
        		"width": 712,
        		"height": 400,
        	}
        },
    },
    "status": {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": False,
    },
    "contentDetails": {
    	"latencyPreference": "low"
    }
}

print("Building Stream...")
api = build("youtube", "v3", credentials=refresh_credentials())
response = api.liveBroadcasts().insert(
    part="snippet,status,contentDetails",
    body=livestream_details,
).execute()

response['snippet']['categoryId'] = '29'

print("Updating Categories...")

updated = api.videos().update(
	part="snippet",
	body={
	"id": response['id'],
	"snippet": response['snippet'],
	}
).execute()

print("Setting Thumbnail...")

thumbnail = api.thumbnails().set(
	videoId = response['id'],
	media_body=MediaFileUpload('thumb.png')
).execute()

print("Done!")