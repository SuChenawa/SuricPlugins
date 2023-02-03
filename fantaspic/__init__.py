#
# !目前是获取静态网页图片，等学点新东西在考虑通过爬虫
import json
import os
import random
from datetime import datetime
from pathlib import Path
import requests
import asyncio
import aiohttp
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
from graia.ariadne.event.lifecycle import ApplicationLaunched
from library.decorator.blacklist import Blacklist
from library.decorator.distribute import Distribution
from library.decorator.function_call import FunctionCall
from library.decorator.switch import Switch
from library.util.dispatcher import PrefixMatch
from library.util.message import send_message

channel = Channel.current()
DATA_PATH = it(Modules).get(channel.module).data_path
url = "https://blog.suchenawa.com/SuricPlugins/fantaspics.json"
filepath = Path(DATA_PATH / "fantaspics.json")


# ################################################################
# *启动更新
@listen(ApplicationLaunched)
async def OnApplicationLaunched_Update():
    logger.info("[Fantaspic] 正在运行启动后文件更新服务")
    await file_update_service()


# ################################################################
# *文件热更新
# @channel.use(SchedulerSchema(timers.every_custom_seconds(20)))
@channel.use(SchedulerSchema(timers.every_hours()))
async def fantaspic_file_sync(app: Ariadne):
    await file_update_service()


# 这里想写定时发送，但是得等我看文档看到这里再说
# @channel.use(SchedulerSchema(timers.crontabify("0 8-24/3 * * *")))
# @channel.use(SchedulerSchema(timers.crontabify("8-24/5 * * * *")))
# async def autosend_service():
#     await send_message()


@listen(GroupMessage, FriendMessage)
@dispatch(Twilight(PrefixMatch(), UnionMatch("fan", "无聊图", "来点图")))
@decorate(
    Switch.check(channel.module),
    Distribution.distribute(),
    Blacklist.check(),
    FunctionCall.record(channel.module),
)
async def fantaspic(app: Ariadne, event: MessageEvent, supplicant: Member | Friend):
    fantaspicurl = Path(DATA_PATH / "fantaspics.json")
    with fantaspicurl.open("r", encoding="UTF-8") as f:
        _data = json.loads(f.read())
        image_Num = _data["picNum"]
    picselect = random.randint(1, image_Num)
    session = Ariadne.service.client_session
    async with session.get(
        f"https://blog.suchenawa.com/SuricPlugins/fantaspic/{picselect}.jpg"
    ) as r:
        data = await r.read()
    await send_message(event, MessageChain(Image(data_bytes=data)), app.account)
    logger.debug(
        f"[Fantaspic] 正在发送Url:('https://blog.suchenawa.com/SuricPlugins/fantaspic/{picselect}.jpg')"
    )


@listen(GroupMessage, FriendMessage)
@dispatch(
    Twilight(
        PrefixMatch(),
        UnionMatch(
            "fupdate",
        ),
    )
)
@decorate(
    Switch.check(channel.module),
    Distribution.distribute(),
    Blacklist.check(),
    FunctionCall.record(channel.module),
)
async def manual_pdate(app: Ariadne, event: MessageEvent, supplicant: Member | Friend):
    logger.info("[Fantaspic] 正在进行配置文件手动更新")
    await file_update_service()
    await send_message(event, MessageChain("[Fantaspic] 配置文件更新完成"), app.account)


async def file_update_service():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            with open(filepath, "wb") as file:
                file.write(data)
                if os.path.exists(filepath):
                    logger.success("[Fantaspic] 资源文件更新成功！")
                else:
                    logger.error("[Fantaspic] 资源文件更新失败！")
