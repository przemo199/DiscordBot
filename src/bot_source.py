import os
from scrapper import scrapper
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():

    print('It works')

@client.command()
async def get_price(ctx, *, nameOfGame):
    values = scrapper.main(nameOfGame)
    if values == False:
        await ctx.send('No Games Found')
    else:
        to_print = ''
        for line in values:
            to_print += f'Full Title: {line[0]}, Store Price: {line[1]}, Key Price: {line[2]}\n'
        await ctx.send(to_print)

client.run(BOT_TOKEN)
