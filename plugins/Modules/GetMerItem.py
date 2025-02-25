import requests
import json
from plugins.CustomClass.response import FuncResponse


class ItemResponse(FuncResponse):
    def __init__(
        self,
        response_code: int = -1,
        product_id: str = "",
        product_name: str = "",
        product_description: str = "",
        product_price: str = "",
        product_price_cny: str = "",
        product_status: str = "",
        imagelist: list = [],
        comment_list: list = [],
        postage_payment: int = 0,
    ):
        super().__init__(response_code, None)
        self.response_code = response_code
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.product_price = product_price
        self.product_price_cny = product_price_cny
        self.product_status = product_status
        self.imagelist = imagelist
        self.comment_list = comment_list
        self.postage_payment = postage_payment


def get_maeitem(mNum: str) -> json:
    # 请求URL
    url = "https://www.maetown.cn/api/web/search/goods/detail"

    # 请求头
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
        "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbjp1c2VyOmtleSI6IjFhNDQ3MWNkNTg4ZTEwMDAifQ.a0r00aY_0ov3C6JedRiwT",
        "Cache-Control": "no-cache",
        "Channel": "3",
        "Content-Type": "application/json",
        "Cookie": "Hm_lvt_11995333e9a8ad827efcd37d5599c8f8=1738728592,1739624818,1740104701,1740480623",
        "Origin": "https://www.maetown.cn",
        "Platform": "104",
        "Pragma": "no-cache",
        "Priority": "u=1,i",
        "Referer": "https://www.maetown.cn/wap/",
        "Sec-Ch-Ua": '"Not(A:Brand";v="99","Microsoft Edge";v="133","Chromium";v="133"',
        "Sec-Ch-Ua-Mobile": "70",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "Version": "145",
        "Zoneid": "Asia/Shanghai",
    }

    # 请求体
    data = {"goodsId": mNum, "platformCode": "101"}

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    return response


async def GetMerItem(mNum: str):
    try:
        response = get_maeitem(mNum)
    except Exception as e:
        return FuncResponse(1, "请求失败，请检查网络")
    if response.status_code == 200:
        data = response.json()
        try:
            product_id = data.get("data", {}).get("goodsId")
            product_name = data.get("data", {}).get("name")
            product_description = data.get("data", {}).get("description")
            product_price = data.get("data", {}).get("price")
            product_price_cny = data.get("data", {}).get("priceCNY")
            product_status = data.get("data", {}).get("status")
            product_photos = data.get("data", {}).get("images", [])
            product_comment = data.get("data", {}).get("comments", [])
            seller_name = data.get("data", {}).get("seller", {}).get("name")
            items = data.get("data", {}).get("items", [])
        except Exception as e:
            return FuncResponse(1, "请求失败，商品不存在")

        imagelist = []
        for index, photo_url in enumerate(product_photos, start=1):
            imagelist.append(photo_url)

        comment_list = []
        for comment in product_comment:
            user_name = comment.get("userName")
            message = comment.get("content")
            time = comment.get("createTime")
            if user_name == seller_name:
                user_name = '【卖家】'+user_name
            comment_add = [user_name, message, time]
            comment_list.append(comment_add)

        for item in items:
            if item.get("value") == "商品运费":
                postage_payment = (
                    0 if item.get("label") == "送料込み(出品者負担)" else 1
                )

        return ItemResponse(
            0,
            product_id,
            product_name,
            product_description,
            product_price,
            product_price_cny,
            product_status,
            imagelist,
            comment_list,
            postage_payment,
        )
    else:
        return FuncResponse(1, "请求失败，未知错误\n" + str(e))
