import os

import discord
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
    print('Locked & loaded')


@client.command()
async def clear(ctx, arg):
    def is_me(message):
        return message.author == client.user

    await ctx.channel.purge(limit = arg, argcheck = is_me)


@client.command()
async def clear_all(ctx):
    await ctx.channel.purge(limit = 100000)


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
async def get_price_newegg(ctx, *, args):
    values = newegg_scrapper.main(args)

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
async def get_price_amazon(ctx, *args):
    links = amazon_scrapper.searchforproduct('+'.join(args))

    if not links:
        await ctx.send('No Items Found')
    else:
        count = 0
        skipped = 0
        for link in links:
            details = amazon_scrapper.getdetails(link)
            if details[1] == '-' and details[2] == '-':
                skipped += 1
                continue

            embed = discord.Embed(title = details[0], url = link, color = discord.Color.from_rgb(255, 153, 0))
            embed.add_field(name = 'Price:', value = details[1])
            embed.add_field(name = 'Used price:', value = details[2])
            embed.add_field(name = 'Delivery date:', value = details[3], inline = False)
            embed.add_field(name = 'Rating:', value = details[4])
            embed.add_field(name = 'Reviews:', value = details[5])
            embed.set_image(url = details[6])
            embed.set_footer(text = link)
            await ctx.send(embed = embed)

            count += 1
            if count > 4:
                break
        if skipped != 0:
            await ctx.send(f'```Skipped over {skipped} item(s) without price.```')


client.run(BOT_TOKEN)
