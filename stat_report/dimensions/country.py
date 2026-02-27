from dataclasses import dataclass
from .base import Dimension
from stat_report.models import LogRecord
from stat_report.geoip_service import GeoIPService

@dataclass(frozen=True)
class CountryDimension(Dimension):
    geoip: GeoIPService

    def __init__(self, geoip: GeoIPService):
        object.__setattr__(self, "name", "Country")
        object.__setattr__(self, "geoip", geoip)

    def extract(self, record: LogRecord) -> str:
        return self.geoip.country_name(record.ip)