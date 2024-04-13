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
from common_global import schedule_start, schedule_end
import common_global

# events
def set_global(name_space):
    logger = common_global.getMyLogger(__name__)
    name_space["logger"] = logger

# # LINEBotのアクセストークンの初期設定
# key_path = os.path.abspath(".\\Key")
# with open(os.path.join(key_path, 'line_bot_info.json')) as f:
#     line_bot_info = json.load(f)
# LINEBOT_ACCESS_TOKEN = line_bot_info['CHANNEL_ACCESS_TOKEN']
# USER_ID = line_bot_info['USER_ID']
# line_bot_api = LineBotApi(LINEBOT_ACCESS_TOKEN)


# main
def main():

    # logger = getMyLogger(__name__)
    set_global(globals())
    logger.setLevel(logging.DEBUG)

    logger.debug("warning")

    # jsonをコントロールするクラスのインスタンス
    jm = JsonManager(logger=logger)

    # Googleカレンダーから予定の取得
    # events = get_calendar_event(
    #     start_status=schedule_start.TODAY,
    #     end_status=schedule_end.ONE_DAY)
    #
    # if events == 0:
    #     logger.warning("Stop get_calendar_event")

    events = {
        ('2024-04-07T09:00:00+09:00', '2024-04-07T10:00:00+09:00', 'test'),
        ('2024-04-07T12:00:00+09:00', '2024-04-07T13:00:00+09:00', 'on schedule'),
        ('2024-04-07T18:00:00+09:00', '2024-04-07T20:00:00+09:00', 'now on time'),
    }

    if events is None:
        # サンプルのメッセージを出力
        payload = jm.package_message_none()
        print(payload)
        return

    else:
        # eventsのpackage
        jm.package_header()
        jm.package_footer()
        jm.package_body(schedule_list=events)
        payload = jm.package_message()
        print(payload)

    # # FlexMessageを送信(まだlineは送らない)
    # container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
    # # ここでlineに通知が行く
    # line_bot_api.push_message(USER_ID, messages=container_obj)


if __name__ == "__main__":
    main()
