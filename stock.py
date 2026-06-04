import os
import requests
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from datetime import datetime

TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

stocks = {
"0050.TW": {"name": "0050 元大台灣50", "cost": 84.81},
"0052.TW": {"name": "0052 富邦科技", "cost": 49.82},
"0056.TW": {"name": "0056 元大高股息", "cost": 38.24},
"00919.TW": {"name": "00919 群益台灣精選高息", "cost": 23.44},
}

message = f"📊 ETF AI盤後分析\n日期：{datetime.now().strftime('%Y-%m-%d')}\n\n"

for code, info in stocks.items():

```
try:

    stock = yf.Ticker(code)
    hist = stock.history(period="6mo")

    if hist.empty:
        raise Exception("查無資料")

    close_series = hist["Close"]

    if hasattr(close_series, "columns"):
        close_series = close_series.iloc[:, 0]

    close_price = float(close_series.dropna().iloc[-1])

    ma20 = float(close_series.rolling(20).mean().iloc[-1])
    ma60 = float(close_series.rolling(60).mean().iloc[-1])

    rsi = float(
        RSIIndicator(close_series).rsi().iloc[-1]
    )

    score = 50

    if close_price > ma20:
        score += 15

    if ma20 > ma60:
        score += 20

    if 50 <= rsi <= 70:
        score += 15

    cost = info["cost"]
    profit = ((close_price - cost) / cost) * 100

    if score >= 85:
        advice = "🟢 強勢續抱"
    elif score >= 70:
        advice = "🟢 續抱"
    elif score >= 60:
        advice = "🟡 觀察"
    else:
        advice = "🔴 注意"

    message += (
        f"{info['name']}\n"
        f"收盤：{close_price:.2f}\n"
        f"成本：{cost:.2f}\n"
        f"報酬率：{profit:.2f}%\n"
        f"20MA：{ma20:.2f}\n"
        f"60MA：{ma60:.2f}\n"
        f"RSI：{rsi:.1f}\n"
        f"AI評分：{score}/100\n"
        f"建議：{advice}\n"
        f"----------------------\n\n"
    )

except Exception as e:

    message += (
        f"{info['name']}\n"
        f"資料取得失敗\n"
        f"錯誤：{str(e)}\n"
        f"----------------------\n\n"
    )
```

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

```
```
