import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = '.peepoo')

@client.event
async def on_ready():
    print('Ready to put the poo in the pee')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server. Good riddance.')
client.run(BOT_TOKEN)