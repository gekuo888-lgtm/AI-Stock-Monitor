import os
import requests
import yfinance as yf
from datetime import datetime

TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

stocks = {
    "0050.TW": {"name": "0050 元大台灣50", "cost": 84.81},
    "0052.TW": {"name": "0052 富邦科技", "cost": 49.82},
    "0056.TW": {"name": "0056 元大高股息", "cost": 38.24},
    "00919.TW": {"name": "00919 群益台灣精選高息", "cost": 23.44},
}

message = f"📊 ETF盤後分析\n日期：{datetime.now().strftime('%Y-%m-%d')}\n\n"

for code, info in stocks.items():

    try:

        stock = yf.Ticker(code)
        hist = stock.history(period="1mo")

        if hist.empty:
            raise Exception("查無資料")

        close_price = float(hist["Close"].dropna().iloc[-1])

        cost = info["cost"]

        profit = ((close_price - cost) / cost) * 100

        if profit >= 20:
            advice = "🟢 強勢續抱"
        elif profit >= 0:
            advice = "🟡 持有觀察"
        else:
            advice = "🔴 注意風險"

        message += (
            f"{info['name']}\n"
            f"收盤價：{close_price:.2f}\n"
            f"持有成本：{cost:.2f}\n"
            f"報酬率：{profit:.2f}%\n"
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
