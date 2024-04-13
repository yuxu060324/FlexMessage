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


class JsonManager:

    def __init__(self, logger):

        self.massage_json_path = os.path.abspath(".\\FlexMessageDictionary")
        self.logger = logger

        # for message
        self._message = ""
        self._header = ""
        self._event = {}
        self._schedule = {}
        self._body = ""
        self._footer = ""

    def load_json(self, path):

        if not os.path.isfile(path):
            print("This file_path does not exist")
            return

        with open(path) as f:
            payload = json.load(f)

        return payload

    # def make_one_schedule_contents(self, type, schedule):
    #
    #     if re.match(r'^\d{4}-\d{2}-\d{2}$', schedule[0]):
    #
    #         start_date = '{0:%m月%d日}'.format(datetime.datetime.strptime(schedule[1], '%Y-%m-%d'))
    #
    #         contents = [
    #             {
    #                 "type": type,
    #                 "text": '{0} All Day'.format(start_date),
    #                 "size": "sm"
    #             },
    #             {
    #                 "type": type,
    #                 "text": schedule[2],
    #                 "size": "sm"
    #             }
    #         ]
    #
    #     else:
    #
    #         start_time = '{0:%m月%d日 %H:%M}'.format(
    #             datetime.datetime.strptime(schedule[0], '%Y-%m-%dT%H:%M:%S+09:00'))
    #         end_time = '{0:%H:%M}'.format(datetime.datetime.strptime(schedule[1], '%Y-%m-%dT%H:%M:%S+09:00'))
    #
    #         contents = [
    #             {
    #                 "type": type,
    #                 "text": '{0} ~ {1}'.format(start_time, end_time),
    #                 "size": "sm"
    #             },
    #             {
    #                 "type": type,
    #                 "text": schedule[2],
    #                 "size": "sm"
    #             }
    #         ]
    #
    #     return contents

    # Flex MessageのHeader部のパッケージ
    def package_header(self, weather="sunny"):

        if not os.path.isfile(HEADER_FILE_PATH):
            self.logger.warning(f'{HEADER_FILE_PATH} does not exist')
            return

        # 日付の文字列
        date_today = datetime.datetime.now()
        date_wod = DAY_OF_WEEK_LIST[date_today.weekday()]
        date_str = date_today.strftime("%m 月 %d 日 ( " + date_wod + " )")

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

    def package_event(self, event):

        self.logger.info("Finished set up body_event")

    def package_schedule(self, event):

        self.logger.info("Finished set up body_event")

    # Flex MessageのBody部のパッケージ
    def package_body(self, schedule_list):

        for event in schedule_list:
            if event['all_day'] == "True":
                self.package_event(event)
            elif event['all_day'] == "False":
                self.package_schedule(event)
            else:
                self.logger.warning("\"all_day\" is Unexpected parameters")
                return -1

        # 予定なし
        if self._event.get("type", False) and self._schedule.get("type", False):
            self._body = pack_vertical([pack_text("予定なし")])
        # 終日イベントのみ
        elif self._event.get("type", False):
            self._body = pack_vertical([self._schedule])
        # 時間範囲のあるイベントのみ
        elif self._schedule.get("type", False):
            self._body = pack_vertical([self._event])
        # どちらも
        else:
            self._body = pack_vertical(
                [self._event, pack_separator(), self._schedule],
                margin="none",
                paddingAll="20px"
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
