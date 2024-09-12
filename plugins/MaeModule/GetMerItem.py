import requests
import os


async def GetMerItem(mNum: str):
    api_url = 'https://www.maetown.cn/Mobile/Mercari/GoodsDetail?id=' + mNum
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        try:
            product_id = data.get('data', {}).get('id')
            product_name = data.get('data', {}).get('name')
            product_description = data.get('data', {}).get('description')
            product_price = data.get('data', {}).get('price')
            product_price_cny = data.get('data', {}).get('priceCNY')
            product_status = data.get('data', {}).get('status')
            product_photos = data.get('data', {}).get('photos', [])
            product_comment = data.get('data', {}).get('comment', [])
            seller_id = data.get('data', {}).get('seller', {}).get('id')
            
        except Exception as e:
            print(e)
            return Exception
        
        imagelist = []
        for index, photo_url in enumerate(product_photos, start=1):
            imagelist.append(photo_url)

        comment_list = []
        for comment in product_comment:
            user_id = comment.get('user', {}).get('id')
            user_name = comment.get('user', {}).get('name')
            message = comment.get('message')
            if user_id == seller_id:
                user_name = user_name + '(卖家)'
            comment_add = [user_name, message]
            comment_list.append(comment_add)
                

        return(product_id, product_name, product_description, product_price, product_price_cny, product_status, imagelist, comment_list)
            
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        