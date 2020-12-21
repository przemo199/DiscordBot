import os

from discord.ext import commands
from dotenv import load_dotenv

from scrappers import amazon_scrapper
from scrappers import game_scrapper
from scrappers import newegg_scrapper

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix = '.')

separator = '\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'


@client.event
async def on_ready():
    print('It works')


@client.command()
async def get_price_gg(ctx, *, name_of_game):
    values = game_scrapper.searchforgame(name_of_game)

    if not values:
        await ctx.send('No Games Found')
    else:
        to_print = separator
        for line in values:
            to_print += f'**Title:** {line[0]}\n**Store Price:** {line[1]}\n**Keyshop Price:** {line[2]}\n' \
                        f'**Metascore:** {line[3]}\n**Userscore:** {line[4]}{separator}'

        await ctx.send(to_print)


@client.command()
async def get_price_newegg(ctx, *, name_of_item):
    values = newegg_scrapper.main(name_of_item)

    if not values:
        await ctx.send('No Items Found')
    else:
        to_print = '```'
        to_print += separator
        for line in values:
            to_print += f'Full Title: {line[0]}, Rating: {line[1]}, Number of Reviews: {line[2]}, Price: {line[3]}{separator}'
        to_print += '```'
        await ctx.send(to_print)


@client.command()
async def get_price_amazon(ctx, *, item_name):
    links = amazon_scrapper.searchforproduct(item_name)

    if not links:
        await ctx.send('No Items Found')
    else:
        to_print = separator
        for link in links[:5]:
            details = amazon_scrapper.getdetails(link)
            to_print += f'**Full Title:** {details[0]}\n**Price:** {details[1]}\n**Used price:** {details[2]}\n' \
                        f'**Rating:** {details[3]}\n**Reviews:** {details[4]}\n**Delivery:** {details[5]}\n' \
                        f'**Link:** <{link}>{separator}'

        await ctx.send(to_print)


client.run(BOT_TOKEN)
