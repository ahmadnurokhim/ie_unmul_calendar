from __future__ import print_function
from datetime import datetime, timezone, timedelta
import pytz
import os.path
import regex as re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
ie_cal_id = '509a74860a1ca36f02df257463e899e06cd314009c8afca8a2172a0cbe7b6780@group.calendar.google.com'

def quickstart():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def add_event(creds, event_name, date_start, date_end, location, desc):    
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': event_name,
        'location': location,
        'description': desc,
        'start': {
            'dateTime': date_start,
            'timeZone': 'Asia/Singapore',
        },
        'end': {
            'dateTime': date_end,
            'timeZone': 'Asia/Singapore',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'popup', 'minutes': 15},
            {'method': 'popup', 'minutes': 0},
            ],
        },
    }
    
    event = service.events().insert(calendarId=ie_cal_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def get_event_details(msg):
    months = {
        'januari': 1,
        'februari': 2,
        'maret': 3,
        'april': 4,
        'mei': 5,
        'juni': 6,
        'juli': 7,
        'agustus': 8,
        'september': 9,
        'oktober': 10,
        'november': 11,
        'desember': 12
    }
    event_abbr = {
        'SEMINAR PROPOSAL SKRIPSI': 'Sempro',
        'SEMINAR PROPOSAL': 'Sempro',
        'SEMINAR HASIL SKRIPSI': 'Semhas',
        'SEMINAR HASIL PENELITIAN': 'Semhas',
        'SEMINAR HASIL': 'Semhas',
        'SIDANG SKRIPSI': 'Sidang',
        'SIDANG': 'Sidang'
    }

    pattern = r"[\W ]{1,5}\[?([A-Z ]*)\]?\n*([\w ]*)\n*([\d]*)\n*[\w\,']*\s([\d]{1,2}) ([\w]*) ([\d]{2,4})\n*(\d{1,2}).(\d{1,2})[\-– ]*(\d{1,2}).(\d{1,2})[\w ]*\n[dD]i ([\w \.\,]*)\n*([\w \(\:\.\\,)-]*)"
    result = re.findall(pattern, msg)[0]
    event_name = f"{event_abbr[result[0]]} {result[1]} ({result[2]})"
    date_start = datetime(int(result[5]), months[result[4].lower()], int(result[3]), int(result[6]), int(result[7]), tzinfo=timezone(timedelta(hours=8))).isoformat()
    date_end = datetime(int(result[5]), months[result[4].lower()], int(result[3]), int(result[8]), int(result[9]), tzinfo=timezone(timedelta(hours=8))).isoformat()
    location = result[10]
    desc = result[11]
    return event_name, date_start, date_end, location, desc

def get_today_event(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        print('Getting the upcoming 10 events')
        events_result = service.events().list(
            calendarId=ie_cal_id, timeMin=datetime.today().replace(hour=0, minute=0, second=0) .astimezone(tz=pytz.UTC).isoformat(),
            timeMax=datetime.today().replace(hour=23, minute=59, second=59).astimezone(tz=pytz.UTC).isoformat(),
            singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        events_text = ""
        for event in events:
            start_time = datetime.strftime(datetime.fromisoformat(event['start']['dateTime']), "%a, %d %b %Y (%H.%M")
            end_time = datetime.strftime(datetime.fromisoformat(event['end']['dateTime']), "-%H.%M)")
            events_text = events_text + "\n" + start_time + end_time + event['summary']
        print(events_text)

    except HttpError as error:
        print('An error occurred: %s' % error)

def get_today_event(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        print('Getting the upcoming 10 events')
        events_result = service.events().list(
            calendarId=ie_cal_id, timeMin=datetime.today().replace(hour=0, minute=0, second=0) .astimezone(tz=pytz.UTC).isoformat(),
            timeMax=datetime.today().replace(hour=23, minute=59, second=59).astimezone(tz=pytz.UTC).isoformat(),
            singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        events_text = ""
        for event in events:
            start_time = datetime.strftime(datetime.fromisoformat(event['start']['dateTime']), "%H.%M")
            end_time = datetime.strftime(datetime.fromisoformat(event['end']['dateTime']), "-%H.%M")
            events_text = events_text + "\n" + start_time + end_time + event['summary']
        print(events_text)

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    creds = quickstart()
    
    # Get the event details
    event_name, date_start, date_end, location, desc = get_event_details()
    
    # Try to add event
    try:
        add_event(creds, event_name, date_start, date_end, location, desc)
    except Exception as e:
        print('Add event error')
        print(e)