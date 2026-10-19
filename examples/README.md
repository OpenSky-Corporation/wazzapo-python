# Примеры wazzapo

Три готовых примера на Python 3.9+ без фреймворков, только стандартная библиотека (`http.server`).

| Файл | Что делает |
|---|---|
| `bot_buttons.py` | Бот с кнопками. На входящее сообщение отвечает тремя кнопками («Цены», «Записаться», «Администратор»), на нажатие кнопки отвечает текстом |
| `lead_to_deal.py` | Заявка с формы сайта (`name`, `phone`, `comment`) становится сделкой, клиент получает приветственный шаблон WhatsApp. Повтор той же заявки дубль не создаёт |
| `webhooks_receiver.py` | Приёмник всех событий: проверяет подпись, сразу отвечает 200 и пишет в журнал смену этапа сделки и статусы сообщений |

## Установка

```bash
pip install wazzapo
```

или `pip install -r requirements.txt` в этой папке.

## Переменные окружения

| Переменная | Где взять | Нужна для |
|---|---|---|
| `WAZZAPO_API_KEY` | Кабинет, раздел «API». Для проверок ключ `wz_test_…`: он ничего не отправляет | всех, кроме приёмника |
| `WAZZAPO_WEBHOOK_SECRET` | Ответ при создании вебхука (`client.webhooks.create(...)`) или в кабинете | `bot_buttons`, `webhooks_receiver` |
| `WAZZAPO_PHONE_NUMBER_ID` | `phone_number_id` из `client.phone_numbers.list(channel="whatsapp")` | `lead_to_deal` |
| `WAZZAPO_TEMPLATE_NAME`, `WAZZAPO_TEMPLATE_LANG` | Одобренный шаблон из `client.templates.list(phone_number_id=..., status="APPROVED")`, язык по умолчанию `ru` | `lead_to_deal` |
| `WAZZAPO_TEMPLATE_NAME_PARAM` | `1`, если в тексте шаблона есть `{{1}}`: подставим имя клиента | `lead_to_deal` |
| `WAZZAPO_PIPELINE_ID` | id воронки из `client.pipelines.list()`; без неё первая воронка | `lead_to_deal` |
| `PORT` | порт сервера: по умолчанию 8080, 8081 и 8082 | всех |

## Запуск

```bash
WAZZAPO_API_KEY=wz_test_... WAZZAPO_WEBHOOK_SECRET=... python bot_buttons.py
WAZZAPO_API_KEY=wz_test_... WAZZAPO_PHONE_NUMBER_ID=... WAZZAPO_TEMPLATE_NAME=... python lead_to_deal.py
WAZZAPO_WEBHOOK_SECRET=... python webhooks_receiver.py
```

Адрес бота и приёмника укажите вебхуком в кабинете или методом `client.webhooks.create({"url": "https://ваш-сайт/...", "event_types": ["message.incoming"]})`. Wazzapo шлёт вебхуки только на https: для своего компьютера подойдёт туннель (например, ngrok или cloudflared).

## Проверка без настоящих клиентов

С тестовым ключом `wz_test_…` запросы проходят все проверки (номер, шаблон, повтор запроса), но ничего не уходит в WhatsApp и не меняется в данных: в ответе `wamid.SANDBOX…` и `sandbox_…`.

Событие, как его пришлёт Wazzapo, можно подписать самим и отправить curl:

```bash
export WAZZAPO_WEBHOOK_SECRET=test_secret
BODY='{"event":"message.incoming","timestamp":"2026-10-19T12:00:00Z","data":{"channel":"whatsapp","phone_number_id":"ВАШ_PHONE_NUMBER_ID","contact":{"name":"Айгерим","phone":"77071234567"},"message":{"from":"77071234567","type":"text","text":"Здравствуйте","interactive_reply_id":null}}}'
python -c 'import os, sys; from wazzapo import webhooks; [print("-H\n%s: %s" % kv) for kv in webhooks.sign(sys.argv[1], os.environ["WAZZAPO_WEBHOOK_SECRET"]).items()]' "$BODY" > /tmp/h.txt
mapfile -t H < /tmp/h.txt
curl -X POST "${H[@]}" -H "X-Wazzapo-Delivery-Id: test-1" --data-binary "$BODY" http://127.0.0.1:8080/
```

Ответ `{"ok": true, "message_id": "wamid.SANDBOX…"}`. Тот же запрос второй раз даст `"duplicate": true`: повтор доставки по `X-Wazzapo-Delivery-Id` отсеивается. Нажатие кнопки: в `message.interactive_reply_id` поставьте `"prices"`.

Заявка:

```bash
curl -X POST -d "name=Айгерим&phone=+7 707 123 45 67&comment=Хочу на замер" http://127.0.0.1:8081/
```

## То же на FastAPI

```python
@app.post("/wazzapo")
async def wazzapo_webhook(request: Request) -> dict:
    event = webhooks.verify(await request.body(), request.headers, os.environ["WAZZAPO_WEBHOOK_SECRET"])
    return {"ok": True}
```

## Что важно в своём коде

- Подпись проверяйте по сырому телу (байты запроса), до разбора JSON.
- Отвечайте на вебхук быстро, долгую обработку делайте после ответа или в очереди.
- Отсев повторов в примере хранит id доставок в памяти процесса. В работе храните их в базе или Redis.
- Чтобы заявка не стала двумя сделками, передавайте свой `external_id`: повтор вернёт `ConflictError` с кодом `deal_exists` и id уже созданной сделки в `exc.details["deal_id"]`.
