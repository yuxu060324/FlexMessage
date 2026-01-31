from __future__ import print_function

import datetime
import re
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from common_global import *

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
JST = datetime.timezone(datetime.timedelta(hours=9))

# WEEKLYを今週と来週、今からの3つ用意したいな

# Google Calendar APIの資格情報の環境変数を更新する
# credentials.to_json()の返り値が"str"型
def _update_environ_credentials(credentials: str):
	# return cls(
	#     token=info.get("token"),
	#     refresh_token=info.get("refresh_token"),
	#     token_uri=_GOOGLE_OAUTH2_TOKEN_ENDPOINT,  # always overrides
	#     scopes=scopes,
	#     client_id=info.get("client_id"),
	#     client_secret=info.get("client_secret"),
	#     quota_project_id=info.get("quota_project_id"),  # may not exist
	#     expiry=expiry,
	#     rapt_token=info.get("rapt_token"),  # may not exist
	#     trust_boundary=info.get("trust_boundary"),  # may not exist
	#     universe_domain=info.get("universe_domain"),  # may not exist
	#     account=info.get("account", ""),  # may not exist
	# )

	credentials_info = json.loads(credentials)

	for key in credentials_info.keys():
		environ_name = "GOOGLE_CALENDAR_CREDENTIALS_" + key.upper()

		if environ_name == "GOOGLE_CALENDAR_CREDENTIALS_SCOPES":
			# scopesのみリストで定義されているため
			os.environ[environ_name] = credentials_info[key][0]
		else:
			os.environ[environ_name] = credentials_info[key]

	# デバッグ用(HOME_ABSPATH/Key/token.jsonに保存)
	if os.getenv("SET_BUILD") == "LOCAL":
		logger.debug("電子情報をtoken.jsonに記載します。")
		debug_token_file_path = os.path.join(HOME_ABSPATH, "Key", "token.json")
		with open(debug_token_file_path, "w", encoding="utf-8") as token_file:
			json.dump(credentials_info, token_file, ensure_ascii=False, indent=4)

	logger.info("###### Google Calendar APIの資格情報を更新しました。 ######")


# Google Calendar APIの資格情報を取得する
def _get_credentials():
	# 環境変数の確認(credentials)
	if (
			not "GOOGLE_CALENDAR_CREDENTIALS_TOKEN" in os.environ or
			not "GOOGLE_CALENDAR_CREDENTIALS_REFRESH_TOKEN" in os.environ or
			not "GOOGLE_CALENDAR_CREDENTIALS_TOKEN_URI" in os.environ or
			not "GOOGLE_CALENDAR_CREDENTIALS_CLIENT_ID" in os.environ or
			not "GOOGLE_CALENDAR_CREDENTIALS_CLIENT_SECRET" in os.environ or
			not "GOOGLE_CALENDAR_CREDENTIALS_SCOPES" in os.environ or
			not "GOOGLE_CALENDAR_CREDENTIALS_EXPIRY" in os.environ
	):

		# 初期設定時(デバッグ)

		logger.info("電子情報が未登録、または不足しています。")

		# 環境変数の確認(credentials installed)
		if (
				not "GOOGLE_CALENDAR_INSTALL_CLIENT_ID" in os.environ or
				not "GOOGLE_CALENDAR_INSTALL_PROJECT_ID" in os.environ or
				not "GOOGLE_CALENDAR_INSTALL_AUTH_URI" in os.environ or
				not "GOOGLE_CALENDAR_INSTALL_TOKEN_URI" in os.environ or
				not "GOOGLE_CALENDAR_INSTALL_AUTH_PROVIDER" in os.environ or
				not "GOOGLE_CALENDAR_INSTALL_CLIENT_SECRET" in os.environ or
				not "GOOGLE_CALENDAR_INSTALL_REDIRECT_URIS" in os.environ
		):
			# 2種類の資格がどっちも環境変数に設定されていない場合はエラー
			raise ValueError("Token is not registered in environment variable.")

		# 資格インストール用の環境変数がある場合

		install_credentials_info = {
			"installed": {
				"client_id": os.environ["GOOGLE_CALENDAR_INSTALL_CLIENT_ID"],
				"project_id": os.environ["GOOGLE_CALENDAR_INSTALL_PROJECT_ID"],
				"auth_uri": os.environ["GOOGLE_CALENDAR_INSTALL_AUTH_URI"],
				"token_uri": os.environ["GOOGLE_CALENDAR_INSTALL_TOKEN_URI"],
				"auth_provider_x509_cert_url": os.environ["GOOGLE_CALENDAR_INSTALL_AUTH_PROVIDER"],
				"client_secret": os.environ["GOOGLE_CALENDAR_INSTALL_CLIENT_SECRET"],
				"redirect_uris": [os.environ["GOOGLE_CALENDAR_INSTALL_REDIRECT_URIS"]]
			}
		}

		try:
			flow = InstalledAppFlow.from_client_config(
				client_config=install_credentials_info,
				scopes=SCOPES
			)
			authorized_credentials = flow.run_local_server(port=0)

		except Exception as e:
			logger.debug(install_credentials_info)
			logger.warning(f'{e.__class__.__name__}: {e}')
			raise EnvironmentError("Could not install credentials.")

		logger.info("トークン情報を登録しました。")

	# Google Auth インストール済み(運用)
	else:

		logger.info("電子情報が登録されています。")

		credentials_keys = {key for key in os.environ.keys() if key.startswith("GOOGLE_CALENDAR_CREDENTIALS_")}
		credentials_info = {}  # 初期化のみ

		for key in credentials_keys:

			key_name = key.removeprefix("GOOGLE_CALENDAR_CREDENTIALS_").lower()
			if key_name == "scopes":
				credentials_info[key_name] = [os.environ[key]]
			else:
				credentials_info[key_name] = os.environ[key]

		try:

			# 電子情報の取得
			authorized_credentials = Credentials.from_authorized_user_info(info=credentials_info, scopes=SCOPES)

			# 電子情報のリフレッシュ
			if (not authorized_credentials.valid
					and authorized_credentials.expired
					and authorized_credentials.refresh_token):
				authorized_credentials.refresh(Request())

		except ValueError:
			logger.debug(credentials_info)
			raise ValueError("Could not approve credentials.")

		except Exception as e:
			logger.debug(credentials_info)
			logger.warning(f'{e.__class__.__name__}: {e}')
			raise ValueError("Could not approve credentials.")

		logger.info("トークン情報を登録しました。")

	# 環境変数の更新
	_update_environ_credentials(credentials=authorized_credentials.to_json())

	return authorized_credentials


# 作成したイベント情報を格納するリストを作成する。
def _init_sort_event_list(start: datetime.datetime, end: datetime.datetime):

	# 終了時間が開始時間より早くないかを判定
	if start > end:
		return None

	temp_date = start       # 内部変数
	events_list = []        # 返却するリスト

	# 日にち分のリストを作成する。
	while True:

		events_list.append(
			dict(
				date=temp_date,
				all_day_events=[],
				schedule_events=[]
			)
		)

		temp_date += datetime.timedelta(days=1)

		if temp_date > end:
			break

	return events_list


# 取得したイベントを終日イベントと期限付きイベントに分ける
def _create_events_list(start_date: datetime.datetime, end_date: datetime.datetime, events: list):

	sort_event_list = _init_sort_event_list(start=start_date, end=end_date)
	logger.debug(f'start: {start_date}, end: {end_date}, len(sort_event_list): {len(sort_event_list)}')

	# イベントが何もない(予定なし)の場合は、初期値のまま返却
	if not events:
		logger.warning('No upcoming events found.')
		return dict(
			start_date=start_date,
			end_date=end_date,
			sort_event_list=sort_event_list
		)

	# イベントを返却関数に設定
	for event in events:

		# イベント内容を表示(デバッグ用)
		logger.debug(f'event: {event}')

		event_start_date = event['start'].get('dateTime', event['start'].get('date'))
		logger.debug(f'event_start_date: {event_start_date}')

		# 終日の予定
		if re.match(r'^\d{4}-\d{2}-\d{2}$', event_start_date):

			logger.debug('all day event')

			# イベント情報の取得
			event_start         = datetime.datetime.strptime(event['start'].get('date'), '%Y-%m-%d')
			event_end           = datetime.datetime.strptime(event['end'].get('date'), '%Y-%m-%d')
			event_title         = event['summary']
			event_description   = event['description'] if 'description' in event else "-"
			event_colorId       = event['colorId'] if 'colorId' in event else "-"

			event_all_day_dict = dict(
				start_date=event_start,
				end_date=event_end,
				title=event_title,
				description=event_description,
				colorId=event_colorId
			)

			# イベントを格納するリストのインデックスを取得
			logger.debug(event_start)
			logger.debug(start_date)
			event_list_index = (event_start.replace(tzinfo=JST) - start_date).days

			# 開始と終了の日数を算出
			bet_date = (event_end - event_start).days

			# 同じイベント予定を別日に追加
			for i in range(bet_date):
				if event_list_index+i <= len(sort_event_list):
					logger.debug(f'bet_date:{bet_date}, event_list_index:{event_list_index}, i:{i}')
					sort_event_list[event_list_index+i]["all_day_events"].append(event_all_day_dict)

		# 時間制限付きの予定
		elif re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+09:00$', event_start_date):

			logger.debug('schedule event')

			event_start         = datetime.datetime.fromisoformat(event_start_date)
			# event_start         = datetime.datetime.strptime(event_start_date, '%Y-%m-%dT%H:%M:%S+09:00')
			event_end           = datetime.datetime.fromisoformat(event['end'].get('dateTime'))
			# event_end           = datetime.datetime.strptime(event['end'].get('dateTime'), '%Y-%m-%dT%H:%M:%S+09:00')
			event_title         = event['summary']
			event_description   = event['description'] if 'description' in event else "-"
			event_colorId       = event['colorId'] if 'colorId' in event else "-"

			event_all_day_dict = dict(
				start_date=event_start,
				end_date=event_end,
				title=event_title,
				description=event_description,
				colorId=event_colorId
			)

			# イベントを格納するリストのインデックスを取得
			event_list_index = (event_start - start_date).days

			# 開始と終了の日数を算出
			bet_date = (event_end - event_start).days + 1		# 開始日の配列にも入れるため、+1を行う。

			# 同じイベント予定を別日に追加
			for i in range(bet_date):
				if event_list_index+i < len(sort_event_list):
					logger.debug(f'bet_date:{bet_date}, schedule_events:{event_list_index}, i:{i}')
					sort_event_list[event_list_index+i]["schedule_events"].append(event_all_day_dict)

		else:
			logger.warning("The time notation does not match your expectations. Or, the time zone is different.")

	return dict(
		start_date=start_date,
		end_date=end_date,
		sort_event_list=sort_event_list
	)


# Google Calendar APIから予定を取得する関数
def get_calendar_event(start_date: datetime.datetime, end_date: datetime.datetime):

	# 資格情報の取得
	try:
		creds = _get_credentials()
	except ValueError as ex:
		logger.warning("Failed to getting credentials of google_api")
		logger.warning(ex)
		return None
	except Exception as e:
		logger.warning("Failed to getting credentials anything")
		logger.warning(f'{e.__class__.__name__}: {e}')
		return None

	start = start_date.isoformat()		# Googleカレンダーのイベントを取得する開始日
	end = end_date.isoformat()			# Googleカレンダーのイベントを取得する終了日

	# Google Calendar APIから予定を取得してくる
	try:
		service = build('calendar', 'v3', credentials=creds)

		# Google APIでカレンダーのイベントを取得する
		events_result = service.events().list(
			calendarId='primary',
			timeMin=start,
			timeMax=end,
			singleEvents=True,
			orderBy='startTime',
			timeZone="Asia/Tokyo"
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

	# エラー時の処理
	except HttpError as error:
		logger.warning('An error occurred: %s' % error)
		return None

	# イベントのログ出力
	logger.debug(events)

	# 取得したすべてのイベントに開始時間が設定されているかを確認
	for event in events:
		dt = event['start'].get('dateTime', event['start'].get('date'))
		if dt == None:
			logger.warning("Event does not include \"start_dateTime\"")
			return None

	# 返却用リストに開始、終了、イベント数を追加
	logger.debug(f'Start_time of getting user schedule: {start_date}')
	logger.debug(f'End_time of getting user schedule: {end_date}')
	len_event = len(events)
	logger.info(f'Number getting event: {len_event}')

	return _create_events_list(start_date=start_date, end_date=end_date, events=events)

if __name__ == "__main__":
	os.environ["SET_BUILD"] = "LOCAL"
	set_environ(build_env="")

	start_date = datetime.datetime.now(JST).replace(hour=0, minute=0, second=0, microsecond=0)
	end_date = start_date + datetime.timedelta(days=1, seconds=-1)

	events = get_calendar_event(start_date=start_date, end_date=end_date)

	if events is None:
		print("Error")
	else:
		print(events)