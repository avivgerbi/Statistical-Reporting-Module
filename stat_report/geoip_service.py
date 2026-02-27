from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import geoip2.database
import geoip2.errors

@dataclass
class GeoIPService:
    """
    Resolves IP -> Country name using a local MaxMind mmdb database.
    IMPORTANT per assignment: use local DB, not API. :contentReference[oaicite:2]{index=2}
    """
    mmdb_path: str
    _reader: Optional[geoip2.database.Reader] = None

    def __enter__(self) -> "GeoIPService":
        self._reader = geoip2.database.Reader(self.mmdb_path)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._reader is not None:
            self._reader.close()
        self._reader = None

    def country_name(self, ip: str) -> str:
        if self._reader is None:
            raise RuntimeError("GeoIPService must be used as a context manager (with GeoIPService(...) as svc:)")

        try:
            resp = self._reader.country(ip)
            name = (resp.country.name or "").strip()
            return name if name else "Unknown"
        except (ValueError, geoip2.errors.AddressNotFoundError, geoip2.errors.GeoIP2Error):
            return "Unknown"