import aiohttp
import asyncio


async def tripleSpread(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://rws-cards-api.herokuapp.com/api/v1/cards/random?n=3") as spread:
            if spread.status == 200:
                user = str(ctx.author)
                await ctx.send('Very well ' + user)
                await asyncio.sleep(4)
                cards = await spread.json()
                await ctx.send(cards["cards"][0]["name"])
                await ctx.send(cards["cards"][1]["name"])
                await ctx.send(cards["cards"][2]["name"])
