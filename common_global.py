# 全ファイルで使用できるグローバル変数の定義
import logging
import os

# filepath
log_file_name = "project"
log_file_path = os.path.join(os.path.abspath("."), "log", f'{log_file_name}.log')

# logger
def getMyLogger(name):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-9s %(asctime)s [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger



