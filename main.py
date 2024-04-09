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
import logging
from line_global import schedule_start, schedule_end

# GoogleカレンダーのURL
SCOPES = ['https://www.googleapis.com/auth/calendar']
# 使用するjsonファイル
LOAD_FILE_PATH = "edit_test.json"

# ログ出力
log_file_name = "project"
log_file_path = os.path.join(os.path.abspath("."), "log", f'{log_file_name}.log')


def getMyLogger(name):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-9s %(asctime)s [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


# LINEBotのアクセストークンの初期設定
key_path = os.path.abspath(".\\Key")
with open(os.path.join(key_path, 'line_bot_info.json')) as f:
    line_bot_info = json.load(f)
LINEBOT_ACCESS_TOKEN = line_bot_info['CHANNEL_ACCESS_TOKEN']
USER_ID = line_bot_info['USER_ID']
line_bot_api = LineBotApi(LINEBOT_ACCESS_TOKEN)


# main
def main():

    logger = getMyLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # jsonをコントロールするクラスのインスタンス
    jm = JsonManager(logger=logger)

    # Googleカレンダーから予定の取得
    events = get_calendar_event(
        start_status=schedule_start.TODAY,
        end_status=schedule_end.ONE_DAY)
    # events = {
    #     ('2024-04-07T09:00:00+09:00', '2024-04-07T10:00:00+09:00', 'test'),
    #     ('2024-04-07T12:00:00+09:00', '2024-04-07T13:00:00+09:00', 'on schedule'),
    #     ('2024-04-07T18:00:00+09:00', '2024-04-07T20:00:00+09:00', 'now on time'),
    # }

    # if events == 0:
    #     # サンプルのメッセージを出力
    #     payload = jm.package_message_none()
    #     print(payload)
    #     return
    #
    # else:
    #
    #     print(events)
    #
    #     jm.package_header()
    #     jm.package_footer()
    #     jm.package_body(schedule_list=events)
    #     payload = jm.package_message()
    #     print(payload)

    # # FlexMessageを送信(まだlineは送らない)
    # container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
    # # ここでlineに通知が行く
    # line_bot_api.push_message(USER_ID, messages=container_obj)


if __name__ == "__main__":
    main()
