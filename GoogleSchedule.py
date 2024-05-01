from __future__ import print_function

import datetime, re
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from common_global import *
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_event(start_status, end_status):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    events_list = {}
    schedule_list = []
    schedule_list_days = []
    start_date = None
    end_date = None

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

        # 取得するスケジュールの開始
        if start_status == schedule_start.TODAY:
            start_date = today + datetime.timedelta(days=0)
        elif start_status == schedule_start.TOMORROW:
            start_date = today + datetime.timedelta(days=1)
        else:
            start_date = today + datetime.timedelta(days=0)
        # 取得するスケジュールの終了時間
        if end_status == schedule_end.ONE_DAY:
            end_date = start_date + datetime.timedelta(days=1)
        elif end_status == schedule_end.WEEKLY:
            end_date = start_date + datetime.timedelta(days=7)
        else:
            end_date = start_date + datetime.timedelta(days=1)

        if start_date > end_date:
            logger.warning("Setting value of getting date is not right")
            return -1

        events_list.update(start_date=start_date)
        events_list.update(end_date=end_date)

        schedule_date = start_date
        start = start_date.isoformat() + 'Z'
        end = end_date.isoformat() + 'Z'

        logger.debug(f'Start_time of getting user schedule: {start}')
        logger.debug(f'End_time of getting user schedule: {end}')

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
            logger.info('No upcoming events found.')
            return 0

        len_event = len(events)
        logger.info(f'Number getting event: {len_event}')
        events_list.update(len_event=len_event)

        # スケジュールのステータスチェック
        for event in events:
            dt = event['start'].get('dateTime', event['start'].get('date'))
            if dt == None:
                logger.warning("Event does not include \"start_dateTime\"")
                return 0


        # データの正規化をする
        while (end_date != schedule_date):

            schedule_list_days = []

            for event in events:

                schedule_dict = {
                    "date": "%Y-%m-%d",
                    "all_day": "True",
                    "start_time": "$start_time",
                    "end_time": "$end_time",
                    "summary": "$summary",
                    "description": "$description",
                    "colorId": "$colorId"
                }

                dt = event['start'].get('dateTime', event['start'].get('date'))

                if schedule_date.strftime("%Y-%m-%d") == dt.split("T")[0]:

                    if re.match(r'^\d{4}-\d{2}-\d{2}$', dt):
                        # all day

                        schedule_dict["date"] = '{0:%m月%d日}'.format(
                            datetime.datetime.strptime(event['start'].get('date'), '%Y-%m-%d'))
                        schedule_dict["all_day"] = "True"
                        schedule_dict["start_time"] = '{0:%m月%d日}'.format(
                            datetime.datetime.strptime(event['start'].get('date'), '%Y-%m-%d'))
                        schedule_dict["end_time"] = '{0:%m月%d日}'.format(
                            datetime.datetime.strptime(event['end'].get('date'), '%Y-%m-%d'))
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

                    print(schedule_dict)
                    schedule_list_days.append(schedule_dict)

            schedule_date += datetime.timedelta(days=1)

            schedule_list.append(schedule_list_days)

        events_list.update(schedule_list=schedule_list)
        logger.info(events_list)

        return events_list

    except HttpError as error:
        logger.warning('An error occurred: %s' % error)
        return []

