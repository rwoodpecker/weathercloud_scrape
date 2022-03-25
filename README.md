# weathercloud_scrape

Uses Selenium to download all available data from your personal weather station from weathercloud.net. On free accounts only the last 12 months of data is available.

## Requires:
* Python 3 (tested on version 3.9.10 but should run on any recent version)
* Selenium (pip3 install selenium)
* ChromeDriver to interact with Google Chrome (https://chromedriver.chromium.org/)
* The Google Chrome web browser installed.

## Running
* python3 weathercloud_scrape.py
* On the first run it will create a configuration file in .config/weathercloud_scrape.ini under your home directory. You must enter your username and password here then re-run the script.
