import os

import aiocqhttp
import nonebot
from nonebot import Message, MessageSegment, message_preprocessor
from nonebot.message import CanceledException

from .log import new_logger
from . import config

__version__ = '2.1.0'

_bot = None
RinYuuki = nonebot.NoneBot
os.makedirs(os.path.expanduser('~/.rin'), exist_ok=True)
logger = new_logger('rin', config.DEBUG)

def init() -> RinYuuki:
    global _bot
    nonebot.init(config)
    _bot = nonebot.get_bot()
    _bot.finish = _finish

    from .log import error_handler, critical_handler
    nonebot.logger.addHandler(error_handler)
    nonebot.logger.addHandler(critical_handler)

    for module_name in config.MODULES_ON:
        nonebot.load_plugins(
            os.path.join(os.path.dirname(__file__), 'modules', module_name),
            f'rin.modules.{module_name}')

    from . import msghandler

    return _bot


async def _finish(event, message, **kwargs):
    if message:
        await _bot.send(event, message, **kwargs)
    raise CanceledException('ServiceFunc of Rin finished.')


def get_bot() -> RinYuuki:
    if _bot is None:
        raise ValueError('Rin has not been initialized')
    return _bot


def get_self_ids():
    return _bot._wsr_api_clients.keys()


from . import R
from .service import Service, sucmd
