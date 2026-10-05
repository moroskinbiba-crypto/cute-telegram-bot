# 💕 Cute Telegram Bot

Полностью автоматический Telegram-бот для одного получателя: отвечает ей сразу и каждые 3 часа присылает милое сообщение.

## Новая архитектура

Бот работает через **Cloudflare Workers**:

- Telegram отправляет новые сообщения боту через webhook;
- бот сразу отвечает пользователю;
- один получатель после `/start` сохраняется в Cloudflare Durable Object;
- Cloudflare Cron Trigger запускает рассылку каждые 3 часа;
- GitHub Actions больше не нужен для работы бота после одноразового деплоя.

Cloudflare Workers поддерживает Cron Triggers, а SQLite Durable Objects используются как постоянное хранилище получателя. citeturn806989search0turn894211search0

## Команды

`/start` — назначить этого человека единственным получателем и получить приветствие.

`/now` — получить милое сообщение сразу.

`/stop` — отключить единственного получателя.

Любое обычное сообщение тоже получает персональный ответ.

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

### 3. Добавь два GitHub Secrets

В:

**Settings → Secrets and variables → Actions**

добавь:

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`


`TELEGRAM_BOT_TOKEN` уже используется из существующего секрета.

### 4. Запусти деплой один раз

Открой:

**Actions → Deploy automatic Telegram bot → Run workflow**

Workflow:

1. загрузит секреты в Cloudflare;
2. создаст Worker;
3. создаст SQLite Durable Object для одного получателя;
4. настроит Telegram webhook;
5. автоматически отключит старые GitHub Actions, которые больше не нужны.

После этого бот работает без постоянных запусков GitHub Actions.

## Расписание

Cloudflare Cron Trigger настроен на:

`0 */3 * * *`

То есть один запуск каждые 3 часа по UTC. citeturn806989search0

## Сообщения

Основные и сюрпризные сообщения для неё находятся в:

`worker/index.js`

Сейчас примерно 25% отправок выбираются из сюрпризной категории — там больше флирта, нежности и Тишки 😼
