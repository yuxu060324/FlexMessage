import requests
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
