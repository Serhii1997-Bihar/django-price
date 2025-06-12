import requests
from django.conf import settings

def send_message(chat_id, message):
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        if not result.get('ok', False):
            error_code = result.get('error_code')
            if error_code == 403:
                print(f"Chat_id: {chat_id} has blocked or deleted the bot.")
    except requests.RequestException as e:
        print(f"Telegram error: {e}")




