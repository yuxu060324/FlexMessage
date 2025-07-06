import sys
import json
import logging
from logging import StreamHandler
import urllib.request
from dotenv import load_dotenv
from common_variable import *


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


# URL check
def checkURL(url):
	logger.debug(f'Valid URL: {url}')
	try:
		f = urllib.request.urlopen(url=url)
		logger.debug(f'URL OK: {url}')
		f.close()
		return True
	except Exception:
		logger.warning(f'URL is not found: {url}')
		return False


# 環境変数の設定(基本的にDebug環境での呼出を想定)
def set_environ(build_env: str):

	if os.getenv("SET_BUILD") == "":
		# エラーログを出力
		logger.warning("The environment variable “SET_BUILD” is not set to a value")
		return None

	if os.getenv("SET_BUILD") == "LOCAL":
		env_dir_path = DOTENV_DIR_PATH_LOCAL
	elif os.getenv("SET_BUILD") == "FLASK_RENDER":
		env_dir_path = DOTENV_DIR_PATH_RENDER
	else:
		# エラーログを出力
		logger.warning("The environment variable “SET_BUILD” has an unexpected value")
		return None

	# MessagingAPI(LINE)用環境変数の設定
	load_dotenv(os.path.join(env_dir_path, linebot_env_file_name))

	# Google Calendar API用の環境変数の設定
	if build_env == "INSTALL":
		load_dotenv(os.path.join(env_dir_path, google_auth_install_env_file_name))
	else:
		load_dotenv(os.path.join(env_dir_path, google_auth_env_file_name))

	return


# loggerの定義
logger = getMyLogger(__name__)

