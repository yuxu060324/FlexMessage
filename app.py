from flask import Flask, request, abort, send_file, url_for, render_template_string
from json_global import *
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, FlexSendMessage, TextSendMessage
)

from MainClass import MainApp

# os.environ["SET_BUILD"] = "LOCAL"			# nogrok環境での動作確認用

set_environ(build_env="")
line_bot_api = LineBotApi(os.getenv("LINE_BOT_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_BOT_CHANNEL_SECRET"))

app = Flask(__name__)
main_app = MainApp()

# default(sleep対策用)
@app.route("/")
def home():
	return "HOME"

# 画像変更
@app.route("/change_image")
def change_image():

	# 画像生成
	main_app.create_hero_image()

	file_name = main_app.get_weather_image_path()
	file_path = os.path.join(app.root_path, "static", "image", "out", file_name)
	logger.debug(f'file_path: {file_path}')

	# ブラウザ表示用の URL（static フォルダから配信）
	image_url = RENDER_PROJECT_URL + "view_weather_image"
	logger.debug(f'image_url: {image_url}')

	html = """
	<!doctype html>
	<html>
		<head>
			<meta charset="utf-8">
			<title>ファイルパスと画像表示</title>
			<style>
				body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Hiragino Kaku Gothic ProN", "メイリオ"; padding: 24px; }
				.path { font-weight: bold; margin-bottom: 12px; }
				img { border: 1px solid #ddd; max-width: 100%; height: auto; display:block; margin-top:8px; }
			</style>
		</head>
		<body>
			<div class="path">file_path: {{ file_path }}</div>
			{% if image_url %}
				<img src="{{ image_url }}" alt="generated image">
			{% else %}
				<div>画像ファイルが見つかりませんでした。</div>
			{% endif %}
		</body>
	</html>
	"""

	return render_template_string(html, file_path=file_path, image_url=image_url)

# 天気画像表示
@app.route("/view_weather_image")
def view_weather_image():

	filename = main_app.get_weather_image_path()
	path = os.path.join(app.root_path, "static", "image", "out", filename)

	if not os.path.exists(path):
		# デフォルトファイルを設定
		path = os.path.join(app.root_path, "image", "weather", "out_weather_image_default.png")

	logger.debug(f'dirname: {OUT_FOLDER_PATH}')
	logger.debug(f'filename: {filename}')

	return send_file(path)

@app.route("/weather/<filename>")
def view_weather_temp_image(filename):

	path = os.path.join(app.root_path, "image", "weather", filename)

	if not os.path.exists(path):
		return "ファイルが存在しません", 404

	logger.debug(f'dirname: {WEATHER_PATH}')
	logger.debug(f'filename: {filename}')

	return send_file(path)

# LINEのユーザからの情報を受け取る。
@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']

	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

	logger.info(f'Event.message: {event.message.text}')

	# 固定文以外のメッセージの場合は、受け取ったメッセージをそのまま返す
	if not event.message.text in LINE_MESSAGE_ACTION_LIST:
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=event.message.text)
		)
		return

	# 送信メッセージの初期化
	payload = None

	if event.message.text == LINE_MESSAGE_ACTION_LIST[0]:			# 今日の予定を通知
		payload = main_app.create_today_schedule_message()
	elif event.message.text == LINE_MESSAGE_ACTION_LIST[1]:			# 明日の予定を通知
		today = datetime.datetime.now(JST).replace(hour=0, minute=0, second=0, microsecond=0)
		tomorrow = today + datetime.timedelta(days=1)
		payload = main_app.create_schedule_message_no_image(date=tomorrow)
	elif event.message.text == LINE_MESSAGE_ACTION_LIST[2]:			# 1週間の予定を通知
		payload = main_app.create_schedule_message_week()

	logger.debug(f'payload: {payload}')

	try:
		# Googleカレンダーから予定の取得
		events = get_calendar_event(schedule_kind=get_schedule_kind)

		if events is None:
			logger.warning("Events is Empty")
			raise EnvironmentError("Could not retrieve event.")

		if get_schedule_kind == schedule_kind.WEEKLY:
			payload = package_carousel_message(schedule_dict=events)
		else:
			payload = package_message_one_day(events_list=events)

		# ログファイルに出力
		logger.debug(f'payload: {payload}')

	except Exception as e:
		payload = package_message_error()
		logger.warning(f'{e.__class__.__name__}: {e}')

	if payload is not None:
		# FlexMessage形式のメッセージ作成
		obj = FlexSendMessage(alt_text="Message", contents=payload)
		# LINEメッセージの送信
		line_bot_api.reply_message(
			reply_token=event.reply_token,
			messages=obj
		)
	else:
		logger.info("This transaction is failed")


if __name__ == "__main__":
	logger.info("Flask App running")
	app.run(threaded=True)
