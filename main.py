from JsonControl import JsonManager

from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from GoogleSchedule import get_calendar_event
from flask import Flask, abort, request
from common_global import *

# テスト環境で使用する変数を環境変数に登録
set_env()

# デプロイ環境で使用する変数
app = Flask(__name__)
handler = WebhookHandler(os.environ['USER_ID'])
configuration = Configuration(access_token=os.environ['LINE_BOT_ACCESS_TOKEN'])

# LINEBotのアクセストークンの初期設定
line_bot_api = LineBotApi(os.environ['LINE_BOT_ACCESS_TOKEN'])

# main( for debug )
def main():

    # jsonをコントロールするクラスのインスタンス
    jm = JsonManager(logger=logger)

    get_schedule_kind = schedule_kind.TODAY

    # Googleカレンダーから予定の取得
    events = get_calendar_event(schedule_kind=get_schedule_kind)

    # 取得したスケジュールのエラー確認
    if events is None:
        exit(-1)

    # events = {
    #     'start_date': datetime.datetime(2024, 5, 3, 0, 0),
    #     'end_date': datetime.datetime(2024, 5, 9, 0, 0),
    #     'len_event': 3,
    #     'schedule_list': [
    #         [],
    #         [{'date': '05月03日', 'all_day': 'False', 'start_time': '19:00', 'end_time': '20:00', 'summary': 'Google Calendar API テスト用', 'description': '-', 'colorId': '-'}],
    #         [{'date': '05月04日', 'all_day': 'False', 'start_time': '21:45', 'end_time': '23:45', 'summary': 'now on time', 'description': 'sdfdsg', 'colorId': '-'}],
    #         [],
    #         [{'date': '05月06日', 'all_day': 'True', 'start_time': '05月06日', 'end_time': '05月07日', 'summary': 'GW最終日', 'description': '-', 'colorId': '-'}],
    #         [],
    #         []
    #     ]
    # }

    # eventsのpackage
    payload = jm.package_message(date=events['start_date'], events_list=events['schedule_list'][0])   # 一日のmessage
    # payload = jm.package_carousel_message(events)   # 一週間の予定
    logger.debug(payload)

    # # jsonファイルに書き込む(Debug用)
    # if __debug__:
    #     path = ".//FlexMessageDictionary//body_event.json"
    #     with open(path, "w") as f:
    #         json.dump(payload, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    if payload != -1:
        # FlexMessageを送信(まだlineは送らない)
        container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
        # ここでlineに通知が行く
        line_bot_api.push_message(os.environ['USER_ID'], messages=container_obj)
    else:
        logger.info("This transaction is failed")


@app.route("/callback", methods=['POST'])
def callback():

    logger.info("Called to callback()")

    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token and more...")
        abort(400)
    return 'OK'

# lineからのメッセージがきたら処理される関数
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    logger.info("Called to handle_message()")

    with ApiClient(configuration) as api_client:

        logger.info(f'Receive message: {event.message.text}')

        if event.message.text == "今日の予定":
            app.logger.debug("今日の予定")
            msg = "today schedule"
        if event.message.text == "明日の予定":
            app.logger.debug("明日の予定")
            msg = "tomorrow schedule"
        if event.message.text == "一週間の予定":
            app.logger.debug("一週間の予定")
            msg = "a week schedule"
        else:
            msg = event.message.text

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )

    logger.info("Finished handle_message()")

if __name__ == "__main__":
    if __debug__:
        logger.info("---------- Debug --------------")
        main()
        logger.info("---------- Debug --------------")
    else:
        port = int(os.getenv("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=False)

'''

flask用のsample code

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

'''