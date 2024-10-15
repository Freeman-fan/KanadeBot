import aiocqhttp
import nonebot
from nonebot import on_startup, on_command, CommandSession

import time
import json

from plugins.Modules.GetMerItem import GetMerItem
from plugins.MerGoodsSearch import maeRate
from plugins.Modules.GetMerUpdata import GetMerUpdate


__plugin_name__ = "监控mer商品更新信息"


@on_startup
async def _():
    global getmerupdata
    getmerupdata = GetMerUpdate()


@nonebot.scheduler.scheduled_job("interval", minutes=1)
async def _():
    bot = nonebot.get_bot()
    updatemNums = getmerupdata.GetAllmNum()

    for mNum in updatemNums:
        database_value = getmerupdata.GetItemInfo(mNum=mNum)
        new_value = await GetMerItem(mNum=mNum)

        db_jpprice = database_value["jpprice"]
        db_status = database_value["status"]
        db_commentNum = database_value["commentNum"]
        _, _, _, new_jpprice, _, new_status, _, new_commentlist = new_value

        id = getmerupdata.GetID(mNum=mNum)
        if new_jpprice != db_jpprice:
            getmerupdata.UpdataItem(mNum=mNum, field="jpprice", value=new_jpprice)
            message = f"价格变动\n{mNum}\n-->{new_jpprice} | {new_jpprice * 0.052:.2f} | {(new_jpprice+50)*maeRate:.2f}"
            await bot.send_private_msg(user_id=id, message=message)
        elif new_status != db_status:
            getmerupdata.DelItem(mNum=mNum)
            message = f'商品售出\n{mNum}\n已从监视列表中移除'
            await bot.send_private_msg(user_id=id, message=message)
        elif len(new_commentlist) != db_commentNum:
            getmerupdata.UpdataItem(mNum=mNum, field='commentNum', value=len(new_commentlist))
            comment = new_commentlist[0]
            comment_sender = comment[0]
            comment_text = comment[1]
            message = f'留言更新\n{mNum}\n{comment_sender}: {comment_text}'
            await bot.send_private_msg(user_id=id, message=message)
        break


@on_command('监控', only_to_me=False)
async def _(session: CommandSession):
    mNum = session.current_arg_text.strip()