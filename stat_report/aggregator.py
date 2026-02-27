from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from .models import LogRecord
from .dimensions.base import Dimension

@dataclass
class StatsResult:
    total: int
    counts_by_dimension: dict[str, Counter]

class StatsAggregator:
    def __init__(self, dimensions: list[Dimension]):
        self._dimensions = dimensions
        self._counts_by_dimension = {d.name: Counter() for d in dimensions}
        self._total = 0

    def consume(self, records: Iterable[LogRecord]) -> StatsResult:
        for r in records:
            self._total += 1
            for d in self._dimensions:
                label = d.extract(r) or "Unknown"
                self._counts_by_dimension[d.name][label] += 1

        return StatsResult(total=self._total, counts_by_dimension=self._counts_by_dimension)