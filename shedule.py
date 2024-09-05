import google
import google.auth.transport.requests
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from planningCenter import getNames
from getThumb import generateThumb
from datetime import datetime
import pytz
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from embeddify import Embedder
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def adding_text(img, text, position, size, colour, font):
	 font = ImageFont.truetype(font, size)
	 W, H = position
	 draw = ImageDraw.Draw(img)
	 _, _, w, h = draw.textbbox((0, 0), text, font=font)
	 draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=colour)
	 return img

def send(to_number, err):
        # Replace the number with your own, or consider using an argument\dict for multiple people.
    auth = ('castlehillsda@gmail.com', 'pdmzliicvmqzgiuq')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])
#    msg = EmailMessage()
    msg = MIMEMultipart('alternative')
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<!--[if gte mso 9]>
<xml>
<o:OfficeDocumentSettings>
<o:AllowPNG/>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
<![endif]-->
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="x-apple-disable-message-reformatting">
<!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
<title></title>

<style type="text/css">
  @media only screen and (min-width: 620px) {
.u-row {
width: 600px !important;
}
.u-row .u-col {
vertical-align: top;
}

.u-row .u-col-100 {
width: 600px !important;
}

}

@media (max-width: 620px) {
.u-row-container {
max-width: 100% !important;
padding-left: 0px !important;
padding-right: 0px !important;
}
.u-row .u-col {
min-width: 320px !important;
max-width: 100% !important;
display: block !important;
}
.u-row {
width: 100% !important;
}
.u-col {
width: 100% !important;
}
.u-col > div {
margin: 0 auto;
}
}
body {
margin: 0;
padding: 0;
}

table,
tr,
td {
vertical-align: top;
border-collapse: collapse;
}

p {
margin: 0;
}

.ie-container table,
.mso-container table {
table-layout: fixed;
}

* {
line-height: inherit;
}

a[x-apple-data-detectors='true'] {
color: inherit !important;
text-decoration: none !important;
}

table, td { color: #000000; } #u_body a { color: #123ce6; text-decoration: underline; } @media (max-width: 480px) { #u_content_heading_1 .v-container-padding-padding { padding: 30px 10px !important; } #u_content_heading_1 .v-font-size { font-size: 35px !important; } #u_content_heading_4 .v-font-size { font-size: 19px !important; } #u_content_image_3 .v-src-width { width: 100% !important; } #u_content_image_3 .v-src-max-width { max-width: 100% !important; } #u_content_button_1 .v-size-width { width: 60% !important; } #u_row_6 .v-row-background-color { background-color: #ffffff !important; } #u_row_6.v-row-background-color { background-color: #ffffff !important; } }
</style>



<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Rubik:400,700&display=swap" rel="stylesheet" type="text/css"><!--<![endif]-->

</head>

<body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">
<!--[if IE]><div class="ie-container"><![endif]-->
<!--[if mso]><div class="mso-container"><![endif]-->
<table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0">
<tbody>
<tr style="vertical-align: top">
<td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #e7e7e7;"><![endif]-->



<div class="u-row-container v-row-background-color" style="padding: 0px;background-color: #ced4d9">
<div class="u-row" style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
  <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: #ced4d9;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
  
<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
<div style="height: 100%;width: 100% !important;">
<!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->

<table id="u_content_heading_1" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
<tbody>
<tr>
  <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:60px 10px;font-family:'Open Sans',sans-serif;" align="left">
    
<h1 class="v-font-size" style="margin: 0px; color: #34495e; line-height: 110%; text-align: center; word-wrap: break-word; font-family: 'Rubik',sans-serif; font-size: 45px; font-weight: 400;"><div>
<div>
<div>
<div>
<div>
<div>
<div>
<div>
<div>
<div>
<div>
<div><strong>Uh Oh!</strong></div></div></div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div></h1>

  </td>
</tr>
</tbody>
</table>

<!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
  <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>





<div class="u-row-container v-row-background-color" style="padding: 0px;background-color: #ecf0f1">
<div class="u-row" style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
  <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: #ecf0f1;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
  
<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
<div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
<!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->

<table id="u_content_heading_4" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
<tbody>
<tr>
  <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:60px 10px 0px;font-family:'Open Sans',sans-serif;" align="left">
    
<h1 class="v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-family: 'Rubik',sans-serif; font-size: 26px; font-weight: 400;">The Livestream Scheduler has encountered an error</strong></h1>

  </td>
</tr>
</tbody>
</table>

<table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
<tbody>
<tr>
  <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Open Sans',sans-serif;" align="left">
    
<div class="v-font-size" style="font-size: 14px; line-height: 140%; text-align: center; word-wrap: break-word;">
<p style="font-size: 14px; line-height: 140%;">""" + err + """</p>
</div>

  </td>
</tr>
</tbody>
</table>

<table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
<tbody>
<tr>
  <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Open Sans',sans-serif;" align="left">
    
<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td style="padding-right: 0px;padding-left: 0px;" align="center">
  
  <!--img align="center" border="0" src="images/image-2.png" alt="Logo" title="Logo" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 4%;max-width: 23.2px;" width="23.2" class="v-src-width v-src-max-width"/-->
  
</td>
</tr>
</table>

  </td>
</tr>
</tbody>
</table>

<table id="u_content_image_3" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
<tbody>
<tr>
  <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px 10px;font-family:'Open Sans',sans-serif;" align="left">
    
<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr>
<td style="padding-right: 0px;padding-left: 0px;" align="center">
  
  <img align="center" border="0" src="https://img.freepik.com/premium-vector/window-operating-system-error-warning-dialog-window-popup-message-with-system-failure-flat-design_812892-54.jpg" alt="Logo" title="Logo" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 580px;" width="580" class="v-src-width v-src-max-width"/>
  
</td>
</tr>
</table>

  </td>
</tr>
</tbody>
</table>

<!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
  <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>





<div id="u_row_6" class="u-row-container v-row-background-color" style="padding: 0px;background-color: #ecf0f1">
<div class="u-row" style="margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
<div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
  <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: #ecf0f1;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: transparent;"><![endif]-->
  
<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
<div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
<!--[if (!mso)&(!IE)]><!--><div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->

<table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
<tbody>
<tr>
  <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px 10px 40px;font-family:'Open Sans',sans-serif;" align="left">
    
<div class="v-font-size" style="font-size: 14px; line-height: 140%; text-align: center; word-wrap: break-word;">
<p style="font-size: 14px; line-height: 140%;">© Castle Hill Seventh Day Adventist Church</p>
</div>

  </td>
</tr>
</tbody>
</table>

<!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
</div>
</div>
<!--[if (mso)|(IE)]></td><![endif]-->
  <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
</div>
</div>
</div>



<!--[if (mso)|(IE)]></td></tr></table><![endif]-->
</td>
</tr>
</tbody>
</table>
<!--[if mso]></div><![endif]-->
<!--[if IE]></div><![endif]-->
</body>

</html>
        """
    msg['From'] = 'castlehillsda@gmail.com'
    msg['To'] = to_number
    msg['Subject'] = 'Livestream Sheduler Error'
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    print(msg)
    # Send text message through SMS gateway of destination number
 #   server.sendmail('castlehillsda@gmail.com',to_number, msg.as_string())
#    print('HIIIIIIIi')


name, sermonTitle, theme = getNames()

#raw_image = requests.get('https://source.unsplash.com/1280x720/?landscape').content
#img = Image.open(BytesIO(raw_image)).convert('RGBA')
#template_image=Image.open('thumb-template.png').convert('RGBA')
#dark = Image.new(mode="RGBA", size=(1280, 720), color=(0, 0, 0, 50))
#generated = Image.alpha_composite(img, dark)
#generated = Image.alpha_composite(generated, template_image)
#generated = adding_text(generated, "CASTLE HILL SDA CHURCH", (1280, 500), 30, (255, 255, 255), 'Montserrat/static/Montserrat-Regular.ttf')
#generated = adding_text(generated, '"' + sermonTitle + '"', (1280, 720), 65, (255, 255, 255), 'Aleo/Aleo-Regular.ttf')
#generated = adding_text(generated, name, (1280, 900), 30, (255, 255, 255), 'Montserrat/static/Montserrat-Regular.ttf')
#imgpath = generated.save('thumb.png')

localStartTime = datetime.strptime(datetime.strftime(datetime.now(), "%Y-%W") + '-6 10:45:00', "%Y-%W-%w %H:%M:%S")
utcStartTime = pytz.timezone("Australia/Sydney").localize(localStartTime, is_dst=None).astimezone(pytz.utc)
print("Sheduling Livestream for: " + localStartTime.strftime("%d %B %Y"))

imgpath = generateThumb()

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
		"privacyStatus": "unlisted",
		"selfDeclaredMadeForKids": False,
	 },
	 "contentDetails": {
	 	"latencyPreference": "low"
	 }
}



try:
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
except Exception as err:
	print(err)
	#send('jesse.donald@gmail.com', str(err))
	#send('cyclooctane@gmail.com', str(err))
with open('videoid.txt', 'w') as id:
	id.write(response['id'])
	url = '?id=' + response['id'] + 'title=' + '"' + sermonTitle + '"' + '-' + name + '&start=' + localStartTime.isoformat()
r=requests.get('https://tools.castlehillchurch.org.au/livestreamsheduler/add-event/' + url)
 
