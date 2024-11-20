'''
拉取中国银行日元现汇汇率
'''

import requests
from bs4 import BeautifulSoup
from typing import Union

from plugins.CustomClass.response import FuncResponse


class JpRateResponse(FuncResponse):
    def __init__(self, response_code: int, response_rate: str, response_date: str):
        super().__init__(response_code, None)
        self.response_code = response_code
        self.response_rate = response_rate
        self.response_date = response_date


class JpRate():
    def __init__(self, jpRate: float = 0.05, date: str = ""):
        self.jpRate = jpRate
        self.date = date

    def UpdateRate(self) -> FuncResponse:
        response = GetJpRate()
        if response.response_code == 0:
            self.jpRate = float(response.response_rate)
            self.date = str(response.response_date)
            return FuncResponse(0, "")
        elif response.response_code == 1:
            return FuncResponse(1, response.response_data)


def GetJpRate() -> Union[FuncResponse, JpRateResponse]:
    try:
        url = "https://www.boc.cn/sourcedb/whpj/"
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            tr_tags = soup.find_all("tr")
            for tr in tr_tags:
                td_tags = tr.find_all("td")
                if td_tags and "日元" in td_tags[0].text:
                    rate = td_tags[3].text.strip()
                    update_date_tag = tr.find("td", class_="pjrq")
                    update_date = update_date_tag.text.strip()
                    return JpRateResponse(0, rate, update_date)
        else:
            print("请求失败：", response.status_code)
            return FuncResponse(1, f"网络错误：{str(response.status_code)}")
    except Exception as e:
        print(f"GetJpRate请求错误：{str(e)}")
        return FuncResponse(1, str(e))
