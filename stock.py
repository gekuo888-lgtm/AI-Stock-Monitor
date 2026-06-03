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
