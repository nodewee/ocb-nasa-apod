from dataclasses import dataclass


class RequestError(BaseException):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class _OrderTypes:
    CREATE_TOPIC: str = "1"


from dataclasses import dataclass


@dataclass(frozen=True)
class _InfoContentTypes:
    TEXT: str = "TEXT"
    MARKDOWN: str = "MARKDOWN"
    HTML: str = "HTML"
    IMAGE: str = "IMAGE"
    VIDEO: str = "VIDEO"
    AUDIO: str = "AUDIO"
    FILE: str = "FILE"


INFO_CONTENT_TYPES = _InfoContentTypes()
ORDER_TYPES = _OrderTypes()
API_BASE_URL = "https://api.infowoods.com/v2"
