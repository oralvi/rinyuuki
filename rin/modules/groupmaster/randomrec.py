import requests, os, random, asyncio
from nonebot import MessageSegment
from nonebot import on_command
from rin.typing import CQEvent
from rin import R, Service, priv, util
import rin
sv = Service('randomrec', visible=True)


@sv.on_command('xcw',only_to_me=False)
async def voicetest(bot, ctx):
        await bot.send(ctx, R.rec('test.silk').cqcode)


