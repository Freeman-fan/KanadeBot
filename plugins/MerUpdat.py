import aiocqhttp
import nonebot
from nonebot import on_startup, on_command, CommandSession

import time

from plugins.Modules.GetMerUpdata import GetMerUpdate, UpdateResponse


__plugin_name__ = "监控mer商品更新信息"


@on_startup
async def _():
    global getmerupdata
    getmerupdata = GetMerUpdate()


# 添加监控
@on_command("监控", only_to_me=False)
async def Add(session: CommandSession):
    mNum = session.current_arg_text.strip()
    additem = await getmerupdata.AddItem(mNum, str(session.event.user_id))
    text = additem.response_data
    text = f"[CQ:reply,id={session.event.message_id}]" + text
    await session.send(message=text)


# 删除监控
@on_command("删除", only_to_me=False)
async def Del(session: CommandSession):
    mNum = session.current_arg_text.strip()
    delItem = getmerupdata.DelItem(mNum, str(session.event.user_id))
    text = delItem.response_data
    text = f"[CQ:reply,id={session.event.message_id}]" + text
    await session.send(message=text)


# 查监控
@on_command("查监控", only_to_me=False)
async def IdItem(session: CommandSession):
    id = str(session.event.user_id)
    idItem = getmerupdata.GetIdItem(id)
    text = ""
    for item in idItem.response_data:
        text += item
        if item != idItem.response_data[-1]:
            text += "\n"
    text = f"[CQ:reply,id={session.event.message_id}]" + text
    await session.send(message=text)


# 主动更新
@nonebot.scheduler.scheduled_job("interval", seconds=60)
async def update():
    bot = nonebot.get_bot()
    updateAll = await getmerupdata.GetAllUpdate()
    if updateAll.response_code == -1:
        return
    elif updateAll.response_code == 1:
        await bot.send_private_msg(user_id=501079827, message=updateAll.response_data)
    elif updateAll.response_code == 0:
        for update in updateAll.response_data:
            text = update.mNum
            if update.updateId == 1:
                text += "\n名称变动\n"
                text += f"{update.oldData} -> \n {update.newData}"
            elif update.updateId == 2:
                text += "\n价格变动\n"
                text += f"{update.oldData}y -> {update.newData}y"
            elif update.updateId == 3:
                text += "\n商品售出\n已结束监控"
            elif update.updateId == 4:
                text += "\n留言变动\n"
                text += f"{update.newData[0]}: {update.newData[1]}"
            elif update.updateId == 5:
                text += "\n商品被删除\n已结束监控"

            ids = update.id.split()
            print(ids,update.id)
            for id in ids:
                await bot.send_private_msg(user_id=int(id), message=text)

