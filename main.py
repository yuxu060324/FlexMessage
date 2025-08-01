# ローカル環境で動作を確認するためのファイル

from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
from common_global import *
from GoogleSchedule import get_calendar_event
from JsonControl import (
	package_message_one_day,
	_package_message_one_day_none_image,
	package_carousel_message
)
from GetWeather import get_weather, get_weather_path

os.environ["SET_BUILD"] = "LOCAL"

# テスト環境で使用する変数を環境変数に登録
set_environ(build_env="")

# LINEBotのアクセストークンの初期設定
line_bot_api = LineBotApi(os.environ['LINE_BOT_CHANNEL_ACCESS_TOKEN'])


def create_message_image_test_message():

	payload = {
		"type": "bubble",
		"size": "mega",
		"header": {
			"type": "box",
			"layout": "horizontal",
			"contents": [
				{
					"type": "box",
					"layout": "vertical",
					"contents": [
						{
							"type": "text",
							"text": "DATE",
							"color": "#ffffffB0",
							"size": "sm"
						},
						{
							"type": "text",
							"text": "08 / 01 ( 金 )",
							"color": "#ffffff",
							"size": "xl",
							"flex": 4,
							"weight": "bold"
						}
					]
				}
			],
			"paddingAll": "20px",
			"backgroundColor": "#0367D3",
			"spacing": "md",
			"height": "90px"
		},
		"hero": {
			"type": "image",
			"url": get_weather_path(),
			"size": "full",
			"aspectRatio": "16:9"
		},
		"body": {
			"type": "box",
			"layout": "vertical",
			"contents": [
				{
					"type": "text",
					"text": "予定なし",
					"color": "#0000a0",
					"size": "xl",
					"weight": "bold"
				}
			],
			"margin": "lg",
			"paddingAll": "lg",
			"alignItems": "center"
		},
		"footer": {
			"type": "box",
			"layout": "vertical",
			"contents": [
				{
					"type": "text",
					"text": "\"Google Calendar\" を開く",
					"color": "#0000ff",
					"action": {
						"type": "uri",
						"label": "action",
						"uri": "https://www.google.com/"
					},
					"decoration": "underline"
				}
			]
		}
	}

	return payload

# main( for debug )
def main():
	get_schedule_kind = schedule_kind.TODAY

	# # Googleカレンダーから予定の取得
	# events = get_calendar_event(schedule_kind=get_schedule_kind)
	# if events is None:
	# 	logger.debug("Events is empty")
	# 	return None

	# logger.info(events)

	# 画像表示デバッグ用のpackage
	payload = create_message_image_test_message()

	# # eventsのpackage(画像有の1日の予定)
	# payload = package_message_one_day(events_list=events)  # 一日のmessage
	# logger.debug(f'payload: {payload}')

	# # eventsのpackage(画像無しの1日の予定)
	# payload = _package_message_one_day_none_image(
	#     date=events.get("start_date"),
	#     events_list=events.get("schedule_list")[0]
	# )
	# logger.debug(f'payload: {payload}')

	# # eventsのpackage(1週間の予定)
	# payload = package_carousel_message(schedule_dict=events)
	# logger.debug(f'payload: {payload}')
	#
	# debug_file_path = os.path.join(HOME_ABSPATH, "TemplateMessage", "debug_message.json")
	# with open(debug_file_path, mode="w", encoding="utf-8") as f:
	# 	json.dump(payload, f, ensure_ascii=False, indent=4)

	if payload is not None:
		# FlexMessageを作成(まだlineは送らない)
		container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
		# ここでlineに通知が行く
		line_bot_api.push_message(os.environ['USER_ID'], messages=container_obj)
	else:
		logger.info("This transaction is failed")


if __name__ == "__main__":
	logger.info("---------- Start(Mode: Debug) --------------")
	main()
	logger.info("---------- End(Mode: Debug) --------------")
