import requests
from json_global import *
from PIL import Image, ImageDraw, ImageFont

try:
	import urlparse
except ImportError:
	import urllib.parse as urlparse


# マクロ定義
def WEATHER_KIND_before(weather_code: int):
	return int((weather_code - (weather_code % 100)) / 100)
def WEATHER_TRANSITION(weather_code):
	return int(((weather_code % 100) - (weather_code % 10)) / 10)
def WEATHER_KIND_after(weather_code):
	return int(weather_code % 10)


def _match_image(base_img, paste_img, position):
	base_img = base_img.convert('RGBA')
	paste_img = paste_img.convert('RGBA')

	# 背景と同サイズの透明な画像を生成
	img_clear = Image.new("RGBA", base_img.size, (255, 255, 255, 0))

	# 透明画像の上にペースト
	img_clear.paste(paste_img, position)

	# 重ね合わせる
	base_img = Image.alpha_composite(base_img, img_clear)

	return base_img


def _save_image(img: Image, name):
	if img is None:
		logger.warning("Image is None")
		return -1

	# ディレクトリが無ければ、作成する
	os.makedirs(OUTPUT_FILE_PATH, exist_ok=True)

	# 保存する画像ファイルのパス
	image_path = os.path.join(OUTPUT_FILE_PATH, name + ".png")

	img.save(image_path, quality=95)
	logger.debug(f'Finished to save a picture: {image_path}')


# "static/image/out"フォルダにある"weather_*.png"ファイルをすべて削除
def _delete_old_images(folder='static/image/out', prefix='out_weather_'):
	for filename in os.listdir(folder):
		if filename.startswith(prefix) and filename.endswith('.png'):
			filepath = os.path.join(folder, filename)
			os.remove(filepath)
			logger.debug(f"Delete: {filepath}")


# weatherが一つ の場合の画像生成
def _create_weather_icon_only(weather_before=None):
	if weather_before is None:
		logger.warning(f'Error:weather_before is setting undefined value(weather_before:{weather_before})')
		return None

	img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
					color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])

	wimg = img.size[0]
	himg = img.size[1]

	# 天気アイコンの合わせこみ

	weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))

	# 変更前のアイコン表示位置 (wimg/4, himg/2)
	before_position = (int(wimg / 2) - int(weather_img_before.size[0] / 2),
					   int(himg / 2) - int(weather_img_before.size[1] / 2))

	img = _match_image(base_img=img, paste_img=weather_img_before, position=before_position)

	# # 画像の保存
	# save_image(img, name="weather_forecast_map")

	logger.info("Finished create to weather_icon(Only)")

	return img


# weather = "時々" の場合の画像生成
def _create_weather_icon_often(weather_before=None, weather_after=None):
	if weather_before is None and weather_after is None:
		logger.warning(
			f'Error:weather_before or weather_after are setting undefined value(weather_before:{weather_before}, weather_after_after:{weather_after})')
		return None

	img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
					color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])
	draw = ImageDraw.Draw(img)

	wimg = img.size[0]
	himg = img.size[1]

	draw.polygon(
		[((wimg * 3) / 7, himg), (wimg / 2, himg / 3), (wimg, himg / 3), (wimg, himg)],
		fill=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["bg_color"],
	)
	draw.line([((wimg * 3) / 7, himg), (wimg / 2, himg / 3)], fill="white", width=3)
	draw.line([(wimg / 2, himg / 3), (wimg, himg / 3)], fill="white", width=3)

	# 天気アイコンの合わせこみ

	weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))
	weather_img_after = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["url"]).resize((100, 100))

	# 変更前のアイコン表示位置 (wimg/4, himg/2)
	before_position = (
		int(wimg / 4) - int(weather_img_before.size[0] / 2), int(himg / 2) - int(weather_img_before.size[1] / 2))
	# 遷移後のアイコン表示位置 -> ((wimg*2)/4, himg/2)
	after_position = (
		int((wimg * 3) / 4) - int(weather_img_after.size[0] / 2),
		int((himg * 2) / 3) - int(weather_img_after.size[1] / 2)
	)

	img = _match_image(base_img=img, paste_img=weather_img_before, position=before_position)
	img = _match_image(base_img=img, paste_img=weather_img_after, position=after_position)

	# # 画像の保存
	# save_image(img, name="weather_forecast_map")

	logger.info("Finished create to weather_icon(often)")

	return img


# weather = "のち" の場合の画像生成
def _create_weather_icon_after(weather_before=None, weather_after=None):
	if weather_before is None and weather_after is None:
		logger.warning(
			f'Error:weather_before or weather_after are setting undefined value(weather_before:{weather_before}, weather_after_after:{weather_after})')
		return None

	# ベース画像の作成

	img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
					color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])
	draw = ImageDraw.Draw(img)

	wimg = int(img.size[0])
	himg = int(img.size[1])

	draw.polygon(
		[((wimg * 3) / 7, 0), ((wimg * 4) / 7, himg / 2), ((wimg * 3) / 7, himg), (wimg, himg), (wimg, 0)],
		fill=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["bg_color"],
	)
	draw.line([((wimg * 3) / 7, 0), ((wimg * 4) / 7, himg / 2)], fill="white", width=3)
	draw.line([((wimg * 4) / 7, himg / 2), ((wimg * 3) / 7, himg)], fill="white", width=3)

	# 天気アイコンの合わせこみ

	weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))
	weather_img_after = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["url"]).resize((100, 100))

	# 変更前のアイコン表示位置 (wimg/4, himg/2)
	before_position = (
		int(wimg / 4) - int(weather_img_before.size[0] / 2), int(himg / 2) - int(weather_img_before.size[1] / 2))
	# 遷移後のアイコン表示位置 -> ((wimg*2)/4, himg/2)
	after_position = (
		int((wimg * 3) / 4) - int(weather_img_after.size[0] / 2), int(himg / 2) - int(weather_img_after.size[1] / 2))

	img = _match_image(base_img=img, paste_img=weather_img_before, position=before_position)
	img = _match_image(base_img=img, paste_img=weather_img_after, position=after_position)

	# # 画像の保存
	# save_image(img, name="weather_forecast_map")

	logger.info("Finished create to weather_icon(after)")

	return img


# weather = "一時" の場合の画像生成
def _create_weather_icon_temporary(weather_before=None, weather_after=None):
	if weather_before is None and weather_after is None:
		logger.warning(
			f'Error:weather_before or weather_after are setting undefined value(weather_before:{weather_before}, weather_after_after:{weather_after})')
		return None

	img = Image.new("RGBA", WEATHER_FORECAST_MAP_SIZE,
					color=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["bg_color"])
	draw = ImageDraw.Draw(img)

	wimg = img.size[0]
	himg = img.size[1]

	draw.polygon(
		[((wimg * 3) / 7, himg), (wimg / 2, himg / 3), (wimg, himg / 3), (wimg, himg)],
		fill=ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["bg_color"],
	)
	draw.line([((wimg * 3) / 7, himg), (wimg / 2, himg / 3)], fill="white", width=3)
	draw.line([(wimg / 2, himg / 3), (wimg, himg / 3)], fill="white", width=3)

	# 天気アイコンの合わせこみ

	weather_img_before = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_before)]]["url"]).resize((100, 100))
	weather_img_after = Image.open(ICON_WEATHER_FILE[WEATHER_CODE[str(weather_after)]]["url"]).resize((100, 100))

	# 変更前のアイコン表示位置 (wimg/4, himg/2)
	before_position = (
		int(wimg / 4) - int(weather_img_before.size[0] / 2), int(himg / 2) - int(weather_img_before.size[1] / 2))
	# 遷移後のアイコン表示位置 -> ((wimg*2)/4, himg/2)
	after_position = (
		int((wimg * 3) / 4) - int(weather_img_after.size[0] / 2),
		int((himg * 2) / 3) - int(weather_img_after.size[1] / 2)
	)

	img = _match_image(base_img=img, paste_img=weather_img_before, position=before_position)
	img = _match_image(base_img=img, paste_img=weather_img_after, position=after_position)

	# # 画像の保存
	# save_image(img, name="weather_forecast_map")

	logger.info("Finished create to weather_icon(temporary)")

	return img


def _create_weather_icon(jma_weather_code=None):
	# パラメータチェック
	if jma_weather_code is None:
		logger.warning("weather_code is None")
		return None

	with open(WEATHER_CODE_LIST_FILE_NAME) as f:
		weather_code_list = json.load(f)
		weather_code = weather_code_list[str(jma_weather_code - (jma_weather_code % 100))][0][str(jma_weather_code)]
		logger.debug(f'exchange weather code is {weather_code}')

	# 変数の初期化
	weather_icon = None  # 返り値として設定する変数
	weather_transition = WEATHER_TRANSITION(weather_code=weather_code)
	weather_before = WEATHER_KIND_before(weather_code=weather_code)
	weather_after = WEATHER_KIND_after(weather_code=weather_code)
	logger.debug(
		f'weather_before: {weather_before}, weather_transition: {weather_transition}, weather_after: {weather_after}'
	)

	# 画像生成の場合分け

	# のち
	# ---------------
	# | 〇   >   ×  |
	# ---------------

	# ときどき or 一時
	# ---------------
	# | 〇   「   ×  |
	# ---------------

	# "晴れ"などのonly表現
	if weather_transition == 0:
		weather_icon = _create_weather_icon_only(weather_before=weather_before)
	# "のち"の場合
	elif weather_transition == 1:
		weather_icon = _create_weather_icon_after(weather_before=weather_before, weather_after=weather_after)
	# "時々"の場合
	elif weather_transition == 2:
		weather_icon = _create_weather_icon_often(weather_before=weather_before, weather_after=weather_after)
	# "一時"の場合
	elif weather_transition == 3:
		weather_icon = _create_weather_icon_temporary(weather_before=weather_before, weather_after=weather_after)
	# 上記のどれにも当てはまらない(Error)
	else:
		logger.warning(f'Set undefined value in weather_transition(value:{weather_transition})')
		return None

	logger.info("Finished create_weather_icon")

	return weather_icon


def _create_detail_weather(weather_detail: str, get_date: datetime.datetime):
	# パラメータチェック
	if weather_detail == "":
		logger.warning("weather_detail does not set info")
		return None

	# 詳細情報の表示
	logger.debug(f'detail weather info: {weather_detail}')

	# ベース画像の作成
	img = Image.new("RGB", WEATHER_NAME_SIZE, color="white")
	draw = ImageDraw.Draw(img)

	# 天気の詳細情報の記載
	weather_detail_position = (int(WEATHER_NAME_SIZE[0] / 2), int(WEATHER_NAME_SIZE[1] / 2))
	font = ImageFont.truetype(FONT_FILE_PATH_MEIRYO, 20)
	draw.text(
		xy=weather_detail_position,
		text=weather_detail,
		fill="black",
		font=font,
		anchor="mm"
	)

	# 天気取得時間の記載
	get_date_position = (int(WEATHER_NAME_SIZE[0]), int(WEATHER_NAME_SIZE[1]))
	font_date = ImageFont.truetype(FONT_FILE_PATH_MEIRYO, 8)
	draw.text(
		xy=get_date_position,
		text=get_date.strftime("%Y年%m月%d日 %H:%M:%S"),
		fill="black",
		font=font_date,
		anchor="rd"
	)

	# # 画像の保存
	# if os.environ.get("SET_BUILD") == "LOCAL" or os.environ.get("SET_BUILD") == "LOCAL_INSTALLED":
	# 	save_image(img, name="detail_weather")

	logger.debug("Finished create_detail_weather()")

	return img


def _create_temperature_icon(temperature_list: list):
	# パラメータチェック
	if len(temperature_list) < 2:
		return -1

	temp_list_int = list(map(int, temperature_list))
	temp_max = max(temp_list_int)
	temp_min = min(temp_list_int)

	# ベース画像の作成
	img = Image.new("RGB", TEMPERATURE_SIZE, color="white")
	draw = ImageDraw.Draw(img)

	# 背景色の設定
	draw.rectangle(
		[(0, 0), (TEMPERATURE_SIZE[0], TEMPERATURE_SIZE[1] / 2)],
		fill=TEMPERATURE_MAX_BG_COLOR,
		outline=TEMPERATURE_MAX_FG_COLOR,
		width=5
	)
	draw.rectangle(
		[(0, TEMPERATURE_SIZE[1] / 2), (TEMPERATURE_SIZE[0], TEMPERATURE_SIZE[1])],
		fill=TEMPERATURE_MIN_BG_COLOR,
		outline=TEMPERATURE_MIN_FG_COLOR,
		width=5
	)

	# 文字の記載
	temperature_max_position = (TEMPERATURE_SIZE[0] / 2, TEMPERATURE_SIZE[1] / 4)
	temperature_min_position = (TEMPERATURE_SIZE[0] / 2, (TEMPERATURE_SIZE[1] * 3) / 4)
	draw.text(
		xy=temperature_max_position,
		text=str(temp_max),
		fill=TEMPERATURE_MAX_FG_COLOR,
		font_size=20,
		anchor="mm"
	)
	draw.text(
		xy=temperature_min_position,
		text=str(temp_min),
		fill=TEMPERATURE_MIN_FG_COLOR,
		font_size=20,
		anchor="mm"
	)

	# # 画像の保存
	# if os.environ.get("SET_BUILD") == "LOCAL" or os.environ.get("SET_BUILD") == "LOCAL_INSTALLED":
	# 	save_image(img, name="temperature_icon")

	logger.debug("Finished create_temperature_icon()")

	return img


def create_weather_image(place_code: str = "130000"):

	# 表示する画像のURL
	now_date = datetime.datetime.now()
	output_file_path = out_file_name_hero + str(now_date.strftime("%Y%m%d%H%M%S"))

	# 気象庁のAPIから東京都のjsonデータを取得
	jma_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{0}.json'.format(place_code)
	try:
		jma_json = requests.get(jma_url).json()
	except Exception as e:
		logger.warning("Could not get JSON data from JMA API.")
		logger.warning(f'{e.__class__.__name__}: {e}')
		return None

	# 気象情報(詳細な情報)
	jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][-1]
	jma_weather = jma_weather.replace("\u3000", " ")  # 空白文字の置き換え
	logger.info(f"weather: {jma_weather}")
	try:
		detail_weather_img = _create_detail_weather(jma_weather, get_date=now_date)
	except Exception as e:
		logger.warning(f'ERROR: create_detail_weather(): jma_weather={jma_weather}')
		logger.warning(f'{e.__class__.__name__}: {e}')
		return None

	# 天気コードの情報取得
	jma_weather_code = int(jma_json[0]["timeSeries"][0]["areas"][0]["weatherCodes"][-1])
	logger.info(f"weather_code: {jma_weather_code}")
	try:
		weather_forecast_map_img = _create_weather_icon(jma_weather_code)
	except Exception as e:
		logger.warning(f'ERROR: create_weather_icon(): jma_weather_code={jma_weather_code}')
		logger.warning(f'{e.__class__.__name__}: {e}')
		return None

	# 東京地方(area_code=130000)の最高/最低気温
	jma_temp = jma_json[0]["timeSeries"][2]["areas"][0]["temps"]
	logger.info(f"temps: {jma_temp}")
	try:
		temperature_img = _create_temperature_icon(jma_temp)
	except Exception as e:
		logger.warning(f'ERROR: create_temperature_icon(): jma_temp={jma_temp}')
		logger.warning(f'{e.__class__.__name__}: {e}')
		return None

	# 1つの画像にPaste
	img = Image.new("RGB", size=HERO_SIZE, color="#000000")
	img.paste(weather_forecast_map_img, HERO_POSITION_WEATHER_MAP)
	img.paste(temperature_img, HERO_POSITION_TEMPERATURE)
	img.paste(detail_weather_img, HERO_POSITION_DETAIL_WEATHER)

	try:
		# ファイルの削除
		_delete_old_images()

		# 画像の保存
		_save_image(img=img, name=output_file_path)
	except Exception as ex:
		logger.warning(f'{ex.__class__.__name__}: {ex}')
		return None

	return output_file_path + ".png"


# 未使用の予定
# def get_weather_image_path(self):
#
# 	# 作成した画像がない場合(一度も画像が作成がされていない場合)
# 	if self.out_file_name == "":
# 		return os.path.join(WEATHER_PATH, OUT_DEFAULT_WEATHER_IMAGE_FILE_NAME)
#
# 	# 今日と出力用ファイル置き場にある画像の作成日付を取得
# 	today_day = datetime.datetime.today().day
# 	image_file_datetime = datetime.datetime.strptime(
# 		self.out_file_name,
# 		out_file_name_hero + "%Y%m%d%H%M%S"
# 	)
# 	image_file_day = image_file_datetime.day
#
# 	# 今日の天気画像が作成されていない場合
# 	if today_day != image_file_day:
# 		return os.path.join(WEATHER_PATH, OUT_DEFAULT_WEATHER_IMAGE_FILE_NAME)
#
# 	path = urlparse.urljoin(self.out_image_par_dir, self.out_file_name + ".png")
# 	logger.debug(f'file_path: {path}')
#
# 	return path


# デバッグ用
if __name__ == "__main__":
	file_path = create_weather_image(place_code="130000")
	print(f'IMAGE_PATH: {file_path}')


