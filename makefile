# "make"で実行
default:
	set SET_BUILD_ENV=LOCAL
	python main.py

# "make" オプション
.PHONY: FLASK_LOCAL

# "make FLASK_LOCAL"
# local環境での接続確認用
FLASK_LOCAL:
	set SET_BUILD_ENV=FLASK_LOCAL
	set FLASK_APP=app.py
	set FLASK_DEBUG=1
	flask run --reload --port 8080

# "make" オプション
.PHONY: NGROK_RUN

# ngrokの起動
NGROK_RUN:
	ngrok http 8080

# "make" オプション
.PHONY: FLASK_HEROKU

# 運用用
FLASK_HEROKU:
	set SET_BUILD_ENV=FLASK_HEROKU
	set FLASK_APP = app.py
	flask run --reload --port 5000

