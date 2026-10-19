# Сгенерировано sdk/codegen/python.py из sdk/openapi.json. Не править руками: cd sdk && python -m codegen

"""Тела запросов, которые Wazzapo присылает на адрес вебхука."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from .types import (
    WebhookContactCreated,
    WebhookContactUpdated,
    WebhookConversationAssigned,
    WebhookConversationStatusChanged,
    WebhookDealChanged,
    WebhookDealClosed,
    WebhookDealCreated,
    WebhookDealStageChanged,
    WebhookInvoiceStatusChanged,
    WebhookMessageIncoming,
    WebhookMessageOutgoing,
    WebhookMessageStatus,
    WebhookNoteAdded,
    WebhookSession,
    WebhookTaskCreated,
    WebhookTemplateEvent,
    WebhookTestEvent,
)


class ContactCreatedEvent(TypedDict):
    """contact.created: Новый контакт: добавлен вручную, через API, пришёл с сообщением или письмом"""
    #: Данные события
    data: WebhookContactCreated
    #: Имя события
    event: Literal['contact.created']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class ContactUpdatedEvent(TypedDict):
    """contact.updated: В карточке контакта поменялись имя, телефон, почта, компания, теги, заметки, блокировка или дополнительные поля: список changes и кто изменил (changed_by)"""
    #: Данные события
    data: WebhookContactUpdated
    #: Имя события
    event: Literal['contact.updated']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class ConversationAssignedEvent(TypedDict):
    """conversation.assigned: Диалог назначили менеджеру, передали другому или сняли назначение"""
    #: Данные события
    data: WebhookConversationAssigned
    #: Имя события
    event: Literal['conversation.assigned']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class ConversationNoteAddedEvent(TypedDict):
    """conversation.note_added: Менеджер оставил заметку в диалоге (клиент её не видит)"""
    #: Данные события
    data: WebhookNoteAdded
    #: Имя события
    event: Literal['conversation.note_added']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class ConversationStatusChangedEvent(TypedDict):
    """conversation.status_changed: Статус диалога изменился: open, pending, snoozed, resolved"""
    #: Данные события
    data: WebhookConversationStatusChanged
    #: Имя события
    event: Literal['conversation.status_changed']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class DealChangedEvent(TypedDict):
    """deal.changed: У сделки поменялись сумма, название, ответственный, клиент или поля воронки: список changes «поле, было, стало»"""
    #: Данные события
    data: WebhookDealChanged
    #: Имя события
    event: Literal['deal.changed']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class DealClosedEvent(TypedDict):
    """deal.closed: Сделка выиграна или проиграна: outcome won или lost, причина проигрыша lost_reason, кто закрыл"""
    #: Данные события
    data: WebhookDealClosed
    #: Имя события
    event: Literal['deal.closed']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class DealCreatedEvent(TypedDict):
    """deal.created: Новая сделка: из карточки, правилом по входящему сообщению, сценарием или через API"""
    #: Данные события
    data: WebhookDealCreated
    #: Имя события
    event: Literal['deal.created']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class DealStageChangedEvent(TypedDict):
    """deal.stage_changed: Сделку перевели на другой этап: из карточки, перетаскиванием, массово, правилом, сценарием или после оплаты"""
    #: Данные события
    data: WebhookDealStageChanged
    #: Имя события
    event: Literal['deal.stage_changed']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class InvoiceStatusChangedEvent(TypedDict):
    """invoice.status_changed: Счёт Kaspi (ApiPay) сменил статус: processing, pending, paid, cancelled, expired, error, partially_refunded"""
    #: Данные события
    data: WebhookInvoiceStatusChanged
    #: Имя события
    event: Literal['invoice.status_changed']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class MessageIncomingEvent(TypedDict):
    """message.incoming: Клиент написал"""
    #: Данные события
    data: WebhookMessageIncoming
    #: Имя события
    event: Literal['message.incoming']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class MessageOutgoingEvent(TypedDict):
    """message.outgoing: Любое сообщение клиенту: менеджер из чата, сценарий или бот, рассылка, шаблон, отправка через API"""
    #: Данные события
    data: WebhookMessageOutgoing
    #: Имя события
    event: Literal['message.outgoing']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class MessageStatusEvent(TypedDict):
    """message.status: Изменение статуса исходящего сообщения (отправлено, доставлено, прочитано, ошибка)"""
    #: Данные события
    data: WebhookMessageStatus
    #: Имя события
    event: Literal['message.status']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class SessionConnectedEvent(TypedDict):
    """session.connected: WhatsApp-сессия успешно подключена"""
    #: Данные события
    data: WebhookSession
    #: Имя события
    event: Literal['session.connected']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class SessionDisconnectedEvent(TypedDict):
    """session.disconnected: WhatsApp-сессия отключена"""
    #: Данные события
    data: WebhookSession
    #: Имя события
    event: Literal['session.disconnected']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class TaskCreatedEvent(TypedDict):
    """task.created: Новая задача менеджеру: из сделки или чата, через API, сценарием, правилом этапа воронки или следующим шагом после выполненной задачи"""
    #: Данные события
    data: WebhookTaskCreated
    #: Имя события
    event: Literal['task.created']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class TemplateCategoryChangedEvent(TypedDict):
    """template.category_changed: Meta сменила категорию шаблона (MARKETING, UTILITY, AUTHENTICATION), от неё зависит цена"""
    #: Данные события
    data: WebhookTemplateEvent
    #: Имя события
    event: Literal['template.category_changed']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class TemplateQualityChangedEvent(TypedDict):
    """template.quality_changed: Meta изменила оценку качества шаблона: GREEN, YELLOW, RED"""
    #: Данные события
    data: WebhookTemplateEvent
    #: Имя события
    event: Literal['template.quality_changed']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class TemplateStatusUpdatedEvent(TypedDict):
    """template.status_updated: Meta проверила шаблон: APPROVED, REJECTED (с причиной reason), PAUSED, DISABLED"""
    #: Данные события
    data: WebhookTemplateEvent
    #: Имя события
    event: Literal['template.status_updated']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


class TestEvent(TypedDict):
    """test: Тестовое событие"""
    #: Данные события
    data: WebhookTestEvent
    #: Имя события
    event: Literal['test']
    #: Когда Wazzapo создал доставку события, UTC, ISO 8601 с Z, например 2026-10-18T09:15:02.481000Z; одно во всех повторах. Время самого события: в data
    timestamp: str


WebhookEvent = Union[
    ContactCreatedEvent,
    ContactUpdatedEvent,
    ConversationAssignedEvent,
    ConversationNoteAddedEvent,
    ConversationStatusChangedEvent,
    DealChangedEvent,
    DealClosedEvent,
    DealCreatedEvent,
    DealStageChangedEvent,
    InvoiceStatusChangedEvent,
    MessageIncomingEvent,
    MessageOutgoingEvent,
    MessageStatusEvent,
    SessionConnectedEvent,
    SessionDisconnectedEvent,
    TaskCreatedEvent,
    TemplateCategoryChangedEvent,
    TemplateQualityChangedEvent,
    TemplateStatusUpdatedEvent,
    TestEvent,
]
"""Любое событие: смотрите поле event."""

EVENT_TYPES: Dict[str, Any] = {
    "contact.created": ContactCreatedEvent,
    "contact.updated": ContactUpdatedEvent,
    "conversation.assigned": ConversationAssignedEvent,
    "conversation.note_added": ConversationNoteAddedEvent,
    "conversation.status_changed": ConversationStatusChangedEvent,
    "deal.changed": DealChangedEvent,
    "deal.closed": DealClosedEvent,
    "deal.created": DealCreatedEvent,
    "deal.stage_changed": DealStageChangedEvent,
    "invoice.status_changed": InvoiceStatusChangedEvent,
    "message.incoming": MessageIncomingEvent,
    "message.outgoing": MessageOutgoingEvent,
    "message.status": MessageStatusEvent,
    "session.connected": SessionConnectedEvent,
    "session.disconnected": SessionDisconnectedEvent,
    "task.created": TaskCreatedEvent,
    "template.category_changed": TemplateCategoryChangedEvent,
    "template.quality_changed": TemplateQualityChangedEvent,
    "template.status_updated": TemplateStatusUpdatedEvent,
    "test": TestEvent,
}

__all__ = [
    "EVENT_TYPES",
    "WebhookEvent",
    "ContactCreatedEvent",
    "ContactUpdatedEvent",
    "ConversationAssignedEvent",
    "ConversationNoteAddedEvent",
    "ConversationStatusChangedEvent",
    "DealChangedEvent",
    "DealClosedEvent",
    "DealCreatedEvent",
    "DealStageChangedEvent",
    "InvoiceStatusChangedEvent",
    "MessageIncomingEvent",
    "MessageOutgoingEvent",
    "MessageStatusEvent",
    "SessionConnectedEvent",
    "SessionDisconnectedEvent",
    "TaskCreatedEvent",
    "TemplateCategoryChangedEvent",
    "TemplateQualityChangedEvent",
    "TemplateStatusUpdatedEvent",
    "TestEvent",
]
