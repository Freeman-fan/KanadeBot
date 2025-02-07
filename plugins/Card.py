from nonebot import on_command, CommandSession, on_startup
import nonebot

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
    if input == "":
        input = "knd"
    chara_id = GetPjskCard.charaName2charaID(input)
    if chara_id:
        response = GetPjskCard.get_membercollect(chara_id)
        if response.response_code == 0:
            message = f"[CQ:reply,id={session.event.message_id}]"
            message += f"[CQ:image,file=file:///{response.response_data}]"
            await session.send(message)
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]查询失败：{response.response_data}"
            )
    else:
        await session.send(f"[CQ:reply,id={session.event.message_id}]未找到角色")


# 删除略缩图缓存
@on_command("delcardcache", only_to_me=False)
async def delcardcache(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        chara_id = GetPjskCard.charaName2charaID(input)
        if chara_id:
            response = GetPjskCard.delete_card_cache(chara_id)
            if response.response_code == 0:
                await session.send(
                    f"[CQ:reply,id={session.event.message_id}]删除缓存成功。"
                )
                bot = nonebot.get_bot()
                await bot.send_private_msg(
                    user_id=501079827,
                    message=f"{session.event.user_id}清除了{input}的卡面缓存",
                )
            else:
                await session.send(
                    f"[CQ:reply,id={session.event.message_id}]删除缓存失败：{response.response_data}"
                )
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]未找到角色：{input}"
            )
    else:
        await session.send(f"[CQ:reply,id={session.event.message_id}]请输入角色名")


# 删除所有略缩图缓存(仅限超级用户)
@on_command(
    "delallcardcache", only_to_me=False, permission=lambda sender: sender.is_superuser
)
async def delallcardcache(session: CommandSession):
    response = GetPjskCard.delete_all_card_cache()
    if response.response_code == 0:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]删除所有缓存成功。"
        )
    else:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]删除所有缓存失败：{response.response_data}"
        )


# 新增角色别名
@on_command("addcharann", aliases=("昵称"), only_to_me=False)
async def addcharann(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        input = input.split(maxsplit=2)
        if len(input) != 2:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：角色名 角色别名"
            )
            return
        response = GetPjskCard.add_charann(*input)
        if response.response_code == 0:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]新增角色别名成功。"
            )
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]新增角色别名失败：{response.response_data}"
            )
    else:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]请输入角色名和角色别名"
        )


# 查看角色别名
@on_command("listcharann", aliases=("查看昵称"), only_to_me=False)
async def listcharann(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        response = GetPjskCard.get_charann(input)
        if response.response_code == 0:
            charann_str = "\n".join(response.response_data)
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]角色{input}的别名：\n{charann_str}"
            )
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]查询失败：{response.response_data}"
            )
    else:
        await session.send(f"[CQ:reply,id={session.event.message_id}]请输入角色名")


# 删除角色别名
@on_command("delcharann", aliases=("删除昵称"), only_to_me=False)
async def delcharann(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        response = GetPjskCard.delete_charann(input)
        if response.response_code == 0:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]删除角色别名成功。"
            )
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]删除角色别名失败：{response.response_data}"
            )
    else:
        await session.send(f"[CQ:reply,id={session.event.message_id}]请输入角色名")


# id查大图
@on_command("card", only_to_me=False)
async def card(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        try:
            card_id = int(input)
        except ValueError:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]请输入正确的卡号"
            )
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
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]查询失败：{response.response_data}"
            )
    else:
        await session.send(f"[CQ:reply,id={session.event.message_id}]请输入卡号")


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
                    await session.send(
                        f"[CQ:reply,id={session.event.message_id}]查询失败：{response.response_data}"
                    )
            else:
                await session.send(
                    f"[CQ:reply,id={session.event.message_id}]未找到卡片：{card_name}"
                )
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]未找到角色：{charaName}"
            )
    else:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]请输入角色名和卡片名"
        )


# "卡"通配
@on_command("卡", only_to_me=False)
async def card_any(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        try:
            input_list = input.split()
            if len(input_list) == 1:
                # 检查是否为纯数字
                if input_list[0].isdigit():
                    await card(session)
                    return
            elif len(input_list) == 2:
                await cardnn(session)
                return
            else:
                await session.send(
                    "[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：角色名 卡面名 或 卡号"
                )
                return
        except:
            await session.send(
                "[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：角色名 卡面名 或 卡号"
            )
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
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：角色名 卡面id 卡面别名"
            )
            return
        chara_id = GetPjskCard.charaName2charaID(input[0])
        if not chara_id:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]未找到角色：{input[0]}"
            )
            return
        input[0] = chara_id
        response = GetPjskCard.add_card_name(*input)
        if response.response_code == 0:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]新增卡面别名成功。"
            )
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]新增卡面别名失败：{response.response_data}"
            )
    else:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]请输入角色名、卡面别名和卡面id"
        )


# 查看卡面别名
@on_command("listcardnn", only_to_me=False)
async def listcardnn(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        response = GetPjskCard.get_card_name(input)
        if response.response_code == 0:
            cardnn_str = "\n".join(response.response_data)
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]卡面id{input}的别名：\n{cardnn_str}"
            )
        else:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]查询失败：{response.response_data}"
            )
    else:
        await session.send(f"[CQ:reply,id={session.event.message_id}]请输入卡面id")


# 删除卡面别名
@on_command("delcardnn", only_to_me=False)
async def delcardnn(session: CommandSession):
    input = session.current_arg_text.strip()
    if input:
        try:
            input_list = input.split(maxsplit=2)
            if len(input_list) != 2:
                await session.send(
                    f"[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：卡面id 需要删除的别名"
                )
                return
            response = GetPjskCard.delete_card_name(*input_list)
            if response.response_code == 0:
                await session.send(
                    f"[CQ:reply,id={session.event.message_id}]删除卡面别名成功。"
                )
            else:
                await session.send(
                    f"[CQ:reply,id={session.event.message_id}]删除卡面别名失败：{response.response_data}"
                )
        except:
            await session.send(
                f"[CQ:reply,id={session.event.message_id}]输入格式错误，请按照格式输入：卡面id 需要删除的别名"
            )
    else:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]请输入卡面id和需要删除的别名"
        )


# 更新卡面数据
@on_command("cardupdate", only_to_me=False)
async def cardupdate(session: CommandSession):
    response = GetPjskCard.update_data()
    if response.response_code == 0:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]卡面数据更新成功：\n{response.response_data}"
        )
    else:
        await session.send(
            f"[CQ:reply,id={session.event.message_id}]卡面数据更新失败：\n{response.response_data}"
        )
