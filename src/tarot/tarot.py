import aiohttp
import asyncio
import random
from src.tarot.magicEight import magicEightBall


async def cardDesc(ctx, first, second, third):
    # Retrieves the description of a card by its name.
    # Single search terms will return all cards containing that term in the name.
    # EG. Searching "Knight" will retrieve ALL Knights.
    # Searching a suit (Swords, Cups, Wands, Pentacles) will retrieve all cards in the suit.
    async with aiohttp.ClientSession() as session:
        async with session.get("https://rws-cards-api.herokuapp.com/api/v1/cards/") as deck:
            if deck.status == 200:

                if third == '':
                    cardName = first + ' ' + second

                if second == '':
                    cardName = first

                if third != '':
                    cardName = first + ' ' + second + ' ' + third

                fullDeck = await deck.json()
                allCards = range(fullDeck["nhits"])
                cardCount = 0
                for card in allCards:
                    if cardName in fullDeck["cards"][card]["name"]:
                        await ctx.send(fullDeck["cards"][card]["desc"])
                    if cardName not in fullDeck["cards"][card]["name"]:
                        cardCount += 1

                if cardCount > max(allCards):
                    await ctx.send("Please check your input. Search is case sensitive.\n"
                                   "Search either by a single term, or match the examples.\n"
                                   "Major Arcana: Wheel Of Fortune\n"
                                   "Minor Arcana: Knight of Swords\n"
                                   "Single Term: Knight / Ace / Devil etc.")


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
