import requests

from plugins.CustomClass.response import FuncResponse


class MaeRateResponse(FuncResponse):
    def __init__(self, response_code: int, response_rate: str):
        super().__init__(response_code, None)
        self.response_code = response_code
        self.response_rate = response_rate


async def GetMaeRate():
    url = "https://www.maetown.cn/Rate/GetMyRate"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cookie": "Hm_lvt_11995333e9a8ad827efcd37d5599c8f8=1724342315,1724599457,1724759322,1725283159; Hm_lpvt_11995333e9a8ad827efcd37d5599c8f8=1725283159; HMACCOUNT=D0A6746103DB4B2A",
        "referer": "https://www.maetown.cn/html/index.html",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "token": "4t1fyiYT/VrtT+en40kqjw==",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        rate = data.get("data", 0.052)
        return MaeRateResponse(0, rate)
    except Exception as e:
        return FuncResponse(1, str(e))
