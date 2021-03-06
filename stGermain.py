import discord
import logging
from discord.ext import commands
from src.server import keepAlive, token
from src.tarot.magicEight import magicEightBall
from src.tarot.tarot import tripleSpread, cardDesc, getCardImage, getMeanings
from src.guidance.userGuide import userGuide

logging.basicConfig()
description = 'St. Germain of The White Lodge'
intents = discord.Intents.default()

intents.members = True

bot = commands.Bot(
    command_prefix='!',
    description=description,
    intents=intents
)

TOKEN = token.replOrLocal(token.repl)


@bot.event
async def on_ready():
    print('The veil is parted.')
    print(bot.user.name + ' ' + 'has arrived.')
    print('~*~*~*~*~*~*~*~*~*')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="White Lodge Dreamers"
        )
    )


@bot.command()
async def guidance(ctx):
    await ctx.send(userGuide)


@bot.command()
async def add(ctx, left: int, right: int):
    # Adds two numbers
    await ctx.send(left + right)


@bot.command()
async def tarot(ctx):
    await tripleSpread(ctx)


@bot.command()
async def meaning(ctx, *, message=''):
    await getMeanings(ctx, message)


@bot.command()
async def describe(ctx, *, message=''):
    await cardDesc(ctx, message)


@bot.command()
async def image(ctx, *, message=''):
    await getCardImage(ctx, message)


@bot.command()
async def magicEight(ctx):
    await magicEightBall(ctx)


if token.repl is True:
    keepAlive.keepAlive()

bot.run(TOKEN)
