import nonebot
from nonebot import on_startup, on_command, CommandSession

from plugins.Modules.GetJpRate import JpRate
from plugins.Modules.GetMaeRate import MaeRate
from plugins.CustomClass.response import FuncResponse


__plugin_name__ = "汇率"


class Rate(JpRate, MaeRate):
    def __init__(self, jpRate: float = 0.05, maeRate: float = 0.052, date: str = ""):
        JpRate.__init__(self, jpRate, date)
        MaeRate.__init__(self, maeRate)

    # 更新所有汇率
    async def UpdateRate(self) -> FuncResponse:
        jpUpdate = JpRate.UpdateRate(self)
        maeUpdate = MaeRate.UpdateRate(self)
        if jpUpdate.response_code == 0 and maeUpdate.response_code == 0:
            return FuncResponse(0, "")
        else:
            return FuncResponse(
                1, jpUpdate.response_data + "\n" + maeUpdate.response_data
            )

    # 更新日元汇率
    async def UpdateJpRate(self) -> FuncResponse:
        jpUpdate = JpRate.UpdateRate(self)
        return jpUpdate

    # 更新mae汇率
    async def UpdateMaeRate(self) -> FuncResponse:
        maeUpdate = MaeRate.UpdateRate(self)
        return maeUpdate


pushrate = 0.0
rate = Rate()
bot = nonebot.get_bot()


# 初始化汇率值
@on_startup
async def _():
    global rate
    await rate.UpdateRate()


# 定时更新汇率
@nonebot.scheduler.scheduled_job("cron", minute="*")
async def _():
    global rate
    updateRate = await rate.UpdateRate()
    if updateRate.response_code == 0:
        return
    elif updateRate.response_code == 1:
        await bot.send_private_msg(
            user_id=501079827, message=f"汇率更新失败\n{updateRate.response_data}"
        )


# 定时推送日元汇率
@nonebot.scheduler.scheduled_job("cron", hour="*")
async def _():
    global rate, pushrate
    if rate != pushrate:
        pushrate = rate
        await bot.send_private_msg(
            user_id=501079827,
            message=f"日元汇率变动：{rate.jpRate}\n更新时间：{rate.date}",
        )


# 主动拉取日元汇率
@on_command("日元", only_to_me=False)
async def _(session: CommandSession):
    global rate
    await rate.UpdateJpRate()
    await session.send(f"日元汇率：{rate.jpRate}\n更新时间：{rate.date}")


# 主动拉取mae汇率
@on_command("汇率", only_to_me=False)
async def _(session: CommandSession):
    global rate
    await rate.UpdateMaeRate()
    await session.send(f"Mae汇率：{rate.maeRate}")
