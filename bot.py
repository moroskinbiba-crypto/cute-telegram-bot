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

    send(chat_id, random.choice(MESSAGES))
    print("Cute message sent 💕")
