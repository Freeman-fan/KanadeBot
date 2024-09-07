from nonebot import on_notice, NoticeSession
import time


__plugin_name__ = '入群欢迎'


@on_notice('group_increase')
async def Welcome(session: NoticeSession):
    await session.send('欢迎新谷东！本群常开切煤、日相卡业务，也有日韩通贩，详情看公告。有需要切煤可以直接把链接甩憂一乘或泛进中举~')
    time.sleep(0.1)
    await session.send('新谷东记得改cn+自推——\n不改也行，不改的话拼煤看见你推就不会艾特你')
    data = '{"app":"com.tencent.miniapp_01"&#44;"desc":""&#44;"view":"view_95A06A1683C80BECC99BE5CC7B6D706B"&#44;"bizsrc":""&#44;"ver":"1.0.0.69"&#44;"prompt":"&#91;QQ小程序&#93;拼谷助手"&#44;"appID":""&#44;"sourceName":""&#44;"actionData":""&#44;"actionData_A":""&#44;"sourceUrl":""&#44;"meta":{"invitation_1":{"appid":"1112117769"&#44;"appType":0&#44;"title":"憂一乘邀请你加入拼团【一些单领】"&#44;"name":"拼谷助手"&#44;"icon":"https:\\/\\/miniapp.gtimg.cn\\/public\\/appicon\\/68fd865843dbfc3ce6ff374f7d76c42b_200.jpg"&#44;"path":"m.q.qq.com\\/a\\/s\\/3487649fee0d0a3d153d1c914542a2cf"&#44;"imageUrl":"https:\\/\\/7072-pro-2gis2vsrb5a3b312-1311684432.tcb.qcloud.la\\/group-avatar-compressed\\/17092926259853WkZ4?imageMogr2\\/crop\\/454x256\\/gravity\\/center\\/ignore-error\\/1"&#44;"scene":1036&#44;"host":{"uin":1746267850&#44;"nick":"宵崎家恶犬"}&#44;"shareTemplateId":"95A06A1683C80BECC99BE5CC7B6D706B"&#44;"shareTemplateData":{"bottomBtnTxt":"我要加入"}}}&#44;"config":{"type":"normal"&#44;"width":0&#44;"height":0&#44;"forward":0&#44;"autoSize":0&#44;"ctime":1725554173&#44;"token":"92134fe46de73a628e5728c8a92ba236"}&#44;"text":""&#44;"extraApps":&#91;&#93;&#44;"sourceAd":""&#44;"extra":""}'
    message = f'''[CQ:json,data={data}]'''
    time.sleep(0.1)
    await session.send(message=message)
