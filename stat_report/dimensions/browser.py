from dataclasses import dataclass
from .base import Dimension
from stat_report.models import LogRecord
from stat_report.ua_service import UserAgentService

@dataclass(frozen=True)
class BrowserDimension(Dimension):
    ua: UserAgentService

    def __init__(self, ua: UserAgentService):
        object.__setattr__(self, "name", "Browser")
        object.__setattr__(self, "ua", ua)

    def extract(self, record: LogRecord) -> str:
        return self.ua.browser_name(record.user_agent)