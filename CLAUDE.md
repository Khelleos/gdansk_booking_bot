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

There are four modules:

- `booking_monitor_bot.py` holds the config, the Telegram command handlers (`/start`, `/stop`, `/check`, `/status`, `/language`) and the background polling loop. It holds no user-facing text.
- `messages.py` builds every user-facing message. Each function takes a language code first and returns the text, along with the date, slot and duration formatting and the plural rules.
- `translations.py` holds only data: `STRINGS[lang][key]` templates, `MONTHS`, `WEEKDAYS` and `LANGUAGES` (en, pl, ru, uk, be). Tuple values are plural forms: two for English, three (one/few/many) for the Slavic languages. When you add a string, add it to all five languages. A missing key falls back to English.
- `subscribers.py` keeps the subscribers in a module-level dict `{chat_id: language}` and writes it to `subscribers.json` as `{"subscribers": [{"id": ..., "language": ...}]}` on every change. The loader also accepts the old format, a list of bare IDs, and gives those subscribers `en`. The path is relative, so the file goes in the current working directory.

How the parts fit together:

- `main()` builds a PTB `Application` and calls `run_polling`. The `post_init` hook saves `application.bot` into the global `bot_instance`, loads the subscribers, and starts `check_availability_loop()` with `asyncio.create_task`. The loop sends its alerts through that global, not through a handler context.
- Each check sends two requests in sequence:
  1. `API_URL` (`.../dates;servicePublicId=...;customSlotLength=40`) returns a list of `{date: ...}` items. An empty list means there are no slots.
  2. `fetch_times_for_date()` is then called for each date (`.../dates/{date}/times;...`) to get the times.

  `fetch_slots()` does both and returns `{date: [times]}`. `messages.format_slots()` turns that into HTML, with each date's times in a collapsed `<blockquote expandable>`. It stops adding dates before the text gets near Telegram's 4096-character limit.
- The branch ID and service ID are hardcoded in both URLs. If you change the office or service, update both of them.
- TLS verification is turned off on purpose (`CERT_NONE`) because the booking server's certificate doesn't validate.
- `CHECK_INTERVAL` is a mutable global. It gets a new random value between 600 and 900 seconds after every check, so polling isn't regular.
- When sending an alert fails with "Forbidden" or "blocked", that subscriber is removed automatically.
- `check_availability()` (broadcast to everyone) and `show_check_result()` (`/check` and the "🔄 Check again" button) share `fetch_slots()`. A manual check edits its "Checking..." message in place rather than sending a new one. A broadcast renders the alert once per language and sends each subscriber the version in their language.
- `chat_language()` picks a chat's language in this order: the language saved for the subscriber, then `context.chat_data['language']` (a choice made while unsubscribed, kept in memory only until restart), then the Telegram app's `language_code`, then `en`. `/start` saves the language it picked.
- `post_init` registers the command menu once per language with `set_my_commands(..., language_code=...)`. Choosing a language with `/language` also sets a per-chat menu (`BotCommandScopeChat`). When you add a command, add it to `messages.command_descriptions()`.
- `last_check_at`, `last_check_result` and `next_check_at` are globals that the loop updates and `/status` reads. `last_check_result` is a `(result, dates)` pair, not text, so `/status` can show it in each reader's language. Manual checks don't change them.

## Sensitive files

`.env` holds the bot token. `keys/` holds the DigitalOcean SSH keys for the deployment host. `subscribers.json` is runtime data. All three are gitignored; don't read them or commit them.
