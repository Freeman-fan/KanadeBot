import requests
import os

async def save_image(photo_url, product_id, index):
    photo_filename = f"{product_id}_{index}.jpg"
    photo_response = requests.get(photo_url)
    try:
        if photo_response.status_code == 200:
            current_dir = os.getcwd()
            photo_abspath = os.path.join(current_dir, photo_filename)
            with open(photo_abspath, 'wb') as f:
                f.write(photo_response.content)
        else:
            print(f"Failed to retrieve image, status code: {photo_response.status_code}")
    except Exception as e:
        pass


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
            seller_name = data.get('data', {}).get('seller', {}).get('name')
        except Exception as e:
            print(e)
            return Exception
        
        # 提取响应数据
        product_id = data.get('data', {}).get('id')
        product_photos = data.get('data', {}).get('photos', [])

        # 循环遍历图片URL列表，并为每张图片使用序号
        imagelist = []
        for index, photo_url in enumerate(product_photos, start=1):
            # imagelist.append(await save_image(photo_url, product_id, index))
            imagelist.append(photo_url)
        return(product_id, product_name, product_description, product_price, product_price_cny, product_status, imagelist)
            
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        