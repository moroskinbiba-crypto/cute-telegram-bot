import json
import os
import random
import urllib.parse
import urllib.request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

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

def api(method, params=None):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = urllib.parse.urlencode(params or {}).encode("utf-8")
    with urllib.request.urlopen(url, data=data, timeout=20) as response:
        result = json.load(response)
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")
    return result["result"]

def send(chat_id, text):
    api("sendMessage", {"chat_id": chat_id, "text": text})

def get_chat_id():
    updates = api("getUpdates", {"timeout": 0, "allowed_updates": json.dumps(["message"])})
    candidates = []
    for update in updates:
        message = update.get("message", {})
        text = message.get("text", "")
        if text.startswith("/start"):
            chat = message.get("chat", {})
            if chat.get("id") is not None:
                candidates.append((update.get("update_id", 0), chat["id"]))
    if not candidates:
        return None
    return candidates[-1][1]

if __name__ == "__main__":
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not chat_id:
        chat_id = get_chat_id()

    if not chat_id:
        print("No /start found yet. Ask the recipient to send /start to the bot.")
        raise SystemExit(0)

    send(chat_id, random.choice(MESSAGES))
    print(f"Cute message sent to chat {chat_id} 💕")
