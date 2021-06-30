import asyncio
import importlib

from rin import Service, priv, sucmd, get_bot
from rin.config import twitter as cfg
from rin.typing import MessageSegment as CommandSession

sv = Service("twitter-poller", use_priv=priv.SU, manage_priv=priv.SU, visible=False)
bot = get_bot()
daemon = None

from .follow import follow_stream
from .track import track_stream

@bot.on_startup
async def start_daemon():
    global daemon

    loop = asyncio.get_event_loop()
    daemon = loop.create_task(stream_daemon(follow_stream))
    loop.create_task(stream_daemon(track_stream))


async def stream_daemon(stream_func):
    while True:
        try:
            await stream_func()
        except (KeyboardInterrupt, asyncio.CancelledError):
            sv.logger.info("Twitter stream daemon exited.")
            return
        except Exception as e:
            sv.logger.exception(e)
            sv.logger.error(f"Error {type(e)} Occurred in twitter stream. Restarting stream in 5s.")
            await asyncio.sleep(5)


@sucmd("reload-twitter-stream-daemon", force_private=False, aliases=("重启转推", "重载转推"))
async def reload_twitter_stream_daemon(session: CommandSession):
    try:
        daemon.cancel()
        importlib.reload(cfg)
        await start_daemon()
        await session.send("ok")
    except Exception as e:
        sv.logger.exception(e)
        await session.send(f"Error: {type(e)}")
