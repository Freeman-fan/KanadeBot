from nonebot import on_command, CommandSession
from plugins.Modules.GetMaeRate import GetMaeRate


__plugin_name__ = '获取机切汇率'


@on_command('汇率', aliases=('查汇率','r','rate'), only_to_me= False)
async def MaeRate(session: CommandSession):
    rate = await GetMaeRate()
    message = f'当前机切汇率为{rate}'
    bot = session.bot
    params = session.event.copy()
    del params['message']
    if session.event.message_type == 'private':
        await bot.send_msg(**params, message= message)
    elif session.event.message_type == 'group':
        await bot.send_group_msg(**params, message=message)