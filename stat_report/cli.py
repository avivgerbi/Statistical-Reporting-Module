from __future__ import annotations

import argparse
import sys

from .geoip_service import GeoIPService
from .ua_service import UserAgentService
from .log_parser import iter_records
from .dimensions.country import CountryDimension
from .dimensions.os import OSDimension
from .dimensions.browser import BrowserDimension
from .aggregator import StatsAggregator
from .report import ReportConfig, format_report

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="stat-report",
        description="Generate statistical report (Country/OS/Browser) from Apache logs."
    )
    p.add_argument("--log", required=True, help="Path to apache log file (10K lines).")
    p.add_argument("--geoip", required=True, help="Path to GeoLite2 Country mmdb file.")
    p.add_argument("--top-k", type=int, default=5, help="Number of top entries per dimension before 'Other'.")
    p.add_argument("--no-other", action="store_true", help="Disable 'Other' bucket.")
    return p

def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    cfg = ReportConfig(top_k=max(args.top_k, 0), include_other=(not args.no_other))
    ua = UserAgentService()

    try:
        with GeoIPService(args.geoip) as geoip:
            dims = [
                CountryDimension(geoip),
                OSDimension(ua),
                BrowserDimension(ua),
            ]
            aggregator = StatsAggregator(dims)

            with open(args.log, "r", encoding="utf-8", errors="replace") as fp:
                result = aggregator.consume(iter_records(fp))

            out = format_report(result.counts_by_dimension, result.total, cfg)
            sys.stdout.write(out)
        return 0
    except FileNotFoundError as e:
        sys.stderr.write(f"File not found: {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())