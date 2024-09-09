from nonebot import on_command, CommandSession


__plugin_name__ = '获取链接'


@on_command('l', aliases=('l1','l2','l3'),only_to_me=False)
async def LinkOrder(session: CommandSession):
    #处理消息
    raw_message = session.event.raw_message
    _, num = raw_message.split('l')
    num=num.strip()
    if num == '1':
        text = '切煤收集表:\n'+r'https://flowus.cn/form/8706a1cd-6480-497f-8eb3-2dd5ffcdb036'
    elif num=='2':
        text = '切煤记录表:\n' + r'https://flowus.cn/share/c4d1ab4e-08fe-43b0-8dc8-459595702111'
    elif num == '3':
        data = '{"app":"com.tencent.miniapp_01"&#44;"desc":""&#44;"view":"view_95A06A1683C80BECC99BE5CC7B6D706B"&#44;"bizsrc":""&#44;"ver":"1.0.0.69"&#44;"prompt":"&#91;QQ小程序&#93;拼谷助手"&#44;"appID":""&#44;"sourceName":""&#44;"actionData":""&#44;"actionData_A":""&#44;"sourceUrl":""&#44;"meta":{"invitation_1":{"appid":"1112117769"&#44;"appType":0&#44;"title":"泛进中举邀请你加入拼团【一些单领】"&#44;"name":"拼谷助手"&#44;"icon":"https:\\/\\/miniapp.gtimg.cn\\/public\\/appicon\\/68fd865843dbfc3ce6ff374f7d76c42b_200.jpg"&#44;"path":"m.q.qq.com\\/a\\/s\\/80a912e1a100c94108e1979d7ff70a42"&#44;"imageUrl":"https:\\/\\/7072-pro-2gis2vsrb5a3b312-1311684432.tcb.qcloud.la\\/group-avatar-compressed\\/17092926259853WkZ4?imageMogr2\\/crop\\/454x256\\/gravity\\/center\\/ignore-error\\/1"&#44;"scene":1036&#44;"host":{"uin":501079827&#44;"nick":"泛进中举"}&#44;"shareTemplateId":"95A06A1683C80BECC99BE5CC7B6D706B"&#44;"shareTemplateData":{"bottomBtnTxt":"我要加入"}}}&#44;"config":{"type":"normal"&#44;"width":0&#44;"height":0&#44;"forward":0&#44;"autoSize":0&#44;"ctime":1725858024&#44;"token":"b152bba2e563f221635f8d1752f0b54a"}&#44;"text":""&#44;"extraApps":&#91;&#93;&#44;"sourceAd":""&#44;"extra":""}'
        text = f'''[CQ:json,data={data}]'''

    message = f'[CQ:reply,id={session.event.message_id}]{text}'
    #回复消息
    bot = session.bot
    params = session.event.copy()
    del params['message']
    if session.event.message_type == 'private':
        await bot.send_msg(**params, message= message)
    elif session.event.message_type == 'group':
        await bot.send_group_msg(**params, message=message)