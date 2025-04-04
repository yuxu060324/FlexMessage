from linebot import LineBotApi
from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuAlias,
    RichMenuSize,
    RichMenuBounds,
    MessageAction,
    URIAction,
)
from linebot.models.actions import RichMenuSwitchAction
from create_rich_menu_image import *
from common_global import *

if os.environ.get("SET_BUILD") == None:
    set_environ("LOCAL")

line_bot_api = LineBotApi(os.environ["LINE_BOT_CHANNEL_ACCESS_TOKEN"])

# リッチメニューを削除する
def reset_rich_menu():
    logger.debug("リッチメニューを削除します")

    # リッチメニューの全aliasを選択して削除する
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

    # 全リッチメニューを選択して削除する
    for rich_menu_alias in line_bot_api.get_rich_menu_alias_list().aliases:
        line_bot_api.delete_rich_menu_alias(rich_menu_alias.rich_menu_alias_id)


# 画像をリッチメニューに設定する
def set_image(rich_menu_id, rich_menu_image_path):
    logger.debug("画像をリッチメニューに設定します。")
    with open(rich_menu_image_path, "rb") as file:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", file)
    return


# リッチメニューのオブジェクトを作成する
def create_rich_menu_object():
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=RICH_MENU_POSITION_TODAY_SCHEDULE[0],
                y=RICH_MENU_POSITION_TODAY_SCHEDULE[1],
                width=RICH_MENU_SIZE_ONE[0],
                height=RICH_MENU_SIZE_ONE[1]
            ),
            action=MessageAction(text=LINE_MESSAGE_ACTION_LIST[0])
        ),
        RichMenuArea(
            bounds=RichMenuBounds(
                x=RICH_MENU_POSITION_TOMORROW_SCHEDULE[0],
                y=RICH_MENU_POSITION_TOMORROW_SCHEDULE[1],
                width=RICH_MENU_SIZE_ONE[0],
                height=RICH_MENU_SIZE_ONE[1]
            ),
            action=MessageAction(text=LINE_MESSAGE_ACTION_LIST[1])
        ),
        RichMenuArea(
            bounds=RichMenuBounds(
                x=RICH_MENU_POSITION_WEEK_SCHEDULE[0],
                y=RICH_MENU_POSITION_WEEK_SCHEDULE[1],
                width=RICH_MENU_SIZE_ONE[0],
                height=RICH_MENU_SIZE_ONE[1]
            ),
            action=MessageAction(text=LINE_MESSAGE_ACTION_LIST[2])
        )
    ]

    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=RICH_MENU_SIZE[0], height=RICH_MENU_SIZE[1]/2),
        selected=True,
        name="plan_rich_menu",
        chat_bar_text="メニュー",
        areas=areas
    )

    logger.debug("リッチメニューの判定を作成します。")

    return line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)


# デフォルトのリッチメニューを設定する
def set_default_rich_menu(rich_menu_id):
    logger.debug("リッチメニューのデフォルトを設定します")
    line_bot_api.set_default_rich_menu(rich_menu_id=rich_menu_id)


# リッチメニューのaliasの登録
def set_rich_menu_alias(rich_menu_id, rich_menu_alias_id):
    logger.debug("リッチメニューのエイリアスを設定します")
    alias = RichMenuAlias(
        rich_menu_alias_id=rich_menu_alias_id,
        rich_menu_id=rich_menu_id
    )
    line_bot_api.create_rich_menu_alias(alias)


def set_rich_menu():

    try:

        logger.debug("リッチメニューの設定を行います.")

        # リッチメニューのリセット
        reset_rich_menu()

        # リッチメニューの作成
        rich_menu_id = create_rich_menu_object()

        # リッチメニューに画像をアップロードする
        create_rich_menu_image_simple()
        set_image(rich_menu_id=rich_menu_id, rich_menu_image_path=GET_IMG_RICH_MENU_URL)

        # デフォルトのリッチメニューに設定する
        set_default_rich_menu(rich_menu_id=rich_menu_id)

        # リッチメニューのエイリアスを作成する
        set_rich_menu_alias(rich_menu_id=rich_menu_id, rich_menu_alias_id="rich_menu-alias")

        logger.debug("リッチメニューの設定が完了しました.")

    except Exception as ex:
        logger.debug("リッチメニューの設定に失敗しました。")
        logger.warning(f'{ex.__class__.__name__}: {ex}')
        return False

