import os
from datetime import datetime, timedelta
from typing import List
from matplotlib import pyplot as plt
try:
    import ujson as json
except:
    import json
from .cbt import *
from aiocqhttp.exceptions import ActionFailed
from nonebot import NoneBot
from nonebot import MessageSegment as ms
from nonebot.typing import Context_T
from rin import util, priv

from .main import sv, cb_cmd
from .argparse import ArgParser, ArgHolder, ParseResult
from .argparse.argtype import *
from .exception import *
USAGE_ADD_MEMBER = '!入会 昵称 (@qq)'

@cb_cmd('入会', ArgParser(usage=USAGE_ADD_MEMBER, arg_dict={
        '': ArgHolder(tip='昵称', default=''),
        '@': ArgHolder(tip='qq号', type=int, default=0)}))
async def add_member(bot:NoneBot, ctx:Context_T, args:ParseResult):
    uid = args['@'] or args.at or ctx['user_id']
    name = args['']
    Recorder.addPlayer({name}, {uid}, 'rmk', 'admin')
    await bot.send(ctx, f"成员{ms.at(uid)}添加成功！欢迎{name}加入拂晓茶会")