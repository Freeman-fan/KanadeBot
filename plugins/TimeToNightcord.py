import nonebot


__plugin_name__ = '25时，上线！'


@nonebot.scheduler.scheduled_job('cron', hour = 1)
async def _():
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=937806799, message='啊，到点了，上线看看其他人在做什么吧……')