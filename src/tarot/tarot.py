import io
import aiohttp
import random
import discord
from PIL import Image
from src.tarot.magicEight import magicEightBall


# Deprecated message parse function below.

# async def searchTerms(first, second, third) -> str:
#     """
#     Parses the users provided card name.
#     :param first: eg. "Knight"
#     :param second: eg. "of"
#     :param third: eg. "Swords"
#     :return: "Knight of Swords"
#     """
#     cardName = None
#     if third == '':
#         cardName = first + ' ' + second
#     if second == '':
#         cardName = first
#     if third != '':
#         cardName = first + ' ' + second + ' ' + third
#
#     # Ensures a blank search field doesn't send the entire list of cards.
#     if first == '':
#         cardName = 'invalid'
#
#     return cardName


async def getFullDeck():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://rws-cards-api.herokuapp.com/api/v1/cards/") as deck:
            if deck.status == 200:
                fullDeck = await deck.json()
                return fullDeck


async def checkInvalid(ctx, cardName):
    invalidTerms = [
        "Ace",
        "King",
        "Queen",
        "Knight",
        "Page",
        "Wands",
        "Cups",
        "Swords",
        "Pentacles",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "",
    ]
    if cardName in invalidTerms:
        await ctx.send("```" + "Please check your input. Search is case sensitive.\n"
                               "Images should be searched by complete name.\n"
                               "Major Arcana: Wheel Of Fortune\n"
                               "Minor Arcana: Knight of Swords\n" + "```")

        return False

    else:
        return True


async def getMeanings(ctx, message: str):
    cardName = message
    fullDeck = await getFullDeck()
    allCards = range(fullDeck["nhits"])

    meaning = ""
    meaningRev = ""

    validated = await checkInvalid(ctx, message)

    if validated is True:
        cardCount = 0
        for card in allCards:
            if cardName in fullDeck["cards"][card]["name"]:
                meaning = fullDeck["cards"][card]["meaning_up"]
                meaningRev = fullDeck["cards"][card]["meaning_rev"]

            if cardName not in fullDeck["cards"][card]["name"]:
                cardCount += 1

        if cardCount > max(allCards):
            await ctx.send("```" + "Please check your input. Search is case sensitive.\n"
                                   "Images should be searched by complete name.\n"
                                   "Major Arcana: Wheel Of Fortune\n"
                                   "Minor Arcana: Knight of Swords\n" + "```")

        else:
            await ctx.send("```" + f"Upright: {meaning}" + "```")
            await ctx.send("```" + f"Reversed: {meaningRev}" + "```")


async def getCardImage(ctx, message: str):
    cardName = message
    fullDeck = await getFullDeck()
    allCards = range(fullDeck["nhits"])

    validated = await checkInvalid(ctx, message)
    if validated is True:

        shortName = ""

        cardCount = 0
        for card in allCards:
            if cardName in fullDeck["cards"][card]["name"]:
                shortName = fullDeck["cards"][card]["name_short"]
            if cardName not in fullDeck["cards"][card]["name"]:
                cardCount += 1

        if cardCount > max(allCards):
            await ctx.send("```" + "Please check your input. Search is case sensitive.\n"
                                   "Images should be searched by complete name.\n"
                                   "Major Arcana: Wheel Of Fortune\n"
                                   "Minor Arcana: Knight of Swords\n" + "```")

        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.sacred-texts.com/tarot/pkt/img/" + shortName + ".jpg") as image:
                if image.status == 200:
                    cardImage = io.BytesIO(await image.read())
                    await ctx.send(file=discord.File(cardImage, f"{cardName}.jpg"))
                else:
                    await ctx.send("Please check input.")


async def cardDesc(ctx, message: str):
    # Retrieves the description of a card by its name.
    # Single search terms will return all cards containing that term in the name.
    # EG. Searching "Knight" will retrieve ALL Knights.
    # Searching a suit (Swords, Cups, Wands, Pentacles) will retrieve all cards in the suit.
    cardName = message
    fullDeck = await getFullDeck()
    allCards = range(fullDeck["nhits"])
    cardCount = 0

    if cardName == '':
        await ctx.send("```" + "Please check your input. Search is case sensitive.\n"
                               "Search either by a single term, or match the examples.\n"
                               "Major Arcana: Wheel Of Fortune\n"
                               "Minor Arcana: Knight of Swords\n"
                               "Single Term: Knight / Ace / Devil etc." + "```")

    else:
        for card in allCards:
            if cardName in fullDeck["cards"][card]["name"]:
                await ctx.send("```" + fullDeck["cards"][card]["desc"] + "```")
            if cardName not in fullDeck["cards"][card]["name"]:
                cardCount += 1

        if cardCount > max(allCards):
            await ctx.send("```" + "Please check your input. Search is case sensitive.\n"
                                   "Search either by a single term, or match the examples.\n"
                                   "Major Arcana: Wheel Of Fortune\n"
                                   "Minor Arcana: Knight of Swords\n"
                                   "Single Term: Knight / Ace / Devil etc." + "```")


async def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


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
                images = []

                for card in range(3):
                    orientation = random.randint(0, 1)
                    # cardName = cards["cards"][card]["name"]

                    if orientation == 0:
                        await ctx.send("***" + "```" + cards["cards"][card]["name"] +
                                       ':\n\n' +
                                       cards["cards"][card]["meaning_up"] + someLines + "```" + "***"
                                       )

                    elif orientation == 1:
                        await ctx.send("***" + "```" + "[Rev.]" +
                                       cards["cards"][card]["name"] +
                                       ':\n\n' +
                                       cards["cards"][card]["meaning_rev"] + someLines + "```" + "***"
                                       )

                    async with session.get("https://www.sacred-texts.com/tarot/pkt/img/"
                                           + cards["cards"][card]["name_short"] +
                                           ".jpg") \
                            as image:

                        if image.status == 200:
                            cardImage = io.BytesIO(await image.read())
                            imageConverted = Image.open(cardImage)
                            images.append(imageConverted)
                            # await ctx.send(file=discord.File(cardImage, f"{cardName}.jpg"))

                combinedImages = await get_concat_h(images[0], images[1])
                combinedImages = combinedImages.open()
                await combinedImages.save("", "jpeg")
                await ctx.send(file=discord.File(r"C:\Users\Owner\Desktop", f"spread.jpg"))

            else:
                await magicEightBall(ctx)
