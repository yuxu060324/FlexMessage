import os
import common_global

HOME_ABSPATH = common_global.base_path

DAY_OF_WEEK_LIST = ["月", "火", "水", "木", "金", "土", "日"]

message_template_folder_name = "FlexMessageDictionary"

header_file_name = "header.json"
body_event_file_name = "body_event.json"
body_schedule_file_name = "body_schedule.json"
footer_file_name = "footer.json"

icon_folder_name = "icon_image"
event_icon_folder_name = "event"
weather_icon_folder_name = "weather"

# -------------------------------
# jsonControl.py から参照する変数
# -------------------------------

HEADER_FILE_PATH = os.path.join(HOME_ABSPATH, message_template_folder_name, header_file_name)
BODY_EVENT_FILE_PATH = os.path.join(HOME_ABSPATH, message_template_folder_name, body_event_file_name)
BODY_SCHEDULE_FILE_PATH = os.path.join(HOME_ABSPATH, message_template_folder_name, body_schedule_file_name)
FOOTER_FILE_PATH = os.path.join(HOME_ABSPATH, message_template_folder_name, footer_file_name)
ICON_EVENT_FOLDER_PATH = os.path.join(HOME_ABSPATH, icon_folder_name, event_icon_folder_name)
ICON_WEATHER_FOLDER_PATH = os.path.join(HOME_ABSPATH, icon_folder_name, weather_icon_folder_name)


# -------------------------------
# Header
# -------------------------------

# 天気アイコンのファイルパス
ICON_WEATHER_FILE = {
    "sunny": "sunny.png",
    "rain": "rain.png",
    "cloudy": "cloudy.png",
    "snow": "snow.png",
    "other": "sunny.png"
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
