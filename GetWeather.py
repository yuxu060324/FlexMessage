import requests
import json
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

# Get Weather from Japan Meteorological Agency
# @param    [in]    place_code      Code for where to get the weather (details: https://www.jma.go.jp/bosai/common/const/area.json)
# @param    [out]   weather_list    Weather list
def get_weather(place_code="130000"):
    jma_url = f'https://www.jma.go.jp/bosai/forecast/data/forecast/{place_code}.json'
    jma_json = requests.get(jma_url).json()