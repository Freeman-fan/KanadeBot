import nonebot
from nonebot import on_startup

import json
import re
import os
import glob

from plugins.Rate import rate
from plugins.Modules.RequestMae import RequestMae


__plugin_name__ = "爬取mer商品并推送"

requests = []


# 初始化
@on_startup
async def _():
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
            print(
                f"{name}:已成功加载配置，关键词{keyword}，状态：{'已启用'if inuse == True else '未启用'}"
            )
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


# 抓取并推送
@nonebot.scheduler.scheduled_job("interval", seconds=10)
async def _():
    bot = nonebot.get_bot()
    for request in requests:
        if request.inuse == True:
            request.Getdata()
            UnsandData = request.GetUnsandData()
            if UnsandData != []:
                messages = ''
                for data in UnsandData:
                    mNum, name, jpprice, firstphoto = data
                    match = re.match(
                        r"https?://mercdn2\.maetown\.cn/c!/w=240,f=webp/thumb/photos/(m\d+)_1\.jpg\?(\d+)",
                        firstphoto,
                    )
                    if match:
                        # 提取匹配的组
                        product_id = match.group(1)
                        # 构造新的链接
                        firstphoto = f"https://image02.doorzo.net/c!/w=240/thumb/photos/{product_id}_1.jpg"
                    kPrice = round(jpprice * 0.052, 2)
                    maePrice = round((jpprice + 50) * rate.maeRate, 2)
                    if jpprice == 9999999:
                        jpprice = "?"
                        maePrice = "?"
                        kPrice = "?"
                    message = f"{mNum}\n{name}\n{jpprice}y | {kPrice}r | {maePrice}r [CQ:image,file={firstphoto}]https://www.maetown.cn/wap/#/pages/base/gDetail/gDetail?gId={mNum}"
                    messages+=message
                    if data != UnsandData[-1]:  # 检查当前数据是否不是最后一条数据
                        messages += '\n—————————\n'
                if request.target_type == "private":
                    for id in request.target_id:
                        await bot.send_private_msg(user_id=id, message=messages)
                elif request.target_type == "group":
                    for id in request.target_id:
                        await bot.send_group_msg(group_id=id, message=messages)
