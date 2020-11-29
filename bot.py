import discord
import os
import sqlite3
import asyncio

from dateutil.parser import *
from dateutil.tz import * 
import datetime


from dotenv import load_dotenv
from discord.ext import commands
from contextlib import closing

from collections.abc import Sequence

def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def reaction_check(message=None, emoji=None, author=None, ignore_bot=True):
    message = make_sequence(message)
    message = tuple(m.id for m in message)
    emoji = make_sequence(emoji)
    author = make_sequence(author)
    def check(reaction, user):
        if ignore_bot and user.bot:
            return False
        if message and reaction.message.id not in message:
            return False
        if emoji and reaction.emoji not in emoji:
            return False
        if author and user not in author:
            return False
        return True
    return check

async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())

async def run_at(dt, coro):
    await wait_until(dt)
    return await coro

with closing(sqlite3.connect('guild_config.db')) as db:
    with closing(db.cursor()) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS events
                     (user TEXT,
                      name TEXT,
                      event_date TEXT,
                      event_time TEXT
                      )
                  ''')
        c.execute('''CREATE TABLE IF NOT EXISTS eventCounter
                      (username TEXT PRIMARY KEY UNIQUE NOT NULL,
                       numEvents INTEGER)
                  ''')

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

# Functions created to execute task at specific time
async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())

async def run_at(dt, coro):
    await wait_until(dt)
    return await coro


async def remind(author,name):
	embed = discord.Embed(title="Reminder", description="This is your reminder")
	embed.add_field(name="The Reminder", value=f"You have {name}")
	await author.send(content=None, embed=embed)

bot = commands.Bot(command_prefix='!')

@bot.command()
async def DM(ctx, user: discord.User, *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)

@bot.command()
async def create(ctx, name, ti, event_date):
	author = ctx.message.author
	message = f"You created a reminder for {name} at {ti} on {event_date}"

	with closing(sqlite3.connect('guild_config.db')) as db:
	    with closing(db.cursor()) as c:
	        c.execute('''INSERT INTO events(user, name, event_date, event_time) VALUES (?, ?, ?, ?)''',
	        (author.name, name, event_date, ti))
	    db.commit()

	date = parse(ti + " " + event_date)
	now = datetime.datetime.now()
	timeDelta = date - now

	msg = await ctx.send(message)

	emoji0 = '0️⃣' # when the event happens 
	emoji1 = '1️⃣' # 10 minutes
	emoji2 = '2️⃣' # 30 mins
	emoji3 = '3️⃣' # 1 hour
	emoji4 = '4️⃣' # 1 day
	await msg.add_reaction(emoji0)
	await msg.add_reaction(emoji1)
	await msg.add_reaction(emoji2)
	await msg.add_reaction(emoji3)
	await msg.add_reaction(emoji4)
	counter0 = counter1 = counter2 = counter3 = counter4 = 0
	loopclose = 0
	while loopclose == 0:
		check = reaction_check(message=msg, author=ctx.author, emoji=(emoji0,emoji1,emoji2,emoji3,emoji4))

		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=timeDelta.seconds, check=check)

			if str(reaction.emoji) == emoji0:
				print("Emoji0 was pressed")
				counter0 += 1
				if counter0 == 1:
					task0 = client.loop.create_task(run_at(date, remind(author,name)))

			elif str(reaction.emoji) == emoji1:
				print("Emoji1 was pressed")
				counter1 += 1
				if counter1 == 1:
					modifiedDate = date - datetime.timedelta(minutes=10)
					task1 = client.loop.create_task(run_at(modifiedDate, remind(author,name)))

			elif str(reaction.emoji) == emoji2:
				print("Emoji2 was pressed")
				counter2 += 1
				if counter2 == 1:
					modifiedDate = date - datetime.timedelta(minutes=30)
					task2 = client.loop.create_task(run_at(modifiedDate, remind(author,name)))

			elif str(reaction.emoji) == emoji3:
				print("Emoji3 was pressed")
				counter3 += 1
				if counter3 == 1:
					modifiedDate = date - datetime.timedelta(hours=1)
					task3 = client.loop.create_task(run_at(modifiedDate, remind(author,name)))

			elif str(reaction.emoji) == emoji4:
				print("Emoji4 was pressed")
				counter4 += 1
				if counter4 == 1:
					modifiedDate = date - datetime.timedelta(days=1)
					task4 = client.loop.create_task(run_at(modifiedDate, remind(author,name)))
			

			# if str(reaction1.emoji) == emoji0:
			# 	task0.cancel()

		except asyncio.TimeoutError:
			print("Successfully timed out")
			loopclose = 1

# db = sqlite3.connect('guild_config.db')
# c = db.cursor()
# c.execute("SELECT user, event_date FROM events WHERE user=?", ("ArmyGuy741",))
# rows = c.fetchall()
# for row in rows:
# 	print(row)


bot.run(TOKEN)