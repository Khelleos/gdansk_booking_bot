# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Telegram bot that polls the Gdansk voivodeship office's Qmatic booking API (`rezerwacja.gdansk.uw.gov.pl:8445`) and messages subscribers when appointment slots show up.

## Commands

```bash
pip install -r requirements.txt     # python-telegram-bot 22.8, aiohttp, python-dotenv
python booking_monitor_bot.py       # needs TELEGRAM_BOT_TOKEN in .env (fails at import time without it)
```

The project has no tests, linter or build step.

## Architecture

There are two modules:

- `booking_monitor_bot.py` holds the config, the Telegram command handlers (`/start`, `/stop`, `/check`, `/status`) and the background polling loop.
- `subscribers.py` keeps the subscriber chat IDs in a module-level `set` and writes them to `subscribers.json` on every add or remove. The path is relative, so the file goes in the current working directory.

How the parts fit together:

- `main()` builds a PTB `Application` and calls `run_polling`. The `post_init` hook saves `application.bot` into the global `bot_instance`, loads the subscribers, and starts `check_availability_loop()` with `asyncio.create_task`. The loop sends its alerts through that global, not through a handler context.
- Each check sends two requests in sequence:
  1. `API_URL` (`.../dates;servicePublicId=...;customSlotLength=40`) returns a list of `{date: ...}` items. An empty list means there are no slots.
  2. `fetch_times_for_date()` is then called for each date (`.../dates/{date}/times;...`) to get the times.

  `fetch_slots()` does both and returns `{date: [times]}`. `format_slots()` turns that into HTML, with each date's times in a collapsed `<blockquote expandable>`. It stops adding dates before the text gets near Telegram's 4096-character limit.
- The branch ID and service ID are hardcoded in both URLs. If you change the office or service, update both of them.
- TLS verification is turned off on purpose (`CERT_NONE`) because the booking server's certificate doesn't validate.
- `CHECK_INTERVAL` is a mutable global. It gets a new random value between 600 and 900 seconds after every check, so polling isn't regular.
- When sending an alert fails with "Forbidden" or "blocked", that subscriber is removed automatically.
- `check_availability()` (broadcast to everyone) and `show_check_result()` (`/check` and the "🔄 Check again" button) share `fetch_slots()`/`format_slots()`. A manual check edits its "Checking..." message in place rather than sending a new one.
- `post_init` registers the command menu with `set_my_commands(BOT_COMMANDS)`. When you add a command, add it there too.
- `last_check_at`, `last_check_result` and `next_check_at` are globals that the loop updates and `/status` reads. Manual checks don't change them.

## Sensitive files

`.env` holds the bot token. `keys/` holds the DigitalOcean SSH keys for the deployment host. `subscribers.json` is runtime data. All three are gitignored; don't read them or commit them.
