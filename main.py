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
import dateutil.parser
from logging import getLogger
from line_global import schedule_start, schedule_end

# GoogleカレンダーのURL
SCOPES = ['https://www.googleapis.com/auth/calendar']
# 使用するjsonファイル
LOAD_FILE_PATH = "edit_test.json"

# ログ出力
logger = getLogger(__name__)
logger.setLevel(logging.DEBUG)

# LINEBotのアクセストークンの初期設定
key_path = os.path.abspath(".\\Key")
with open(os.path.join(key_path, 'line_bot_info.json')) as f:
    line_bot_info = json.load(f)
LINEBOT_ACCESS_TOKEN = line_bot_info['CHANNEL_ACCESS_TOKEN']
USER_ID = line_bot_info['USER_ID']
line_bot_api = LineBotApi(LINEBOT_ACCESS_TOKEN)


def get_calender():
    dic_process = {}

    return dic_process


# main
def main():
    # jsonをコントロールするクラスのインスタンス
    jm = JsonManager(logger=logger)

    # Googleカレンダーから予定の取得
    events = get_calendar_event(
        start_status=schedule_start.TODAY,
        end_status=schedule_end.ONE_DAY)

    if events == 0:
        # サンプルのメッセージを出力
        payload = jm.package_message_none()
        print(payload)

    else:

        print(events)

        jm.package_header()
        jm.package_footer()
        jm.package_body(schedule_list=events)
        payload = jm.package_message()

    # # 予定をLOAD_FILE_PATHに入力
    # jm.edit_json(LOAD_FILE_PATH, events)
    #
    # # LOAD_FILE_PATHをjson形式で取得
    # payload = jm.load_json_template_message(LOAD_FILE_PATH)
    # # FlexMessageを送信(まだlineは送らない)
    # container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
    # # ここでlineに通知が行く
    # line_bot_api.push_message(USER_ID, messages=container_obj)


if __name__ == "__main__":
    main()
