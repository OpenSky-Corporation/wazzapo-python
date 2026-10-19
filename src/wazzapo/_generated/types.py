# Сгенерировано sdk/codegen/python.py из sdk/openapi.json. Не править руками: cd sdk && python -m codegen

"""Типы запросов и ответов API v2: словари с подсказками для редактора."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union


class _AddNoteInRequired(TypedDict):
    #: Текст заметки до 4096 символов, например «Перезвонить после 18:00». Клиент её не видит
    text: str


class AddNoteIn(_AddNoteInRequired, total=False):
    #: Кого упомянуть: id сотрудников из GET /api/v2/external/team, например ["7"], до 50. Им придёт уведомление в кабинете; имя в тексте (@Ерлан) уведомление не отправляет
    mention_user_ids: List[str]


class AssignConversationIn(TypedDict):
    #: id сотрудника строкой из цифр: поле id из GET /api/v2/external/team, например "7" (можно и числом 7). Поле обязательно: чтобы снять ответственного, передайте {"user_id": null}. Сотрудник отключён или не из команды: 409 CONFLICT, наблюдатель: 403 FORBIDDEN
    user_id: Optional[str]


class AttributionSourceOut(TypedDict, total=False):
    """Один источник клиента. Набор полей зависит от kind: заполнены только известные."""
    #: id объявления Meta, по которому клиент написал, например 120210000000000001
    ad_id: Optional[str]
    #: Название объявления в рекламном кабинете Meta
    ad_name: Optional[str]
    #: Что открыл клиент по данным Meta: ad или post
    ad_type: Optional[str]
    #: Название группы объявлений в рекламном кабинете Meta
    adset: Optional[str]
    #: Когда источник записан, ISO 8601 UTC
    at: Optional[str]
    #: Текст объявления, которое видел клиент
    body: Optional[str]
    #: Кампания: utm_campaign, название рекламной кампании Meta или название ссылки с меткой
    campaign: Optional[str]
    #: id рекламной кампании Meta
    campaign_id: Optional[str]
    #: Метка клика: ctwa_clid рекламы WhatsApp, gclid Google, yclid Яндекса или fbclid Facebook
    click_id: Optional[str]
    #: utm_content из адреса или запроса
    content: Optional[str]
    #: Заголовок объявления, которое видел клиент
    headline: Optional[str]
    #: Вид источника: ad (реклама Meta «Написать в WhatsApp» или Instagram), utm (метки в адресе сайта), referrer (переход с другого сайта), link (ссылка с меткой из раздела «Ссылки с меткой»), api (метки utm_* переданы через API или форму сайта)
    kind: Optional[str]
    #: Код ссылки с меткой из раздела «Ссылки с меткой», только у kind=link
    link_code: Optional[str]
    #: Название ссылки с меткой, только у kind=link
    link_name: Optional[str]
    #: Тип трафика: utm_medium (cpc, email), ad у рекламы, link у ссылки с меткой
    medium: Optional[str]
    #: Страница сайта, с которой пришёл клиент, например /implant
    page: Optional[str]
    #: Адрес сайта, с которого перешли на вашу страницу
    referrer: Optional[str]
    #: Откуда: для рекламы instagram, facebook или meta; для меток значение utm_source (google, yandex); для перехода адрес сайта, например 2gis.kz; для ссылки её канал
    source: Optional[str]
    #: utm_term из адреса или запроса
    term: Optional[str]
    #: Ссылка на объявление или пост
    url: Optional[str]


class BusinessProfileIn(TypedDict, total=False):
    """Поля профиля компании; переданные заменяют текущие, не переданные не меняются."""
    #: Статус под именем в WhatsApp, до 139 знаков
    about: Optional[str]
    #: Адрес, до 256 знаков, например «Астана, пр. Абая, 15»
    address: Optional[str]
    #: Описание компании, до 512 знаков
    description: Optional[str]
    #: Почта для клиентов, до 128 знаков
    email: Optional[str]
    #: Отрасль из списка Meta: BEAUTY, RETAIL, EDU, HEALTH, RESTAURANT, PROF_SERVICES, OTHER и другие
    vertical: Optional[str]
    #: Сайты компании, до 2 адресов с http:// или https://
    websites: Optional[List[str]]


class BusinessProfileOut(TypedDict, total=False):
    """Профиль компании в WhatsApp, поля как в Cloud API."""
    #: Статус под именем в WhatsApp
    about: Optional[str]
    #: Адрес компании
    address: Optional[str]
    #: Описание компании
    description: Optional[str]
    #: Почта для клиентов
    email: Optional[str]
    #: Ссылка на фото профиля; ссылка временная, не храните её
    profile_picture_url: Optional[str]
    #: Отрасль из списка Meta, например BEAUTY
    vertical: Optional[str]
    #: Сайты компании
    websites: Optional[List[str]]


class BusinessProfileUpdateOut(TypedDict, total=False):
    #: true: Meta сохранила профиль
    success: bool


class ContactAttributionOut(TypedDict, total=False):
    #: Первый источник: откуда клиент пришёл впервые. Не меняется после записи
    first: Optional[AttributionSourceOut]
    #: Последний источник: откуда пришёл в последний раз (при одном источнике совпадает с first)
    last: Optional[AttributionSourceOut]


class _ContactCardRequired(TypedDict):
    #: Имя контакта
    name: ContactCardName


class ContactCard(_ContactCardRequired, total=False):
    """Карточка контакта Cloud API. Остальные поля Meta (emails, org, urls, addresses,
    birthday) принимаются и передаются как есть.
    """
    #: Номера контакта
    phones: List[ContactCardPhone]


class _ContactCardNameRequired(TypedDict):
    #: Имя, как его покажет WhatsApp, например «Ерлан Сапаров»
    formatted_name: str


class ContactCardName(_ContactCardNameRequired, total=False):
    #: Имя, например Ерлан
    first_name: Optional[str]
    #: Фамилия, например Сапаров
    last_name: Optional[str]


class _ContactCardPhoneRequired(TypedDict):
    #: Номер в любом виде, например +7 707 123 45 67
    phone: str


class ContactCardPhone(_ContactCardPhoneRequired, total=False):
    #: Вид номера: CELL, MAIN, IPHONE, HOME или WORK
    type: Optional[str]
    #: Номер WhatsApp цифрами без +, например 77071234567: у клиента появится кнопка «Написать»
    wa_id: Optional[str]


class _ContactCreateInRequired(TypedDict):
    #: Номер клиента: цифры с кодом страны, плюс в начале можно: 77071234567 или +77071234567. Пробелы, скобки и дефисы не принимаются (422 VALIDATION_ERROR). 8 в начале казахстанского номера заменяется на 7 (87071234567 сохранится как 77071234567). Номер не похож на настоящий: 422 invalid_phone. Номер уже есть у контакта: 409 contact_exists
    phone: str


class ContactCreateIn(_ContactCreateInRequired, total=False):
    #: Свои поля контакта из раздела «Поля контакта» в кабинете. Ключ: имя переменной поля (колонка «Переменная», например city или birthday; у поля без переменной его id). Значение по типу поля: текст и список строкой, число числом, флажок true/false, дата строкой ГГГГ-ММ-ДД. Пример: {"city": "Алматы", "orders_count": 3}. Поля, которых нет в кабинете: ошибка 422 unknown_custom_field
    custom_fields: Dict[str, Any]
    #: Почта клиента, например aigul@example.kz
    email: Optional[str]
    #: Ваш id этого клиента в своей CRM или учётной системе, например 1c-00042. Wazzapo его не проверяет и не требует уникальности; найти контакт по нему: GET /contacts?external_id=1c-00042. До 200 символов
    external_id: Optional[str]
    #: Имя клиента, как его видят менеджеры в диалогах и сделках, например Айгуль Серикова. До 200 символов
    name: Optional[str]
    #: Метки контакта: любые строки, например vip или опт; по ним фильтрует ?tag= и сегменты рассылок. До 100 меток
    tags: List[str]


class _ContactListOutRequired(TypedDict):
    #: Контакты страницы, старые первыми
    data: List[ContactV2Out]


class ContactListOut(_ContactListOutRequired, total=False):
    #: true, если есть следующая страница
    has_more: bool
    #: Передайте в ?cursor=, чтобы получить следующую страницу; null на последней
    next_cursor: Optional[str]


class ContactUpdateIn(TypedDict, total=False):
    """Меняются только переданные поля. custom_fields дополняют сохранённые, null убирает поле."""
    #: Меняются только переданные ключи, остальные поля остаются; значение null очищает поле. Свои поля контакта из раздела «Поля контакта» в кабинете. Ключ: имя переменной поля (колонка «Переменная», например city или birthday; у поля без переменной его id). Значение по типу поля: текст и список строкой, число числом, флажок true/false, дата строкой ГГГГ-ММ-ДД. Пример: {"city": "Алматы", "orders_count": 3}. Поля, которых нет в кабинете: ошибка 422 unknown_custom_field
    custom_fields: Optional[Dict[str, Any]]
    #: Почта клиента, например aigul@example.kz
    email: Optional[str]
    #: Ваш id этого клиента в своей CRM или учётной системе, например 1c-00042. Wazzapo его не проверяет и не требует уникальности; найти контакт по нему: GET /contacts?external_id=1c-00042
    external_id: Optional[str]
    #: Имя клиента, как его видят менеджеры в диалогах и сделках, например Айгуль Серикова. До 200 символов
    name: Optional[str]
    #: Новый список меток целиком: заменяет старый. [] или null убирают все метки. Чтобы добавить метку, передайте старые метки вместе с новой
    tags: Optional[List[str]]


class _ContactV2OutRequired(TypedDict):
    #: id контакта в Wazzapo, например 6712f0c4a1b2c3d4e5f60718: для GET, PATCH и DELETE /contacts/{contact_id}
    id: str
    #: Как контакт появился: manual (добавили в кабинете), whatsapp (сам написал в мессенджер), import (загрузили из файла), api (создан через API), email (пришло письмо)
    source: str


class ContactV2Out(_ContactV2OutRequired, total=False):
    """Контакт (клиент) аккаунта."""
    #: Откуда пришёл клиент: реклама Meta, метки сайта (UTM), ссылка с меткой. null, если неизвестно
    attribution: Optional[ContactAttributionOut]
    #: Когда создан, ISO 8601 UTC
    created_at: Optional[str]
    #: Свои поля контакта из раздела «Поля контакта» в кабинете. Ключ: имя переменной поля (колонка «Переменная», например city или birthday; у поля без переменной его id). Значение по типу поля: текст и список строкой, число числом, флажок true/false, дата строкой ГГГГ-ММ-ДД. Пример: {"city": "Алматы", "orders_count": 3}. Поля, которых нет в кабинете: ошибка 422 unknown_custom_field
    custom_fields: Dict[str, Any]
    #: Почта клиента, например aigul@example.kz
    email: Optional[str]
    #: Ваш id этого клиента в своей CRM или учётной системе, например 1c-00042. Wazzapo его не проверяет и не требует уникальности; найти контакт по нему: GET /contacts?external_id=1c-00042
    external_id: Optional[str]
    #: Имя клиента, как его видят менеджеры в диалогах и сделках, например Айгуль Серикова
    name: Optional[str]
    #: Номер цифрами с кодом страны, без плюса и пробелов, например 77071234567
    phone: Optional[str]
    #: Метки контакта: любые строки, например vip или опт; по ним фильтрует ?tag= и сегменты рассылок. До 100 меток
    tags: List[str]
    #: Когда изменён в последний раз, ISO 8601 UTC
    updated_at: Optional[str]


class ConversationContactOut(TypedDict, total=False):
    #: Адрес клиента в канале без телефона: id чата Telegram, почта, id в Instagram или OLX. У WhatsApp null
    external_id: Optional[str]
    #: id контакта Wazzapo, как в GET /api/v2/external/contacts; null у участника группы
    id: Optional[str]
    #: Имя клиента в Wazzapo или из профиля канала, например Айгуль; null, если неизвестно
    name: Optional[str]
    #: Телефон клиента цифрами с кодом страны без +, например 77071234567. Есть у WhatsApp и чата на сайте, у остальных каналов null (адрес в external_id)
    phone: Optional[str]


class _ConversationItemOutRequired(TypedDict):
    #: Канал диалога: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
    channel: str
    #: Клиент, с которым идёт диалог
    contact: ConversationContactOut
    #: Номер диалога в кабинете, как #5 в списке чатов
    display_id: int
    #: id диалога, например 6a7d5d3712f8e1a5c19f40c4: conversation_id в остальных методах и вебхуках
    id: str
    #: Последнее сообщение диалога для списка
    last_message: ConversationLastMessageOut
    #: Подключение (канал) диалога в Wazzapo, например meta_103799815708451; то же поле в вебхуках
    session_id: str
    #: Статус диалога: open (открыт, менеджеру нужно ответить), pending (ожидает: ответ дан, ждём клиента или другой отдел), snoozed (отложен до snoozed_until), resolved (решён, закрыт). Новое сообщение клиента снова открывает решённый и отложенный диалог
    status: Literal['open', 'pending', 'snoozed', 'resolved']


class ConversationItemOut(_ConversationItemOutRequired, total=False):
    """Диалог с клиентом в одном канале: контакт, ответственный, статус, метки."""
    #: Ответственный менеджер; null, если не назначен. Назначить: POST .../assign
    assignee: Optional[StaffRefOut]
    #: Когда диалог появился, UTC в формате ISO 8601, например 2026-10-18T09:15:00Z
    created_at: Optional[str]
    #: true: групповой чат WhatsApp, а не переписка с одним клиентом
    is_group: bool
    #: Номер WhatsApp, через который идёт диалог: phone_number_id из GET /api/v2/external/phone-numbers. У других каналов null
    phone_number_id: Optional[str]
    #: До какого времени отложен (статус snoozed), UTC в формате ISO 8601, например 2026-10-18T09:15:00Z; иначе null
    snoozed_until: Optional[str]
    #: Метки диалога, например ["VIP", "доставка"]. Задать: POST .../labels
    tags: List[str]
    #: Сколько сообщений клиента ещё не прочитали в кабинете
    unread_count: int
    #: Когда диалог последний раз менялся (сообщение, статус, ответственный, метки), UTC в формате ISO 8601, например 2026-10-18T09:15:00Z. По нему работает updated_since в GET /conversations
    updated_at: Optional[str]


class ConversationLastMessageOut(TypedDict, total=False):
    #: Начало последнего сообщения, как в списке чатов; пустая строка, если сообщений нет
    text: str
    #: Когда пришло или ушло последнее сообщение, UTC в формате ISO 8601, например 2026-10-18T09:15:00Z
    timestamp: Optional[str]
    #: Тип последнего сообщения: text, image, video, audio, voice, document, location, contact, sticker, call; null, если сообщений нет
    type: Optional[str]


class _ConversationListOutRequired(TypedDict):
    #: Диалоги страницы от давно изменённых к недавним
    data: List[ConversationItemOut]


class ConversationListOut(_ConversationListOutRequired, total=False):
    #: true: есть следующая страница, запросите её с next_cursor
    has_more: bool
    #: Курсор следующей страницы: передайте его в параметр cursor. null, если это последняя страница
    next_cursor: Optional[str]


class _ConversationMessageListOutRequired(TypedDict):
    #: Сообщения страницы от старых к новым
    data: List[ConversationMessageOut]


class ConversationMessageListOut(_ConversationMessageListOutRequired, total=False):
    #: true: есть следующая страница, запросите её с next_cursor
    has_more: bool
    #: Курсор следующей страницы: передайте его в параметр cursor. null, если это последняя страница
    next_cursor: Optional[str]


class _ConversationMessageOutRequired(TypedDict):
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
    channel: str
    #: Клиент диалога; в группе участник, который написал
    contact: ConversationContactOut
    #: in: от клиента, out: от вас (менеджер, бот, API)
    direction: Literal['in', 'out']
    #: id сообщения: у WhatsApp wamid, например wamid.HBgLNzcwNzEyMzQ1NjcVAgARGBI1
    id: str
    #: Кто написал сообщение
    sender: MessageSenderOut
    #: Подключение, через которое прошло сообщение, например meta_103799815708451
    session_id: str
    #: Тип: text, image, video, audio, voice, document, location, contact, sticker, call. Шаблон приходит как text, его имя и значения в template. Нажатие кнопки клиентом тоже text: текст кнопки в text, сама кнопка в interactive
    type: str


class ConversationMessageOut(_ConversationMessageOutRequired, total=False):
    """Сообщение диалога или заметка сотрудника."""
    #: id диалога из GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Только у входящего: клиент нажал кнопку или выбрал пункт списка, как message.interactive в вебхуке message.incoming. Кнопка сообщения type=interactive: type=button_reply и id = reply.id; быстрая кнопка шаблона: type=button, id и payload = payload кнопки. У остальных сообщений null
    interactive: Optional[InteractiveResponseOut]
    #: true: сообщение удалено, text и media_url пустые
    is_deleted: bool
    #: true: заметка сотрудника, клиент её не видит
    is_note: bool
    #: Ссылка на файл (картинка, документ, голосовое); null у текста
    media_url: Optional[str]
    #: Доставка исходящего: pending (в очереди), sent (отправлено), delivered (доставлено), read (прочитано), failed (ошибка). Изменения приходят вебхуком message.status
    status: Optional[str]
    #: Шаблон WhatsApp, если сообщение шаблонное; иначе null
    template: Optional[MessageTemplateRefOut]
    #: Текст или подпись к файлу; пустая строка у удалённого сообщения
    text: str
    #: Время сообщения, UTC в формате ISO 8601, например 2026-10-18T09:15:00Z. Его передают в since
    timestamp: Optional[str]


class CreateTemplateIn(TypedDict):
    """Новый шаблон: уходит на проверку Meta, обычно ответ за минуты, иногда до 24 часов."""
    #: UTILITY: служебное по заказу или записи клиента (подтверждение, напоминание, статус), дешевле рекламного. MARKETING: реклама, акции, скидки, приглашения. AUTHENTICATION: код подтверждения входа. Meta сама переносит в MARKETING служебный шаблон с рекламой, об этом придёт событие template.category_changed
    category: Literal['MARKETING', 'UTILITY', 'AUTHENTICATION']
    #: Части шаблона: BODY обязателен, HEADER, FOOTER и BUTTONS по желанию, каждая не больше одной. Вид части выбирается полем type, у шапки ещё полем format
    components: List[Union[TemplateHeaderText, TemplateHeaderMedia, TemplateHeaderLocation, TemplateBody, TemplateFooter, TemplateButtons]]
    #: Код языка Meta: ru, kk, en, en_US, uz и др. Полный список: developers.facebook.com, раздел WhatsApp, Templates, Supported languages
    language: str
    #: Имя шаблона: латиница в нижнем регистре, цифры и _, до 512 символов, например zapis_napominanie. Уникально для номера и языка. Имя удалённого одобренного шаблона занято 30 дней
    name: str
    #: id номера WhatsApp: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
    phone_number_id: str


class CtaUrlParameters(TypedDict):
    #: Надпись на кнопке, до 20 знаков
    display_text: str
    #: Адрес, который откроется по нажатию, начинается с http:// или https://
    url: str


class _DealContactInRequired(TypedDict):
    #: Телефон клиента: цифры с кодом страны, плюс в начале можно: 77071234567 или +77071234567. Здесь можно и с пробелами, скобками и дефисами (+7 707 123-45-67), 8 в начале казахстанского номера заменяется на 7 (8 707 123 45 67). Номер, который не похож на настоящий: 422 VALIDATION_ERROR. Если контакт с этим номером есть, сделка привяжется к нему, иначе создадим новый
    phone: str


class DealContactIn(_DealContactInRequired, total=False):
    #: Имя для нового контакта, например «Айгуль Сейткали»
    name: Optional[str]


class _DealContactOutRequired(TypedDict):
    #: id контакта Wazzapo: его можно передать в contact_id новой сделки
    id: str


class DealContactOut(_DealContactOutRequired, total=False):
    #: Имя клиента, например «Айгуль Сейткали»
    name: Optional[str]
    #: Телефон цифрами с кодом страны, без плюса и пробелов, например 77071234567
    phone: Optional[str]


class _DealCreateInRequired(TypedDict):
    #: id воронки: поле id из GET /pipelines, например 6712a0c4e1b2c3d4e5f60718
    pipeline_id: str


class DealCreateIn(_DealCreateInRequired, total=False):
    #: Сумма сделки. Целое число в тиынах: 1 ₸ = 100 тиынов, 150 000 ₸ = 15000000. Целым, чтобы сумма не искажалась при округлении дробей. Пишется в поле суммы воронки (is_amount). Внимание: в тиынах (× 100), а не в тенге: 150 000 ₸ = 15000000. В шаблоне WhatsApp (messages.send, currency.amount_1000) множитель другой, × 1000: 150 000 ₸ = 150000000
    amount: Optional[int]
    #: Клиент по телефону, если id контакта не знаете: найдём по номеру или создадим
    contact: Optional[DealContactIn]
    #: id существующего контакта из GET /contacts. Передайте его или contact с телефоном
    contact_id: Optional[str]
    #: Валюта суммы, должна совпасть с currency поля суммы воронки (обычно KZT), иначе 422 currency_mismatch
    currency: Optional[str]
    #: Свои поля сделки: ключ: id поля из GET /pipelines (custom_fields[].id воронки), значение по типу поля: text и multiline строкой, number числом, money целым в тиынах, select одной строкой из options, date строкой ГГГГ-ММ-ДД, checkbox true или false. Например {"9c8b7a6d5e4f": "Сайт", "3e4f5a6b7c8d": "Астана", "7d8e9f0a1b2c": "2026-10-21"}. Поля не из этой воронки: 422 unknown_custom_field
    custom_fields: Dict[str, Any]
    #: id этой сделки в вашей системе (CRM, сайт, 1С), до 200 знаков, например site-order-4521. Повтор POST /deals с тем же external_id (например, клиент дважды отправил форму) сделку не создаёт: 409 deal_exists, id существующей сделки в details.deal_id. Одновременные запросы закрывает ещё и заголовок Idempotency-Key. Найти сделку: GET /deals?external_id=...
    external_id: Optional[str]
    #: Ответственный: id сотрудника строкой: поле id из GET /team, например "12". Не передали: без ответственного (у ключа сотрудника с ограниченным доступом: сам сотрудник)
    responsible_user_id: Optional[str]
    #: id этапа: stages[].id нужной воронки из GET /pipelines, например a1b2c3d4e5f6a7b8c9d0e1f2. Не передали: первый рабочий этап воронки
    stage_id: Optional[str]
    #: Название, до 300 знаков. Не передали: номер сделки, например #0128
    title: Optional[str]


class _DealListOutRequired(TypedDict):
    #: Сделки на этой странице
    data: List[DealOut]


class DealListOut(_DealListOutRequired, total=False):
    #: true: есть ещё страницы, запросите их с cursor=next_cursor
    has_more: bool
    #: next_cursor для следующей страницы; null: это последняя страница
    next_cursor: Optional[str]


class _DealMoveInRequired(TypedDict):
    #: id этапа: stages[].id нужной воронки из GET /pipelines, например a1b2c3d4e5f6a7b8c9d0e1f2 (этап той же воронки, где сделка)
    stage_id: str


class DealMoveIn(_DealMoveInRequired, total=False):
    #: Причина отказа при переносе на этап с is_lost, до 500 знаков, например «Дорого»
    lost_reason: Optional[str]
    #: Воронка этапа; можно не передавать. Другая воронка пока не поддерживается: 422 pipeline_change_not_supported
    pipeline_id: Optional[str]


class _DealOutRequired(TypedDict):
    #: Клиент сделки
    contact: DealContactOut
    #: id сделки: нужен для GET, PATCH, move и задач
    id: str
    #: Номер сделки в воронке, как в кабинете (#0128)
    number: int
    #: id воронки из GET /pipelines
    pipeline_id: str
    #: id текущего этапа из stages[] воронки
    stage_id: str
    #: open: в работе, won: успешно реализована, lost: закрыта и не реализована
    status: Literal['open', 'won', 'lost']
    #: Название сделки
    title: str


class DealOut(_DealOutRequired, total=False):
    #: Сумма сделки. Целое число в тиынах: 1 ₸ = 100 тиынов, 150 000 ₸ = 15000000. Целым, чтобы сумма не искажалась при округлении дробей
    amount: int
    #: Когда закрыта (успехом или отказом). Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    closed_at: Optional[str]
    #: Диалог с клиентом, к которому привязана сделка: GET /conversations/{conversation_id}
    conversation_id: Optional[str]
    #: Когда создана. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    created_at: Optional[str]
    #: Валюта суммы, например KZT
    currency: str
    #: Свои поля сделки: ключ: id поля из GET /pipelines (custom_fields[].id воронки), значение по типу поля: text и multiline строкой, number числом, money целым в тиынах, select одной строкой из options, date строкой ГГГГ-ММ-ДД, checkbox true или false. Например {"9c8b7a6d5e4f": "Сайт", "3e4f5a6b7c8d": "Астана", "7d8e9f0a1b2c": "2026-10-21"}. Поля не из этой воронки: 422 unknown_custom_field. Поле суммы воронки (is_amount) тоже здесь, с тем же значением, что amount: это не вторая сумма
    custom_fields: Dict[str, Any]
    #: id сделки в вашей системе, если передавали
    external_id: Optional[str]
    #: Когда перенесена на этап отказа. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    lost_at: Optional[str]
    #: Причина отказа, если сделка проиграна
    lost_reason: Optional[str]
    #: Ответственный: id сотрудника строкой: поле id из GET /team, например "12"
    responsible_user_id: Optional[str]
    #: Откуда сделка: api: создана через API, workflow: сценарием, manual: вручную в кабинете, rule: правилом по входящему
    source: Optional[str]
    #: Название текущего этапа
    stage_name: str
    #: Когда изменена. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    updated_at: Optional[str]
    #: Когда перенесена на успешный этап. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    won_at: Optional[str]


class DealUpdateIn(TypedDict, total=False):
    #: Новая сумма. Целое число в тиынах: 1 ₸ = 100 тиынов, 150 000 ₸ = 15000000. Целым, чтобы сумма не искажалась при округлении дробей. Внимание: в тиынах (× 100), а не в тенге: 150 000 ₸ = 15000000. В шаблоне WhatsApp (messages.send, currency.amount_1000) множитель другой, × 1000: 150 000 ₸ = 150000000
    amount: Optional[int]
    #: Валюта суммы, как у поля суммы воронки, обычно KZT
    currency: Optional[str]
    #: Свои поля сделки: ключ: id поля из GET /pipelines (custom_fields[].id воронки), значение по типу поля: text и multiline строкой, number числом, money целым в тиынах, select одной строкой из options, date строкой ГГГГ-ММ-ДД, checkbox true или false. Например {"9c8b7a6d5e4f": "Сайт", "3e4f5a6b7c8d": "Астана", "7d8e9f0a1b2c": "2026-10-21"}. Поля не из этой воронки: 422 unknown_custom_field. Меняются только переданные поля, null очищает поле
    custom_fields: Optional[Dict[str, Any]]
    #: id этой сделки в вашей системе (CRM, сайт, 1С), до 200 знаков, например site-order-4521. При правке на повтор не проверяется. null очищает
    external_id: Optional[str]
    #: Новый ответственный: id сотрудника строкой: поле id из GET /team, например "12". null не снимает ответственного
    responsible_user_id: Optional[str]
    #: Новое название, 1–300 знаков
    title: Optional[str]


class _ErrorBodyRequired(TypedDict):
    #: Машинный код ошибки, на него ориентируйтесь в коде, например outside_24h_window. Список в описании API
    code: str
    #: Причина по-русски, для человека; текст может меняться
    message: str


class ErrorBody(_ErrorBodyRequired, total=False):
    #: Подробности, если есть. Для VALIDATION_ERROR это список полей, не прошедших проверку (field, message), для остальных кодов объект: у INSUFFICIENT_SCOPE required_scope, у USAGE_LIMIT_EXCEEDED current, limit и upgrade_url
    details: Optional[Union[List[ErrorField], Dict[str, Any]]]


class ErrorField(TypedDict):
    """Поле запроса, не прошедшее проверку (details у VALIDATION_ERROR)."""
    #: Где ошибка: body.to, query.limit и т.п.
    field: str
    #: Что не так с этим полем
    message: str


class _ErrorOutRequired(TypedDict):
    #: Что случилось
    error: ErrorBody


class ErrorOut(_ErrorOutRequired, total=False):
    """Тело любой ошибки API v2."""
    #: id запроса (или ваш заголовок X-Request-Id): сообщите его в поддержку, чтобы мы нашли запрос в журнале
    request_id: Optional[str]
    #: Всегда false
    success: bool


class InteractiveAction(TypedDict, total=False):
    """Что под текстом: кнопки (button), список (list), ссылка (cta_url) или запрос места."""
    #: Для type=list: надпись кнопки, открывающей список, до 20 знаков, например «Выбрать»
    button: Optional[str]
    #: Для type=button: от 1 до 3 кнопок с разными id и надписями
    buttons: Optional[List[InteractiveReplyButton]]
    #: cta_url для type=cta_url, send_location для type=location_request_message
    name: Optional[Literal['cta_url', 'send_location']]
    #: Для type=cta_url: надпись и адрес кнопки
    parameters: Optional[CtaUrlParameters]
    #: Для type=list: разделы списка, до 10
    sections: Optional[List[InteractiveListSection]]


class _InteractiveContentRequired(TypedDict):
    #: Кнопки, список, ссылка или запрос места
    action: InteractiveAction
    #: Основной текст сообщения
    body: InteractiveText
    #: button: до 3 кнопок быстрого ответа; list: список до 10 строк; cta_url: кнопка-ссылка; location_request_message: кнопка «Отправить местоположение»
    type: Literal['button', 'list', 'cta_url', 'location_request_message']


class InteractiveContent(_InteractiveContentRequired, total=False):
    """Объект interactive Cloud API: button, list, cta_url или location_request_message."""
    #: Серая подпись внизу, до 60 знаков
    footer: Optional[InteractiveFooterText]
    #: Заголовок; у запроса места не передаётся
    header: Optional[InteractiveHeader]


class InteractiveFooterText(TypedDict):
    #: Серая подпись внизу, до 60 знаков, например «Цены в тенге»
    text: str


class _InteractiveHeaderRequired(TypedDict):
    #: Вид заголовка; нужно поле с тем же именем
    type: Literal['text', 'image', 'video', 'document']


class InteractiveHeader(_InteractiveHeaderRequired, total=False):
    """Заголовок над текстом: строка или файл. У списка только текстом."""
    #: Документ для type=document
    document: Optional[InteractiveMedia]
    #: Картинка для type=image
    image: Optional[InteractiveMedia]
    #: Текст заголовка для type=text, до 60 знаков
    text: Optional[str]
    #: Видео для type=video
    video: Optional[InteractiveMedia]


class _InteractiveListRowRequired(TypedDict):
    #: Ваш код строки, вернётся во входящем сообщении в interactive.id, например massage_60
    id: str
    #: Название строки, до 24 знаков
    title: str


class InteractiveListRow(_InteractiveListRowRequired, total=False):
    #: Пояснение под названием, до 72 знаков
    description: Optional[str]


class _InteractiveListSectionRequired(TypedDict):
    #: Строки раздела; во всех разделах вместе до 10
    rows: List[InteractiveListRow]


class InteractiveListSection(_InteractiveListSectionRequired, total=False):
    #: Название раздела до 24 знаков; обязательно, если разделов больше одного
    title: Optional[str]


class InteractiveMedia(TypedDict, total=False):
    """Файл: id из POST /media или публичная ссылка, ровно одно из двух."""
    #: Имя файла у клиента, только для документа, например price.pdf
    filename: Optional[str]
    #: media_id из POST /api/v2/external/media, например 1013859600285441
    id: Optional[str]
    #: Публичная ссылка https на файл, Meta скачает его сама, например https://example.kz/price.pdf
    link: Optional[str]


class InteractiveReply(TypedDict):
    #: Ваш код кнопки, вернётся во входящем сообщении в interactive.id, например confirm
    id: str
    #: Надпись на кнопке, до 20 знаков, например «Да, приду»
    title: str


class _InteractiveReplyButtonRequired(TypedDict):
    #: Код и надпись кнопки
    reply: InteractiveReply


class InteractiveReplyButton(_InteractiveReplyButtonRequired, total=False):
    #: Всегда reply: кнопка быстрого ответа
    type: Literal['reply']


class _InteractiveResponseOutRequired(TypedDict):
    #: Что вы задали кнопке при отправке. button_reply: reply.id кнопки, list_reply: id строки списка, button: payload кнопки шаблона (если payload не задан, WhatsApp присылает текст кнопки)
    id: str
    #: Что нажал клиент. button_reply: кнопка сообщения type=interactive (interactive.type=button), list_reply: пункт списка (interactive.type=list), button: быстрая кнопка шаблона (QUICK_REPLY), nfm_reply: отправленная форма WhatsApp Flow. В Telegram, Instagram и чате на сайте всегда button_reply
    type: str


class InteractiveResponseOut(_InteractiveResponseOutRequired, total=False):
    """Нажатие кнопки или выбор пункта списка клиентом."""
    #: Описание пункта списка (только list_reply, если оно было задано)
    description: Optional[str]
    #: Только у type=button: payload быстрой кнопки шаблона, то же значение, что в id. У остальных типов поля нет
    payload: Optional[str]
    #: Текст нажатой кнопки или пункта, как его видел клиент, например «Записаться»
    title: str


class InteractiveText(TypedDict):
    #: Основной текст: до 1024 знаков у кнопок, ссылки и запроса места, до 4096 у списка (type=list). Длиннее: 422
    text: str


class _LocationContentRequired(TypedDict):
    #: Широта, например 51.1282 (Астана)
    latitude: float
    #: Долгота, например 71.4304 (Астана)
    longitude: float


class LocationContent(_LocationContentRequired, total=False):
    """Точка на карте."""
    #: Адрес строкой, например «Астана, пр. Абая, 15»
    address: Optional[str]
    #: Название места, например «Салон Айгуль»
    name: Optional[str]


class MarkReadIn(TypedDict):
    #: wamid входящих сообщений, которые отметить прочитанными. wamid сообщения: из вебхука message.incoming или из списка сообщений переписки, например wamid.HBgLNzcwNzEyMzQ1Njc...
    message_ids: List[str]
    #: id номера WhatsApp, с которого работаете: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
    phone_number_id: str


class MediaContent(TypedDict, total=False):
    """Файл по ссылке или id из POST /media: ровно одно из двух, как в Cloud API."""
    #: Подпись под файлом, до 1024 знаков; у аудио и стикера не показывается
    caption: Optional[str]
    #: Имя файла у клиента, только для document, например schet_1024.pdf
    filename: Optional[str]
    #: media_id из POST /api/v2/external/media, например 1013859600285441
    id: Optional[str]
    #: Публичная ссылка https на файл, Meta скачает его сама
    link: Optional[str]


class MediaUploadForm(TypedDict):
    #: Файл формой multipart/form-data, поле file, до 100 МБ: картинка, видео, аудио, документ или стикер
    file: str


class MediaUploadOut(TypedDict):
    #: id файла в WhatsApp: передайте его в POST /api/v2/external/messages/send как image.id, document.id и т.д. Действует 30 дней
    media_id: str


class MessageContext(TypedDict):
    #: wamid сообщения, на которое отвечаете: из вебхука message.incoming или GET /api/v2/external/conversations/{id}/messages, например wamid.HBgLNzcwNzEyMzQ1Njc...
    message_id: str


class _MessageSenderOutRequired(TypedDict):
    #: Кто написал: contact (клиент), manager (сотрудник), workflow (сценарий), chatbot (бот или ИИ-ассистент), broadcast (рассылка), api (ваша программа через API или MCP), system (служебное)
    type: str


class MessageSenderOut(_MessageSenderOutRequired, total=False):
    #: id сотрудника у manager, как в GET /api/v2/external/team, например "7"
    id: Optional[str]
    #: Имя сотрудника, название сценария или бота
    name: Optional[str]
    #: Откуда отправлено: external_api (API), mcp, amocrm и другие интеграции; null из кабинета
    via: Optional[str]
    #: id сценария у workflow: тот же id, что в списке сценариев кабинета
    workflow_id: Optional[str]


class _MessageTemplateRefOutRequired(TypedDict):
    #: Имя шаблона, как в GET /api/v2/external/templates, например zapis_napominanie
    name: str


class MessageTemplateRefOut(_MessageTemplateRefOutRequired, total=False):
    """Какой шаблон WhatsApp отправлен: текст шаблона уже в поле text сообщения."""
    #: Язык шаблона: ru, kk, en или другой код WhatsApp
    language: Optional[str]
    #: Откуда отправлен шаблон, если не из чата: mcp, cliniccards_reminder и другие; иначе null
    source: Optional[str]
    #: Значения переменных {{1}}, {{2}} по порядку, например ["Айгуль", "20 октября"]; пустой список, если переменных нет или они не сохранились
    variables: List[str]


class _PhoneNumberListOutRequired(TypedDict):
    #: Номера аккаунта; отключённые не показываются
    data: List[PhoneNumberOut]


class PhoneNumberListOut(_PhoneNumberListOutRequired, total=False):
    #: total: сколько номеров в списке
    meta: Dict[str, Any]


class _PhoneNumberOutRequired(TypedDict):
    #: id номера: передавайте его в phone_number_id при отправке сообщений, загрузке файлов и работе с шаблонами, например 123456789012345
    phone_number_id: str
    #: Как подключён канал: whatsapp_business (WhatsApp Cloud API), evolution_api (старое подключение WhatsApp), telegram, instagram, olx, satu, email, webchat
    provider_type: str
    #: connected: можно отправлять; pending и connecting: подключение не завершено; disconnected, failed: не работает
    status: Literal['pending', 'connecting', 'connected', 'disconnected', 'failed']


class PhoneNumberOut(_PhoneNumberOutRequired, total=False):
    """Подключённый номер WhatsApp."""
    #: Канал: whatsapp, telegram, instagram, olx, satu (чат Satu.kz), email (почтовый ящик), webchat (чат на сайте). Отправить сообщение через POST /messages/send и шаблоны можно только у whatsapp
    channel: str
    #: Подтверждён ли номер кодом из SMS или звонка
    code_verification_status: Optional[Literal['VERIFIED', 'NOT_VERIFIED', 'EXPIRED']]
    #: Сам номер, как его видят клиенты, например +7 707 123 45 67
    display_phone_number: Optional[str]
    #: Качество номера по оценке Meta: GREEN хорошо, YELLOW внимание, RED риск блокировки
    quality_rating: Optional[Literal['GREEN', 'YELLOW', 'RED', 'UNKNOWN']]
    #: Имя компании в WhatsApp, одобренное Meta, например «Салон Айгуль»
    verified_name: Optional[str]


class _PipelineFieldOutRequired(TypedDict):
    #: id поля: ключ в custom_fields сделки, например 9c8b7a6d5e4f
    id: str
    #: Название поля, как в кабинете, например «Источник»
    name: str
    #: Тип значения: text и multiline (строка), number (число), money (целое в тиынах), select (строка из options), date (ГГГГ-ММ-ДД), checkbox (true или false)
    type: str


class PipelineFieldOut(_PipelineFieldOutRequired, total=False):
    #: Валюта денежного поля, например KZT; у других типов null
    currency: Optional[str]
    #: true: это поле суммы воронки, его значение и есть amount сделки
    is_amount: bool
    #: Допустимые значения для select, для других типов пусто
    options: List[str]
    #: Поле отмечено обязательным (звёздочка в кабинете). Само по себе перенос не запрещает: запрещает required_from_stage_id
    required: bool
    #: С какого этапа поле обязательно: stages[].id этой воронки. Перенос на этот этап и дальше (и на успешный этап) без значения: 422 required_fields; на этап отказа можно. null: перенос не проверяет это поле
    required_from_stage_id: Optional[str]


class _PipelineListOutRequired(TypedDict):
    #: Воронки на этой странице
    data: List[PipelineOut]


class PipelineListOut(_PipelineListOutRequired, total=False):
    #: true: есть ещё страницы, запросите их с cursor=next_cursor
    has_more: bool
    #: next_cursor для следующей страницы; null: это последняя страница
    next_cursor: Optional[str]


class _PipelineOutRequired(TypedDict):
    #: Свои поля сделок этой воронки: их id: ключи в custom_fields сделки
    custom_fields: List[PipelineFieldOut]
    #: id воронки: передавайте в pipeline_id сделки
    id: str
    #: Основная воронка аккаунта
    is_default: bool
    #: Название воронки, например «Продажи»
    name: str
    #: Этапы по порядку (sort)
    stages: List[PipelineStageOut]


class PipelineOut(_PipelineOutRequired, total=False):
    #: Когда создана. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    created_at: Optional[str]
    #: Когда изменена. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    updated_at: Optional[str]


class _PipelineStageOutRequired(TypedDict):
    #: Цвет этапа в кабинете, HEX, например #3B82F6
    color: str
    #: id этапа: его передают в stage_id сделки и в POST /deals/{deal_id}/move
    id: str
    #: Название этапа, как в кабинете, например «Переговоры»
    name: str
    #: Порядок этапа в воронке, по возрастанию, с 0
    sort: int


class PipelineStageOut(_PipelineStageOutRequired, total=False):
    #: Этап «Закрыто и не реализовано»: перенос сюда закрывает сделку как проигранную
    is_lost: bool
    #: Этап «Успешно реализовано»: перенос сюда закрывает сделку как выигранную
    is_won: bool


class ReactionIn(TypedDict):
    #: Один эмодзи, например 👍. Пустая строка снимает реакцию
    emoji: str
    #: На какое сообщение реакция. wamid сообщения: из вебхука message.incoming или из списка сообщений переписки, например wamid.HBgLNzcwNzEyMzQ1Njc...
    message_id: str
    #: id номера WhatsApp, с которого работаете: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
    phone_number_id: str
    #: Номер клиента, которому принадлежит сообщение: цифры с кодом страны, плюс в начале можно, например 77071234567. Уходит в Meta как есть: без пробелов, 8 в начале на 7 не заменяется
    to: str


class _ReactionOutRequired(TypedDict):
    #: accepted: WhatsApp принял реакцию
    status: str


class ReactionOut(_ReactionOutRequired, total=False):
    #: wamid сообщения-реакции
    message_id: Optional[str]


class _RegisterPhoneNumberInRequired(TypedDict):
    #: Название подключения в кабинете, видно только вам, например «Отдел продаж»
    display_name: str


class RegisterPhoneNumberIn(_RegisterPhoneNumberInRequired, total=False):
    #: Номер, который подключаете, в международном формате, например +77071234567
    phone_e164: Optional[str]


class _RegisterPhoneNumberOutRequired(TypedDict):
    #: id номера: передавайте его в phone_number_id при отправке сообщений, загрузке файлов и работе с шаблонами, например 123456789012345
    phone_number_id: str
    #: Как подключён канал: whatsapp_business (WhatsApp Cloud API), evolution_api (старое подключение WhatsApp), telegram, instagram, olx, satu, email, webchat
    provider_type: str
    #: connected: можно отправлять; pending и connecting: подключение не завершено; disconnected, failed: не работает
    status: Literal['pending', 'connecting', 'connected', 'disconnected', 'failed']


class RegisterPhoneNumberOut(_RegisterPhoneNumberOutRequired, total=False):
    #: Канал: whatsapp, telegram, instagram, olx, satu (чат Satu.kz), email (почтовый ящик), webchat (чат на сайте). Отправить сообщение через POST /messages/send и шаблоны можно только у whatsapp
    channel: str
    #: Подтверждён ли номер кодом из SMS или звонка
    code_verification_status: Optional[Literal['VERIFIED', 'NOT_VERIFIED', 'EXPIRED']]
    #: Сам номер, как его видят клиенты, например +7 707 123 45 67
    display_phone_number: Optional[str]
    #: Ссылка на подключение номера в Meta (Embedded Signup): откройте её во всплывающем окне, владелец номера войдёт в Facebook и подтвердит номер. Пусто, если подтверждение не нужно
    embedded_signup_url: Optional[str]
    #: Качество номера по оценке Meta: GREEN хорошо, YELLOW внимание, RED риск блокировки
    quality_rating: Optional[Literal['GREEN', 'YELLOW', 'RED', 'UNKNOWN']]
    #: Имя компании в WhatsApp, одобренное Meta, например «Салон Айгуль»
    verified_name: Optional[str]


class _SendMessageInRequired(TypedDict):
    #: id номера WhatsApp, с которого работаете: поле phone_number_id из GET /api/v2/external/phone-numbers, например 123456789012345
    phone_number_id: str
    #: Номер клиента: цифры с кодом страны, плюс в начале можно: 77071234567 или +77071234567. Пробелы, скобки и дефисы не принимаются (422 VALIDATION_ERROR). 8 в начале на 7 НЕ заменяется: 87071234567 уйдёт в Meta как номер с кодом страны 8 и не дойдёт, пишите 77071234567
    to: str
    #: Вид сообщения; рядом нужен блок с тем же именем, например type=text и text={...}
    type: Literal['text', 'image', 'video', 'audio', 'document', 'template', 'interactive', 'location', 'contacts', 'sticker']


class SendMessageIn(_SendMessageInRequired, total=False):
    """Сообщение в форме Cloud API: заполните ровно один блок с именем из type."""
    #: Для type=audio: MP3, M4A, AAC или OGG до 16 МБ; голосовое OGG/OPUS только по id
    audio: Optional[MediaContent]
    #: Для type=contacts: одна или несколько карточек
    contacts: Optional[List[ContactCard]]
    #: Ответ на сообщение клиента: цитата над пузырём. С шаблоном не передаётся
    context: Optional[MessageContext]
    #: Для type=document: PDF, Word, Excel и другие до 100 МБ
    document: Optional[MediaContent]
    #: Для type=image: JPG или PNG до 5 МБ
    image: Optional[MediaContent]
    #: Для type=interactive: кнопки, список, кнопка-ссылка или запрос местоположения
    interactive: Optional[InteractiveContent]
    #: Для type=location: точка на карте
    location: Optional[LocationContent]
    #: Для type=sticker: WEBP 512×512, до 100 КБ (анимированный до 500 КБ)
    sticker: Optional[MediaContent]
    #: Для type=template: одобренный шаблон; единственный вид, который можно отправить вне окна 24 часа
    template: Optional[TemplateMessageIn]
    #: Для type=text
    text: Optional[TextContent]
    #: Для type=video: MP4 или 3GP до 16 МБ
    video: Optional[MediaContent]


class _SendMessageOutRequired(TypedDict):
    #: id сообщения (wamid): по нему вебхук message.status сообщит о доставке и прочтении
    message_id: str


class SendMessageOut(_SendMessageOutRequired, total=False):
    #: id сообщения у WhatsApp; для номеров Cloud API совпадает с message_id
    provider_message_id: Optional[str]
    #: accepted: WhatsApp принял сообщение; дальнейшие статусы приходят вебхуком message.status
    status: Literal['accepted', 'sent', 'delivered', 'read', 'failed']


class _SetConversationStatusInRequired(TypedDict):
    #: Новый статус. Статус диалога: open (открыт, менеджеру нужно ответить), pending (ожидает: ответ дан, ждём клиента или другой отдел), snoozed (отложен до snoozed_until), resolved (решён, закрыт). Новое сообщение клиента снова открывает решённый и отложенный диалог
    status: Literal['open', 'pending', 'snoozed', 'resolved']


class SetConversationStatusIn(_SetConversationStatusInRequired, total=False):
    #: До какого времени отложить, ISO 8601 с часовым поясом, например 2026-10-20T09:00:00+05:00. Если передано, статус становится snoozed
    snoozed_until: Optional[str]


class SetLabelsIn(TypedDict):
    #: Все метки диалога после изменения, до 100, например ["VIP", "доставка"]. Список заменяет прежний целиком: чтобы добавить метку, передайте старые и новую. [] убирает все. Повторы и пустые строки отбрасываются
    labels: List[str]


class _StaffRefOutRequired(TypedDict):
    #: id сотрудника строкой, как в GET /api/v2/external/team, например "7"
    id: str


class StaffRefOut(_StaffRefOutRequired, total=False):
    #: Имя сотрудника, например Ерлан; null, если не заполнено
    name: Optional[str]


class SuccessOut(TypedDict):
    #: true: действие выполнено
    success: bool


class _TaskCreateInRequired(TypedDict):
    #: Срок в ISO 8601. Лучше в UTC с Z: Казахстан живёт по UTC+5, поэтому «завтра в 10:00 по Астане» = 05:00Z, например 2026-10-19T05:00:00Z. Можно с поясом: 2026-10-19T10:00:00+05:00. Время без пояса считается UTC
    due_at: str
    #: Что сделать, 1–300 знаков
    title: str


class TaskCreateIn(_TaskCreateInRequired, total=False):
    #: Подробности, до 5000 знаков
    description: str
    #: Исполнитель: id сотрудника строкой: поле id из GET /team, например "12". Не передали: ответственный сделки
    responsible_user_id: Optional[str]
    #: Тип задачи: системные call (звонок), meeting (встреча), email (письмо), task (дело) или ключ своего типа вида c_6713d0a1b2c3. Списка своих типов в API нет: их заводят и видят в кабинете, «Настройки задач», а ключ виден в task_type задач этого типа (GET /deals/{deal_id}/tasks). Неизвестный или скрытый тип: 400 BAD_REQUEST
    task_type: str


class _TaskListOutRequired(TypedDict):
    #: Задачи на этой странице
    data: List[TaskOut]


class TaskListOut(_TaskListOutRequired, total=False):
    #: true: есть ещё страницы, запросите их с cursor=next_cursor
    has_more: bool
    #: next_cursor для следующей страницы; null: это последняя страница
    next_cursor: Optional[str]


class _TaskOutRequired(TypedDict):
    #: id задачи: нужен для PATCH /tasks/{task_id}
    id: str
    #: open: в работе, done: выполнена, cancelled: отменена в кабинете
    status: Literal['open', 'done', 'cancelled']
    #: Что сделать, например «Перезвонить Айгуль по замеру»
    title: str


class TaskOut(_TaskOutRequired, total=False):
    #: Когда выполнена. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    completed_at: Optional[str]
    #: Когда создана. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    created_at: Optional[str]
    #: Сделка, к которой относится задача
    deal_id: Optional[str]
    #: Подробности задачи
    description: str
    #: true: задача выполнена
    done: bool
    #: Срок. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z (10:00 по Астане = 05:00Z)
    due_at: Optional[str]
    #: Исполнитель: id сотрудника строкой: поле id из GET /team, например "12"
    responsible_user_id: Optional[str]
    #: Тип задачи: системные call (звонок), meeting (встреча), email (письмо), task (дело) или ключ своего типа вида c_6713d0a1b2c3. Списка своих типов в API нет: их заводят и видят в кабинете, «Настройки задач», а ключ виден в task_type задач этого типа (GET /deals/{deal_id}/tasks). Неизвестный или скрытый тип: 400 BAD_REQUEST
    task_type: str
    #: Когда изменена. Время ISO 8601 в UTC с Z, например 2026-10-18T06:30:00Z
    updated_at: Optional[str]


class TaskUpdateIn(TypedDict, total=False):
    #: true: отметить выполненной (как кнопка «Выполнено»), false: вернуть в работу
    done: Optional[bool]
    #: Новый срок. Срок в ISO 8601. Лучше в UTC с Z: Казахстан живёт по UTC+5, поэтому «завтра в 10:00 по Астане» = 05:00Z, например 2026-10-19T05:00:00Z. Можно с поясом: 2026-10-19T10:00:00+05:00. Время без пояса считается UTC
    due_at: Optional[str]
    #: Новый исполнитель: id сотрудника строкой: поле id из GET /team, например "12"
    responsible_user_id: Optional[str]
    #: Новое название, 1–300 знаков
    title: Optional[str]


class _TeamListOutRequired(TypedDict):
    #: Сотрудники страницы: первым владелец аккаунта
    data: List[TeamMemberOut]


class TeamListOut(_TeamListOutRequired, total=False):
    #: true: есть следующая страница, запросите её с next_cursor
    has_more: bool
    #: Курсор следующей страницы: передайте его в параметр cursor. null на последней странице
    next_cursor: Optional[str]


class _TeamMemberOutRequired(TypedDict):
    #: id сотрудника строкой, например "7": его передают в user_id метода POST /conversations/{conversation_id}/assign и в mention_user_ids заметки
    id: str
    #: false: сотрудник отключён: назначить на него диалог (409 CONFLICT), сделку или задачу (422 responsible_user_not_found) нельзя
    is_active: bool
    #: Роль. owner приходит строчными буквами, остальные заглавными: так исторически, значения не изменятся, сравнивайте строки как есть. owner (владелец аккаунта), ADMIN (управляет командой, видит всё), AGENT (менеджер: чаты, контакты, сделки), VIEWER (только просмотр, назначить диалог на него нельзя)
    role: Literal['owner', 'ADMIN', 'AGENT', 'VIEWER']


class TeamMemberOut(_TeamMemberOutRequired, total=False):
    #: Имя сотрудника в Wazzapo, например Ерлан; null, если не заполнено
    name: Optional[str]
    #: Номера WhatsApp (phone_number_id из GET /api/v2/external/phone-numbers), в которых сотрудник работает; null: все номера аккаунта
    phone_number_ids: Optional[List[str]]


class _TemplateBodyRequired(TypedDict):
    #: BODY: основной текст, обязателен и только один
    type: Literal['BODY']


class TemplateBody(_TemplateBodyRequired, total=False):
    #: Только AUTHENTICATION: добавить «Не сообщайте этот код никому»
    add_security_recommendation: Optional[bool]
    #: Примеры значений переменных: обязательны, если в text есть {{1}}
    example: Optional[TemplateBodyExample]
    #: Текст до 1024 символов с переменными {{1}}, {{2}} по порядку. Переменная не может стоять в самом начале или в самом конце текста: Meta отклонит шаблон. Для AUTHENTICATION не передаётся: текст задаёт Meta
    text: Optional[str]


class TemplateBodyExample(TypedDict):
    """Примеры значений переменных текста."""
    #: Один список значений по порядку переменных: для «{{1}}, ваша запись {{2}}» это [["Айгуль", "20 октября в 15:00"]]
    body_text: List[List[str]]


class TemplateButtonCopyCode(TypedDict):
    #: Пример кода до 15 символов, например OSEN25
    example: str
    #: COPY_CODE: копирует промокод (рекламные шаблоны), не больше 1. Надпись задаёт WhatsApp
    type: Literal['COPY_CODE']


class _TemplateButtonOtherRequired(TypedDict):
    #: Тип кнопки Meta, кроме перечисленных выше: FLOW, CATALOG, MPM, SPM, VOICE_CALL или ORDER_DETAILS. Другой тип (например, опечатка QUICK_REPLAY): 422
    type: str


class TemplateButtonOther(_TemplateButtonOtherRequired, total=False):
    """Другие кнопки Meta (FLOW, CATALOG, MPM, SPM, VOICE_CALL, ORDER_DETAILS) передаются в Meta как есть."""
    #: Надпись на кнопке до 25 символов
    text: Optional[str]


class _TemplateButtonOtpRequired(TypedDict):
    #: COPY_CODE: «Копировать код», работает везде. ONE_TAP и ZERO_TAP: код сам подставляется в ваше Android-приложение, нужны supported_apps
    otp_type: Literal['COPY_CODE', 'ONE_TAP', 'ZERO_TAP']
    #: OTP: кнопка кода подтверждения, только для AUTHENTICATION и одна
    type: Literal['OTP']


class TemplateButtonOtp(_TemplateButtonOtpRequired, total=False):
    #: ONE_TAP: надпись кнопки автозаполнения
    autofill_text: Optional[str]
    #: ONE_TAP и ZERO_TAP: ваши Android-приложения, до 5
    supported_apps: Optional[List[TemplateOtpApp]]
    #: Надпись «Копировать код» по-своему, до 25 символов
    text: Optional[str]
    #: ZERO_TAP: согласие с условиями Meta, true
    zero_tap_terms_accepted: Optional[bool]


class TemplateButtonPhoneNumber(TypedDict):
    #: Номер с кодом страны до 20 символов, например +77071234567
    phone_number: str
    #: Надпись на кнопке до 25 символов, например «Позвонить»
    text: str
    #: PHONE_NUMBER: звонок по номеру, не больше 1
    type: Literal['PHONE_NUMBER']


class TemplateButtonQuickReply(TypedDict):
    #: Надпись на кнопке до 25 символов, например «Подтверждаю»
    text: str
    #: QUICK_REPLY: ответ одним нажатием, до 10 штук
    type: Literal['QUICK_REPLY']


class _TemplateButtonUrlRequired(TypedDict):
    #: Надпись на кнопке до 25 символов, например «Открыть каталог»
    text: str
    #: URL: открывает сайт, не больше 2 в шаблоне
    type: Literal['URL']
    #: Адрес https до 2000 символов; переменная {{1}} только в конце, например https://shop.kz/order/{{1}}
    url: str


class TemplateButtonUrl(_TemplateButtonUrlRequired, total=False):
    #: Если в url есть {{1}}: полный пример адреса, например ["https://shop.kz/order/1024"]
    example: Optional[List[str]]


class TemplateButtons(TypedDict):
    #: До 10 кнопок: QUICK_REPLY до 10, URL до 2, PHONE_NUMBER и COPY_CODE по 1. Кнопки QUICK_REPLY ставьте подряд, не вперемешку с другими. Для AUTHENTICATION одна кнопка OTP
    buttons: List[Union[Union[TemplateButtonQuickReply, TemplateButtonUrl, TemplateButtonPhoneNumber, TemplateButtonCopyCode, TemplateButtonOtp], TemplateButtonOther]]
    #: BUTTONS: блок кнопок под сообщением, не больше одного
    type: Literal['BUTTONS']


class _TemplateComponentInRequired(TypedDict):
    #: header: шапка, body: основной текст, button: кнопка (нужны sub_type и index)
    type: Literal['header', 'body', 'footer', 'button']


class TemplateComponentIn(_TemplateComponentInRequired, total=False):
    """Часть шаблона, в которую подставляются значения: шапка, текст или кнопка."""
    #: Только для type=button: номер кнопки в шаблоне, считая с 0 (от 0 до 9)
    index: Optional[int]
    #: Значения переменных по порядку: первое вместо {{1}}, второе вместо {{2}}
    parameters: List[TemplateParameter]
    #: Только для type=button: quick_reply (быстрый ответ), url (кнопка-ссылка), copy_code (промокод)
    sub_type: Optional[str]


class TemplateCurrency(TypedDict):
    #: Сумма в тенге, умноженная на 1000 (так требует Meta): 150 000 ₸ = 150000000, 15 000 ₸ = 15000000. Внимание: в сделках (POST /deals, amount) та же сумма в тиынах, то есть × 100: 150 000 ₸ = 15000000. Не путайте, иначе клиент увидит сумму в 10 раз меньше
    amount_1000: int
    #: Код валюты ISO 4217 заглавными буквами: KZT, RUB, USD
    code: str
    #: Сумма текстом, её увидит клиент, если телефон не сможет показать формат, например «150 000 ₸»
    fallback_value: str


class TemplateDateTime(TypedDict):
    #: Дата и время текстом, как их увидит клиент, например «25 октября, 15:00»
    fallback_value: str


class _TemplateFooterRequired(TypedDict):
    #: FOOTER: строка мелким шрифтом под текстом
    type: Literal['FOOTER']


class TemplateFooter(_TemplateFooterRequired, total=False):
    #: Только AUTHENTICATION: срок действия кода в минутах, от 1 до 90
    code_expiration_minutes: Optional[int]
    #: Подпись до 60 символов без переменных, например «Wazzapo, Астана»
    text: Optional[str]


class TemplateHeaderLocation(TypedDict):
    #: LOCATION: карта с точкой, координаты передаются при отправке. Примера не нужно
    format: Literal['LOCATION']
    #: HEADER: шапка над текстом, не больше одной
    type: Literal['HEADER']


class _TemplateHeaderMediaRequired(TypedDict):
    #: IMAGE: картинка, VIDEO: видео, DOCUMENT: файл PDF. Сам файл передаётся при отправке
    format: Literal['IMAGE', 'VIDEO', 'DOCUMENT']
    #: HEADER: шапка над текстом, не больше одной
    type: Literal['HEADER']


class TemplateHeaderMedia(_TemplateHeaderMediaRequired, total=False):
    #: Образец файла для модерации: обязателен, проще всего media_url
    example: Optional[TemplateMediaExample]


class _TemplateHeaderTextRequired(TypedDict):
    #: TEXT: шапка текстом
    format: Literal['TEXT']
    #: Текст шапки до 60 символов, можно одну переменную {{1}}, например «Запись на {{1}}»
    text: str
    #: HEADER: шапка над текстом, не больше одной
    type: Literal['HEADER']


class TemplateHeaderText(_TemplateHeaderTextRequired, total=False):
    #: Пример для {{1}}: обязателен, если в text есть переменная
    example: Optional[TemplateHeaderTextExample]


class TemplateHeaderTextExample(TypedDict):
    """Пример значения переменной {{1}} в текстовой шапке."""
    #: Ровно одно значение для {{1}} в шапке, например ["Айгуль"]
    header_text: List[str]


class TemplateLanguage(TypedDict):
    #: Язык шаблона, как в GET /api/v2/external/templates (поле language): ru, kk, en_US. Шаблон в Meta определяется парой имя + язык
    code: str


class _TemplateListOutRequired(TypedDict):
    #: Шаблоны на этой странице
    data: List[TemplateOut]


class TemplateListOut(_TemplateListOutRequired, total=False):
    #: true, если есть следующая страница
    has_more: bool
    #: total: всего шаблонов с учётом фильтров
    meta: Dict[str, Any]
    #: Передайте в cursor, чтобы получить следующую страницу
    next_cursor: Optional[str]


class TemplateMedia(TypedDict, total=False):
    """Файл шапки шаблона: id из POST /media или публичная ссылка, ровно одно из двух."""
    #: Имя файла у клиента, только для документа, например price.pdf
    filename: Optional[str]
    #: media_id из POST /api/v2/external/media, например 1013859600285441
    id: Optional[str]
    #: Публичная ссылка https на файл, Meta скачает его сама, например https://example.kz/price.pdf
    link: Optional[str]


class TemplateMediaExample(TypedDict, total=False):
    """Образец файла шапки: Meta проверяет шаблон вместе с ним."""
    #: Уже загруженный в Meta образец (Resumable Upload API), если вы загрузили его сами
    header_handle: Optional[List[str]]
    #: Ссылка https на образец файла, например https://example.kz/promo.jpg. Wazzapo скачает файл и загрузит его в Meta сам. Картинка JPG/PNG до 5 МБ, видео MP4 до 16 МБ, документ PDF до 100 МБ
    media_url: Optional[str]


class _TemplateMessageInRequired(TypedDict):
    #: Язык шаблона
    language: TemplateLanguage
    #: Имя одобренного шаблона из GET /api/v2/external/templates (поле name, статус APPROVED): латиница в нижнем регистре, цифры и _, до 512 символов, например zapis_napominanie. Нет одобренного шаблона с таким именем и языком: 422 template_not_found
    name: str


class TemplateMessageIn(_TemplateMessageInRequired, total=False):
    """Одобренный Meta шаблон и значения его переменных."""
    #: Значения переменных. Шаблону без переменных и без файла в шапке не нужны. Если в шапке картинка, видео или документ, передайте файл в каждой отправке
    components: List[TemplateComponentIn]


class TemplateOtpApp(TypedDict):
    #: Имя пакета Android-приложения, например kz.shop.app
    package_name: str
    #: Хеш ключа подписи приложения (11 символов), например K8a/AINcGX7
    signature_hash: str


class _TemplateOutRequired(TypedDict):
    #: Категория, от неё зависит цена сообщения в Meta
    category: Literal['MARKETING', 'UTILITY', 'AUTHENTICATION']
    #: Код языка, его передают в messages.send как template.language.code
    language: str
    #: Имя шаблона, его передают в messages.send как template.name
    name: str
    #: PENDING: на проверке. APPROVED: можно отправлять. REJECTED: отклонён, причина в rejected_reason. PAUSED: Meta приостановила из-за жалоб. DISABLED: отключён
    status: Literal['PENDING', 'APPROVED', 'REJECTED', 'DISABLED', 'PAUSED']
    #: id шаблона в Meta, например 1252715608684590: для get, update, delete
    template_id: str


class TemplateOut(_TemplateOutRequired, total=False):
    """Шаблон и его статус проверки в Meta."""
    #: Кнопки шаблона, те же, что в части BUTTONS
    buttons: Optional[List[Union[Union[TemplateButtonQuickReply, TemplateButtonUrl, TemplateButtonPhoneNumber, TemplateButtonCopyCode, TemplateButtonOtp], TemplateButtonOther]]]
    #: Части шаблона в том же виде, что при создании. Пусто, если содержимое неизвестно
    components: Optional[List[Union[TemplateHeaderText, TemplateHeaderMedia, TemplateHeaderLocation, TemplateBody, TemplateFooter, TemplateButtons]]]
    #: Когда шаблон появился в Wazzapo, UTC
    created_at: Optional[str]
    #: Вид шапки: при отправке для IMAGE, VIDEO, DOCUMENT нужен файл, для LOCATION координаты
    header_format: Optional[Literal['TEXT', 'IMAGE', 'VIDEO', 'DOCUMENT', 'LOCATION']]
    #: Качество по оценке Meta: при LOW шаблон могут приостановить
    quality_score: Optional[Literal['HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']]
    #: Причина отказа Meta, если status=REJECTED
    rejected_reason: Optional[str]
    #: Когда шаблон последний раз менялся, UTC
    updated_at: Optional[str]
    #: Сколько переменных {{n}} в тексте и шапке: столько значений передать при отправке
    variables_count: Optional[int]


class TemplateParameter(TypedDict, total=False):
    """Значение одной переменной шаблона. Поле с именем из type обязательно."""
    #: Для type=coupon_code: промокод, который клиент скопирует кнопкой, до 20 знаков
    coupon_code: Optional[str]
    #: Сумма для type=currency
    currency: Optional[TemplateCurrency]
    #: Дата для type=date_time
    date_time: Optional[TemplateDateTime]
    #: Документ шапки для type=document: PDF до 100 МБ, filename задаёт имя файла у клиента
    document: Optional[TemplateMedia]
    #: Картинка шапки для type=image: JPG или PNG до 5 МБ
    image: Optional[TemplateMedia]
    #: Место в шапке для type=location
    location: Optional[LocationContent]
    #: Имя переменной для шаблонов с именованными переменными {{name}}, например first_name. Для нумерованных {{1}}, {{2}} не передавайте: значения идут по порядку
    parameter_name: Optional[str]
    #: Для type=payload в кнопке быстрого ответа: строка, которая вернётся вам во входящем сообщении, когда клиент нажмёт кнопку
    payload: Optional[str]
    #: Значение для type=text: подставится вместо {{1}} или {{name}}, в кнопке-ссылке окончание адреса
    text: Optional[str]
    #: Вид значения. В тексте и заголовке: text, currency, date_time. В шапке с файлом: image, video, document, location. В кнопке: payload (быстрый ответ), text (окончание ссылки), coupon_code (кнопка «Скопировать код»)
    type: Literal['text', 'currency', 'date_time', 'image', 'video', 'document', 'location', 'payload', 'coupon_code']
    #: Видео шапки для type=video: MP4 до 16 МБ
    video: Optional[TemplateMedia]


class _TextContentRequired(TypedDict):
    #: Текст сообщения, до 4096 знаков; *жирный*, _курсив_
    body: str


class TextContent(_TextContentRequired, total=False):
    #: Показать превью первой ссылки в тексте
    preview_url: Optional[bool]


class UpdateTemplateIn(TypedDict, total=False):
    """Правка шаблона в Meta: компоненты заменяются целиком, имя и язык не меняются."""
    #: Новая категория: только у отклонённого или приостановленного шаблона. UTILITY: служебное по заказу или записи клиента (подтверждение, напоминание, статус), дешевле рекламного. MARKETING: реклама, акции, скидки, приглашения. AUTHENTICATION: код подтверждения входа. Meta сама переносит в MARKETING служебный шаблон с рекламой, об этом придёт событие template.category_changed
    category: Optional[Literal['MARKETING', 'UTILITY', 'AUTHENTICATION']]
    #: Все части шаблона заново: Meta заменяет их целиком, по одной части не правится. Части шаблона: BODY обязателен, HEADER, FOOTER и BUTTONS по желанию, каждая не больше одной. Вид части выбирается полем type, у шапки ещё полем format
    components: Optional[List[Union[TemplateHeaderText, TemplateHeaderMedia, TemplateHeaderLocation, TemplateBody, TemplateFooter, TemplateButtons]]]


class WebhookCardName(TypedDict, total=False):
    #: Имя, если WhatsApp его прислал
    first_name: Optional[str]
    #: Имя в карточке, например «Ерлан Сапаров»
    formatted_name: str
    #: Фамилия, если WhatsApp её прислал
    last_name: Optional[str]


class WebhookCardPhone(TypedDict, total=False):
    #: Номер, как он записан в карточке, например +7 707 123 45 67
    phone: Optional[str]
    #: Вид номера: CELL, MAIN, HOME, WORK
    type: Optional[str]
    #: Номер WhatsApp цифрами, если он есть в WhatsApp
    wa_id: Optional[str]


class _WebhookContactRequired(TypedDict):
    #: id контакта, как в GET /api/v2/external/contacts
    id: str


class WebhookContact(_WebhookContactRequired, total=False):
    #: Категория контакта
    category: Optional[str]
    #: Компания
    company: Optional[str]
    #: Создан, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    created_at: Optional[str]
    #: Дополнительные поля: ключ и значение
    custom_fields: Dict[str, Any]
    #: Почта
    email: Optional[str]
    #: true: контакт заблокирован
    is_blocked: bool
    #: Имя, например Айгуль
    name: Optional[str]
    #: Заметки в карточке
    notes: Optional[str]
    #: Телефон цифрами без +, например 77071234567
    phone: Optional[str]
    #: Должность
    position: Optional[str]
    #: Откуда контакт: whatsapp, manual, api, import и другие
    source: Optional[str]
    #: Теги, например ["vip"]
    tags: List[str]
    #: Изменён, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    updated_at: Optional[str]


class _WebhookContactCardRequired(TypedDict):
    #: Имя в карточке
    name: WebhookCardName


class WebhookContactCard(_WebhookContactCardRequired, total=False):
    """Карточка контакта, присланная клиентом. Из WhatsApp приходит как у Meta (могут быть emails, org)."""
    #: Номера из карточки (WhatsApp)
    phones: Optional[List[WebhookCardPhone]]
    #: Карточка в формате vCard (другие каналы)
    vcard: Optional[str]


class _WebhookContactCreatedRequired(TypedDict):
    #: Карточка контакта
    contact: WebhookContact
    #: contact.created
    event: str


class WebhookContactCreated(_WebhookContactCreatedRequired, total=False):
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email; null, если создан вручную или через API
    channel: Optional[str]
    #: id номера WhatsApp, как phone_number_id в GET /api/v2/external/phone-numbers; null у других каналов
    phone_number_id: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id; null, если не из сообщения
    session_id: Optional[str]
    #: Когда создан, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class WebhookContactRef(TypedDict, total=False):
    #: Только у каналов без телефона: id чата Telegram, почта, id в Instagram или OLX. У WhatsApp поля нет
    external_id: Optional[str]
    #: id контакта Wazzapo, как в GET /api/v2/external/contacts; null у участника группы
    id: Optional[str]
    #: Имя клиента, например Айгуль; null, если неизвестно
    name: Optional[str]
    #: Телефон цифрами с кодом страны без +, например 77071234567. Есть у WhatsApp и чата на сайте, у других каналов null (адрес в external_id)
    phone: Optional[str]


class _WebhookContactUpdatedRequired(TypedDict):
    #: Кто изменил: manager, workflow, api или system
    changed_by: WebhookPerson
    #: Что поменялось
    changes: List[WebhookFieldChange]
    #: Карточка после правки
    contact: WebhookContact
    #: contact.updated
    event: str


class WebhookContactUpdated(_WebhookContactUpdatedRequired, total=False):
    #: Когда изменён, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookConversationAssignedRequired(TypedDict):
    #: Кто назначил: сотрудник, сценарий или система
    assigned_by: WebhookPerson
    #: Клиент диалога; в группе участник, который написал
    contact: WebhookContactRef
    #: Имя события, как поле event оболочки
    event: str


class WebhookConversationAssigned(_WebhookConversationAssignedRequired, total=False):
    #: Новый ответственный; null, если назначение сняли
    assignee: Optional[WebhookPerson]
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
    channel: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Прежний ответственный; null, если не было
    previous_assignee: Optional[WebhookPerson]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id
    session_id: Optional[str]
    #: Когда произошло событие, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookConversationStatusChangedRequired(TypedDict):
    #: Кто сменил: сотрудник, сценарий или система
    changed_by: WebhookPerson
    #: Клиент диалога; в группе участник, который написал
    contact: WebhookContactRef
    #: Имя события, как поле event оболочки
    event: str


class WebhookConversationStatusChanged(_WebhookConversationStatusChangedRequired, total=False):
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
    channel: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Новый статус: open, pending, snoozed, resolved
    new_status: Optional[str]
    #: Прежний статус: open, pending, snoozed, resolved
    old_status: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id
    session_id: Optional[str]
    #: Когда произошло событие, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookCreateInRequired(TypedDict):
    #: На какие события подписаться, хотя бы одно; список с описаниями: GET /webhook-event-types. Сейчас: message.incoming, message.outgoing, message.status, conversation.assigned, conversation.status_changed, conversation.note_added, session.connected, session.disconnected, deal.stage_changed, deal.closed, deal.created, deal.changed, contact.created, contact.updated, template.status_updated, template.quality_changed, template.category_changed, invoice.status_changed, task.created
    event_types: List[Literal['message.incoming', 'message.outgoing', 'message.status', 'conversation.assigned', 'conversation.status_changed', 'conversation.note_added', 'session.connected', 'session.disconnected', 'deal.stage_changed', 'deal.closed', 'deal.created', 'deal.changed', 'contact.created', 'contact.updated', 'template.status_updated', 'template.quality_changed', 'template.category_changed', 'invoice.status_changed', 'task.created']]
    #: Адрес вашего сервера, куда Wazzapo отправляет события запросом POST: только https:// и только публичный адрес (localhost и внутренние сети нельзя), до 2048 символов. Пример: https://crm.example.kz/hooks/wazzapo
    url: str


class WebhookCreateIn(_WebhookCreateInRequired, total=False):
    #: Подпись для себя, чтобы отличать приёмники, например «CRM: заявки». До 100 символов
    description: Optional[str]


class _WebhookDealRequired(TypedDict):
    #: Клиент сделки
    contact: WebhookDealContact
    #: id сделки, как в GET /api/v2/external/deals
    id: str
    #: Воронка сделки {id, name}; id тот же, что pipeline_id
    pipeline: WebhookPipelineRef
    #: open (в работе), won (выиграна), lost (проиграна)
    status: str


class WebhookDeal(_WebhookDealRequired, total=False):
    #: Сумма сделки в тиынах, как amount в GET /api/v2/external/deals: 1 ₸ = 100 тиынов, 300 000 ₸ = 30000000
    amount: int
    #: Ответственный {id, name, email}, id числом; null, если нет. Тот же сотрудник строкой: responsible_user_id
    assignee: Optional[WebhookPerson]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Создана, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    created_at: Optional[str]
    #: Валюта суммы, как currency в REST, обычно KZT
    currency: Optional[str]
    #: id сделки в вашей системе, как external_id в REST (если передавали в POST /deals)
    external_id: Optional[str]
    #: Проиграна, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z; иначе null
    lost_at: Optional[str]
    #: Причина отказа текстом у проигранной
    lost_reason: Optional[str]
    #: id причины отказа из настроек воронки
    lost_reason_id: Optional[str]
    #: Номер сделки в кабинете, например 152
    number: Optional[int]
    #: Сколько оплачено, в тенге
    paid_amount: Optional[float]
    #: id воронки, как pipeline_id в REST (GET /api/v2/external/pipelines)
    pipeline_id: Optional[str]
    #: Ответственный, как responsible_user_id в REST: id из GET /api/v2/external/team строкой, например "12"; null, если нет
    responsible_user_id: Optional[str]
    #: Откуда сделка, то же значение, что source в REST: api (через API), manual (вручную в кабинете), rule (правилом по входящему), amocrm, form, канал (whatsapp, instagram, telegram, webchat, email, olx); null, если неизвестно
    source: Optional[str]
    #: Текущий этап {id, name, is_won, is_lost}; id тот же, что stage_id
    stage: Optional[WebhookStage]
    #: id текущего этапа, как stage_id в REST (stages[].id воронки)
    stage_id: Optional[str]
    #: Название сделки
    title: Optional[str]
    #: Изменена, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    updated_at: Optional[str]
    #: Сумма в целых тенге (не тиыны), например 300000: оставлено для совместимости; используйте amount в тиынах, как в REST
    value: Optional[float]
    #: Выиграна, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z; иначе null
    won_at: Optional[str]


class _WebhookDealChangedRequired(TypedDict):
    #: Что поменялось, кроме этапа
    changes: List[WebhookFieldChange]
    #: Сделка после правки
    deal: WebhookDeal
    #: deal.changed
    event: str


class WebhookDealChanged(_WebhookDealChangedRequired, total=False):
    #: Когда изменили, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    changed_at: Optional[str]
    #: Сотрудник {id, name, email}; null, если действие сделал не сотрудник
    changed_by: Optional[WebhookPerson]
    #: id сценария, если действие сделал сценарий; иначе null
    changed_by_workflow: Optional[str]


class _WebhookDealClosedRequired(TypedDict):
    #: Закрытая сделка
    deal: WebhookDeal
    #: deal.closed
    event: str
    #: won (выиграна) или lost (проиграна)
    outcome: str


class WebhookDealClosed(_WebhookDealClosedRequired, total=False):
    #: Когда закрыли, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    closed_at: Optional[str]
    #: Сотрудник {id, name, email}; null, если действие сделал не сотрудник
    closed_by: Optional[WebhookPerson]
    #: id сценария, если действие сделал сценарий; иначе null
    closed_by_workflow: Optional[str]
    #: Причина отказа у lost
    lost_reason: Optional[str]


class WebhookDealContact(TypedDict, total=False):
    #: id контакта, как в GET /api/v2/external/contacts
    id: Optional[str]
    #: Имя клиента
    name: Optional[str]
    #: Телефон, как в карточке, например +77071234567
    phone: Optional[str]


class _WebhookDealCreatedRequired(TypedDict):
    #: Новая сделка
    deal: WebhookDeal
    #: deal.created
    event: str


class WebhookDealCreated(_WebhookDealCreatedRequired, total=False):
    #: Когда создана, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    created_at: Optional[str]
    #: Сотрудник {id, name, email}; null, если действие сделал не сотрудник
    created_by: Optional[WebhookPerson]
    #: id сценария, если действие сделал сценарий; иначе null
    created_by_workflow: Optional[str]


class _WebhookDealStageChangedRequired(TypedDict):
    #: Сделка после перевода
    deal: WebhookDeal
    #: deal.stage_changed
    event: str


class WebhookDealStageChanged(_WebhookDealStageChangedRequired, total=False):
    #: С какого этапа
    from_stage: Optional[WebhookStage]
    #: Когда перевели, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    moved_at: Optional[str]
    #: Сотрудник {id, name, email}; null, если действие сделал не сотрудник
    moved_by: Optional[WebhookPerson]
    #: id сценария, если действие сделал сценарий; иначе null
    moved_by_workflow: Optional[str]
    #: На какой этап
    to_stage: Optional[WebhookStage]


class _WebhookDeliveryListOutRequired(TypedDict):
    #: Доставки на этой странице, новые первыми
    data: List[WebhookDeliveryOut]


class WebhookDeliveryListOut(_WebhookDeliveryListOutRequired, total=False):
    #: true, если есть следующая страница
    has_more: bool
    #: Передайте в ?cursor=, чтобы получить следующую страницу; null на последней
    next_cursor: Optional[str]


class _WebhookDeliveryOutRequired(TypedDict):
    #: Номер последней попытки: 1 первая, всего до 6
    attempt: int
    #: Событие, например message.incoming
    event_type: str
    #: id доставки, тот же, что в заголовке X-Wazzapo-Delivery-Id запроса на ваш адрес; нужен для POST /webhooks/{webhook_id}/deliveries/{delivery_id}/retry
    id: str
    #: pending (ждёт отправки), sending (отправляется), success (ваш адрес ответил 2xx), retry_scheduled (не дошло, следующая попытка в next_retry_at), failed (не дошло за все 6 попыток)
    status: str


class WebhookDeliveryOut(_WebhookDeliveryOutRequired, total=False):
    """Одна доставка события на ваш адрес вместе со всеми её попытками."""
    #: Когда произошло событие, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    created_at: Optional[str]
    #: Причина неудачи последней попытки, например HTTP 500
    error_message: Optional[str]
    #: Когда следующая попытка, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    next_retry_at: Optional[str]
    #: HTTP-код последнего ответа вашего адреса, например 500
    response_status: Optional[int]
    #: Когда отправлена последняя попытка, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    sent_at: Optional[str]


class _WebhookEventTypeListOutRequired(TypedDict):
    #: События на этой странице
    data: List[WebhookEventTypeOut]


class WebhookEventTypeListOut(_WebhookEventTypeListOutRequired, total=False):
    #: true, если есть следующая страница
    has_more: bool
    #: Передайте в ?cursor=, чтобы получить следующую страницу; null на последней
    next_cursor: Optional[str]


class _WebhookEventTypeOutRequired(TypedDict):
    #: Когда приходит событие и что в нём
    description: str
    #: Имя события для event_types, например deal.created
    name: str


class WebhookEventTypeOut(_WebhookEventTypeOutRequired, total=False):
    #: Пример поля data в теле запроса на ваш адрес
    example: Optional[Dict[str, Any]]


class _WebhookFieldChangeRequired(TypedDict):
    #: Что поменялось: имя поля (value, title, assignee_id, tags, name...) или custom_fields.<ключ> у контакта и custom_attributes.<id поля> у сделки. У value old и new в целых тенге, как deal.value
    field: str


class WebhookFieldChange(_WebhookFieldChangeRequired, total=False):
    #: Стало; null, если поле очистили
    new: Any
    #: Было: значение того же типа, что поле; null, если было пусто
    old: Any


_WebhookIncomingMessageRequired = TypedDict(
    "_WebhookIncomingMessageRequired",
    {
    },
    total=True,
)


_WebhookIncomingMessageOptional = TypedDict(
    "_WebhookIncomingMessageOptional",
    {
        #: Только у type=contact: карточки
        "contacts": "Optional[List[WebhookContactCard]]",
        #: Адрес отправителя: у WhatsApp телефон цифрами, например 77071234567
        "from": "Optional[str]",
        #: id сообщения: у WhatsApp wamid, например wamid.HBgLNzcwNzEy...
        "id": "Optional[str]",
        #: Клиент нажал кнопку или выбрал пункт списка; иначе null
        "interactive": "Optional[InteractiveResponseOut]",
        #: Старое поле, то же, что interactive.id: оставлено для совместимости
        "interactive_reply_id": "Optional[str]",
        #: Только у type=location: точка на карте
        "location": "Optional[WebhookLocation]",
        #: Ссылка на файл (картинка, документ, голосовое); null у текста
        "media_url": "Optional[str]",
        #: Имя клиента из профиля WhatsApp или из Wazzapo
        "name": "Optional[str]",
        #: Текст сообщения, подпись к файлу или текст нажатой кнопки
        "text": "str",
        #: Когда клиент отправил сообщение, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
        "timestamp": "Optional[str]",
        #: text, image, video, audio, voice, document, location, contact, sticker. Нажатие кнопки приходит как text: текст кнопки в text, сама кнопка в interactive
        "type": "Optional[str]",
    },
    total=False,
)


class WebhookIncomingMessage(_WebhookIncomingMessageRequired, _WebhookIncomingMessageOptional):
    pass


class _WebhookInvoiceRequired(TypedDict):
    #: Сумма в тиынах: 30000000 = 300 000 тенге
    amount: int
    #: id счёта в Wazzapo
    id: str


class WebhookInvoice(_WebhookInvoiceRequired, total=False):
    #: id счёта в ApiPay
    apipay_invoice_id: Optional[str]
    #: Имя плательщика из Kaspi
    client_name: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Выставлен, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    created_at: Optional[str]
    #: Всегда KZT
    currency: str
    #: id сделки счёта
    deal_id: Optional[str]
    #: Назначение платежа
    description: str
    #: Код ошибки у status=error
    error_code: Optional[str]
    #: Текст ошибки у status=error
    error_text: Optional[str]
    #: Срок оплаты, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    expires_at: Optional[str]
    #: true: тестовый счёт
    is_sandbox: bool
    #: Состав счёта
    items: List[WebhookInvoiceItem]
    #: Номер Kaspi клиента у method=phone
    kaspi_phone: Optional[str]
    #: Как выставлен: phone (на номер Kaspi) или link (ссылка)
    method: Optional[str]
    #: Оплачен, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z; иначе null
    paid_at: Optional[str]
    #: Ссылка на оплату у method=link
    payment_url: Optional[str]
    #: Откуда выставлен: chat, deal, workflow, api
    source: Optional[str]
    #: processing, pending, paid, cancelled, expired, error, partially_refunded
    status: Optional[str]
    #: Сколько возвращено, в тиынах; null без возврата
    total_refunded: Optional[int]


class WebhookInvoiceItem(TypedDict, total=False):
    #: id товара в каталоге кассы ApiPay, если есть
    catalog_item_id: Optional[Any]
    #: Количество
    count: Optional[float]
    #: Название позиции
    name: Optional[str]
    #: Цена за единицу в тенге, как её прислал Kaspi (ApiPay)
    price: Optional[float]


class _WebhookInvoiceStatusChangedRequired(TypedDict):
    #: Клиент
    contact: WebhookContactRef
    #: Имя события
    event: str
    #: Счёт на момент смены статуса
    invoice: WebhookInvoice


class WebhookInvoiceStatusChanged(_WebhookInvoiceStatusChangedRequired, total=False):
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email; null без диалога
    channel: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: id номера WhatsApp, как phone_number_id в GET /api/v2/external/phone-numbers; null у других каналов
    phone_number_id: Optional[str]
    #: Прежний статус
    previous_status: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id; null без диалога
    session_id: Optional[str]
    #: Новый статус, как invoice.status
    status: Optional[str]
    #: Когда произошло, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookListOutRequired(TypedDict):
    #: Вебхуки аккаунта на этой странице, без секретов
    data: List[WebhookOut]


class WebhookListOut(_WebhookListOutRequired, total=False):
    #: true, если есть следующая страница
    has_more: bool
    #: Передайте в ?cursor=, чтобы получить следующую страницу; null на последней
    next_cursor: Optional[str]


class WebhookLocation(TypedDict, total=False):
    #: Адрес места, если есть
    address: Optional[str]
    #: Широта, например 51.128207
    latitude: Optional[float]
    #: Долгота, например 71.430411
    longitude: Optional[float]
    #: Название места, если клиент выбрал место, а не точку
    name: Optional[str]


class _WebhookMessageIncomingRequired(TypedDict):
    #: Клиент диалога; в группе участник, который написал
    contact: WebhookContactRef
    #: Имя события, как поле event оболочки
    event: str
    #: Входящее сообщение
    message: WebhookIncomingMessage


class WebhookMessageIncoming(_WebhookMessageIncomingRequired, total=False):
    """message.incoming: клиент написал или нажал кнопку."""
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
    channel: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: id номера WhatsApp, как phone_number_id в GET /api/v2/external/phone-numbers; null у других каналов
    phone_number_id: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id
    session_id: Optional[str]
    #: Когда произошло событие, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookMessageOutgoingRequired(TypedDict):
    #: Клиент диалога; в группе участник, который написал
    contact: WebhookContactRef
    #: Имя события, как поле event оболочки
    event: str
    #: Исходящее сообщение
    message: WebhookOutgoingMessage
    #: Кто отправил
    sender: WebhookPerson


class WebhookMessageOutgoing(_WebhookMessageOutgoingRequired, total=False):
    """message.outgoing: любое сообщение клиенту."""
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
    channel: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id
    session_id: Optional[str]
    #: Статус в момент записи: pending, sent, delivered, read
    status: Optional[str]
    #: Когда произошло событие, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookMessageStatusRequired(TypedDict):
    #: message.status
    event: str
    #: sent (отправлено), delivered (доставлено), read (прочитано), failed (ошибка)
    status: str


class WebhookMessageStatus(_WebhookMessageStatusRequired, total=False):
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Причина у failed; иначе null
    error: Optional[WebhookStatusError]
    #: wamid исходящего: message.id из message.outgoing или ответа отправки
    message_id: Optional[str]
    #: id номера WhatsApp, как phone_number_id в GET /api/v2/external/phone-numbers; null у других каналов
    phone_number_id: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id
    session_id: Optional[str]


class WebhookMessageTemplate(TypedDict, total=False):
    #: Текст шаблона, если сохранён
    body: Optional[str]
    #: id загруженного файла шапки, если он был
    header_media_id: Optional[str]
    #: Ссылка на файл шапки шаблона, если он был
    header_media_url: Optional[str]
    #: Язык шаблона: ru, kk, en
    language: Optional[str]
    #: Имя шаблона, как в GET /api/v2/external/templates
    name: Optional[str]
    #: Откуда отправлен, если не из чата: mcp, cliniccards_reminder
    source: Optional[str]
    #: Значения {{1}}, {{2}} по порядку
    variables: Optional[List[Any]]


class WebhookNote(TypedDict, total=False):
    #: id заметки
    id: Optional[str]
    #: Текст заметки, клиент его не видит
    text: str


class _WebhookNoteAddedRequired(TypedDict):
    #: Кто оставил заметку
    author: WebhookPerson
    #: Клиент диалога; в группе участник, который написал
    contact: WebhookContactRef
    #: Имя события, как поле event оболочки
    event: str
    #: Заметка
    note: WebhookNote


class WebhookNoteAdded(_WebhookNoteAddedRequired, total=False):
    """conversation.note_added: заметка сотрудника."""
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email
    channel: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id
    session_id: Optional[str]
    #: Когда произошло событие, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookOutRequired(TypedDict):
    #: События подписки, например ["message.incoming", "deal.stage_changed"]
    event_types: List[str]
    #: id вебхука: из ответа POST /webhooks или GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
    id: str
    #: true: события доставляются. false: выключен вами или автоматически после 10 доставок подряд, не дошедших за все попытки. Включить: PATCH /webhooks/{webhook_id} с is_active=true
    is_active: bool
    #: Адрес, куда приходят события, например https://crm.example.kz/hooks/wazzapo
    url: str


class WebhookOut(_WebhookOutRequired, total=False):
    """Подписка на события: адрес, события и состояние доставки."""
    #: Сколько доставок подряд не дошли за все 6 попыток. Обнуляется при успешной доставке и при включении; на 10 вебхук выключается
    consecutive_failures: int
    #: Когда создан, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    created_at: Optional[str]
    #: Ваша подпись к вебхуку, например «CRM: заявки»
    description: Optional[str]
    #: Последний провал доставки, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    last_failure_at: Optional[str]
    #: Последняя успешная доставка, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    last_success_at: Optional[str]


class WebhookOutgoingMessage(TypedDict, total=False):
    #: id сообщения: у WhatsApp wamid; по нему придёт message.status
    id: Optional[str]
    #: Ссылка на файл; null у текста
    media_url: Optional[str]
    #: Шаблон WhatsApp, если сообщение шаблонное
    template: Optional[WebhookMessageTemplate]
    #: Текст или подпись; у шаблона его текст с подставленными значениями
    text: str
    #: text, image, video, audio, document, location, contact, sticker
    type: Optional[str]


class WebhookPerson(TypedDict, total=False):
    """Кто сделал действие или сотрудник. type есть у отправителя и автора, у ответственного его нет."""
    #: Почта сотрудника
    email: Optional[str]
    #: id сотрудника, как в GET /api/v2/external/team (там строкой)
    id: Optional[int]
    #: Имя сотрудника, название сценария или бота
    name: Optional[str]
    #: manager (сотрудник), workflow (сценарий), chatbot (бот или ИИ-ассистент), broadcast (рассылка), api (ваша программа через API или MCP), contact (клиент), system (служебное)
    type: Optional[str]
    #: Откуда отправлено: external_api, mcp, amocrm и другие интеграции
    via: Optional[str]
    #: id сценария у type=workflow
    workflow_id: Optional[str]


class WebhookPipelineRef(TypedDict, total=False):
    #: id воронки, как в GET /api/v2/external/pipelines
    id: Optional[str]
    #: Название воронки, например Продажи
    name: Optional[str]


class WebhookRetryOut(TypedDict):
    #: true, если на этот раз ваш адрес ответил 2xx
    delivered: bool
    #: id повторённой доставки
    delivery_id: str


class WebhookSecretOut(TypedDict):
    #: id вебхука: из ответа POST /webhooks или GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
    id: str
    #: Новый секрет подписи, показывается один раз. Старый перестаёт действовать сразу: обновите секрет на своём сервере
    secret: str


class _WebhookSessionRequired(TypedDict):
    #: session.connected или session.disconnected
    event: str


class WebhookSession(_WebhookSessionRequired, total=False):
    #: id номера WhatsApp, как phone_number_id в GET /api/v2/external/phone-numbers; null у других каналов
    phone_number_id: Optional[str]
    #: Только у session.disconnected: user_disconnected (отключили в кабинете)
    reason: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id
    session_id: Optional[str]


class _WebhookStageRequired(TypedDict):
    #: id этапа из stages[] в GET /api/v2/external/pipelines
    id: str


class WebhookStage(_WebhookStageRequired, total=False):
    #: true: этап «Отказ» (сделка проиграна)
    is_lost: bool
    #: true: этап «Успешно» (сделка выиграна)
    is_won: bool
    #: Название этапа, например «Отправлено КП»
    name: str


class WebhookStatusError(TypedDict, total=False):
    #: Код ошибки WhatsApp (Meta), например 131047
    code: str
    #: Подробности от Meta, если есть
    details: str
    #: Текст ошибки от Meta
    message: str


class _WebhookTaskRequired(TypedDict):
    #: id задачи, как id в TaskOut: по нему задачу меняют и закрывают через PATCH /api/v2/external/tasks/{task_id}. Отдельного GET /tasks нет: задачи сделки отдаёт GET /api/v2/external/deals/{deal_id}/tasks
    id: str


class WebhookTask(_WebhookTaskRequired, total=False):
    #: true: на весь день, без времени
    all_day: bool
    #: Исполнитель {id, name, email}
    assignee: Optional[WebhookPerson]
    #: id контакта
    contact_id: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: Создана, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    created_at: Optional[str]
    #: Автор {id, name, email}
    created_by: Optional[WebhookPerson]
    #: id сделки задачи, как deal_id в REST: GET /api/v2/external/deals/{deal_id}; null у задачи без сделки
    deal_id: Optional[str]
    #: Описание
    description: str
    #: Срок, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    due_at: Optional[str]
    #: low, normal, high
    priority: Optional[str]
    #: open или done
    status: Optional[str]
    #: Тип задачи, те же значения, что task_type в REST (TaskCreateIn, TaskOut): call (звонок), meeting (встреча), email (письмо), task (дело) или ключ своего типа вида c_6713d0a1b2c3
    task_type: Optional[str]
    #: Название задачи
    title: Optional[str]
    #: Тип задачи, то же значение, что task_type (старое имя поля)
    type: Optional[str]


class _WebhookTaskCreatedRequired(TypedDict):
    #: Клиент
    contact: WebhookContactRef
    #: Имя события
    event: str
    #: Новая задача
    task: WebhookTask


class WebhookTaskCreated(_WebhookTaskCreatedRequired, total=False):
    #: Канал: whatsapp, telegram, instagram, webchat (чат на сайте), olx, satu, email; null без диалога
    channel: Optional[str]
    #: id диалога: тот же id, что в GET /api/v2/external/conversations
    conversation_id: Optional[str]
    #: id сценария, если действие сделал сценарий; иначе null
    created_by_workflow: Optional[str]
    #: id номера WhatsApp, как phone_number_id в GET /api/v2/external/phone-numbers; null у других каналов
    phone_number_id: Optional[str]
    #: Подключение (канал) в Wazzapo, например meta_103799815708451: у WhatsApp это meta_ + phone_number_id; null без диалога
    session_id: Optional[str]
    #: Когда произошло, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]


class _WebhookTemplateEventRequired(TypedDict):
    #: Имя события
    event: str
    #: Шаблон
    template: WebhookTemplateRef


class WebhookTemplateEvent(_WebhookTemplateEventRequired, total=False):
    """template.status_updated, template.quality_changed, template.category_changed."""
    #: category_changed: true, если только предупреждение
    is_warning: Optional[bool]
    #: category_changed: стало MARKETING, UTILITY
    new_category: Optional[str]
    #: quality_changed: стало, в формате Meta GREEN (хорошо), YELLOW (внимание), RED (низкое, шаблон могут приостановить), UNKNOWN. То же в формате REST: quality_score
    new_quality: Optional[str]
    #: id номера WhatsApp, как phone_number_id в GET /api/v2/external/phone-numbers; null у других каналов
    phone_number_id: Optional[str]
    #: category_changed: было MARKETING, UTILITY
    previous_category: Optional[str]
    #: quality_changed: было, в формате Meta GREEN, YELLOW, RED, UNKNOWN. То же в формате REST: previous_quality_score
    previous_quality: Optional[str]
    #: quality_changed: previous_quality в формате REST (TemplateOut.quality_score): GREEN = HIGH, YELLOW = MEDIUM, RED = LOW, остальное UNKNOWN
    previous_quality_score: Optional[Literal['HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']]
    #: quality_changed: new_quality в формате REST, как quality_score в GET /api/v2/external/templates: GREEN = HIGH, YELLOW = MEDIUM, RED = LOW, остальное UNKNOWN
    quality_score: Optional[Literal['HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']]
    #: status_updated: причина отказа, например INVALID_FORMAT
    reason: Optional[str]
    #: status_updated: APPROVED, REJECTED, PAUSED, DISABLED
    status: Optional[str]
    #: Когда пришло уведомление Meta, UTC в формате ISO 8601, например 2026-10-18T09:15:02Z
    timestamp: Optional[str]
    #: id бизнес-аккаунта WhatsApp (WABA) шаблона
    waba_id: Optional[str]


class WebhookTemplateRef(TypedDict, total=False):
    #: id шаблона в Meta, как id в GET /api/v2/external/templates
    id: Optional[str]
    #: Язык шаблона: ru, kk, en
    language: Optional[str]
    #: Имя шаблона, например invoice_ready
    name: Optional[str]
    #: id шаблона в Meta, то же значение, что id: имя как template_id в GET /api/v2/external/templates и в путях /templates/{template_id}
    template_id: Optional[str]


class WebhookTestEvent(TypedDict):
    """Тело data тестового события test из POST /api/v2/external/webhooks/{webhook_id}/test."""
    #: Всегда «This is a test webhook event from Wazzapo.»: проверка адреса и подписи, обрабатывать как событие не нужно
    message: str


class _WebhookTestOutRequired(TypedDict):
    #: true, если ваш адрес ответил кодом 2xx за 10 секунд
    delivered: bool


class WebhookTestOut(_WebhookTestOutRequired, total=False):
    #: Почему не доставлено: HTTP 500, таймаут, не удалось соединиться; null при успехе
    error: Optional[str]
    #: HTTP-код ответа вашего адреса, например 200; null, если ответа не было
    response_status: Optional[int]
    #: Сколько миллисекунд ждали ответ, например 184
    response_time_ms: Optional[int]


class WebhookUpdateIn(TypedDict, total=False):
    """Меняются только переданные поля."""
    #: Подпись для себя, чтобы отличать приёмники, например «CRM: заявки». До 100 символов
    description: Optional[str]
    #: Новый список событий целиком: заменяет старый. Чтобы добавить событие, передайте старые вместе с новым. На какие события подписаться, хотя бы одно; список с описаниями: GET /webhook-event-types. Сейчас: message.incoming, message.outgoing, message.status, conversation.assigned, conversation.status_changed, conversation.note_added, session.connected, session.disconnected, deal.stage_changed, deal.closed, deal.created, deal.changed, contact.created, contact.updated, template.status_updated, template.quality_changed, template.category_changed, invoice.status_changed, task.created
    event_types: Optional[List[Literal['message.incoming', 'message.outgoing', 'message.status', 'conversation.assigned', 'conversation.status_changed', 'conversation.note_added', 'session.connected', 'session.disconnected', 'deal.stage_changed', 'deal.closed', 'deal.created', 'deal.changed', 'contact.created', 'contact.updated', 'template.status_updated', 'template.quality_changed', 'template.category_changed', 'invoice.status_changed', 'task.created']]]
    #: false выключает доставку: события за это время не копятся и не придут потом. true включает снова и обнуляет consecutive_failures: так включают вебхук, выключенный автоматически после 10 провалов подряд
    is_active: Optional[bool]
    #: Новый адрес. Адрес вашего сервера, куда Wazzapo отправляет события запросом POST: только https:// и только публичный адрес (localhost и внутренние сети нельзя), до 2048 символов. Пример: https://crm.example.kz/hooks/wazzapo
    url: Optional[str]


class _WebhookWithSecretOutRequired(TypedDict):
    #: События подписки, например ["message.incoming", "deal.stage_changed"]
    event_types: List[str]
    #: id вебхука: из ответа POST /webhooks или GET /webhooks, например 6712f0c4a1b2c3d4e5f60719
    id: str
    #: true: события доставляются. false: выключен вами или автоматически после 10 доставок подряд, не дошедших за все попытки. Включить: PATCH /webhooks/{webhook_id} с is_active=true
    is_active: bool
    #: Секрет подписи HMAC-SHA256, вида whsec_… Показывается только в этом ответе: сохраните его у себя. Им проверяйте заголовок X-Wazzapo-Signature-V2. Потеряли: POST /webhooks/{webhook_id}/rotate-secret выдаст новый
    secret: str
    #: Адрес, куда приходят события, например https://crm.example.kz/hooks/wazzapo
    url: str


class WebhookWithSecretOut(_WebhookWithSecretOutRequired, total=False):
    """Созданный вебхук вместе с секретом подписи: секрет больше нигде не показывается."""
    #: Сколько доставок подряд не дошли за все 6 попыток. Обнуляется при успешной доставке и при включении; на 10 вебхук выключается
    consecutive_failures: int
    #: Когда создан, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    created_at: Optional[str]
    #: Ваша подпись к вебхуку, например «CRM: заявки»
    description: Optional[str]
    #: Последний провал доставки, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    last_failure_at: Optional[str]
    #: Последняя успешная доставка, ISO 8601 UTC, например 2026-10-18T09:15:00+00:00
    last_success_at: Optional[str]


__all__ = [
    "AddNoteIn",
    "AssignConversationIn",
    "AttributionSourceOut",
    "BusinessProfileIn",
    "BusinessProfileOut",
    "BusinessProfileUpdateOut",
    "ContactAttributionOut",
    "ContactCard",
    "ContactCardName",
    "ContactCardPhone",
    "ContactCreateIn",
    "ContactListOut",
    "ContactUpdateIn",
    "ContactV2Out",
    "ConversationContactOut",
    "ConversationItemOut",
    "ConversationLastMessageOut",
    "ConversationListOut",
    "ConversationMessageListOut",
    "ConversationMessageOut",
    "CreateTemplateIn",
    "CtaUrlParameters",
    "DealContactIn",
    "DealContactOut",
    "DealCreateIn",
    "DealListOut",
    "DealMoveIn",
    "DealOut",
    "DealUpdateIn",
    "ErrorBody",
    "ErrorField",
    "ErrorOut",
    "InteractiveAction",
    "InteractiveContent",
    "InteractiveFooterText",
    "InteractiveHeader",
    "InteractiveListRow",
    "InteractiveListSection",
    "InteractiveMedia",
    "InteractiveReply",
    "InteractiveReplyButton",
    "InteractiveResponseOut",
    "InteractiveText",
    "LocationContent",
    "MarkReadIn",
    "MediaContent",
    "MediaUploadForm",
    "MediaUploadOut",
    "MessageContext",
    "MessageSenderOut",
    "MessageTemplateRefOut",
    "PhoneNumberListOut",
    "PhoneNumberOut",
    "PipelineFieldOut",
    "PipelineListOut",
    "PipelineOut",
    "PipelineStageOut",
    "ReactionIn",
    "ReactionOut",
    "RegisterPhoneNumberIn",
    "RegisterPhoneNumberOut",
    "SendMessageIn",
    "SendMessageOut",
    "SetConversationStatusIn",
    "SetLabelsIn",
    "StaffRefOut",
    "SuccessOut",
    "TaskCreateIn",
    "TaskListOut",
    "TaskOut",
    "TaskUpdateIn",
    "TeamListOut",
    "TeamMemberOut",
    "TemplateBody",
    "TemplateBodyExample",
    "TemplateButtonCopyCode",
    "TemplateButtonOther",
    "TemplateButtonOtp",
    "TemplateButtonPhoneNumber",
    "TemplateButtonQuickReply",
    "TemplateButtonUrl",
    "TemplateButtons",
    "TemplateComponentIn",
    "TemplateCurrency",
    "TemplateDateTime",
    "TemplateFooter",
    "TemplateHeaderLocation",
    "TemplateHeaderMedia",
    "TemplateHeaderText",
    "TemplateHeaderTextExample",
    "TemplateLanguage",
    "TemplateListOut",
    "TemplateMedia",
    "TemplateMediaExample",
    "TemplateMessageIn",
    "TemplateOtpApp",
    "TemplateOut",
    "TemplateParameter",
    "TextContent",
    "UpdateTemplateIn",
    "WebhookCardName",
    "WebhookCardPhone",
    "WebhookContact",
    "WebhookContactCard",
    "WebhookContactCreated",
    "WebhookContactRef",
    "WebhookContactUpdated",
    "WebhookConversationAssigned",
    "WebhookConversationStatusChanged",
    "WebhookCreateIn",
    "WebhookDeal",
    "WebhookDealChanged",
    "WebhookDealClosed",
    "WebhookDealContact",
    "WebhookDealCreated",
    "WebhookDealStageChanged",
    "WebhookDeliveryListOut",
    "WebhookDeliveryOut",
    "WebhookEventTypeListOut",
    "WebhookEventTypeOut",
    "WebhookFieldChange",
    "WebhookIncomingMessage",
    "WebhookInvoice",
    "WebhookInvoiceItem",
    "WebhookInvoiceStatusChanged",
    "WebhookListOut",
    "WebhookLocation",
    "WebhookMessageIncoming",
    "WebhookMessageOutgoing",
    "WebhookMessageStatus",
    "WebhookMessageTemplate",
    "WebhookNote",
    "WebhookNoteAdded",
    "WebhookOut",
    "WebhookOutgoingMessage",
    "WebhookPerson",
    "WebhookPipelineRef",
    "WebhookRetryOut",
    "WebhookSecretOut",
    "WebhookSession",
    "WebhookStage",
    "WebhookStatusError",
    "WebhookTask",
    "WebhookTaskCreated",
    "WebhookTemplateEvent",
    "WebhookTemplateRef",
    "WebhookTestEvent",
    "WebhookTestOut",
    "WebhookUpdateIn",
    "WebhookWithSecretOut",
]
