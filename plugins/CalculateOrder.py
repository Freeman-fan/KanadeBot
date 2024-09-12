from nonebot import on_command, CommandSession
from plugins.MaeModule.GetMaeRate import GetMaeRate


__plugin_name__ = '计算价格'


@on_command('y', aliases=('Y'), only_to_me=False)
async def CalculateOrder(session: CommandSession):
    message = session.current_arg_text
    message = message.lstrip('y')
    message = message.split()
    if len(message) ==0:
        message = (await session.aget(prompt=f'[CQ:reply,id={session.event.message_id}]参数错误！请输入需要计算的金额')).strip()
        message = message.split()
        while len(message)==0:
            message = (await session.aget(prompt=f'[CQ:reply,id={session.event.message_id}]参数错误！请输入需要计算的金额')).strip()


    if len(message) == 1:
        jp = message[0]
        point = 1
    elif len(message) == 2:
        jp, point = message
        where = '1'
    elif len(message) == 3:
        jp, point, where = message
    try:
        jp = int(jp)
        point = int(point)
        rate = await GetMaeRate()
        #计算
        price1 = jp * 0.053
        price2 = (jp + 50) * rate
        text = f'''参考汇率：{rate}\n人工: {price1:.2f}r\n机切: {price2:.2f}r'''
        if point != 1:
            if where == '1':
                point_price = price1 / point
            elif where == '2':
                point_price = price2 / point
            text = text + f'\n共{point}点，{point_price:.2f}r/'
                
    except Exception as e:
        text = '出现未知错误，请检查输入或联系开发者\n'+str(e)
    #发送消息
    bot = session.bot
    text = f'[CQ:reply,id={session.event.message_id}]' + text
    params = session.event.copy()
    del params['message']
    if session.event.message_type == 'private':
        await bot.send_msg(**params, message= text)
    elif session.event.message_type == 'group':
        await bot.send_group_msg(**params, message=text)


