import aiocqhttp
import nonebot
from nonebot import on_startup, on_websocket_connect

import time
import json
import re
import os
import glob

from plugins.MaeModule.RequestMae import RequestMae
from plugins.MaeModule.GetMaeRate import GetMaeRate


__plugin_name__ = "爬取mer商品并推送"

requests = []
maeRate = 0


# 初始化
@on_startup
async def _():
    global maeRate
    maeRate = await GetMaeRate()

    # 构建匹配所有 'mer_*.db' 文件的路径模式
    pattern = "./Database/mer_*.db"

    # 使用 glob.glob 查找所有匹配的文件路径
    for db_path in glob.glob(pattern):
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"已删除数据库文件：{db_path}")
    try:
        config_path = ".\plugins\Config\GetMerItem.json"
        with open(config_path, "r", encoding="utf-8-sig") as configfile:
            data = json.load(configfile)
        for item in data:
            name = item.get("name")
            target_type = item.get("target_type")
            target_id = item.get("target_id")
            keyword = item.get("keyword")
            priceMin = item.get("priceMin")
            priceMax = item.get("priceMax")
            inuse = item.get("inuse")
            print(f"{name}:已成功加载配置")
            requesemae = RequestMae(
                name=name,
                target_type=target_type,
                target_id=target_id,
                keyword=keyword,
                priceMin=priceMin,
                priceMax=priceMax,
                inuse=inuse,
            )
            requests.append(requesemae)
            print(f"{name}:数据库初始化成功")
    except Exception as e:
        print(str(e))


# 每小时更新一次mae汇率
@nonebot.scheduler.scheduled_job("interval", hours=1)
async def updateMaeRate():
    global maeRate
    maeRate = await GetMaeRate()


# 每秒抓取并推送
@nonebot.scheduler.scheduled_job("interval", seconds=10)
async def _():
    bot = nonebot.get_bot()
    for request in requests:
        if request.inuse == True:
            request.Getdata()
            UnsandData = request.GetUnsandData()
            if UnsandData != []:
                for data in UnsandData:
                    mNum, name, jpprice, firstphoto = data
                    match = re.match(
                        r"https?://mercdn\.maetown\.cn/c!/w=240,f=webp/thumb/photos/(m\d+)_1\.jpg\?(\d+)",
                        firstphoto,
                    )
                    if match:
                        # 提取匹配的组
                        product_id = match.group(1)
                        query_param = match.group(2)
                        # 构造新的链接
                        firstphoto = f"https://mercdn.maetown.cn/item/detail/orig/photos/{product_id}_1.jpg?{query_param}"
                    kPrice = round(jpprice * 0.052, 2)
                    maePrice = round((jpprice + 50) * maeRate, 2)
                    if jpprice == 9999999:
                        jpprice = "?"
                        maePrice = "?"
                        kPrice = "?"
                    message = f"{mNum}\n{name}\n{jpprice}y | {kPrice}r | {maePrice}r [CQ:image,file={firstphoto}] https://www.maetown.cn/wap/#/pages/base/gDetail/gDetail?gId={mNum}"
                    if request.target_type == "private":
                        for id in request.target_id:
                            await bot.send_private_msg(user_id=id, message=message)
                    elif request.target_type == "group":
                        for id in request.target_id:
                            await bot.send_group_msg(group_id=id, message=message)
                    time.sleep(0.1)
