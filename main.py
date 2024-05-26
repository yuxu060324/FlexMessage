import logging
import os
import json
import datetime
from JsonControl import JsonManager

import google.auth
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
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import Flask, abort, request
from common_global import *

set_env()

# LINEBotのアクセストークンの初期設定
line_bot_api = LineBotApi(os.environ['LINE_BOT_ACCESS_TOKEN'])

app = Flask(__name__)

handler = WebhookHandler(os.environ['USER_ID'])
configuration = Configuration(access_token=os.environ['LINE_BOT_ACCESS_TOKEN'])

# main
def main():

    # jsonをコントロールするクラスのインスタンス
    jm = JsonManager(logger=logger)

    # # Googleカレンダーから予定の取得
    # events = get_calendar_event(
    #     start_status=schedule_start.TODAY,
    #     end_status=schedule_end.WEEKLY)
    #
    # if events == 0:
    #     logger.warning("Stop get_calendar_event")
    #
    # print(events)

    # logger.info(f'schedule_dict: {events}')

    events = {
        'start_date': datetime.datetime(2024, 5, 2, 0, 0),
        'end_date': datetime.datetime(2024, 5, 9, 0, 0),
        'len_event': 3,
        'schedule_list': [
            [],
            [{'date': '05月03日', 'all_day': 'False', 'start_time': '19:00', 'end_time': '20:00', 'summary': 'Google Calendar API テスト用', 'description': '-', 'colorId': '-'}],
            [{'date': '05月04日', 'all_day': 'False', 'start_time': '21:45', 'end_time': '23:45', 'summary': 'now on time', 'description': 'sdfdsg', 'colorId': '-'}],
            [],
            [{'date': '05月06日', 'all_day': 'True', 'start_time': '05月06日', 'end_time': '05月07日', 'summary': 'GW最終日', 'description': '-', 'colorId': '-'}],
            [],
            []
        ]
    }

    # eventsのpackage
    payload = jm.package_message(date=events['start_date'], events_list=events['schedule_list'][1], weather="sunny")   # 一日のmessage
    # payload = jm.package_carousel_message(events)   # 一週間の予定
    print(payload)

    # jsonファイルに書き込む(Debug用)
    path = ".//FlexMessageDictionary//body_event.json"
    with open(path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    # # FlexMessageを送信(まだlineは送らない)
    # container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
    # # ここでlineに通知が行く
    # line_bot_api.push_message(os.environ['USER_ID'], messages=container_obj)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token and more...")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:

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

if __name__ == "__main__":
    main()
    # if __debug__:
    #     print("Hello")
    # else:
    #     print("Debug off")

'''

flask用のsample code

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

'''