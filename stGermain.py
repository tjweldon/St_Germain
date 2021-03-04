import discord
import logging
import json
from discord.ext import commands
from src.server import keepAlive
from src.tarot.magicEight import magicEightBall
from src.tarot.tarot import tripleSpread, cardDesc

logging.basicConfig()
description = 'St. Germain of The White Lodge'
intents = discord.Intents.default()

intents.members = True

bot = commands.Bot(
    command_prefix='!',
    description=description,
    intents=intents
)

with open("data/stGermain.json", "r") as configjsonFile:
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
async def tarot(ctx):
    await tripleSpread(ctx)


@bot.command()
async def describe(ctx, first='', second='', third=''):
    await cardDesc(ctx, first, second, third)


@bot.command()
async def magicEight(ctx):
    await magicEightBall(ctx)

keepAlive.keepAlive()
bot.run(TOKEN)
