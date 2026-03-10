"""
お天気ロボット - 毎日の天気情報を取得して weather.txt に保存するスクリプト
使用API:
  - Open-Meteo (天気データ、無料・登録不要)
  - ip-api.com (現在地の自動検出)
"""

import urllib.request
import urllib.parse
import json
import datetime
import os


def get_location() -> dict:
    """ip-api.com で現在地の緯度・経度・都市名を取得する。"""
    url = "http://ip-api.com/json/?lang=ja&fields=status,city,regionName,country,lat,lon"
    req = urllib.request.Request(url, headers={"User-Agent": "WeatherRobot/1.0"})
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read().decode("utf-8"))
    if data.get("status") != "success":
        raise RuntimeError("現在地の取得に失敗しました。")
    return data


# Open-Meteo の WMO 天気コードを日本語に変換
WMO_CODES = {
    0: "快晴", 1: "ほぼ快晴", 2: "一部曇り", 3: "曇り",
    45: "霧", 48: "着氷霧",
    51: "小雨（霧雨）", 53: "中程度の霧雨", 55: "強い霧雨",
    61: "小雨", 63: "中程度の雨", 65: "大雨",
    71: "小雪", 73: "中程度の雪", 75: "大雪",
    77: "霰（あられ）",
    80: "にわか雨（小）", 81: "にわか雨（中）", 82: "にわか雨（強）",
    85: "にわか雪（小）", 86: "にわか雪（強）",
    95: "雷雨", 96: "雷雨+小さな雹", 99: "雷雨+大きな雹",
}


def get_weather(lat: float, lon: float) -> dict:
    """Open-Meteo API から天気情報を取得する。"""
    params = {
        "latitude"      : lat,
        "longitude"     : lon,
        "current"       : "temperature_2m,apparent_temperature,relative_humidity_2m,"
                          "wind_speed_10m,weather_code",
        "daily"         : "temperature_2m_max,temperature_2m_min",
        "timezone"      : "Asia/Tokyo",
        "forecast_days" : 1,
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "WeatherRobot/1.0"})
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read().decode("utf-8"))

    c = data["current"]
    d = data["daily"]
    code = c["weather_code"]
    return {
        "temp_c"      : round(c["temperature_2m"], 1),
        "feels_like_c": round(c["apparent_temperature"], 1),
        "humidity"    : round(c["relative_humidity_2m"]),
        "wind_kmph"   : round(c["wind_speed_10m"]),
        "description" : WMO_CODES.get(code, f"天気コード {code}"),
        "max_c"       : round(d["temperature_2m_max"][0], 1),
        "min_c"       : round(d["temperature_2m_min"][0], 1),
    }


def save_weather(location: dict, weather: dict, filepath: str = "weather.txt") -> None:
    """取得した天気情報を weather.txt に追記する。"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "=" * 45,
        f"  お天気レポート  {now}",
        "=" * 45,
        f"  場所      : {location['city']}, {location['regionName']}, {location['country']}",
        f"  天気      : {weather['description']}",
        f"  現在気温  : {weather['temp_c']} °C  (体感 {weather['feels_like_c']} °C)",
        f"  最高 / 最低: {weather['max_c']} °C / {weather['min_c']} °C",
        f"  湿度      : {weather['humidity']} %",
        f"  風速      : {weather['wind_kmph']} km/h",
        "=" * 45,
        "",
    ]

    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[完了] 天気情報を {os.path.abspath(filepath)} に保存しました。")
    for line in lines:
        print(line)


def main() -> None:
    output_path = os.environ.get("OUTPUT_PATH", "weather.txt")

    print("現在地を取得中...")
    location = get_location()
    print(f"  → {location['city']}, {location['regionName']}, {location['country']}")

    print("天気情報を取得中...")
    weather = get_weather(location["lat"], location["lon"])

    save_weather(location, weather, output_path)


if __name__ == "__main__":
    main()
