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
@nonebot.scheduler.scheduled_job("interval", seconds=30)
async def update():
    bot = nonebot.get_bot()
    updateAll = await getmerupdata.GetAllUpdate()
    if updateAll.response_code == -1:
        return
    elif updateAll.response_code == 1:
        await bot.send_private_msg(501079827, message=updateAll.response_data)
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
                text += "\n商品售出\n已删除监控"
            elif update.updateId == 4:
                text += "\n留言变动\n"
                text += f"{update.newData[0]}: {update.newData[1]}"

            ids = update.id.split()
            print(ids,update.id)
            for id in ids:
                await bot.send_private_msg(user_id=int(id), message=text)


# @nonebot.scheduler.scheduled_job("interval", minutes=1)
# async def _():
#     bot = nonebot.get_bot()
#     updatemNums = getmerupdata.GetAllmNum()

#     for mNum in updatemNums:
#         database_value = getmerupdata.GetItemInfo(mNum=mNum)
#         new_value = await GetMerItem(mNum=mNum)

#         db_jpprice = database_value["jpprice"]
#         db_status = database_value["status"]
#         db_commentNum = database_value["commentNum"]
#         _, _, _, new_jpprice, _, new_status, _, new_commentlist = new_value

#         id = getmerupdata.GetID(mNum=mNum)
#         if new_jpprice != db_jpprice:
#             getmerupdata.UpdataItem(mNum=mNum, field="jpprice", value=new_jpprice)
#             message = f"价格变动\n{mNum}\n-->{new_jpprice} | {new_jpprice * 0.052:.2f} | {(new_jpprice+50)*maeRate:.2f}"
#             await bot.send_private_msg(user_id=id, message=message)
#         elif new_status != db_status:
#             getmerupdata.DelItem(mNum=mNum)
#             message = f'商品售出\n{mNum}\n已从监视列表中移除'
#             await bot.send_private_msg(user_id=id, message=message)
#         elif len(new_commentlist) != db_commentNum:
#             getmerupdata.UpdataItem(mNum=mNum, field='commentNum', value=len(new_commentlist))
#             comment = new_commentlist[0]
#             comment_sender = comment[0]
#             comment_text = comment[1]
#             message = f'留言更新\n{mNum}\n{comment_sender}: {comment_text}'
#             await bot.send_private_msg(user_id=id, message=message)
#         break
