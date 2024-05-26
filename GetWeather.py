import requests
import json
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

# 定数(後で_global.pyに移動する)

# Get Weather from Japan Meteorological Agency
# @param    [in]    place_code      Code for where to get the weather (details: https://www.jma.go.jp/bosai/common/const/area.json)
# @param    [out]   weather_list    Weather list
def get_weather(place_code="130000"):

    # 気象庁のAPIから東京都のデータを取得
    jma_url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/{0}.json'.format(place_code)
    jma_json = requests.get(jma_url).json()

    # APIから取得したデータから必要なデータを抜き出す
    jma_dict = {"MaxTemp": 20, "MinTemp": 15, "weather": "sunny"}

    return jma_dict