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

def getAuthURL():
	SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube.upload']
	flow = InstalledAppFlow.from_client_secrets_file(
		'credentials.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
	url = flow.authorization_url(prompt='consent')
	return url

def authWithCode(code):
	SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube.upload']
	flow = InstalledAppFlow.from_client_secrets_file(
		'credentials.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
	creds = flow.fetch_token(code=code)
	with open('token.json', 'w') as token:
				token.write(flow.credentials.to_json())
	writeConfig('Status','Ready')
