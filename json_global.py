import os

HOME_ABSPATH = os.path.abspath(".//")

DAY_OF_WEEK_LIST = ["月", "火", "水", "木", "金", "土", "日"]

message_template_folder_name = "FlexMessageDictionary"

header_file_name = "header.json"
footer_file_name = "footer.json"

icon_folder_name = "icon_image"
event_icon_folder_name = "event"
weather_icon_folder_name = "weather"

# -------------------------------
# 他ファイルから参照する変数
# -------------------------------

HEADER_FILE_PATH = os.path.join(HOME_ABSPATH, message_template_folder_name, header_file_name)
FOOTER_FILE_PATH = os.path.join(HOME_ABSPATH, message_template_folder_name, footer_file_name)
ICON_EVENT_FOLDER_PATH = os.path.join(HOME_ABSPATH, icon_folder_name, event_icon_folder_name)
ICON_WEATHER_FOLDER_PATH = os.path.join(HOME_ABSPATH, icon_folder_name, weather_icon_folder_name)

# イベントアイコンのファイルパス
ICON_EVENT_FILE = {
    "task": "task.jpg",
    "event": "event.jpg",
    "game": "game.jpg",
    "commu": "commu.jpg",
    "other": "other.jpg",
}

# 天気アイコンのファイルパス
ICON_WEATHER_FILE = {
    "sunny": "sunny.jpg",
    "rain": "rain.jpg",
    "cloudy": "cloudy.jpg",
    "snow": "snow.jpg",
}

