# Gdansk Booking Monitor Bot

A Telegram bot that monitors appointment availability at the Gdansk office and sends notifications when slots become available.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided

### 3. Configure the Bot

Create a `.env` file in the project root:

```
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

### 4. Run the Bot

```bash
python booking_monitor_bot.py
```

## Commands

- `/start` - Subscribe to notifications
- `/stop` - Unsubscribe from notifications
- `/check` - Manually check availability now
- `/status` - View bot status
- `/language` - Change language (English, Polski, Русский, Українська, Беларуская)

## How It Works

- Checks booking availability every 10-15 minutes
- Notifies all subscribers when appointments become available
- Persists subscriber list and each subscriber's language across restarts (stored in `subscribers.json`)
- Uses the language of the user's Telegram app by default, if it's one of the supported ones
- Logs all activity to console

## Notes

- Bot token is stored in `.env` file (never commit this file)
- Subscriber data is stored in `subscribers.json` (auto-created on first run)

