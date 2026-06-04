import os
import requests
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from datetime import datetime

TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

stocks = {
    "0050.TW": {"name": "0050 元大台灣50", "cost": 84.81},
    "0052.TW": {"name": "0052 富邦科技", "cost": 49.82},
    "0056.TW": {"name": "0056 元大高股息", "cost": 38.24},
    "00919.TW": {"name": "00919 群益台灣精選高息", "cost": 23.44},
}

message = f"📊 ETF盤後AI分析\n日期：{datetime.now().strftime('%Y-%m-%d')}\n\n"

for code, info in stocks.items():
    try:
        df = yf.download(
            code,
            period="1y",
            auto_adjust=True,
            progress=False
        )

  close_series = df["Close"]

if isinstance(close_series, pd.DataFrame):
    close_series = close_series.iloc[:, 0]

close_price = float(close_series.iloc[-1])

ma20 = float(close_series.rolling(20).mean().iloc[-1])
ma60 = float(close_series.rolling(60).mean().iloc[-1])
ma120 = float(close_series.rolling(120).mean().iloc[-1])

rsi = float(
    RSIIndicator(close_series).rsi().iloc[-1]
)

macd_obj = MACD(close_series)

        macd_line = float(macd_obj.macd().iloc[-1])
        signal_line = float(macd_obj.macd_signal().iloc[-1])

        score = 50

        if ma20 > ma60:
            score += 15

        if ma60 > ma120:
            score += 15

       if close_price > ma20:
            score += 10

        if 50 <= rsi <= 70:
            score += 10

        if macd_line > signal_line:
            score += 20

        if score >= 90:
            advice = "🟢 強勢續抱"
        elif score >= 75:
            advice = "🟢 續抱"
        elif score >= 60:
            advice = "🟡 觀察"
        else:
            advice = "🔴 減碼觀察"

        cost = info["cost"]

        profit = ((close_price - cost) / cost) * 100

        message += (
            f"{info['name']}\n"
            f"收盤：{close_price:.2f}\n"
            f"成本：{cost:.2f}\n"
            f"報酬率：{profit:.2f}%\n"
            f"20MA：{ma20:.2f}\n"
            f"60MA：{ma60:.2f}\n"
            f"120MA：{ma120:.2f}\n"
            f"RSI：{rsi:.1f}\n"
            f"AI評分：{score}/100\n"
            f"建議：{advice}\n"
            f"----------------\n\n"
        )

    except Exception as e:
        message += (
            f"{info['name']}\n"
            f"資料取得失敗\n"
            f"錯誤：{str(e)}\n"
            f"----------------\n\n"
        )

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "to": USER_ID,
    "messages": [
        {
            "type": "text",
            "text": message[:5000]
        }
    ]
}

response = requests.post(
    "https://api.line.me/v2/bot/message/push",
    headers=headers,
    json=payload
)

print(response.status_code)
print(response.text)
