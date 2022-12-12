# 急需有人来帮我扩充一下文案！！
# 
# TODO!:将news_settings.json拆分并写入datapath
# TODO?:可能需要优化一下网页结构了，之前几十分钟写出来的貌似有点过于凌乱
# TODO!:想把整个文件写的正经一点，以方便在附近有人的时候进行修改
import json
import os
import random
from datetime import datetime
from pathlib import Path
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
from graiax.playwright import PlaywrightBrowser
from graia.scheduler import GraiaScheduler
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema
from graia.ariadne.event.lifecycle import ApplicationLaunched
from library.decorator.blacklist import Blacklist
from library.decorator.distribute import Distribution
from library.decorator.function_call import FunctionCall
from library.decorator.switch import Switch
from library.util.dispatcher import PrefixMatch
from library.util.message import send_message
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()

assets_path = Path(Path(__file__).parent, "assets")
DATA_PATH = it(Modules).get(channel.module).data_path
url = 'https://blog.suchenawa.com/SuricPlugins/husbands.json'
filepath = Path(DATA_PATH / "husbands.json")

# ################################################################
# *启动更新
@listen(ApplicationLaunched)
async def OnApplicationLaunched_Update():
    logger.info("[Daily_News] 正在运行启动后文件更新服务")
    await file_update_service()

# ################################################################
# *文件热更新
# @channel.use(SchedulerSchema(timers.every_minute())) 
# @channel.use(SchedulerSchema(timers.crontabify("30 7 * * * 30")))
@channel.use(SchedulerSchema(timers.every_hours())) 
async def dailynews_file_sync(app: Ariadne):
    await file_update_service()


# ################################################################
# 读取Json文件
settings_file = Path(assets_path / "news_settings.json")
with settings_file.open("r", encoding="UTF-8") as f:
    _data = json.loads(f.read())
    COLOR_TEMPLATES = _data["news_color"]
    OUTWARD_TEMPLATES = _data["outward"]
    EVALUATE_TEMPLATES_0 = _data["news_evaluate_0"]
    EVALUATE_TEMPLATES_1 = _data["news_evaluate_1"]
    EVALUATE_TEMPLATES_2 = _data["news_evaluate_2"]
    EVALUATE_TEMPLATES_3 = _data["news_evaluate_3"]
    EVALUATE_TEMPLATES_4 = _data["news_evaluate_4"]
    EVALUATE_TEMPLATES_5 = _data["news_evaluate_5"]
    BFPJ_TEMPLATES = _data["bfpj"]
    COMMENT_TEMPLATES_0 = _data["public_comment_0"]
    COMMENT_TEMPLATES_1 = _data["public_comment_1"]
    COMMENT_TEMPLATES_2 = _data["public_comment_2"]
    COMMENT_TEMPLATES_3 = _data["public_comment_3"]
    COMMENT_TEMPLATES_4 = _data["public_comment_4"]
    COMMENT_TEMPLATES_5 = _data["public_comment_5"]
    BFDZDP_TEMPLATES = _data["bfdzdp"]
    Bignews = _data["Abuse_of_power"]
# ################################################################


@listen(GroupMessage, FriendMessage)
@dispatch(Twilight(PrefixMatch(), UnionMatch("今日牛子", "随机牛子", "我几把呢")))
@decorate(
    Switch.check(channel.module),
    Distribution.distribute(),
    Blacklist.check(),
    FunctionCall.record(channel.module),
)
async def daily_news_playwright(app: Ariadne, event: MessageEvent,supplicant: Member | Friend ):
    with filepath.open("r", encoding="UTF-8") as f:
        _data = json.loads(f.read())
        image_Num = _data["picNum"]
    picselect = random.randint(1,image_Num)
    random_seed(event.sender)
    # #######################################################################
    # TODO:PlayWright重构
    # #######################################################################
    # * 需要首先判断牛子是否大于0
    if(supplicant.id == 1306542338):
        news_length = random.randint(18, 30)
    elif(supplicant.id == 2970290021):
        news_length = random.randint(-30, 0)
    else:
        news_length = random.randint(-10, 30)
    
    a = "\n"

    phimosis_status = "未知"
    boki_status = "未知"
    egg_weight = "未知"
    angle = f"未知"

    if news_length > 0:

        # * 确定拥有的生殖器类型
        news_or_cloaca = "牛子"

        # * 确定是否勃起
        if random.randint(0, 1) == 1:
            boki_status = "勃起"
            angle_status = "勃起"
            angle = f"{random.randint(90, 180)}度"
        else:
            boki_status = "软掉"
            angle_status = ""
            angle = f"{random.randint(0, 90)}度"

        # * 判断是否包茎
        rd_phimosis_status = random.randint(0, 2)
        if rd_phimosis_status == 0:
            phimosis_status = "包茎"
        elif rd_phimosis_status == 1:
            phimosis_status = "半包茎"
        else:
            phimosis_status = "非包茎"

        # * 判断蛋蛋重量
        rd_egg_weight = random.randint(50, 500)
        egg_weight = f"{rd_egg_weight}"

        # * 生成牛子的系统评价 # 生成牛子的大众点评
        if news_length > 20:
            dick_length_evaluate = random.choice(EVALUATE_TEMPLATES_0)
            dick_comment = random.choice(COMMENT_TEMPLATES_0)
            news_score = random.randint(60, 100)
        elif 15 < news_length <= 20:
            dick_length_evaluate = random.choice(EVALUATE_TEMPLATES_1)
            dick_comment = random.choice(COMMENT_TEMPLATES_1)
            news_score = random.randint(40, 80)
        elif 6 < news_length <= 15:
            dick_length_evaluate = random.choice(EVALUATE_TEMPLATES_2)
            dick_comment = random.choice(COMMENT_TEMPLATES_2)
            news_score = random.randint(30, 60)
        elif 3 <= news_length <= 6:
            dick_length_evaluate = random.choice(BFPJ_TEMPLATES)
            dick_comment = random.choice(BFDZDP_TEMPLATES)
            news_score = random.randint(20, 30)
        else:
            dick_length_evaluate = random.choice(EVALUATE_TEMPLATES_3)
            dick_comment = random.choice(COMMENT_TEMPLATES_3)
            news_score = random.randint(0, 20)

    elif news_length < 0:
        news_or_cloaca = "泄殖腔"
        # * 生成泄殖腔的系统评价 # 生成泄殖腔的大众点评
        dick_length_evaluate = random.choice(EVALUATE_TEMPLATES_5)
        dick_comment = random.choice(COMMENT_TEMPLATES_5)
        news_score = random.randint(0, 100)

    else:
        news_or_cloaca = "如履平地"
        # * 生成独特的评价
        dick_length_evaluate = random.choice(EVALUATE_TEMPLATES_4)
        dick_comment = random.choice(COMMENT_TEMPLATES_4)
        news_score = 0

    # * 照搬旧版的附魔系统
    if random.randint(0, 4) == 0:
        enchant_lv = ["Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ"]
        enchant_list = [
            "附魔上了消失诅咒",
            "附魔上了经*修补",
            "附魔上了火焰附加",
            "附魔上了耐久",
            "附魔上了荆棘",
            "附魔上了力量",
        ]
        rd_enchant = random.randint(0, 5)
        dick_enchant = enchant_list[rd_enchant]
        dick_comment_score = 0
        if rd_enchant < 2:
            dick_comment_score += rd_enchant * 10
        else:
            if rd_enchant == 2:
                rd_lv = random.randint(0, 1)
                dick_comment_score += (rd_lv + 1) * 5
            elif rd_enchant < 5:
                rd_lv = random.randint(0, 2)
                dick_comment_score += (rd_lv + 1) * 10 / 3.0
            else:
                rd_lv = random.randint(0, 4)
                dick_comment_score += (rd_lv + 1) * 2
            dick_enchant += enchant_lv[rd_lv]
        dick_enchant += "的"
    else:
        dick_enchant = "None"

    # 新功能
    # 牛子颜色
    # * 定义三个数值来生成 RGB
    cr = random.randint(0, 255)
    cg = random.randint(0, 255)
    cb = random.randint(0, 255)
    # # 临时测试
    # cr = 0
    # cg = 0
    # cb = 0
    ## 没用的两个参数
    black = "black"
    white = "white"
    ## 设想是如果r+g+b大于382就将覆盖层文字修改为黑色，否则为白色
    if cr + cg + cb > 382:
        hextextcolor = "rgb(0,0,0)"
    else:
        hextextcolor = "rgb(255,255,255)"
    # * RGB-to-Hex 将RGB转换为Hex值，使其占用长度减少
    hexcolor = ("{:02X}" * 3).format(cr, cg, cb)
    # print(cr, cg, cb)
    # print(hexcolor)
    # print(hextextcolor)
    # #######################################################################
    # 先判断牛子是否大于0
    # >0 为正常牛子
    # <0 为腔
    # #######################################################################

# * 向PlayWright输出的参数内容
    # * 生殖器类型
    news_or_cloaca_out = news_or_cloaca
    # * 长度
    news_length_out = news_length
    # * 系统评价
    system_comment_out = dick_length_evaluate
    # * 颜色底色
    hextextcolor_out = hextextcolor
    # * 颜色
    hexcolor_out = f"#{hexcolor}"
    # * 附魔
    dick_enchant_out = dick_enchant
    # * 是否包茎
    phimosis_status_out = phimosis_status
    # * 是否勃起
    boki_status_out = boki_status
    # * 蛋蛋重量
    egg_weight_out = egg_weight
    # * 大众点评分数
    score_out = news_score / 10
    Image_url_out = picselect
    logger.debug(f"[Daily_News] 正在发送Url:('https://blog.suchenawa.com/SuricPlugins/husband/{Image_url_out}.png')")
    # #######################################################################
    # 史前巨型屎山，没用了 但是不是很想删除，可能是有感情了
    # Commented since not used
    # if news_or_cloaca == "牛子":
    #     news_message = f"你今天有一根{dick_enchant}{hexcolor_out}{boki_status}的{news_length_out}CM长的，{angle_status}角度为{angle}的{phimosis_status}的,并且蛋蛋{egg_weight}的牛子{a}系统点评：{system_comment_out}{a}大众点评：{Score_out}分，{dick_comment}"
    # else:
    #     news_message = f"你今天有一根{dick_enchant}{hexcolor_out}的{news_length_out}CM深的泄殖腔{a}系统点评：{system_comment_out}{a}大众点评：{Score_out}分，{dick_comment}"
    # #######################################################################
    random.seed()
    html = (
        """
    
<!doctype html>
<html lang="zh-cmn-Hans">
<html>

<head>
</head>
<style>
    @font-face {
        font-family: Rubik;
        src: url('Rubik-VariableFont_wght.ttf') format("ttf");
    }

    /* fallback */
    @font-face {
        font-family: 'Material Symbols Rounded';
        font-style: normal;
        font-weight: 100 700;
        src: url(https://fonts.gstatic.com/s/materialsymbolsoutlined/v63/kJEhBvYX7BgnkSrUwT8OhrdQw4oELdPIeeII9v6oFsI.woff2) format('woff2');
    }

    /* cyrillic-ext */
    @font-face {
        font-family: 'Rubik';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/rubik/v21/iJWZBXyIfDnIV5PNhY1KTN7Z-Yh-B4iFWkU1Z4Y.woff2) format('woff2');
        unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
    }

    /* cyrillic */
    @font-face {
        font-family: 'Rubik';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/rubik/v21/iJWZBXyIfDnIV5PNhY1KTN7Z-Yh-B4iFU0U1Z4Y.woff2) format('woff2');
        unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
    }

    /* hebrew */
    @font-face {
        font-family: 'Rubik';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/rubik/v21/iJWZBXyIfDnIV5PNhY1KTN7Z-Yh-B4iFVUU1Z4Y.woff2) format('woff2');
        unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F;
    }

    /* latin-ext */
    @font-face {
        font-family: 'Rubik';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/rubik/v21/iJWZBXyIfDnIV5PNhY1KTN7Z-Yh-B4iFWUU1Z4Y.woff2) format('woff2');
        unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
    }

    /* latin */
    @font-face {
        font-family: 'Rubik';
        font-style: normal;
        font-weight: 400;
        font-display: swap;
        src: url(https://fonts.gstatic.com/s/rubik/v21/iJWZBXyIfDnIV5PNhY1KTN7Z-Yh-B4iFV0U1.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }

    * {
        margin: 0;
        padding: 0;
        font-family: 'Rubik', Fallback, sans-serif;
    }

    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded';
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
    }

    .Rubik-font {
        font-family: Rubik;
    }

    .right-align {
        text-align: right;
    }

    .limit {
        width: 1080px;
        height: 800px;
        background-color: red;
    }

    .husband {
"""+f"""
        background: url(https://blog.suchenawa.com/SuricPlugins/husband/{Image_url_out}.png) no-repeat center center;
"""+"""
        background-size: contain;
        background-size: 600px;
        /* position: fixed; */
        /* -moz-background-size: cover;
        -ms-background-size: cover;
        -o-background-size: cover; */

    }
    
</style>

"""
        + f"""

<body class="limit" style="margin:0px;padding:0px;background-color:transparent;">
    <div style="background-color: #FDFCFC; border-radius: 64px;">
        <div style="height:180px;background-color: rgba(46, 101, 120, 0.05);">
            <div style="display: flex;line-height: 180px">
                <span class="Rubik-font" style="font-size: 56px;margin-left:56px;">Random_News</span>
                <span class="Rubik-font right-align"
                    style="font-size: 64px;margin-right: 56px;flex: 1;">{score_out}<span
                        style="font-size: 24px;;">分</span></span>
            </div>
            <div style="display: flex;">
                <div style="width: 400px;padding: 20px 0px 40px 40px;">
                    <h1 style="text-align: center;">您今天拥有的是{news_or_cloaca_out}</h1><br>
                    <div style="border: 1px dashed #74787A;border-radius: 50px;text-align: center;padding: 20px;">
                        <div style="display: flex;">
                            <div style="flex: 1;"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" style="padding:3px 0px">
                                <path
                                    d="M11.875 22.8q-2.225 0-4.2-.85t-3.437-2.312Q2.775 18.175 1.925 16.2q-.85-1.975-.85-4.2 0-2.25.863-4.225Q2.8 5.8 4.3 4.338q1.5-1.463 3.5-2.301 2-.837 4.275-.837 2.2 0 4.163.762 1.962.763 3.45 2.1 1.487 1.338 2.362 3.15.875 1.813.875 3.938 0 3.325-2.15 4.937-2.15 1.613-4.8 1.613h-1.25q-.075 0-.137.062-.063.063-.063.138 0 .15.25.525t.25 1.125q0 1.35-.937 2.3-.938.95-2.213.95ZM12 12Zm-5.725 1.3q.75 0 1.275-.525.525-.525.525-1.275 0-.75-.525-1.275Q7.025 9.7 6.275 9.7q-.75 0-1.275.525-.525.525-.525 1.275 0 .75.525 1.275.525.525 1.275.525Zm3.05-4.1q.75 0 1.275-.525.525-.525.525-1.275 0-.75-.525-1.275-.525-.525-1.275-.525-.75 0-1.275.525-.525.525-.525 1.275 0 .75.525 1.275.525.525 1.275.525Zm5.1 0q.75 0 1.275-.525.525-.525.525-1.275 0-.75-.525-1.275-.525-.525-1.275-.525-.75 0-1.275.525-.525.525-.525 1.275 0 .75.525 1.275.525.525 1.275.525Zm3.1 4.1q.75 0 1.275-.525.525-.525.525-1.275 0-.75-.525-1.275-.525-.525-1.275-.525-.75 0-1.275.525-.525.525-.525 1.275 0 .75.525 1.275.525.525 1.275.525Zm-5.75 6.85q.275 0 .438-.112.162-.113.162-.338 0-.375-.375-.787-.375-.413-.375-1.363 0-1.125.75-1.812.75-.688 1.8-.688h1.8q1.55 0 2.925-.838 1.375-.837 1.375-3.062 0-3.175-2.437-5.238Q15.4 3.85 12.075 3.85q-3.475 0-5.913 2.362Q3.725 8.575 3.725 12q0 3.4 2.325 5.775 2.325 2.375 5.725 2.375Z" />
                            </svg>
                            <div style="width: 12px;"></div>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding:0px 8px 0px 0px">颜色</span>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;background-color: {hexcolor_out};padding:0px 8px;color:{hextextcolor_out}">{hexcolor_out}</span>
                            <div style="flex: 1;"></div>
                        </div>
                    </div>
                    <br>
                    <div style="border: 1px dashed #74787A;border-radius: 50px;text-align: center;padding: 20px;">
                        <div style="display: flex;">
                            <div style="flex: 1;"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" style="padding:3px 0px">
                                <path
                                    d="M5 22.325q-1.375 0-2.35-.975-.975-.975-.975-2.35 0-1.025.563-1.837.562-.813 1.437-1.213v-7.9q-.875-.4-1.437-1.213Q1.675 6.025 1.675 5q0-1.375.975-2.35.975-.975 2.35-.975 1.025 0 1.838.562.812.563 1.212 1.438h7.9q.375-.875 1.187-1.438.813-.562 1.863-.562 1.375 0 2.35.975.975.975.975 2.35 0 1.05-.562 1.863-.563.812-1.438 1.187v7.9q.875.4 1.438 1.213.562.812.562 1.837 0 1.375-.975 2.35-.975.975-2.35.975-1.025 0-1.837-.563-.813-.562-1.213-1.437h-7.9q-.4.875-1.212 1.437-.813.563-1.838.563Zm0-16.65q.275 0 .475-.2.2-.2.2-.475 0-.275-.2-.475-.2-.2-.475-.2-.275 0-.475.2-.2.2-.2.475 0 .275.2.475.2.2.475.2Zm14 0q.275 0 .475-.2.2-.2.2-.475 0-.275-.2-.475-.2-.2-.475-.2-.275 0-.475.2-.2.2-.2.475 0 .275.2.475.2.2.475.2Zm-10.95 12h7.9q.25-.575.7-1.025.45-.45 1.025-.7v-7.9q-.575-.25-1.025-.7-.45-.45-.7-1.025h-7.9q-.25.575-.7 1.025-.45.45-1.025.7v7.9q.575.25 1.025.7.45.45.7 1.025Zm10.95 2q.275 0 .475-.2.2-.2.2-.475 0-.275-.2-.475-.2-.2-.475-.2-.275 0-.475.2-.2.2-.2.475 0 .275.2.475.2.2.475.2Zm-14 0q.275 0 .475-.2.2-.2.2-.475 0-.275-.2-.475-.2-.2-.475-.2-.275 0-.475.2-.2.2-.2.475 0 .275.2.475.2.2.475.2ZM5 5Zm14 0Zm0 14ZM5 19Z" />
                            </svg>
                            <div style="width: 12px;"></div>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding:0px 8px 0px 0px">附魔</span>
                            <span class="Rubik-font" style="line-height: 30px;font-size: 24px;padding-right: 5px;">{
                                dick_enchant_out}</span>
                            <div style="flex: 1;"></div>
                        </div>
                    </div>
                    <br>
                    <div style="border: 1px dashed #74787A;border-radius: 50px;text-align: center;padding: 20px;">
                        <div style="display: flex;">
                            <div style="flex: 1;"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" style="padding:3px 0px">
                                <path
                                    d="M4.85 21.8q-1.1 0-1.875-.775Q2.2 20.25 2.2 19.15v-4.1h2.65v4.1h4.1v2.65Zm10.2 0v-2.65h4.1v-4.1h2.65v4.1q0 1.1-.775 1.875-.775.775-1.875.775ZM2.2 8.95v-4.1q0-1.1.775-1.875Q3.75 2.2 4.85 2.2h4.1v2.65h-4.1v4.1Zm16.95 0v-4.1h-4.1V2.2h4.1q1.1 0 1.875.775.775.775.775 1.875v4.1Z" />
                            </svg>
                            <div style="width: 12px;"></div>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding:0px 8px 0px 0px">长度</span>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding-right: 5px;">{news_length_out}</span>
                            <span class="Rubik-font" style="line-height: 30px;font-size: 24px;">CM</span>
                            <div style="flex: 1;"></div>
                        </div>
                    </div>
                    <br>
                    <div style="border: 1px dashed #74787A;border-radius: 50px;text-align: center;padding: 20px;">
                        <div style="display: flex;">
                            <div style="flex: 1;"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" style="padding:3px 0px">
                                <path
                                    d="m9.9 22.275-1.85-1.85 9.2-9.2H16v-2.65h5.75v5.75H19.1v-1.25Zm-1.7-6.4L2.625 3.85l1.9-1.9L16.55 7.525 14.825 9.25 11.95 7.9 8.6 11.25l1.375 2.85ZM7.6 9.25 9.975 6.9 5.4 4.675l-.05.05Z" />
                            </svg>
                            <div style="width: 12px;"></div>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding:0px 8px 0px 0px">角度</span>
                            <span class="Rubik-font" style="line-height: 30px;font-size: 24px;">{angle}</span>
                            <span class="Rubik-font" style="line-height: 30px;font-size: 24px;">°</span>
                            <div style="flex: 1;"></div>
                        </div>
                    </div>
                    <br>
                    <div style="border: 1px dashed #74787A;border-radius: 50px;text-align: center;padding: 20px;">
                        <div style="display: flex;">
                            <div style="flex: 1;"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" style="padding:3px 0px">
                                <path d="M6.4 18.45 4.55 16.6l9.25-9.275H5.675v-2.65h12.65v12.65h-2.65V9.2Z" />
                            </svg>
                            <div style="width: 12px;"></div>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding:0px 8px 0px 0px;overflow: hidden;">{boki_status_out}/{phimosis_status_out}</span>
                            <div style="flex: 1;"></div>
                        </div>
                    </div>
                    <br>
                    <div style="border: 1px dashed #74787A;border-radius: 50px;text-align: center;padding: 20px;">
                        <div style="display: flex;">
                            <div style="flex: 1;"></div>
                            <svg xmlns="http://www.w3.org/2000/svg" height="24" width="24" style="padding:3px 0px">
                                <path
                                    d="m13.25 22.3-1.65-1.65 3.6-3.6L6.95 8.8l-3.6 3.6-1.65-1.65 1.5-1.5L1.55 7.6l2.1-2.1L2 3.85 3.85 2 5.5 3.65l2.1-2.1L9.25 3.2l1.5-1.5 1.65 1.65-3.6 3.6 8.25 8.25 3.6-3.6 1.65 1.65-1.5 1.5 1.65 1.65-2.1 2.1L22 20.15 20.15 22l-1.65-1.65-2.1 2.1-1.65-1.65Z" />
                            </svg>
                            <div style="width: 12px;"></div>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding:0px 8px 0px 0px">蛋蛋重量</span>
                            <span class="Rubik-font"
                                style="line-height: 30px;font-size: 24px;padding-right: 5px;">{egg_weight_out}</span>
                            <span class="Rubik-font" style="line-height: 30px;font-size: 24px;">克</span>
                            <div style="flex: 1;"></div>
                        </div>
                    </div>


                </div>
                <div style="width: 100%; flex: 1;padding: 20px 40px 20px 40px;">
                    <div style="background-color: rgba(46, 101, 120, 0.05);padding: 40px;border-radius: 50px;">
                        <div style="display: flex;">
                            <span class="Rubic-font"
                                style="font-size: 36px;font-weight:600;line-height: 40px;">大众点评分数：</span>
                            <div style="flex: 1;"></div>
                            <div style="">
                                <span class="Rubic-font"
                                    style="font-size: 48px;font-weight:600;line-height: 40px;">{score_out}</span>
                                <span style="" font-size:32px>分</span>
                            </div>

                        </div>
                        <br>
                        <span style="font-size:24px">{dick_comment}</span>
                        <!-- <span>Test Text</span><br>
                        <span>Test Text</span><br> -->
                    </div>
                    <div style="padding: 40px;border-radius: 50px;">
                        <span style="font-size:24px">系统评价：</span>
                        <span style="font-size:24px">{system_comment_out}</span>
                    </div>
                    <div style="background-color: rgba(46, 101, 120, 0.05);border-radius: 50px;width: 100%;">
                        <div class="husband" style="height: 300px;width: 100%;border-radius: 50px;">
                            

                        </div>

                    </div>
                </div>
            </div>
        </div>
</body>

</html>
    
    """
    )
    browser = Ariadne.current().launch_manager.get_interface(PlaywrightBrowser)
    async with browser.page(
        viewport={"width": 800, "height": 800}, device_scale_factor=1.0
    ) as page:
        await page.set_content(html)
        img = await page.screenshot(
            type="jpeg", quality=80, full_page=True, scale="device"
        )
    return await send_message(event, MessageChain(Image(data_bytes=img)), app.account)



@listen(GroupMessage, FriendMessage)
@dispatch(Twilight(PrefixMatch(), UnionMatch("Null几把呢", "你几把呢")))
@decorate(
    Switch.check(channel.module),
    Distribution.distribute(),
    Blacklist.check(),
    FunctionCall.record(channel.module),
)
async def daily_news_playwright(app: Ariadne, event: MessageEvent,supplicant: Member | Friend ):
    await send_message(
            event.sender.group if isinstance(event, GroupMessage) else event.sender,
            MessageChain("你几把消失了"),
            app.account,
        )


@listen(GroupMessage, FriendMessage)
@dispatch(Twilight(PrefixMatch(), UnionMatch("我想拥有bb", "我想拥有逼逼")))
@decorate(
    Switch.check(channel.module),
    Distribution.distribute(),
    Blacklist.check(),
    FunctionCall.record(channel.module),
)
async def bb(app: Ariadne, event: MessageEvent,supplicant: Member | Friend ):
    bblength = 0
    await send_message(
            event.sender.group if isinstance(event, GroupMessage) else event.sender,
            MessageChain("你先别急，我还没写"),
            app.account,
        )
    
async def file_update_service():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            with open(filepath,"wb") as file:
                file.write(data)
                if os.path.exists(filepath):
                    logger.success("[Daily_News] 资源文件更新成功！")
                else:
                    logger.error("[Daily_News] 资源文件更新失败！")

# Seed
def random_seed(supplicant: Member | Friend):
    random.seed(int(f"{datetime.now().strftime('%Y%m%d')}{supplicant.id}"))

