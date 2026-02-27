from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from stat_report.models import LogRecord

@dataclass(frozen=True)
class Dimension(ABC):
    name: str

    @abstractmethod
    def extract(self, record: LogRecord) -> str:
        raise NotImplementedError