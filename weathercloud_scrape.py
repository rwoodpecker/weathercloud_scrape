from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import configparser
import os
import sys

config_access = configparser.ConfigParser()
config_location = os.path.join(
    os.path.expanduser("~"), ".config", "weathercloud_scrape.ini"
)


def init_config():
    def write_file():
        config_access.write(open(config_location, "w"))

    if not os.path.exists(config_location):
        print(f"Config file not found. Writing default to: {config_location}.")
        config_access["main"] = {"username": "username", "password": "password"}
        write_file()
        sys.exit(
            "Update the configuration file with your username and password and re-run the script"
        )


def read_setting(setting, section="main"):
    config_access.read(config_location)
    return config_access.get(section, setting)


def weathercloud_scrape():
    website = "https://app.weathercloud.net/signin"
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.automatic_downloads": 1}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get(website)

    all_matches_button = driver.find_element(
        By.XPATH, "//button[@class='btn btn-primary pull-right' and not(@disabled)]"
    )

    driver.execute_script("arguments[0].click();", all_matches_button)

    username_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[9]/div/div/div/div/form/div[1]/div/input")
        )
    )

    # wait a second, the site is slow.
    time.sleep(2)

    username_element.send_keys(read_setting("username"))

    password_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[9]/div/div/div/div/form/div[2]/div/input")
        )
    )
    password_element.send_keys(read_setting("password"))

    login_click = driver.find_element(
        By.XPATH, "/html/body/div[9]/div/div/div/div/form/div[4]/button"
    )

    driver.execute_script("arguments[0].click();", login_click)

    # dismiss the 30 day trial popup.

    dismiss_login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#free-trial-account > div:nth-child(1) > button:nth-child(1)",
            )
        )
    )

    driver.execute_script("arguments[0].click();", dismiss_login)

    # Click on the database page.

    click_database = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#header-main-menu > li:nth-child(3) > a > span",
            )
        )
    )

    driver.execute_script("arguments[0].click();", click_database)

    # select year

    dropdown_year = Select(
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[9]/div/div/div/div[1]/div/div[2]/div/select")
            )
        )
    )

    # select month

    dropdown_month = Select(
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[9]/div/div/div/div[1]/div/div[3]/div/select")
            )
        )
    )

    # click download button

    download_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[9]/div/div/div/div[2]/div/div[2]/a")
        )
    )

    # iterate through ALL years and months and download all available files. On a free account you can only access the last 12 months data

    for index in range(2, len(dropdown_year.options)):
        dropdown_year
        dropdown_year.select_by_index(index)
        print(f"Grabbing year: 202{index}")
        time.sleep(3)
        for index in range(1, len(dropdown_month.options)):
            dropdown_month
            dropdown_month.select_by_index(index)
            print(f"Grabbing month: {index}")
            time.sleep(3)
            driver.execute_script("arguments[0].click();", download_btn)
            time.sleep(6)


if __name__ == "__main__":
    init_config()
    weathercloud_scrape()
