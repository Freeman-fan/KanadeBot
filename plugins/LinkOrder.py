from nonebot import on_command, CommandSession


__plugin_name__ = '获取链接'


@on_command('l', aliases=('l1','l2'),only_to_me=False)
async def LinkOrder(session: CommandSession):
    #处理消息
    raw_message = session.event.raw_message
    _, num = raw_message.split('l')
    num=num.strip()
    if num == '1':
        text = '切煤收集表:\n'+r'https://flowus.cn/form/8706a1cd-6480-497f-8eb3-2dd5ffcdb036'
    elif num=='2':
        text = '切煤记录表:\n' + r'https://flowus.cn/share/c4d1ab4e-08fe-43b0-8dc8-459595702111'
    message = f'[CQ:reply,id={session.event.message_id}]{text}'
    #回复消息
    bot = session.bot
    params = session.event.copy()
    del params['message']
    if session.event.message_type == 'private':
        await bot.send_msg(**params, message= message)
    elif session.event.message_type == 'group':
        await bot.send_group_msg(**params, message=message)