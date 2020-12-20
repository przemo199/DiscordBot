import os
from scrapper import *
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():

    print('It works')


client.run(BOT_TOKEN)
