from dataclasses import dataclass
from ua_parser import user_agent_parser

@dataclass(frozen=True)
class UserAgentService:

    def parse(self, ua: str) -> dict:
        if not ua or ua == "Unknown":
            return {}
        try:
            return user_agent_parser.Parse(ua)
        except Exception:
            return {}

    def os_name(self, ua: str) -> str:
        parsed = self.parse(ua)
        os_ = parsed.get("os") or {}
        family = (os_.get("family") or "").strip()
        return family if family else "Unknown"

    def browser_name(self, ua: str) -> str:
        parsed = self.parse(ua)
        ua_ = parsed.get("user_agent") or {}
        family = (ua_.get("family") or "").strip()
        return family if family else "Unknown"