from __future__ import print_function

import datetime, re
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from line_global import schedule_start, schedule_end

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleAPIManager():

    def __init__(self, logger):

        self.logger = logger


def get_calendar_event(start_status, end_status):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    events_list = []

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'Key\\credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    else:
        raise FileNotFoundError

    try:
        service = build('calendar', 'v3', credentials=creds)

        # 基準のdatetimeを取得(時間・分・秒・マイクロ秒を0にする)
        today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)  # 'Z' indicates UTC time

        # 取得するスケジュールの開始と終了
        if (start_status == schedule_start.TODAY):
            start = (today + datetime.timedelta(days=0)).isoformat() + 'Z'
        if (start_status == schedule_start.TOMORROW):
            start = (today + datetime.timedelta(days=1)).isoformat() + 'Z'
        if (end_status == schedule_end.ONE_DAY):
            end = (today + datetime.timedelta(days=2)).isoformat() + 'Z'
        if (end_status == schedule_end.WEEKLY):
            end = (today + datetime.timedelta(days=8)).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary',
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        # events.keys()
        # 'kind',       calendar#event
        # 'etag',       "3425504655088000"
        # 'id',         57tvj2vnkgqgk6odsgflgjaesc
        # 'status',     confirmed
        # 'htmlLink',   https://www.google.com/calendar/event?eid=NTd0dmoydm5rZ3FnazZvZHNnZmxnamFlc2MgYXlhbm91ZS4wMzI1LmFuZG9yYUBt
        # 'created',    2024-04-07T06:40:06.000Z
        # 'updated',    2024-04-10T12:32:07.544Z
        # 'summary',    on schedule
        # 'creator',    {'email': 'ayanoue.0325.andora@gmail.com', 'self': True}
        # 'organizer',  {'email': 'ayanoue.0325.andora@gmail.com', 'self': True}
        # 'start',      {'dateTime': '2024-04-10T08:30:00+09:00', 'timeZone': 'Asia/Tokyo'}
        #  'end',       {'dateTime': '2024-04-10T09:30:00+09:00', 'timeZone': 'Asia/Tokyo'}
        #  'iCalUID',   57tvj2vnkgqgk6odsgflgjaesc@google.com
        #  'sequence',  2
        #  'reminders', {'useDefault': True}
        #  'eventType'  default

        if not events:
            print('No upcoming events found.')
            return 0

        len_event = len(events)
        print(f'[イベント{len_event}件]')

        # データの正規化をする
        for event in events:

            dt = event['start']['dateTime']

            schedule_dict = {
                "date": "%Y-%m-%d",
                "all_day": "True",
                "start_time": "$start_time",
                "end_time": "$end_time",
                "summary": "$summary",
                "description": "$description",
                "colorId": "$colorId"
            }

            if re.match(r'^\d{4}-\d{2}-\d{2}$', dt):
                # all day

                schedule_dict["date"] = '{0:%m月%d日}'.format(
                    datetime.datetime.strptime(event['start'].get('dateTime'), '%Y-%m-%d'))
                schedule_dict["all_day"] = "True"
                schedule_dict["start_time"] = '{0:%m月%d日}'.format(
                    datetime.datetime.strptime(event['start'].get('dateTime'), '%Y-%m-%d'))
                schedule_dict["end_time"] = '{0:%m月%d日}'.format(
                    datetime.datetime.strptime(event['end'].get('dateTime'), '%Y-%m-%d'))
                schedule_dict["summary"] = event['summary']

                schedule_dict['description'] = event['description'] if 'description' in event else "-"
                schedule_dict['colorId'] = event['colorId'] if 'colorId' in event else "-"

            else:
                # schedule

                schedule_dict["date"] = '{0:%m月%d日}'.format(
                    datetime.datetime.strptime(event['start'].get('dateTime'), '%Y-%m-%dT%H:%M:%S+09:00'))
                schedule_dict["all_day"] = "False"
                schedule_dict["start_time"] = '{0:%H:%M}'.format(
                    datetime.datetime.strptime(event['start'].get('dateTime'), '%Y-%m-%dT%H:%M:%S+09:00'))
                schedule_dict["end_time"] = '{0:%H:%M}'.format(
                    datetime.datetime.strptime(event['end'].get('dateTime'), '%Y-%m-%dT%H:%M:%S+09:00'))
                schedule_dict["summary"] = event['summary']

                schedule_dict['description'] = event['description'] if 'description' in event else "-"
                schedule_dict['colorId'] = event['colorId'] if 'colorId' in event else "-"

            events_list.append(schedule_dict)

        print(events_list)

        return events_list

    except HttpError as error:
        print('An error occurred: %s' % error)
        return []

