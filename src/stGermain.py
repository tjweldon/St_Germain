import discord
import logging
import random
import json
from discord.ext import commands

logging.basicConfig()
description = 'St. Germain of The White Lodge'
intents = discord.Intents.default()

intents.members = True

bot = commands.Bot(
    command_prefix='!',
    description=description,
    intents=intents
)

with open("../data/stGermain.json", "r") as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["API_TOKEN"]


@bot.event
async def on_ready():
    print('The veil is parted.')
    print(bot.user.name + ' ' + 'has arrived.')
    print('~*~*~*~*~*~*~*~*~*')


@bot.command()
async def add(ctx, left: int, right: int):
    # Adds two numbers
    await ctx.send(left + right)


@bot.command()
async def letters(ctx, amount):
    lettersList = ['a', 'b', 'c', 'd', 'e', 'f']
    user = str(ctx.author)
    if int(amount) <= len(lettersList):
        await ctx.send('Very well ' + user)
        for each in range(int(amount)):
            index = random.randint(0, len(lettersList) - 1)
            await ctx.send(lettersList[index])
            lettersList.remove(lettersList[index])

    else:
        await ctx.send('No.')


bot.run(TOKEN)
