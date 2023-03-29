from __future__ import print_function

import datetime, re
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calendar_event():
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
                'Key\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)  # 'Z' indicates UTC time
        tomorrow = (today + datetime.timedelta(days=1)).isoformat() + 'Z'
        after_week = (today + datetime.timedelta(days=8)).isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=tomorrow,
            timeMax=after_week,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        # for event in events:
            # start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])
        formatted_events = [(event['start'].get('dateTime', event['start'].get('date')),  # start time or day
                             event['end'].get('dateTime', event['end'].get('date')),  # end time or day
                             event['summary']) for event in events]
        len_event = len(formatted_events)
        response = f'[1週間のイベント{len_event}件]\n'
        # データの正規化をする
        for event in formatted_events:
            if re.match(r'^\d{4}-\d{2}-\d{2}$', event[0]):
                start_date = '{0:%Y-%m-%d}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%d'))
                response += '{0} All Day\n{1}\n\n'.format(start_date, event[2])
            # For all day events
            else:
                start_time = '{0:%Y-%m-%d %H:%M}'.format(
                    datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00'))
                end_time = '{0:%H:%M}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S+09:00'))
                response += '{0} ~ {1}\n{2}\n\n'.format(start_time, end_time, event[2])
        response = response.rstrip('\n')
        print(response)

        return formatted_events

    except HttpError as error:
        print('An error occurred: %s' % error)
        return []

