from nonebot import on_command, CommandSession
from pathlib import Path
import nonebot
import os
import re
import time

from plugins.Modules.GetMerItem import GetMerItem
from plugins.Modules.CreateForwardMsg import ForwardMsg
from plugins.Modules.BaiduTranslate import BaiduTranslate


__plugin_name__ = "读取单一商品信息"


# 基本信息
@on_command("m", aliases=("煤炉", "mer", "煤", "好价"), only_to_me=False)
async def MerGood(session: CommandSession):
    # 处理消息
    try:
        message = session.current_arg_text.strip()
        mNum = GetMerNum(message)
        if mNum:
            MerItem = await GetMerItem(mNum=mNum)
            if MerItem.response_code == 0:
                text = f"{MerItem.product_id}\n{MerItem.product_name}\n"
                if MerItem.postage_payment == 1:
                    text += f"【此商品为到付件！】\n"
                k_price = int(MerItem.product_price) * 0.052
                text += f"{MerItem.product_price:.0f}y  人工{k_price:.2f}r  机切{MerItem.product_price_cny}r\n"
                text += f"状态：{'在售' if MerItem.product_status == 1 else '已售出'}"
                message = message.split()
                if len(message) == 2:
                    _, point = message
                    point_price = k_price / int(point)
                    text = text + f"\n共{point}点，{point_price:.2f}r/"
                elif len(message) == 3:
                    _, point, where = message
                    if where == "1" or where == "2":
                        if where == "1":
                            point_price = k_price / int(point)
                        elif where == "2":
                            point_price = MerItem.product_price_cny / int(point)
                        text = text + f"\n共{point}点，{point_price:.2f}r/"
                for index in range(len(MerItem.imagelist)):
                    if index + 1 > 3:
                        text += (
                            f"共{len(MerItem.imagelist)+1}图，为避免刷屏，请使用.mm获取"
                        )
                        break
                    photo_url = f"https://image03.doorzo.net/item/detail/orig/photos/{mNum}_{index+1}.jpg"
                    photo_cq = f"[CQ:image,file={photo_url}]"
                    text = text + photo_cq
            elif MerItem.response_code == 1:
                text = MerItem.response_data
        else:
            text = "m码格式错误"
    except Exception as e:
        text = f"出现错误\n{str(e)}"
    # 回复消息
    message = f"[CQ:reply,id={session.event.message_id}]" + text
    bot = session.bot
    params = session.event.copy()
    del params["message"]
    if session.event.message_type == "private":
        await bot.send_msg(**params, message=message)
    elif session.event.message_type == "group":
        await bot.send_group_msg(**params, message=message)
        if MerItem.response_code == 0:
            if MerItem.product_status == 1:
                file_uri = Path(os.path.abspath("./Temp/mnr_getGood.jpg")).as_uri()
            else:
                file_uri = Path(os.path.abspath("./Temp/miku_sold.jpg")).as_uri()
            time.sleep(0.2)
            await bot.send_group_msg(**params, message=f"[CQ:image,file={file_uri}]")


@on_command("mm", only_to_me=False)
async def MerGoodMore(session: CommandSession):
    # 处理消息
    try:
        raw_message = session.event.raw_message
        mNum = GetMerNum(raw_message)
        if mNum:
            forwardMsg = ForwardMsg()
            merItem = await GetMerItem(mNum=mNum)
            if merItem.response_code == 0:
                # m码
                message = f"{merItem.product_id}"
                forwardMsg.AddTextMessage(message)
                # 商品名
                name = merItem.product_name
                name_cn = BaiduTranslate(name).response_data
                message = f"{name}\n"
                message += "--------\n"
                message += f"{name_cn}"
                forwardMsg.AddTextMessage(message)
                # 价格
                k_price = int(merItem.product_price) * 0.052
                message = f"{merItem.product_price:.0f}y\n人工{k_price:.2f}r\n机切{merItem.product_price_cny}r"
                forwardMsg.AddTextMessage(message)
                # 简介
                text = merItem.product_description
                message = text
                message += "\n--------\n"
                text_cn = BaiduTranslate(text).response_data
                message += text_cn
                forwardMsg.AddTextMessage(message)
                # 图片
                for index in range(len(merItem.imagelist)):
                    photo_url = f"https://image03.doorzo.net/item/detail/orig/photos/{mNum}_{index+1}.jpg"
                    forwardMsg.AddSignalImageMessage(photo_url)
                # 留言
                if len(merItem.comment_list) > 0:
                    for comment in merItem.comment_list:
                        message = ""
                        seller, text, time = comment
                        text_cn = BaiduTranslate(text).response_data
                        message += (
                            f"{seller}：\n{text}\n--------\n{text_cn}\n--------\n{time}"
                        )
                        forwardMsg.AddTextMessage(message)
                # 免责声明
                forwardMsg.AddTextMessage("中文翻译由百度翻译提供，仅供参考")
            elif merItem.response_code == 1:
                text = merItem.response_data
        else:
            text = "m码格式错误"
    except Exception as e:
        text = f"出现错误\n{str(e)}"

    bot = nonebot.get_bot()
    if session.event.message_type == "private":
        await bot.send_private_forward_msg(
            user_id=session.event.user_id, message=forwardMsg.msg
        )
    elif session.event.message_type == "group":
        await bot.send_group_forward_msg(
            group_id=session.event.group_id, message=forwardMsg.msg
        )


# 从文本中提取m码
def GetMerNum(rawText: str) -> str:
    match = re.search(r"(?<!\d)\d{11}(?!\d)", rawText)
    if match:
        return f"m{match.group()}"
    else:
        return None
