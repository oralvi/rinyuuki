import requests, os, random, asyncio
from nonebot import MessageSegment
from nonebot import on_command
from rin.typing import CQEvent
from rin import R, Service, priv, util
import rin

sv = Service('easyclanbattle', visible=True)
bs1 = 0
bs2 = 0
bs3 = 0
bs4 = 0
bs5 = 0

@sv.on_keyword(('我进1了'))
async def chat_in1(bot, ctx, bs1=bs1):
    bs1 += 1
    if bs1 == 1:
        await bot.send(ctx, f"你已申请出刀1王，祝武运昌隆！")
    else:
        await bot.send(ctx, f"你已申请出刀1王，目前有{bs1-1}人在内请注意，祝武运昌隆！")

@sv.on_keyword(('我进2了'))
async def chat_in1(bot, ctx, bs2=bs2):
    bs2 += 1
    if bs2 == 1:
        await bot.send(ctx, f"你已申请出刀2王，祝武运昌隆！")
    else:
        await bot.send(ctx, f"你已申请出刀2王，目前有{bs2-1}人在内请注意，祝武运昌隆！")

@sv.on_keyword(('我进3了'))
async def chat_in1(bot, ctx, bs3=bs3):
    bs3 += 1
    if bs3 == 1:
        await bot.send(ctx, f"你已申请出刀3王，祝武运昌隆！")
    else:
        await bot.send(ctx, f"你已申请出刀3王，目前有{bs3-1}人在内请注意，祝武运昌隆！")

@sv.on_keyword(('我进4了'))
async def chat_in1(bot, ctx, bs4=bs4):
    bs4 += 1
    if bs4 == 1:
        await bot.send(ctx, f"你已申请出刀4王，祝武运昌隆！")
    else:
        await bot.send(ctx, f"你已申请出刀4王，目前有{bs4-1}人在内请注意，祝武运昌隆！")

@sv.on_keyword(('我进5了'))
async def chat_in1(bot, ctx, bs5=bs5):
    bs5 += 1
    if bs5 == 1:
        await bot.send(ctx, f"你已申请出刀3王，祝武运昌隆！")
    else:
        await bot.send(ctx, f"你已申请出刀3王，目前有{bs5-1}人在内请注意，祝武运昌隆！")


@sv.on_keyword(('我不进1了'))
async def chat_nin1(bot, ctx, bs1=bs1):
    bs1 -= 1
    if bs1 == 0:
        await bot.send(ctx, f"你不出了，现在1王无人出刀")
    else:
        await bot.send(ctx, f"你不出了，目前有{bs1-1}人仍在战斗")

@sv.on_keyword(('我不进2了'))
async def chat_nin2(bot, ctx, bs2=bs2):
    bs2 -= 1
    if bs2 == 0:
        await bot.send(ctx, f"你不出了，现在2王无人出刀")
    else:
        await bot.send(ctx, f"你不出了，目前有{bs2-1}人仍在战斗")

@sv.on_keyword(('我不进3了'))
async def chat_nin3(bot, ctx, bs3=bs3):
    bs3 -= 1
    if bs3 == 0:
        await bot.send(ctx, f"你不出了，现在3王无人出刀")
    else:
        await bot.send(ctx, f"你不出了，目前有{bs3-1}人仍在战斗")

@sv.on_keyword(('我不进4了'))
async def chat_nin4(bot, ctx, bs4=bs4):
    bs4 -= 1
    if bs4 == 0:
        await bot.send(ctx, f"你不出了，现在4王无人出刀")
    else:
        await bot.send(ctx, f"你不出了，目前有{bs4-1}人仍在战斗")

@sv.on_keyword(('我不进5了'))
async def chat_nin5(bot, ctx, bs5=bs5):
    bs5 -= 1
    if bs5 == 0:
        await bot.send(ctx, f"你不出了，现在5王无人出刀")
    else:
        await bot.send(ctx, f"你不出了，目前有{bs5-1}人仍在战斗")


@sv.on_keyword(('我出1了'))
async def chat_out1(bot, ctx, bs1=bs1):
    bs1 -= 1
    if bs1 == 0:
        await bot.send(ctx, f"你出完了，现在1王无人出刀")
    else:
        await bot.send(ctx, f"你出完了，目前有{bs1-1}人仍在战斗")

@sv.on_keyword(('我出2了'))
async def chat_out2(bot, ctx, bs2=bs2):
    bs2 -= 1
    if bs2 == 0:
        await bot.send(ctx, f"你出完了，现在2王无人出刀")
    else:
        await bot.send(ctx, f"你出完了，目前有{bs2-1}人仍在战斗")

@sv.on_keyword(('我出3了'))
async def chat_out3(bot, ctx, bs3=bs3):
    bs3 -= 1
    if bs3 == 0:
        await bot.send(ctx, f"你出完了，现在3王无人出刀")
    else:
        await bot.send(ctx, f"你出完了，目前有{bs3-1}人仍在战斗")

@sv.on_keyword(('我出4了'))
async def chat_out4(bot, ctx, bs4=bs4):
    bs4 -= 1
    if bs4 == 0:
        await bot.send(ctx, f"你出完了，现在4王无人出刀")
    else:
        await bot.send(ctx, f"你出完了，目前有{bs4-1}人仍在战斗")

@sv.on_keyword(('我出5了'))
async def chat_out5(bot, ctx, bs5=bs5):
    bs5 -= 1
    if bs5 == 0:
        await bot.send(ctx, f"你出完了，现在5王无人出刀")
    else:
        await bot.send(ctx, f"你出完了，目前有{bs5-1}人仍在战斗")