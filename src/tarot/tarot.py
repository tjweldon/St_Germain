import io
from typing import Iterable, Optional, Dict, List

import aiohttp
import random
import discord
from discord.ext.commands import Context

from src.images.imageManipulators import combineImageListHorizontal, convertImage

SPACER: str = '\n' + '__ ' * 22
CARD_LIMIT: int = 7
COMBINED_IMAGE_PATH: str = r"C:\Users\Owner\PycharmProjects\StGermain\images\combined.jpg"
SUITS: List[str] = [
    "Wands",
    "Cups",
    "Swords",
    "Pentacles",
]
CARD_NUMBERS: List[str] = [
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
]
CARD_COURTS: List[str] = [
    "Ace",
    "King",
    "Queen",
    "Knight",
    "Page",
]

INVALID_MESSAGE: str = "Please check your input. Search is case sensitive.\n" \
                       "Images should be searched by complete name.\n" \
                       "Major Arcana: Wheel Of Fortune\n" \
                       "Minor Arcana: Knight of Swords\n"


async def sendDelimited(ctx: Context, message: str, delimiters: Iterable[str] = ("```",)) -> None:
    """
    Sends a message using the passed context with any delimiters specified.
    Delimiters should be provided as a tuple of strings, they are applied to
    the message sequentially such that the first supplied delimiter is the innermost.
    @param ctx:
    @param message:
    @param delimiters:
    """
    for delimiter in delimiters:
        message = delimiter + message + delimiter

    await ctx.send(message)


async def getResponseBody(url: str) -> Optional[dict]:
    """
    Gets a resource at url and parses the json body to a dict,
    returns None on failed requests.
    @param url:
    @return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            body = await response.json()

    return body


async def downloadFile(url: str) -> Optional[bytes]:
    """
    Downloads a file at url, returns None on failed requests.
    @param url:
    @return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            filestream = await response.read()

    return filestream


async def getFullDeck() -> Optional[dict]:
    url = "https://rws-cards-api.herokuapp.com/api/v1/cards/"
    return await getResponseBody(url)


async def getRandomCards(number: int) -> Optional[dict]:
    url = f"https://rws-cards-api.herokuapp.com/api/v1/cards/random?n={number}"
    return await getResponseBody(url)


async def downloadCardImage(card: Dict[str, str]) -> Optional[bytes]:
    url = "https://www.sacred-texts.com/tarot/pkt/img/{}.jpg".format(card["name_short"])
    return await downloadFile(url)


async def checkInvalid(ctx: Context, cardName):
    """
    Responds to the discord user with an error message if they provide
    a search term that is too generic
    @param ctx:
    @param cardName:
    @return:
    """
    numbersOf = list(map(lambda s: f"{s} of", CARD_NUMBERS))
    courtsOf = list(map(lambda s: f"{s} of", CARD_COURTS))
    invalidTerms = CARD_NUMBERS + numbersOf + CARD_COURTS + courtsOf + SUITS + [""]
    if cardName in invalidTerms:
        await sendDelimited(ctx, INVALID_MESSAGE)
        return False

    # Single letter input is invalid
    if len(cardName) == 1:
        await sendDelimited(ctx, INVALID_MESSAGE)
        return False

    return True


async def getMeanings(ctx: Context, message: str):
    """
    Responds to the user with the meanings of the provided car
    @param ctx:
    @param message:
    @return:
    """
    searchTerm = message
    fullDeck = await getFullDeck()

    if not await checkInvalid(ctx, message) or fullDeck is None:
        return

    meanings = {}
    for card in fullDeck["cards"]:
        if searchTerm in card["name"]:
            meanings = {
                'up': card['meaning_up'],
                'rev': card['meaning_rev'],
            }

    if not meanings:
        await sendDelimited(ctx, INVALID_MESSAGE)
    else:
        await sendDelimited(ctx, f"Upright: {meanings.get('up', '')}")
        await sendDelimited(ctx, f"Reversed: {meanings.get('rev', '')}")


async def getCardImage(ctx: Context, message: str):
    """
    Responds to the discord user with the image associated to a card
    @param ctx:
    @param message:
    @return:
    """
    global INVALID_MESSAGE
    cardName = message
    fullDeck = await getFullDeck()

    if not await checkInvalid(ctx, message) or fullDeck is None:
        return

    desiredCard = None
    for card in fullDeck["cards"]:
        if cardName in card["name"]:
            desiredCard = card

    if desiredCard is None:
        await sendDelimited(ctx, INVALID_MESSAGE)
        return

    rawImage = await downloadCardImage(desiredCard)
    if rawImage is None:
        await ctx.send("Please check input.")
        return

    cardImage = io.BytesIO(rawImage)
    await ctx.send(file=discord.File(cardImage, f"{cardName}.jpg"))


async def cardDesc(ctx: Context, message: str) -> None:
    """
    Retrieves the description of a card by its name.
    Single search terms will return all cards containing that term in the name.
    EG. Searching "Knight" will retrieve ALL Knights.
    Searching a suit (Swords, Cups, Wands, Pentacles) will retrieve all cards in the suit.
    """
    cardName = message
    thisInvalidMessage = INVALID_MESSAGE + "Single Term: Knight / Ace / Devil etc."
    if cardName == '':
        await sendDelimited(ctx, thisInvalidMessage)
        return

    fullDeck = await getFullDeck()
    if fullDeck is None:
        return

    cardsFound = False
    for card in fullDeck["cards"]:
        if cardName in card["name"]:
            await sendDelimited(ctx, card['desc'])
            cardsFound = True

    if not cardsFound:
        await sendDelimited(ctx, thisInvalidMessage)


async def tarotSpread(ctx: Context, numberOfCards):
    """
    Retrieves random cards as JSON.
    If API response is OK, creates a variable to hold the username and prepares cards.
    Card orientation is represented as 0 or 1 (card meanings are tied to orientation)
    Sends either the card name, or card name + * to represent a reversed card.
    """
    if numberOfCards > CARD_LIMIT:
        numberOfCards = CARD_LIMIT

    cards = await getRandomCards(numberOfCards)

    await ctx.send(f"Very well {str(ctx.author)}{SPACER}")
    images = []

    # Determines card orientation and posts message in sequence.
    for card in cards["cards"]:
        await sendDelimited(
            ctx,
            await getCardMessage(card),
            delimiters=("```", "***")
        )
        image = await downloadCardImage(card)
        images.append(await convertImage(image))

    finalSpread = await combineImageListHorizontal(images)
    finalSpread.save(COMBINED_IMAGE_PATH)

    # Sends the final combined image.
    await ctx.send(
        file=discord.File(COMBINED_IMAGE_PATH, "spread.jpg")
    )


async def getCardMessage(card: dict, orientation=random.randint(0, 1)) -> str:
    """
    Given a card and a orientation (of value 1 or 0) this will return a formatted
    message as a string
    @param card:
    @param orientation:
    @return:
    """
    meaning = card['meaning_up'] if orientation == 0 else card['meaning_rev']
    revTag = "" if orientation == 0 else "[Rev.]"
    message = "{}{}:\n\n{}{}".format(
        revTag,
        card["name"],
        meaning,
        SPACER,
    )
    return message
