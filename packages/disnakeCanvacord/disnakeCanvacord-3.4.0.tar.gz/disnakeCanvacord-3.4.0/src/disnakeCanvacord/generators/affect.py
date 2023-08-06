from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageColor
import asyncio
import aiohttp
from random import randint
from io import BytesIO
import disnake
from typing import Union
from disnakeCanvacord.generators.versionchecker import checkversion

async def getavatar(user: Union[disnake.User, disnake.Member]) -> bytes:
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    disver = str(disnake.__version__)
    if disver.startswith("1"):
        async with session.get(str(user.avatar_url)) as response:
            avatarbytes = await response.read()
        await session.close()
    elif disver.startswith("2"):
        async with session.get(str(user.display_avatar.url)) as response:
            avatarbytes = await response.read()
        await session.close()
    return avatarbytes

async def getbackground(background):
    session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
    async with session.get("https://cdn.glitch.com/dff50ce1-3805-4fdb-a7a5-8cabd5e53756%2Faffect.bmp?v=1628443415269") as response:
        backgroundbytes = await response.read()
    await session.close()
    return backgroundbytes

async def affect(user):
        avatar = Image.open(BytesIO(await getavatar(user))).resize((200, 157)).convert('RGBA')
        base = Image.open(BytesIO(await getbackground("affect"))).convert('RGBA')
        base.paste(avatar, (180, 383, 380, 540), avatar)
        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        await checkversion()
        return b