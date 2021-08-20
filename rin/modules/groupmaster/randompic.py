import requests, os, random, asyncio
from nonebot import MessageSegment
from nonebot import on_command
from rin.typing import CQEvent
from rin import R, Service, priv, util
import rin
sv = Service('randompic', visible=True)



@sv.on_keyword(('确实', '有一说一', 'u1s1', 'yysy'))
async def chat_queshi(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img(f"确实{random.randint(1, 2)}.jpg").cqcode)


@sv.on_keyword(('会战'))
async def chat_clanba(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img('我的天啊你看看都几点了.jpg').cqcode)


@sv.on_keyword(('内鬼'))
async def chat_neigui(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img('内鬼.png').cqcode)

nyb_player = f'''{R.img('nyb.gif').cqcode}
正在播放：New Year Burst
──●━━━━ 1:05/1:30
⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
'''.strip()

@sv.on_keyword(('春黑', '新黑'))
async def new_year_burst(bot, ev):
    if random.random() < 0.10:
        await bot.send(ev, nyb_player)

@sv.on_keyword(('露娜', 'luna'))
async def luna(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img('luna.gif').cqcode)

@sv.on_keyword(('就这'))
async def jiuzhe(bot, ctx):
    if random.random() < 0.5:
        await bot.send(ctx, R.img('就这.png').cqcode)


@sv.on_keyword(('绝了'))
async def juele(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img('绝了.jpg').cqcode)

@sv.on_keyword(('啊这', 'az'))
async def az(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img('啊这.jpg').cqcode)

@sv.on_keyword(('laopo', 'lp', '老婆'))
async def hanlaopo(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img(f"laopo{random.randint(1, 2)}.jpg").cqcode)

@sv.on_keyword(('se', '涩', '色图'))
async def buzhunkansetu(bot, ctx):
    if random.random() < 0.10:
        await bot.send(ctx, R.img(f"涩图审核{random.randint(1, 2)}.jpg").cqcode)


