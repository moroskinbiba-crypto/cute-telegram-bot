import json
import os
import random
import urllib.error
import urllib.parse
import urllib.request

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_API_VERSION = "2026-03-10"

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

    "Мурзилка, это твоё маленькое напоминание: ты чудесная 💛",
    "Мурочка, пожалуйста, сегодня не забывай улыбаться. Хотя бы чуть-чуть 🥹💕",
    "Киселёнок, тебе срочно доставлено немного нежности. Распишись здесь: 💌",
    "Мурзилка, Тишка и я считаем, что тебе давно пора получить что-нибудь хорошее 🐱💗",
    "Мурочка, Тишка официально назначил меня ответственным за твоё хорошее настроение 😼",
    "Киселёнок, если тебе сегодня никто этого не сказал: ты очень-очень особенная 🤍",
    "Мурзилка, береги себя. У тебя, между прочим, есть Тишка, которому ты очень нужна 🐾",
    "Мурочка, это сообщение пришло по секретному кото-каналу от Тишки: «мяу» 🐱",
    "Киселёнок, Тишка передаёт тебе пушистое обнимашечное настроение. Не потеряй 🫶",
    "Мурзилка, я просто заглянул напомнить, что кто-то где-то сейчас думает о тебе 💕",
    "Мурочка, тебе можно сегодня ничего не успеть. Можно просто быть собой 🌷",
    "Киселёнок, срочное распоряжение: сделать глоток чего-нибудь вкусного и немного выдохнуть ☕️",
    "Тишка сказал, что ты хорошая. А Тишке виднее. Коты редко ошибаются 😼",
    "Тишка просил передать: «Не грусти, Мурочка». Суровый начальник, пришлось выполнить 🐱",
    "Мурзилка, пусть сегодня всё вокруг будет к тебе немного добрее, чем обычно ✨",
    "Мурочка, маленькое кото-сообщение специально для тебя: мур-мур и крепко обнимаю 💗",
    "Киселёнок, если день идёт не по плану — официально разрешаю начать его заново 🌸",
]

SURPRISE_MESSAGES = [
    "Мурочка, маленькое расследование показало: ты почему-то стала появляться у меня в мыслях подозрительно часто 💕",
    "Киселёнок, Тишка настаивает: тебе сегодня положено хотя бы одно обнимашко. Апелляции не принимаются 😼",
    "Мурзилка, это не флирт. Это просто я совершенно случайно ещё раз подумал, какая ты милая. Совершенно случайно 😏",
    "Мурочка, у меня к тебе претензия: почему ты такая симпатичная и мешаешь мне сосредоточиться? 😌💗",
    "Киселёнок, срочная новость: сегодняшний день официально стал чуточку приятнее, потому что в нём есть ты ✨",
    "Тишка только что посмотрел на меня так, будто знает, что ты мне нравишься. Кот слишком много себе позволяет 😼",
    "Мурзилка, предупреждаю заранее: это сообщение может вызвать внезапную улыбку. Сопротивление бесполезно 💌",
    "Мурочка, иногда хочется просто взять тебя за руку и сказать: «Пойдём, я покажу тебе что-нибудь красивое» 🤍",
    "Киселёнок, если сегодня у тебя нет повода улыбнуться — считай, что я только что его прислал 🥰",
    "Мурзилка, Тишка разрешил мне официально напомнить: ты у нас одна такая. Очень даже одна 💗",
    "Мурочка, я бы сейчас отправил тебе цветочек, но бот умеет только сообщения. Поэтому держи: 🌷",
    "Киселёнок, это твоё персональное уведомление: кто-то считает тебя очень, очень привлекательной. И кот Тишка пока не возражает 😌🐱",
]

def api(method, params=None):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = urllib.parse.urlencode(params or {}).encode("utf-8")

    try:
        with urllib.request.urlopen(url, data=data, timeout=20) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Telegram HTTP {exc.code}: {body}") from exc

    if not result.get("ok"):
        raise RuntimeError(f"Telegram API error: {result}")

    return result["result"]


def github_api(method, path, payload=None):
    if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
        raise RuntimeError("GitHub Actions token/repository is unavailable")

    url = f"https://api.github.com{path}"
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API HTTP {exc.code}: {body_text}") from exc


def save_chat_id(chat_id):
    if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
        print("GitHub variable persistence is unavailable; continuing without saving chat.")
        return False

    owner, repo = GITHUB_REPOSITORY.split("/", 1)
    path = f"/repos/{owner}/{repo}/actions/variables/TELEGRAM_CHAT_ID"
    payload = {"name": "TELEGRAM_CHAT_ID", "value": str(chat_id)}

    try:
        try:
            github_api("GET", path)
            github_api("PATCH", path, payload)
        except RuntimeError as exc:
            if "HTTP 404" not in str(exc):
                raise
            github_api("POST", f"/repos/{owner}/{repo}/actions/variables", payload)

        print("Recipient chat saved in GitHub Actions variable.")
        return True
    except Exception as exc:
        print(f"Warning: could not save recipient chat: {exc}")
        return False


def send(chat_id, text):
    api("sendMessage", {"chat_id": chat_id, "text": text})


def get_chat_id():
    updates = api(
        "getUpdates",
        {
            "timeout": 0,
            "allowed_updates": json.dumps(["message"]),
        },
    )

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


def health_check():
    me = api("getMe")
    api(
        "getUpdates",
        {
            "timeout": 0,
            "allowed_updates": json.dumps(["message"]),
        },
    )
    print(f"Telegram OK: @{me.get('username', me.get('first_name', 'bot'))}")
    print("Polling via getUpdates is OK.")


if __name__ == "__main__":
    if os.environ.get("TEST_MODE") == "1":
        health_check()
        raise SystemExit(0)

    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not chat_id:
        chat_id = get_chat_id()
        if chat_id is not None:
            save_chat_id(chat_id)

    if not chat_id:
        print("No /start found yet. The bot is waiting for the recipient.")
        raise SystemExit(0)

    message_pool = random.choices(\n        [MESSAGES, SURPRISE_MESSAGES],\n        weights=[3, 1],\n        k=1,\n    )[0]\n    send(chat_id, random.choice(message_pool))
    print("Cute message sent 💕")
