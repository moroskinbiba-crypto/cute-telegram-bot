# 💕 Cute Telegram Bot

Небольшой Telegram-бот, который каждые 3 часа отправляет случайное милое сообщение.

## Настройка

### 1. Создай бота в Telegram

Если бот уже создан — этот шаг пропусти.

### 2. Добавь секреты в GitHub

Открой:

**Settings → Secrets and variables → Actions → New repository secret**

Создай два секрета:

- `TELEGRAM_BOT_TOKEN` — токен бота от @BotFather
- `TELEGRAM_CHAT_ID` — ID чата, куда отправлять сообщения

Токен не добавляй в файлы репозитория.

### 3. Узнай CHAT_ID

Напиши своему боту в Telegram сообщение, например:

`/start`

Затем можно получить ID чата через Telegram Bot API. Удобнее всего сделать это локально, не публикуя токен:

```python
import os
import urllib.request
import json

token = os.environ["TELEGRAM_BOT_TOKEN"]
url = f"https://api.telegram.org/bot{token}/getUpdates"

with urllib.request.urlopen(url) as response:
    data = json.load(response)

print(data)
```

В результате найди:

```text
"chat": {
  "id": 123456789
}
```

Число `123456789` и есть `TELEGRAM_CHAT_ID`.

### 4. Запусти вручную первый раз

Открой:

**Actions → Send cute message → Run workflow**

Если всё настроено правильно, бот сразу отправит сообщение.

После этого GitHub Actions будет запускать отправку автоматически примерно раз в 3 часа.

## Изменить частоту

Расписание находится в:

`.github/workflows/send-message.yml`

Сейчас:

```yaml
cron: "0 */3 * * *"
```

Это запуск каждые 3 часа.

Например, каждые 2 часа:

```yaml
cron: "0 */2 * * *"
```

Важно: GitHub Actions может запускать scheduled workflow с небольшой задержкой.

## Добавить свои сообщения

Список сообщений находится в `bot.py`, внутри `MESSAGES`.
