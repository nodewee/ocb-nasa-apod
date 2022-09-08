from dataclasses import dataclass


@dataclass(frozen=True)
class _OrderTypes:
    CREATE_CHANNEL: str = "1"


@dataclass(frozen=True)
class _InfoContentTypes:
    TEXT: str = "TEXT"
    MARKDOWN: str = "MARKDOWN"
    HTML: str = "HTML"
    IMAGE: str = "IMAGE"
    VIDEO: str = "VIDEO"
    AUDIO: str = "AUDIO"
    FILE: str = "FILE"


@dataclass(frozen=True)
class _SettingNames:
    LANG: str = "lang"
    UTC_OFFSET: str = "utc"


API_BASE_URL = "https://api.infowoods.com/v3"
ORDER_TYPES = _OrderTypes()
INFO_CONTENT_TYPES = _InfoContentTypes()
SETTING_NAMES = _SettingNames()