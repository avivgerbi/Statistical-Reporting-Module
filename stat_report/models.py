from dataclasses import dataclass

@dataclass(frozen=True)
class LogRecord:
    ip: str
    user_agent: str