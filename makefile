# "make"�Ŏ��s
default:
	set SET_BUILD_ENV=LOCAL
	python main.py

# "make" �I�v�V����
.PHONY: FLASK_LOCAL

# "make FLASK_LOCAL"
# local���ł̐ڑ��m�F�p
FLASK_LOCAL:
	set SET_BUILD_ENV=FLASK_LOCAL
	set FLASK_APP=app.py
	set FLASK_DEBUG=1
	flask run --reload --port 8080

# "make" �I�v�V����
.PHONY: NGROK_RUN

# ngrok�̋N��
NGROK_RUN:
	ngrok http 8080

# "make" �I�v�V����
.PHONY: FLASK_HEROKU

# �^�p�p
FLASK_HEROKU:
	set SET_BUILD_ENV=FLASK_HEROKU
	set FLASK_APP = app.py
	flask run --reload --port 5000

