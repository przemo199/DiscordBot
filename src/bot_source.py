import os

from discord.ext import commands
from dotenv import load_dotenv

from scrapper import scrapper

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():
    print('It works')


@client.command()
async def get_price(ctx, *, name_of_game):
    values = scrapper.main(name_of_game)

    if not values:
        await ctx.send('No Games Found')
    else:
        to_print = ''
        for line in values:
            to_print += f'Full Title: {line[0]}, Store Price: {line[1]}, Key Price: {line[2]}\n'
        await ctx.send(to_print)


client.run(BOT_TOKEN)
