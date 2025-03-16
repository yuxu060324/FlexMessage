import os
import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List

# --------------------------------
# PATH
# --------------------------------

# ABSPATH(__file__)
HOME_ABSPATH = os.path.dirname(os.path.abspath(__file__))
GITHUB_PROJECT_PATH = "https://github.com/yuxu060324/FlexMessage/"
GITHUB_PROJECT_CONTENT_PATH = "https://raw.githubusercontent.com/yuxu060324/FlexMessage/master/"
RENDER_PROJECT_URL = "https://lineplanbotyamanaka.onrender.com/"
log_file_name = "project"

# path for debug
DEBUG_OUTPUT_IMAGE_URL = "https://raw.githubusercontent.com/yuxu060324/FlexMessage/master/image/out/out_hero.png"

# --------------------------------
# environ variable
# --------------------------------

# GoogleAPI用(初期インストール)が設定されているかを確認する環境変数のリスト
ENV_NAME_GOOGLE = [
    "GOOGLE_CALENDAR_CREDENTIALS_TOKEN",
    "GOOGLE_CALENDAR_CREDENTIALS_REFRESH_TOKEN",
    "GOOGLE_CALENDAR_CREDENTIALS_TOKEN_URI",
    "GOOGLE_CALENDAR_CREDENTIALS_CLIENT_ID",
    "GOOGLE_CALENDAR_CREDENTIALS_CLIENT_SECRET",
    "GOOGLE_CALENDAR_CREDENTIALS_SCOPES",
    "GOOGLE_CALENDAR_CREDENTIALS_EXPIRY",
]

# GoogleAPI用(インストール済み)が設定されているかを確認する環境変数のリスト
ENV_NAME_GOOGLE_INSTALLED = [
    "GOOGLE_CALENDAR_INSTALL_CLIENT_ID",
    "GOOGLE_CALENDAR_INSTALL_PROJECT_ID",
    "GOOGLE_CALENDAR_INSTALL_AUTH_URI",
    "GOOGLE_CALENDAR_INSTALL_TOKEN_URI",
    "GOOGLE_CALENDAR_INSTALL_AUTH_PROVIDER",
    "GOOGLE_CALENDAR_INSTALL_CLIENT_SECRET",
    "GOOGLE_CALENDAR_INSTALL_REDIRECT_URIS",
]

# LINEからのメッセージとして、固有の処理を行うメッセージの配列
LINE_MESSAGE_ACTION_LIST = [
    "@TodaySchedule",                       # 今日の予定を通知する処理を実行
    "@TomorrowSchedule",                    # 明日の予定を通知する処理を実行
    "@WeekSchedule"                         # 1週間の予定を通知する処理を実行
]


# Google Calendarで取得する予定の種類
class schedule_kind(Enum):
    TODAY = 0,
    TOMORROW = 1,
    WEEKLY = 2,
    NUM_KIND = 3


@dataclass
class RichMenuSizeStruct:
    width: int
    height: int


@dataclass
class RichMenuBoundsStruct:
    x: int
    y: int
    width: int
    height: int


@dataclass
class RichMenuAreasStruct:
    bounds: RichMenuBoundsStruct
    action: dict


@dataclass
class RichMenuObjectStruct:
    size: RichMenuSizeStruct
    selected: bool
    name: str
    chatBarText: str
    areas: List[RichMenuAreasStruct]


# 各イベントの詳細情報
@dataclass
class EventDetail:
    start_date: datetime.datetime
    end_date: datetime.datetime
    title: str
    description: str
    colorId: str


# 日付のイベント情報
@dataclass
class SortEventList:
    data: datetime.datetime
    all_day_event: list
    schedule_event: list


# すべてのイベント情報
@dataclass
class EventsList:
    start_date: datetime.datetime
    end_date: datetime.datetime
    sort_event_list: list
