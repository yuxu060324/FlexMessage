import requests
import os
from common_global import *
from PIL import Image

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


# マクロ定義
def WEATHER_KIND_before(weather_code):
    return int(weather_code - (weather_code % 100))/100
def WEATHER_TRANSITION(weather_code):
    return int(((weather_code % 100) - (weather_code % 10)) / 10)
def WEATHER_KIND_after(weather_code):
    return int(weather_code % 10)

# Get Weather from Japan Meteorological Agency
# @param    [in]    place_code      Code for where to get the weather (details: https://www.jma.go.jp/bosai/common/const/area.json)
# @param    [out]   weather_list    Weather list
# @discription
# - 外部公開API
# - このファイルに定義している関数は、この関数以外、直接呼び出さないようにする
def get_weather(place_code="130000"):
    jma_dict = {"temp": None, "weather": None}

    # 気象庁のAPIから東京都のjsonデータを取得
    jma_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{0}.json'.format(place_code)
    jma_json = requests.get(jma_url).json()

    # 東京地方(area_code=130010)の気象情報
    jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][-1]
    if (len(jma_weather.split("\u3000")) >= 3):
        jma_weather = jma_weather.split("\u3000")[0:3]

    # 東京地方(area_code=130010)の最高/最低気温
    jma_temp = jma_json[0]["timeSeries"][2]["areas"][0]["temps"]

    # APIから取得したデータから必要なデータを抜き出す
    jma_dict = {"temp": jma_temp, "weather": jma_weather}

    return jma_dict


def get_weather_icon(weather: list = None):
    # 返却するアイコンを格納する変数
    weather_icon = 0

    if weather is None:
        logger.info("\"weather\" is not setting value")

    # weather newsのようなレイアウトで画像を生成する

    # のち
    # ---------------
    # | 〇   >   ×  |
    # ---------------

    # ときどき
    # ---------------
    # | 〇   「   ×  |
    # ---------------

    # weather_memo.txtを参考に関数の場合分けを行う処理
    weather_code = 123
    weather_transition = WEATHER_TRANSITION(weather_code=weather_code)

    # 画像生成の場合分け
    # "晴れ"などのonly表現
    if weather_transition == 0:
        create_weather_icon_only(weather_code=weather_code)
    # "のち"の場合
    elif weather_transition == 1:
        create_weather_icon_after(weather_code=weather_code)
    # "時々"の場合
    elif weather_transition == 2:
        create_weather_icon_often(weather_code=weather_code)
    # "一時"の場合
    elif weather_transition == 3:
        create_weather_icon_temporary(weather_code=weather_code)
    # 上記のどれにも当てはまらない(Error)
    else:
        return -1

    # backgroud Image
    size = (320, 240)
    rgb_color = (0, 128, 255, 0)
    img = Image.new("RGBA", size, rgb_color)
    img_back = Image.new("RGBA", size, rgb_color)

    sunny_path = os.path.join(os.path.abspath(".\\icon_image\\weather"), "sunny.png")
    img_sunny = Image.open(sunny_path).convert('RGBA')  # sunny.pngを透過画像で開く

    img.paste(img_sunny)
    img_back = Image.alpha_composite(img_back, img)

    save_image(img_back, name="sample.png")

    return weather_icon


def save_image(img, name):
    image_path = os.path.join(os.path.abspath("./icon_image//weather"), name)

    if img is None:
        logger.warning("Image is None")
        return -1

    img.save(image_path, quality=95)


# weatherが一つ の場合の画像生成
def create_weather_icon_only(weather_code=None):

    if weather_code is None:
        logger.warning("Error get_weather_icon")
        return -1

    create_weather_icon(weather_code=weather_code)

    return


# weather = "時々" の場合の画像生成
def create_weather_icon_often(weather_code=None):

    if weather_code is None:
        logger.warning("Error get_weather_icon")
        return -1

    create_weather_icon(weather_code=weather_code)

    return


# weather = "のち" の場合の画像生成
def create_weather_icon_after(weather_code=None):

    if weather_code is None:
        logger.warning("Error get_weather_icon")
        return -1

    create_weather_icon(weather_code=weather_code)

    return


# weather = "一時" の場合の画像生成
def create_weather_icon_temporary(weather_code=None):

    if weather_code is None:
        logger.warning("Error get_weather_icon")
        return -1

    create_weather_icon(weather_code=weather_code)

    return


def create_weather_icon(weather_code):

    if weather_code is None:
        logger.warning("Error")
        return -1

    logger.info("Finished create_weather_icon")

    return
