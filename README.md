# Wealthsimpleton
fork from https://github.com/ImranR98/Wealthsimpleton

A Python script that scrapes your Wealthsimple activity history and saves the data in a JSON file.
This repo has been modified so that it is installable as a pip package, and it's scraping output are meant to be used directly in other scripts.

The data scraped includes:
- Transaction description
- Transaction type
- Transaction amount
- Transaction date

## Usage

0. recommended to be used on macos (tested on sequoia & tahoe). Had logging in/web scraping issues on linux (ubuntu)
1. Ensure Python dependencies are installed: `pip install -r requirements.txt`
2. Ensure you have Chromium or Google Chrome installed.
3. Ensure you have Chrome Webdriver installed and that it is compatible with the version of Chromium/Chrome you have.
4. Optionally, create a [`.env`](https://www.dotenv.org/docs/security/env.html) file with your Wealthsimple credentials defined as `WS_EMAIL` and `WS_PASSWORD` (or ensure those environment variables are present in some other way).
   - If you skip this, you will need to login manually when the script starts.
   - Note that even with these variables defined, you may still need to manually perform some login steps like 2FA or CAPTCHA.
   - recommended for speed
   - the `.env` file placement should be with your main scripts, not in this repo. Unless your environment variables are system-wide (i assume not), you are most likely using something like `dotenv` to temporarily load them in.
5. pip install ../Wealthsimpleton/  or pip install ../path to your Wealthsimpleton/