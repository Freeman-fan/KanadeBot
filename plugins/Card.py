from nonebot import on_command, CommandSession, on_startup

import plugins.Modules.GetPjskCard as GetPjskCard

__plugin_name__ = "查卡器"


# 初始化
@on_startup
async def card_init():
    GetPjskCard.init_data()


# 略缩图
@on_command("findcard", only_to_me=False)
async def findcard(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        chara_id = GetPjskCard.charaName2charaID(input)
        if chara_id:
            response = GetPjskCard.get_membercollect(chara_id)
            if response.response_code == 0:
                message = f"[CQ:reply,id={session.event.message_id}]"
                message += f"[CQ:image,file=file:///{response.response_data}]"
                await session.send(message)
            else:
                await session.send(f"查询失败：{response.response_data}")
        else:
            await session.send(f"未找到角色")
    else:
        await session.send("请输入角色名")


#大图
@on_command("card", only_to_me=False)
async def card(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        try:
            card_id = int(input)
        except ValueError:
            await session.send("请输入正确的卡号")
            return
        
        response = GetPjskCard.get_card_fullsize(card_id)
        if response.response_code == 0:
            message = f"[CQ:reply,id={session.event.message_id}]"
            if type(response.response_data) == list:
                for file in response.response_data:
                    message += f"[CQ:image,file=file:///{file}]"
            else:
                message += f"[CQ:image,file=file:///{response.response_data}]"
            await session.send(message)
        else:
            await session.send(f"查询失败：{response.response_data}")
    else:
        await session.send("请输入卡号")


#更新卡面数据
@on_command("cardupdate", only_to_me=False)
async def cardupdate(session: CommandSession):
    response = GetPjskCard.update_data()
    if response.response_code == 0:
        await session.send(f"卡面数据更新成功：\n{response.response_data}")
    else:
        await session.send(f"卡面数据更新失败：\n{response.response_data}")