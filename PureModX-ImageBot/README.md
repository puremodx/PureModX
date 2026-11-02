# PureModX Image Bot

A Python Telegram bot starter using long polling.

## Features

- `/start` welcome message
- `/help` and `/cancel`
- Receives text prompts and replies with a confirmation
- Uses the Telegram Bot API directly through `requests`

## Setup

1. Install Python 3.10+.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set the `BOT_TOKEN` environment variable in your hosting provider.
4. Run: `python bot.py`.

Never put a real bot token in source code, commits, screenshots, or public issues.
If a token has been exposed, revoke it with BotFather and use a fresh token.

## Image generation

This repository currently contains the Telegram bot foundation only. A generator adapter is not included yet. Integration with the original Perchance website must not automate its service contrary to its terms. Add an authorized API or obtain explicit permission before connecting a generator.

## Hosting notes

Run exactly one polling instance for this bot token. Do not run polling alongside an active webhook or another getUpdates process.
