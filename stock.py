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

message = "📊 ETF盤後AI分析\n"
message += f"日期：{datetime.now().strftime('%Y-%m-%d')}\n\n"

for code, info in stocks.items():

```
try:

    df = yf.download(
        code,
        period="1y",
        auto_adjust=True,
        progress=False
    )

    close = float(df["Close"].iloc[-1])

    ma20 = float(df["Close"].rolling(20).mean().iloc[-1])
    ma60 = float(df["Close"].rolling(60).mean().iloc[-1])
    ma120 = float(df["Close"].rolling(120).mean().iloc[-1])

    rsi = float(
        RSIIndicator(df["Close"]).rsi().iloc[-1]
    )

    macd = MACD(df["Close"])

    macd_line = float(macd.macd().iloc[-1])
    signal_line = float(macd.macd_signal().iloc[-1])

    score = 50

    if ma20 > ma60:
        score += 15

    if ma60 > ma120:
        score += 15

    if close > ma20:
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

    profit = (
        (close - cost)
        / cost
        * 100
    )

    message += f"{info['name']}\n"
    message += f"收盤：{close:.2f}\n"
    message += f"成本：{cost:.2f}\n"
    message += f"報酬率：{profit:.2f}%\n"
    message += f"RSI：{rsi:.1f}\n"
    message += f"AI評分：{score}/100\n"
    message += f"建議：{advice}\n"
    message += "----------------\n\n"

except Exception:
    message += f"{info['name']}\n"
    message += "資料取得失敗\n\n"
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
