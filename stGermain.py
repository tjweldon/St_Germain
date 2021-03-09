import discord
import logging
from discord.ext import commands
from src.server import keepAlive, token
from src.tarot.magicEight import magicEightBall
from src.tarot.tarot import tarotSpread, cardDesc, getCardImage, getMeanings
from src.guidance.userGuide import userGuide

# Bot setup.
logging.basicConfig()
description = 'St. Germain of The White Lodge'
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    description=description,
    intents=intents
)

# Get correct API token path.
TOKEN = token.replOrLocal(token.repl, token.devFlag)

# Channel ID for inChannel check.
whiteLodgeChannel = 817823496352169985


# Decorator for limiting commands per channel.
def inChannels(*args):
    def predicate(ctx):
        return ctx.message.channel.id in args

    return commands.check(predicate)


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
@inChannels(whiteLodgeChannel)
async def tarot(ctx, number=3):
    await tarotSpread(ctx, number)


@bot.command()
@inChannels(whiteLodgeChannel)
async def meaning(ctx, *, message=''):
    await getMeanings(ctx, message)


@bot.command()
@inChannels(whiteLodgeChannel)
async def describe(ctx, *, message=''):
    await cardDesc(ctx, message)


@bot.command()
@inChannels(whiteLodgeChannel)
async def image(ctx, *, message=''):
    await getCardImage(ctx, message)


@bot.command()
async def magicEight(ctx, *, message='question'):
    await magicEightBall(ctx, message)


if token.repl is True:
    keepAlive.keepAlive()

bot.run(TOKEN)
