import requests, os, random, asyncio
from nonebot import MessageSegment
from nonebot import on_command
from rin.typing import CQEvent
from rin import R, Service, priv, util
import rin

sv = Service('randomrec', visible=True)


@sv.on_keyword('xcw')
async def voicetest(bot, ev):
    await bot.send(ev, R.rec('test.silk').cqcode)
