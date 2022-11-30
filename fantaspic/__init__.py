# 
# !目前是获取静态网页图片，等学点新东西在考虑通过爬虫
import json
import os
import random
from datetime import datetime
from pathlib import Path
import requests
from creart import it
from library.util.module import Modules
from graia.ariadne import Ariadne
from graia.ariadne.event.message import (
    Friend,
    Member,
    GroupMessage,
    FriendMessage,
    MessageEvent,
)
from loguru import logger
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.message.parser.twilight import Twilight, UnionMatch
from graia.ariadne.util.saya import listen, dispatch, decorate
from graia.saya import Channel
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from library.decorator.blacklist import Blacklist
from library.decorator.distribute import Distribution
from library.decorator.function_call import FunctionCall
from library.decorator.switch import Switch
from library.util.dispatcher import PrefixMatch
from library.util.message import send_message

channel = Channel.current()
DATA_PATH = it(Modules).get(channel.module).data_path
url = 'https://blog.suchenawa.com/SuricPlugins/fantaspic.json'
# @channel.use(SchedulerSchema(timers.every_custom_seconds(5))) 
@channel.use(SchedulerSchema(timers.every_hours())) 
async def fantaspic_file_sync(app: Ariadne):
    
    filepath = Path(DATA_PATH / "husbands.json")
    open(filepath,'w')
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        logger.success("[Fantaspic] 文件'fantaspics.Json'不存在，即将自动下载")
       
    hfile = requests.get(url)
    open(filepath,'wb').write(hfile.content)
    logger.success("[Fantaspic] 资源文件更新完毕！")

# husbandurl = Path(DATA_PATH / "fantaspics.json")
# with husbandurl.open("r", encoding="UTF-8") as f:
#     _data = json.loads(f.read())
#     image_Num = _data["picNum"]

@listen(GroupMessage, FriendMessage)
@dispatch(Twilight(PrefixMatch(), UnionMatch("fan", "无聊图", "来点图")))
@decorate(
    Switch.check(channel.module),
    Distribution.distribute(),
    Blacklist.check(),
    FunctionCall.record(channel.module),
)
async def fantaspic(app: Ariadne, event: MessageEvent,supplicant: Member | Friend ):

    picselect = random.randint(1,image_Num)
    async with Ariadne.service.client_session as session:
        async with session.get(f"https://blog.suchenawa.com/SuricPlugins/fantaspic/{image_Num}.jpg") as r:
            img = await r.read()
    await send_message(event, MessageChain(Image(data_bytes=img)), app.account)



