# 全ファイルで使用できるグローバル変数の定義
import os
import logging
from enum import Enum

# filepath
base_path = os.path.abspath(".//")
log_file_name = "project"
log_file_path = os.path.join(os.path.abspath("."), "log", f'{log_file_name}.log')

# logger
def getMyLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-9s %(asctime)s [%(filename)s:%(lineno)d %(funcName)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class schedule_start(Enum):
    TODAY = 1,
    TOMORROW = 2,
    MONDAY = 3,
    MONTH = 4


class schedule_end(Enum):
    ONE_DAY = 1,
    WEEKLY = 2,
    MONTH = 3


