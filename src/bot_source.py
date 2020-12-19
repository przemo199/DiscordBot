import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('I fucking hate jannies')

client.run(BOT_TOKEN)