from nonebot import on_notice, CommandSession
from pathlib import Path
import os


__plugin_name__ = '消息提示'


@on_notice('notify')
async def Poke(session: CommandSession):
    print(session.event)
    #戳一戳
    if session.event.sub_type == 'poke' and session.event.target_id == session.event.self_id:
        #回复消息
        file_uri = Path(os.path.abspath("./images/knd_question.jpg")).as_uri()
        await session.send(f"[CQ:image,file={file_uri}]")

