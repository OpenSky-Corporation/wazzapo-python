"""Wazzapo: SDK для API v2 (WhatsApp, контакты, сделки, вебхуки).

    from wazzapo import Wazzapo
    client = Wazzapo()  # ключ из WAZZAPO_API_KEY
    client.messages.send(body={"phone_number_id": "...", "to": "77071234567", "type": "text", "text": {"body": "Привет"}})
"""

from . import errors, types, webhooks
from ._client import AsyncWazzapo, Wazzapo
from ._generated import API_VERSION
from ._version import __version__
from .errors import (
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NotFoundError,
    OutsideWindowError,
    PaymentRequiredError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    TemplateError,
    UnprocessableEntityError,
    UsageLimitError,
    ValidationError,
    WazzapoError,
    WebhookSignatureError,
)

__all__ = [
    "API_VERSION",
    "APIConnectionError",
    "APITimeoutError",
    "AsyncWazzapo",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "NotFoundError",
    "OutsideWindowError",
    "PaymentRequiredError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "TemplateError",
    "UnprocessableEntityError",
    "UsageLimitError",
    "ValidationError",
    "Wazzapo",
    "WazzapoError",
    "WebhookSignatureError",
    "__version__",
    "errors",
    "types",
    "webhooks",
]
