import os
from PIL import Image, ImageDraw, ImageFont
from common_global import *
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

# file path
HOME_ABSPATH = os.path.dirname(os.path.abspath(__file__))
FILE_NAME_RICH_MENU_IMAGE = "rich_menu.png"
IMG_RICH_MENU_PATH = os.path.join(HOME_ABSPATH, "image", "out", FILE_NAME_RICH_MENU_IMAGE)
RENDER_PROJECT_PATH_IMAGE = urlparse.urljoin(RENDER_PROJECT_URL, "out/")
GET_IMG_RICH_MENU_URL = urlparse.urljoin(RENDER_PROJECT_PATH_IMAGE, FILE_NAME_RICH_MENU_IMAGE)

# Rich Menu Size
RICH_MENU_SIZE = (1250, 750)                                             # リッチメニュー全体のサイズ
RICH_MENU_SIZE_ONE = (RICH_MENU_SIZE[0]/3, RICH_MENU_SIZE[1]/2)         # リッチメニューの一つのサイズ

# リッチメニューの位置(左上の座標)
RICH_MENU_POSITION_TODAY_SCHEDULE = (0, 0)
RICH_MENU_POSITION_TOMORROW_SCHEDULE = (RICH_MENU_SIZE[0]/3, 0)
RICH_MENU_POSITION_WEEK_SCHEDULE = ((RICH_MENU_SIZE[0]*2)/3, 0)
RICH_MENU_POSITION_WEATHER_SCHEDULE = (0, RICH_MENU_SIZE[1]/2)
RICH_MENU_POSITION_ADD_SCHEDULE = (RICH_MENU_SIZE[0]/3, RICH_MENU_SIZE[1]/2)
RICH_MENU_POSITION_HOW_TO_USE = ((RICH_MENU_SIZE[0]*2)/3, RICH_MENU_SIZE[1]/2)


def save_image(img: Image.Image):
    img.save(IMG_RICH_MENU_PATH, quality=95)
    logger.debug(f'save: {IMG_RICH_MENU_PATH}')
    return


# 3*2のリッチメニューを作成
def image_init():

    # ベース画像
    img = Image.new("RGB", RICH_MENU_SIZE, (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("meiryo.ttc", 20)

    # 左上
    draw.rectangle((0, 0, img.width / 3, img.height / 2), fill=(255, 0, 0))
    font_position = (img.width / 6, img.height / 4)
    draw.text(xy=font_position, text="今日の予定", font=font, fill="white", anchor="mm")
    # 中央上
    draw.rectangle((img.width / 3, 0, (img.width * 2) / 3, img.height / 2), fill=(0, 255, 0))
    font_position = (img.width / 2, img.height / 4)
    draw.text(xy=font_position, text="明日の予定", font=font, fill="black", anchor="mm")
    # 右上
    draw.rectangle(((img.width * 2) / 3, 0, img.width, img.height / 2), fill=(0, 0, 255))
    font_position = ((img.width*5) / 6, img.height / 4)
    draw.text(xy=font_position, text="1週間の予定", font=font, fill="white", anchor="mm")

    # 左下
    draw.rectangle((0, img.height / 2, img.width / 3, img.height), fill=(255, 125, 0))
    font_position = (img.width / 6, (img.height*3) / 4)
    draw.text(xy=font_position, text="今日の天気", font=font, fill="black", anchor="mm")
    # 中央下
    draw.rectangle((img.width / 3, img.height / 2, (img.width * 2) / 3, img.height), fill=(125, 125, 125))
    font_position = (img.width / 2, (img.height*3) / 4)
    draw.text(xy=font_position, text="予定追加", font=font, fill="white", anchor="mm")
    # 右下
    draw.rectangle(((img.width * 2) / 3, img.height / 2, img.width, img.height), fill=(125, 0, 255))
    font_position = ((img.width*5) / 6, (img.height*3) / 4)
    draw.text(xy=font_position, text="How to use", font=font, fill="black", anchor="mm")

    save_image(img)


# お試し版のリッチメニュー作成用
def create_rich_menu_image_simple():

    logger.debug("リッチメニューの画像を作成します")

    # ベース画像
    img = Image.new("RGB", (RICH_MENU_SIZE[0], int(RICH_MENU_SIZE[1]/2)), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_FILE_PATH_MEIRYO, size=60)

    # 左上
    draw.rectangle((0, 0, img.width / 3, img.height), fill=(255, 0, 0))
    font_position = (img.width / 6, img.height / 2)
    draw.text(xy=font_position, text="今日の予定", font=font, fill="white", anchor="mm")
    # 中央上
    draw.rectangle((img.width / 3, 0, (img.width * 2) / 3, img.height), fill=(0, 255, 0))
    font_position = (img.width / 2, img.height / 2)
    draw.text(xy=font_position, text="明日の予定", font=font, fill="black", anchor="mm")
    # 右上
    draw.rectangle(((img.width * 2) / 3, 0, img.width, img.height), fill=(0, 0, 255))
    font_position = ((img.width * 5) / 6, img.height / 2)
    draw.text(xy=font_position, text="1週間の予定", font=font, fill="white", anchor="mm")

    save_image(img)

    logger.debug("リッチメニューの画像の作成が完了しました")

    return


if __name__ == "__main__":

    # if os.environ.get("SET_BUILD") == "FLASK_RENDER":
    #     raise EnvironmentError("フォントファイル(.ttk)がないため、運用環境では実行しないでください。")

    create_rich_menu_image_simple()

