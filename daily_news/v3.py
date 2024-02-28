from asyncio.log import logger
import json
import os
import random
from datetime import datetime
from pathlib import Path

themelist = ["light", "dark"]
assets_path = Path(Path(__file__).parent, "assets")
# 读取基本配置文件
settings_file = Path(assets_path / "news_settings_v3.json")
with settings_file.open("r", encoding="UTF-8") as f:
    _data = json.loads(f.read())
    TYPE_TEMPLATES = _data["news_type"]

async def _newstype():
    news_type = random.choice(TYPE_TEMPLATES)

def daily_random(seed):
    # 获取当前 UTC 日期的整数形式
    today_utc = datetime.utcnow().date()
    today_seed = int(today_utc.strftime("%m%d"))

    random.seed(today_seed + seed)

    # 生成一个0到99之间的随机数
    random_number = random.randint(0, 99)

    # 返回随机数和种子
    return random_number, today_seed + seed




# 初始化需要的对象
    #类型
news_type ="未知"
    #大小
news_length = 0
    #大小
egg_weight = "未知"

news_type ="未知"

# 随机类型



# 随机长度
    
news_length = random.randint(5,30)
# 传入QQ号作为seed
seed_value =114
result,filnal_seed = daily_random(seed_value)
print(result,filnal_seed)
# 随机抽取一名幸运儿
if result < 1:
    misfortune = True




timeformat = '%H'
themeTime = datetime.now().strftime(timeformat)
if( 7 < int(themeTime) < 18):
    light_theme_status = 'theme'
    light_hover_status = 'theme-h'
    dark_theme_status = 'disable_theme'
    dark_hover_status = 'disable_theme-h'
    logger.debug("当前是LightMode")
else:
    dark_theme_status = 'theme'
    dark_hover_status = 'theme-h'
    light_theme_status = 'disable_theme'
    light_hover_status = 'disable_theme-h'
    logger.debug("当前是DarkMode")

