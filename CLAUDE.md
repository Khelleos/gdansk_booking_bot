# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Telegram bot that polls the Gdansk voivodeship office's Qmatic booking API (`rezerwacja.gdansk.uw.gov.pl:8445`) and messages subscribers when appointment slots show up. Qmatic is the vendor of the office's web booking system.

## Commands

```bash
pip install -r requirements.txt     # python-telegram-bot 22.8, aiohttp, python-dotenv
python booking_monitor_bot.py       # needs TELEGRAM_BOT_TOKEN in .env
python -m unittest                  # run all tests (stdlib unittest, no extra dependencies)
python -m unittest tests.test_messages   # run one test module
```

There's no linter or build step. `booking_monitor_bot.py` is only a launcher for `bot.main.main()`. The systemd unit on the droplet runs it, so keep the file.

## Architecture

The code lives in the `bot/` package. Dependencies point one way: `main` → `handlers` and `monitor` → `qmatic`, `storage`, `i18n` and `keyboards` → `config`. `qmatic`, `storage` and `i18n` don't import Telegram.

- `config.py` holds the booking URL, `BRANCH_ID` (the office), `SERVICE_ID` (the appointment type), the timeouts and `CHECK_INTERVAL_RANGE`. `load()` reads `.env` from the project root and returns a frozen `Config` (token and subscribers file path). It runs from `main()`, so importing modules needs no token.
- `qmatic.py` has `QmaticClient`, which makes all the HTTP calls and builds both URLs from the IDs:
  - `fetch_dates()` calls `.../dates;servicePublicId=...;customSlotLength=40`. It raises on network errors and non-200 responses.
  - `fetch_times(date)` calls `.../dates/{date}/times;...` and returns `[]` on any failure.
  - `fetch_slots()` returns `{date: [times]}`, and an empty dict when there are no slots.

  The client keeps one aiohttp session, created on first use and closed in `post_shutdown`. TLS verification is off on purpose (`CERT_NONE`) because the booking server's certificate doesn't validate.
- `monitor.py` has `Monitor`, the background loop that `post_init` starts with `asyncio.create_task`. After each check it picks a new random interval from `CHECK_INTERVAL_RANGE`, so polling isn't regular. When there are slots, it renders the alert once per language and sends each subscriber their version. A subscriber whose send fails with "Forbidden" or "blocked" is removed. Its `last_check_at`, `last_result` and `next_check_at` are what `/status` shows. `last_result` is a `(result, dates)` pair, not text, so it can be shown in any language. Manual checks don't change these values.
- `storage.py` has `SubscriberStore`, a dict `{chat_id: language}` saved to `subscribers.json` in the project root as `{"subscribers": [{"id": ..., "language": ...}]}` on every change. It writes `subscribers.json.tmp` first and swaps it in with `os.replace`. The loader also accepts the old format (a list of bare IDs) and gives those subscribers `en`.
- `handlers.py` holds the command and button handlers (`/start`, `/stop`, `/check`, `/status`, `/language`, the "🔄 Check again" and language buttons) and `register()`. Shared objects come from `application.bot_data`: `"store"`, `"client"` and `"monitor"`, set up in `main.py`. A manual check edits its "Checking..." message in place rather than sending a new one.
- `chat_language()` in `handlers.py` picks a chat's language in this order:
  1. the language saved for the subscriber;
  2. `context.chat_data['language']`, a choice made while unsubscribed, kept in memory until restart;
  3. the Telegram app's `language_code`;
  4. `en`.

  `/start` saves the language it picked.
- `keyboards.py` holds the inline buttons, the language picker, the callback data constants and `bot_commands(lang)`.
- `main.py` sets up logging and wires everything together. `post_init` registers a command menu for each language with `set_my_commands(..., language_code=...)`, loads the subscribers and starts the monitor. Choosing a language with `/language` also sets a menu for that chat (`BotCommandScopeChat`). When you add a command, add it to `messages.command_descriptions()` and `handlers.register()`.

### Translations (`bot/i18n/`)

- `messages.py` builds every user-facing message. Each function takes a language code first and returns the text. It also formats dates, slot lists and durations and applies the plural rules. No other module contains user-facing text.
- `locales/{en,pl,ru,uk,be}.py` hold only data: `NAME`, `MONTHS` (in the form used after a day number), `WEEKDAYS` and `STRINGS`. `locales/__init__.py` collects them into the `LANGUAGES`, `MONTHS`, `WEEKDAYS` and `STRINGS` tables. In `STRINGS`, tuple values are plural forms: two for English, three (one/few/many) for the Slavic languages.
- When you add a string, add it to all five locale files; `tests/test_messages.py` checks that the keys match. A missing key falls back to English.
- `messages.format_slots()` puts each date's times in a collapsed `<blockquote expandable>`. It stops adding dates before the text gets near Telegram's 4096-character limit.

## Sensitive files

`.env` holds the bot token. `keys/` holds the DigitalOcean SSH keys for the deployment host. `subscribers.json` is runtime data. All three are gitignored; don't read them or commit them.
