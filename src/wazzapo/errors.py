"""Ошибки SDK. Ловите WazzapoError или нужного наследника и смотрите error.code.

Тело ошибки API v2: {"success": false, "error": {"code", "message", "details"}, "request_id"}.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Type


class WazzapoError(Exception):
    """Ошибка API или соединения.

    status: HTTP-статус (None, если ответа не было)
    code: машинный код, например outside_24h_window; на него и ориентируйтесь в коде
    message: причина для человека
    details: подробности: список полей у VALIDATION_ERROR, объект у остальных
    request_id: id запроса, сообщите его в поддержку
    """

    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        code: Optional[str] = None,
        details: Any = None,
        request_id: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.details = details
        self.request_id = request_id
        self.headers: Dict[str, str] = dict(headers or {})

    def __str__(self) -> str:
        parts = [f"[{self.status}]" if self.status else "", self.code or "", self.message]
        text = " ".join(p for p in parts if p)
        return f"{text} (request_id {self.request_id})" if self.request_id else text

    def __repr__(self) -> str:
        return f"{type(self).__name__}(status={self.status!r}, code={self.code!r}, message={self.message!r})"


class APIConnectionError(WazzapoError):
    """Нет ответа: сбой сети или DNS. SDK уже повторил запрос max_retries раз."""


class APITimeoutError(APIConnectionError):
    """Сервер не ответил за timeout секунд."""


class BadRequestError(WazzapoError):
    """400: неверный запрос."""


class AuthenticationError(WazzapoError):
    """401: нет ключа, ключ неверный или отозван."""


class PaymentRequiredError(WazzapoError):
    """402: тариф Wazzapo не оплачен или Meta не может списать оплату."""


class PermissionDeniedError(WazzapoError):
    """403: у ключа нет права, IP не разрешён или метод не входит в тариф."""


class UsageLimitError(PermissionDeniedError):
    """403 USAGE_LIMIT_EXCEEDED: исчерпан лимит тарифа; в details current, limit и upgrade_url."""


class NotFoundError(WazzapoError):
    """404: объекта нет в этом аккаунте."""


class ConflictError(WazzapoError):
    """409: объект уже есть или запрос с этим Idempotency-Key ещё выполняется."""


class UnprocessableEntityError(WazzapoError):
    """422: запрос понятен, но выполнить нельзя: проверка полей или отказ Meta."""


class ValidationError(UnprocessableEntityError):
    """422 VALIDATION_ERROR: поля не прошли проверку, список в details (field, message)."""


class OutsideWindowError(UnprocessableEntityError):
    """422 outside_24h_window: клиент не писал 24 часа, отправьте шаблон."""


class TemplateError(UnprocessableEntityError):
    """422 template_*: шаблон не найден, не одобрен, приостановлен или отключён."""


class RateLimitError(WazzapoError):
    """429: слишком много запросов; retry_after: через сколько секунд повторить."""

    @property
    def retry_after(self) -> Optional[float]:
        value = {k.lower(): v for k, v in self.headers.items()}.get("retry-after")
        try:
            return float(value) if value is not None else None
        except ValueError:
            return None


class ServerError(WazzapoError):
    """5xx: сбой Wazzapo или WhatsApp (Meta). SDK уже повторил запрос."""


class WebhookSignatureError(ValueError):
    """Подпись вебхука не сошлась или метка времени слишком старая."""


ConnectionError = APIConnectionError  # noqa: A001 (имя из описания SDK: wazzapo.errors.ConnectionError)
TimeoutError = APITimeoutError  # noqa: A001

_BY_STATUS: Dict[int, Type[WazzapoError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    402: PaymentRequiredError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}
_BY_CODE: Dict[str, Type[WazzapoError]] = {
    "USAGE_LIMIT_EXCEEDED": UsageLimitError,
    "VALIDATION_ERROR": ValidationError,
    "outside_24h_window": OutsideWindowError,
    "template_not_found": TemplateError,
    "template_not_approved": TemplateError,
    "template_paused": TemplateError,
    "template_disabled": TemplateError,
}


def error_class(status: int, code: Optional[str]) -> Type[WazzapoError]:
    """Класс ошибки: сначала по коду, потом по статусу."""
    if code in _BY_CODE:
        return _BY_CODE[code]
    if status >= 500:
        return ServerError
    return _BY_STATUS.get(status, WazzapoError)


def from_response(status: int, body: Any, headers: Mapping[str, str]) -> WazzapoError:
    """Ошибка из ответа: тело v2, старое {"detail": ...} или просто текст."""
    code: Optional[str] = None
    details: Any = None
    request_id: Optional[str] = None
    message = f"HTTP {status}"
    if isinstance(body, dict):
        error = body.get("error")
        if isinstance(error, dict):
            code = error.get("code")
            message = str(error.get("message") or message)
            details = error.get("details")
        elif "detail" in body:
            message = str(body["detail"])
        request_id = body.get("request_id")
    elif isinstance(body, str) and body.strip():
        message = body.strip()[:500]
    lower = {k.lower(): v for k, v in headers.items()}
    request_id = request_id or lower.get("x-request-id")
    cls = error_class(status, code)
    return cls(message, status=status, code=code, details=details, request_id=request_id, headers=headers)


__all__ = [
    "APIConnectionError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "ConnectionError",
    "NotFoundError",
    "OutsideWindowError",
    "PaymentRequiredError",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "TemplateError",
    "TimeoutError",
    "UnprocessableEntityError",
    "UsageLimitError",
    "ValidationError",
    "WazzapoError",
    "WebhookSignatureError",
    "error_class",
    "from_response",
]
