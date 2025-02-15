import os
import sys
import json
import logging
from logging import StreamHandler
import urllib.request
from enum import Enum
from dotenv import load_dotenv

# Get value for setting

HOME_ABSPATH = os.path.dirname(os.path.abspath(__file__))
GITHUB_PROJECT_PATH = "https://github.com/yuxu060324/FlexMessage/"
GITHUB_PROJECT_CONTENT_PATH = "https://raw.githubusercontent.com/yuxu060324/FlexMessage/master/"
RENDER_PROJECT_URL = "https://lineplanbotyamanaka.onrender.com/"
log_file_name = "project"


# logger
def getMyLogger(name):

    my_logger = logging.getLogger(name)

    # デプロイ環境
    if os.getenv("SET_BUILD") == "FLASK_RENDER":
        my_logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(filename)s:%(lineno)d %(funcName)s] %(message)s')

        handler.setFormatter(formatter)
        my_logger.addHandler(handler)

    # デバッグ環境
    else:

        log_file_path = os.path.join(HOME_ABSPATH, "log", f'{log_file_name}.log')
        my_logger.setLevel(logging.DEBUG)

        # ディレクトリの存在確認
        if not os.path.isdir(os.path.join(HOME_ABSPATH, "log")):
            # ディレクトリの作成
            os.makedirs(os.path.join(HOME_ABSPATH, "log"))
            # ファイルの存在確認
            if not os.path.isfile(log_file_path):
                # ファイルの作成
                with open(log_file_path, "w"):
                    pass

        handler = logging.FileHandler(log_file_path, encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)-9s %(asctime)s [%(filename)s:%(lineno)d %(funcName)s] %(message)s')

        handler.setFormatter(formatter)
        my_logger.addHandler(handler)

    return my_logger


# 環境変数を設定するための関数( Debug用 = 本番ではデプロイ環境に直接設定する )
def set_env():
    google_calendar_credentials_installed = False

    # LINE FLEX MESSAGE API
    key_filepath = os.path.join(HOME_ABSPATH, "Key", "line_bot_info.json")
    with open(key_filepath) as file:
        line_bot_info = json.load(file)
    os.environ['LINE_BOT_CHANNEL_ACCESS_TOKEN'] = line_bot_info['CHANNEL_ACCESS_TOKEN']
    os.environ['LINE_BOT_CHANNEL_SECRET'] = line_bot_info['CHANNEL_SECRET']
    os.environ['USER_ID'] = line_bot_info['USER_ID']

    # すでに資格情報がインストールされている場合(token.jsonを参照)
    if google_calendar_credentials_installed:

        # GOOGLE CALENDAR API CREDENTIALS
        key_filepath = os.path.join(HOME_ABSPATH, "Key", "token.json")
        with open(key_filepath, encoding="utf-8") as file:
            google_calendar_token = json.load(file)

        for key in google_calendar_token.keys():
            environ_key = "GOOGLE_CALENDAR_CREDENTIALS_" + key.upper()
            os.environ[environ_key] = google_calendar_token[key]

        logger.info('##### テスト環境(API_Credentials)用変数を環境変数に登録しました #####')

    # 資格情報がまだインストールされていない場合
    else:

        # GOOGLE CALENDAR API INSTALL CREDENTIALS
        key_filepath = os.path.join(HOME_ABSPATH, "Key", "credentials.json")
        with open(key_filepath, encoding="utf-8") as file:
            google_calendar_install_info = json.load(file)["installed"]
        os.environ["GOOGLE_CALENDAR_INSTALL_CLIENT_ID"] = google_calendar_install_info["client_id"]
        os.environ["GOOGLE_CALENDAR_INSTALL_PROJECT_ID"] = google_calendar_install_info["project_id"]
        os.environ["GOOGLE_CALENDAR_INSTALL_AUTH_URI"] = google_calendar_install_info["auth_uri"]
        os.environ["GOOGLE_CALENDAR_INSTALL_TOKEN_URI"] = google_calendar_install_info["token_uri"]
        os.environ["GOOGLE_CALENDAR_INSTALL_AUTH_PROVIDER"] = google_calendar_install_info["auth_provider_x509_cert_url"]
        os.environ["GOOGLE_CALENDAR_INSTALL_CLIENT_SECRET"] = google_calendar_install_info["client_secret"]
        os.environ["GOOGLE_CALENDAR_INSTALL_REDIRECT_URIS"] = google_calendar_install_info["redirect_uris"][0]

        logger.info("##### テスト環境(Install_Credentials)用変数を環境変数に登録しました #####")


# URL check
def checkURL(url):
    logger.debug(f'Valid URL: {url}')
    try:
        f = urllib.request.urlopen(url=url)
        logger.debug(f'URL OK: {url}')
        f.close()
        return True
    except:
        logger.warning(f'URL is not found: {url}')
        return False


# 環境変数の設定
def set_environ(build_env: str):
    if build_env == "LOCAL":
        load_dotenv(os.path.join(HOME_ABSPATH, "Key", "local.env"))
    if build_env == "LOCAL_INSTALLED":
        load_dotenv(os.path.join(HOME_ABSPATH, "Key", "local_installed.env"))
    elif build_env == "FLASK_LOCAL":
        load_dotenv(os.path.join(HOME_ABSPATH, "Key", "flask_local.env"))
    else:
        raise ValueError


# loggerの定義
logger = getMyLogger(__name__)


# Google Calendarで取得する予定の種類
class schedule_kind(Enum):
    TODAY = 0,
    TOMORROW = 1,
    WEEKLY = 2,
    NUM_KIND = 3
