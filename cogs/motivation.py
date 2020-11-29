import discord
import requests

from discord.ext import commands
from random import randint
from bs4 import BeautifulSoup

url = 'https://www.spongecoach.com/david-goggins-quotes/' # Where quotes are sourced
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

quotes = soup.find(class_ = 'td-post-content')
quotes_items = quotes.find_all('p')

fixedQuotes = []

for quote in quotes_items:
	quote = quote.get_text()
	fixedQuotes.append(quote)

for i in range(5):
	fixedQuotes.pop(0)

for i in range(3):
	fixedQuotes.pop(-1)

quotesLength = len(fixedQuotes)

class Motivation(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(help="I'll motivate your punk ass.")
	async def motivate(self, ctx, user: discord.User = None):
		index = randint(0,quotesLength-1) # Choosing a random quote
		q = fixedQuotes[index]
		q = q[4:-16]
		embed = discord.Embed(description=q)
		if user:
			await user.send(content=None, embed=embed)
		else:
			await ctx.send(content=None, embed=embed)

def setup(client):
	client.add_cog(Motivation(client))


