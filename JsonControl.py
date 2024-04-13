import os, re, datetime
import json
from typing import Dict, Union, Any

from json_global import HOME_ABSPATH, HEADER_FILE_PATH, FOOTER_FILE_PATH, ICON_EVENT_FILE, ICON_WEATHER_FOLDER_PATH
from json_global import BODY_EVENT_FILE_PATH, BODY_SCHEDULE_FILE_PATH
from json_global import DAY_OF_WEEK_LIST, ICON_EVENT_FILE, ICON_WEATHER_FILE


# boxで囲むだけの関数
def pack_vertical(arr: list, margin=None, spacing=None, width=None, height=None,
                  paddingAll=None, backgroundColor=None, offsetStart=None):
    pattern = {"type": "box", "layout": "vertical", "contents": arr}

    if margin is not None:
        pattern.update(margin=margin)
    if paddingAll is not None:
        pattern.update(paddingAll=paddingAll)
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

    return pattern


def pack_horizontal(arr: list, margin=None, spacing=None, width=None, height=None,
                    paddingAll=None, backgroundColor=None, offsetStart=None):
    pattern = {"type": "box", "layout": "horizontal", "contents": arr}

    if margin is not None:
        pattern.update(margin=margin)
    if paddingAll is not None:
        pattern.update(paddingAll=paddingAll)
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

    return pattern


def pack_text(str, color=None, size=None, flex=None, url=None, weight=None):
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

    return pattern


def pack_image(path):
    pattern = {"type": "image", "url": path}
    return pattern

def pack_separator():
    return {"type": "separator", "margin": "lg"}

def pack_filter():
    return {"type": "filter"}


class JsonManager:

    def __init__(self, logger):

        self.massage_json_path = os.path.abspath(".\\FlexMessageDictionary")
        self.logger = logger

        # for message
        self._message = ""
        self._header = ""
        self._event_all_day = {}
        self._event_schedule = {}
        self._body = ""
        self._footer = ""

    def load_json(self, path):

        if not os.path.isfile(path):
            self.logger.warning(f'{path} does not exist')
            return

        with open(path) as f:
            payload = json.load(f)

        return payload

    # Flex MessageのHeader部のパッケージ
    def package_header(self, weather="sunny"):

        if not os.path.isfile(HEADER_FILE_PATH):
            self.logger.warning(f'{HEADER_FILE_PATH} does not exist')
            return

        # 日付の文字列
        date_today = datetime.datetime.now()
        date_wod = DAY_OF_WEEK_LIST[date_today.weekday()]
        date_str = date_today.strftime("%m / %d ( " + date_wod + " )")

        # 天気アイコンのファイルパス
        weather_file_path = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png"  # os.path.join(ICON_WEATHER_FOLDER_PATH, ICON_WEATHER_FILE[weather])
        # if not os.path.isfile(weather_file_path):
        #     self.logger.warning(f'{weather_file_path} does not exist')
        #     return

        self._header = self.load_json(HEADER_FILE_PATH)
        self.logger.info("Finished load header_file")

        # 日付のboxの追加
        date_box = pack_vertical([
            pack_text("DATE", color="#ffffff66", size="sm"),
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

        self.logger.info("Finished set up header")

    def package_event_all_body(self, events):

        title_box = pack_horizontal(
            [pack_text("終日", size="lg")],
            spacing="lg",
            margin="xl",
        )
        temp_event = []

        for event in events:
            temp_event.append(pack_horizontal(
                [
                    pack_text(event['start_time']),
                #     icon_event
                    pack_text(event['summary'])
                ]
            ))

        event_detail = pack_vertical(temp_event)

        self._event_all_day = pack_vertical([title_box, event_detail])

        self.logger.info("Finished set up body_event")

    def package_event_schedule(self, events):

        title_box = pack_horizontal(
            [pack_text("スケジュール", size="lg")],
            spacing="lg",
            margin="xl",
        )
        temp_event = []

        for event in events:
            temp_event.append(pack_horizontal(
                [
                    pack_text(event['start_time']),
                #     icon_event
                    pack_text(event['summary'])
                ]
            ))

        event_detail = pack_vertical(temp_event)

        self._event_schedule = pack_vertical([title_box, event_detail])
        self.logger.debug(self._event_schedule)

        self.logger.info("Finished set up body_event")

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
        if not 'type' in self._event_all_day.keys() or not 'type' in self._event_schedule:
            self._body = pack_vertical([pack_text("予定なし")])
        # 終日イベントのみ
        elif not 'type' in self._event_all_day.keys():
            self._body = pack_vertical([self._event_schedule])
        # 時間範囲のあるイベントのみ
        elif not 'type' in self._event_schedule.keys():
            self._body = pack_vertical([self._event_all_day])
        # どちらも
        else:
            self._body = pack_vertical(
                [self._event_all_day, pack_separator(), self._event_schedule],
                margin="none",
                paddingAll="15px"
            )

        return 0

    # Flex MessageのFooter部のパッケージ
    def package_footer(self):

        if not os.path.isfile(FOOTER_FILE_PATH):
            self.logger.info(f'{FOOTER_FILE_PATH} does not exist')
            return

        self._footer = self.load_json(FOOTER_FILE_PATH)
        self.logger.info("Finished load footer_file")

    # Flex Messageのパッケージ
    def package_message(self):

        # Bodyがない場合はエラー
        if (self._body == ""):
            self.logger.warning("Do call this module before \"package_body\"")
            return -1

        # HeaderとFooterが無い場合はパッケージを行う
        if (self._header == ""):
            self.package_header()
        if (self._footer == ""):
            self.package_footer()

        self._message = {
            "type": "bubble",
            "size": "mega",
            "header": self._header,
            "body": self._body,
            "footer": self._footer
        }

        return self._message

    def package_message_none(self):

        sample_path = os.path.join(HOME_ABSPATH, "FlexMessageDictionary", "sample_simple.json")

        self._message = self.load_json(path=sample_path)

        return self._message
