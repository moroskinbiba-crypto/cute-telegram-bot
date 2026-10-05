import os
import random
import urllib.parse
import urllib.request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MESSAGES = [
    "Просто напоминаю: ты сегодня уже достаточно молодец 💛",
    "Маленькое сообщение от твоего бота: пусть сегодня всё сложится чуть лучше, чем ты ожидал(а) 🌷",
    "Ты справляешься. Даже если кажется, что совсем не справляешься 🫶",
    "Пусть у тебя сегодня будет хотя бы один очень тёплый момент ☀️",
    "Это твоё официальное напоминание сделать паузу и немного выдохнуть 🌿",
    "Ты заслуживаешь добрых слов, даже без особой причины 💕",
    "Эй! Просто хотел сказать: ты классный человек 🐾",
    "Пусть сегодня тебе встретится что-нибудь маленькое и прекрасное ✨",
    "Не забывай заботиться о себе так же бережно, как о тех, кого любишь 🤍",
    "Всё необязательно успеть прямо сейчас. Можно идти маленькими шагами 🌸",
    "Отправляю тебе немного виртуального тепла. Лови! ☕️💗",
    "Если сегодня было тяжело — это не значит, что завтра будет таким же 🌙",
]

def send_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
    }).encode("utf-8")

    with urllib.request.urlopen(url, data=data, timeout=20) as response:
        body = response.read().decode("utf-8")
        if '"ok":true' not in body:
            raise RuntimeError(f"Telegram API error: {body}")

if __name__ == "__main__":
    send_message(random.choice(MESSAGES))
    print("Cute message sent successfully 💕")
