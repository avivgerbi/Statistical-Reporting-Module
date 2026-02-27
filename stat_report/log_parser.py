import re
from typing import Iterator, TextIO
from .models import LogRecord

_IP_RE = re.compile(r"^(?P<ip>\S+)\s+")
_QUOTED_RE = re.compile(r'"([^"]*)"')

class LogParseError(Exception):
    pass

def iter_records(fp: TextIO) -> Iterator[LogRecord]:

    for line_num, line in enumerate(fp, start=1):
        line = line.strip()
        if not line:
            continue

        m = _IP_RE.match(line)
        if not m:
            # skip malformed
            continue
        ip = m.group("ip")

        quoted = _QUOTED_RE.findall(line)
        if not quoted:
            # no quoted fields => can't get UA
            continue

        user_agent = quoted[-1].strip()
        if not user_agent:
            user_agent = "Unknown"

        yield LogRecord(ip=ip, user_agent=user_agent)