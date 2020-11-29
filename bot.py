import discord
import os
import asyncio

from dateutil.parser import *
from dateutil.tz import * 
import datetime


from dotenv import load_dotenv
from discord.ext import commands
from contextlib import closing

from collections.abc import Sequence

PREFIX = '!' # Change to prefix desired on your personal server

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

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

async def sendRemind(author, name, date):
	# calculates the days until the event
	days = date - datetime.datetime.now()
	hours = days.days * 24 + days.seconds//3600
	if hours < 0:
		hours = 0

	# converts date to appropriate string representation
	# representation is: 0:00PM on Saturday, Oct 24 (in x hours)
	event_time = date.strftime("%I:%M%p on %A, %B %d, %Y")
	event_time += " (in " + str(hours) + " hours)"

	# creates embed
	embed = discord.Embed(
		title=name.title() + " Reminder",
		description="You've got an event coming up!")
	embed.set_footer(text="P.S. STAY HARD")
	embed.add_field(name="Event Time", value=date.strftime(event_time))
	await author.send(content=None, embed=embed)

bot = commands.Bot(command_prefix=PREFIX)

@bot.command(help="Set up a reminder by inputting the event name in quotes followed by the time and date.")
async def remind(ctx, name, *, time):
	author = ctx.message.author
 
	# reminder emojis
	emoji0 = '0️⃣' # when the event happens 
	emoji1 = '1️⃣' # 10 minutes
	emoji2 = '2️⃣' # 30 mins
	emoji3 = '3️⃣' # 1 hour
	emoji4 = '4️⃣' # 1 day

	# creates message to react to
	embed = discord.Embed(
		title="Set Reminders",
		description="When should I remind you?\n 0️⃣ At the time of the event\n 1️⃣ 10 minutes before event\n 2️⃣ 30 minutes before event\n 3️⃣ 1 hour before event\n 4️⃣ 1 day before event")
	embed.set_footer(text="Let me know with a reaction!")

	date = parse(time)
	now = datetime.datetime.now()
	timeDelta = date - now

	msg = await ctx.send(content=None, embed=embed)

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
					task0 = client.loop.create_task(run_at(date, sendRemind(author,name,date)))

			elif str(reaction.emoji) == emoji1:
				print("Emoji1 was pressed")
				counter1 += 1
				if counter1 == 1:
					modifiedDate = date - datetime.timedelta(minutes=10)
					task1 = client.loop.create_task(run_at(modifiedDate, sendRemind(author,name,date)))

			elif str(reaction.emoji) == emoji2:
				print("Emoji2 was pressed")
				counter2 += 1
				if counter2 == 1:
					modifiedDate = date - datetime.timedelta(minutes=30)
					task2 = client.loop.create_task(run_at(modifiedDate, sendRemind(author,name,date)))

			elif str(reaction.emoji) == emoji3:
				print("Emoji3 was pressed")
				counter3 += 1
				if counter3 == 1:
					modifiedDate = date - datetime.timedelta(hours=1)
					task3 = client.loop.create_task(run_at(modifiedDate, sendRemind(author,name,date)))

			elif str(reaction.emoji) == emoji4:
				print("Emoji4 was pressed")
				counter4 += 1
				if counter4 == 1:
					modifiedDate = date - datetime.timedelta(days=1)
					task4 = client.loop.create_task(run_at(modifiedDate, sendRemind(author,name,date)))

		except asyncio.TimeoutError:
			print("Successfully timed out")
			loopclose = 1

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)