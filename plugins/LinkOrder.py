import json

from nonebot import on_command, CommandSession, on_startup

from plugins.CustomClass.response import FuncResponse

__plugin_name__ = "获取链接"

aliases_list = []


class LinkResponse(FuncResponse):
    def __init__(
        self,
        response_code: int,
        response_num: int,
        response_order: str,
        reponse_reply: str,
        response_message_type: str,
    ):
        super().__init__(response_code, None)
        self.response_code = response_code
        self.response_num = response_num
        self.response_order = response_order
        self.response_reply = reponse_reply
        self.response_message_type = response_message_type



@on_command("l", patterns="l\d+", only_to_me=False)
async def LinkOrder(session: CommandSession):
    # 处理消息
    raw_message = session.event.raw_message
    _, order = raw_message.split("l")
    order = order.strip()
    if order.isdigit():
        try:
            num = int(order.strip())
            response = Link(num=num)
        except Exception as e:
            print("1" * 100)
    else:
        response = Link(order=order)
    if response.response_code == 0:
        if response.response_message_type == None:
            message = f"{response.response_order}:\n{response.response_reply}"
        elif response.response_message_type == "json":
            if response.response_order == '拼谷助手':
                with open(r'./plugins/Config/miniProgram', 'r', encoding = 'utf-8') as file:
                    data = file.read()
                message = f'''[CQ:json,data={data}]'''
    elif response.response_code == 1:
        message = response.response_data

    # 回复消息
    bot = session.bot
    params = session.event.copy()
    del params["message"]
    if session.event.message_type == "private":
        await bot.send_msg(**params, message=message)
    elif session.event.message_type == "group":
        await bot.send_group_msg(**params, message=message)


def Link(num: int = None, order: str = None) -> LinkResponse:
    # 打开配置文件
    with open("./plugins/Config/Link.json", "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)
        

    # 无传入值
    if num == None and order == None:
        text = "请正确输入链接序号或链接关键字，支持以下链接\n"
        for item in data:
            num = item.get("num")
            order = item.get("order")[0]
            text += f"{num}：{order}\n"
        return FuncResponse(1, text)

    # 有传入值
    if num:
        for item in data:
            if num == item.get("num"):
                return LinkResponse(
                    response_code=0,
                    response_num=item.get("num"),
                    response_order=item.get("order")[0],
                    reponse_reply=item.get("reply"),
                    response_message_type=item.get("message_type"),
                )
    elif order:
        for item in data:
            if order == item.get("order"):
                return LinkResponse(
                    response_code=0,
                    response_num=item.get("num"),
                    response_order=item.get("order")[0],
                    reponse_reply=item.get("reply"),
                    response_message_type=item.get("message_type"),
                )
    else:
        text = "请正确输入链接序号或链接关键字，支持以下链接\n"
        for item in data:
            num = item.get("num")
            order = item.get("order")[0]
            text += f"{num}：{order}\n"
        return FuncResponse(1, text)
