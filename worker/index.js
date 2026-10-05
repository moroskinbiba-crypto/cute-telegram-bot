import { DurableObject } from "cloudflare:workers";

const MESSAGES = [
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
  "Тишка сказал, что ты хорошая. А Тишке виднее. Коты редко ошибаются 😼",
  "Тишка просил передать: «Не грусти, Мурочка». Суровый начальник, пришлось выполнить 🐱",
  "Мурзилка, пусть сегодня всё вокруг будет к тебе немного добрее, чем обычно ✨",
  "Мурочка, маленькое кото-сообщение специально для тебя: мур-мур и крепко обнимаю 💗",
  "Киселёнок, если день идёт не по плану — официально разрешаю начать его заново 🌸",
];

const SURPRISE_MESSAGES = [
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
];

function randomMessage() {
  const pool = Math.random() < 0.25 ? SURPRISE_MESSAGES : MESSAGES;
  return pool[Math.floor(Math.random() * pool.length)];
}

async function telegram(token, method, body) {
  const response = await fetch(
    `https://api.telegram.org/bot${token}/${method}`,
    {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    },
  );

  const data = await response.json();
  if (!data.ok) {
    const error = new Error(data.description || "Telegram API error");
    error.telegramStatus = response.status;
    throw error;
  }

  return data.result;
}

function subscribers(env) {
  const id = env.SUBSCRIBERS.idFromName("main");
  return env.SUBSCRIBERS.get(id);
}

async function addSubscriber(env, chatId) {
  await subscribers(env).fetch("https://do/add", {
    method: "POST",
    body: JSON.stringify({ chatId: String(chatId) }),
  });
}

async function removeSubscriber(env, chatId) {
  await subscribers(env).fetch("https://do/remove", {
    method: "POST",
    body: JSON.stringify({ chatId: String(chatId) }),
  });
}

async function getSubscribers(env) {
  const response = await subscribers(env).fetch("https://do/list");
  return response.json();
}

async function getWebhookSecret(env) {
  return subscribers(env).fetch("https://do/webhook-secret").then((response) => response.text());
}

async function ensureWebhook(env, origin) {
  const secret = await getWebhookSecret(env);
  const webhookUrl = `${origin}/telegram`;

  await telegram(env.TELEGRAM_BOT_TOKEN, "setWebhook", {
    url: webhookUrl,
    secret_token: secret,
    allowed_updates: ["message"],
    drop_pending_updates: false,
  });

  return webhookUrl;
}

async function webhookUpdate(request, env) {
  const secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token");
  const expectedSecret = await getWebhookSecret(env);

  if (!secret || secret !== expectedSecret) {
    return new Response("Unauthorized", { status: 401 });
  }

  const update = await request.json();
  const message = update.message;

  if (!message || !message.chat || message.chat.type !== "private") {
    return Response.json({ ok: true });
  }

  const chatId = String(message.chat.id);
  const text = (message.text || "").trim();

  if (text.startsWith("/stop")) {
    await removeSubscriber(env, chatId);
    await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
      chat_id: chatId,
      text: "Хорошо 💛 Я больше не буду присылать сообщения. Если соскучишься — просто нажми /start.",
    });
    return Response.json({ ok: true });
  }

  await addSubscriber(env, chatId);

  if (text.startsWith("/start")) {
    await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
      chat_id: chatId,
      text: "Привет 💕 Я здесь. Теперь ты официально в списке тех, кому иногда прилетает немного тепла. А конкретно тебе — потому что ты самая важная 😽",
    });
  } else if (text.startsWith("/now")) {
    await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
      chat_id: chatId,
      text: randomMessage(),
    });
  } else {
    await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
      chat_id: chatId,
      text: randomMessage(),
    });
  }

  return Response.json({ ok: true });
}

async function broadcast(env) {
  const chatIds = await getSubscribers(env);

  for (const chatId of chatIds) {
    try {
      await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
        chat_id: chatId,
        text: randomMessage(),
      });
    } catch (error) {
      if (error.telegramStatus === 403) {
        await removeSubscriber(env, chatId);
      }
      console.log(`Failed to send to ${chatId}: ${error.message}`);
    }
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "GET" && url.pathname === "/") {
      try {
        const webhookUrl = await ensureWebhook(env, url.origin);
        return new Response(`Cute Telegram Bot is alive 💕 Webhook: ${webhookUrl}`);
      } catch (error) {
        return new Response(`Bot setup error: ${error.message}`, { status: 500 });
      }
    }

    if (request.method === "POST" && url.pathname === "/telegram") {
      return webhookUpdate(request, env);
    }

    if (request.method === "GET" && url.pathname === "/health") {
      try {
        await ensureWebhook(env, url.origin);
        return Response.json({ ok: true, webhook: `${url.origin}/telegram` });
      } catch (error) {
        return Response.json({ ok: false, error: error.message }, { status: 500 });
      }
    }

    return new Response("Not found", { status: 404 });
  },

  async scheduled(controller, env, ctx) {
    ctx.waitUntil(
      (async () => {
        await ensureWebhook(env, new URL(controller.cron ? "https://cute-telegram-bot.dssmirnov2.workers.dev" : "https://cute-telegram-bot.dssmirnov2.workers.dev").origin);
        await broadcast(env);
      })(),
    );
  },
};

export class Subscribers extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.ctx = ctx;
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === "POST" && url.pathname === "/add") {
      const { chatId } = await request.json();
      await this.ctx.storage.put(`subscriber:${chatId}`, true);
      return Response.json({ ok: true });
    }

    if (request.method === "POST" && url.pathname === "/remove") {
      const { chatId } = await request.json();
      await this.ctx.storage.delete(`subscriber:${chatId}`);
      return Response.json({ ok: true });
    }

    if (request.method === "GET" && url.pathname === "/list") {
      const entries = await this.ctx.storage.list({ prefix: "subscriber:" });
      const chatIds = [...entries.keys()].map((key) => key.slice("subscriber:".length));
      return Response.json(chatIds);
    }

    if (request.method === "GET" && url.pathname === "/webhook-secret") {
      let secret = await this.ctx.storage.get("webhook-secret");
      if (!secret) {
        secret = crypto.randomUUID().replace(/-/g, "") + crypto.randomUUID().replace(/-/g, "");
        await this.ctx.storage.put("webhook-secret", secret);
      }
      return new Response(secret);
    }

    return new Response("Not found", { status: 404 });
  }
}
