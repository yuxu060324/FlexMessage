from flask import Flask, request, abort, send_from_directory
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
from GoogleSchedule import get_calendar_event
from JsonControl import (
    package_message_one_day,
    package_carousel_message,
    package_message_error
)
from setRichMenu import set_rich_menu

# if os.getenv("SET_BUILD") != "FLASK_RENDER":
#     set_environ(build_env="FLASK_LOCAL")

CHANNEL_ACCESS_TOKEN = os.environ["LINE_BOT_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["LINE_BOT_CHANNEL_SECRET"]

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)



@app.route("/")
def home():
    return "HOME"

@app.route("/out/<filename>")
def view_image(filename):

    logger.debug(f'dirname: {OUT_FOLDER_PATH}')
    logger.debug(f'filename: {filename}')

    return send_from_directory(OUT_FOLDER_PATH, filename)
    #
    # message = f'<img src={OUT_FILE_PATH_HERO}>'
    #
    # # ログファイルの中身を取得
    # path = os.path.join(HOME_ABSPATH, "log", "project.log")
    # if os.path.isdir(path) and os.path.isfile(path):
    #     with open(path) as file:
    #         message = json.load(file)
    #
    # OUT_FILE_PATH_HERO
    #
    # if message is None:
    #     message = "Not log"
    #
    # return message

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

    get_schedule_kind = schedule_kind.NUM_KIND

    logger.info(f'Event.message: {event.message.text}')

    # 固定文以外のメッセージの場合は、受け取ったメッセージをそのまま返す
    if event.message.text in LINE_MESSAGE_ACTION_LIST:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
        return

    if event.message.text == LINE_MESSAGE_ACTION_LIST[0]:           # 今日の予定を通知
        get_schedule_kind = schedule_kind.TODAY
    elif event.message.text == LINE_MESSAGE_ACTION_LIST[1]:         # 明日の予定を通知
        get_schedule_kind = schedule_kind.TOMORROW
    elif event.message.text == LINE_MESSAGE_ACTION_LIST[2]:         # 1週間の予定を通知
        get_schedule_kind = schedule_kind.WEEKLY

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
    set_rich_menu()
    app.run(threaded=True)
