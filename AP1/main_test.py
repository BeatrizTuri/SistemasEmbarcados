import requests

TELEGRAM_TOKEN = "7971761015:AAHrrcGHJJ3AmfrMX4RrVP7KygV5R1Ao6XI"
CHAT_ID = "7525968418"
MESSAGE = "Teste manual de envio"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
params = {"chat_id": CHAT_ID, "text": MESSAGE}

response = requests.get(url, params=params)
print(response.json())  # Exibe a resposta da API do Telegram
