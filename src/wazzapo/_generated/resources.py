# Сгенерировано sdk/codegen/python.py из sdk/openapi.json. Не править руками: cd sdk && python -m codegen

"""Методы API v2 по ресурсам: client.messages.send(...), client.contacts.list_all(...)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Dict, Iterator, List, Literal, Optional, Union, cast  # noqa: F401

from .._files import FileInput, _file_part
from .._http import _quote
from .types import (
    AddNoteIn,
    AssignConversationIn,
    BusinessProfileIn,
    BusinessProfileOut,
    BusinessProfileUpdateOut,
    ContactCreateIn,
    ContactListOut,
    ContactUpdateIn,
    ContactV2Out,
    ConversationItemOut,
    ConversationListOut,
    ConversationMessageListOut,
    ConversationMessageOut,
    CreateTemplateIn,
    DealCreateIn,
    DealListOut,
    DealMoveIn,
    DealOut,
    DealUpdateIn,
    MarkReadIn,
    MediaUploadOut,
    PhoneNumberListOut,
    PhoneNumberOut,
    PipelineListOut,
    PipelineOut,
    ReactionIn,
    ReactionOut,
    RegisterPhoneNumberIn,
    RegisterPhoneNumberOut,
    SendMessageIn,
    SendMessageOut,
    SetConversationStatusIn,
    SetLabelsIn,
    SuccessOut,
    TaskCreateIn,
    TaskListOut,
    TaskOut,
    TaskUpdateIn,
    TeamListOut,
    TeamMemberOut,
    TemplateListOut,
    TemplateOut,
    UpdateTemplateIn,
    WebhookCreateIn,
    WebhookDeliveryListOut,
    WebhookDeliveryOut,
    WebhookEventTypeListOut,
    WebhookEventTypeOut,
    WebhookListOut,
    WebhookOut,
    WebhookRetryOut,
    WebhookSecretOut,
    WebhookTestOut,
    WebhookUpdateIn,
    WebhookWithSecretOut,
)

if TYPE_CHECKING:
    from .._client import AsyncWazzapo, Wazzapo

__all__ = [
    "Contacts",
    "AsyncContacts",
    "Conversations",
    "AsyncConversations",
    "Deals",
    "AsyncDeals",
    "Media",
    "AsyncMedia",
    "Messages",
    "AsyncMessages",
    "PhoneNumbers",
    "AsyncPhoneNumbers",
    "Pipelines",
    "AsyncPipelines",
    "Tasks",
    "AsyncTasks",
    "Team",
    "AsyncTeam",
    "Templates",
    "AsyncTemplates",
    "WebhookEventTypes",
    "AsyncWebhookEventTypes",
    "Webhooks",
    "AsyncWebhooks",
]


class Contacts:
    """Методы contacts: create, delete, get, list, update."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def create(
        self,
        *,
        body: ContactCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ContactV2Out:
        """Создать контакт

        Добавляет клиента в контакты: номер обязателен, имя, почта, метки, свои поля и external_id по желанию.

        Номер приводится к виду 77071234567: плюс можно, 8 в начале заменяется на 7. Удалённый ранее
        контакт с этим номером восстанавливается с новыми данными. Свои поля сначала создайте в кабинете,
        раздел «Поля контакта». Заголовок Idempotency-Key защищает от двойного создания при повторе запроса.
        Ошибки: 409 contact_exists (номер уже есть: id в error.details.contact_id, измените его через
        PATCH /contacts/{contact_id}), 422 invalid_phone, 422 unknown_custom_field, 403 USAGE_LIMIT_EXCEEDED
        (лимит контактов тарифа).

        POST /api/v2/external/contacts

        Аргументы:
            body: тело запроса, словарь ContactCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactV2Out",
            self._client._request(
                "POST",
                "/contacts",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def delete(self, contact_id: str, *, timeout: Optional[float] = None) -> None:
        """Удалить контакт

        Удаляет контакт мягко, как в кабинете: он пропадает из списка и поиска, переписка остаётся.

        Восстановить: клиент напишет с этого номера или вызовите POST /contacts с тем же номером.
        Ответ 204 без тела. Ошибки: 404 contact_not_found (уже удалён или чужой).

        DELETE /api/v2/external/contacts/{contact_id}

        Аргументы:
            contact_id: id контакта: поле id из GET /contacts или из ответа POST /contacts, например 6712f0c4a1b2c3d4e5f60718
            timeout: таймаут этого запроса в секундах
        """
        self._client._request("DELETE", f"/contacts/{_quote(contact_id)}", timeout=timeout)
        return None

    def get(self, contact_id: str, *, timeout: Optional[float] = None) -> ContactV2Out:
        """Получить контакт

        Карточка одного контакта: номер, имя, метки, свои поля, источник (attribution).

        id берите из GET /contacts (найти по номеру: ?search=77071234567) или из ответа создания.
        Ошибки: 404 contact_not_found, если контакта нет в этом аккаунте или он удалён.

        GET /api/v2/external/contacts/{contact_id}

        Аргументы:
            contact_id: id контакта: поле id из GET /contacts или из ответа POST /contacts, например 6712f0c4a1b2c3d4e5f60718
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactV2Out",
            self._client._request(
                "GET",
                f"/contacts/{_quote(contact_id)}",
                timeout=timeout,
            ),
        )

    def list(
        self,
        *,
        search: Optional[str] = None,
        tag: Optional[str] = None,
        updated_since: Optional[str] = None,
        external_id: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ContactListOut:
        """Список контактов

        Контакты аккаунта постранично, старые первыми. Удалённые и объединённые не показываются.

        Фильтры складываются: ?search=Айгуль&tag=vip. Найти клиента своей CRM: ?external_id=1c-00042.
        Следующая страница: передайте next_cursor из ответа в ?cursor=, пока has_more=true.
        Ошибки: 401 неверный ключ, 422 неверный cursor или updated_since.

        GET /api/v2/external/contacts

        Аргументы:
            search: Поиск без учёта регистра по части имени (Айгуль) или номера от 3 цифр (7071234, 8 707 123 45 67, +7 707 123-45-67)
            tag: Только контакты с этой меткой, например vip
            updated_since: Только изменённые с этого времени, ISO 8601: 2026-10-01T00:00:00Z. Удобно для обмена с вашей CRM: запоминайте время прошлого запроса
            external_id: Только контакты с этим external_id (вашим id из своей CRM), например 1c-00042
            limit: Сколько контактов на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactListOut",
            self._client._request(
                "GET",
                "/contacts",
                params={"search": search, "tag": tag, "updated_since": updated_since, "external_id": external_id, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        search: Optional[str] = None,
        tag: Optional[str] = None,
        updated_since: Optional[str] = None,
        external_id: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[ContactV2Out]:
        """Список контактов: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            search: Поиск без учёта регистра по части имени (Айгуль) или номера от 3 цифр (7071234, 8 707 123 45 67, +7 707 123-45-67)
            tag: Только контакты с этой меткой, например vip
            updated_since: Только изменённые с этого времени, ISO 8601: 2026-10-01T00:00:00Z. Удобно для обмена с вашей CRM: запоминайте время прошлого запроса
            external_id: Только контакты с этим external_id (вашим id из своей CRM), например 1c-00042
            limit: Сколько контактов на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate(
            "/contacts",
            params={"search": search, "tag": tag, "updated_since": updated_since, "external_id": external_id, "limit": limit},
            timeout=timeout,
        )

    def update(
        self,
        contact_id: str,
        *,
        body: ContactUpdateIn,
        timeout: Optional[float] = None,
    ) -> ContactV2Out:
        """Изменить контакт

        Меняет только переданные поля, остальные остаются как были. Номер не меняется.

        tags заменяют весь список меток. custom_fields дополняют сохранённые: переданный ключ
        перезаписывается, null очищает поле, непереданные не трогаются. Изменение видно менеджерам
        сразу и запускает сценарии на изменение полей, как правка в кабинете.
        Ошибки: 404 contact_not_found, 422 unknown_custom_field.

        PATCH /api/v2/external/contacts/{contact_id}

        Аргументы:
            contact_id: id контакта: поле id из GET /contacts или из ответа POST /contacts, например 6712f0c4a1b2c3d4e5f60718
            body: тело запроса, словарь ContactUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactV2Out",
            self._client._request(
                "PATCH",
                f"/contacts/{_quote(contact_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class AsyncContacts:
    """Методы contacts: create, delete, get, list, update."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def create(
        self,
        *,
        body: ContactCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ContactV2Out:
        """Создать контакт

        Добавляет клиента в контакты: номер обязателен, имя, почта, метки, свои поля и external_id по желанию.

        Номер приводится к виду 77071234567: плюс можно, 8 в начале заменяется на 7. Удалённый ранее
        контакт с этим номером восстанавливается с новыми данными. Свои поля сначала создайте в кабинете,
        раздел «Поля контакта». Заголовок Idempotency-Key защищает от двойного создания при повторе запроса.
        Ошибки: 409 contact_exists (номер уже есть: id в error.details.contact_id, измените его через
        PATCH /contacts/{contact_id}), 422 invalid_phone, 422 unknown_custom_field, 403 USAGE_LIMIT_EXCEEDED
        (лимит контактов тарифа).

        POST /api/v2/external/contacts

        Аргументы:
            body: тело запроса, словарь ContactCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactV2Out",
            await self._client._request(
                "POST",
                "/contacts",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def delete(self, contact_id: str, *, timeout: Optional[float] = None) -> None:
        """Удалить контакт

        Удаляет контакт мягко, как в кабинете: он пропадает из списка и поиска, переписка остаётся.

        Восстановить: клиент напишет с этого номера или вызовите POST /contacts с тем же номером.
        Ответ 204 без тела. Ошибки: 404 contact_not_found (уже удалён или чужой).

        DELETE /api/v2/external/contacts/{contact_id}

        Аргументы:
            contact_id: id контакта: поле id из GET /contacts или из ответа POST /contacts, например 6712f0c4a1b2c3d4e5f60718
            timeout: таймаут этого запроса в секундах
        """
        await self._client._request("DELETE", f"/contacts/{_quote(contact_id)}", timeout=timeout)
        return None

    async def get(self, contact_id: str, *, timeout: Optional[float] = None) -> ContactV2Out:
        """Получить контакт

        Карточка одного контакта: номер, имя, метки, свои поля, источник (attribution).

        id берите из GET /contacts (найти по номеру: ?search=77071234567) или из ответа создания.
        Ошибки: 404 contact_not_found, если контакта нет в этом аккаунте или он удалён.

        GET /api/v2/external/contacts/{contact_id}

        Аргументы:
            contact_id: id контакта: поле id из GET /contacts или из ответа POST /contacts, например 6712f0c4a1b2c3d4e5f60718
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactV2Out",
            await self._client._request(
                "GET",
                f"/contacts/{_quote(contact_id)}",
                timeout=timeout,
            ),
        )

    async def list(
        self,
        *,
        search: Optional[str] = None,
        tag: Optional[str] = None,
        updated_since: Optional[str] = None,
        external_id: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ContactListOut:
        """Список контактов

        Контакты аккаунта постранично, старые первыми. Удалённые и объединённые не показываются.

        Фильтры складываются: ?search=Айгуль&tag=vip. Найти клиента своей CRM: ?external_id=1c-00042.
        Следующая страница: передайте next_cursor из ответа в ?cursor=, пока has_more=true.
        Ошибки: 401 неверный ключ, 422 неверный cursor или updated_since.

        GET /api/v2/external/contacts

        Аргументы:
            search: Поиск без учёта регистра по части имени (Айгуль) или номера от 3 цифр (7071234, 8 707 123 45 67, +7 707 123-45-67)
            tag: Только контакты с этой меткой, например vip
            updated_since: Только изменённые с этого времени, ISO 8601: 2026-10-01T00:00:00Z. Удобно для обмена с вашей CRM: запоминайте время прошлого запроса
            external_id: Только контакты с этим external_id (вашим id из своей CRM), например 1c-00042
            limit: Сколько контактов на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactListOut",
            await self._client._request(
                "GET",
                "/contacts",
                params={"search": search, "tag": tag, "updated_since": updated_since, "external_id": external_id, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        search: Optional[str] = None,
        tag: Optional[str] = None,
        updated_since: Optional[str] = None,
        external_id: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[ContactV2Out]:
        """Список контактов: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            search: Поиск без учёта регистра по части имени (Айгуль) или номера от 3 цифр (7071234, 8 707 123 45 67, +7 707 123-45-67)
            tag: Только контакты с этой меткой, например vip
            updated_since: Только изменённые с этого времени, ISO 8601: 2026-10-01T00:00:00Z. Удобно для обмена с вашей CRM: запоминайте время прошлого запроса
            external_id: Только контакты с этим external_id (вашим id из своей CRM), например 1c-00042
            limit: Сколько контактов на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate(
            "/contacts",
            params={"search": search, "tag": tag, "updated_since": updated_since, "external_id": external_id, "limit": limit},
            timeout=timeout,
        )

    async def update(
        self,
        contact_id: str,
        *,
        body: ContactUpdateIn,
        timeout: Optional[float] = None,
    ) -> ContactV2Out:
        """Изменить контакт

        Меняет только переданные поля, остальные остаются как были. Номер не меняется.

        tags заменяют весь список меток. custom_fields дополняют сохранённые: переданный ключ
        перезаписывается, null очищает поле, непереданные не трогаются. Изменение видно менеджерам
        сразу и запускает сценарии на изменение полей, как правка в кабинете.
        Ошибки: 404 contact_not_found, 422 unknown_custom_field.

        PATCH /api/v2/external/contacts/{contact_id}

        Аргументы:
            contact_id: id контакта: поле id из GET /contacts или из ответа POST /contacts, например 6712f0c4a1b2c3d4e5f60718
            body: тело запроса, словарь ContactUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ContactV2Out",
            await self._client._request(
                "PATCH",
                f"/contacts/{_quote(contact_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class Conversations:
    """Методы conversations: add_note, assign, get, list, list_messages, set_labels, set_status."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def add_note(
        self,
        conversation_id: str,
        *,
        body: AddNoteIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationMessageOut:
        """Добавить заметку

        Добавляет заметку сотрудника в диалог: её видят только сотрудники в кабинете, клиенту она не уходит. Упомянутым в `mention_user_ids` (id из GET /team) приходит уведомление в кабинете. Автор заметки сотрудник, чей ключ. Уходит вебхук `conversation.note_added` (только по явной подписке).

        Передайте заголовок `Idempotency-Key`: повтор запроса с тем же ключом не создаст вторую заметку. В переписке заметка видна с `include_notes=true`.

        Ошибки: 403 `FORBIDDEN`, 404 `conversation_not_found`, 422 `VALIDATION_ERROR` (пустой текст или id не из GET /team). Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/notes

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь AddNoteIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationMessageOut",
            self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/notes",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def assign(
        self,
        conversation_id: str,
        *,
        body: AssignConversationIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationItemOut:
        """Назначить ответственного

        Назначает ответственного менеджера (`user_id`) или снимает его (`null`). id сотрудника возьмите из GET /team: поле `id`, сотрудник должен быть активным (`is_active: true`) и не VIEWER.

        Права как в чате: назначить на другого может владелец, администратор команды или текущий ответственный; взять себе чужой диалог менеджер может, если владелец это разрешил. Новому ответственному приходит уведомление в кабинете, в диалог пишется служебная заметка, уходит вебхук `conversation.assigned`.

        Ошибки: 403 `FORBIDDEN` (у сотрудника ключа нет права назначать или выбран наблюдатель VIEWER), 404 `conversation_not_found`, 409 `CONFLICT` (сотрудник отключён, `is_active: false`, или его нет в команде аккаунта; или диалог одновременно назначили из кабинета: перечитайте и повторите), 422 `VALIDATION_ERROR` (в user_id не только цифры, например «abc»: передайте id строкой из GET /team, например «7»). В сделках и задачах тот же отключённый сотрудник даёт 422 `responsible_user_not_found`: там ответственный проверяется как поле тела запроса. Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/assign

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь AssignConversationIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/assign",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def get(self, conversation_id: str, *, timeout: Optional[float] = None) -> ConversationItemOut:
        """Диалог

        Один диалог по id: контакт, канал, статус, ответственный, метки, непрочитанные и последнее сообщение. id берут из GET /conversations или из поля `conversation_id` вебхука `message.incoming`.

        Ошибка 404 `conversation_not_found`: диалога нет в этом аккаунте или он скрыт от сотрудника, чей ключ. Право ключа: `conversations:read`.

        GET /api/v2/external/conversations/{conversation_id}

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            self._client._request(
                "GET",
                f"/conversations/{_quote(conversation_id)}",
                timeout=timeout,
            ),
        )

    def list(
        self,
        *,
        phone_number_id: Optional[str] = None,
        channel: Optional[Literal['whatsapp', 'telegram', 'instagram', 'olx', 'satu', 'email', 'webchat']] = None,
        status: Optional[Literal['open', 'pending', 'snoozed', 'resolved']] = None,
        assignee_user_id: Optional[str] = None,
        unread: Optional[bool] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationListOut:
        """Список диалогов

        Диалоги аккаунта из всех каналов (WhatsApp, Telegram, Instagram, чат на сайте, OLX, Satu, почта), отсортированные по `updated_at` от давно изменённых к недавним.

        **Синхронизация.** Первый раз выгрузите всё, листая по `next_cursor`, пока `has_more` не станет false. Запомните `updated_at` последнего диалога и в следующий раз передайте его в `updated_since`: придут только диалоги, изменённые после (новое сообщение, статус, ответственный, метки). Диалог, изменённый во время листания, придёт ещё раз в конце, изменения не теряются. Чтобы узнавать сразу, подпишитесь на вебхуки `message.incoming` и `conversation.*`.

        Фильтры складываются: `status=open&assignee_user_id=none` даёт открытые диалоги без ответственного. Ключ сотрудника видит и меняет то же, что сотрудник в чате кабинета: диалоги по правилам видимости команды и только в доступных ему каналах.

        Ошибки: 404 `phone_number_not_found` (чужой или неверный phone_number_id), 422 `VALIDATION_ERROR` (неверный assignee_user_id или cursor). Право ключа: `conversations:read`.

        GET /api/v2/external/conversations

        Аргументы:
            phone_number_id: Только диалоги этого номера WhatsApp: phone_number_id из GET /api/v2/external/phone-numbers, например 103799815708451. Если передан, channel не учитывается
            channel: Только диалоги канала: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
            status: Только диалоги в статусе: open (открыт, нужно ответить), pending (ожидает), snoozed (отложен), resolved (решён)
            assignee_user_id: Только диалоги ответственного: id из GET /api/v2/external/team, например 7; none: диалоги без ответственного
            unread: true: есть непрочитанные сообщения клиента, false: всё прочитано
            updated_since: Только диалоги, изменённые после этого момента, ISO 8601, например 2026-10-01T00:00:00Z. Для синхронизации: updated_at последнего диалога прошлой выгрузки
            limit: Диалогов на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationListOut",
            self._client._request(
                "GET",
                "/conversations",
                params={"phone_number_id": phone_number_id, "channel": channel, "status": status, "assignee_user_id": assignee_user_id, "unread": unread, "updated_since": updated_since, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        phone_number_id: Optional[str] = None,
        channel: Optional[Literal['whatsapp', 'telegram', 'instagram', 'olx', 'satu', 'email', 'webchat']] = None,
        status: Optional[Literal['open', 'pending', 'snoozed', 'resolved']] = None,
        assignee_user_id: Optional[str] = None,
        unread: Optional[bool] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[ConversationItemOut]:
        """Список диалогов: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            phone_number_id: Только диалоги этого номера WhatsApp: phone_number_id из GET /api/v2/external/phone-numbers, например 103799815708451. Если передан, channel не учитывается
            channel: Только диалоги канала: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
            status: Только диалоги в статусе: open (открыт, нужно ответить), pending (ожидает), snoozed (отложен), resolved (решён)
            assignee_user_id: Только диалоги ответственного: id из GET /api/v2/external/team, например 7; none: диалоги без ответственного
            unread: true: есть непрочитанные сообщения клиента, false: всё прочитано
            updated_since: Только диалоги, изменённые после этого момента, ISO 8601, например 2026-10-01T00:00:00Z. Для синхронизации: updated_at последнего диалога прошлой выгрузки
            limit: Диалогов на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate(
            "/conversations",
            params={"phone_number_id": phone_number_id, "channel": channel, "status": status, "assignee_user_id": assignee_user_id, "unread": unread, "updated_since": updated_since, "limit": limit},
            timeout=timeout,
        )

    def list_messages(
        self,
        conversation_id: str,
        *,
        include_notes: Optional[bool] = None,
        since: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationMessageListOut:
        """Переписка диалога

        Переписка диалога от старых сообщений к новым: клиент, менеджеры, сценарии, боты, рассылки и API (кто написал, в `sender.type`). Листайте по `next_cursor`, на последней странице `next_cursor: null`.

        **Только новые сообщения.** Передайте в `since` поле `timestamp` последнего полученного сообщения: придут сообщения после него. Сразу узнавать о новых удобнее вебхуком `message.incoming`.

        Заметки сотрудников (клиент их не видит) приходят только с `include_notes=true`, у них `is_note: true`. Ошибка 404 `conversation_not_found`. Право ключа: `conversations:read`.

        GET /api/v2/external/conversations/{conversation_id}/messages

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            include_notes: true: добавить заметки сотрудников (is_note: true), клиент их не видит
            since: Только сообщения после этого времени, ISO 8601, например 2026-10-18T09:15:00Z: timestamp последнего полученного сообщения
            limit: Сообщений на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationMessageListOut",
            self._client._request(
                "GET",
                f"/conversations/{_quote(conversation_id)}/messages",
                params={"include_notes": include_notes, "since": since, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_messages_all(
        self,
        conversation_id: str,
        *,
        include_notes: Optional[bool] = None,
        since: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[ConversationMessageOut]:
        """Переписка диалога: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            include_notes: true: добавить заметки сотрудников (is_note: true), клиент их не видит
            since: Только сообщения после этого времени, ISO 8601, например 2026-10-18T09:15:00Z: timestamp последнего полученного сообщения
            limit: Сообщений на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate(
            f"/conversations/{_quote(conversation_id)}/messages",
            params={"include_notes": include_notes, "since": since, "limit": limit},
            timeout=timeout,
        )

    def set_labels(
        self,
        conversation_id: str,
        *,
        body: SetLabelsIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationItemOut:
        """Задать метки диалога

        Задаёт метки диалога. Список **заменяет прежний целиком**: чтобы добавить метку, прочитайте текущие `tags` из GET /conversations/{conversation_id} и передайте их вместе с новой; `[]` убирает все. Метки копируются в карточку контакта, как в чате. В ответе метки в поле `tags`.

        Отдельного вебхука о метках нет: изменение видно по `updated_at` диалога. Ошибки: 403 `FORBIDDEN`, 404 `conversation_not_found`. Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/labels

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь SetLabelsIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/labels",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def set_status(
        self,
        conversation_id: str,
        *,
        body: SetConversationStatusIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationItemOut:
        """Сменить статус диалога

        Меняет статус диалога: `open` (открыт, нужно ответить), `pending` (ожидает: например, ответа клиента или решения коллеги), `snoozed` (отложен до `snoozed_until`), `resolved` (решён).

        Закрыть диалог: `{"status": "resolved"}`. Как в чате, клиенту уходит запрос оценки качества, если он включён в настройках, и бот снова отвечает в этом диалоге. Новое сообщение клиента откроет решённый или отложенный диалог само. Уходит вебхук `conversation.status_changed` (если статус действительно изменился).

        Ошибки: 403 `FORBIDDEN` (у сотрудника только просмотр), 404 `conversation_not_found`. Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/status

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь SetConversationStatusIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/status",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )



class AsyncConversations:
    """Методы conversations: add_note, assign, get, list, list_messages, set_labels, set_status."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def add_note(
        self,
        conversation_id: str,
        *,
        body: AddNoteIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationMessageOut:
        """Добавить заметку

        Добавляет заметку сотрудника в диалог: её видят только сотрудники в кабинете, клиенту она не уходит. Упомянутым в `mention_user_ids` (id из GET /team) приходит уведомление в кабинете. Автор заметки сотрудник, чей ключ. Уходит вебхук `conversation.note_added` (только по явной подписке).

        Передайте заголовок `Idempotency-Key`: повтор запроса с тем же ключом не создаст вторую заметку. В переписке заметка видна с `include_notes=true`.

        Ошибки: 403 `FORBIDDEN`, 404 `conversation_not_found`, 422 `VALIDATION_ERROR` (пустой текст или id не из GET /team). Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/notes

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь AddNoteIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationMessageOut",
            await self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/notes",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def assign(
        self,
        conversation_id: str,
        *,
        body: AssignConversationIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationItemOut:
        """Назначить ответственного

        Назначает ответственного менеджера (`user_id`) или снимает его (`null`). id сотрудника возьмите из GET /team: поле `id`, сотрудник должен быть активным (`is_active: true`) и не VIEWER.

        Права как в чате: назначить на другого может владелец, администратор команды или текущий ответственный; взять себе чужой диалог менеджер может, если владелец это разрешил. Новому ответственному приходит уведомление в кабинете, в диалог пишется служебная заметка, уходит вебхук `conversation.assigned`.

        Ошибки: 403 `FORBIDDEN` (у сотрудника ключа нет права назначать или выбран наблюдатель VIEWER), 404 `conversation_not_found`, 409 `CONFLICT` (сотрудник отключён, `is_active: false`, или его нет в команде аккаунта; или диалог одновременно назначили из кабинета: перечитайте и повторите), 422 `VALIDATION_ERROR` (в user_id не только цифры, например «abc»: передайте id строкой из GET /team, например «7»). В сделках и задачах тот же отключённый сотрудник даёт 422 `responsible_user_not_found`: там ответственный проверяется как поле тела запроса. Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/assign

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь AssignConversationIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            await self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/assign",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def get(self, conversation_id: str, *, timeout: Optional[float] = None) -> ConversationItemOut:
        """Диалог

        Один диалог по id: контакт, канал, статус, ответственный, метки, непрочитанные и последнее сообщение. id берут из GET /conversations или из поля `conversation_id` вебхука `message.incoming`.

        Ошибка 404 `conversation_not_found`: диалога нет в этом аккаунте или он скрыт от сотрудника, чей ключ. Право ключа: `conversations:read`.

        GET /api/v2/external/conversations/{conversation_id}

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            await self._client._request(
                "GET",
                f"/conversations/{_quote(conversation_id)}",
                timeout=timeout,
            ),
        )

    async def list(
        self,
        *,
        phone_number_id: Optional[str] = None,
        channel: Optional[Literal['whatsapp', 'telegram', 'instagram', 'olx', 'satu', 'email', 'webchat']] = None,
        status: Optional[Literal['open', 'pending', 'snoozed', 'resolved']] = None,
        assignee_user_id: Optional[str] = None,
        unread: Optional[bool] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationListOut:
        """Список диалогов

        Диалоги аккаунта из всех каналов (WhatsApp, Telegram, Instagram, чат на сайте, OLX, Satu, почта), отсортированные по `updated_at` от давно изменённых к недавним.

        **Синхронизация.** Первый раз выгрузите всё, листая по `next_cursor`, пока `has_more` не станет false. Запомните `updated_at` последнего диалога и в следующий раз передайте его в `updated_since`: придут только диалоги, изменённые после (новое сообщение, статус, ответственный, метки). Диалог, изменённый во время листания, придёт ещё раз в конце, изменения не теряются. Чтобы узнавать сразу, подпишитесь на вебхуки `message.incoming` и `conversation.*`.

        Фильтры складываются: `status=open&assignee_user_id=none` даёт открытые диалоги без ответственного. Ключ сотрудника видит и меняет то же, что сотрудник в чате кабинета: диалоги по правилам видимости команды и только в доступных ему каналах.

        Ошибки: 404 `phone_number_not_found` (чужой или неверный phone_number_id), 422 `VALIDATION_ERROR` (неверный assignee_user_id или cursor). Право ключа: `conversations:read`.

        GET /api/v2/external/conversations

        Аргументы:
            phone_number_id: Только диалоги этого номера WhatsApp: phone_number_id из GET /api/v2/external/phone-numbers, например 103799815708451. Если передан, channel не учитывается
            channel: Только диалоги канала: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
            status: Только диалоги в статусе: open (открыт, нужно ответить), pending (ожидает), snoozed (отложен), resolved (решён)
            assignee_user_id: Только диалоги ответственного: id из GET /api/v2/external/team, например 7; none: диалоги без ответственного
            unread: true: есть непрочитанные сообщения клиента, false: всё прочитано
            updated_since: Только диалоги, изменённые после этого момента, ISO 8601, например 2026-10-01T00:00:00Z. Для синхронизации: updated_at последнего диалога прошлой выгрузки
            limit: Диалогов на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationListOut",
            await self._client._request(
                "GET",
                "/conversations",
                params={"phone_number_id": phone_number_id, "channel": channel, "status": status, "assignee_user_id": assignee_user_id, "unread": unread, "updated_since": updated_since, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        phone_number_id: Optional[str] = None,
        channel: Optional[Literal['whatsapp', 'telegram', 'instagram', 'olx', 'satu', 'email', 'webchat']] = None,
        status: Optional[Literal['open', 'pending', 'snoozed', 'resolved']] = None,
        assignee_user_id: Optional[str] = None,
        unread: Optional[bool] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[ConversationItemOut]:
        """Список диалогов: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            phone_number_id: Только диалоги этого номера WhatsApp: phone_number_id из GET /api/v2/external/phone-numbers, например 103799815708451. Если передан, channel не учитывается
            channel: Только диалоги канала: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
            status: Только диалоги в статусе: open (открыт, нужно ответить), pending (ожидает), snoozed (отложен), resolved (решён)
            assignee_user_id: Только диалоги ответственного: id из GET /api/v2/external/team, например 7; none: диалоги без ответственного
            unread: true: есть непрочитанные сообщения клиента, false: всё прочитано
            updated_since: Только диалоги, изменённые после этого момента, ISO 8601, например 2026-10-01T00:00:00Z. Для синхронизации: updated_at последнего диалога прошлой выгрузки
            limit: Диалогов на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate(
            "/conversations",
            params={"phone_number_id": phone_number_id, "channel": channel, "status": status, "assignee_user_id": assignee_user_id, "unread": unread, "updated_since": updated_since, "limit": limit},
            timeout=timeout,
        )

    async def list_messages(
        self,
        conversation_id: str,
        *,
        include_notes: Optional[bool] = None,
        since: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationMessageListOut:
        """Переписка диалога

        Переписка диалога от старых сообщений к новым: клиент, менеджеры, сценарии, боты, рассылки и API (кто написал, в `sender.type`). Листайте по `next_cursor`, на последней странице `next_cursor: null`.

        **Только новые сообщения.** Передайте в `since` поле `timestamp` последнего полученного сообщения: придут сообщения после него. Сразу узнавать о новых удобнее вебхуком `message.incoming`.

        Заметки сотрудников (клиент их не видит) приходят только с `include_notes=true`, у них `is_note: true`. Ошибка 404 `conversation_not_found`. Право ключа: `conversations:read`.

        GET /api/v2/external/conversations/{conversation_id}/messages

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            include_notes: true: добавить заметки сотрудников (is_note: true), клиент их не видит
            since: Только сообщения после этого времени, ISO 8601, например 2026-10-18T09:15:00Z: timestamp последнего полученного сообщения
            limit: Сообщений на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationMessageListOut",
            await self._client._request(
                "GET",
                f"/conversations/{_quote(conversation_id)}/messages",
                params={"include_notes": include_notes, "since": since, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_messages_all(
        self,
        conversation_id: str,
        *,
        include_notes: Optional[bool] = None,
        since: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[ConversationMessageOut]:
        """Переписка диалога: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            include_notes: true: добавить заметки сотрудников (is_note: true), клиент их не видит
            since: Только сообщения после этого времени, ISO 8601, например 2026-10-18T09:15:00Z: timestamp последнего полученного сообщения
            limit: Сообщений на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate(
            f"/conversations/{_quote(conversation_id)}/messages",
            params={"include_notes": include_notes, "since": since, "limit": limit},
            timeout=timeout,
        )

    async def set_labels(
        self,
        conversation_id: str,
        *,
        body: SetLabelsIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationItemOut:
        """Задать метки диалога

        Задаёт метки диалога. Список **заменяет прежний целиком**: чтобы добавить метку, прочитайте текущие `tags` из GET /conversations/{conversation_id} и передайте их вместе с новой; `[]` убирает все. Метки копируются в карточку контакта, как в чате. В ответе метки в поле `tags`.

        Отдельного вебхука о метках нет: изменение видно по `updated_at` диалога. Ошибки: 403 `FORBIDDEN`, 404 `conversation_not_found`. Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/labels

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь SetLabelsIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            await self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/labels",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def set_status(
        self,
        conversation_id: str,
        *,
        body: SetConversationStatusIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ConversationItemOut:
        """Сменить статус диалога

        Меняет статус диалога: `open` (открыт, нужно ответить), `pending` (ожидает: например, ответа клиента или решения коллеги), `snoozed` (отложен до `snoozed_until`), `resolved` (решён).

        Закрыть диалог: `{"status": "resolved"}`. Как в чате, клиенту уходит запрос оценки качества, если он включён в настройках, и бот снова отвечает в этом диалоге. Новое сообщение клиента откроет решённый или отложенный диалог само. Уходит вебхук `conversation.status_changed` (если статус действительно изменился).

        Ошибки: 403 `FORBIDDEN` (у сотрудника только просмотр), 404 `conversation_not_found`. Право ключа: `conversations:write`.

        POST /api/v2/external/conversations/{conversation_id}/status

        Аргументы:
            conversation_id: id диалога: поле id из GET /api/v2/external/conversations или conversation_id из вебхука message.incoming, например 6a7d5d3712f8e1a5c19f40c4
            body: тело запроса, словарь SetConversationStatusIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ConversationItemOut",
            await self._client._request(
                "POST",
                f"/conversations/{_quote(conversation_id)}/status",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )



class Deals:
    """Методы deals: create, get, list, move, update."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def create(
        self,
        *,
        body: DealCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> DealOut:
        """Создать сделку

        Создаёт сделку, например из заявки с сайта, так же, как окно «Новая сделка» в кабинете.

        До вызова: pipeline_id и stage_id из GET /pipelines, ответственный из GET /team. Клиент:
        contact_id из GET /contacts или contact {phone, name}: найдём контакт по номеру или создадим.
        Сумма amount целым в тиынах, не в тенге: 150 000 ₸ = 15000000 (в шаблоне WhatsApp
        сумма другая: amount_1000 = 150000000). custom_fields по id полей воронки.
        Без дублей: передайте свой external_id. Повтор формы с тем же external_id, который уже
        есть у сделки аккаунта, сделку не создаёт: 409 deal_exists, id существующей в
        details.deal_id. Два одновременных запроса закрывает ещё и заголовок Idempotency-Key:
        шлите тот же ключ при повторе после сбоя сети.
        responsible_user_id ставит ответственного только сделки: ответственный переписки не
        меняется, для него POST /conversations/{conversation_id}/assign.
        Срабатывают действия этапа и уходит вебхук deal.created. Право deals:write.
        Частые ошибки: 404 pipeline_not_found, 422 stage_not_found, unknown_custom_field,
        amount_field_missing (в воронке нет поля суммы), responsible_user_not_found (нет такого
        сотрудника или он отключён: is_active false в GET /team), VALIDATION_ERROR (нет ни
        contact_id, ни contact), 404 contact_not_found, 409 deal_exists. Код open_deal_exists
        (у переписки уже есть открытая сделка) этот метод не возвращает: сделка из API не
        проверяет переписку и создаётся, даже если у клиента есть открытая в этой воронке.

        POST /api/v2/external/deals

        Аргументы:
            body: тело запроса, словарь DealCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealOut",
            self._client._request(
                "POST",
                "/deals",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def get(self, deal_id: str, *, timeout: Optional[float] = None) -> DealOut:
        """Сделка

        Одна сделка: этап, сумма в тиынах, клиент, ответственный, свои поля.

        Сделка чужого аккаунта или скрытая от сотрудника, которому выдан ключ: 404 deal_not_found.
        Право deals:read.

        GET /api/v2/external/deals/{deal_id}

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            timeout: таймаут этого запроса в секундах
        """
        return cast("DealOut", self._client._request("GET", f"/deals/{_quote(deal_id)}", timeout=timeout))

    def list(
        self,
        *,
        pipeline_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        external_id: Optional[str] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> DealListOut:
        """Список сделок

        Сделки аккаунта по времени изменения, старые первыми, страницами по cursor.

        Синхронизация с вашей системой: запомните updated_at последней сделки и в следующий раз
        передайте его в updated_since. Дубль перед созданием ищут по external_id.
        Сумма amount и денежные custom_fields в тиынах (150 000 ₸ = 15000000).
        Ключ сотрудника видит те же сделки, что сотрудник в кабинете. Право deals:read.

        GET /api/v2/external/deals

        Аргументы:
            pipeline_id: Только сделки воронки: id из GET /pipelines
            stage_id: Только сделки на этапе: stages[].id из GET /pipelines
            contact_id: Только сделки клиента: id контакта из GET /contacts
            external_id: Найти сделку по вашему id (external_id при создании), например site-order-4521: так проверяют дубль перед POST /deals
            updated_since: Только изменённые начиная с этого времени, ISO 8601, например 2026-10-18T00:00:00Z
            limit: Сколько сделок на странице, от 1 до 200, по умолчанию 50
            cursor: next_cursor из прошлого ответа; для первой страницы не передавайте
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealListOut",
            self._client._request(
                "GET",
                "/deals",
                params={"pipeline_id": pipeline_id, "stage_id": stage_id, "contact_id": contact_id, "external_id": external_id, "updated_since": updated_since, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        pipeline_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        external_id: Optional[str] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[DealOut]:
        """Список сделок: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            pipeline_id: Только сделки воронки: id из GET /pipelines
            stage_id: Только сделки на этапе: stages[].id из GET /pipelines
            contact_id: Только сделки клиента: id контакта из GET /contacts
            external_id: Найти сделку по вашему id (external_id при создании), например site-order-4521: так проверяют дубль перед POST /deals
            updated_since: Только изменённые начиная с этого времени, ISO 8601, например 2026-10-18T00:00:00Z
            limit: Сколько сделок на странице, от 1 до 200, по умолчанию 50
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate(
            "/deals",
            params={"pipeline_id": pipeline_id, "stage_id": stage_id, "contact_id": contact_id, "external_id": external_id, "updated_since": updated_since, "limit": limit},
            timeout=timeout,
        )

    def move(
        self,
        deal_id: str,
        *,
        body: DealMoveIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> DealOut:
        """Перенести сделку на этап

        Переносит сделку на другой этап её воронки, как перетаскивание карточки в кабинете.

        stage_id берите из stages[] воронки в GET /pipelines. Перенос на этап с is_won закрывает
        сделку успехом, на этап с is_lost отказом (причину передайте в lost_reason).
        После переноса срабатывает то же, что в кабинете: сценарии «Событие в воронке», действия
        этапа (поставить или закрыть задачи), вебхуки deal.stage_changed и при закрытии deal.closed, передача
        продажи или заявки в Meta, если клиент пришёл с рекламы «Написать в WhatsApp».
        Поля, обязательные с этого этапа (custom_fields[].required_from_stage_id в GET /pipelines),
        заполните заранее через PATCH /deals/{deal_id}, иначе
        422 required_fields со списком полей в details. Другая воронка: 422 pipeline_change_not_supported.
        Право deals:write.

        POST /api/v2/external/deals/{deal_id}/move

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            body: тело запроса, словарь DealMoveIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealOut",
            self._client._request(
                "POST",
                f"/deals/{_quote(deal_id)}/move",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def update(self, deal_id: str, *, body: DealUpdateIn, timeout: Optional[float] = None) -> DealOut:
        """Изменить сделку

        Меняет название, сумму, ответственного, свои поля и external_id сделки.

        Меняются только переданные поля, остальные не трогаются. Сумма amount целым в тиынах.
        В custom_fields передавайте только меняемые поля, null очищает поле. Снять ответственного
        нельзя: responsible_user_id=null значит «не менять». Ответственный меняется только у
        сделки, не у переписки (её: POST /conversations/{conversation_id}/assign); если в
        кабинете включено правило, новому ответственному ставится задача. Этап этим методом не меняется:
        для этого POST /deals/{deal_id}/move. В ленте сделки появится «было → стало», уходит
        вебхук deal.changed. Право deals:write.
        Частые ошибки: 404 deal_not_found, 422 unknown_custom_field, responsible_user_not_found
        (нет такого сотрудника или он отключён), currency_mismatch.

        PATCH /api/v2/external/deals/{deal_id}

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            body: тело запроса, словарь DealUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealOut",
            self._client._request(
                "PATCH",
                f"/deals/{_quote(deal_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class AsyncDeals:
    """Методы deals: create, get, list, move, update."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def create(
        self,
        *,
        body: DealCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> DealOut:
        """Создать сделку

        Создаёт сделку, например из заявки с сайта, так же, как окно «Новая сделка» в кабинете.

        До вызова: pipeline_id и stage_id из GET /pipelines, ответственный из GET /team. Клиент:
        contact_id из GET /contacts или contact {phone, name}: найдём контакт по номеру или создадим.
        Сумма amount целым в тиынах, не в тенге: 150 000 ₸ = 15000000 (в шаблоне WhatsApp
        сумма другая: amount_1000 = 150000000). custom_fields по id полей воронки.
        Без дублей: передайте свой external_id. Повтор формы с тем же external_id, который уже
        есть у сделки аккаунта, сделку не создаёт: 409 deal_exists, id существующей в
        details.deal_id. Два одновременных запроса закрывает ещё и заголовок Idempotency-Key:
        шлите тот же ключ при повторе после сбоя сети.
        responsible_user_id ставит ответственного только сделки: ответственный переписки не
        меняется, для него POST /conversations/{conversation_id}/assign.
        Срабатывают действия этапа и уходит вебхук deal.created. Право deals:write.
        Частые ошибки: 404 pipeline_not_found, 422 stage_not_found, unknown_custom_field,
        amount_field_missing (в воронке нет поля суммы), responsible_user_not_found (нет такого
        сотрудника или он отключён: is_active false в GET /team), VALIDATION_ERROR (нет ни
        contact_id, ни contact), 404 contact_not_found, 409 deal_exists. Код open_deal_exists
        (у переписки уже есть открытая сделка) этот метод не возвращает: сделка из API не
        проверяет переписку и создаётся, даже если у клиента есть открытая в этой воронке.

        POST /api/v2/external/deals

        Аргументы:
            body: тело запроса, словарь DealCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealOut",
            await self._client._request(
                "POST",
                "/deals",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def get(self, deal_id: str, *, timeout: Optional[float] = None) -> DealOut:
        """Сделка

        Одна сделка: этап, сумма в тиынах, клиент, ответственный, свои поля.

        Сделка чужого аккаунта или скрытая от сотрудника, которому выдан ключ: 404 deal_not_found.
        Право deals:read.

        GET /api/v2/external/deals/{deal_id}

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealOut",
            await self._client._request(
                "GET",
                f"/deals/{_quote(deal_id)}",
                timeout=timeout,
            ),
        )

    async def list(
        self,
        *,
        pipeline_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        external_id: Optional[str] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> DealListOut:
        """Список сделок

        Сделки аккаунта по времени изменения, старые первыми, страницами по cursor.

        Синхронизация с вашей системой: запомните updated_at последней сделки и в следующий раз
        передайте его в updated_since. Дубль перед созданием ищут по external_id.
        Сумма amount и денежные custom_fields в тиынах (150 000 ₸ = 15000000).
        Ключ сотрудника видит те же сделки, что сотрудник в кабинете. Право deals:read.

        GET /api/v2/external/deals

        Аргументы:
            pipeline_id: Только сделки воронки: id из GET /pipelines
            stage_id: Только сделки на этапе: stages[].id из GET /pipelines
            contact_id: Только сделки клиента: id контакта из GET /contacts
            external_id: Найти сделку по вашему id (external_id при создании), например site-order-4521: так проверяют дубль перед POST /deals
            updated_since: Только изменённые начиная с этого времени, ISO 8601, например 2026-10-18T00:00:00Z
            limit: Сколько сделок на странице, от 1 до 200, по умолчанию 50
            cursor: next_cursor из прошлого ответа; для первой страницы не передавайте
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealListOut",
            await self._client._request(
                "GET",
                "/deals",
                params={"pipeline_id": pipeline_id, "stage_id": stage_id, "contact_id": contact_id, "external_id": external_id, "updated_since": updated_since, "limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        pipeline_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        external_id: Optional[str] = None,
        updated_since: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[DealOut]:
        """Список сделок: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            pipeline_id: Только сделки воронки: id из GET /pipelines
            stage_id: Только сделки на этапе: stages[].id из GET /pipelines
            contact_id: Только сделки клиента: id контакта из GET /contacts
            external_id: Найти сделку по вашему id (external_id при создании), например site-order-4521: так проверяют дубль перед POST /deals
            updated_since: Только изменённые начиная с этого времени, ISO 8601, например 2026-10-18T00:00:00Z
            limit: Сколько сделок на странице, от 1 до 200, по умолчанию 50
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate(
            "/deals",
            params={"pipeline_id": pipeline_id, "stage_id": stage_id, "contact_id": contact_id, "external_id": external_id, "updated_since": updated_since, "limit": limit},
            timeout=timeout,
        )

    async def move(
        self,
        deal_id: str,
        *,
        body: DealMoveIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> DealOut:
        """Перенести сделку на этап

        Переносит сделку на другой этап её воронки, как перетаскивание карточки в кабинете.

        stage_id берите из stages[] воронки в GET /pipelines. Перенос на этап с is_won закрывает
        сделку успехом, на этап с is_lost отказом (причину передайте в lost_reason).
        После переноса срабатывает то же, что в кабинете: сценарии «Событие в воронке», действия
        этапа (поставить или закрыть задачи), вебхуки deal.stage_changed и при закрытии deal.closed, передача
        продажи или заявки в Meta, если клиент пришёл с рекламы «Написать в WhatsApp».
        Поля, обязательные с этого этапа (custom_fields[].required_from_stage_id в GET /pipelines),
        заполните заранее через PATCH /deals/{deal_id}, иначе
        422 required_fields со списком полей в details. Другая воронка: 422 pipeline_change_not_supported.
        Право deals:write.

        POST /api/v2/external/deals/{deal_id}/move

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            body: тело запроса, словарь DealMoveIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealOut",
            await self._client._request(
                "POST",
                f"/deals/{_quote(deal_id)}/move",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def update(self, deal_id: str, *, body: DealUpdateIn, timeout: Optional[float] = None) -> DealOut:
        """Изменить сделку

        Меняет название, сумму, ответственного, свои поля и external_id сделки.

        Меняются только переданные поля, остальные не трогаются. Сумма amount целым в тиынах.
        В custom_fields передавайте только меняемые поля, null очищает поле. Снять ответственного
        нельзя: responsible_user_id=null значит «не менять». Ответственный меняется только у
        сделки, не у переписки (её: POST /conversations/{conversation_id}/assign); если в
        кабинете включено правило, новому ответственному ставится задача. Этап этим методом не меняется:
        для этого POST /deals/{deal_id}/move. В ленте сделки появится «было → стало», уходит
        вебхук deal.changed. Право deals:write.
        Частые ошибки: 404 deal_not_found, 422 unknown_custom_field, responsible_user_not_found
        (нет такого сотрудника или он отключён), currency_mismatch.

        PATCH /api/v2/external/deals/{deal_id}

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            body: тело запроса, словарь DealUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "DealOut",
            await self._client._request(
                "PATCH",
                f"/deals/{_quote(deal_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class Media:
    """Методы media: download, upload."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def download(self, media_id: str, *, phone_number_id: str, timeout: Optional[float] = None) -> bytes:
        """Скачать файл

        Скачивает файл по media_id: тело ответа сам файл, тип в заголовке Content-Type.

        Так забирают фото, голосовые и документы, которые прислал клиент. Сохраните файл у себя:
        Meta хранит его ограниченное время. Ошибки: 400 BAD_REQUEST (номер не через Cloud API),
        502 provider_error (файл удалён в Meta или сбой).

        GET /api/v2/external/media/{media_id}

        Аргументы:
            media_id: id файла: media.id из входящего сообщения (вебхук message.incoming) или из POST /media
            phone_number_id: id номера: phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "bytes",
            self._client._request(
                "GET",
                f"/media/{_quote(media_id)}",
                params={"phone_number_id": phone_number_id},
                timeout=timeout,
                raw=True,
            ),
        )

    def upload(
        self,
        file: FileInput,
        *,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        phone_number_id: str,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> MediaUploadOut:
        """Загрузить файл

        Загружает файл в WhatsApp и возвращает media_id для отправки в POST /messages/send.

        Нужен, когда у файла нет публичной ссылки, и для голосовых OGG/OPUS (по ссылке Meta их
        не доставляет). Пример: curl -F "file=@schet_1024.pdf" "…/media?phone_number_id=123456789012345".
        media_id действует 30 дней. Повтор с тем же Idempotency-Key
        не загружает файл второй раз. Ошибки: 400 BAD_REQUEST (номер не через Cloud API),
        413 PAYLOAD_TOO_LARGE, 422 media_unavailable (формат не подходит).

        POST /api/v2/external/media

        Аргументы:
            file: путь к файлу, bytes или открытый файл (до 100 МБ)
            filename: имя файла для WhatsApp, по умолчанию из пути
            content_type: тип файла, по умолчанию по расширению
            phone_number_id: id номера: phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "MediaUploadOut",
            self._client._request(
                "POST",
                "/media",
                params={"phone_number_id": phone_number_id},
                files=_file_part(file, filename, content_type),
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )



class AsyncMedia:
    """Методы media: download, upload."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def download(
        self,
        media_id: str,
        *,
        phone_number_id: str,
        timeout: Optional[float] = None,
    ) -> bytes:
        """Скачать файл

        Скачивает файл по media_id: тело ответа сам файл, тип в заголовке Content-Type.

        Так забирают фото, голосовые и документы, которые прислал клиент. Сохраните файл у себя:
        Meta хранит его ограниченное время. Ошибки: 400 BAD_REQUEST (номер не через Cloud API),
        502 provider_error (файл удалён в Meta или сбой).

        GET /api/v2/external/media/{media_id}

        Аргументы:
            media_id: id файла: media.id из входящего сообщения (вебхук message.incoming) или из POST /media
            phone_number_id: id номера: phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "bytes",
            await self._client._request(
                "GET",
                f"/media/{_quote(media_id)}",
                params={"phone_number_id": phone_number_id},
                timeout=timeout,
                raw=True,
            ),
        )

    async def upload(
        self,
        file: FileInput,
        *,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
        phone_number_id: str,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> MediaUploadOut:
        """Загрузить файл

        Загружает файл в WhatsApp и возвращает media_id для отправки в POST /messages/send.

        Нужен, когда у файла нет публичной ссылки, и для голосовых OGG/OPUS (по ссылке Meta их
        не доставляет). Пример: curl -F "file=@schet_1024.pdf" "…/media?phone_number_id=123456789012345".
        media_id действует 30 дней. Повтор с тем же Idempotency-Key
        не загружает файл второй раз. Ошибки: 400 BAD_REQUEST (номер не через Cloud API),
        413 PAYLOAD_TOO_LARGE, 422 media_unavailable (формат не подходит).

        POST /api/v2/external/media

        Аргументы:
            file: путь к файлу, bytes или открытый файл (до 100 МБ)
            filename: имя файла для WhatsApp, по умолчанию из пути
            content_type: тип файла, по умолчанию по расширению
            phone_number_id: id номера: phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "MediaUploadOut",
            await self._client._request(
                "POST",
                "/media",
                params={"phone_number_id": phone_number_id},
                files=_file_part(file, filename, content_type),
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )



class Messages:
    """Методы messages: mark_read, react, send."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def mark_read(
        self,
        *,
        body: MarkReadIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> SuccessOut:
        """Отметить прочитанными

        Отмечает входящие сообщения прочитанными: клиент увидит синие галочки.

        Передайте wamid входящих из вебхука message.incoming. Отметка в WhatsApp не меняет
        счётчик непрочитанных в кабинете. Тестовый ключ ничего не отправляет.
        Ошибки: 404 phone_number_not_found, 501 not_supported (номер не через Cloud API).

        POST /api/v2/external/messages/mark-read

        Аргументы:
            body: тело запроса, словарь MarkReadIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "SuccessOut",
            self._client._request(
                "POST",
                "/messages/mark-read",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def react(
        self,
        *,
        body: ReactionIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ReactionOut:
        """Поставить реакцию

        Ставит эмодзи-реакцию на сообщение клиента или своё; пустой emoji снимает реакцию.

        Meta принимает реакцию на сообщения не старше 30 дней. Тестовый ключ ничего не отправляет.
        Ошибки: 404 phone_number_not_found, 422 invalid_parameters (неверный message_id), 501 not_supported.

        POST /api/v2/external/messages/reaction

        Аргументы:
            body: тело запроса, словарь ReactionIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ReactionOut",
            self._client._request(
                "POST",
                "/messages/reaction",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def send(
        self,
        *,
        body: SendMessageIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> SendMessageOut:
        """Отправить сообщение

        Отправляет клиенту сообщение с номера phone_number_id (GET /api/v2/external/phone-numbers).

        **Окно 24 часа.** Обычное сообщение (текст, файл, кнопки, место) можно отправить, только если клиент писал вам за последние 24 часа. Первое сообщение и всё вне окна: только одобренный шаблон (type=template, имена в GET /api/v2/external/templates).

        **Файлы.** Передайте link (публичная ссылка https) или id: сначала загрузите файл в POST /api/v2/external/media и возьмите media_id из ответа.

        **Повтор.** Заголовок Idempotency-Key: повтор с тем же ключом не отправит второе сообщение, а вернёт первый ответ.

        **Тестовый ключ** wz_test_… ничего не отправляет и отвечает id вида wamid.SANDBOX….

        **После отправки** сообщение появляется в переписке кабинета, а на ваш адрес приходит вебхук message.outgoing; статусы доставки и прочтения приходят вебхуком message.status с тем же message_id.

        **Лимиты.** Каждое сообщение расходует лимит тарифа (403 USAGE_LIMIT_EXCEEDED); частоту запросов показывают заголовки X-RateLimit-*. Meta тоже ограничивает частоту (429 rate_limited).

        **Как узнать, открыто ли окно.** Окно 24 часа отсчитывается от последнего входящего сообщения клиента: возьмите timestamp последнего сообщения с direction=in из GET /api/v2/external/conversations/{conversation_id}/messages (или время вебхука message.incoming) и прибавьте 24 часа. Позже этого времени отправляйте шаблон.

        **Сумма в шаблоне** (type=currency): amount_1000 = тенге × 1000, 150 000 ₸ = 150000000. В сделках сумма в тиынах (× 100): 150 000 ₸ = 15000000.

        **Частые ошибки:** 422 outside_24h_window (окно закрыто, отправьте шаблон), 422 template_not_found (нет одобренного шаблона с таким именем и языком; именно 422, а не 404: адрес /messages/send существует, не подходит значение в теле. GET /templates/{template_id} с неизвестным id отвечает 404), 422 invalid_parameters (type не совпадает с блоком, например type=text вместе с template, или файл без id и link), 422 recipient_unavailable (у номера нет WhatsApp), 422 media_unavailable (Meta не скачала файл по ссылке), 404 phone_number_not_found.

        POST /api/v2/external/messages/send

        Аргументы:
            body: тело запроса, словарь SendMessageIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "SendMessageOut",
            self._client._request(
                "POST",
                "/messages/send",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )



class AsyncMessages:
    """Методы messages: mark_read, react, send."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def mark_read(
        self,
        *,
        body: MarkReadIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> SuccessOut:
        """Отметить прочитанными

        Отмечает входящие сообщения прочитанными: клиент увидит синие галочки.

        Передайте wamid входящих из вебхука message.incoming. Отметка в WhatsApp не меняет
        счётчик непрочитанных в кабинете. Тестовый ключ ничего не отправляет.
        Ошибки: 404 phone_number_not_found, 501 not_supported (номер не через Cloud API).

        POST /api/v2/external/messages/mark-read

        Аргументы:
            body: тело запроса, словарь MarkReadIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "SuccessOut",
            await self._client._request(
                "POST",
                "/messages/mark-read",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def react(
        self,
        *,
        body: ReactionIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> ReactionOut:
        """Поставить реакцию

        Ставит эмодзи-реакцию на сообщение клиента или своё; пустой emoji снимает реакцию.

        Meta принимает реакцию на сообщения не старше 30 дней. Тестовый ключ ничего не отправляет.
        Ошибки: 404 phone_number_not_found, 422 invalid_parameters (неверный message_id), 501 not_supported.

        POST /api/v2/external/messages/reaction

        Аргументы:
            body: тело запроса, словарь ReactionIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "ReactionOut",
            await self._client._request(
                "POST",
                "/messages/reaction",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def send(
        self,
        *,
        body: SendMessageIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> SendMessageOut:
        """Отправить сообщение

        Отправляет клиенту сообщение с номера phone_number_id (GET /api/v2/external/phone-numbers).

        **Окно 24 часа.** Обычное сообщение (текст, файл, кнопки, место) можно отправить, только если клиент писал вам за последние 24 часа. Первое сообщение и всё вне окна: только одобренный шаблон (type=template, имена в GET /api/v2/external/templates).

        **Файлы.** Передайте link (публичная ссылка https) или id: сначала загрузите файл в POST /api/v2/external/media и возьмите media_id из ответа.

        **Повтор.** Заголовок Idempotency-Key: повтор с тем же ключом не отправит второе сообщение, а вернёт первый ответ.

        **Тестовый ключ** wz_test_… ничего не отправляет и отвечает id вида wamid.SANDBOX….

        **После отправки** сообщение появляется в переписке кабинета, а на ваш адрес приходит вебхук message.outgoing; статусы доставки и прочтения приходят вебхуком message.status с тем же message_id.

        **Лимиты.** Каждое сообщение расходует лимит тарифа (403 USAGE_LIMIT_EXCEEDED); частоту запросов показывают заголовки X-RateLimit-*. Meta тоже ограничивает частоту (429 rate_limited).

        **Как узнать, открыто ли окно.** Окно 24 часа отсчитывается от последнего входящего сообщения клиента: возьмите timestamp последнего сообщения с direction=in из GET /api/v2/external/conversations/{conversation_id}/messages (или время вебхука message.incoming) и прибавьте 24 часа. Позже этого времени отправляйте шаблон.

        **Сумма в шаблоне** (type=currency): amount_1000 = тенге × 1000, 150 000 ₸ = 150000000. В сделках сумма в тиынах (× 100): 150 000 ₸ = 15000000.

        **Частые ошибки:** 422 outside_24h_window (окно закрыто, отправьте шаблон), 422 template_not_found (нет одобренного шаблона с таким именем и языком; именно 422, а не 404: адрес /messages/send существует, не подходит значение в теле. GET /templates/{template_id} с неизвестным id отвечает 404), 422 invalid_parameters (type не совпадает с блоком, например type=text вместе с template, или файл без id и link), 422 recipient_unavailable (у номера нет WhatsApp), 422 media_unavailable (Meta не скачала файл по ссылке), 404 phone_number_not_found.

        POST /api/v2/external/messages/send

        Аргументы:
            body: тело запроса, словарь SendMessageIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "SendMessageOut",
            await self._client._request(
                "POST",
                "/messages/send",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )



class PhoneNumbers:
    """Методы phone_numbers: create, delete, get, get_business_profile, list, update_business_profile."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def create(
        self,
        *,
        body: RegisterPhoneNumberIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> RegisterPhoneNumberOut:
        """Подключить номер

        Начинает подключение нового номера WhatsApp.

        В ответе может быть embedded_signup_url: откройте его во всплывающем окне, владелец
        номера войдёт в Facebook и подтвердит номер в Meta. Пока подключение не завершено,
        status=pending. Номер расходует лимит устройств тарифа.
        Ошибки: 402 DEVICE_QUOTA_EXCEEDED (лимит номеров), 503 SERVICE_UNAVAILABLE
        (подключение через API недоступно, подключите номер в кабинете).

        POST /api/v2/external/phone-numbers

        Аргументы:
            body: тело запроса, словарь RegisterPhoneNumberIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "RegisterPhoneNumberOut",
            self._client._request(
                "POST",
                "/phone-numbers",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def delete(self, phone_number_id: str, *, timeout: Optional[float] = None) -> None:
        """Отключить номер

        Отключает номер от Wazzapo: сообщения с него больше не отправляются и не приходят.

        Переписка в кабинете сохраняется. Тестовый ключ номер не отключает.
        Ошибка: 404 NOT_FOUND, если номера нет в этом аккаунте.

        DELETE /api/v2/external/phone-numbers/{phone_number_id}

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        self._client._request("DELETE", f"/phone-numbers/{_quote(phone_number_id)}", timeout=timeout)
        return None

    def get(self, phone_number_id: str, *, timeout: Optional[float] = None) -> PhoneNumberOut:
        """Номер

        Возвращает один номер: статус подключения, имя компании, оценку качества Meta.

        Проверяйте status=connected перед рассылкой. Ошибка: 404 NOT_FOUND, если номера
        нет в этом аккаунте.

        GET /api/v2/external/phone-numbers/{phone_number_id}

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "PhoneNumberOut",
            self._client._request(
                "GET",
                f"/phone-numbers/{_quote(phone_number_id)}",
                timeout=timeout,
            ),
        )

    def get_business_profile(
        self,
        phone_number_id: str,
        *,
        timeout: Optional[float] = None,
    ) -> BusinessProfileOut:
        """Профиль компании

        Возвращает профиль компании в WhatsApp: описание, адрес, почту, сайты, фото.

        Клиенты видят его, открыв карточку номера. Только для номеров WhatsApp Cloud API.
        Ошибки: 404 NOT_FOUND, 501 not_supported.

        GET /api/v2/external/phone-numbers/{phone_number_id}/business-profile

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "BusinessProfileOut",
            self._client._request(
                "GET",
                f"/phone-numbers/{_quote(phone_number_id)}/business-profile",
                timeout=timeout,
            ),
        )

    def list(self, *, timeout: Optional[float] = None) -> PhoneNumberListOut:
        """Список номеров

        Возвращает номера WhatsApp, подключённые к аккаунту ключа.

        С этого метода начинают: phone_number_id из ответа нужен для отправки сообщений,
        загрузки файлов и шаблонов. Номер подключают в кабинете Wazzapo
        или методом POST /phone-numbers. Отключённые номера в списке не показываются.

        GET /api/v2/external/phone-numbers

        Аргументы:
            timeout: таймаут этого запроса в секундах
        """
        return cast("PhoneNumberListOut", self._client._request("GET", "/phone-numbers", timeout=timeout))

    def update_business_profile(
        self,
        phone_number_id: str,
        *,
        body: BusinessProfileIn,
        timeout: Optional[float] = None,
    ) -> BusinessProfileUpdateOut:
        """Изменить профиль компании

        Меняет профиль компании в WhatsApp. Передайте только поля, которые меняете.

        Фото профиля этим методом не меняется. Тестовый ключ ничего не меняет.
        Ошибки: 404 NOT_FOUND, 422 invalid_parameters (Meta не приняла значение, например
        неизвестная отрасль vertical), 501 not_supported.

        PATCH /api/v2/external/phone-numbers/{phone_number_id}/business-profile

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            body: тело запроса, словарь BusinessProfileIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "BusinessProfileUpdateOut",
            self._client._request(
                "PATCH",
                f"/phone-numbers/{_quote(phone_number_id)}/business-profile",
                json=body,
                timeout=timeout,
            ),
        )



class AsyncPhoneNumbers:
    """Методы phone_numbers: create, delete, get, get_business_profile, list, update_business_profile."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def create(
        self,
        *,
        body: RegisterPhoneNumberIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> RegisterPhoneNumberOut:
        """Подключить номер

        Начинает подключение нового номера WhatsApp.

        В ответе может быть embedded_signup_url: откройте его во всплывающем окне, владелец
        номера войдёт в Facebook и подтвердит номер в Meta. Пока подключение не завершено,
        status=pending. Номер расходует лимит устройств тарифа.
        Ошибки: 402 DEVICE_QUOTA_EXCEEDED (лимит номеров), 503 SERVICE_UNAVAILABLE
        (подключение через API недоступно, подключите номер в кабинете).

        POST /api/v2/external/phone-numbers

        Аргументы:
            body: тело запроса, словарь RegisterPhoneNumberIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "RegisterPhoneNumberOut",
            await self._client._request(
                "POST",
                "/phone-numbers",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def delete(self, phone_number_id: str, *, timeout: Optional[float] = None) -> None:
        """Отключить номер

        Отключает номер от Wazzapo: сообщения с него больше не отправляются и не приходят.

        Переписка в кабинете сохраняется. Тестовый ключ номер не отключает.
        Ошибка: 404 NOT_FOUND, если номера нет в этом аккаунте.

        DELETE /api/v2/external/phone-numbers/{phone_number_id}

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        await self._client._request("DELETE", f"/phone-numbers/{_quote(phone_number_id)}", timeout=timeout)
        return None

    async def get(self, phone_number_id: str, *, timeout: Optional[float] = None) -> PhoneNumberOut:
        """Номер

        Возвращает один номер: статус подключения, имя компании, оценку качества Meta.

        Проверяйте status=connected перед рассылкой. Ошибка: 404 NOT_FOUND, если номера
        нет в этом аккаунте.

        GET /api/v2/external/phone-numbers/{phone_number_id}

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "PhoneNumberOut",
            await self._client._request(
                "GET",
                f"/phone-numbers/{_quote(phone_number_id)}",
                timeout=timeout,
            ),
        )

    async def get_business_profile(
        self,
        phone_number_id: str,
        *,
        timeout: Optional[float] = None,
    ) -> BusinessProfileOut:
        """Профиль компании

        Возвращает профиль компании в WhatsApp: описание, адрес, почту, сайты, фото.

        Клиенты видят его, открыв карточку номера. Только для номеров WhatsApp Cloud API.
        Ошибки: 404 NOT_FOUND, 501 not_supported.

        GET /api/v2/external/phone-numbers/{phone_number_id}/business-profile

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "BusinessProfileOut",
            await self._client._request(
                "GET",
                f"/phone-numbers/{_quote(phone_number_id)}/business-profile",
                timeout=timeout,
            ),
        )

    async def list(self, *, timeout: Optional[float] = None) -> PhoneNumberListOut:
        """Список номеров

        Возвращает номера WhatsApp, подключённые к аккаунту ключа.

        С этого метода начинают: phone_number_id из ответа нужен для отправки сообщений,
        загрузки файлов и шаблонов. Номер подключают в кабинете Wazzapo
        или методом POST /phone-numbers. Отключённые номера в списке не показываются.

        GET /api/v2/external/phone-numbers

        Аргументы:
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "PhoneNumberListOut",
            await self._client._request(
                "GET",
                "/phone-numbers",
                timeout=timeout,
            ),
        )

    async def update_business_profile(
        self,
        phone_number_id: str,
        *,
        body: BusinessProfileIn,
        timeout: Optional[float] = None,
    ) -> BusinessProfileUpdateOut:
        """Изменить профиль компании

        Меняет профиль компании в WhatsApp. Передайте только поля, которые меняете.

        Фото профиля этим методом не меняется. Тестовый ключ ничего не меняет.
        Ошибки: 404 NOT_FOUND, 422 invalid_parameters (Meta не приняла значение, например
        неизвестная отрасль vertical), 501 not_supported.

        PATCH /api/v2/external/phone-numbers/{phone_number_id}/business-profile

        Аргументы:
            phone_number_id: id номера: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
            body: тело запроса, словарь BusinessProfileIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "BusinessProfileUpdateOut",
            await self._client._request(
                "PATCH",
                f"/phone-numbers/{_quote(phone_number_id)}/business-profile",
                json=body,
                timeout=timeout,
            ),
        )



class Pipelines:
    """Методы pipelines: list."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> PipelineListOut:
        """Список воронок

        Воронки аккаунта с этапами по порядку и своими полями сделки.

        С этого метода начинают работу со сделками: отсюда берут pipeline_id (data[].id),
        stage_id (stages[].id) и id своих полей для custom_fields (custom_fields[].id, тип и
        варианты options). Поле с is_amount=true хранит сумму сделки amount.
        Ключ сотрудника видит только доступные ему воронки. Право ключа deals:read, без него 403.
        Воронки меняются редко: можно кешировать на час и перечитывать при 422 stage_not_found.

        GET /api/v2/external/pipelines

        Аргументы:
            limit: Сколько воронок на странице, от 1 до 200, по умолчанию 50
            cursor: next_cursor из прошлого ответа; для первой страницы не передавайте
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "PipelineListOut",
            self._client._request(
                "GET",
                "/pipelines",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[PipelineOut]:
        """Список воронок: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сколько воронок на странице, от 1 до 200, по умолчанию 50
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate("/pipelines", params={"limit": limit}, timeout=timeout)



class AsyncPipelines:
    """Методы pipelines: list."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> PipelineListOut:
        """Список воронок

        Воронки аккаунта с этапами по порядку и своими полями сделки.

        С этого метода начинают работу со сделками: отсюда берут pipeline_id (data[].id),
        stage_id (stages[].id) и id своих полей для custom_fields (custom_fields[].id, тип и
        варианты options). Поле с is_amount=true хранит сумму сделки amount.
        Ключ сотрудника видит только доступные ему воронки. Право ключа deals:read, без него 403.
        Воронки меняются редко: можно кешировать на час и перечитывать при 422 stage_not_found.

        GET /api/v2/external/pipelines

        Аргументы:
            limit: Сколько воронок на странице, от 1 до 200, по умолчанию 50
            cursor: next_cursor из прошлого ответа; для первой страницы не передавайте
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "PipelineListOut",
            await self._client._request(
                "GET",
                "/pipelines",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[PipelineOut]:
        """Список воронок: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сколько воронок на странице, от 1 до 200, по умолчанию 50
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate("/pipelines", params={"limit": limit}, timeout=timeout)



class Tasks:
    """Методы tasks: create, list, update."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def create(
        self,
        deal_id: str,
        *,
        body: TaskCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TaskOut:
        """Поставить задачу по сделке

        Ставит задачу по сделке: перезвонить, встретиться, отправить смету.

        due_at в ISO 8601: Казахстан живёт по UTC+5, «завтра в 10:00 по Астане» это 05:00Z
        (2026-10-19T05:00:00Z) или 2026-10-19T10:00:00+05:00. Исполнитель по умолчанию
        ответственный сделки, другой: id из GET /team. Исполнитель получит уведомление и
        напоминание, уходит вебхук task.created. Повтор с тем же Idempotency-Key задачу не дублирует.
        Право tasks:write. Ошибки: 404 deal_not_found, 422 responsible_user_not_found.

        POST /api/v2/external/deals/{deal_id}/tasks

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            body: тело запроса, словарь TaskCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TaskOut",
            self._client._request(
                "POST",
                f"/deals/{_quote(deal_id)}/tasks",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def list(
        self,
        deal_id: str,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TaskListOut:
        """Задачи сделки

        Задачи сделки по сроку, ближайшие первыми, вместе с выполненными (done=true).

        Срок due_at в UTC с Z: 05:00Z это 10:00 по Астане. Ключ сотрудника без права видеть чужие
        задачи получит только свои. Право tasks:read. Нет сделки: 404 deal_not_found.

        GET /api/v2/external/deals/{deal_id}/tasks

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            limit: Сколько задач на странице, от 1 до 200, по умолчанию 50
            cursor: next_cursor из прошлого ответа; для первой страницы не передавайте
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TaskListOut",
            self._client._request(
                "GET",
                f"/deals/{_quote(deal_id)}/tasks",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        deal_id: str,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[TaskOut]:
        """Задачи сделки: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            limit: Сколько задач на странице, от 1 до 200, по умолчанию 50
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate(
            f"/deals/{_quote(deal_id)}/tasks",
            params={"limit": limit},
            timeout=timeout,
        )

    def update(self, task_id: str, *, body: TaskUpdateIn, timeout: Optional[float] = None) -> TaskOut:
        """Изменить задачу

        Меняет название, срок или исполнителя задачи, отмечает её выполненной.

        Меняются только переданные поля. done=true отмечает выполненной, как кнопка «Выполнено»
        в кабинете, done=false возвращает в работу. id задачи из GET /deals/{deal_id}/tasks.
        Право tasks:write. Ошибки: 404 task_not_found, 422 responsible_user_not_found.

        PATCH /api/v2/external/tasks/{task_id}

        Аргументы:
            task_id: id задачи: поле id из GET /deals/{deal_id}/tasks или из ответа POST /deals/{deal_id}/tasks
            body: тело запроса, словарь TaskUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TaskOut",
            self._client._request(
                "PATCH",
                f"/tasks/{_quote(task_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class AsyncTasks:
    """Методы tasks: create, list, update."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def create(
        self,
        deal_id: str,
        *,
        body: TaskCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TaskOut:
        """Поставить задачу по сделке

        Ставит задачу по сделке: перезвонить, встретиться, отправить смету.

        due_at в ISO 8601: Казахстан живёт по UTC+5, «завтра в 10:00 по Астане» это 05:00Z
        (2026-10-19T05:00:00Z) или 2026-10-19T10:00:00+05:00. Исполнитель по умолчанию
        ответственный сделки, другой: id из GET /team. Исполнитель получит уведомление и
        напоминание, уходит вебхук task.created. Повтор с тем же Idempotency-Key задачу не дублирует.
        Право tasks:write. Ошибки: 404 deal_not_found, 422 responsible_user_not_found.

        POST /api/v2/external/deals/{deal_id}/tasks

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            body: тело запроса, словарь TaskCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TaskOut",
            await self._client._request(
                "POST",
                f"/deals/{_quote(deal_id)}/tasks",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def list(
        self,
        deal_id: str,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TaskListOut:
        """Задачи сделки

        Задачи сделки по сроку, ближайшие первыми, вместе с выполненными (done=true).

        Срок due_at в UTC с Z: 05:00Z это 10:00 по Астане. Ключ сотрудника без права видеть чужие
        задачи получит только свои. Право tasks:read. Нет сделки: 404 deal_not_found.

        GET /api/v2/external/deals/{deal_id}/tasks

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            limit: Сколько задач на странице, от 1 до 200, по умолчанию 50
            cursor: next_cursor из прошлого ответа; для первой страницы не передавайте
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TaskListOut",
            await self._client._request(
                "GET",
                f"/deals/{_quote(deal_id)}/tasks",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        deal_id: str,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[TaskOut]:
        """Задачи сделки: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            deal_id: id сделки: поле id из GET /deals или из ответа POST /deals, например 6713b1d5f2c3d4e5f6071829
            limit: Сколько задач на странице, от 1 до 200, по умолчанию 50
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate(
            f"/deals/{_quote(deal_id)}/tasks",
            params={"limit": limit},
            timeout=timeout,
        )

    async def update(self, task_id: str, *, body: TaskUpdateIn, timeout: Optional[float] = None) -> TaskOut:
        """Изменить задачу

        Меняет название, срок или исполнителя задачи, отмечает её выполненной.

        Меняются только переданные поля. done=true отмечает выполненной, как кнопка «Выполнено»
        в кабинете, done=false возвращает в работу. id задачи из GET /deals/{deal_id}/tasks.
        Право tasks:write. Ошибки: 404 task_not_found, 422 responsible_user_not_found.

        PATCH /api/v2/external/tasks/{task_id}

        Аргументы:
            task_id: id задачи: поле id из GET /deals/{deal_id}/tasks или из ответа POST /deals/{deal_id}/tasks
            body: тело запроса, словарь TaskUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TaskOut",
            await self._client._request(
                "PATCH",
                f"/tasks/{_quote(task_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class Team:
    """Методы team: list."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TeamListOut:
        """Сотрудники

        Владелец аккаунта и сотрудники команды: отсюда берут `id` для назначения ответственного (`user_id` в POST /conversations/{conversation_id}/assign) и для упоминаний в заметках (`mention_user_ids`). Первым в списке идёт владелец.

        Отключённые сотрудники тоже в списке (`is_active: false`): по ним видно прежних ответственных, но назначить на них нельзя. `phone_number_ids: null` значит, что сотрудник работает во всех номерах. Почты и телефонов сотрудников в ответе нет. Право ключа: `team:read`.

        GET /api/v2/external/team

        Аргументы:
            limit: Сотрудников на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TeamListOut",
            self._client._request(
                "GET",
                "/team",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[TeamMemberOut]:
        """Сотрудники: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сотрудников на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate("/team", params={"limit": limit}, timeout=timeout)



class AsyncTeam:
    """Методы team: list."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TeamListOut:
        """Сотрудники

        Владелец аккаунта и сотрудники команды: отсюда берут `id` для назначения ответственного (`user_id` в POST /conversations/{conversation_id}/assign) и для упоминаний в заметках (`mention_user_ids`). Первым в списке идёт владелец.

        Отключённые сотрудники тоже в списке (`is_active: false`): по ним видно прежних ответственных, но назначить на них нельзя. `phone_number_ids: null` значит, что сотрудник работает во всех номерах. Почты и телефонов сотрудников в ответе нет. Право ключа: `team:read`.

        GET /api/v2/external/team

        Аргументы:
            limit: Сотрудников на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TeamListOut",
            await self._client._request(
                "GET",
                "/team",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[TeamMemberOut]:
        """Сотрудники: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сотрудников на странице, от 1 до 200
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate("/team", params={"limit": limit}, timeout=timeout)



class Templates:
    """Методы templates: create, delete, get, get_status, list, update."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def create(
        self,
        *,
        body: CreateTemplateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TemplateOut:
        """Отправить шаблон на проверку

        Создаёт шаблон и отправляет его на проверку Meta. Первое сообщение клиенту и сообщение после 24 часов
        тишины можно отправить только одобренным шаблоном.

        До вызова: возьмите phone_number_id из GET /phone-numbers. Ответ приходит со status=PENDING; итог проверки
        узнайте через GET /templates/{template_id} или событие вебхука template.status_updated.
        Картинку, видео или PDF в шапке передайте ссылкой в example.media_url: Wazzapo сам загрузит образец в Meta.
        Ошибки: 422 VALIDATION_ERROR (нет обязательного поля), 422 media_unavailable (образец файла не скачался),
        422 invalid_parameters (Meta не приняла шаблон, например имя уже занято), 404 номер не найден.
        Повтор с тем же Idempotency-Key не создаёт второй шаблон.

        POST /api/v2/external/templates

        Аргументы:
            body: тело запроса, словарь CreateTemplateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            self._client._request(
                "POST",
                "/templates",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def delete(self, template_id: str, *, timeout: Optional[float] = None) -> None:
        """Удалить шаблон

        Удаляет шаблон в Meta (только этот язык) и в Wazzapo. Отменить нельзя.

        Имя удалённого одобренного шаблона Meta не даёт занять снова 30 дней; отключённый (DISABLED) шаблон
        Meta не удаляет. Ошибки: 404 шаблон не найден. Тестовый ключ ничего не удаляет.

        DELETE /api/v2/external/templates/{template_id}

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            timeout: таймаут этого запроса в секундах
        """
        self._client._request("DELETE", f"/templates/{_quote(template_id)}", timeout=timeout)
        return None

    def get(self, template_id: str, *, timeout: Optional[float] = None) -> TemplateOut:
        """Шаблон целиком

        Шаблон со всеми частями (components), числом переменных и кнопками; статус свежий из Meta.

        Используйте перед отправкой, чтобы знать, сколько значений и какой файл шапки передать.
        Шаблоны, созданные в WhatsApp Manager, появляются здесь после синхронизации в кабинете Wazzapo,
        до неё ищите их в GET /templates. Ошибки: 404 NOT_FOUND, шаблона с таким id нет в этом
        аккаунте. Это 404, потому что не найден сам адрес-объект; при отправке неизвестного шаблона
        POST /messages/send отвечает 422 template_not_found (не подошло значение в теле запроса).

        GET /api/v2/external/templates/{template_id}

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            self._client._request(
                "GET",
                f"/templates/{_quote(template_id)}",
                timeout=timeout,
            ),
        )

    def get_status(self, template_id: str, *, timeout: Optional[float] = None) -> TemplateOut:
        """Статус шаблона

        Свежий статус проверки шаблона в Meta: PENDING, APPROVED, REJECTED, PAUSED или DISABLED.

        Короткий вариант для опроса статуса: смотрите в ответе status и rejected_reason. Полное
        содержимое шаблона (части, переменные, кнопки) берите из GET /templates/{template_id}.
        Опрашивайте после создания или правки, пока статус PENDING (раз в минуту достаточно), или подпишитесь
        на событие template.status_updated. При REJECTED причина в rejected_reason.
        Ошибки: 404 NOT_FOUND, шаблона с таким id нет в этом аккаунте (при отправке неизвестного
        шаблона POST /messages/send отвечает 422 template_not_found).

        GET /api/v2/external/templates/{template_id}/status

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            self._client._request(
                "GET",
                f"/templates/{_quote(template_id)}/status",
                timeout=timeout,
            ),
        )

    def list(
        self,
        *,
        phone_number_id: str,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        name: Optional[str] = None,
        language: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TemplateListOut:
        """Список шаблонов

        Все шаблоны номера прямо из Meta, со статусом и содержимым (components).

        Нужен, чтобы выбрать шаблон для messages.send: передайте его name и language, а значений переменных
        столько, сколько variables_count. Фильтры status, category, name, language можно сочетать.
        Страницы курсором: next_cursor передайте в cursor. Ошибки: 404 номер не найден, 403 account_restricted.

        GET /api/v2/external/templates

        Аргументы:
            phone_number_id: id номера из GET /api/v2/external/phone-numbers, например 123456789012345
            limit: Сколько шаблонов на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа
            status: Только с этим статусом: PENDING, APPROVED, REJECTED, PAUSED, DISABLED
            category: Только этой категории: MARKETING, UTILITY, AUTHENTICATION
            name: Часть имени без учёта регистра, например zapis
            language: Только этого языка, например ru или kk
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateListOut",
            self._client._request(
                "GET",
                "/templates",
                params={"phone_number_id": phone_number_id, "limit": limit, "cursor": cursor, "status": status, "category": category, "name": name, "language": language},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        phone_number_id: str,
        limit: Optional[int] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        name: Optional[str] = None,
        language: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[TemplateOut]:
        """Список шаблонов: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            phone_number_id: id номера из GET /api/v2/external/phone-numbers, например 123456789012345
            limit: Сколько шаблонов на странице, от 1 до 200
            status: Только с этим статусом: PENDING, APPROVED, REJECTED, PAUSED, DISABLED
            category: Только этой категории: MARKETING, UTILITY, AUTHENTICATION
            name: Часть имени без учёта регистра, например zapis
            language: Только этого языка, например ru или kk
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate(
            "/templates",
            params={"phone_number_id": phone_number_id, "limit": limit, "status": status, "category": category, "name": name, "language": language},
            timeout=timeout,
        )

    def update(
        self,
        template_id: str,
        *,
        body: UpdateTemplateIn,
        timeout: Optional[float] = None,
    ) -> TemplateOut:
        """Изменить шаблон

        Меняет части шаблона или категорию в Meta, после чего Meta проверяет шаблон заново (status=PENDING).

        Правила Meta: править можно шаблон в статусе APPROVED, REJECTED или PAUSED; имя и язык не меняются;
        components заменяются целиком; категорию одобренного шаблона сменить нельзя. Одобренный шаблон можно
        править 1 раз в сутки и не больше 10 раз за 30 дней, отклонённый без ограничений.
        Ошибки: 404 шаблон не найден, 409 CONFLICT (статус не даёт править), 422 VALIDATION_ERROR,
        422 invalid_parameters (Meta отказала, например исчерпан лимит правок). Тестовый ключ ничего не меняет.

        PATCH /api/v2/external/templates/{template_id}

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            body: тело запроса, словарь UpdateTemplateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            self._client._request(
                "PATCH",
                f"/templates/{_quote(template_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class AsyncTemplates:
    """Методы templates: create, delete, get, get_status, list, update."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def create(
        self,
        *,
        body: CreateTemplateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TemplateOut:
        """Отправить шаблон на проверку

        Создаёт шаблон и отправляет его на проверку Meta. Первое сообщение клиенту и сообщение после 24 часов
        тишины можно отправить только одобренным шаблоном.

        До вызова: возьмите phone_number_id из GET /phone-numbers. Ответ приходит со status=PENDING; итог проверки
        узнайте через GET /templates/{template_id} или событие вебхука template.status_updated.
        Картинку, видео или PDF в шапке передайте ссылкой в example.media_url: Wazzapo сам загрузит образец в Meta.
        Ошибки: 422 VALIDATION_ERROR (нет обязательного поля), 422 media_unavailable (образец файла не скачался),
        422 invalid_parameters (Meta не приняла шаблон, например имя уже занято), 404 номер не найден.
        Повтор с тем же Idempotency-Key не создаёт второй шаблон.

        POST /api/v2/external/templates

        Аргументы:
            body: тело запроса, словарь CreateTemplateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            await self._client._request(
                "POST",
                "/templates",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def delete(self, template_id: str, *, timeout: Optional[float] = None) -> None:
        """Удалить шаблон

        Удаляет шаблон в Meta (только этот язык) и в Wazzapo. Отменить нельзя.

        Имя удалённого одобренного шаблона Meta не даёт занять снова 30 дней; отключённый (DISABLED) шаблон
        Meta не удаляет. Ошибки: 404 шаблон не найден. Тестовый ключ ничего не удаляет.

        DELETE /api/v2/external/templates/{template_id}

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            timeout: таймаут этого запроса в секундах
        """
        await self._client._request("DELETE", f"/templates/{_quote(template_id)}", timeout=timeout)
        return None

    async def get(self, template_id: str, *, timeout: Optional[float] = None) -> TemplateOut:
        """Шаблон целиком

        Шаблон со всеми частями (components), числом переменных и кнопками; статус свежий из Meta.

        Используйте перед отправкой, чтобы знать, сколько значений и какой файл шапки передать.
        Шаблоны, созданные в WhatsApp Manager, появляются здесь после синхронизации в кабинете Wazzapo,
        до неё ищите их в GET /templates. Ошибки: 404 NOT_FOUND, шаблона с таким id нет в этом
        аккаунте. Это 404, потому что не найден сам адрес-объект; при отправке неизвестного шаблона
        POST /messages/send отвечает 422 template_not_found (не подошло значение в теле запроса).

        GET /api/v2/external/templates/{template_id}

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            await self._client._request(
                "GET",
                f"/templates/{_quote(template_id)}",
                timeout=timeout,
            ),
        )

    async def get_status(self, template_id: str, *, timeout: Optional[float] = None) -> TemplateOut:
        """Статус шаблона

        Свежий статус проверки шаблона в Meta: PENDING, APPROVED, REJECTED, PAUSED или DISABLED.

        Короткий вариант для опроса статуса: смотрите в ответе status и rejected_reason. Полное
        содержимое шаблона (части, переменные, кнопки) берите из GET /templates/{template_id}.
        Опрашивайте после создания или правки, пока статус PENDING (раз в минуту достаточно), или подпишитесь
        на событие template.status_updated. При REJECTED причина в rejected_reason.
        Ошибки: 404 NOT_FOUND, шаблона с таким id нет в этом аккаунте (при отправке неизвестного
        шаблона POST /messages/send отвечает 422 template_not_found).

        GET /api/v2/external/templates/{template_id}/status

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            await self._client._request(
                "GET",
                f"/templates/{_quote(template_id)}/status",
                timeout=timeout,
            ),
        )

    async def list(
        self,
        *,
        phone_number_id: str,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        name: Optional[str] = None,
        language: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> TemplateListOut:
        """Список шаблонов

        Все шаблоны номера прямо из Meta, со статусом и содержимым (components).

        Нужен, чтобы выбрать шаблон для messages.send: передайте его name и language, а значений переменных
        столько, сколько variables_count. Фильтры status, category, name, language можно сочетать.
        Страницы курсором: next_cursor передайте в cursor. Ошибки: 404 номер не найден, 403 account_restricted.

        GET /api/v2/external/templates

        Аргументы:
            phone_number_id: id номера из GET /api/v2/external/phone-numbers, например 123456789012345
            limit: Сколько шаблонов на странице, от 1 до 200
            cursor: next_cursor из прошлого ответа
            status: Только с этим статусом: PENDING, APPROVED, REJECTED, PAUSED, DISABLED
            category: Только этой категории: MARKETING, UTILITY, AUTHENTICATION
            name: Часть имени без учёта регистра, например zapis
            language: Только этого языка, например ru или kk
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateListOut",
            await self._client._request(
                "GET",
                "/templates",
                params={"phone_number_id": phone_number_id, "limit": limit, "cursor": cursor, "status": status, "category": category, "name": name, "language": language},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        phone_number_id: str,
        limit: Optional[int] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        name: Optional[str] = None,
        language: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[TemplateOut]:
        """Список шаблонов: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            phone_number_id: id номера из GET /api/v2/external/phone-numbers, например 123456789012345
            limit: Сколько шаблонов на странице, от 1 до 200
            status: Только с этим статусом: PENDING, APPROVED, REJECTED, PAUSED, DISABLED
            category: Только этой категории: MARKETING, UTILITY, AUTHENTICATION
            name: Часть имени без учёта регистра, например zapis
            language: Только этого языка, например ru или kk
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate(
            "/templates",
            params={"phone_number_id": phone_number_id, "limit": limit, "status": status, "category": category, "name": name, "language": language},
            timeout=timeout,
        )

    async def update(
        self,
        template_id: str,
        *,
        body: UpdateTemplateIn,
        timeout: Optional[float] = None,
    ) -> TemplateOut:
        """Изменить шаблон

        Меняет части шаблона или категорию в Meta, после чего Meta проверяет шаблон заново (status=PENDING).

        Правила Meta: править можно шаблон в статусе APPROVED, REJECTED или PAUSED; имя и язык не меняются;
        components заменяются целиком; категорию одобренного шаблона сменить нельзя. Одобренный шаблон можно
        править 1 раз в сутки и не больше 10 раз за 30 дней, отклонённый без ограничений.
        Ошибки: 404 шаблон не найден, 409 CONFLICT (статус не даёт править), 422 VALIDATION_ERROR,
        422 invalid_parameters (Meta отказала, например исчерпан лимит правок). Тестовый ключ ничего не меняет.

        PATCH /api/v2/external/templates/{template_id}

        Аргументы:
            template_id: id шаблона в Meta: template_id из POST или GET /api/v2/external/templates, например 1252715608684590
            body: тело запроса, словарь UpdateTemplateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "TemplateOut",
            await self._client._request(
                "PATCH",
                f"/templates/{_quote(template_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class WebhookEventTypes:
    """Методы webhook_event_types: list."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookEventTypeListOut:
        """Каталог событий

        Все события, на которые можно подписаться: имя для event_types, описание и пример поля data.

        Тело запроса на ваш адрес: {"event": "deal.created", "timestamp": "...", "data": {...}};
        заголовок X-Wazzapo-Event дублирует имя события. Новые события добавляются без смены версии API.
        Схема каждого поля data, примеры нажатий кнопок и подпись запроса: раздел webhooks в
        /api/v2/external/openapi.json и описание POST /webhooks.

        GET /api/v2/external/webhook-event-types

        Аргументы:
            limit: Сколько записей на странице
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookEventTypeListOut",
            self._client._request(
                "GET",
                "/webhook-event-types",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[WebhookEventTypeOut]:
        """Каталог событий: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сколько записей на странице
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate("/webhook-event-types", params={"limit": limit}, timeout=timeout)



class AsyncWebhookEventTypes:
    """Методы webhook_event_types: list."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookEventTypeListOut:
        """Каталог событий

        Все события, на которые можно подписаться: имя для event_types, описание и пример поля data.

        Тело запроса на ваш адрес: {"event": "deal.created", "timestamp": "...", "data": {...}};
        заголовок X-Wazzapo-Event дублирует имя события. Новые события добавляются без смены версии API.
        Схема каждого поля data, примеры нажатий кнопок и подпись запроса: раздел webhooks в
        /api/v2/external/openapi.json и описание POST /webhooks.

        GET /api/v2/external/webhook-event-types

        Аргументы:
            limit: Сколько записей на странице
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookEventTypeListOut",
            await self._client._request(
                "GET",
                "/webhook-event-types",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[WebhookEventTypeOut]:
        """Каталог событий: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сколько записей на странице
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate("/webhook-event-types", params={"limit": limit}, timeout=timeout)



class Webhooks:
    """Методы webhooks: create, delete, get, list, list_deliveries, retry_delivery, rotate_secret, test, update."""

    def __init__(self, client: "Wazzapo") -> None:
        self._client = client

    def create(
        self,
        *,
        body: WebhookCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookWithSecretOut:
        """Подписаться на события

        Подписывает ваш адрес https на события: Wazzapo шлёт на него POST с JSON.

        Ответ содержит `secret`: он показывается один раз, сохраните его. Ключ `wz_test_…` вебхук не создаёт, но отдаёт ответ того же вида.

        Ошибки: 422 `invalid_event_types` (список: GET /webhook-event-types), 422 адрес не https или внутренний, 403 `USAGE_LIMIT_EXCEEDED` (лимит вебхуков тарифа).

        **Тело**: `{"event": "<имя>", "timestamp": "<когда создана доставка, ISO 8601 UTC>", "data": {...}}`. `timestamp` одинаков во всех повторах; время самого события внутри `data`. Поля `data` у каждого события описаны в разделе Webhooks описания API (openapi.json, ключ `webhooks`).

        **Единицы сумм** (пример: 150 000 ₸)

        | Где | Поле | Единица | 150 000 ₸ |
        |---|---|---|---|
        | Шаблон, переменная type=currency (messages.send) | `currency.amount_1000` | тенге × 1000 | `150000000` |
        | Сделка в REST (GET/POST/PATCH /deals) | `amount` | тиыны, тенге × 100 | `15000000` |
        | Сделка в вебхуках deal.* | `data.deal.amount` | тиыны, тенге × 100, как в REST | `15000000` |
        | Сделка в вебхуках deal.* | `data.deal.value` | целые тенге, оставлено для совместимости | `150000` |
        | Счёт в вебхуке invoice.status_changed | `data.invoice.amount` | тиыны, тенге × 100 | `15000000` |

        ## Заголовки запроса

        | Заголовок | Что в нём |
        |---|---|
        | `X-Wazzapo-Timestamp` | Время отправки этой попытки: Unix-время в секундах, целое число, UTC, например `1760000000`. В каждой попытке новое |
        | `X-Wazzapo-Signature-V2` | `v2=` и 64 символа hex строчными буквами: HMAC-SHA256 от `{X-Wazzapo-Timestamp}.{тело}`. Проверяйте этот заголовок |
        | `X-Wazzapo-Signature` | Старая подпись без времени: `sha256=` и hex строчными, HMAC-SHA256 от тела. Оставлена для совместимости, не защищает от повтора перехваченного запроса |
        | `X-Wazzapo-Delivery-Id` | id доставки, одинаковый во всех повторах: по нему отсеивайте дубли. Его же принимает POST /webhooks/{webhook_id}/deliveries/{delivery_id}/retry |
        | `X-Wazzapo-Event` | Имя события, то же, что поле `event` тела |
        | `X-Wazzapo-Attempt` | Номер попытки: 1 у первой, до 6 |
        | `Content-Type` | `application/json`; `User-Agent: Wazzapo-Webhooks/1.0` |

        У тестового события (POST /webhooks/{webhook_id}/test, event=test) нет `X-Wazzapo-Delivery-Id` и `X-Wazzapo-Attempt`.

        **Как проверить подпись**

        1. Возьмите тело запроса сырыми байтами, как пришло, до разбора JSON. Не собирайте JSON заново: порядок полей, отсутствие пробелов и кириллица в UTF-8 (без `\\u`-экранирования) должны совпасть байт в байт.
        2. Строка для подписи: значение `X-Wazzapo-Timestamp`, точка, тело: `{timestamp}.{body}`.
        3. Ключ HMAC: секрет вебхука целиком, вместе с `whsec_`, в UTF-8 (из ответа POST /webhooks или rotate-secret).
        4. Ожидаемое значение: `v2=` + HMAC-SHA256(ключ, строка) в hex строчными буквами.
        5. Сравните с `X-Wazzapo-Signature-V2` сравнением за постоянное время (`hash_equals`, `crypto.timingSafeEqual`, `hmac.compare_digest`). Не совпало: ответьте 401.
        6. Отклоните запрос, если `X-Wazzapo-Timestamp` отличается от вашего времени больше чем на 300 секунд.

        **Пример с готовыми значениями**: секрет `whsec_test`, `X-Wazzapo-Timestamp: 1760000000`, тело `{"event":"message.incoming"}` (28 байт). Строка для подписи `1760000000.{"event":"message.incoming"}`, `X-Wazzapo-Signature-V2: v2=a7e2dad2ec4a0f54d4f46ea51f2c28803b66f4effebb959c6ff8e8cc59f47fca`, старая `X-Wazzapo-Signature: sha256=b8745e4a15618d503f14d3e7fb12aa3c5cf3064a4bbc50b5f515eae87ee76cd7`.

        **PHP**

        ```php
        $body = file_get_contents('php://input');           // сырое тело
        $ts   = $_SERVER['HTTP_X_WAZZAPO_TIMESTAMP'] ?? '';
        $sig  = $_SERVER['HTTP_X_WAZZAPO_SIGNATURE_V2'] ?? '';
        $expected = 'v2=' . hash_hmac('sha256', $ts . '.' . $body, $secret);
        if (!hash_equals($expected, $sig) || abs(time() - (int)$ts) > 300) { http_response_code(401); exit; }
        $event = json_decode($body, true);
        http_response_code(200);
        ```

        **Node.js (Express)**

        ```js
        app.post('/hooks/wazzapo', express.raw({ type: 'application/json' }), (req, res) => {
          const ts = req.get('X-Wazzapo-Timestamp') || '';
          const sig = req.get('X-Wazzapo-Signature-V2') || '';
          const expected = 'v2=' + crypto.createHmac('sha256', SECRET)
            .update(ts + '.').update(req.body).digest('hex');   // req.body: Buffer
          const ok = sig.length === expected.length &&
            crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected));
          if (!ok || Math.abs(Date.now() / 1000 - Number(ts)) > 300) return res.sendStatus(401);
          res.sendStatus(200);                                 // ответ сразу, обработка потом
          const event = JSON.parse(req.body.toString('utf8'));
        });
        ```

        **Ответ и повторы.** Ответьте любым 2xx за 10 секунд; тело ответа не важно. Иначе повторы через 1 мин, 5 мин, 30 мин, 2 ч и 6 ч (±20%), всего 6 попыток, с тем же телом и `X-Wazzapo-Delivery-Id`. Доставка «хотя бы один раз»: дубли возможны, отсеивайте их по `X-Wazzapo-Delivery-Id`. Порядок событий не гарантирован: сверяйте поле `timestamp`. После 10 доставок подряд, не дошедших за все попытки, вебхук выключается (`is_active=false`), включить снова: PATCH с `is_active=true`.

        POST /api/v2/external/webhooks

        Аргументы:
            body: тело запроса, словарь WebhookCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookWithSecretOut",
            self._client._request(
                "POST",
                "/webhooks",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def delete(self, webhook_id: str, *, timeout: Optional[float] = None) -> None:
        """Удалить вебхук

        Удаляет вебхук вместе с историей доставок: события на адрес больше не приходят.

        Чтобы остановить на время, лучше выключите: PATCH с is_active=false. Ответ 204 без тела.
        Ошибки: 404 webhook_not_found.

        DELETE /api/v2/external/webhooks/{webhook_id}

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            timeout: таймаут этого запроса в секундах
        """
        self._client._request("DELETE", f"/webhooks/{_quote(webhook_id)}", timeout=timeout)
        return None

    def get(self, webhook_id: str, *, timeout: Optional[float] = None) -> WebhookOut:
        """Вебхук

        Один вебхук: адрес, события, включён ли и сколько доставок подряд не дошли. Без секрета.

        Ошибки: 404 webhook_not_found.

        GET /api/v2/external/webhooks/{webhook_id}

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookOut",
            self._client._request(
                "GET",
                f"/webhooks/{_quote(webhook_id)}",
                timeout=timeout,
            ),
        )

    def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookListOut:
        """Список вебхуков

        Все вебхуки аккаунта: созданные через API v1, v2 и в кабинете. Секреты не показываются.

        Смотрите is_active и consecutive_failures: так видно вебхук, выключенный после 10 провалов подряд.
        Ошибки: 401 неверный ключ.

        GET /api/v2/external/webhooks

        Аргументы:
            limit: Сколько записей на странице
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookListOut",
            self._client._request(
                "GET",
                "/webhooks",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[WebhookOut]:
        """Список вебхуков: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сколько записей на странице
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate("/webhooks", params={"limit": limit}, timeout=timeout)

    def list_deliveries(
        self,
        webhook_id: str,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookDeliveryListOut:
        """История доставок

        История доставок вебхука, новые первыми: событие, статус, номер попытки, ответ вашего адреса.

        Смотрите здесь, почему события не доходят (error_message, response_status) и когда следующая
        попытка (next_retry_at). Не дошедшую доставку можно отправить ещё раз методом retry.
        Ошибки: 404 webhook_not_found.

        GET /api/v2/external/webhooks/{webhook_id}/deliveries

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            limit: Сколько записей на странице
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookDeliveryListOut",
            self._client._request(
                "GET",
                f"/webhooks/{_quote(webhook_id)}/deliveries",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_deliveries_all(
        self,
        webhook_id: str,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Iterator[WebhookDeliveryOut]:
        """История доставок: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            limit: Сколько записей на странице
            timeout: таймаут этого запроса в секундах
        """
        return self._client._paginate(
            f"/webhooks/{_quote(webhook_id)}/deliveries",
            params={"limit": limit},
            timeout=timeout,
        )

    def retry_delivery(
        self,
        webhook_id: str,
        delivery_id: str,
        *,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookRetryOut:
        """Повторить доставку

        Сразу отправляет доставку ещё раз, не дожидаясь расписания повторов, и ждёт ответ.

        Нужен, когда вы починили приёмник и не хотите ждать следующей попытки. Тело и
        X-Wazzapo-Delivery-Id те же, что раньше: дубль отсеется по нему. Счётчик attempt растёт.
        Ошибки: 404 webhook_not_found, 404 webhook_delivery_not_found.

        POST /api/v2/external/webhooks/{webhook_id}/deliveries/{delivery_id}/retry

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            delivery_id: id доставки: поле id из GET /webhooks/{webhook_id}/deliveries или заголовок X-Wazzapo-Delivery-Id запроса, пришедшего на ваш адрес
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookRetryOut",
            self._client._request(
                "POST",
                f"/webhooks/{_quote(webhook_id)}/deliveries/{_quote(delivery_id)}/retry",
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def rotate_secret(
        self,
        webhook_id: str,
        *,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookSecretOut:
        """Сменить секрет подписи

        Выдаёт новый секрет подписи, старый перестаёт действовать сразу.

        Нужен, если секрет потерян или мог утечь. Новый секрет показывается один раз: сразу замените
        его на своём сервере, иначе проверка подписи у вас перестанет проходить. Ошибки: 404 webhook_not_found.

        POST /api/v2/external/webhooks/{webhook_id}/rotate-secret

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookSecretOut",
            self._client._request(
                "POST",
                f"/webhooks/{_quote(webhook_id)}/rotate-secret",
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def test(
        self,
        webhook_id: str,
        *,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookTestOut:
        """Отправить тестовое событие

        Сразу отправляет на адрес вебхука тестовое событие test с настоящей подписью и ждёт ответ.

        Проверьте так приёмник и проверку подписи до боевых событий. Повторов нет, в историю не пишется.
        Результат в ответе: delivered, код и время ответа, ошибка. Ошибки: 404 webhook_not_found.

        POST /api/v2/external/webhooks/{webhook_id}/test

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookTestOut",
            self._client._request(
                "POST",
                f"/webhooks/{_quote(webhook_id)}/test",
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    def update(
        self,
        webhook_id: str,
        *,
        body: WebhookUpdateIn,
        timeout: Optional[float] = None,
    ) -> WebhookOut:
        """Изменить вебхук

        Меняет адрес, события, подпись или включает и выключает вебхук. Непереданные поля не меняются.

        event_types заменяют весь список. is_active=false выключает доставку, is_active=true включает
        снова и обнуляет счётчик провалов (так включают вебхук после автоотключения). Секрет не меняется.
        Ошибки: 404 webhook_not_found, 422 invalid_event_types, 422 адрес не https.

        PATCH /api/v2/external/webhooks/{webhook_id}

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            body: тело запроса, словарь WebhookUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookOut",
            self._client._request(
                "PATCH",
                f"/webhooks/{_quote(webhook_id)}",
                json=body,
                timeout=timeout,
            ),
        )



class AsyncWebhooks:
    """Методы webhooks: create, delete, get, list, list_deliveries, retry_delivery, rotate_secret, test, update."""

    def __init__(self, client: "AsyncWazzapo") -> None:
        self._client = client

    async def create(
        self,
        *,
        body: WebhookCreateIn,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookWithSecretOut:
        """Подписаться на события

        Подписывает ваш адрес https на события: Wazzapo шлёт на него POST с JSON.

        Ответ содержит `secret`: он показывается один раз, сохраните его. Ключ `wz_test_…` вебхук не создаёт, но отдаёт ответ того же вида.

        Ошибки: 422 `invalid_event_types` (список: GET /webhook-event-types), 422 адрес не https или внутренний, 403 `USAGE_LIMIT_EXCEEDED` (лимит вебхуков тарифа).

        **Тело**: `{"event": "<имя>", "timestamp": "<когда создана доставка, ISO 8601 UTC>", "data": {...}}`. `timestamp` одинаков во всех повторах; время самого события внутри `data`. Поля `data` у каждого события описаны в разделе Webhooks описания API (openapi.json, ключ `webhooks`).

        **Единицы сумм** (пример: 150 000 ₸)

        | Где | Поле | Единица | 150 000 ₸ |
        |---|---|---|---|
        | Шаблон, переменная type=currency (messages.send) | `currency.amount_1000` | тенге × 1000 | `150000000` |
        | Сделка в REST (GET/POST/PATCH /deals) | `amount` | тиыны, тенге × 100 | `15000000` |
        | Сделка в вебхуках deal.* | `data.deal.amount` | тиыны, тенге × 100, как в REST | `15000000` |
        | Сделка в вебхуках deal.* | `data.deal.value` | целые тенге, оставлено для совместимости | `150000` |
        | Счёт в вебхуке invoice.status_changed | `data.invoice.amount` | тиыны, тенге × 100 | `15000000` |

        ## Заголовки запроса

        | Заголовок | Что в нём |
        |---|---|
        | `X-Wazzapo-Timestamp` | Время отправки этой попытки: Unix-время в секундах, целое число, UTC, например `1760000000`. В каждой попытке новое |
        | `X-Wazzapo-Signature-V2` | `v2=` и 64 символа hex строчными буквами: HMAC-SHA256 от `{X-Wazzapo-Timestamp}.{тело}`. Проверяйте этот заголовок |
        | `X-Wazzapo-Signature` | Старая подпись без времени: `sha256=` и hex строчными, HMAC-SHA256 от тела. Оставлена для совместимости, не защищает от повтора перехваченного запроса |
        | `X-Wazzapo-Delivery-Id` | id доставки, одинаковый во всех повторах: по нему отсеивайте дубли. Его же принимает POST /webhooks/{webhook_id}/deliveries/{delivery_id}/retry |
        | `X-Wazzapo-Event` | Имя события, то же, что поле `event` тела |
        | `X-Wazzapo-Attempt` | Номер попытки: 1 у первой, до 6 |
        | `Content-Type` | `application/json`; `User-Agent: Wazzapo-Webhooks/1.0` |

        У тестового события (POST /webhooks/{webhook_id}/test, event=test) нет `X-Wazzapo-Delivery-Id` и `X-Wazzapo-Attempt`.

        **Как проверить подпись**

        1. Возьмите тело запроса сырыми байтами, как пришло, до разбора JSON. Не собирайте JSON заново: порядок полей, отсутствие пробелов и кириллица в UTF-8 (без `\\u`-экранирования) должны совпасть байт в байт.
        2. Строка для подписи: значение `X-Wazzapo-Timestamp`, точка, тело: `{timestamp}.{body}`.
        3. Ключ HMAC: секрет вебхука целиком, вместе с `whsec_`, в UTF-8 (из ответа POST /webhooks или rotate-secret).
        4. Ожидаемое значение: `v2=` + HMAC-SHA256(ключ, строка) в hex строчными буквами.
        5. Сравните с `X-Wazzapo-Signature-V2` сравнением за постоянное время (`hash_equals`, `crypto.timingSafeEqual`, `hmac.compare_digest`). Не совпало: ответьте 401.
        6. Отклоните запрос, если `X-Wazzapo-Timestamp` отличается от вашего времени больше чем на 300 секунд.

        **Пример с готовыми значениями**: секрет `whsec_test`, `X-Wazzapo-Timestamp: 1760000000`, тело `{"event":"message.incoming"}` (28 байт). Строка для подписи `1760000000.{"event":"message.incoming"}`, `X-Wazzapo-Signature-V2: v2=a7e2dad2ec4a0f54d4f46ea51f2c28803b66f4effebb959c6ff8e8cc59f47fca`, старая `X-Wazzapo-Signature: sha256=b8745e4a15618d503f14d3e7fb12aa3c5cf3064a4bbc50b5f515eae87ee76cd7`.

        **PHP**

        ```php
        $body = file_get_contents('php://input');           // сырое тело
        $ts   = $_SERVER['HTTP_X_WAZZAPO_TIMESTAMP'] ?? '';
        $sig  = $_SERVER['HTTP_X_WAZZAPO_SIGNATURE_V2'] ?? '';
        $expected = 'v2=' . hash_hmac('sha256', $ts . '.' . $body, $secret);
        if (!hash_equals($expected, $sig) || abs(time() - (int)$ts) > 300) { http_response_code(401); exit; }
        $event = json_decode($body, true);
        http_response_code(200);
        ```

        **Node.js (Express)**

        ```js
        app.post('/hooks/wazzapo', express.raw({ type: 'application/json' }), (req, res) => {
          const ts = req.get('X-Wazzapo-Timestamp') || '';
          const sig = req.get('X-Wazzapo-Signature-V2') || '';
          const expected = 'v2=' + crypto.createHmac('sha256', SECRET)
            .update(ts + '.').update(req.body).digest('hex');   // req.body: Buffer
          const ok = sig.length === expected.length &&
            crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected));
          if (!ok || Math.abs(Date.now() / 1000 - Number(ts)) > 300) return res.sendStatus(401);
          res.sendStatus(200);                                 // ответ сразу, обработка потом
          const event = JSON.parse(req.body.toString('utf8'));
        });
        ```

        **Ответ и повторы.** Ответьте любым 2xx за 10 секунд; тело ответа не важно. Иначе повторы через 1 мин, 5 мин, 30 мин, 2 ч и 6 ч (±20%), всего 6 попыток, с тем же телом и `X-Wazzapo-Delivery-Id`. Доставка «хотя бы один раз»: дубли возможны, отсеивайте их по `X-Wazzapo-Delivery-Id`. Порядок событий не гарантирован: сверяйте поле `timestamp`. После 10 доставок подряд, не дошедших за все попытки, вебхук выключается (`is_active=false`), включить снова: PATCH с `is_active=true`.

        POST /api/v2/external/webhooks

        Аргументы:
            body: тело запроса, словарь WebhookCreateIn
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookWithSecretOut",
            await self._client._request(
                "POST",
                "/webhooks",
                json=body,
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def delete(self, webhook_id: str, *, timeout: Optional[float] = None) -> None:
        """Удалить вебхук

        Удаляет вебхук вместе с историей доставок: события на адрес больше не приходят.

        Чтобы остановить на время, лучше выключите: PATCH с is_active=false. Ответ 204 без тела.
        Ошибки: 404 webhook_not_found.

        DELETE /api/v2/external/webhooks/{webhook_id}

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            timeout: таймаут этого запроса в секундах
        """
        await self._client._request("DELETE", f"/webhooks/{_quote(webhook_id)}", timeout=timeout)
        return None

    async def get(self, webhook_id: str, *, timeout: Optional[float] = None) -> WebhookOut:
        """Вебхук

        Один вебхук: адрес, события, включён ли и сколько доставок подряд не дошли. Без секрета.

        Ошибки: 404 webhook_not_found.

        GET /api/v2/external/webhooks/{webhook_id}

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookOut",
            await self._client._request(
                "GET",
                f"/webhooks/{_quote(webhook_id)}",
                timeout=timeout,
            ),
        )

    async def list(
        self,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookListOut:
        """Список вебхуков

        Все вебхуки аккаунта: созданные через API v1, v2 и в кабинете. Секреты не показываются.

        Смотрите is_active и consecutive_failures: так видно вебхук, выключенный после 10 провалов подряд.
        Ошибки: 401 неверный ключ.

        GET /api/v2/external/webhooks

        Аргументы:
            limit: Сколько записей на странице
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookListOut",
            await self._client._request(
                "GET",
                "/webhooks",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_all(
        self,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[WebhookOut]:
        """Список вебхуков: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            limit: Сколько записей на странице
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate("/webhooks", params={"limit": limit}, timeout=timeout)

    async def list_deliveries(
        self,
        webhook_id: str,
        *,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookDeliveryListOut:
        """История доставок

        История доставок вебхука, новые первыми: событие, статус, номер попытки, ответ вашего адреса.

        Смотрите здесь, почему события не доходят (error_message, response_status) и когда следующая
        попытка (next_retry_at). Не дошедшую доставку можно отправить ещё раз методом retry.
        Ошибки: 404 webhook_not_found.

        GET /api/v2/external/webhooks/{webhook_id}/deliveries

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            limit: Сколько записей на странице
            cursor: next_cursor из прошлого ответа; без него первая страница
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookDeliveryListOut",
            await self._client._request(
                "GET",
                f"/webhooks/{_quote(webhook_id)}/deliveries",
                params={"limit": limit, "cursor": cursor},
                timeout=timeout,
            ),
        )

    def list_deliveries_all(
        self,
        webhook_id: str,
        *,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncIterator[WebhookDeliveryOut]:
        """История доставок: все страницы подряд.

        Обходит страницы сам, по одной за раз; элементы отдаёт по одному

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            limit: Сколько записей на странице
            timeout: таймаут этого запроса в секундах
        """
        return self._client._apaginate(
            f"/webhooks/{_quote(webhook_id)}/deliveries",
            params={"limit": limit},
            timeout=timeout,
        )

    async def retry_delivery(
        self,
        webhook_id: str,
        delivery_id: str,
        *,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookRetryOut:
        """Повторить доставку

        Сразу отправляет доставку ещё раз, не дожидаясь расписания повторов, и ждёт ответ.

        Нужен, когда вы починили приёмник и не хотите ждать следующей попытки. Тело и
        X-Wazzapo-Delivery-Id те же, что раньше: дубль отсеется по нему. Счётчик attempt растёт.
        Ошибки: 404 webhook_not_found, 404 webhook_delivery_not_found.

        POST /api/v2/external/webhooks/{webhook_id}/deliveries/{delivery_id}/retry

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            delivery_id: id доставки: поле id из GET /webhooks/{webhook_id}/deliveries или заголовок X-Wazzapo-Delivery-Id запроса, пришедшего на ваш адрес
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookRetryOut",
            await self._client._request(
                "POST",
                f"/webhooks/{_quote(webhook_id)}/deliveries/{_quote(delivery_id)}/retry",
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def rotate_secret(
        self,
        webhook_id: str,
        *,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookSecretOut:
        """Сменить секрет подписи

        Выдаёт новый секрет подписи, старый перестаёт действовать сразу.

        Нужен, если секрет потерян или мог утечь. Новый секрет показывается один раз: сразу замените
        его на своём сервере, иначе проверка подписи у вас перестанет проходить. Ошибки: 404 webhook_not_found.

        POST /api/v2/external/webhooks/{webhook_id}/rotate-secret

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookSecretOut",
            await self._client._request(
                "POST",
                f"/webhooks/{_quote(webhook_id)}/rotate-secret",
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def test(
        self,
        webhook_id: str,
        *,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> WebhookTestOut:
        """Отправить тестовое событие

        Сразу отправляет на адрес вебхука тестовое событие test с настоящей подписью и ждёт ответ.

        Проверьте так приёмник и проверку подписи до боевых событий. Повторов нет, в историю не пишется.
        Результат в ответе: delivered, код и время ответа, ошибка. Ошибки: 404 webhook_not_found.

        POST /api/v2/external/webhooks/{webhook_id}/test

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            idempotency_key: свой ключ повтора; без него SDK создаст новый на каждый вызов
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookTestOut",
            await self._client._request(
                "POST",
                f"/webhooks/{_quote(webhook_id)}/test",
                idempotency_key=idempotency_key,
                timeout=timeout,
            ),
        )

    async def update(
        self,
        webhook_id: str,
        *,
        body: WebhookUpdateIn,
        timeout: Optional[float] = None,
    ) -> WebhookOut:
        """Изменить вебхук

        Меняет адрес, события, подпись или включает и выключает вебхук. Непереданные поля не меняются.

        event_types заменяют весь список. is_active=false выключает доставку, is_active=true включает
        снова и обнуляет счётчик провалов (так включают вебхук после автоотключения). Секрет не меняется.
        Ошибки: 404 webhook_not_found, 422 invalid_event_types, 422 адрес не https.

        PATCH /api/v2/external/webhooks/{webhook_id}

        Аргументы:
            webhook_id: id вебхука: поле id из ответа POST /webhooks или из GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
            body: тело запроса, словарь WebhookUpdateIn
            timeout: таймаут этого запроса в секундах
        """
        return cast(
            "WebhookOut",
            await self._client._request(
                "PATCH",
                f"/webhooks/{_quote(webhook_id)}",
                json=body,
                timeout=timeout,
            ),
        )



RESOURCES = {
    "contacts": (Contacts, AsyncContacts),
    "conversations": (Conversations, AsyncConversations),
    "deals": (Deals, AsyncDeals),
    "media": (Media, AsyncMedia),
    "messages": (Messages, AsyncMessages),
    "phone_numbers": (PhoneNumbers, AsyncPhoneNumbers),
    "pipelines": (Pipelines, AsyncPipelines),
    "tasks": (Tasks, AsyncTasks),
    "team": (Team, AsyncTeam),
    "templates": (Templates, AsyncTemplates),
    "webhook_event_types": (WebhookEventTypes, AsyncWebhookEventTypes),
    "webhooks": (Webhooks, AsyncWebhooks),
}
