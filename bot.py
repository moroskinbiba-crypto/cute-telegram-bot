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


def variable_path(name):
    owner, repo = GITHUB_REPOSITORY.split("/", 1)
    return f"/repos/{owner}/{repo}/actions/variables/{name}"


def get_variable(name, default=None):
    if not GITHUB_TOKEN or not GITHUB_REPOSITORY:
        return default

    try:
        _, result = github_api("GET", variable_path(name))
        return result.get("value", default)
    except RuntimeError as exc:
        if "HTTP 404" in str(exc):
            return default
        raise


def set_variable(name, value):
    owner, repo = GITHUB_REPOSITORY.split("/", 1)
    path = variable_path(name)
    payload = {"name": name, "value": str(value)}

    try:
        github_api("GET", path)
        github_api("PATCH", path, payload)
    except RuntimeError as exc:
        if "HTTP 404" not in str(exc):
            raise
        github_api("POST", f"/repos/{owner}/{repo}/actions/variables", payload)


def load_chat_ids():
    raw = get_variable("TELEGRAM_CHAT_IDS", "")
    if raw:
        try:
            return {int(chat_id) for chat_id in json.loads(raw)}
        except (TypeError, ValueError, json.JSONDecodeError):
            print("Warning: invalid TELEGRAM_CHAT_IDS variable; starting with an empty list.")

    # Migrate the old single-recipient setup if it exists.
    old_chat_id = get_variable("TELEGRAM_CHAT_ID", "")
    if old_chat_id:
        try:
            return {int(old_chat_id)}
        except ValueError:
            pass

    return set()


def save_chat_ids(chat_ids):
    set_variable("TELEGRAM_CHAT_IDS", json.dumps(sorted(chat_ids), separators=(",", ":")))
    print(f"Saved {len(chat_ids)} recipients.")


def load_update_offset():
    raw = get_variable("TELEGRAM_UPDATE_OFFSET", "0")
    try:
        return int(raw)
    except (TypeError, ValueError):
        return 0


def save_update_offset(offset):
    set_variable("TELEGRAM_UPDATE_OFFSET", str(offset))


def collect_new_chats():
    offset = load_update_offset()
    params = {
        "timeout": 0,
        "allowed_updates": json.dumps(["message"]),
    }
    if offset > 0:
        params["offset"] = offset

    updates = api("getUpdates", params)
    chat_ids = set()
    next_offset = offset

    for update in updates:
        update_id = update.get("update_id")
        if isinstance(update_id, int):
            next_offset = max(next_offset, update_id + 1)

        message = update.get("message", {})
        text = message.get("text", "")
        chat = message.get("chat", {})
        chat_id = chat.get("id")

        if chat_id is not None and text.startswith("/start"):
            chat_ids.add(int(chat_id))

    if next_offset != offset:
        save_update_offset(next_offset)

    return chat_ids


def send(chat_id, text):
    api("sendMessage", {"chat_id": chat_id, "text": text})


def send_to_all(chat_ids):
    if not chat_ids:
        print("No recipients yet. Waiting for /start.")
        return

    message_pool = random.choices(
        [MESSAGES, SURPRISE_MESSAGES],
        weights=[3, 1],
        k=1,
    )[0]
    text = random.choice(message_pool)

    active_chat_ids = set(chat_ids)
    for chat_id in sorted(chat_ids):
        try:
            send(chat_id, text)
            print(f"Sent to {chat_id}")
        except RuntimeError as exc:
            print(f"Could not send to {chat_id}: {exc}")
            if "Telegram HTTP 403" in str(exc):
                active_chat_ids.discard(chat_id)

    save_chat_ids(active_chat_ids)


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

    chat_ids = load_chat_ids()
    new_chat_ids = collect_new_chats()

    if new_chat_ids:
        before = len(chat_ids)
        chat_ids.update(new_chat_ids)
        if len(chat_ids) != before:
            save_chat_ids(chat_ids)

    send_to_all(chat_ids)
