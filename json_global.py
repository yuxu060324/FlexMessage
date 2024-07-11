import os
from common_global import *
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

DAY_OF_WEEK_LIST = ["月", "火", "水", "木", "金", "土", "日"]

message_template_folder_name = "FlexMessageDictionary"

icon_folder_name = "icon_image/"
event_icon_folder_name = icon_folder_name + "event/"
weather_icon_folder_name = icon_folder_name + "weather/"

# -------------------------------
# jsonControl.py から参照する変数
# -------------------------------

# 予定のアイコンを格納しているフォルダ
ICON_EVENT_FOLDER_PATH = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH, event_icon_folder_name)
# 天気のアイコンを格納しているフォルダ
ICON_WEATHER_FOLDER_PATH = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH, weather_icon_folder_name)

# -------------------------------
# Header
# -------------------------------

# 天気アイコンのファイルパス
ICON_WEATHER_FILE = {
    "sunny": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "sunny.png"),
    "cloudy": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "cloudy.png"),
    "rain": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "rain.png"),
    "snow": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "snow.png"),
    "thunder": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "thunderstorm.json"),
    "other": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "sunny.png")
}


# -------------------------------
# Body
# -------------------------------

# イベントアイコンのファイルパス
ICON_EVENT_FILE = {
    "task": "task.png",
    "event": "event.png",
    "game": "game.png",
    "commu": "commu.png",
    "eating": "eating.png",
    "hospital": "hospital.png",
    "other": "other.png",
}

EVENT_KIND = {
    "1": "eating",
    "2": "other",
    "3": "commu",
    "4": "other",
    "5": "game",
    "6": "event",
    "7": "other",
    "8": "other",
    "9": "hospital",
    "10": "other",
    "11": "task",
    "-": "other"
}


# -------------------------------
# Footer
# -------------------------------

FOOTER_URL = "https://google.com/"
GOOGLE_CALENDAR_URL = 'https://calendar.google.com/calendar/u/0/r'

# -------------------------------
# Weather Code
# -------------------------------

WEATHER_CODE = {
    "0": "sunny",
    "1": "cloudy",
    "2": "rain",
    "3": "snow",
    "4": "thunder"
}
