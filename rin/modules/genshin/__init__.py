from .getImg import draw_pic,draw_abyss_pic,draw_abyss0_pic,draw_wordcloud,draw_event_pic
from .getDB import (CheckDB, GetAward, GetCharInfo, GetDaily, GetMysInfo,
                    GetSignInfo, GetSignList, GetWeaponInfo, MysSign, OpenPush,
                    connectDB, cookiesDB, deletecache, selectDB, get_alots,
                    GetEnemiesInfo,GetAudioInfo)
from nonebot import *
from rin import Service,R,priv,util
from rin.typing import MessageSegment,CQEvent, RinYuuki

import requests,random,os,json,re,time,datetime,string,base64,math

import threading
import rin
import asyncio
import hashlib
import sqlite3
from io import BytesIO
import urllib
import requests
from base64 import b64encode

sv = Service('genshinuid')
bot = get_bot()

FILE_PATH = os.path.dirname(__file__)
FILE2_PATH = os.path.join(FILE_PATH,'mys')
INDEX_PATH = os.path.join(FILE2_PATH, 'index')
Texture_PATH = os.path.join(FILE2_PATH,'texture2d')

avatar_json = {
    "Albedo": "阿贝多",
    "Ambor": "安柏",
    "Barbara": "芭芭拉",
    "Beidou": "北斗",
    "Bennett": "班尼特",
    "Chongyun": "重云",
    "Diluc": "迪卢克",
    "Diona": "迪奥娜",
    "Eula": "优菈",
    "Fischl": "菲谢尔",
    "Ganyu": "甘雨",
    "Hutao": "胡桃",
    "Jean": "琴",
    "Kazuha": "枫原万叶",
    "Kaeya": "凯亚",
    "Ayaka": "神里绫华",
    "Keqing": "刻晴",
    "Klee": "可莉",
    "Lisa": "丽莎",
    "Mona": "莫娜",
    "Ningguang": "凝光",
    "Noel": "诺艾尔",
    "Qiqi": "七七",
    "Razor": "雷泽",
    "Rosaria": "罗莎莉亚",
    "Sucrose": "砂糖",
    "Tartaglia": "达达利亚",
    "Venti": "温迪",
    "Xiangling": "香菱",
    "Xiao": "魈",
    "Xingqiu": "行秋",
    "Xinyan": "辛焱",
    "Yanfei": "烟绯",
    "Zhongli": "钟离",
    "Yoimiya": "宵宫",
    "Sayu": "早柚",
    "Shogun": "雷电将军",
    "Aloy": "埃洛伊",
    "Sara": "九条裟罗",
    "Kokomi": "珊瑚宫心海",
    "Shenhe":"申鹤"
}

daily_im = '''
*数据刷新可能存在一定延迟，请以当前游戏实际数据为准{}
==============
原粹树脂：{}/{}{}
每日委托：{}/{} 奖励{}领取
周本减半：{}/{}
洞天宝钱：{}
探索派遣：
总数/完成/上限：{}/{}/{}
{}'''

month_im = '''
==============
{}
UID：{}
==============
本日获取原石：{}
本日获取摩拉：{}
==============
昨日获取原石：{}
昨日获取摩拉：{}
==============
本月获取原石：{}
本月获取摩拉：{}
==============
上月获取原石：{}
上月获取摩拉：{}
==============
原石收入组成：
{}=============='''

weapon_im = '''【名称】：{}
【类型】：{}
【稀有度】：{}
【介绍】：{}
【攻击力】：{}{}{}'''

char_info_im = '''{}
【稀有度】：{}
【武器】：{}
【元素】：{}
【突破加成】：{}
【生日】：{}
【命之座】：{}
【cv】：{}
【介绍】：{}'''

audio_json = {
    "357":["357_01","357_02","357_03"],
    "1000000":["1000000_01","1000000_02","1000000_03","1000000_04","1000000_05","1000000_06","1000000_07"],
    "1000001":["1000001_01","1000001_02","1000001_03"],
    "1000002":["1000002_01","1000002_02","1000002_03"],
    "1000100":["1000100_01","1000100_02","1000100_03","1000100_04","1000100_05"],
    "1000101":["1000101_01","1000101_02","1000101_03","1000101_04","1000101_05","1000101_06"],
    "1000200":["1000200_01","1000200_02","1000200_03"],
    "1010201":["1010201_01"],
    "1000300":["1000300_01","1000300_02"],
    "1000400":["1000400_01","1000400_02","1000400_03"],
    "1000500":["1000500_01","1000500_02","1000500_03"],
    "1010000":["1010000_01","1010000_02","1010000_03","1010000_04","1010000_05"],
    "1010001":["1010001_01","1010001_02"],
    "1010100":["1010100_01","1010100_02","1010100_03","1010100_04","1010100_05"],
    "1010200":["1010200_01","1010200_02","1010200_03","1010200_04","1010200_05"],
    "1010300":["1010300_01","1010300_02","1010300_03","1010300_04","1010300_05"],
    "1010301":["1010301_01","1010301_02","1010301_03","1010301_04","1010301_05"],
    "1010400":["1010400_01","1010400_02","1010400_03"],
    "1020000":["1020000_01"]
}

@sv.on_prefix('语音')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    message = message.replace(' ', "")
    name = ''.join(re.findall('[\u4e00-\u9fa5]', message))

    if name == "列表":
        f=open(os.path.join(INDEX_PATH,"语音.png"),'rb')
        ls_f = base64.b64encode(f.read()).decode()
        imgmes = 'base64://' + ls_f
        f.close()
        im = f"[CQ:image,file={imgmes}]"
        await bot.send(ev,im)
    elif name == "":
        return
    else:
        audioid = re.findall(r"[0-9]+", message)[0]
        if audioid in audio_json:
            audioid = random.choice(audio_json[audioid])
        url = await GetAudioInfo(name,audioid)
        audio = BytesIO(requests.get(url).content)
        audios = 'base64://' + b64encode(audio.getvalue()).decode()
        im = f"[CQ:record,file={audios}]"
        try:
            await bot.send(ev,im)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,"不存在该语音ID或者不存在该角色。")

@sv.on_fullmatch('活动列表')
async def _(bot:RinYuuki,  ev: CQEvent):
    img_path = os.path.join(FILE2_PATH,"event.jpg")
    while(1):
        if os.path.exists(img_path):
            f=open(img_path,'rb')
            ls_f = base64.b64encode(f.read()).decode()
            imgmes = 'base64://' + ls_f
            f.close()
            im = f"[CQ:image,file={imgmes}]"
            break
        else:
            await draw_event_pic()
    await bot.send(ev,im)

@sv.on_fullmatch('御神签')
async def _(bot:RinYuuki,  ev: CQEvent):
    qid = ev.sender["user_id"]
    raw_data = await get_alots(qid)
    im = base64.b64decode(raw_data).decode("utf-8")
    await bot.send(ev,im)

@sv.on_prefix('材料')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    message = message.replace(' ', "")
    im = await char_wiki(message,"costs")
    await bot.send(ev,im)
    
@sv.on_prefix('原魔')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    im = await enemies_wiki(message)
    await bot.send(ev,im)

@sv.on_prefix('天赋')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
    num = re.findall(r"[0-9]+", message)
    if len(num) == 1:
        im = await char_wiki(name,"talents",num[0])
    else:
        im = "参数不正确。"
    await bot.send(ev,im)

@sv.on_prefix('武器')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
    level = re.findall(r"[0-9]+", message)
    if len(level) == 1:
        im = await weapon_wiki(name,level=level[0])
    else:
        im = await weapon_wiki(name)
    await bot.send(ev,im,at_sender=True)

@sv.on_prefix('角色')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    message = message.replace(' ', "")
    name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
    level = re.findall(r"[0-9]+", message)
    if len(level) == 1:
        im = await char_wiki(name,"char",level=level[0])
    else:
        im = await char_wiki(name)
    await bot.send(ev,im)

async def enemies_wiki(name):
    raw_data = await GetEnemiesInfo(name)
    reward = ""
    for i in raw_data["rewardpreview"]:
        reward += i["name"] + "：" + str(i["count"]) if "count" in i.keys() else i["name"] + "：" + "可能"
        reward += "\n"
    im = "【{}】\n——{}——\n类型：{}\n信息：{}\n掉落物：\n{}".format(raw_data["name"],raw_data["specialname"],
                                                    raw_data["category"],raw_data["description"],reward)
    return im

@sv.on_prefix('命座')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    num = int(re.findall(r"\d+", message)[0])  # str
    m = ''.join(re.findall('[\u4e00-\u9fa5]', message))
    if num<= 0 or num >6:
        await bot.send(ev,"你家{}有{}命？".format(m,num),at_sender = True)
    else:
        im = await char_wiki(m, "constellations", num)
        await bot.send(ev,im,at_sender=True)
    
#每日零点清空cookies使用缓存
@sv.scheduled_job('cron', hour='0')
async def delete():
    deletecache()

@sv.scheduled_job('cron', hour='2')
async def delete():
    await draw_event_pic()

@sv.on_fullmatch('全部重签')
async def _(bot:RinYuuki,  ev: CQEvent):
    if ev.user_id not in bot.config.SUPERUSERS:
        return
    await bot.send(ev,"已开始执行")
    await dailysign()

#每日零点半进行米游社签到
@sv.scheduled_job('cron', hour='0',minute="30")
async def dailysign():
    await dailysign()

async def dailysign():
    conn = sqlite3.connect('ID_DATA.db')
    c = conn.cursor()
    cursor = c.execute(
        "SELECT *  FROM NewCookiesTable WHERE StatusB != ?", ("off",))
    c_data = cursor.fetchall()

    for row in c_data:

        im = await sign(str(row[0]))
        if row[4] == "on":
            await bot.send_private_msg(user_id = row[2],message = im)
        else:
            await bot.send_group_msg(group_id = row[4],message = f"[CQ:at,qq={row[2]}]" + "\n" + im)

        await asyncio.sleep(7)

#每隔半小时检测树脂是否超过设定值
@sv.scheduled_job('interval', minutes=30)
async def push():
    daily_data = await daily()
    if daily_data != None:
        for i in daily_data:
            if i['gid'] == "on":
                await bot.send_private_msg(user_id = i['qid'],message = i['message'])
            else:
                await bot.send_group_msg(group_id = i['gid'],message = f"[CQ:at,qq={i['qid']}]" + "\n" + i['message'])
    else:
        pass

#私聊事件
@bot.on_message('private')
async def setting(ctx):
    message = ctx['raw_message']
    sid=int(ctx["self_id"])
    userid=int(ctx["sender"]["user_id"])
    gid=0
    if '添加 ' in message:
        try:
            mes = message.replace('添加 ','')
            aid = re.search(r"account_id=(\d*)", mes)
            mysid_data = aid.group(0).split('=')
            mysid = mysid_data[1]
            cookie = ';'.join(filter(lambda x: x.split('=')[0] in ["cookie_token", "account_id"], [i.strip() for i in mes.split(';')]))
            mys_data = await GetMysInfo(mysid,cookie)
            for i in mys_data['data']['list']:
                if i['game_id'] != 2:
                    mys_data['data']['list'].remove(i)
            uid = mys_data['data']['list'][0]['game_role_id']
            await cookiesDB(uid,cookie,userid)
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=f'添加Cookies成功！Cookies属于个人重要信息，如果你是在不知情的情况下添加，请马上修改米游社账户密码，保护个人隐私！')
        except Exception as e:
            print(e.with_traceback)
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=f'校验失败！请输入正确的Cookies！')
    elif '开启推送' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"on","StatusA")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            print(e.with_traceback)
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")
    elif '关闭推送' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"off","StatusA")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            print(e.with_traceback)
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")
    elif '开启自动签到' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"on","StatusB")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            print(e.with_traceback)
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")
    elif '关闭自动签到' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"off","StatusA")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            print(e.with_traceback)
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")

#群聊开启 自动签到 和 推送树脂提醒 功能
@sv.on_prefix('开启')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    m = ''.join(re.findall('[\u4e00-\u9fa5]',message))
    
    qid = ev.sender["user_id"]
    at = re.search(r"\[CQ:at,qq=(\d*)\]", message)

    if m == "自动签到":
        try:
            if at and qid in bot.config.SUPERUSERS:
                qid = at.group(1)
            elif at and at.group(1) != qid:
                await bot.send(ev,"你没有权限。",at_sender=True)
                return
            else:
                pass
            gid = ev.group_id
            uid = await selectDB(ev.sender['user_id'],mode = "uid")
            im = await OpenPush(int(uid[0]),ev.sender['user_id'],str(gid),"StatusB")
            await bot.send(ev,im,at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,"未绑定uid信息！",at_sender=True)
    elif m == "推送":
        try:
            if at and qid in bot.config.SUPERUSERS:
                qid = at.group(1)
            elif at and at.group(1) != qid:
                await bot.send(ev,"你没有权限。",at_sender=True)
                return
            else:
                pass
            gid = ev.group_id
            uid = await selectDB(ev.sender['user_id'],mode = "uid")
            im = await OpenPush(int(uid[0]),ev.sender['user_id'],str(gid),"StatusA")
            await bot.send(ev,im,at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,"未绑定uid信息！",at_sender=True)
            
#群聊关闭 自动签到 和 推送树脂提醒 功能
@sv.on_prefix('关闭')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    m = ''.join(re.findall('[\u4e00-\u9fa5]',message))

    qid = ev.sender["user_id"]
    at = re.search(r"\[CQ:at,qq=(\d*)\]", message)

    if m == "自动签到":
        try:
            if at and qid in bot.config.SUPERUSERS:
                qid = at.group(1)
            elif at and at.group(1) != qid:
                await bot.send(ev,"你没有权限。",at_sender=True)
                return
            else:
                pass
            gid = ev.group_id
            uid = await selectDB(ev.sender['user_id'],mode = "uid")
            im = await OpenPush(int(uid[0]),ev.sender['user_id'],"off","StatusB")
            await bot.send(ev,im,at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,"未绑定uid信息！",at_sender=True)
    elif m == "推送":
        try:
            if at and qid in bot.config.SUPERUSERS:
                qid = at.group(1)
            elif at and at.group(1) != qid:
                await bot.send(ev,"你没有权限。",at_sender=True)
                return
            else:
                pass
            gid = ev.group_id
            uid = await selectDB(ev.sender['user_id'],mode = "uid")
            im = await OpenPush(int(uid[0]),ev.sender['user_id'],"off","StatusA")
            await bot.send(ev,im,at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,"未绑定uid信息！",at_sender=True)
            
#群聊内 每月统计 功能
@sv.on_fullmatch('每月统计')
async def _(bot:RinYuuki,  ev: CQEvent):
    try:
        qid = ev.sender["user_id"]
        uid = await selectDB(ev.sender['user_id'],mode = "uid")
        uid = uid[0]
        data = await GetAward(uid)
        nickname = data['data']['nickname']
        day_stone = data['data']['day_data']['current_primogems']
        day_mora = data['data']['day_data']['current_mora']
        lastday_stone = data['data']['day_data']['last_primogems']
        lastday_mora = data['data']['day_data']['last_mora']
        month_stone = data['data']['month_data']['current_primogems']
        month_mora = data['data']['month_data']['current_mora']
        lastmonth_stone = data['data']['month_data']['last_primogems']
        lastmonth_mora = data['data']['month_data']['last_mora']
        group_str = ''
        for i in data['data']['month_data']['group_by']:
            group_str = group_str + i['action'] + "：" + str(i['num']) + "（" + str(i['percent']) + "%）" + '\n'

        im = month_im.format(nickname,uid,day_stone,day_mora,lastday_stone,lastday_mora,month_stone,month_mora,lastmonth_stone,lastmonth_mora,group_str)
        await bot.send(ev,im,at_sender=True)
    except Exception as e:
        print(e.with_traceback)
        await bot.send(ev,'未找到绑定信息',at_sender=True)
        
#群聊内 签到 功能
@sv.on_fullmatch('签到')
async def _(bot:RinYuuki,  ev: CQEvent):
    try:
        qid = ev.sender["user_id"]
        uid = await selectDB(ev.sender['user_id'],mode = "uid")
        uid = uid[0]
        im = await sign(uid)
        await bot.send(ev,im,at_sender=True)
    except Exception as e:
        print(e.with_traceback)
        await bot.send(ev,'未找到绑定信息',at_sender=True)

#群聊内 数据库v2 迁移至 数据库v3 的命令，一般只需要更新时执行一次
@sv.on_fullmatch('优化Cookies')
async def _(bot:RinYuuki,  ev: CQEvent):
    try:
        im = await OpCookies()
        await bot.send(ev,im,at_sender=True)
    except Exception as e:
        print(e.with_traceback)
        pass

#群聊内 校验Cookies 是否正常的功能，不正常自动删掉
@sv.on_fullmatch('校验全部Cookies')
async def _(bot:RinYuuki,  ev: CQEvent):
    im = await CheckDB()
    await bot.send(ev,im)   

#群聊内 数据库v1 迁移至 数据库v2 的命令，一般只需要更新时执行一次
@sv.on_fullmatch('迁移Cookies')
async def _(bot:RinYuuki,  ev: CQEvent):
    im = await TransDB()
    await bot.send(ev,im)   

#群聊内 查询当前树脂状态以及派遣状态 的命令
@sv.on_fullmatch('当前状态')
async def _(bot:RinYuuki,  ev: CQEvent):
    try:
        uid = await selectDB(ev.sender['user_id'],mode = "uid")
        uid = uid[0]
        mes = await daily("ask",uid)
        im = mes[0]['message']
    except Exception as e:
        print(e.with_traceback)
        im = "没有找到绑定信息。"

    await bot.send(ev,im, at_sender=True)   
    
#群聊内 查询uid 的命令
@sv.on_prefix('uid')
async def _(bot:RinYuuki,  ev: CQEvent):
    image = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    message = ev.message.extract_plain_text()
    uid = re.findall(r"\d+", message)[0]  # str
    m = ''.join(re.findall('[\u4e00-\u9fa5]',message))
    if m == "深渊":
        try:
            if len(re.findall(r"\d+", message)) == 2:
                floor_num = re.findall(r"\d+", message)[1]
                im = await draw_abyss_pic(uid,ev.sender['nickname'],floor_num,image)
                await bot.send(ev, im, at_sender=True)
            else:
                im = await draw_abyss0_pic(uid,ev.sender['nickname'],image)
                await bot.send(ev, im, at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,'深渊输入错误！')
    elif m == "上期深渊":
        try:
            if len(re.findall(r"\d+", message)) == 2:
                floor_num = re.findall(r"\d+", message)[1]
                im = await draw_abyss_pic(uid,ev.sender['nickname'],floor_num,image,2,"2")
                await bot.send(ev, im, at_sender=True)
            else:
                im = await draw_abyss0_pic(uid,ev.sender['nickname'],image,2,"2")
                await bot.send(ev, im, at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,'深渊输入错误！')        
    else:
        try:
            im = await draw_pic(uid,ev.sender['nickname'],image,2)
            await bot.send(ev, im, at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,'输入错误！')
            
#群聊内 绑定uid 的命令，会绑定至当前qq号上
@sv.on_prefix('绑定uid')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    uid = re.findall(r"\d+", message)[0]  # str
    await connectDB(ev.sender['user_id'],uid)
    await bot.send(ev,'绑定uid成功！', at_sender=True)
    
#群聊内 绑定米游社通行证 的命令，会绑定至当前qq号上，和绑定uid不冲突，两者可以同时绑定
@sv.on_prefix('绑定mys')
async def _(bot:RinYuuki,  ev: CQEvent):
    message = ev.message.extract_plain_text()
    mys = re.findall(r"\d+", message)[0]  # str
    await connectDB(ev.sender['user_id'],None,mys)
    await bot.send(ev,'绑定米游社id成功！', at_sender=True)

#群聊内 绑定过uid/mysid的情况下，可以查询，默认优先调用米游社通行证，多出世界等级一个参数
@sv.on_prefix('查询')
async def _(bot,  ev):
    image = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    at = re.search(r"\[CQ:at,qq=(\d*)\]", str(ev.raw_message.strip()))
    message = ev.message.extract_plain_text()
    if at:
        qid = at.group(1)
        mi =await bot.get_group_member_info(group_id=ev.group_id, user_id=qid)
        nickname = mi["nickname"]
        uid = await selectDB(qid)
    else:
        nickname = ev.sender['nickname']
        uid = await selectDB(ev.sender['user_id'])
        
    m = ''.join(re.findall('[\u4e00-\u9fa5]',message))
    if uid:
        if m == "深渊":
            try:
                if len(re.findall(r"\d+", message)) == 1:
                    floor_num = re.findall(r"\d+", message)[0]
                    im = await draw_abyss_pic(uid[0],nickname,floor_num,image,uid[1])
                    await bot.send(ev, im, at_sender=True) 
                else:
                    im = await draw_abyss0_pic(uid[0],nickname,image,uid[1])
                    await bot.send(ev, im, at_sender=True)
            except Exception as e:
                print(e.with_traceback)
                await bot.send(ev,'输入错误！')
        elif m == "上期深渊":
            try:
                if len(re.findall(r"\d+", message)) == 1:
                    floor_num = re.findall(r"\d+", message)[0]
                    im = await draw_abyss_pic(uid[0],nickname,floor_num,image,uid[1],"2")
                    await bot.send(ev, im, at_sender=True)
                else:
                    im = await draw_abyss0_pic(uid[0],nickname,image,uid[1],"2")
                    await bot.send(ev, im, at_sender=True)
            except Exception as e:
                print(e.with_traceback)
                await bot.send(ev,'深渊输入错误！') 
        elif m == "词云":
            try:
                im = await draw_wordcloud(uid[0],image,uid[1])
                await bot.send(ev,im, at_sender=True)
            except Exception as e:
                print(e.with_traceback)
                await bot.send(ev,'遇到错误！') 
        elif m == "":
            try:
                bg = await draw_pic(uid[0],nickname,image,uid[1])
                await bot.send(ev, bg, at_sender=True)
            except Exception as e:
                print(e.with_traceback)
                await bot.send(ev,'输入错误！')
        else:
            pass
    else:
        await bot.send(ev,'未找到绑定记录！')

#群聊内 查询米游社通行证 的命令
@sv.on_prefix('mys')
async def _(bot:RinYuuki,  ev: CQEvent):
    image = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", str(ev.message))
    message = ev.message.extract_plain_text()
    uid = re.findall(r"\d+", message)[0]  # str
    m = ''.join(re.findall('[\u4e00-\u9fa5]',message))
    if m == "深渊":
        try:
            if len(re.findall(r"\d+", message)) == 2:
                floor_num = re.findall(r"\d+", message)[1]
                im = await draw_abyss_pic(uid,ev.sender['nickname'],floor_num,image,3)
                await bot.send(ev, im, at_sender=True)
            else:
                im = await draw_abyss0_pic(uid,ev.sender['nickname'],image,3)
                await bot.send(ev, im, at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,'深渊输入错误！')
    elif m == "上期深渊":
        try:
            if len(re.findall(r"\d+", message)) == 1:
                floor_num = re.findall(r"\d+", message)[0]
                im = await draw_abyss_pic(uid,ev.sender['nickname'],floor_num,image,3,"2")
                await bot.send(ev, im, at_sender=True)
            else:
                im = await draw_abyss0_pic(uid,ev.sender['nickname'],image,3,"2")
                await bot.send(ev, im, at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,'深渊输入错误！') 
    else:
        try:
            im = await draw_pic(uid,ev.sender['nickname'],image,3)
            await bot.send(ev, im, at_sender=True)
        except Exception as e:
            print(e.with_traceback)
            await bot.send(ev,'输入错误！')

#签到函数
async def sign(uid):
    try:
        sign_data = await MysSign(uid)        
        status = sign_data['message']                
        im = "\n"
        sign_info = await GetSignInfo(uid)
        sign_info_data = sign_info['data']
        if status == "OK" and sign_info_data['is_sign'] == True:
            mes_im = "签到成功"
        else:
            mes_im = status
        im = im + mes_im +"!" + "\n"

        sign_missed = sign_info_data['sign_cnt_missed']
        sign_list = await GetSignList()      
        getitem = sign_list['data']['awards'][int(sign_info_data['total_sign_day'])-1]['name']
        getnum = sign_list['data']['awards'][int(sign_info_data['total_sign_day'])-1]['cnt']
        get_im = f"本次签到获得{getitem}x{getnum}"        
        im = "\n" + mes_im +"!" + "\n" + get_im + "\n" + f"本月漏签次数：{sign_missed}"
            #im = im + "\n" + "本次签到获取物品请求失败"

    except Exception as e:
        print(e.with_traceback)
        im = im + "签到失败，请检查Cookies是否失效。"
    return im

#统计状态函数
async def daily(mode="push", uid=None):

    def seconds2hours(seconds: int) -> str:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    temp_list = []
    conn = sqlite3.connect('ID_DATA.db')
    c = conn.cursor()
    if mode == "push":
        cursor = c.execute(
            "SELECT *  FROM NewCookiesTable WHERE StatusA != ?", ("off",))
        c_data = cursor.fetchall()
    elif mode == "ask":
        c_data = ([uid, 0, 0, 0, 0, 0, 0],)

    for row in c_data:
        raw_data = await GetDaily(str(row[0]))
        if raw_data["retcode"] != 0:
            temp_list.append(
                {"qid": row[2], "gid": row[3], "message": "你的推送状态有误；可能是uid绑定错误或没有在米游社打开“实时便筏”功能。"})
        else:
            dailydata = raw_data["data"]
            current_resin = dailydata['current_resin']

            if current_resin >= row[6]:
                tip = ''

                if row[1] != 0:
                    tip = "\n==============\n你的树脂快满了！"
                max_resin = dailydata['max_resin']
                rec_time = ''
                # print(dailydata)
                if current_resin < 160:
                    resin_recovery_time = seconds2hours(
                        dailydata['resin_recovery_time'])
                    next_resin_rec_time = seconds2hours(
                        8 * 60 - ((dailydata['max_resin'] - dailydata['current_resin']) * 8 * 60 - int(dailydata['resin_recovery_time'])))
                    rec_time = f' ({next_resin_rec_time}/{resin_recovery_time})'

                finished_task_num = dailydata['finished_task_num']
                total_task_num = dailydata['total_task_num']
                is_extra_got = '已' if dailydata['is_extra_task_reward_received'] else '未'

                resin_discount_num_limit = dailydata['resin_discount_num_limit']
                used_resin_discount_num = resin_discount_num_limit - \
                    dailydata['remain_resin_discount_num']

                current_expedition_num = dailydata['current_expedition_num']
                max_expedition_num = dailydata['max_expedition_num']
                finished_expedition_num = 0
                expedition_info: list[str] = []
                for expedition in dailydata['expeditions']:
                    avatar: str = expedition['avatar_side_icon'][89:-4]
                    try:
                        avatar_name: str = avatar_json[avatar]
                    except KeyError:
                        avatar_name: str = avatar

                    if expedition['status'] == 'Finished':
                        expedition_info.append(f"{avatar_name} 探索完成")
                        finished_expedition_num += 1
                    else:
                        remained_timed: str = seconds2hours(
                            expedition['remained_time'])
                        expedition_info.append(
                            f"{avatar_name} 剩余时间{remained_timed}")
                expedition_data = "\n".join(expedition_info)

                coin = str(dailydata["current_home_coin"]) + "/" + str(dailydata["max_home_coin"])
                send_mes = daily_im.format(tip, current_resin, max_resin, rec_time, finished_task_num, total_task_num, is_extra_got, used_resin_discount_num,
                                        resin_discount_num_limit, coin,current_expedition_num, finished_expedition_num, max_expedition_num, expedition_data)

                temp_list.append(
                    {"qid": row[2], "gid": row[3], "message": send_mes})
    return temp_list

async def weapon_wiki(name,level = None):
    data = await GetWeaponInfo(name)
    if level:
        data2 = await GetWeaponInfo(name,level+"plus" if level else level)
        if data["substat"] != "":
            sp = data["substat"] + "：" + '%.1f%%' % (data2["specialized"] * 100) if data["substat"] != "元素精通" else data["substat"] + "：" + str(math.floor(data2["specialized"]))
        else:
            sp = ""
        im = (data["name"] + "\n等级：" + str(data2["level"]) + "（突破" + str(data2["ascension"]) + "）" + 
                    "\n攻击力：" + str(math.floor(data2["attack"])) + "\n" + sp)
    else:
        name = data['name']
        type = data['weapontype']
        star = data['rarity'] + "星"
        info = data['description']
        atk = str(data['baseatk'])
        sub_name = data['substat']
        if data['subvalue'] != "":
            sub_val = (data['subvalue'] +
                    '%') if sub_name != '元素精通' else data['subvalue']
            sub = "\n" + "【" + sub_name + "】" + sub_val
        else:
            sub = ""

        if data['effectname'] != "":
            raw_effect = data['effect']
            rw_ef = []
            for i in range(len(data['r1'])):
                now = ''
                for j in range(1, 6):
                    now = now + data['r{}'.format(j)][i] + "/"
                now = now[:-1]
                rw_ef.append(now)
            raw_effect = raw_effect.format(*rw_ef)
            effect = "\n" + "【" + data['effectname'] + "】" + "：" + raw_effect
        else:
            effect = ""
        im = weapon_im.format(name, type, star, info, atk,
                            sub, effect)
    return im

async def char_wiki(name, mode="char", level=None):
    data = await GetCharInfo(name, mode, level if mode == "char" else None)
    if mode == "char":
        if isinstance(data,str):
            raw_data = data.replace("[","").replace("\n","").replace("]","").replace(" ","").replace("'","").split(',')
            if data.replace("\n","").replace(" ","") == "undefined":
                im = "不存在该角色或类型。"
            else:
                im = ','.join(raw_data)
        elif level:
            data2 = await GetCharInfo(name, mode)
            sp = data2["substat"] + "：" + '%.1f%%' % (data["specialized"] * 100) if data2["substat"] != "元素精通" else data2["substat"] + "：" + str(math.floor(data["specialized"]))
            im = (data2["name"] + "\n等级：" + str(data["level"]) + "\n血量：" + str(math.floor(data["hp"])) +
                "\n攻击力：" + str(math.floor(data["attack"])) + "\n防御力：" + str(math.floor(data["defense"])) +
                "\n" + sp)
        else:
            name = data['title'] + ' — ' + data['name']
            star = data['rarity']
            type = data["weapontype"]
            element = data['element']
            up_val = data['substat']
            bdday = data['birthday']
            polar = data['constellation']
            cv = data['cv']['chinese']
            info = data['description']
            im = char_info_im.format(
                name, star, type, element, up_val, bdday, polar, cv, info)
    elif mode == "costs":
        im = "【天赋材料(一份)】\n{}\n【突破材料】\n{}"
        im1 = ""
        im2 = ""
        
        talent_temp = {}
        talent_cost = data[1]["costs"]
        for i in talent_cost.values():
            for j in i:
                if j["name"] not in talent_temp:
                    talent_temp[j["name"]] = j["count"]
                else:
                    talent_temp[j["name"]] = talent_temp[j["name"]] + j["count"]
        for k in talent_temp:
            im1 = im1 + k + ":" + str(talent_temp[k]) + "\n"

        temp = {}
        cost = data[0]
        for i in range(1,7):
            for j in cost["ascend{}".format(i)]:
                if j["name"] not in temp:
                    temp[j["name"]] = j["count"]
                else:
                    temp[j["name"]] = temp[j["name"]] + j["count"]
                    
        for k in temp:
            im2 = im2 + k + ":" + str(temp[k]) + "\n"
        
        im = im.format(im1,im2)
    elif mode == "constellations":
        im = "【" + data["c{}".format(level)]['name'] + "】" + "：" + \
            "\n" + data["c{}".format(level)]['effect'].replace("*", "")
    elif mode == "talents":
        if int(level) <= 3 :
            if level == "1":
                data = data["combat1"]
            elif level == "2":
                data = data["combat2"]
            elif level == "3":
                data = data["combat3"]
            skill_name = data["name"]
            skill_info = data["info"]
            skill_detail = ""

            for i in data["attributes"]["parameters"]:
                temp = ""
                for k in data["attributes"]["parameters"][i]:
                    temp += "%.2f%%" % (k * 100) + "/"
                data["attributes"]["parameters"][i] = temp[:-1]

            for i in data["attributes"]["labels"]:
                #i = i.replace("{","{{")
                i = re.sub(r':[a-zA-Z0-9]+}', "}", i)
                #i.replace(r':[a-zA-Z0-9]+}','}')
                skill_detail += i + "\n"

            skill_detail = skill_detail.format(**data["attributes"]["parameters"])

            im = "【{}】\n{}\n————\n{}".format(skill_name,skill_info,skill_detail)

        else:
            if level == "4":
                data = data["passive1"]
            elif level == "5":
                data = data["passive2"]
            elif level == "6":
                data = data["passive3"]
            elif level == "7":
                data = data["passive4"]
            skill_name = data["name"]
            skill_info = data["info"]
            im = "【{}】\n{}".format(skill_name,skill_info)
    return im
