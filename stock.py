import os
import requests
import yfinance as yf

TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

stocks = {
    "0050.TW": "0050 元大台灣50",
    "0052.TW": "0052 富邦科技",
    "0056.TW": "0056 元大高股息",
    "00919.TW": "00919 群益台灣精選高息",
    "2330.TW": "2330 台積電",
    "3665.TW": "3665 貿聯-KY"
}

message = "📈 股票監控報告\n\n"

for code, name in stocks.items():
    try:
        stock = yf.Ticker(code)
        price = stock.history(period="1d")["Close"].iloc[-1]

        message += f"{name}\n"
        message += f"目前價格：{price:.2f}\n\n"

    except Exception as e:
        message += f"{name}\n"
        message += "資料取得失敗\n\n"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "to": USER_ID,
    "messages": [
        {
            "type": "text",
            "text": message
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
