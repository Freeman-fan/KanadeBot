from nonebot import scheduler
from nonebot.log import logger

import plugins.MerGoodsSearch
import plugins.MerUpdate
import plugins.Rate

import time

plugin_name = "定时任务触发器"


# 整点任务
@scheduler.scheduled_job("cron", hour="*")
async def scheduled_job_1hour():
    print("1小时任务")
    await plugins.Rate.PushRate()
    logger.info(f'整点任务触发')


# 整分钟任务
@scheduler.scheduled_job("cron", minute="*")
async def scheduled_job_1min():
    await plugins.MerUpdate.MerItemUpdate()
    await plugins.Rate.UpdateRate()
    logger.info(f"整分钟任务触发")


# 10秒任务
@scheduler.scheduled_job("interval", seconds=10)
async def scheduled_job_10sec():
    await plugins.MerGoodsSearch.MerPush()
    logger.info(f"10秒定时器触发")
