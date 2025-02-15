# "make"で実行
default:
	python -O main.py

# "make" オプション
.PHONY: FLASK_LOCAL

# "make FLASK_LOCAL"
# local環境での接続確認用
FLASK_LOCAL:
	set FLASK_APP=app.py
	set FLASK_DEBUG=1
	flask run --reload --port 8080

# "make" オプション
.PHONY: NGROK_RUN

# ngrokの起動
NGROK_RUN:
	ngrok http 8080

# "make" オプション
.PHONY: FLASK_RENDER

# 運用用
FLASK_RENDER:
	gunicorn app:app --workers 4 --threads 2 --max-requests 500

