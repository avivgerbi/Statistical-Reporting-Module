from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

@dataclass(frozen=True)
class ReportConfig:
    top_k: int = 5
    include_other: bool = True

def _sorted_items(counter: Counter) -> list[tuple[str, int]]:
    items = list(counter.items())
    items.sort(key=lambda kv: kv[1], reverse=True)
    return items

def format_section(title: str, counter: Counter, total: int, cfg: ReportConfig) -> str:
    items = _sorted_items(counter)

    if total <= 0:
        return f"{title}:\n(No data)\n"

    if cfg.top_k > 0 and len(items) > cfg.top_k:
        head = items[: cfg.top_k]
        tail = items[cfg.top_k :]

        if cfg.include_other and tail:
            other_count = sum(v for _, v in tail)
            head = head + [("Other", other_count)]
        items = head

    lines = [f"{title}:"]
    for label, count in items:
        pct = (count / total) * 100.0
        lines.append(f"{label} {pct:.2f}%")
    return "\n".join(lines) + "\n"

def format_report(counts_by_dimension: dict[str, Counter], total: int, cfg: ReportConfig) -> str:
    parts: list[str] = []
    order = ["Country", "OS", "Browser"]
    for name in order:
        if name in counts_by_dimension:
            parts.append(format_section(name, counts_by_dimension[name], total, cfg))

    for name in counts_by_dimension:
        if name not in order:
            parts.append(format_section(name, counts_by_dimension[name], total, cfg))
    return "\n".join(parts).rstrip() + "\n"