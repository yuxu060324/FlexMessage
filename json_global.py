import os
from common_global import *

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

DAY_OF_WEEK_LIST = ["月", "火", "水", "木", "金", "土", "日"]

message_template_folder_name = "FlexMessageDictionary"

icon_folder_name = "icon_image"
event_icon_folder_name = os.path.join(icon_folder_name, "event")
weather_icon_folder_name = os.path.join(icon_folder_name, "weather")
output_icon_folder_name = os.path.join(icon_folder_name, "out")

# 天候コードをまとめているJSONファイル名
weather_code_list_file_name = "weatherCodeList.json"

# -------------------------------
# jsonControl.py から参照する変数
# -------------------------------

# 予定のアイコンを格納しているフォルダ
ICON_EVENT_FOLDER_PATH = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH, event_icon_folder_name)
# 天気のアイコンを格納しているフォルダ
ICON_WEATHER_FOLDER_PATH = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH, weather_icon_folder_name)
# 作成したアイコンを格納しているフォルダ
ICON_OUTPUT_FOLDER_PATH = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH, output_icon_folder_name)

# -------------------------------
# Header
# -------------------------------

# # 天気アイコンのファイルパス(実際に使うよう)
# ICON_WEATHER_FILE = {
#     "sunny": {
#         "url": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "sunny.png"),
#         "bg_color": "#ff7f50"
#     },
#     "cloudy": {
#         "url": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "cloudy.png"),
#         "bg_color": "#c0c0c0"
#     },
#     "rain": {
#         "url": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "rain.png"),
#         "bg_color": "#4169e1"
#     },
#     "snow": {
#         "url": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "snow.png"),
#         "bg_color": "#afeeee"
#     },
#     "thunder": {
#         "url": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "thunderstorm.json"),
#         "bg_color": "#ffd700"
#     },
#     "other": {
#         "url": urlparse.urljoin(ICON_WEATHER_FOLDER_PATH, "sunny.png"),
#         "bg_color": "#777777"
#     }
# }

ICON_WEATHER_FILE = {
    "sunny": {
        "url": os.path.join(HOME_ABSPATH, weather_icon_folder_name, "sunny.png"),
        "bg_color": "#ff7f50"
    },
    "cloudy": {
        "url": os.path.join(HOME_ABSPATH, weather_icon_folder_name, "cloudy.png"),
        "bg_color": "#c0c0c0"
    },
    "rain": {
        "url": os.path.join(HOME_ABSPATH, weather_icon_folder_name, "rain.png"),
        "bg_color": "#4169e1"
    },
    "snow": {
        "url": os.path.join(HOME_ABSPATH, weather_icon_folder_name, "snow.png"),
        "bg_color": "#afeeee"
    },
    "thunder": {
        "url": os.path.join(HOME_ABSPATH, weather_icon_folder_name, "thunderstorm.png"),
        "bg_color": "#ffd700"
    },
    "other": {
        "url": os.path.join(HOME_ABSPATH, weather_icon_folder_name, "sunny.png"),
        "bg_color": "#777777"
    }
}

# -------------------------------
# Hero
# -------------------------------

WEATHER_CODE_LIST_FILE_NAME = os.path.join(HOME_ABSPATH,
                                           weather_icon_folder_name, weather_code_list_file_name)
OUT_FOLDER_PATH = os.path.join(HOME_ABSPATH, output_icon_folder_name)

HERO_SIZE = (480, 270)

WEATHER_FORECAST_MAP_SIZE = (320, 180)
TEMPERATURE_SIZE = (HERO_SIZE[0]-WEATHER_FORECAST_MAP_SIZE[0], WEATHER_FORECAST_MAP_SIZE[1])
WEATHER_NAME_SIZE = (HERO_SIZE[0], HERO_SIZE[1]-WEATHER_FORECAST_MAP_SIZE[1])

HERO_POSITION_WEATHER_MAP = (0, 0)
HERO_POSITION_TEMPERATURE = (WEATHER_FORECAST_MAP_SIZE[0], 0)
HERO_POSITION_DETAIL_WEATHER = (0, WEATHER_FORECAST_MAP_SIZE[1])

# ファイル名
out_file_name_detail_weather = "detail_weather"
out_file_name_temperature = "temperature_icon"
out_file_name_weather_map = "weather_forecast_map"
out_file_name_hero = "out_hero"

# 最高/最低気温の背景/枠 の色
TEMPERATURE_MAX_BG_COLOR = "#ffc0c0"    # 最高気温の背景色
TEMPERATURE_MAX_FG_COLOR = "#ff0000"    # 最高気温の枠/文字の色
TEMPERATURE_MIN_BG_COLOR = "#c0c0ff"    # 最低気温の背景色
TEMPERATURE_MIN_FG_COLOR = "#0000ff"    # 最低気温の枠/文字の色

# heroファイル操作用
OUT_FILE_PATH_DETAIL_WEATHER = os.path.join(OUT_FOLDER_PATH, out_file_name_detail_weather + ".png")
OUT_FILE_PATH_WEATHER_MAP = os.path.join(OUT_FOLDER_PATH, out_file_name_weather_map + ".png")
OUT_FILE_PATH_TEMPERATURE = os.path.join(OUT_FOLDER_PATH, out_file_name_temperature + ".png")

# hero設定用URL
OUT_FILE_PATH_HERO = urlparse.urljoin(ICON_OUTPUT_FOLDER_PATH, out_file_name_hero + ".png")

# -------------------------------
# Body
# -------------------------------

# イベントアイコンのファイルパス
ICON_EVENT_FILE = {
    "task": urlparse.urljoin(ICON_EVENT_FOLDER_PATH, "task.png"),
    "event": urlparse.urljoin(ICON_EVENT_FOLDER_PATH, "event.png"),
    "game": urlparse.urljoin(ICON_EVENT_FOLDER_PATH, "game.png"),
    "commu": urlparse.urljoin(ICON_EVENT_FOLDER_PATH, "commu.png"),
    "eating": urlparse.urljoin(ICON_EVENT_FOLDER_PATH, "eating.png"),
    "hospital": urlparse.urljoin(ICON_EVENT_FOLDER_PATH, "hospital.png"),
    "other": urlparse.urljoin(ICON_EVENT_FOLDER_PATH, "other.png"),
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
