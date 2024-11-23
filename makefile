# "make"で実行
default:
	python main.py

# "make" オプション
.PHONY: FLASK

# "make FLASK"で実行
FLASK:
	python -O main.py