import logging
import os, re, datetime
import json
import urllib.request
from typing import Dict, Union, Any
from json_global import *
from GetWeather import get_weather

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

# エラー時にユーザーに送信するメッセージを記載しているファイルのPATH
ERROR_MESSAGE_FILE_PATH = os.path.join(HOME_ABSPATH, "TemplateMessage", "error_message.json")

# boxで囲むだけの関数
def pack_vertical(arr: list, margin=None, spacing=None, width=None, height=None,
                  paddingAll=None, paddingTop=None, backgroundColor=None, offsetStart=None, justifyContent=None,
                  cornerRadius=None, borderColor=None, borderWidth=None, alignItems=None, flex=None):
    pattern = {"type": "box", "layout": "vertical", "contents": arr}

    if margin is not None:
        pattern.update(margin=margin)
    if paddingAll is not None:
        pattern.update(paddingAll=paddingAll)
    if paddingTop is not None:
        pattern.update(paddingTop=paddingTop)
    if backgroundColor is not None:
        pattern.update(backgroundColor=backgroundColor)
    if spacing is not None:
        pattern.update(spacing=spacing)
    if width is not None:
        pattern.update(width=width)
    if height is not None:
        pattern.update(height=height)
    if offsetStart is not None:
        pattern.update(offsetStart=offsetStart)
    if alignItems is not None:
        pattern.update(alignItems=alignItems)
    if flex is not None:
        pattern.update(flex=flex)

    # サークル描画用
    if cornerRadius is not None:
        pattern.update(cornerRadius=cornerRadius)
    if justifyContent is not None:
        pattern.update(justifyContent=justifyContent)
    if borderWidth is not None:
        pattern.update(borderWidth=borderWidth)
    if borderColor is not None:
        pattern.update(borderColor=borderColor)

    return pattern


def pack_horizontal(arr: list, margin=None, spacing=None, width=None, height=None, align=None,
                    paddingAll=None, paddingStart=None, backgroundColor=None, offsetStart=None, alignItems=None):
    pattern = {"type": "box", "layout": "horizontal", "contents": arr}

    if margin is not None:
        pattern.update(margin=margin)
    if paddingAll is not None:
        pattern.update(paddingAll=paddingAll)
    if paddingStart is not None:
        pattern.update(paddingStart=paddingStart)
    if backgroundColor is not None:
        pattern.update(backgroundColor=backgroundColor)
    if spacing is not None:
        pattern.update(spacing=spacing)
    if width is not None:
        pattern.update(width=width)
    if height is not None:
        pattern.update(height=height)
    if offsetStart is not None:
        pattern.update(offsetStart=offsetStart)
    if align is not None:
        pattern.update(align=align)
    if alignItems is not None:
        pattern.update(alignItems=alignItems)

    return pattern


def pack_baseline(arr: list, margin=None, spacing=None, width=None, height=None, paddingAll=None,
                  paddingStart=None, backgroundColor=None, offsetStart=None, offsetTop=None, alignItems=None):
    pattern = {"type": "box", "layout": "baseline", "contents": arr}

    if margin is not None:
        pattern.update(margin=margin)
    if paddingAll is not None:
        pattern.update(paddingAll=paddingAll)
    if paddingStart is not None:
        pattern.update(paddingStart=paddingStart)
    if backgroundColor is not None:
        pattern.update(backgroundColor=backgroundColor)
    if spacing is not None:
        pattern.update(spacing=spacing)
    if width is not None:
        pattern.update(width=width)
    if height is not None:
        pattern.update(height=height)
    if offsetStart is not None:
        pattern.update(offsetStart=offsetStart)
    if offsetTop is not None:
        pattern.update(offsetTop=offsetTop)
    if alignItems is not None:
        pattern.update(alignItems=alignItems)

    return pattern


def pack_text(str, color=None, size=None, flex=None, uri=None, weight=None, margin=None, decoration=None):
    pattern = {"type": "text", "text": str}
    if color is not None:
        pattern.update(color=color)
    if size is not None:
        pattern.update(size=size)
    if flex is not None:
        pattern.update(flex=flex)
    if uri is not None:
        pattern.update(action={"type": "uri", "label": "action", "uri": uri})
    if weight is not None:
        pattern.update(weight=weight)
    if margin is not None:
        pattern.update(margin=margin)
    if decoration is not None:
        pattern.update(decoration=decoration)

    return pattern


def pack_image(path, size=None, aspectRatio=None, aspectMode=None):
    pattern = {"type": "image", "url": path}
    if size is not None:
        pattern.update(size=size)
    if aspectRatio is not None:
        pattern.update(aspectRatio=aspectRatio)
    if aspectMode is not None:
        pattern.update(aspectMode=aspectMode)
    return pattern


def pack_icon(path, size, scaling=None):
    pattern = {"type": "icon", "size": size, "url": path}
    if scaling is not None:
        pattern.update(scaling=scaling)
    return pattern


def pack_separator(margin="none"):
    return {"type": "separator", "margin": margin}


def pack_filter():
    return {"type": "filter"}


def pack_circle(width, hegiht, cornerRadius="30px", borderColor="#ff0000", borderWidth="2px"):
    return pack_vertical(
        [
            pack_vertical(
                [],
                cornerRadius=cornerRadius,
                height=hegiht,
                width=width,
                borderColor=borderColor,
                borderWidth=borderWidth
            ),
        ],
        flex=0,
        justifyContent="center"
    )


def get_icon(icon_kind, icon_file_kind):

    icon_file_path = ""

    if icon_kind != "weather" and icon_kind != "event":
        logger.warning(f'{icon_kind} is unexpected')
        return

    if icon_kind == "weather":
        if icon_file_kind in ICON_WEATHER_FILE:
            icon_file_name = ICON_WEATHER_FILE[icon_file_kind]
        else:
            icon_file_name = ICON_WEATHER_FILE['other']
        icon_file_path = icon_file_name
    if icon_kind == "event":
        if icon_file_kind in ICON_EVENT_FILE:
            icon_file_name = ICON_EVENT_FILE[icon_file_kind]
        else:
            icon_file_name = ICON_EVENT_FILE['other']
        icon_file_path = icon_file_name

    # icon_file_pathがインターネット上に公開されている場合
    try:
        with urllib.request.urlopen(icon_file_path) as file:
            logger.info(f'{icon_file_path} is exist')
        return icon_file_path

    except:
        logger.warning(f'{icon_file_path} does not exist')
        return None


# Flex Messageのヘッダ部をパッケージする関数
def _package_header(date: datetime.datetime):

    # パラメータチェック
    if type(date) is not datetime.datetime:
        logger.warning("Setting parameter(data) is not right")
        return None

    # 日付の文字列
    date_wod = DAY_OF_WEEK_LIST[date.weekday()]
    date_str = date.strftime("%m / %d ( " + date_wod + " )")

    # 日付のboxの追加
    date_box = pack_vertical([
        pack_text("DATE", color="#ffffffB0", size="sm"),
        pack_text(date_str, color="#ffffff", size="xl", flex=4, weight="bold")
    ])

    # weatherのlayoutなしでheaderを作成
    _message_header = pack_horizontal(
        [date_box],
        paddingAll="20px",
        backgroundColor="#0367D3",
        spacing='md',
        height="90px"
    )

    logger.debug("Finished set up header")
    return _message_header


# Flex Messageのボディ部(終日イベントの予定のみ)をパッケージする関数
def _package_event_all_body(events: list):

    if len(events) == 0:
        logger.warning("events(all_day) is empty")
        return None

    title_box = pack_horizontal(
        [pack_text("終日", size="lg", weight="bold")],
    )
    temp_event = []

    for event in events:
        temp_event.append(pack_horizontal(
            [
                pack_circle(width="8px", hegiht="8px"),
                pack_text(event['summary'], size="sm", margin="md")
            ],
            paddingStart="lg",
            alignItems="center"
        ))

    event_detail = pack_vertical(temp_event)

    _message_body_all_day = pack_vertical([title_box, event_detail])

    logger.debug("Finished set up body_event")

    return _message_body_all_day


# Flex Messageのボディ部(時間指定イベントの予定のみ)をパッケージする関数
def _package_event_schedule(events: list):

    if len(events) == 0:
        logger.warning("events(all_day) is empty")
        return None

    title_box = pack_horizontal(
        [pack_text("スケジュール", size="lg", weight="bold")],
    )
    temp_event = []

    for event in events:

        if event['colorId'] in EVENT_KIND:
            event_kind = EVENT_KIND[event['colorId']]
        else:
            logger.warning("events does not include \"colorId\"")
            return None

        icon_path = get_icon(icon_kind="event", icon_file_kind=event_kind)
        if icon_path is None:
            logger.warning(f'{event_kind} does not include in \"ICON_WEATHER_FILE\"')
            return None

        temp_event.append(pack_horizontal(
            [
                pack_text(event['start_time'], size="sm", flex=0),
                pack_baseline(
                    [pack_icon(
                        path=icon_path, size="sm"
                    )],
                    offsetStart="5px",
                    offsetTop="3px",
                    width="25px",
                    height="25px"
                ),
                pack_text(event['summary'], size="sm")
            ],
            margin="md",
            paddingStart="lg",
            align="center"
            # alignItems="flex-start"
        ))

    event_detail = pack_vertical(temp_event)

    _message_body_schedule = pack_vertical([title_box, event_detail], paddingTop="md")

    logger.debug("Finished set up body_event")

    return _message_body_schedule


# Flex Messageのボディ部(全体)をパッケージする関数
def _package_body(events: list):

    event_all_day_list = []
    event_schedule_list = []

    _message_body_all_day = {}
    _message_body_schedule = {}

    # 取得するイベントがない場合
    if len(events) == 0:
        _body = pack_vertical(
            [pack_text("予定なし", color="#0000a0", size="xl", weight="bold")],
            paddingAll="lg",
            margin="lg",
            alignItems="center"
        )
        return _body

    # イベントを終日(時間指定なし)とスケジュール(時間指定あり)
    for event in events:
        if event['all_day'] == "True":
            event_all_day_list.append(event)
        elif event['all_day'] == "False":
            event_schedule_list.append(event)
        else:
            logger.warning("\"all_day\" is Unexpected parameters")
            return -1

    if event_all_day_list:
        _message_body_all_day = _package_event_all_body(event_all_day_list)
    if event_schedule_list:
        _message_body_schedule = _package_event_schedule(event_schedule_list)

    # 時間範囲のあるイベントのみ
    if 'type' not in _message_body_all_day.keys():
        body_event_list = [_message_body_schedule]
    # 終日イベントのみ
    elif 'type' not in _message_body_schedule.keys():
        body_event_list = [_message_body_all_day]
    # どちらも
    else:
        body_event_list = [
            _message_body_all_day,
            pack_separator(margin="lg"),
            _message_body_schedule
        ]

    _message_body = pack_vertical(
        body_event_list,
        paddingAll="lg"
    )

    return _message_body


# Flex Messageのフッダ部(全体)をパッケージする関数
def _package_footer():

    _message_footer = pack_vertical(
        [pack_text("\"Google Calendar\" を開く", uri=FOOTER_URL, color="#0000ff", decoration="underline")]
    )

    logger.debug("Finished set up footer")

    return _message_footer


# Flex Messageのヒーロ部(画像)をパッケージ
def _package_hero():

    # place_codeは気象庁APIを参照(130000は東京地方の場所コード)
    weather_picture_path = get_weather(place_code="130000")

    if checkURL(weather_picture_path) is not True:
        return None

    _message_hero = pack_image(path=weather_picture_path, size="full", aspectRatio="16:9")

    logger.debug("Finished set up hero")

    return _message_hero


# 1日分の予定をFlex Message形式でパッケージ(画像有り)
# @param    [in]    events_list   setting schedule event in body of message
# @param    [out]   payload       output message
def package_message_one_day(events_list: dict):

    # 開始日、終了日、イベント数が用意されているかを確認する。
    if events_list.get("start_date") is None:
        logger.warning("\"start_date\" is not set in the list of arguments.")
        return None
    if events_list.get("end_date") is None:
        logger.warning("\"end_date\" is not set in the list of arguments.")
        return None
    if events_list.get("len_event") is None:
        logging.warning("\"len_event\" is not set in the list of arguments.")
        return None

    date = events_list.get("start_date")                    # 予定の開始日を取得
    schedule_list = []

    # スケジュールのリストを取得
    if "schedule_list" in events_list.keys():
        schedule_list = events_list.get("schedule_list")[0]     # 1日分のため、リストの最初のみ取得

    _message_header = _package_header(date=date)
    _message_hero = _package_hero()
    _message_body = _package_body(events=schedule_list)
    _message_footer = _package_footer()

    if _message_header is None:
        logger.warning("package_header() is failed")
        return None

    # メッセージのHero(天気の画像)を作成
    if _message_hero is None:
        logger.warning("package_hero() is failed")
        return None

    if _message_body is None:
        logger.warning("package_body() is failed")
        return None

    if _message_footer is None:
        logger.warning("package_footer() is failed")
        return None

    # Payloadの作成
    _message = {
        "type": "bubble",
        "size": "mega",
        "header": _message_header,
        "hero": _message_hero,
        "body": _message_body,
        "footer": _message_footer
    }

    logger.info("Finished set up message_package_one_day")

    return _message


# 1日分の予定をFlex Message形式でパッケージ(画像なし)
# @param    [in]    date          setting schedule date in header of message
# @param    [in]    events_list   setting schedule event in body of message
# @param    [out]   payload       output message
def _package_message_one_day_none_image(date: datetime.datetime, events_list: list):

    _message_header = _package_header(date=date)
    _message_body = _package_body(events=events_list)
    _message_footer = _package_footer()

    if _message_header is None:
        logger.warning("package_header() is failed")
        return None

    if _message_body is None:
        logger.warning("package_body() is failed")
        return None

    if _message_footer is None:
        logger.warning("package_footer() is failed")
        return None

    # Payloadの作成
    _message = {
        "type": "bubble",
        "size": "mega",
        "header": _message_header,
        "body": _message_body,
        "footer": _message_footer
    }

    logger.debug("Finished set up message_package_one_day_none_image")

    return _message


# 一週間のスケジュールを出力する用(carouselで日にちごとにbubbleを作成してメッセージを作成)
def package_carousel_message(schedule_dict: dict):

    logger.debug("call package_carousel_message")

    bubble_dict = []

    if 'start_date' not in schedule_dict or 'schedule_list' not in schedule_dict:
        logger.warning("events_list dose not include \"start_date\" or \"schedule_list\"")
        return None

    schedule_start_date = schedule_dict['start_date']
    len_date = len(schedule_dict['schedule_list'])

    for schedule_list_index in range(len_date):
        schedule_date = schedule_start_date + datetime.timedelta(days=schedule_list_index)

        payload = _package_message_one_day_none_image(
            date=schedule_date,
            events_list=schedule_dict['schedule_list'][schedule_list_index]
        )

        bubble_dict.append(payload)

    _message = {
        "type": "carousel",
        "contents": bubble_dict
    }

    logger.debug("Finished set up package_carousel_message")

    return _message

def package_message_error():

    with open(ERROR_MESSAGE_FILE_PATH, "r") as file:
        _message = json.load(file)

    return _message
