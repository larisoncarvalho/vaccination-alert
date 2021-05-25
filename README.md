# Vaccination alert bot

#### A Telegram bot that alerts you when vaccination slots are available for the 18-45 age group in Goa.

This bot can be easily modified to run on other platforms like discord and to check for vaccination slots in other states and age groups.

### Installation and usage
Install requirements using
`pip install --no-cache-dir -r requirements.txt`

Create a Telegram bot
https://core.telegram.org/bots

Create an environment variable called `TOKEN` with its value as the Telegram bot token

Start the bot by running
`python run.py`

You can create an alert by running the command `/alert_district <district> <dose>`
`district` can be north or south
`dose` can be 1 or 2

#### Docker
You can also run this bot in a container by building using the provided dockerfile.

Replace `<token>` in the dockerfile with your Telegram bot token
Build the image using
`docker build -t telegram-cowin-bot .`
Run the image using
`docker run telegram-cowin-bot`

### Disclaimer
Please do not use this bot as your only source of information. This is only meant to be an extra tool to aid you.
The Co-Win API is subject to a rate limit of 100 calls per 5 minutes and the data is cached so it maybe upto 30 minutes old
