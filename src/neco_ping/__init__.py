import requests

def send(token: str, chat_id: str, text: str) -> None:
    """
    Отправляет сообщение в Telegram.
    Тихий режим: если нет интернета или токен битый, 
    ошибка подавляется, чтобы не крашить ML-пайплайн.
    """
    try:
        requests.post(
            url=f'https://api.telegram.org/bot{token}/sendMessage',
            data={'chat_id': chat_id, 'text': text},
            timeout=5  # Тайм-аут, чтобы обучение не висело, если телега лежит
        )
    except Exception:
        # Игнорируем ошибки, чтобы твой скрипт обучения не упал 
        # в самом конце из-за проблем с сетью при отправке уведомления.
        pass
