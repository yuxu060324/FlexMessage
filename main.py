# ローカル環境で動作を確認するためのファイル

from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage
from common_global import *
import argparse
from MainClass import MainApp

# ビルドオプションの取得
parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=["massage", "image"], default="message")
args = parser.parse_args()

os.environ["SET_BUILD"] = "LOCAL"

# テスト環境で使用する変数を環境変数に登録
set_environ(build_env="")

# LINEBotのアクセストークンの初期設定
line_bot_api = LineBotApi(os.environ['LINE_BOT_CHANNEL_ACCESS_TOKEN'])

main_app = MainApp()

# main( for debug )
def main():

	payload = main_app.create_schedule_message_week()

	# デバッグ用
	# debug_file_path = os.path.join(HOME_ABSPATH, "TemplateMessage", "debug_message.json")
	# with open(debug_file_path, mode="w", encoding="utf-8") as f:
	# 	json.dump(payload, f, ensure_ascii=False, indent=4)

	if payload is not None:
		# FlexMessageを作成(まだlineは送らない)
		container_obj = FlexSendMessage(alt_text='Test Message', contents=payload)
		# ここでlineに通知が行く
		line_bot_api.push_message(os.environ['USER_ID'], messages=container_obj)
	else:
		logger.info("This transaction is failed")


if __name__ == "__main__":
	logger.info("---------- Start(Mode: Debug) --------------")
	if args.mode == "message":
		main()
	else:
		exit(0)
	logger.info("---------- End(Mode: Debug) --------------")
