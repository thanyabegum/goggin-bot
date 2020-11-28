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

async def wait_until(dt):
    # sleep until the specified datetime
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())

async def run_at(dt, coro):
    await wait_until(dt)
    return await coro

client = discord.Client()

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
	client.loop.create_task(run_at(date, remind(author,name)))
	await ctx.send(message)


db = sqlite3.connect('guild_config.db')
c = db.cursor()
c.execute("SELECT user, event_date FROM events WHERE user=?", ("ArmyGuy741",))
rows = c.fetchall()
for row in rows:
	print(row)


bot.run(TOKEN)