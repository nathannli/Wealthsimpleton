# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Wealthsimpleton is a Python package that scrapes Wealthsimple activity history using Selenium WebDriver. It's a fork designed to be installable as a pip package with output intended for use in other scripts.

## Installation and Setup

Install the package in development mode:
```bash
pip install -e .
```

Install from a path:
```bash
pip install ../Wealthsimpleton/
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Prerequisites

- Python 3.8+
- Chromium or Google Chrome installed
- Chrome WebDriver compatible with your browser version
- Optional: `.env` file with `WS_EMAIL` and `WS_PASSWORD` in your consuming script's directory (NOT in this repo)

## Core Architecture

### Main Module: `wealthsimpleton/wealthsimpleton.py`

The package exposes a single primary function `get_transactions()` that:

1. **Browser Setup**: Configures Chrome WebDriver with stealth settings to avoid bot detection
   - Uses selenium-stealth to mask automation
   - Configures browser window to half-screen width positioned on right side
   - Attempts to use existing Chrome profile from `~/.config/chromium` or `~/.config/google-chrome`

2. **Authentication Flow**:
   - Supports automated login via `WS_EMAIL` and `WS_PASSWORD` env vars
   - Falls back to manual login with 3600s timeout for 2FA/CAPTCHA
   - Waits for URL change to confirm authentication

3. **Transaction Scraping**:
   - Navigates to account activity page via `account_activity_url_suffix` parameter
   - Requires manual user intervention: user must click "Load More" repeatedly to load all transactions, then type 'ok'
   - Scrapes transaction elements using XPath selectors
   - Clicks each transaction to extract date from detail view
   - Supports filtering by `after_date` parameter to stop scraping at a specific date

4. **Date Parsing**:
   - Handles two formats: "January 30" and "January 30, 2024"
   - Assumes current year if year not specified
   - Attempts to extract date from multiple possible fields: 'Date', 'Filled', or 'Submitted'
   - See wealthsimpleton.py:26-34 for `convert_datetime()` implementation

### Return Format

Returns a list of dictionaries with:
- `description`: Transaction ticker/name
- `type`: Transaction type (buy, sell, etc.)
- `amount`: Transaction amount as string
- `date`: ISO format datetime string

## Important Implementation Notes

### Environment Variable Location
The `.env` file should be placed with your consuming scripts, NOT in this repository. The README explicitly states this is for users loading env vars with `dotenv` in their own scripts.

### Browser Profile Management
The `delete_data_dir()` function (line 37-40) removes the Google Chrome data directory at the start of execution. This is called before browser initialization in `get_transactions()`.

### Manual Interaction Required
The scraper requires manual user interaction to:
- Complete 2FA/CAPTCHA during login
- Click "Load More" to paginate through all transactions
- Type 'ok' after scrolling back to top

This is by design - the script pauses execution waiting for user input at line 104-106.

### XPath Selectors
The scraper relies on specific XPath patterns (lines 101, 108, 111-137) that may break if Wealthsimple changes their UI structure. When debugging scraping issues, check these selectors first.

## Package Structure

```
wealthsimpleton/
├── __init__.py          # Exports get_transactions
└── wealthsimpleton.py   # Main scraping logic
```

The package is minimal by design - it exposes only `get_transactions()` through `__init__.py` for importing into other scripts.
