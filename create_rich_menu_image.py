import os
import PIL
from PIL import Image, ImageDraw, ImageFont

# file path
HOME_ABSPATH = os.path.dirname(os.path.abspath(__file__))
FILE_NAME_RICH_MENU_IMAGE = "rich_menu.png"
IMG_RICH_MENU_PATH = os.path.join(HOME_ABSPATH, "image/out", FILE_NAME_RICH_MENU_IMAGE)

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


def save_image(img: PIL.Image.Image):
    img.save(IMG_RICH_MENU_PATH, quality=95)
    print(f'save: {IMG_RICH_MENU_PATH}')
    return


def image_init():

    # ベース画像
    img = PIL.Image.new("RGB", RICH_MENU_SIZE, (255, 255, 255))
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


if __name__ == "__main__":

    if os.environ.get("SET_BUILD") == "FLASK_RENDER":
        raise EnvironmentError("フォントファイル(.ttk)がないため、運用環境では実行しないでください。")

    image_init()

