from nonebot import on_command, CommandSession
from pathlib import Path
import os
import re
import time
from plugins.MaeModule.GetMerItem import GetMerItem


__plugin_name__ = '读取单一商品信息'


@on_command('m', aliases=('煤炉', 'mer', '煤', '好价'), only_to_me=False)
async def MerGood(session: CommandSession):
    #处理消息
    try:
        raw_message = session.event.raw_message
        match = re.search(r'(?<!\d)\d{11}(?!\d)', raw_message)
        if match:
            goodID, name, _, price, mae_price, status, imagelist = await GetMerItem(mNum=f'm{match.group()}')
            k_price = int(price) *0.052
            text = f"{goodID}\n{name}\n{price:.0f}y  人工{k_price:.2f}r  机切{mae_price}r\n状态：{'在售' if status == 'on_sale' else '已售出'}"
            message = raw_message.split()
            if len(message) == 3:
                _, _, point = message
                point_price = k_price / int(point)
                text = text + f'\n共{point}点，{point_price:.2f}r/'
            elif len(message) == 4:
                _, _, point, where = message
                if where == '1':
                    point_price = k_price / int(point)
                elif where == '2':
                    point_price = mae_price / int(point)
                text = text + f'\n共{point}点，{point_price:.2f}r/'
            for photo_url in imagelist:
                photo_cq = f"[CQ:image,file={photo_url}]"
                text = text+photo_cq
        else:
            text = '请输入正确的m码'
    except Exception as e:
        text = f'出现错误\n{str(e)}'
    #回复消息
    message = f'[CQ:reply,id={session.event.message_id}]' + text
    bot = session.bot
    params = session.event.copy()
    del params['message']
    if session.event.message_type == 'private':
        await bot.send_msg(**params, message= message)
    elif session.event.message_type == 'group':
        await bot.send_group_msg(**params, message=message)
        if status == 'on_sale':
            file_uri = Path(os.path.abspath("./images/mnr_getGood.jpg")).as_uri()
        else:
            file_uri = Path(os.path.abspath("./images/miku_sold.jpg")).as_uri()
        time.sleep(0.2)
        await bot.send_group_msg(**params, message= f"[CQ:image,file={file_uri}]")
