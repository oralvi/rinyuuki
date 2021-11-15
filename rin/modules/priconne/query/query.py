import itertools
from rin import util, R
from rin.typing import CQEvent
from . import sv

rank_jp = '19-4'
p1 = R.img(f'priconne/quick/1jp1.jpg').cqcode
p2 = R.img(f'priconne/quick/1jp2.jpg').cqcode
p3 = R.img(f'priconne/quick/1jp3.jpg').cqcode
p4 = R.img(f'priconne/quick/2jp1.jpg').cqcode
p5 = R.img(f'priconne/quick/2jp2.jpg').cqcode
p6 = R.img(f'priconne/quick/2jp3.jpg').cqcode


@sv.on_rex(r'^(\*?([日])服?)?rank(表|推荐|指南)?([012]*)?$')
async def rank_sheet(bot, ev):
    match = ev['match']
    is_chosen = match.group(4)
    if not is_chosen:
        await bot.send(ev, '\n请问您要查询哪家rank表？（eg.日rank表0）\n0*GWrank表\n1*とう佬rank表（不定时更新\n2*うさ*アリスrank表（不定时更新', at_sender=True)
        return
    msg = [
        '\n表格仅供参考',
        # '\n※rank表仅供参考，升r有风险，强化需谨慎\n※请以会长要求为准',
    ]
    if is_chosen:

        pos = match.group(4)
        if not pos or '0' in pos:
            msg.append(f'※来自GameWith\n日服 rank链接：\n')
            msg.append(f'https://gamewith.jp/pricone-re/article/show/148926')
        if '1' in pos:
            msg.append(f'※来自とう佬@tou21snR\n更新日期210816（已过时！！）\n日服 rank表：\n')
            msg.append(str(p1))
            msg.append(str(p2))
            msg.append(str(p3))
        if '2' in pos:
            msg.append(f'※来自うさ*アリス@usausa_1321\n更新日期210816（已过时！！！）\n日服 rank表：\n')
            msg.append(str(p4))
            msg.append(str(p5))
            msg.append(str(p6))
        await bot.send(ev, '\n'.join(msg), at_sender=True)
        #await util.silence(ev, 60)



@sv.on_fullmatch(('jjc', 'JJC', 'JJC作业', 'JJC作业网', 'JJC数据库', 'jjc作业', 'jjc作业网', 'jjc数据库'))
async def say_arina_database(bot, ev):
    await bot.send(ev, '公主连接Re:Dive 竞技场编成数据库\n日文：https://nomae.net/arenadb \n中文：https://pcrdfans.com/battle')


OTHER_KEYWORDS = '【日rank】【台rank】【b服rank】【jjc作业网】【黄骑充电表】【一个顶俩】'
PCR_SITES = f'''
【繁中wiki/兰德索尔图书馆】pcredivewiki.tw
【日文wiki/GameWith】gamewith.jp/pricone-re
【日文wiki/AppMedia】appmedia.jp/priconne-redive
【竞技场作业库(中文)】pcrdfans.com/battle
【竞技场作业库(日文)】nomae.net/arenadb
【论坛/NGA社区】bbs.nga.cn/thread.php?fid=-10308342
【iOS实用工具/初音笔记】bbs.nga.cn/read.php?tid=14878762
【安卓实用工具/静流笔记】bbs.nga.cn/read.php?tid=20499613
【台服卡池千里眼】bbs.nga.cn/read.php?tid=16986067
【日官网】priconne-redive.jp
【台官网】www.princessconnect.so-net.tw

===其他查询关键词===
{OTHER_KEYWORDS}
※B服速查请输入【bcr速查】'''

BCR_SITES = f'''
【妈宝骑士攻略(懒人攻略合集)】bbs.nga.cn/read.php?tid=20980776
【机制详解】bbs.nga.cn/read.php?tid=19104807
【初始推荐】bbs.nga.cn/read.php?tid=20789582
【术语黑话】bbs.nga.cn/read.php?tid=18422680
【角色点评】bbs.nga.cn/read.php?tid=20804052
【秘石规划】bbs.nga.cn/read.php?tid=20101864
【卡池亿里眼】bbs.nga.cn/read.php?tid=20816796
【为何卡R卡星】bbs.nga.cn/read.php?tid=20732035
【推图阵容推荐】bbs.nga.cn/read.php?tid=21010038

===其他查询关键词===
{OTHER_KEYWORDS}
※日台服速查请输入【pcr速查】'''

@sv.on_fullmatch(('pcr速查', 'pcr图书馆', '图书馆'))
async def pcr_sites(bot, ev: CQEvent):
    await bot.send(ev, PCR_SITES, at_sender=True)
    await util.silence(ev, 60)
@sv.on_fullmatch(('bcr速查', 'bcr攻略'))
async def bcr_sites(bot, ev: CQEvent):
    await bot.send(ev, BCR_SITES, at_sender=True)
    await util.silence(ev, 60)


YUKARI_SHEET_ALIAS = map(lambda x: ''.join(x), itertools.product(('黄骑', '酒鬼'), ('充电', '充电表', '充能', '充能表')))
YUKARI_SHEET = f'''
{R.img('priconne/quick/黄骑充电.jpg').cqcode}
※大圈是1动充电对象 PvP测试
※黄骑四号位例外较多
※对面羊驼或中后卫坦 有可能歪
※我方羊驼算一号位
※图片搬运自漪夢奈特'''
@sv.on_fullmatch(YUKARI_SHEET_ALIAS)
async def yukari_sheet(bot, ev):
    await bot.send(ev, YUKARI_SHEET, at_sender=True)
    await util.silence(ev, 60)


DRAGON_TOOL = f'''
拼音对照表：{R.img('priconne/KyaruMiniGame/注音文字.jpg').cqcode}{R.img('priconne/KyaruMiniGame/接龙.jpg').cqcode}
龍的探索者們小遊戲單字表 https://hanshino.nctu.me/online/KyaruMiniGame
镜像 https://hoshino.monster/KyaruMiniGame
网站内有全词条和搜索，或需科学上网'''
@sv.on_fullmatch(('一个顶俩', '拼音接龙', '韵母接龙'))
async def dragon(bot, ev):
    await bot.send(ev, DRAGON_TOOL, at_sender=True)
    await util.silence(ev, 60)
