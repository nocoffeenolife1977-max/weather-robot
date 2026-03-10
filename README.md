# お天気ロボット 🤖🌤

現在地の天気を毎日自動で取得し、`weather.txt` に記録するシンプルな Python スクリプトです。

## 機能

- IP アドレスから現在地を自動検出（[ip-api.com](http://ip-api.com)）
- [Open-Meteo](https://open-meteo.com/) APIで天気・気温・湿度・風速を取得（登録不要・無料）
- 結果を `weather.txt` に追記保存
- GitHub Actions で毎朝 7:00 JST に自動実行し、結果をコミット

## 使い方

### ローカルで実行

```bash
python weather_robot.py
```

### 環境変数（オプション）

| 変数名 | 説明 | デフォルト |
|---|---|---|
| `OUTPUT_PATH` | 出力ファイルのパス | `weather.txt` |

## weather.txt の出力例

```
=============================================
  お天気レポート  2026-03-10 07:00:00
=============================================
  場所      : 小田原市, 神奈川県, Japan
  天気      : 快晴
  現在気温  : 3.0 °C  (体感 -0.5 °C)
  最高 / 最低: 9.4 °C / 3.3 °C
  湿度      : 61 %
  風速      : 6 km/h
=============================================
```

## GitHub Actions

`.github/workflows/weather.yml` により、毎朝 7:00 JST に自動実行されます。
実行後、`weather.txt` が自動でコミット・プッシュされます。

手動実行は GitHub の「Actions」タブ → 「Run workflow」から可能です。

## 使用ライブラリ

標準ライブラリのみ使用（`urllib`, `json`, `datetime`）。追加インストール不要です。
