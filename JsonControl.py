import os, re, datetime
import json
from typing import Dict, Union, Any
from json_global import *


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


def pack_horizontal(arr: list, margin=None, spacing=None, width=None, height=None,
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
    if alignItems is not None:
        pattern.update(alignItems=alignItems)

    return pattern


def pack_text(str, color=None, size=None, flex=None, url=None, weight=None, margin=None, decoration=None):
    pattern = {"type": "text", "text": str}
    if color is not None:
        pattern.update(color=color)
    if size is not None:
        pattern.update(size=size)
    if flex is not None:
        pattern.update(flex=flex)
    if url is not None:
        pattern.update(action={"type": "url", "label": "action", "url": url})
    if weight is not None:
        pattern.update(weight=weight)
    if margin is not None:
        pattern.update(margin=margin)
    if decoration is not None:
        pattern.update(decoration=decoration)

    return pattern


def pack_image(path):
    pattern = {"type": "image", "url": path}
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


class JsonManager:

    def __init__(self, logger):

        self.massage_json_path = os.path.abspath(".\\FlexMessageDictionary")
        self.logger = logger

        # for message
        self._message = {}
        self._header = {}
        self._event_all_day = {}
        self._event_schedule = {}
        self._body = {}
        self._footer = {}

    def load_json(self, path):

        if not os.path.isfile(path):
            self.logger.warning(f'{path} does not exist')
            return

        with open(path) as f:
            payload = json.load(f)

        return payload

    def get_icon(self, icon_kind, icon_file_kind):

        icon_file_path = ""

        if icon_kind != "weather" and icon_kind != "event":
            self.logger.warning(f'{icon_kind} is unexpected')
            return

        if icon_kind == "weather":
            if icon_file_kind in ICON_WEATHER_FILE:
                icon_file_name = ICON_WEATHER_FILE[icon_file_kind]
            else:
                icon_file_name = ICON_WEATHER_FILE['other']
            icon_file_path = os.path.join(ICON_WEATHER_FOLDER_PATH, icon_file_name)
        if icon_kind == "event":
            if icon_file_kind in ICON_EVENT_FILE:
                icon_file_name = ICON_EVENT_FILE[icon_file_kind]
            else:
                icon_file_name = ICON_EVENT_FILE['other']
            icon_file_path = os.path.join(ICON_EVENT_FOLDER_PATH, icon_file_name)

        if os.path.isfile(icon_file_path):
            return icon_file_path
        else:
            self.logger.warning(f'{icon_file_path} does not exist')
            return -1

    # Flex MessageのHeader部のパッケージ
    def package_header(self, date, weather="sunny"):

        # 日付の文字列
        date_today = datetime.datetime.now()
        date_wod = DAY_OF_WEEK_LIST[date_today.weekday()]
        date_str = date_today.strftime("%m / %d ( " + date_wod + " )")

        # 天気アイコンのファイルパス
        weather_file_path = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png"  # os.path.join(ICON_WEATHER_FOLDER_PATH, ICON_WEATHER_FILE[weather])
        # if not os.path.isfile(weather_file_path):
        #     self.logger.warning(f'{weather_file_path} does not exist')
        #     return

        # 日付のboxの追加
        date_box = pack_vertical([
            pack_text("DATE", color="#ffffffB0", size="sm"),
            pack_text(date_str, color="#ffffff", size="xl", flex=4, weight="bold")
        ])

        # 天気アイコンのboxの追加
        weather_box = pack_vertical(
            [pack_image(path=weather_file_path)],
            margin="none",
            spacing="none",
            width="60px",
            height="60px"
        )

        self._header = pack_horizontal(
            [date_box, weather_box],
            paddingAll="20px",
            backgroundColor="#0367D3",
            spacing='md',
            height="90px"
        )

        self.logger.debug("Finished set up header")

    def package_event_all_body(self, events):

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

        self._event_all_day = pack_vertical([title_box, event_detail])

        self.logger.debug("Finished set up body_event")

    def package_event_schedule(self, events):

        title_box = pack_horizontal(
            [pack_text("スケジュール", size="lg", weight="bold")],
        )
        temp_event = []

        for event in events:

            if event['colorId'] in EVENT_KIND:
                event_kind = EVENT_KIND[event['colorId']]
            else:
                self.logger.warning("events does not include \"colorId\"")
                return -1

            icon_path = self.get_icon(icon_kind="event", icon_file_kind=event_kind)
            if icon_path == -1:
                self.logger.warning(f'{event_kind} does not include in \"ICON_WEATHER_FILE\"')
                return -1

            temp_event.append(pack_horizontal(
                [
                    pack_text(event['start_time'], flex=0, size="sm"),
                    pack_vertical(
                        [pack_image("https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png")],
                        alignItems="center",
                        width="35px",
                        height="25px"
                    ),
                    pack_text(event['summary'], size="sm", margin="md")
                ],
                paddingStart="lg",
                alignItems="center"
            ))

        event_detail = pack_vertical(temp_event)

        self._event_schedule = pack_vertical([title_box, event_detail], paddingTop="md")

        self.logger.debug("Finished set up body_event")

    # Flex MessageのBody部のパッケージ
    def package_body(self, schedule_list):

        event_all_day_list = []
        event_schedule_list = []

        for event in schedule_list:
            if event['all_day'] == "True":
                event_all_day_list.append(event)
            elif event['all_day'] == "False":
                event_schedule_list.append(event)
            else:
                self.logger.warning("\"all_day\" is Unexpected parameters")
                return -1

        if event_all_day_list:
            self.package_event_all_body(event_all_day_list)
        if event_schedule_list:
            self.package_event_schedule(event_schedule_list)

        # 予定なし
        if 'type' not in self._event_all_day.keys() or 'type' not in self._event_schedule:
            self._body = pack_vertical(
                [pack_text("予定なし", weight="bold", size="xl", color="#0000a0")],
                paddingAll="lg",
                margin="lg",
                alignItems="center"
            )
            return 0

        # 終日イベントのみ
        if 'type' not in self._event_all_day.keys():
            body_event_list = [self._event_schedule]
        # 時間範囲のあるイベントのみ
        elif 'type' not in self._event_schedule.keys():
            body_event_list = [self._event_all_day]
        # どちらも
        else:
            body_event_list = [
                self._event_all_day,
                pack_separator(margin="lg"),
                self._event_schedule
            ]

        if not body_event_list:
            self.logger.warning("message_body is empty")

        self._body = pack_vertical(
            body_event_list,
            paddingAll="lg"
        )

        return 0

    # Flex MessageのFooter部のパッケージ
    def package_footer(self):

        self._footer = pack_vertical(
            [pack_text("\"Google Calendar\" を開く", url=FOOTER_URL, decoration="underline", color="#0000ff")]
        )

        if self._footer is None:
            print("None date")

        self.logger.debug("Finished set up footer")

    # Flex Messageのパッケージ
    def package_message(self, events_list):

        self.logger.debug(events_list)

        if "start_date" not in events_list:
            self.logger.warning("\"events_list\" is empty")
            return -1

        self.package_header(date=events_list['start_date'])
        self.package_body(schedule_list=events_list['schedule_list'])
        self.package_footer()

        # Bodyがない場合はエラー
        if "type" not in self._header or "type" not in self._body or "type" not in self._footer:
            self.logger.warning("Failure getting package")
            return -1

        self._message = {
            "type": "bubble",
            "size": "mega",
            "header": self._header,
            "body": self._body,
            "footer": self._footer
        }

        self.logger.info("Finished set up message")

        return self._message

    def package_message_none(self):

        sample_path = os.path.join(HOME_ABSPATH, message_template_folder_name, "body_event.json")

        self._message = self.load_json(path=sample_path)
        self.logger.info("Set up sample_message")

        return self._message

    # 一週間のスケジュールを出力する用(carouselで日にちごとにbubbleを作成してメッセージを作成)
    def package_carousel_message(self, events_list: dict):

        bubble_dict = []

        if events_list is None:
            self.logger.warning("\"events_list\" is empty")
            return -1

        for event in events_list:

            if event is None:
                self.logger.warning("\"events_list\" is empty")
                return -1

            self.package_header()
            self.package_body(schedule_list=event)
            self.package_footer()

            bubble_dict.append(
                {
                    "type": "bubble",
                    "size": "mega",
                    "header": self._header,
                    "body": self._body,
                    "footer": self._footer
                }
            )
        self.logger.debug("call package_carousel_message")
        return self._message
