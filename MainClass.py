from common_global import *
from get_schedule import get_calendar_event
from create_weather_image import create_weather_image
from create_message import (
	package_message_one_day,
	package_message_one_day_none_image,
	package_carousel_message,
	package_message_error
)

class MainApp:
	def __init__(self):
		self.out_file_name = None

	def get_weather_image_path(self):
		if self.out_file_name is None:
			return None

		path = self.out_file_name

		logger.info(f'file_path: {path}')
		return path

	def create_hero_image(self):
		self.out_file_name = create_weather_image(place_code="130000")
		return

	def create_today_schedule_message(self):

		# スケジュールを取得する開始日と終了日を設定
		today = datetime.datetime.now(JST).replace(hour=0, minute=0, second=0, microsecond=0)
		tomorrow = today + datetime.timedelta(days=1, microseconds=-1)

		try:
			# 予定の取得
			events = get_calendar_event(start_date=today, end_date=tomorrow)
			logger.debug(f'event: {events}')
			payload = package_message_one_day(events_list=events, image_path=self.get_weather_image_path())
		except Exception as e:
			payload = package_message_error()
			logger.warning(f'{e.__class__.__name__}: {e}')

		return payload

	def create_schedule_message_no_image(self, date: datetime.datetime):

		# 開始日の設定
		if date is None:
			return None

		# 終了日の設定
		end_date = date + datetime.timedelta(days=1, microseconds=-1)

		try:
			# 予定の取得
			events = get_calendar_event(start_date=date, end_date=end_date)
			logger.debug(f'event: {events}')
			payload = package_message_one_day_none_image(date=date, events_list=events["sort_event_list"][0])
		except Exception as e:
			payload = package_message_error()
			logger.warning(f'{e.__class__.__name__}: {e}')

		return payload

	def create_schedule_message_week(self):

		# スケジュールを取得する開始日と終了日を設定
		start_date = datetime.datetime.now(JST).replace(hour=0, minute=0, second=0, microsecond=0)
		end_date = start_date + datetime.timedelta(days=8, microseconds=-1)

		try:
			# 予定の取得
			events_dict = get_calendar_event(start_date=start_date, end_date=end_date)
			logger.debug(f'event: {events_dict}')
			payload = package_carousel_message(schedule_dict=events_dict)
		except Exception as e:
			payload = package_message_error()
			logger.warning(f'{e.__class__.__name__}: {e}')

		return payload

