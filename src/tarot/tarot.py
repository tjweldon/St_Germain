import aiohttp
import asyncio
import random
from src.tarot.magicEight import magicEightBall


async def tripleSpread(ctx):
    # Retrieves 3 random cards as JSON.
    # If API response is OK, creates a variable to hold the username and prepares cards.
    # Card orientation is represented as 0 or 1 (card meanings are tied to orientation)
    # Sends either the card name, or card name + * to represent a reversed card.

    async with aiohttp.ClientSession() as session:
        async with session.get("https://rws-cards-api.herokuapp.com/api/v1/cards/random?n=3") as spread:

            if spread.status == 200:
                someLines = '\n__ ' + '__ ' * 21  # buffer characters for visual formatting between messages
                user = str(ctx.author)  # the discord username of whoever seeks wisdom
                await ctx.send('Very well ' + user + someLines)
                cards = await spread.json()

                for card in range(3):
                    orientation = random.randint(0, 1)

                    if orientation == 0:
                        await ctx.send('***' + cards["cards"][card]["name"] + '***' +
                                       ' ***' + ':\n\n' + '***' +
                                       cards["cards"][card]["meaning_up"] + someLines
                                       )

                    elif orientation == 1:
                        await ctx.send("[Rev.] " +
                                       '***' + cards["cards"][card]["name"] + '***' +
                                       ' ***' + ':\n\n' + '***' +
                                       cards["cards"][card]["meaning_rev"] + someLines
                                       )

            else:
                await magicEightBall(ctx)
