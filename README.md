# 💕 Cute Telegram Bot

Полностью автоматический Telegram-бот, который отвечает пользователям и каждые 3 часа отправляет им милые сообщения.

## Новая архитектура

Бот работает через **Cloudflare Workers**:

- Telegram отправляет новые сообщения боту через webhook;
- бот сразу отвечает пользователю;
- каждый пользователь, который нажал `/start`, сохраняется в Cloudflare Durable Object;
- Cloudflare Cron Trigger запускает рассылку каждые 3 часа;
- GitHub Actions больше не нужен для работы бота после одноразового деплоя.

Cloudflare Workers поддерживает Cron Triggers, а SQLite Durable Objects доступны и на бесплатном плане. citeturn806989search0turn894211search0

## Команды

`/start` — добавить пользователя в рассылку и получить приветствие.

`/now` — получить милое сообщение сразу.

`/stop` — убрать себя из рассылки.

Любое обычное сообщение тоже получает ответ.

## Токен

В GitHub уже должен находиться секрет:

- `TELEGRAM_BOT_TOKEN`

Токен нельзя размещать в коде или отправлять в чат.

## Одноразовый деплой Cloudflare

Для полностью автоматической работы нужно один раз подключить Cloudflare.

### 1. Создай аккаунт Cloudflare

Открой Cloudflare и создай Workers-проект.

### 2. Получи данные для GitHub

Нужны:

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`

API Token должен иметь разрешение **Workers Scripts: Edit** для нужного аккаунта.

### 3. Добавь три GitHub Secrets

В:

**Settings → Secrets and variables → Actions**

добавь:

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`
- `WEBHOOK_SETUP_SECRET`

Для последних двух можно использовать любые длинные случайные строки.

`TELEGRAM_BOT_TOKEN` уже используется из существующего секрета.

### 4. Запусти деплой один раз

Открой:

**Actions → Deploy automatic Telegram bot → Run workflow**

Workflow:

1. загрузит секреты в Cloudflare;
2. создаст Worker;
3. создаст SQLite Durable Object для списка пользователей;
4. настроит Telegram webhook;
5. автоматически отключит старые GitHub Actions, которые больше не нужны.

После этого бот работает без постоянных запусков GitHub Actions.

## Расписание

Cloudflare Cron Trigger настроен на:

`0 */3 * * *`

То есть один запуск каждые 3 часа по UTC. citeturn806989search0

## Сообщения

Основные и сюрпризные сообщения находятся в:

`worker/index.js`

Сейчас примерно 25% отправок выбираются из сюрпризной категории — там больше флирта, нежности и Тишки 😼
