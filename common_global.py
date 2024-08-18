# 主にmain.pyまで使用するグローバル変数の定義
# main.pyで使用しない定義はここに公開しない用に修正する

import os
import json
import logging
import urllib.request
from enum import Enum

# Get value for setting

HOME_ABSPATH = os.path.dirname(os.path.abspath(__file__))
GITHUB_PROJECT_PATH = "https://github.com/yuxu060324/FlexMessage/"
GITHUB_PROJECT_CONTENT_PATH = "https://raw.githubusercontent.com/yuxu060324/FlexMessage/master/"
log_file_name = "project"

# logger
def getMyLogger(name):
    project_path = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(project_path, "log", f'{log_file_name}.log')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-9s %(asctime)s [%(filename)s:%(lineno)d %(funcName)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

# For line-bot
def set_env():
    key_filepath = os.path.join(HOME_ABSPATH, "Key", "line_bot_info.json")
    with open(key_filepath) as file:
        line_bot_info = json.load(file)
    os.environ['LINE_BOT_ACCESS_TOKEN'] = line_bot_info['CHANNEL_ACCESS_TOKEN']
    os.environ['USER_ID'] = line_bot_info['USER_ID']

# URL check
def checkURL(url):
    try:
        f = urllib.request.urlopen(url=url)
        f.close()
        return True
    except:
        logger.warning(f'URL is not found: {url}')
        return False

# loggerの定義
logger = getMyLogger(__name__)

# Google Calendarで取得する予定の開始日
class schedule_start(Enum):
    TODAY = 1,
    TOMORROW = 2,
    MONDAY = 3,
    MONTH = 4

# Google Calendarで取得する予定の終了日
class schedule_end(Enum):
    ONE_DAY = 1,
    WEEKLY = 2,
    MONTH = 3
