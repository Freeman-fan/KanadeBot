import requests
import os
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


async def GetMerItem(mNum: str):
    api_url = "https://www.maetown.cn/Mobile/Mercari/GoodsDetail?id=" + mNum
    try:
        response = requests.get(api_url)
    except Exception as e:
        return FuncResponse(1, '请求失败，请检查网络')
    if response.status_code == 200:
        data = response.json()
        try:
            product_id = data.get("data", {}).get("id")
            product_name = data.get("data", {}).get("name")
            product_description = data.get("data", {}).get("description")
            product_price = data.get("data", {}).get("price")
            product_price_cny = data.get("data", {}).get("priceCNY")
            product_status = data.get("data", {}).get("status")
            product_photos = data.get("data", {}).get("photos", [])
            product_comment = data.get("data", {}).get("comments", [])
            seller_id = data.get("data", {}).get("seller", {}).get("id")
        except Exception as e:
            return FuncResponse(1, '请求失败，商品不存在')

        imagelist = []
        for index, photo_url in enumerate(product_photos, start=1):
            imagelist.append(photo_url)

        comment_list = []
        for comment in product_comment:
            user_id = comment.get("user", {}).get("id")
            user_name = comment.get("user", {}).get("name")
            message = comment.get("message")
            if user_id == seller_id:
                user_name = user_name + "(卖家)"
            comment_add = [user_name, message]
            comment_list.append(comment_add)

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
        )
    else:
        return FuncResponse(1, '请求失败，未知错误\n'+str(e))
