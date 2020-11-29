# Goggin-Bot
Goggin-Bot is not just any reminder-bot for Discord; Goggin emulates the hardest man on the planet: David Goggins. He'll remind you to get your work done and make sure you stay hard!

## Installation and Usage

To install, download the repository and execute the following command in the terminal:

`pip install -r requirements.txt`

In the same directory as the code, create a `.env file` that contains the following information: 

`DISCORD_TOKEN=<discord-bot-token>` where `<discord-bot-token>` is replaced by a string of your bot's token.

Before running, edit line 16 in the `bot.py` file to your server's desired prefix. Finally, run `bot.py` by executing the command `python3 bot.py` in the terminal.

## Commands

The prefix used in the following command examples will be `!`, so execute the commands using the prefix you assigned.

`!remind "<insert name of event" <insert date and time in whatever format please>` For example,


`!remind "Study for test" Dec 15th 2020 8 AM` will create a reminder to study on December 15th, 2020 at 8:00 AM.

`!motivate <optional tag user>` For example, to send a motivational quote to a specified person, execute:

`!motivate @person` to have the bot send a DM with a quote from David Goggins. If no person is specified, the bot will send the quote in the channel the command was executed.
