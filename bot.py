import discord
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


client = discord.Client()

client.run(TOKEN)