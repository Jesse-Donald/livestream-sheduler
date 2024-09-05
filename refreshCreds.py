from google_auth_oauthlib.flow import InstalledAppFlow
import google
import google.auth.transport.requests
import requests
from google.oauth2.credentials import Credentials
import os

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
	
	
refresh_credentials()
