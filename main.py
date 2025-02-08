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

    # # eventsのpackage(画像有の1日の予定)
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

    # jsonファイルに書き込む(Debug用)
    path = "TemplateMessage/error_message.json"
    with open(path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    if payload is not None:
        # FlexMessageを作成(まだlineは送らない)
        container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
        # ここでlineに通知が行く
        line_bot_api.push_message(os.environ['USER_ID'], messages=container_obj)
    else:
        logger.info("This transaction is failed")


# @app.route("/callback", methods=['POST'])
# def callback():
#
#     logger.info("Called to callback()")
#
#     signature = request.headers['X-Line-Signature']
#
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         app.logger.info("Invalid signature. Please check your channel access token and more...")
#         abort(400)
#     return 'OK'
#
# # lineからのメッセージがきたら処理される関数
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#
#     logger.info("Called to handle_message()")
#
#     with ApiClient(configuration) as api_client:
#
#         logger.info(f'Receive message: {event.message.text}')
#
#         if event.message.text == "今日の予定":
#             app.logger.debug("今日の予定")
#             msg = "today schedule"
#         if event.message.text == "明日の予定":
#             app.logger.debug("明日の予定")
#             msg = "tomorrow schedule"
#         if event.message.text == "一週間の予定":
#             app.logger.debug("一週間の予定")
#             msg = "a week schedule"
#         else:
#             msg = event.message.text
#
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=msg)]
#             )
#         )
#
#     logger.info("Finished handle_message()")

if __name__ == "__main__":
    logger.info("---------- Debug --------------")
    # main()
    logger.info("---------- Debug --------------")

'''

flask用のsample code

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

'''
