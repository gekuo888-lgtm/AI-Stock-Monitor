import os
import requests

TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

message = "🚀 AI股票系統測試成功"

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
