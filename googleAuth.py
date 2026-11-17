import google
import google.auth.transport.requests
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from getConfig import *

def refresh_credentials():
	request = google.auth.transport.requests.Request()
	SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube.upload']
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	if True: #not creds or not creds.valid:
		if False: # creds and creds.expired and creds.refresh_token:
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

def getAuthURL():
	SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube.upload']
	flow = InstalledAppFlow.from_client_secrets_file(
		'credentials.json', SCOPES, redirect_uri='https://coffee.castlehilladventist.church/stream/auth_return')
	url = flow.authorization_url(prompt='consent')
	return url[0]

def authWithCode(code):
	SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube.upload']
	flow = InstalledAppFlow.from_client_secrets_file(
		'credentials.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
	creds = flow.fetch_token(code=code)
	with open('token.json', 'w') as token:
				token.write(flow.credentials.to_json())
	writeConfig('Status','Ready')

def auth_creds_return(request):
#       token = Flow.fetch_token(code=request.GET['code'])
        CLIENT_SECRETS_FILENAME = 'credentials.json'
        SCOPES=['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube,upload']
        flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME, scopes=SCOPES, state=request.GET['state'])
        flow.redirect_uri='https://coffee.castlehilladventist.church/stream/auth_return'
        state = request.GET['state']
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.build_absolute_uri()
        if "http:" in authorization_response:
                authorization_response  = "https:" + authorization_response[5:]
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
        localStartTime, utcStartTime, name, sermonTitle, theme = shedule.generateImage(credentials)
        shedule.generateStream(localStartTime, utcStartTime, name, sermonTitle, theme, credentials)
    # Store the credentials in the session.
#go     credentials = flow.credentials
        test = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
        return
