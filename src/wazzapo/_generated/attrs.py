# Сгенерировано sdk/codegen/python.py из sdk/openapi.json. Не править руками: cd sdk && python -m codegen

"""Атрибуты ресурсов клиента, чтобы редактор подсказывал client.messages и т.д."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import resources as _r


class SyncResources:
    contacts: "_r.Contacts"
    conversations: "_r.Conversations"
    deals: "_r.Deals"
    media: "_r.Media"
    messages: "_r.Messages"
    phone_numbers: "_r.PhoneNumbers"
    pipelines: "_r.Pipelines"
    tasks: "_r.Tasks"
    team: "_r.Team"
    templates: "_r.Templates"
    webhook_event_types: "_r.WebhookEventTypes"
    webhooks: "_r.Webhooks"


class AsyncResources:
    contacts: "_r.AsyncContacts"
    conversations: "_r.AsyncConversations"
    deals: "_r.AsyncDeals"
    media: "_r.AsyncMedia"
    messages: "_r.AsyncMessages"
    phone_numbers: "_r.AsyncPhoneNumbers"
    pipelines: "_r.AsyncPipelines"
    tasks: "_r.AsyncTasks"
    team: "_r.AsyncTeam"
    templates: "_r.AsyncTemplates"
    webhook_event_types: "_r.AsyncWebhookEventTypes"
    webhooks: "_r.AsyncWebhooks"
