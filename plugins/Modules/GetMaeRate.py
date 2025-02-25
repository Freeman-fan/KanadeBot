'''
拉取Mae交易汇率
'''

import requests
from typing import Union
import configparser


from plugins.CustomClass.response import FuncResponse
from plugins.Modules.GetMerItem import get_maeitem


class MaeRateResponse(FuncResponse):
    def __init__(self, response_code: int, response_rate: str):
        super().__init__(response_code, None)
        self.response_code = response_code
        self.response_rate = response_rate


class MaeRate():
    def __init__(self, maeRate: float = 0.052):
        self.maeRate = maeRate

    def UpdateRate(self) -> FuncResponse:
        newRate = GetMaeRate()
        if newRate.response_code == 0:
            self.maeRate = newRate.response_rate
            return FuncResponse(0, "")
        elif newRate.response_code == 1:
            return FuncResponse(1, newRate.response_data)


def GetMaeRate() -> Union[FuncResponse, MaeRateResponse]:
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read("./plugins/config/Config.ini", encoding="utf-8")
    rateitem = config.get("rateitem", "item")
    response = get_maeitem(rateitem)
    try:
        response = response.json()
        rate = response.get("data",{}).get("rate",0.052)
        return MaeRateResponse(0, rate)
    except Exception as e:
        return FuncResponse(1, str(e))
