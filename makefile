# "make"で実行
default:
	python -O main.py

# make optionの確認用
.PHONY: help
help:
	@echo make [option]
	@echo [option]: FLASK_RENDER, FLASK_LOCAL, NGROK_RUN, rich_image
	@echo FLASK_RENDER: Option for operational use, running apps on servers
	@echo FLASK_LOCAL: Option for debugging, sending line messages in the local_env.
	@echo NGROK_RUN: Option for debugging, set up server for line in local_env
	@echo rich_image: Local work options, generate rich menu images


# =====================================================
# 					本番(Render.com)用
# =====================================================

# 運用用
.PHONY: FLASK_RENDER
FLASK_RENDER:
	gunicorn app:app --workers 4 --threads 2 --max-requests 500


# =====================================================
# 					ローカル検証用
# =====================================================

# local環境での接続確認用
.PHONY: FLASK_LOCAL
FLASK_LOCAL:
	set FLASK_APP=app.py
	set FLASK_DEBUG=1
	flask run --reload --port 8080

# ngrokの起動
.PHONY: NGROK_RUN
NGROK_RUN:
	ngrok http 8080


# =====================================================
# 					ローカル動作用
# =====================================================

# リッチメニュー画像作成(ローカルテスト用)
.PHONY: rich_image
rich_image:
	python create_rich_menu_image.py

# 予定表を取得(ローカルテスト用)
.PHONY: get_schedule
get_schedule:
	python get_schedule.py



