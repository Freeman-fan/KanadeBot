import hashlib
import random
import requests
import configparser

from plugins.CustomClass.response import FuncResponse


def BaiduTranslate(text:str = 'apple', raw_lang:str = 'auto', to_lang:str = 'zh') -> FuncResponse:
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read("./plugins/config/BaiduTranslate.ini", encoding="utf-8")
    appid = config.get("BaiduTranslate", "appid")
    secret_key = config.get("BaiduTranslate", "secret_key")
    # 签名生成
    salt = str(random.randint(1, 65536))
    sign_str = appid + text + salt + secret_key
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
    # 构造请求参数
    params = {"q": text, "from": raw_lang, "to": to_lang, "appid": appid, "salt": salt, "sign": sign}
    # 发送请求
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    response = requests.get(url, params=params)
    # 响应
    if response.status_code == 200:
        result = response.json()
        if "trans_result" in result:
            dst = ''
            for item in result["trans_result"]:
                dst += item['dst']
                if item != result["trans_result"][-1]:  # 检查当前数据是否不是最后一条数据
                    dst += '\n'
            return FuncResponse(0, dst)
        else:
            return FuncResponse(1, '解析错误')
    else:
        return FuncResponse(1, f"请求失败，状态码：{response.status_code}")


