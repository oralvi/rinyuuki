from .cbt import Recorder
from nonebot import on_command
from .argparse import ArgParser
from .exception import *
from rin import R, Service, util
from rin.typing import *


sv = Service('cbt')
SORRY = 'ごめんなさい！嘤嘤嘤(〒︿〒)'

if __name__ == '__main__':
    recorder = Recorder()
    bosses = {
        1: [1000, 2000, 3000, 4000, 5000],
        2: [1000, 2000, 3000, 4000, 5000],
        3: [1000, 2000, 3000, 4000, 5000],
        4: [1400, 2000, 3000, 4000, 5000],
        5: [1000, 2000, 3000, 4000, 5000],
    }
    recorder.addUser('admin', 3, '随便')
''' #kmr 为普通用户，rmk 为管理用户
    recorder.setBossHP(bosses, 'rmk') #设置 boss 血量
    recorder.dayStarts() #定时运行，新的一天开始，刀数清零
    recorder.getBossStatus('kmr') #查询当前血量，返回字典，值为 tuple(周目数, 血量)
    recorder.getPlayerStatus('rmk') #查刀，返回包含所有玩家情况的字典，值为 tuple(已出刀数, 剩余补时数)
    recorder.addPlayer('baka', 1, 'rmk') #添加普通玩家 baka
    recorder.enterBattle('kmr', 3) #进入战斗
    recorder.cancelBattle('kmr') #我不进了
    recorder.reportDamage(3, 'kmr', True, 23333) #报刀，参数为：boss, 玩家, 是否为完整刀, 伤害
'''
_registry:Dict[str, Tuple[Callable, ArgParser]] = {}

@sv.on_message('group')
async def _clanbattle_bus(bot, ctx):
    # check prefix
    start = ''
    for m in ctx['message']:
        if m.type == 'text':
            start = m.data.get('text', '').lstrip()
            break
    if not start or start[0] not in '!！':
        return

    # find cmd
    plain_text = ctx['message'].extract_plain_text()
    cmd, *args = plain_text[1:].split()
    cmd = util.normalize_str(cmd)
    if cmd in _registry:
        func, parser = _registry[cmd]
        try:
            sv.logger.info(f'Message {ctx["message_id"]} is a clanbattle command, start to process by {func.__name__}.')
            args = parser.parse(args, ctx['message'])
            await func(bot, ctx, args)
            sv.logger.info(f'Message {ctx["message_id"]} is a clanbattle command, handled by {func.__name__}.')
        except DatabaseError as e:
            await bot.send(ctx, f'DatabaseError: {e.message}\n{SORRY}\n※请及时联系维护组', at_sender=True)
        except ClanBattleError as e:
            await bot.send(ctx, e.message, at_sender=True)
        except Exception as e:
            sv.logger.exception(e)
            sv.logger.error(f'{type(e)} occured when {func.__name__} handling message {ctx["message_id"]}.')
            await bot.send(ctx, f'Error: 机器人出现未预料的错误\n{SORRY}\n※请及时联系维护组', at_sender=True)


def cb_cmd(name, parser:ArgParser) -> Callable:
    if isinstance(name, str):
        name = (name, )
    if not isinstance(name, Iterable):
        raise ValueError('`name` of cb_cmd must be `str` or `Iterable[str]`')
    names = map(lambda x: util.normalize_str(x), name)
    def deco(func) -> Callable:
        for n in names:
            if n in _registry:
                sv.logger.warning(f'出现重名命令：{func.__name__} 与 {_registry[n].__name__}命令名冲突')
            else:
                _registry[n] = (func, parser)
        return func
    return deco


from .cmd import *