from datetime import datetime
import google.auth.transport.requests
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

matchedrow = []

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/youtube.upload']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1oggJlofC_Rdu5uLYMsqv6ZRvVv7ejGgkXroJC3rFnF0'
SAMPLE_RANGE_NAME = 'A1:AG'

def getNames():
    global matchedrow
    request = google.auth.transport.requests.Request()
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    date = datetime.strptime(datetime.strftime(datetime.now(), "%Y-%W") + '-6', "%Y-%W-%w")
    formatteddate = date.strftime("%d %b %Y")
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if False: # creds and creds.expired and creds.refresh_token:
            creds.refresh(request)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        global matchedrow
        service = build('sheets', 'v4', credentials=creds)
         # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        for row in values:
            try:
 #               print(row[2] + '  : ' + row[3] + ' : ' + row[4])
#                print(date.strftime("%d %b %Y").lstrip('0'))
                if row[0] == formatteddate:
                        matchedrow = row
            except:
                pass
    except HttpError as err:
        print(err)
#    return(matchedrow[4].split(':')[0].split('(')[0], matchedrow[3], matchedrow[2])
    return('Pr Joshua Stothers','The Shape of Faith', 'The Shape of Faith')
getNames()


