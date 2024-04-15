import logging

import google.auth
from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
import os
import json
from JsonControl import JsonManager
from GoogleSchedule import get_calendar_event
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import Flask, abort, request
from common_global import schedule_start, schedule_end
import common_global

# events
def set_global(name_space):
    logger = common_global.getMyLogger(__name__)
    name_space["logger"] = logger

# LINEBotのアクセストークンの初期設定
key_path = os.path.abspath(".\\Key")
with open(os.path.join(key_path, 'line_bot_info.json')) as f:
    line_bot_info = json.load(f)
LINEBOT_ACCESS_TOKEN = line_bot_info['CHANNEL_ACCESS_TOKEN']
USER_ID = line_bot_info['USER_ID']
line_bot_api = LineBotApi(LINEBOT_ACCESS_TOKEN)

# main
def main():

    # logger = getMyLogger(__name__)
    set_global(globals())

    # jsonをコントロールするクラスのインスタンス
    jm = JsonManager(logger=logger)

    # Googleカレンダーから予定の取得
    # events = get_calendar_event(
    #     start_status=schedule_start.TODAY,
    #     end_status=schedule_end.ONE_DAY)
    #
    # if events == 0:
    #     logger.warning("Stop get_calendar_event")

    events = [
        {'date': '04月13日', 'all_day': 'True', 'start_time': '04月13日', 'end_time': '04月14日', 'summary': 'マイナンバー発行', 'description': '-', 'colorId': '-'},
        {'date': '04月13日', 'all_day': 'True', 'start_time': '04月13日', 'end_time': '04月14日', 'summary': '住民票発行', 'description': '-', 'colorId': '-'},
        {'date': '04月13日', 'all_day': 'False', 'start_time': '10:00', 'end_time': '11:00', 'summary': 'on schedule', 'description': '僕の見てた', 'colorId': '11'},
        {'date': '04月13日', 'all_day': 'False', 'start_time': '21:45', 'end_time': '23:45', 'summary': 'now on time', 'description': 'sdfdsg', 'colorId': '-'}
    ]

    # eventsのpackage
    jm.package_header()
    jm.package_footer()
    jm.package_body(schedule_list=events)
    payload = jm.package_message()

    # jsonファイルに書き込む(Debug用)
    path = ".//FlexMessageDictionary//body_event.json"
    with open(path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    # FlexMessageを送信(まだlineは送らない)
    container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
    # ここでlineに通知が行く
    line_bot_api.push_message(USER_ID, messages=container_obj)


if __name__ == "__main__":
    main()

'''

flask用のsample code


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

'''