# Gdansk Booking Monitor Bot

A Telegram bot that monitors appointment availability at the Gdansk office and sends notifications when slots become available.

## Features

- 🔄 Automatic periodic checking (every 5 minutes by default)
- 📢 Instant notifications when appointments are available
- 👥 Multiple user support
- 🎯 Manual availability checks
- ⚙️ Easy configuration

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided

### 3. Configure the Bot

Edit `booking_monitor_bot.py` and replace:
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```
with your actual bot token.

### 4. Run the Bot

```bash
python booking_monitor_bot.py
```

Or make it executable and run directly:
```bash
chmod +x booking_monitor_bot.py
./booking_monitor_bot.py
```

## Usage

### Commands

- `/start` - Subscribe to notifications
- `/stop` - Unsubscribe from notifications
- `/check` - Manually check availability now
- `/status` - View bot status and subscription info

### Configuration

You can adjust these settings in the script:

- `CHECK_INTERVAL` - Time between checks (in seconds, default: 300 = 5 minutes)
- `API_URL` - The booking API endpoint (already configured)

## Running as a Service

To keep the bot running continuously, you can use a process manager like systemd or screen/tmux.

### Using systemd (Linux)

Create `/etc/systemd/system/booking-bot.service`:

```ini
[Unit]
Description=Gdansk Booking Monitor Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/bot/directory
ExecStart=/usr/bin/python3 /path/to/bot/directory/booking_monitor_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable booking-bot
sudo systemctl start booking-bot
sudo systemctl status booking-bot
```

## Troubleshooting

- **Bot not responding**: Check that your token is correct and the bot is running
- **No notifications**: Ensure you've sent `/start` to the bot
- **Connection errors**: Check your internet connection and API availability

## Notes

- The bot checks the booking API every 5 minutes by default
- All subscribers receive notifications when availability is detected
- The bot only sends notifications when the API response is not empty
- Logs are displayed in the console for monitoring
