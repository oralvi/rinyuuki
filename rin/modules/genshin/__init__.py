from .getDB import (CheckDB, OpenPush, connectDB, deletecache, selectDB, get_alots, config_check)
from .getImg import (draw_abyss0_pic, draw_abyss_pic, draw_event_pic, draw_pic, draw_wordcloud)
from .getMes import (foods_wiki, artifacts_wiki, enemies_wiki, sign, daily, weapon_wiki, char_wiki, audio_wiki, award, deal_ck)

from nonebot import *
from hoshino import Service,R,priv,util
from hoshino.typing import MessageSegment,CQEvent, HoshinoBot

import hoshino
import asyncio
import sqlite3,random,traceback,os,re
import base64

sv = Service('genshinuid')
bot = get_bot()

FILE_PATH = os.path.dirname(__file__)
FILE2_PATH = os.path.join(FILE_PATH,'mys')
INDEX_PATH = os.path.join(FILE2_PATH, 'index')
Texture_PATH = os.path.join(FILE2_PATH,'texture2d')

@sv.on_prefix('语音')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        message = message.replace(' ', "")
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        im = await audio_wiki(name,message)
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_fullmatch('活动列表')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
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
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_fullmatch('御神签')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        qid = ev.sender["user_id"]
        raw_data = await get_alots(qid)
        im = base64.b64decode(raw_data).decode("utf-8")
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_prefix('材料')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        message = message.replace(' ', "")
        im = await char_wiki(message,"costs")
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
    
@sv.on_prefix('原魔')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        im = await enemies_wiki(message)
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_prefix('食物')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        im = await foods_wiki(message)
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_prefix('圣遗物')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        im = await artifacts_wiki(message)
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_prefix('天赋')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        num = re.findall(r"[0-9]+", message)
        if len(num) == 1:
            im = await char_wiki(name,"talents",num[0])
        else:
            im = "参数不正确。"
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_prefix('武器')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        level = re.findall(r"[0-9]+", message)
        if len(level) == 1:
            im = await weapon_wiki(name,level=level[0])
        else:
            im = await weapon_wiki(name)
        await bot.send(ev,im,at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_prefix('角色')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        message = message.replace(' ', "")
        name = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        level = re.findall(r"[0-9]+", message)
        if len(level) == 1:
            im = await char_wiki(name,"char",level=level[0])
        else:
            im = await char_wiki(name)
        await bot.send(ev,im)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

@sv.on_prefix('命座')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        num = int(re.findall(r"\d+", message)[0])  # str
        m = ''.join(re.findall('[\u4e00-\u9fa5]', message))
        if num<= 0 or num >6:
            await bot.send(ev,"你家{}有{}命？".format(m,num),at_sender = True)
        else:
            im = await char_wiki(m, "constellations", num)
            await bot.send(ev,im,at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
    
#每日零点清空cookies使用缓存
@sv.scheduled_job('cron', hour='0')
async def delete():
    await deletecache()

@sv.scheduled_job('cron', hour='2')
async def delete():
    await draw_event_pic()

@sv.on_fullmatch('全部重签')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        if ev.user_id not in bot.config.SUPERUSERS:
            return
        await bot.send(ev,"已开始执行")
        await dailysign()
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

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
    temp_list = []
    for row in c_data:
        im = await sign(str(row[0]))
        if row[4] == "on":
            try:
                await bot.send_private_msg(user_id = row[2],message = im)
            except:
                traceback.print_exc()
                print(im + "\nerror")
        else:
            message = f"[CQ:at,qq={row[2]}]\n{im}"
            if await config_check("SignReportSimple"):
                for i in temp_list:
                    if row[4] == i["push_group"]:
                        if im == "签到失败，请检查Cookies是否失效。" or im.startswith("网络有点忙，请稍后再试~!"):
                            i["failed"] += 1
                            i["push_message"] += "\n" + message
                        else:
                            i["success"] += 1
                        break
                else:
                    if im == "签到失败，请检查Cookies是否失效。":
                        temp_list.append({"push_group":row[4],"push_message":message,"success":0,"failed":1})
                    else:
                        temp_list.append({"push_group":row[4],"push_message":"","success":1,"failed":0})
            else:
                for i in temp_list:
                    if row[4] == i["push_group"] and i["num"] < 4:
                        i["push_message"] += "\n" + message
                        i["num"] += 1
                        break
                else:
                    temp_list.append({"push_group":row[4],"push_message":message,"num":1})
        await asyncio.sleep(6+random.randint(1,3))
    if await config_check("SignReportSimple"):
        for i in temp_list:
            try:
                report = "以下为签到失败报告：{}".format(i["push_message"]) if i["push_message"] != "" else ""
                await bot.send_group_msg(group_id = i["push_group"],message = "今日自动签到已完成！\n本群共签到成功{}人，共签到失败{}人。{}".format(i["success"],i["failed"],report))
            except:
                traceback.print_exc()
                print(i["push_message"])
            await asyncio.sleep(4+random.randint(1,3))
    else:
        for i in temp_list:
            try:
                await bot.send_group_msg(group_id = i["push_group"],message = i["push_message"])
            except:
                traceback.print_exc()
                print(i["push_message"])
            await asyncio.sleep(4+random.randint(1,3))
    conn.close()
    return

#每隔半小时检测树脂是否超过设定值
@sv.scheduled_job('interval', hours = 1)
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
            await deal_ck(mes,userid)
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=f'添加Cookies成功！\nCookies属于个人重要信息，如果你是在不知情的情况下添加，请马上修改米游社账户密码，保护个人隐私！\n————\n如果需要【开启自动签到】和【开启推送】还需要使用命令“绑定uid”绑定你的uid。\n例如：绑定uid123456789。')
        except Exception as e:
            traceback.print_exc()
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message='校验失败！请输入正确的Cookies！\n错误信息为{}'.format(e))
    elif '开启推送' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"on","StatusA")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            traceback.print_exc()
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")
    elif '关闭推送' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"off","StatusA")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            traceback.print_exc()
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")
    elif '开启自动签到' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"on","StatusB")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            traceback.print_exc()
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")
    elif '关闭自动签到' in message:
        try:
            uid = await selectDB(userid,mode = "uid")
            im = await OpenPush(int(uid[0]),userid,"off","StatusA")
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message=im)
        except Exception as e:
            traceback.print_exc()
            await bot.send_msg(self_id=sid, user_id=userid, group_id=gid, message="未找到uid绑定记录。")

#群聊开启 自动签到 和 推送树脂提醒 功能
@sv.on_prefix('开启')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
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
                traceback.print_exc()
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
                traceback.print_exc()
                await bot.send(ev,"未绑定uid信息！",at_sender=True)
        elif m == "简洁签到报告":
            try:
                if qid in bot.config.SUPERUSERS:
                    _ = await config_check("SignReportSimple","OPEN")
                    await bot.send(ev,"成功!", at_sender=True)
                else:
                    return
            except Exception as e:
                await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
                traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
            
#群聊关闭 自动签到 和 推送树脂提醒 功能
@sv.on_prefix('关闭')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
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
                traceback.print_exc()
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
                traceback.print_exc()
                await bot.send(ev,"未绑定uid信息！",at_sender=True)
        elif m == "简洁签到报告":
            try:
                if qid in bot.config.SUPERUSERS:
                    _ = await config_check("SignReportSimple","CLOSED")
                    await bot.send(ev,"成功!", at_sender=True)
                else:
                    return
            except Exception as e:
                await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
                traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
            
#群聊内 每月统计 功能
@sv.on_fullmatch('每月统计')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        qid = ev.sender["user_id"]
        uid = await selectDB(ev.sender['user_id'],mode = "uid")
        uid = uid[0]
        im = await award(uid)
        await bot.send(ev,im,at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,'未找到绑定信息',at_sender=True)
        
#群聊内 签到 功能
@sv.on_fullmatch('签到')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        qid = ev.sender["user_id"]
        uid = await selectDB(ev.sender['user_id'],mode = "uid")
        uid = uid[0]
        im = await sign(uid)
        await bot.send(ev,im,at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,'未找到绑定信息',at_sender=True)

#群聊内 校验Cookies 是否正常的功能，不正常自动删掉
@sv.on_fullmatch('校验全部Cookies')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        raw_mes = await CheckDB()
        im = raw_mes[0]
        await bot.send(ev,im)
        for i in raw_mes[1]:
            await bot.send_private_msg(user_id = i[0],
                                        message = "您绑定的Cookies（uid{}）已失效，以下功能将会受到影响：\n查看完整信息列表\n查看深渊配队\n自动签到/当前状态/每月统计\n请及时重新绑定Cookies并重新开关相应功能。".format(i[1]))
            await asyncio.sleep(3+random.randint(1,3)) 
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

#群聊内 查询当前树脂状态以及派遣状态 的命令
@sv.on_fullmatch('当前状态')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        uid = await selectDB(ev.sender['user_id'],mode = "uid")
        uid = uid[0]
        mes = await daily("ask",uid)
        im = mes[0]['message']
    except Exception as e:
        traceback.print_exc()
        im = "没有找到绑定信息。"

    await bot.send(ev,im, at_sender=True)   
    
#群聊内 查询uid 的命令
@sv.on_prefix('uid')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
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
            except TypeError:
                await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                traceback.print_exc()
            except Exception as e:
                await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                traceback.print_exc()
        elif m == "上期深渊":
            try:
                if len(re.findall(r"\d+", message)) == 2:
                    floor_num = re.findall(r"\d+", message)[1]
                    im = await draw_abyss_pic(uid,ev.sender['nickname'],floor_num,image,2,"2")
                    await bot.send(ev, im, at_sender=True)
                else:
                    im = await draw_abyss0_pic(uid,ev.sender['nickname'],image,2,"2")
                    await bot.send(ev, im, at_sender=True)
            except TypeError:
                await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                traceback.print_exc()
            except Exception as e:
                await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                traceback.print_exc()    
        else:
            try:
                im = await draw_pic(uid,ev.sender['nickname'],image,2)
                await bot.send(ev, im, at_sender=True)
            except TypeError:
                await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                traceback.print_exc()
            except Exception as e:
                await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
            
#群聊内 绑定uid 的命令，会绑定至当前qq号上
@sv.on_prefix('绑定uid')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        uid = re.findall(r"\d+", message)[0]  # str
        await connectDB(ev.sender['user_id'],uid)
        await bot.send(ev,'绑定uid成功！', at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
    
#群聊内 绑定米游社通行证 的命令，会绑定至当前qq号上，和绑定uid不冲突，两者可以同时绑定
@sv.on_prefix('绑定mys')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
        message = ev.message.extract_plain_text()
        mys = re.findall(r"\d+", message)[0]  # str
        await connectDB(ev.sender['user_id'],None,mys)
        await bot.send(ev,'绑定米游社id成功！', at_sender=True)
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

#群聊内 绑定过uid/mysid的情况下，可以查询，默认优先调用米游社通行证，多出世界等级一个参数
@sv.on_prefix('查询')
async def _(bot,  ev):
    try:
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
                except TypeError:
                    await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                    traceback.print_exc()
                except Exception as e:
                    await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                    traceback.print_exc()
            elif m == "上期深渊":
                try:
                    if len(re.findall(r"\d+", message)) == 1:
                        floor_num = re.findall(r"\d+", message)[0]
                        im = await draw_abyss_pic(uid[0],nickname,floor_num,image,uid[1],"2")
                        await bot.send(ev, im, at_sender=True)
                    else:
                        im = await draw_abyss0_pic(uid[0],nickname,image,uid[1],"2")
                        await bot.send(ev, im, at_sender=True)
                except TypeError:
                    await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                    traceback.print_exc()
                except Exception as e:
                    await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                    traceback.print_exc()
            elif m == "词云":
                try:
                    im = await draw_wordcloud(uid[0],image,uid[1])
                    await bot.send(ev,im, at_sender=True)
                except TypeError:
                    await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                    traceback.print_exc()
                except Exception as e:
                    await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                    traceback.print_exc()
            elif m == "":
                try:
                    bg = await draw_pic(uid[0],nickname,image,uid[1])
                    await bot.send(ev, bg, at_sender=True)
                except TypeError:
                    await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                    traceback.print_exc()
                except Exception as e:
                    await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                    traceback.print_exc()
            else:
                pass
        else:
            await bot.send(ev,'未找到绑定记录！')
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))

#群聊内 查询米游社通行证 的命令
@sv.on_prefix('mys')
async def _(bot:HoshinoBot,  ev: CQEvent):
    try:
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
            except TypeError:
                await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                traceback.print_exc()
            except Exception as e:
                await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                traceback.print_exc()
        elif m == "上期深渊":
            try:
                if len(re.findall(r"\d+", message)) == 1:
                    floor_num = re.findall(r"\d+", message)[0]
                    im = await draw_abyss_pic(uid,ev.sender['nickname'],floor_num,image,3,"2")
                    await bot.send(ev, im, at_sender=True)
                else:
                    im = await draw_abyss0_pic(uid,ev.sender['nickname'],image,3,"2")
                    await bot.send(ev, im, at_sender=True)
            except TypeError:
                await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                traceback.print_exc()
            except Exception as e:
                await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                traceback.print_exc()
        else:
            try:
                im = await draw_pic(uid,ev.sender['nickname'],image,3)
                await bot.send(ev, im, at_sender=True)
            except TypeError:
                await bot.send("获取失败，可能是Cookies失效或者未打开米游社角色详情开关。")
                traceback.print_exc()
            except Exception as e:
                await bot.send("获取失败，有可能是数据状态有问题,\n{}\n请检查后台输出。".format(e))
                traceback.print_exc()
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,"发生错误 {},请检查后台输出。".format(e))
