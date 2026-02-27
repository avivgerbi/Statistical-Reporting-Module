# Statistical Reporting Module

This module analyzes an Apache web server log file and generates a statistical report showing the percentage of requests by Country, Operating System (OS), and Browser.  
The system is designed with a modular and extensible architecture, allowing easy addition of new reporting dimensions.

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
````

Download the GeoLite2 Country database from MaxMind and place the file `GeoLite2-Country.mmdb` in the project directory.

---

## Usage

Run the module with:

```bash
python -m stat_report.cli --log apache_log.txt --geoip GeoLite2-Country.mmdb
```

The program will output the percentage distribution of requests by Country, OS, and Browser.
