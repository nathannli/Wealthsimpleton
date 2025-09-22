import getpass
import os
import shutil
import time
import tkinter as tk
from datetime import date, datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth

BASE_LINK = "https://my.wealthsimple.com"


# Function to get the screen width and height
def get_screen_dimensions():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


# Convert a date/time string from 'January 30' or 'January 30, 2024' format to a date
def convert_datetime(input_string):
    current_year = datetime.now().year
    if "," in input_string:
        date_format = "%B %d, %Y"
    else:
        date_format = "%B %d"
        input_string += f", {current_year}"  # Add the current year
    return datetime.strptime(input_string, date_format)


def delete_data_dir():
    dataDir = f"/home/{getpass.getuser()}/.config/google-chrome"
    if os.path.isdir(dataDir):
        shutil.rmtree(dataDir)


def get_transactions(
    account_activity_url_suffix: str, after_date: date = None
) -> list[dict]:
    delete_data_dir()
    print(f"{account_activity_url_suffix=}")
    account_activity_url = f"{BASE_LINK}/{account_activity_url_suffix}"
    print(f"{account_activity_url=}")
    # Setup Webdriver and load env. vars.
    screen_width, screen_height = get_screen_dimensions()
    window_width = screen_width // 2
    window_height = screen_height
    options = webdriver.ChromeOptions()
    options.add_argument(f"window-size={window_width},{window_height}")
    options.add_argument(f"window-position={screen_width},0")
    dataDir = f"/home/{getpass.getuser()}/.config/chromium"
    if not os.path.isdir(dataDir):
        dataDir = f"/home/{getpass.getuser()}/.config/google-chrome"
    if os.path.isdir(dataDir):
        options.add_argument(f"--user-data-dir={dataDir}")
        options.add_argument("--profile-directory=Default")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    driver.get(BASE_LINK)
    email = os.getenv("WS_EMAIL")
    password = os.getenv("WS_PASSWORD")
    if email:  # If not defined, you can login manually
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div > div > div > input"))
        )
        fields = driver.find_elements(By.CSS_SELECTOR, "div > div > div > input")
        fields[0].send_keys(email)
        fields[1].click()
    if password:  # If not defined, you can login manually
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div > div > div > input"))
        )
        fields = driver.find_elements(By.CSS_SELECTOR, "div > div > div > input")
        fields[1].send_keys(password)
        fields[0].click()
    if email and password:  # If not defined, you can login manually
        driver.find_elements(By.CSS_SELECTOR, "div > div > div > button").pop().click()
    WebDriverWait(driver, 3600).until(
        EC.url_changes(driver.current_url)
    )  # Long timeout needed for manual login or 2FA
    driver.get(account_activity_url)
    WebDriverWait(driver, 500).until(
        EC.presence_of_element_located((By.XPATH, "//button/div/div/div[2]/p[1]"))
    )
    time.sleep(
        2
    )  # If you need to scroll down to 'Load More', increase this timeout to have enough time to scroll manually (scrolling is not automated)
    tickers = driver.find_elements(By.XPATH, "//button/div/div/div[2]/p[1]")
    transactions = []
    for x in range(len(tickers)):
        ticker = driver.find_elements(By.XPATH, "//button/div/div/div[2]/p[1]")[x]
        transactionType = ticker.find_element(By.XPATH, "../div/p[1]")
        try:
            amount = ticker.find_element(By.XPATH, "../../../div[2]/p[1]")
        except:
            continue
        amount.click()
        time.sleep(1)
        details_div = amount.find_element(By.XPATH, "../../../../../div[2]")
        try:
            date = convert_datetime(
                details_div.find_element(
                    By.XPATH, "//p[text() = 'Date']/../div/div/p"
                ).text
            ).isoformat()
        except:
            try:
                date = convert_datetime(
                    details_div.find_element(
                        By.XPATH, "//p[text() = 'Filled']/../div/div/p"
                    ).text
                ).isoformat()
            except:
                date = convert_datetime(
                    details_div.find_element(
                        By.XPATH, "//p[text() = 'Submitted']/../div/div/p"
                    ).text
                ).isoformat()

        if after_date is not None:
            curr_date = datetime.fromisoformat(date)
            if after_date > curr_date:
                break

        transactions.append(
            {
                "description": ticker.text,
                "type": transactionType.text,
                "amount": amount.text,
                "date": date,
            }
        )
        amount.click()

    # Output
    return transactions


if __name__ == "__main__":
    transactions = get_transactions(after_date=None)
    print(transactions)
