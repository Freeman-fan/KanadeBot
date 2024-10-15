import nonebot
from nonebot import on_websocket_connect

from plugins.CustomClass.response import FuncResponse
from plugins.Modules.JpRate import GetJpRate, JpRateResponse

Jprate = 0.05


# 初始化汇率值
@on_websocket_connect
async def _():
    global Jprate
    bot = nonebot.get_bot()

    response = GetJpRate()
    if response.response_code == 0:
        Jprate = response.response_rate
        await bot.send_private_msg(
            user_id=501079827,
            message=f"日元汇率初始化成功",
        )
    elif response.response_code == 1:
        await bot.send_private_msg(
            user_id=501079827,
            message=f"日元汇率初始化失败，将使用默认值0.05\n{response.response_data}",
        )


# 定时获得汇率值并更新
@nonebot.scheduler.scheduled_job("cron", hour="*")
async def _():
    global Jprate
    bot = nonebot.get_bot()

    response = GetJpRate()
    if response.response_code == 0:
        rate_update = response.response_rate
        date_update = response.response_date
        if rate_update != Jprate:
            await bot.send_private_msg(
                user_id=501079827,
                message=f"日元汇率变动：{rate_update}\n更新时间{date_update}",
            )
            Jprate = rate_update
    elif response.response_code == 1:
        await bot.send_private_msg(
            user_id=501079827, message=f"日元汇率请求失败\n{response.response_data}"
        )
