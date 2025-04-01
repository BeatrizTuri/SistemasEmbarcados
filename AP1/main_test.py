import requests

TELEGRAM_TOKEN = ""
CHAT_ID = ""
MESSAGE = "Teste manual de envio"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
params = {"chat_id": CHAT_ID, "text": MESSAGE}

response = requests.get(url, params=params)
print(response.json())  # Exibe a resposta da API do Telegram
