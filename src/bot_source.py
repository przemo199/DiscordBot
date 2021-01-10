"""Main file for discord bot"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from scrappers import amazon_scrapper
from scrappers import currency_scrapper
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
        to_print = '** **\n'
        to_print += '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
        for line in values:
            to_print += f'**{line[0]}**\n**Price**: {line[1]}\n**Number of Reviews**: {line[2]}\n**Rating**: {line[3]}\n<{line[4]}>{separator}'
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


@client.command()
async def get_currency_exchange(ctx, *args):
    args = list(args)

    if len(args) == 3:
        request = args[0].upper() + ' ' + args[1].lower() + ' ' + args[2].upper()
    else:
        request = args[1].upper() + ' ' + args[2].lower() + ' ' + args[3].upper()

    details = currency_scrapper.getdetails(request)
    details[1] = details[1].replace('.', '')

    embed = discord.Embed(title = request)
    if len(args) == 4:
        embed = discord.Embed(title = request,
                              description = f'{args[0]} {args[1].upper()} = {round(float(details[0]) * float(args[0]), 2)}'
                                            f' {args[3].upper()} {details[1]}')
    else:
        embed = discord.Embed(title = request,
                              description = f'1 {args[0].upper} = {details[0]} {args[2].upper} {details[1]}')
        embed.add_field(name = 'Previous close:', value = details[2])
        embed.add_field(name = 'Open:', value = details[3])
        embed.add_field(name = '52-week range:', value = details[4])

    await ctx.send(embed = embed)


client.run(BOT_TOKEN)
