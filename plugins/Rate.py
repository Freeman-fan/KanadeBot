import nonebot
from nonebot import on_startup

from plugins.Modules.JpRate import GetJpRate
from plugins.Modules.GetMaeRate import GetMaeRate


__plugin_name__ = "汇率"


class Rate:
    def __init__(self, Jprate: float = 0.05, maeRate: float = 0.052):
        self.jpRate = Jprate
        self.maeRate = maeRate


rate = Rate()


# 初始化汇率值
@on_startup
async def _():
    global rate
    jprate_response = GetJpRate()
    if jprate_response.response_code == 0:
        rate.jpRate = jprate_response.response_rate
    maerate_response = await GetMaeRate()
    if maerate_response.response_code == 0:
        rate.maeRate = maerate_response.response_rate


# 定时获得日元汇率值并更新
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


# 定时获得mae汇率值并更新
@nonebot.scheduler.scheduled_job("cron", hour="*")
async def _():
    global maeRate
    maerate_response = await GetMaeRate()
    if maerate_response.response_code == 0:
        maeRate = maerate_response.response_rate
    elif maerate_response.response_code == 1:
        bot = nonebot.get_bot()
        await bot.send_private_msg(
            user_id=501079827,
            message=f"Mae汇率请求失败\n{maerate_response.response_data}",
        )
