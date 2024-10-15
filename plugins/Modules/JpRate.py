import requests
from bs4 import BeautifulSoup
from plugins.CustomClass.response import FuncResponse


class JpRateResponse(FuncResponse):
    def __init__(self, response_code: int, response_rate: str, response_date: str):
        super().__init__(response_code, None)
        self.response_code = response_code
        self.response_rate = response_rate
        self.response_date = response_date


def GetJpRate():
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
