# Wazzapo для Python

Официальная библиотека для [API v2 Wazzapo](https://wazzapo.kz/api/v2/external/docs): сообщения WhatsApp, шаблоны, контакты, сделки, переписки и вебхуки. Лицензия MIT.

- подсказки в редакторе по-русски: у каждого метода и поля описание из документации API;
- повторы на 429, 5xx и сбоях сети с учётом `Retry-After`;
- `Idempotency-Key` на каждый POST: повтор не отправит сообщение дважды;
- ошибки отдельными классами с `code`, `message`, `details`, `request_id`;
- списки: одна страница или все подряд итератором;
- проверка подписи вебхуков;
- синхронный и async клиент, одна зависимость (httpx), Python 3.9+.

## Установка

```bash
pip install wazzapo
```

## Первое сообщение за 5 минут

1. В кабинете Wazzapo откройте раздел «API» и создайте ключ. Для пробы берите тестовый ключ `wz_test_…`: он ничего не отправляет и не меняет, а отвечает как настоящий.
2. Положите ключ в переменную окружения:

```bash
export WAZZAPO_API_KEY=wz_test_...
```

3. Узнайте `phone_number_id` своего номера и отправьте сообщение:

```python
from wazzapo import Wazzapo

client = Wazzapo()  # ключ из WAZZAPO_API_KEY, можно передать Wazzapo(api_key="...")

# В списке все каналы аккаунта (WhatsApp, Telegram, OLX, почта...): берём подключённый WhatsApp
numbers = client.phone_numbers.list()["data"]
whatsapp = next(
    n for n in numbers
    if n["provider_type"] in ("meta_cloud", "evolution_api") and n["status"] == "connected"
)
phone_number_id = whatsapp["phone_number_id"]

# Текст доходит, только если клиент писал вам за последние 24 часа
sent = client.messages.send({
    "phone_number_id": phone_number_id,
    "to": "77071234567",
    "type": "text",
    "text": {"body": "Айгуль, здравствуйте! Запись на 25 октября в 15:00 подтверждена."},
})
print(sent["message_id"])
```

4. Первое сообщение клиенту (или через 24 часа тишины) отправляйте одобренным шаблоном:

```python
client.messages.send({
    "phone_number_id": phone_number_id,
    "to": "77071234567",
    "type": "template",
    "template": {
        "name": "zapis_napominanie",
        "language": {"code": "ru"},
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "Айгуль"},
                    {"type": "text", "text": "25 октября, 15:00"},
                ],
            }
        ],
    },
})
```

Список шаблонов и их статус: `client.templates.list(phone_number_id=phone_number_id, status="APPROVED")`.

## Как устроены методы

- `client.<ресурс>.<действие>(...)`: `client.contacts.create`, `client.deals.move`, `client.phone_numbers.get_business_profile`.
- id из адреса передаётся первым аргументом: `client.contacts.get("6a7d...")`.
- Тело запроса: словарь первым аргументом после id (`client.contacts.update("6a7d...", {"name": "Айгуль"})`) или `body=`; поля подсказывает редактор. Параметры списка: именованные аргументы.
- Ответ: обычный словарь, как в документации. Типы для своего кода: `from wazzapo.types import SendMessageIn, DealOut`.
- У каждого метода есть настройки одного вызова: `timeout=` (секунды), `headers=` (свои заголовки, например `{"X-Request-Id": "order-4521"}`; ключ и `Idempotency-Key` они не заменяют), `max_retries=`; у POST ещё `idempotency_key=`.

```python
deal = client.deals.create(
    {
        "pipeline_id": "6712a0c4e1b2c3d4e5f60718",
        "title": "Заявка с сайта: кухня на заказ",
        "contact": {"name": "Айгуль Сейткали", "phone": "77071234567"},
        "amount": 15000000,  # в тиынах: 150 000 тенге
        "currency": "KZT",
        "external_id": "site-order-4521",
    },
    idempotency_key="site-order-4521",  # повтор с тем же ключом не создаст вторую сделку
)
```

Загрузка и скачивание файлов:

```python
# путь, bytes или открытый файл; путь к несуществующему файлу сразу даёт FileNotFoundError
media = client.media.upload("schet_1024.pdf", phone_number_id=phone_number_id)
client.messages.send({"phone_number_id": phone_number_id, "to": "77071234567", "type": "document",
                      "document": {"id": media["media_id"], "filename": "schet_1024.pdf"}})
data: bytes = client.media.download(media["media_id"], phone_number_id=phone_number_id)
```

## Ошибки

```python
from wazzapo import OutsideWindowError, RateLimitError, ValidationError, WazzapoError

try:
    client.messages.send({...})
except OutsideWindowError:
    ...  # клиент не писал 24 часа: отправьте шаблон
except ValidationError as e:
    print(e.fields)  # [{"field": "body.to", "message": "Field required"}]
except RateLimitError as e:
    print(e.retry_after)  # SDK уже повторил запрос max_retries раз
except WazzapoError as e:
    print(e.status, e.code, e.message, e.request_id)  # request_id сообщите в поддержку
```

| Класс | Когда |
|---|---|
| `BadRequestError` | 400: неверный запрос |
| `AuthenticationError` | 401: нет ключа или он неверный |
| `PaymentRequiredError` | 402: тариф не оплачен или Meta не может списать оплату |
| `PermissionDeniedError` | 403: нет права у ключа, IP не разрешён |
| `UsageLimitError` | 403 `USAGE_LIMIT_EXCEEDED`: исчерпан лимит тарифа |
| `NotFoundError` | 404 |
| `ConflictError` | 409: объект уже есть, например `contact_exists` (id в `details`) |
| `ValidationError` | 422 `VALIDATION_ERROR`: поля не прошли проверку, список в `fields` |
| `OutsideWindowError` | 422 `outside_24h_window` |
| `TemplateError` | 422 `template_*`: шаблон не найден, не одобрен, приостановлен |
| `UnprocessableEntityError` | остальные 422, например `invalid_parameters` |
| `RateLimitError` | 429 |
| `ServerError` | 5xx |
| `APIConnectionError`, `APITimeoutError` | ответа не было: `code` равен `CONNECTION_ERROR` или `TIMEOUT` |
| `PaginationError` | сервер вернул тот же `next_cursor` ещё раз, обход списка остановлен |
| `WebhookVerificationError` | вебхук не прошёл проверку (см. «Вебхуки») |

Все классы наследуют `WazzapoError`. Если ответ пришёл не от API (например, страница прокси с 502), `code` берётся по статусу: `BAD_GATEWAY`, `SERVICE_UNAVAILABLE` и т.д.

Все коды и их значения: раздел «Коды ошибок» в [документации](https://wazzapo.kz/api/v2/external/docs).

## Списки

```python
page = client.contacts.list(tag="vip", limit=100)  # одна страница: data, next_cursor, has_more
if page["has_more"]:
    next_page = client.contacts.list(tag="vip", limit=100, cursor=page["next_cursor"])

for contact in client.contacts.list_all(tag="vip"):  # все страницы, по одной за раз
    print(contact["phone"])
```

## Async

```python
import asyncio
from wazzapo import AsyncWazzapo

async def main() -> None:
    async with AsyncWazzapo() as client:
        await client.messages.send({...})
        async for deal in client.deals.list_all(pipeline_id="6712a0c4e1b2c3d4e5f60718"):
            print(deal["title"])

asyncio.run(main())
```

## Вебхуки

Создайте вебхук и сохраните секрет: он показывается один раз.

```python
hook = client.webhooks.create({"url": "https://example.kz/wazzapo", "event_types": ["message.incoming", "deal.created"]})
secret = hook["secret"]
```

Проверяйте подпись на сыром теле запроса, до разбора JSON. `verify` сверяет подпись и время (допуск 5 минут) и возвращает событие. Без секрета (пустая строка или `None`, например не задана переменная окружения) `verify` сразу бросает `WebhookVerificationError`: так поддельный запрос не пройдёт. Та же ошибка, если подписи нет, она чужая, запрос старый или тело не JSON.

FastAPI:

```python
from fastapi import FastAPI, HTTPException, Request
from wazzapo import webhooks

app = FastAPI()

@app.post("/wazzapo")
async def wazzapo_hook(request: Request) -> dict[str, bool]:
    try:
        event = webhooks.verify(await request.body(), request.headers, secret)
    except webhooks.WebhookVerificationError:
        raise HTTPException(status_code=400)
    if event["event"] == "message.incoming":
        print(event["data"]["message"]["text"])
    return {"ok": True}
```

Flask:

```python
from flask import Flask, abort, request
from wazzapo import webhooks

app = Flask(__name__)

@app.post("/wazzapo")
def wazzapo_hook() -> dict[str, bool]:
    try:
        # verify принимает любые заголовки с items(): request.headers Flask, dict, заголовки FastAPI
        event = webhooks.verify(request.get_data(), request.headers, secret)
    except webhooks.WebhookVerificationError:
        abort(400)
    return {"ok": True}
```

Ответьте 2xx быстрее 10 секунд, долгую работу делайте в фоне. Одно событие может прийти дважды (повтор доставки): у всех повторов один и тот же заголовок `X-Wazzapo-Delivery-Id` (`webhooks.DELIVERY_ID_HEADER`), по нему и отсеивайте дубли.

```python
delivery_id = request.headers.get(webhooks.DELIVERY_ID_HEADER)
if already_processed(delivery_id):  # ваша проверка: таблица, Redis и т.п.
    return {"ok": True}
```

Для своих тестов подпись ставит `webhooks.sign(body, secret)`, а `webhooks.verify(..., now=...)` проверяет на заданное время.

## Тестовый ключ

Ключ `wz_test_…` проходит все проверки, но ничего не отправляет в WhatsApp и не меняет данные: сообщения получают id `wamid.SANDBOX…`. Чтение работает по-настоящему. `client.is_test` показывает, какой ключ в работе.

## Настройки

```python
Wazzapo(
    api_key="wz_live_...",            # или WAZZAPO_API_KEY
    base_url="https://wazzapo.kz",   # или WAZZAPO_BASE_URL
    timeout=30,                      # секунды на запрос
    max_retries=2,                   # повторы на 429, 5xx и сбоях сети
    http_client=None,                # свой httpx.Client: прокси, свои заголовки
)
```

Ключ не попадает в логи и `repr` (ни клиента, ни его настроек): видны только первые 8 знаков, они же в `client.api_key_hint`. Отладка запросов: `logging.getLogger("wazzapo").setLevel(logging.DEBUG)`.

## Разработка

Код в `src/wazzapo/_generated` собирается из описания API: `cd sdk && python -m codegen python`. Руками его не правят.

```bash
uv venv && uv pip install -e ".[dev]"
pytest
mypy src/wazzapo
WAZZAPO_TEST_API_KEY=wz_test_... pytest tests/test_live.py
```
