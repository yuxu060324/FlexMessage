import os
from datetime import datetime
from common_global import *

try:
	import urlparse
except ImportError:
	import urllib.parse as urlparse

DAY_OF_WEEK_LIST = ["月", "火", "水", "木", "金", "土", "日"]

message_template_folder_name = "TemplateMessage"

icon_folder_name = "image/"
event_icon_folder_name = "event/"
weather_icon_folder_name = "weather/"
output_folder_name = "out/"

# 天候コードをまとめているJSONファイル名
weather_code_list_file_name = "weatherCodeList.json"

# -------------------------------
# jsonControl.py から参照する変数
# -------------------------------

# URL用のURL
GITHUB_PROJECT_CONTENT_PATH_IMAGE = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH, icon_folder_name)
RENDER_PROJECT_PATH_IMAGE = urlparse.urljoin(RENDER_PROJECT_URL, output_folder_name)

# 予定のアイコンを格納しているフォルダ
ICON_EVENT_FOLDER_URL = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH_IMAGE, event_icon_folder_name)
# 作成したアイコンを格納しているフォルダ
ICON_OUTPUT_FOLDER_URL = urlparse.urljoin(GITHUB_PROJECT_CONTENT_PATH_IMAGE, output_folder_name)

# -------------------------------
# Header
# -------------------------------

# "DATE"
HEADER_TEXT_DATE = "DATE"
HEADER_TEXT_DATE_COLOR = "#ffffffB0"
HEADER_TEXT_DATE_SIZE = "sm"

# text of date
HEADER_TEXT_COLOR = "#c00000"
HEADER_TEXT_SIZE = "xl"

HEADER_BACK_COLOR = "#0367D3"

# -------------------------------
# Hero
# -------------------------------

WEATHER_PATH = os.path.join(HOME_ABSPATH, icon_folder_name, weather_icon_folder_name)		# 天気の画像が保存されているPATH
OUT_DEFAULT_WEATHER_IMAGE_FILE_NAME = "out_weather_image_default.png"						# エラー時に返す天気画像のファイル名

ICON_WEATHER_FILE = {
	"sunny": {
		"url": os.path.join(WEATHER_PATH, "sunny.png"),
		"bg_color": "#ff7f50"
	},
	"cloudy": {
		"url": os.path.join(WEATHER_PATH, "cloudy.png"),
		"bg_color": "#c0c0c0"
	},
	"rain": {
		"url": os.path.join(WEATHER_PATH, "rain.png"),
		"bg_color": "#4169e1"
	},
	"snow": {
		"url": os.path.join(WEATHER_PATH, "snow.png"),
		"bg_color": "#afeeee"
	},
	"thunder": {
		"url": os.path.join(WEATHER_PATH, "thunderstorm.png"),
		"bg_color": "#ffd700"
	},
	"other": {
		"url": os.path.join(WEATHER_PATH, "sunny.png"),
		"bg_color": "#777777"
	}
}

WEATHER_CODE = {
	"1": "sunny",
	"2": "cloudy",
	"3": "rain",
	"4": "snow",
	"5": "thunder"
}

WEATHER_CODE_LIST_FILE_NAME = os.path.join(HOME_ABSPATH, icon_folder_name, weather_icon_folder_name, weather_code_list_file_name)
OUT_FOLDER_PATH = os.path.join(HOME_ABSPATH, icon_folder_name, output_folder_name)

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
out_file_name_hero = "out_weather_"

# 最高/最低気温の背景/枠 の色
TEMPERATURE_MAX_BG_COLOR = "#ffc0c0"    # 最高気温の背景色
TEMPERATURE_MAX_FG_COLOR = "#ff0000"    # 最高気温の枠/文字の色
TEMPERATURE_MIN_BG_COLOR = "#c0c0ff"    # 最低気温の背景色
TEMPERATURE_MIN_FG_COLOR = "#0000ff"    # 最低気温の枠/文字の色

# heroファイル操作用
OUT_FILE_PATH_DETAIL_WEATHER = os.path.join(OUT_FOLDER_PATH, out_file_name_detail_weather + ".png")
OUT_FILE_PATH_WEATHER_MAP = os.path.join(OUT_FOLDER_PATH, out_file_name_weather_map + ".png")
OUT_FILE_PATH_TEMPERATURE = os.path.join(OUT_FOLDER_PATH, out_file_name_temperature + ".png")

# -------------------------------
# Body
# -------------------------------

# イベントアイコンのファイルパス
ICON_EVENT_FILE = {
	"task": urlparse.urljoin(ICON_EVENT_FOLDER_URL, "task.png"),
	"event": urlparse.urljoin(ICON_EVENT_FOLDER_URL, "event.png"),
	"game": urlparse.urljoin(ICON_EVENT_FOLDER_URL, "game.png"),
	"commu": urlparse.urljoin(ICON_EVENT_FOLDER_URL, "commu.png"),
	"eating": urlparse.urljoin(ICON_EVENT_FOLDER_URL, "eating.png"),
	"hospital": urlparse.urljoin(ICON_EVENT_FOLDER_URL, "hospital.png"),
	"other": urlparse.urljoin(ICON_EVENT_FOLDER_URL, "other.png"),
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

FOOTER_URL = "https://www.google.com/"
GOOGLE_CALENDAR_URL = 'https://calendar.google.com/calendar/u/0/r'
