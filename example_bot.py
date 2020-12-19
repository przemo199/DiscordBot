import discord
from discord.ext import commands

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

client.run('Nzg5OTQ2MzI0OTE2NTAyNTMw.X95c2A.CX5_wFTk0cje_DaW1Vdn7y6ENZY')