import requests
import os
from common_global import *
from json_global import *
from PIL import Image, ImageDraw, ImageFont
from urllib import request, error

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


# マクロ定義
def WEATHER_KIND_before(weather_code: int):
    return int((weather_code - (weather_code % 100)) / 100)


def WEATHER_TRANSITION(weather_code):
    return int(((weather_code % 100) - (weather_code % 10)) / 10)


def WEATHER_KIND_after(weather_code):
    return int(weather_code % 10)


def match_image(base_img, paste_img, position):
    base_img = base_img.convert('RGBA')
    paste_img = paste_img.convert('RGBA')

    # 背景と同サイズの透明な画像を生成
    img_clear = Image.new("RGBA", base_img.size, (255, 255, 255, 0))

    # 透明画像の上にペースト
    img_clear.paste(paste_img, position)

    # 重ね合わせる
    base_img = Image.alpha_composite(base_img, img_clear)

    return base_img


def save_image(img, name):
    if not os.path.isdir(os.path.abspath("./icon_image/out")):
        logger.warning(f'create dir path: ./icon_image/out')
        return -1

    image_path = os.path.join(os.path.abspath("./icon_image/out"), name + ".png")

    if img is None:
        logger.warning("Image is None")
        return -1

    img.save(image_path, quality=95)


def get_sample_weather_icon(weather_code=None):
    # 返却するアイコンを格納する変数
    weather_code = 123

    if weather_code is None:
        logger.info("\"weather\" is not setting value")

    # weather_memo.txtを参考に関数の場合分けを行う処理
    # weather_icon = create_weather_icon(weather_code=weather_code)

    # if weather_icon is None:
    #     logger.warning("Cannot create to weather_icon")
    #     return None

    # backgroud Image
    size = (320, 240)
    rgb_color = (0, 128, 255, 0)
    img = Image.new("RGBA", size, rgb_color)
    img_back = Image.new("RGBA", size, rgb_color)

    sunny_path = os.path.join(os.path.abspath(".\\icon_image\\weather"), "sunny.png")
    img_sunny = Image.open(sunny_path).convert('RGBA')  # sunny.pngを透過画像で開く

    img.paste(img_sunny)
    img_back = Image.alpha_composite(img_back, img)

    save_image(img_back, name="weather_test")

    return


# weatherが一つ の場合の画像生成
def create_weather_icon_only(weather_before=None):
    if weather_before is None:
        logger.warning(f'Error:weather_before is setting undefined value(weather_before:{weather_before})')
        return None

    img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
                    color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])

    wimg = img.size[0]
    himg = img.size[1]

    # 天気アイコンの合わせこみ

    weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))

    # 変更前のアイコン表示位置 (wimg/4, himg/2)
    before_position = (int(wimg / 2) - int(weather_img_before.size[0] / 2),
                       int(himg / 2) - int(weather_img_before.size[1] / 2))

    img = match_image(base_img=img, paste_img=weather_img_before, position=before_position)

    # 画像の保存
    save_image(img, name="weather_forecast_map")

    logger.info("Finished create to weather_icon(Only)")

    return


# weather = "時々" の場合の画像生成
def create_weather_icon_often(weather_before=None, weather_after=None):
    if weather_before is None and weather_after is None:
        logger.warning(
            f'Error:weather_before or weather_after are setting undefined value(weather_before:{weather_before}, weather_after_after:{weather_after})')
        return None

    img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
                    color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])
    draw = ImageDraw.Draw(img)

    wimg = img.size[0]
    himg = img.size[1]

    draw.polygon(
        [((wimg * 3) / 7, himg), (wimg / 2, himg / 3), (wimg, himg / 3), (wimg, himg)],
        fill=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["bg_color"],
    )
    draw.line([((wimg * 3) / 7, himg), (wimg / 2, himg / 3)], fill="white", width=3)
    draw.line([(wimg / 2, himg / 3), (wimg, himg / 3)], fill="white", width=3)

    # 天気アイコンの合わせこみ

    weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))
    weather_img_after = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["url"]).resize((100, 100))

    # 変更前のアイコン表示位置 (wimg/4, himg/2)
    before_position = (
    int(wimg / 4) - int(weather_img_before.size[0] / 2), int(himg / 2) - int(weather_img_before.size[1] / 2))
    # 遷移後のアイコン表示位置 -> ((wimg*2)/4, himg/2)
    after_position = (
    int((wimg * 3) / 4) - int(weather_img_after.size[0] / 2), int((himg * 2) / 3) - int(weather_img_after.size[1] / 2))

    img = match_image(base_img=img, paste_img=weather_img_before, position=before_position)
    img = match_image(base_img=img, paste_img=weather_img_after, position=after_position)

    # 画像の保存
    save_image(img, name="weather_forecast_map")

    logger.info("Finished create to weather_icon(often)")

    return


# weather = "のち" の場合の画像生成
def create_weather_icon_after(weather_before=None, weather_after=None):
    if weather_before is None and weather_after is None:
        logger.warning(
            f'Error:weather_before or weather_after are setting undefined value(weather_before:{weather_before}, weather_after_after:{weather_after})')
        return None

    # ベース画像の作成

    img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
                    color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])
    draw = ImageDraw.Draw(img)

    wimg = int(img.size[0])
    himg = int(img.size[1])

    draw.polygon(
        [((wimg * 3) / 7, 0), ((wimg * 4) / 7, himg / 2), ((wimg * 3) / 7, himg), (wimg, himg), (wimg, 0)],
        fill=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["bg_color"],
    )
    draw.line([((wimg * 3) / 7, 0), ((wimg * 4) / 7, himg / 2)], fill="white", width=3)
    draw.line([((wimg * 4) / 7, himg / 2), ((wimg * 3) / 7, himg)], fill="white", width=3)

    # 天気アイコンの合わせこみ

    weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))
    weather_img_after = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["url"]).resize((100, 100))

    # 変更前のアイコン表示位置 (wimg/4, himg/2)
    before_position = (
    int(wimg / 4) - int(weather_img_before.size[0] / 2), int(himg / 2) - int(weather_img_before.size[1] / 2))
    # 遷移後のアイコン表示位置 -> ((wimg*2)/4, himg/2)
    after_position = (
    int((wimg * 3) / 4) - int(weather_img_after.size[0] / 2), int(himg / 2) - int(weather_img_after.size[1] / 2))

    img = match_image(base_img=img, paste_img=weather_img_before, position=before_position)
    img = match_image(base_img=img, paste_img=weather_img_after, position=after_position)

    # 画像の保存
    save_image(img, name="weather_forecast_map")

    logger.info("Finished create to weather_icon(after)")

    return


# weather = "一時" の場合の画像生成
def create_weather_icon_temporary(weather_before=None, weather_after=None):
    if weather_before is None and weather_after is None:
        logger.warning(
            f'Error:weather_before or weather_after are setting undefined value(weather_before:{weather_before}, weather_after_after:{weather_after})')
        return None

    img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
                    color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])
    draw = ImageDraw.Draw(img)

    wimg = img.size[0]
    himg = img.size[1]

    draw.polygon(
        [((wimg * 3) / 7, himg), (wimg / 2, himg / 3), (wimg, himg / 3), (wimg, himg)],
        fill=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["bg_color"],
    )
    draw.line([((wimg * 3) / 7, himg), (wimg / 2, himg / 3)], fill="white", width=3)
    draw.line([(wimg / 2, himg / 3), (wimg, himg / 3)], fill="white", width=3)

    # 天気アイコンの合わせこみ

    weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))
    weather_img_after = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["url"]).resize((100, 100))

    # 変更前のアイコン表示位置 (wimg/4, himg/2)
    before_position = (
    int(wimg / 4) - int(weather_img_before.size[0] / 2), int(himg / 2) - int(weather_img_before.size[1] / 2))
    # 遷移後のアイコン表示位置 -> ((wimg*2)/4, himg/2)
    after_position = (
    int((wimg * 3) / 4) - int(weather_img_after.size[0] / 2), int((himg * 2) / 3) - int(weather_img_after.size[1] / 2))

    img = match_image(base_img=img, paste_img=weather_img_before, position=before_position)
    img = match_image(base_img=img, paste_img=weather_img_after, position=after_position)

    # 画像の保存
    save_image(img, name="weather_forecast_map")

    logger.info("Finished create to weather_icon(temporary)")

    return


def create_weather_icon(jma_weather_code=None):
    # パラメータチェック
    if jma_weather_code is None:
        logger.warning("weather_code is None")
        return None

    with open(WEATHER_CODE_LIST_FILE_NAME) as f:
        weather_code_list = json.load(f)
        weather_code = weather_code_list[str(jma_weather_code - (jma_weather_code % 100))][0][str(jma_weather_code)]
        logger.debug(f'exchange weather code is {weather_code}')

    # 変数の初期化
    weather_icon = None  # 返り値として設定する変数
    weather_transition = WEATHER_TRANSITION(weather_code=weather_code)
    weather_before = WEATHER_KIND_before(weather_code=weather_code)
    weather_after = WEATHER_KIND_after(weather_code=weather_code)
    logger.debug(f'weather_before: {weather_before}, weather_transition: {weather_transition}, weather_after: {weather_after}')

    # 画像生成の場合分け

    # のち
    # ---------------
    # | 〇   >   ×  |
    # ---------------

    # ときどき or 一時
    # ---------------
    # | 〇   「   ×  |
    # ---------------

    # "晴れ"などのonly表現
    if weather_transition == 0:
        weather_icon = create_weather_icon_only(weather_before=weather_before)
    # "のち"の場合
    elif weather_transition == 1:
        weather_icon = create_weather_icon_after(weather_before=weather_before, weather_after=weather_after)
    # "時々"の場合
    elif weather_transition == 2:
        weather_icon = create_weather_icon_often(weather_before=weather_before, weather_after=weather_after)
    # "一時"の場合
    elif weather_transition == 3:
        weather_icon = create_weather_icon_temporary(weather_before=weather_before, weather_after=weather_after)
    # 上記のどれにも当てはまらない(Error)
    else:
        logger.warning(f'Set undefined value in weather_transition(value:{weather_transition})')
        return None

    logger.info("Finished create_weather_icon")

    return weather_icon


def create_detail_weather(weather_detail: str):
    if weather_detail == "":
        logger.warning("weather_detail does not set info")
        return -1

    img = Image.new("RGB", WEATHER_NAME_SIZE, color="white")
    draw = ImageDraw.Draw(img)

    # 天気の詳細情報の記載
    weather_detail_position = (int(WEATHER_NAME_SIZE[0] / 2), int(WEATHER_NAME_SIZE[1] / 2))
    font = ImageFont.truetype("meiryo.ttc", 12)
    draw.text(xy=weather_detail_position,
              text=weather_detail,
              fill="black", font=font, anchor="mm")

    # 画像の保存
    save_image(img, name="detail_weather")

    logger.debug("Finished create_detail_weather()")

    return img


def create_temperature_icon(temperature_list: list):
    if len(temperature_list) < 2:
        return -1

    img = Image.new("RGB", TEMPERATURE_SIZE, color="white")
    draw = ImageDraw.Draw(img)

    # 背景色の設定
    draw.rectangle([(0, 0), (TEMPERATURE_SIZE[0], TEMPERATURE_SIZE[1] / 2)],
                   fill=TEMPERATURE_MAX_BG_COLOR,
                   outline=TEMPERATURE_MAX_FG_COLOR, width=5)
    draw.rectangle([(0, TEMPERATURE_SIZE[1] / 2), (TEMPERATURE_SIZE[0], TEMPERATURE_SIZE[1])],
                   fill=TEMPERATURE_MIN_BG_COLOR,
                   outline=TEMPERATURE_MIN_FG_COLOR, width=5)

    # 文字の記載
    temperature_max_position = (TEMPERATURE_SIZE[0] / 2, TEMPERATURE_SIZE[1] / 4)
    temperature_min_position = (TEMPERATURE_SIZE[0] / 2, (TEMPERATURE_SIZE[1] * 3) / 4)
    draw.text(xy=temperature_max_position,
              text=temperature_list[1], fill=TEMPERATURE_MAX_FG_COLOR, font_size=20, anchor="mm")
    draw.text(xy=temperature_min_position,
              text=temperature_list[0], fill=TEMPERATURE_MIN_FG_COLOR, font_size=20, anchor="mm")

    # 画像の保存
    save_image(img, name="temperature_icon")

    logger.debug("Finished create_temperature_icon()")

    return img


# Get Weather from Japan Meteorological Agency
# @param    [in]    place_code      Code for where to get the weather (details: https://www.jma.go.jp/bosai/common/const/area.json)
# @param    [out]   weather_picture_path    path of weather_picture
# @discription
# - 外部公開API
# - このファイルに定義している関数は、この関数以外、直接呼び出さないようにする
# - 天気、詳細内容、最高/最低気温の情報をまとめた画像を返り値として設定
def get_weather(place_code="130000"):
    # # デバッグ用の処理
    # return OUT_FILE_PATH_HERO

    # 気象庁のAPIから東京都のjsonデータを取得
    jma_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{0}.json'.format(place_code)
    try:
        jma_json = requests.get(jma_url).json()
    except Exception as e:
        logger.warning("Could not get JSON data from JMA API.")
        logger.warning(f'{e.__class__.__name__}: {e}')
        return None

    # 気象情報(詳細な情報)
    jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][-1]
    jma_weather = jma_weather.replace("\u3000", " ")    # 空白文字の置き換え
    logger.info(f"weather: {jma_weather}")
    try:
        create_detail_weather(jma_weather)
    except Exception as e:
        logger.warning(f'ERROR: create_detail_weather(): jma_weather={jma_weather}')
        logger.warning(f'{e.__class__.__name__}: {e}')
        return None

    # 天気コードの情報取得
    jma_weather_code = int(jma_json[0]["timeSeries"][0]["areas"][0]["weatherCodes"][-1])
    logger.info(f"weather_code: {jma_weather_code}")
    try:
        create_weather_icon(jma_weather_code)
    except Exception as e:
        logger.warning(f'ERROR: create_weather_icon(): jma_weather_code={jma_weather_code}')
        logger.warning(f'{e.__class__.__name__}: {e}')
        return None

    # 東京地方(area_code=130010)の最高/最低気温
    jma_temp = jma_json[0]["timeSeries"][2]["areas"][0]["temps"]
    logger.info(f"temps: {jma_temp}")
    try:
        create_temperature_icon(jma_temp)
    except Exception as e:
        logger.warning(f'ERROR: create_temperature_icon(): jma_temp={jma_temp}')
        logger.warning(f'{e.__class__.__name__}: {e}')
        return None

    # 作成した画像から一つの画像を作成する

    img = Image.new("RGB", size=HERO_SIZE, color="#000000")
    weather_forecast_map_img = Image.open(OUT_FILE_PATH_WEATHER_MAP)
    temperature_img = Image.open(OUT_FILE_PATH_TEMPERATURE)
    detail_weather_img = Image.open(OUT_FILE_PATH_DETAIL_WEATHER)

    img.paste(weather_forecast_map_img, HERO_POSITION_WEATHER_MAP)
    img.paste(temperature_img, HERO_POSITION_TEMPERATURE)
    img.paste(detail_weather_img, HERO_POSITION_DETAIL_WEATHER)

    save_image(img=img, name=out_file_name_hero)

    return OUT_FILE_PATH_HERO
