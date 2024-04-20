# 全ファイルで使用できるグローバル変数の定義
import os
import logging
from enum import Enum

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

logger = getMyLogger(__name__)

class schedule_start(Enum):
    TODAY = 1,
    TOMORROW = 2,
    MONDAY = 3,
    MONTH = 4


class schedule_end(Enum):
    ONE_DAY = 1,
    WEEKLY = 2,
    MONTH = 3


