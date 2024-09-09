from aiocqhttp import Event
import nonebot
import json
import random


__plugin_name__ = '聊天'



bot = nonebot.get_bot()


@bot.on_message
async def _(event: Event):
    raw_message = event.raw_message
    if f'[CQ:at,qq={event.self_id}]' not in raw_message:
        return
    
    chat_reply = Chat(raw_message=raw_message)
    message = chat_reply
    if chat_reply == None and raw_message.strip() == f'[CQ:at,qq={event.self_id}]':
        message = '我在。'
    await bot.send(event=event, message=message)


def Chat(raw_message: str):
    with open('./plugins/Config/Chat.json', 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)

    for item in data:
        order = item.get('order')
        for text in order:
            if text in raw_message:
                reply = item.get('reply')
                message = random.choice(reply)

                return message