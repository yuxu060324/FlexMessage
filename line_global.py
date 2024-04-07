# 環境変数などのすべてのファイルで使用できる変数の定義ファイル
import os
from enum import Enum

class schedule_start(Enum):
    TODAY = 1,
    TOMORROW = 2,
    MONDAY = 3,
    MONTH = 4


class schedule_end(Enum):
    ONE_DAY = 1,
    WEEKLY = 2,
    MONTH = 3


PROJECT_CURRENT_PATH = os.path.abspath(".//")
