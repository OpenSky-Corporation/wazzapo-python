# Изменения

## 0.1.0 (2026-10-19)

Первый выпуск для API v2.

- Все 49 методов API v2: номера, сообщения, шаблоны, файлы, контакты, воронки, сделки, задачи, переписки, сотрудники, вебхуки.
- Синхронный `Wazzapo` и асинхронный `AsyncWazzapo` на httpx.
- Повторы на 429, 5xx и сбоях сети с учётом `Retry-After`, `Idempotency-Key` на каждый POST.
- Ошибки по классам: `OutsideWindowError`, `RateLimitError`, `UsageLimitError` и другие.
- Итераторы по всем страницам списков: `list_all`, `list_messages_all`, `list_deliveries_all`.
- Проверка подписи вебхуков `webhooks.verify` и типы всех событий.
- Типы всех запросов и ответов с описаниями по-русски.
- Вебхук без секрета не проверяется: `verify` и `sign` с пустым секретом бросают `WebhookVerificationError` (старое имя `WebhookSignatureError` оставлено), константа `DELIVERY_ID_HEADER` для отсева повторов.
- Тело запроса первым аргументом после id или `body=`, у каждого вызова `headers=` и `max_retries=`.
- `BadRequestError`, `ValidationError.fields`, `PaginationError` при повторе курсора, `Retry-After` датой HTTP, код ошибки по статусу для ответов не от API, `CONNECTION_ERROR` и `TIMEOUT`.
- Ключ скрыт в `repr` настроек; `client.api_key` заменён на `client.api_key_hint`.
