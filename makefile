# "make"�Ŏ��s
default:
	python -O main.py

# "make" �I�v�V����
.PHONY: FLASK_LOCAL

# "make FLASK_LOCAL"
# local���ł̐ڑ��m�F�p
FLASK_LOCAL:
	set FLASK_APP=app.py
	set FLASK_DEBUG=1
	flask run --reload --port 8080

# "make" �I�v�V����
.PHONY: NGROK_RUN

# ngrok�̋N��
NGROK_RUN:
	ngrok http 8080

# "make" �I�v�V����
.PHONY: FLASK_RENDER

# �^�p�p
FLASK_RENDER:
	gunicorn app:app --workers 4 --threads 2 --max-requests 500


# ���b�`���j���[�摜�쐬
.PHONY: rich_image

# ���b�`���j���[�̍쐬�t�@�C�����s
rich_image:
	python create_rich_menu_image.py

