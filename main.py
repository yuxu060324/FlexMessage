from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
from common_global import *
from GoogleSchedule import get_calendar_event
from JsonControl import (
    package_message_one_day,
    _package_message_one_day_none_image,
    package_carousel_message
)

# テスト環境で使用する変数を環境変数に登録
set_environ(build_env="LOCAL")

# LINEBotのアクセストークンの初期設定
line_bot_api = LineBotApi(os.environ['LINE_BOT_CHANNEL_ACCESS_TOKEN'])


# main( for debug )
def main():
    get_schedule_kind = schedule_kind.WEEKLY

    # Googleカレンダーから予定の取得
    events = get_calendar_event(schedule_kind=get_schedule_kind)

    logger.info(events)

    # eventsのpackage(画像有の1日の予定)
    # payload = package_message_one_day(events_list=events)  # 一日のmessage
    # logger.debug(f'payload: {payload}')

    # # eventsのpackage(画像無しの1日の予定)
    # payload = _package_message_one_day_none_image(
    #     date=events.get("start_date"),
    #     events_list=events.get("schedule_list")[0]
    # )
    # logger.debug(f'payload: {payload}')

    # eventsのpackage(1週間の予定)
    payload = package_carousel_message(schedule_dict=events)
    logger.debug(f'payload: {payload}')

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
