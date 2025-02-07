from nonebot import on_command, CommandSession, on_startup

import plugins.Modules.GetPjskCard as GetPjskCard

__plugin_name__ = "查卡器"


# 初始化
@on_startup
async def card_init():
    GetPjskCard.init_data()


# 略缩图
@on_command("findcard", aliases=("查卡"), only_to_me=False)
async def findcard(session: CommandSession):
    input = session.current_arg_text.strip()
    if input is '':
        input = 'knd'
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

#新增角色别名
@on_command("addcharann",aliases=("昵称"), only_to_me=False)
async def addcharann(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        input = input.split(maxsplit=2)
        if len(input) != 2:
            await session.send("输入格式错误，请按照格式输入：角色名 角色别名")
            return
        response = GetPjskCard.add_charann(*input)
        if response.response_code == 0:
            await session.send(f"新增角色别名成功。")
        else:
            await session.send(f"新增角色别名失败：{response.response_data}")
    else:
        await session.send("请输入角色名和角色别名")


# id查大图
@on_command("card", only_to_me=False)
async def card(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        try:
            card_id = int(input)
        except ValueError:
            await session.send("请输入正确的卡号")
            return
        # 查卡
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


# 卡面别名查大图
@on_command("cardnn", only_to_me=False)
async def cardnn(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        charaName, card_name = input.split(maxsplit=2)
        Chara_id = GetPjskCard.charaName2charaID(charaName)
        if Chara_id:
            card_id = GetPjskCard.cardName2cardID(Chara_id, card_name)
            if card_id.response_code == 0:
                response = GetPjskCard.get_card_fullsize(int(card_id.response_data))
                if response.response_code == 0:
                    message = f"[CQ:reply,id={session.event.message_id}]"
                    message += f"卡面id：{card_id.response_data}"
                    if type(response.response_data) == list:
                        for file in response.response_data:
                            message += f"[CQ:image,file=file:///{file}]"
                    else:
                        message += f"[CQ:image,file=file:///{response.response_data}]"
                    await session.send(message)
                else:
                    await session.send(f"查询失败：{response.response_data}")
            else:
                await session.send(f"未找到卡片：{card_name}")
        else:
            await session.send(f"未找到角色：{charaName}")
    else:
        await session.send("请输入角色名和卡片名")

# "卡"通配
@on_command("卡", only_to_me=False)
async def card_any(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        try:
            input_list = input.split()
            if len(input_list) == 1:
                #检查是否为纯数字
                if input_list[0].isdigit():
                    await card(session)
                    return
            elif len(input_list) == 2:
                await cardnn(session)
                return
            else:
                await session.send("[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：角色名 卡面名 或 卡号")
                return
        except:
            await session.send("[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：角色名 卡面名 或 卡号")
            return
    else:
        return


# 新增卡面别名
@on_command("addcardnn", only_to_me=False)
async def addcardnn(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        input = input.split(maxsplit=3)
        if len(input) != 3:
            await session.send("输入格式错误，请按照格式输入：角色名 卡面别名 卡面id")
            return
        chara_id = GetPjskCard.charaName2charaID(input[0])
        if not chara_id:
            await session.send(f"未找到角色：{input[0]}")
            return
        input[0] = chara_id
        response = GetPjskCard.add_card_name(*input)
        if response.response_code == 0:
            await session.send(f"新增卡面别名成功。")
        else:
            await session.send(f"新增卡面别名失败：{response.response_data}")
    else:
        await session.send("请输入角色名、卡面别名和卡面id")

# 更新卡面数据
@on_command("cardupdate", only_to_me=False)
async def cardupdate(session: CommandSession):
    response = GetPjskCard.update_data()
    if response.response_code == 0:
        await session.send(f"卡面数据更新成功：\n{response.response_data}")
    else:
        await session.send(f"卡面数据更新失败：\n{response.response_data}")
