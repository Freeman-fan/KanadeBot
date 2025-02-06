import requests
import json
import os
import configparser
from PIL import Image, ImageDraw, ImageFont

from plugins.CustomClass.response import FuncResponse


# 初始化数据
def init_data():
    global proxies
    global temp_path

    # #读取代理配置
    # try:
    #     config = configparser.ConfigParser()
    #     config.read('./plugins/config/Config.ini', encoding='utf-8')
    #     proxy_host = config.get('Proxy', 'host')
    #     proxy_port = config.get('Proxy', 'port')
    # except Exception as e:
    #     print(f"查卡模块代理初始化错误：{e}")

    # 读取代理配置
    try:
        config = configparser.ConfigParser()
        config.read("./plugins/config/Config.ini", encoding="utf-8")
        proxy_host = config.get("Proxy", "host")
        proxy_port = config.get("Proxy", "port")
    except Exception as e:
        return FuncResponse(1, f"代理配置文件读取失败:{e}")

    proxies = {
        "http": f"socks5://{proxy_host}:{proxy_port}",
        "https": f"socks5://{proxy_host}:{proxy_port}",
    }

    # 读取缓存路径
    temp_path = "./Temp"
    # 检查缓存路径是否存在
    if not os.path.exists(fr"{temp_path}/card_fullsize_temp"):
        os.makedirs(fr"{temp_path}/card_fullsize_temp")
    if not os.path.exists(fr"{temp_path}/card_membercollect_temp"):
        os.makedirs(fr"{temp_path}/card_membercollect_temp")
    if not os.path.exists(fr"{temp_path}/card_mini_image"):
        os.makedirs(fr"{temp_path}/card_mini_image")
    if not os.path.exists(fr"{temp_path}/example_image"):
        print(fr"查卡器素材图片路径不存在，创建略缩图功能会受到影响，请检查")
        os.makedirs(fr"{temp_path}/example_image")
    if not os.path.exists(fr"{temp_path}/cards.json"):
        print(f"查卡器卡片数据不存在，请检查")


# 更新数据
def update_data() -> FuncResponse:
    global proxies
    global temp_path

    # 更新cards.json
    try:
        response = requests.get(
            "https://sekai-world.github.io/sekai-master-db-diff/cards.json",
            proxies=proxies,
            timeout=10,
        )
        response.raise_for_status()
    except Exception as e:
        return FuncResponse(1, f"cards.josn获取失败:{e}")

    # 检查是否有更新
    try:
        with open(fr"{temp_path}/cards.json", "r", encoding="utf-8") as f:
            old_cards = json.load(f)
        # 检查旧数据和新数据的最后一项是否一致
        if old_cards[-1]["id"] == response.json()[-1]["id"]:
            return FuncResponse(0, "卡面数据同步结束，没有发现新数据")
        else:
            with open(fr"{temp_path}/cards.json", "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
    except Exception as e:
        return FuncResponse(1, fr"卡面数据更新失败:{e}")

    # 更新卡面略缩图
    card_update_Response = FuncResponse(0, [])
    count = 0
    with open(fr"{temp_path}/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)
    for card in cards:
        normal_url = (
            "https://storage.sekai.best/sekai-jp-assets/thumbnail/chara_rip/"
            + card["assetbundleName"]
            + "_normal.png"
        )
        after_traning_url = (
            "https://storage.sekai.best/sekai-jp-assets/thumbnail/chara_rip/"
            + card["assetbundleName"]
            + "_after_training.png"
        )
        # 花前
        try:
            if not os.path.exists(
                fr"{temp_path}/card_mini_image/{card['assetbundleName']}_normal.png"
            ):
                response = requests.get(normal_url, proxies=proxies, timeout=10)
                response.raise_for_status()
                with open(
                    fr"{temp_path}/card_mini_image/{card['assetbundleName']}_normal.png",
                    "wb",
                ) as f:
                    f.write(response.content)
                count += 1
        except Exception as e:
            card_update_Response.response_code = 1
            card_update_Response.response_data.append(
                f"卡面{card['assetbundleName']}花前略缩图更新失败:{e}"
            )
        # 花后
        try:
            if not os.path.exists(
                fr"{temp_path}/card_mini_image/{card['assetbundleName']}_after_training.png"
            ) and card["cardRarityType"] in ["rarity_3", "rarity_4"]:
                response = requests.get(after_traning_url, proxies=proxies, timeout=10)
                response.raise_for_status()
                with open(
                    fr"{temp_path}/card_mini_image/{card['assetbundleName']}_after_training.png",
                    "wb",
                ) as f:
                    f.write(response.content)
                count += 1
        except Exception as e:
            card_update_Response.response_code = 1
            card_update_Response.response_data.append(
                f"卡面{card['assetbundleName']}花后略缩图更新失败:{e}"
            )
    if card_update_Response.response_code == 0:
        card_update_Response.response_data.append(
            f"卡面数据同步完成，本次添加了{count}张卡面"
        )
    else:
        card_update_Response.response_data.append(
            f"卡面数据同步完成，本次添加了{count}张卡面"
        )
    return card_update_Response

#角色昵称转换为id
def charaName2charaID(chara_name: str) -> int:
    dic = {
        'ick': 1,
        'saki': 2, 
        'hnm': 3, 
        'shiho': 4,
        'mnr': 5, 
        'hrk': 6, 
        'airi': 7, 
        'szk': 8,
        'khn': 9, 
        'an': 10, 
        'akt': 11, 
        'toya': 12,
        'tks': 13, 
        'emu':14, 
        'nene': 15, 
        'rui': 16,
        'knd': 17, 
        'mfy': 18, 
        'ena': 19, 
        'mzk': 20,
        'miku': 21, 
        'rin': 22, 
        'len': 23, 
        'luka': 24, 
        'meiko': 25, 
        'kaito': 26
    }
    try:
        return dic[chara_name.lower()]
    except:
        return None



#请求卡面大图
def get_card_fullsize(card_id: int) -> FuncResponse:
    global temp_path

    if not os.path.exists(fr"{temp_path}/cards.json"):
        return FuncResponse(1, "卡面数据不存在，请先更新卡面数据")
    
    #检查id合法性，提取卡面数据
    with open(fr"{temp_path}/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)
    for card in cards:
        if card["id"] == card_id:
            break
    if card["id"] != card_id:
        return FuncResponse(1, "卡面id不存在，请检查")
    #检查缓存中是否有对应卡面
    if os.path.exists(fr"{temp_path}/card_fullsize_temp/{card['assetbundleName']}_normal.png"):
        #遍历所有匹配的图片，返回匹配的图片的全部绝对路径
        file_list = [os.path.abspath(fr"{temp_path}/card_fullsize_temp/{card['assetbundleName']}_normal.png")]
        if card["cardRarityType"] in ["rarity_3", "rarity_4"]:
            file_list.append(
                os.path.abspath(fr"{temp_path}/card_fullsize_temp/{card['assetbundleName']}_after_training.png")
            )
        return FuncResponse(0, file_list)
    else:
        #缓存中没有，联网获取
        normal_url = 'https://storage.sekai.best/sekai-jp-assets/character/member/'+card['assetbundleName']+'_rip/card_normal.png'
        after_training_url = 'https://storage.sekai.best/sekai-jp-assets/character/member/'+card['assetbundleName']+'_rip/card_after_training.png'
        try:
            response = requests.get(normal_url, proxies=proxies, timeout=10)
            response.raise_for_status()
            with open(fr"{temp_path}/card_fullsize_temp/{card['assetbundleName']}_normal.png", "wb") as f:
                f.write(response.content)
            file_list = [os.path.abspath(fr"{temp_path}/card_fullsize_temp/{card['assetbundleName']}_normal.png")]
            if card["cardRarityType"] in ["rarity_3", "rarity_4"]:
                response = requests.get(after_training_url, proxies=proxies, timeout=10)
                response.raise_for_status()
                with open(fr"{temp_path}/card_fullsize_temp/{card['assetbundleName']}_after_training.png", "wb") as f:
                    f.write(response.content)
                file_list.append(os.path.abspath(fr"{temp_path}/card_fullsize_temp/{card['assetbundleName']}_after_training.png"))
            return FuncResponse(0, file_list)
        except Exception as e:
            return FuncResponse(1, f"卡面获取失败:{e}")


# 请求角色略缩图
def get_membercollect(charaid: int) -> FuncResponse:
    global temp_path

    if not os.path.exists(fr"{temp_path}/cards.json"):
        return FuncResponse(1, "卡面数据不存在，请先更新卡面数据")
    
    #检查缓存中是否有对应角色的最新图片
    count = 0
    with open(fr"{temp_path}/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)
    for card in cards:
        if card["characterId"] == charaid:
            count += 1
    if os.path.exists(fr"{temp_path}/card_membercollect_temp/{charaid}_{count}.png"):
        #存在，返回绝对路径
        return FuncResponse(0, os.path.abspath(fr"{temp_path}/card_membercollect_temp/{charaid}_{count}.png"))
    else:
        #不存在或不是最新，重新生成
        response = create_membercollect(charaid)
        response.response_data = os.path.abspath(response.response_data)
        return response


# 创建角色略缩图_大图
def create_membercollect(charaid: int) -> FuncResponse:
    global temp_path

    with open(fr"{temp_path}/cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)
    # 创建图片
    count = 0
    pic = Image.new("RGB", (1500, 8000), (235, 235, 235))
    json_path = "./cards.json"
    # 绘制略缩图
    for card in cards:
        if card["characterId"] == charaid:
            single = create_single(card)
            pos = (int(70 + count % 3 * 470), int(count / 3) * 310 + 60)
            count += 1
            pic.paste(single, pos)
    pic = pic.crop((0, 0, 1500, (int((count - 1) / 3) + 1) * 310 + 60))
    # 绘制右下角水印
    font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 28)
    image_width, image_height = pic.size
    text_width, text_height = font.getsize(f"create by KanadeBot(Github@Freeman-fan")
    text_coordinate = (
        (image_width - text_width - 20),
        (image_height - text_height - 10),
    )
    draw = ImageDraw.Draw(pic)
    draw.text(
        text_coordinate, f"create by KanadeBot(Github@Freeman-fan)", "#505050", font
    )
    # 保存图片
    save_path = fr"{temp_path}/card_membercollect_temp/{charaid}_{count}.png"
    pic.save(save_path)
    return FuncResponse(0, save_path)


# 创建角色略缩图_活动小图
def create_single(card) -> Image:
    # 创建画布
    pic = Image.new("RGB", (420, 260), (255,255,255))
    #绘制卡面略缩图
    if card["cardRarityType"] == "rarity_3" or card["cardRarityType"] == "rarity_4":
        thumnail = create_mini_single(card, False)#花前
        _, _, _, mask = thumnail.split()
        pic.paste(thumnail, (45, 15), mask)
        thumnail = create_mini_single(card, True)#花后
        _, _, _, mask = thumnail.split()
        pic.paste(thumnail, (220, 15), mask)
    else:
        thumnail = create_mini_single(card, False)
        _, _, _, mask = thumnail.split()
        pic.paste(thumnail, (132, 15), mask)
    # 添加卡名
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 28)
    text_width = font.getsize(card["prefix"])
    if text_width[0] > 420:
        font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", int(28 / (text_width[0] / 420)))
        text_width = font.getsize(card["prefix"])
    text_coordinate = ((210 - text_width[0] / 2), int(195 - text_width[1] / 2))
    draw.text(text_coordinate, card["prefix"], '#000000', font)
    # 添加卡号
    font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 28)
    text_width = font.getsize(f'id:{card["id"]}')
    text_coordinate = ((210 - text_width[0] / 2), int(230 - text_width[1] / 2))
    draw.text(text_coordinate, f'id:{card["id"]}', "#505050", font)
    return pic


# 创建单张卡面略缩图
def create_mini_single(card, istrained=False) -> Image:
    global temp_path

    # 查找图片路径
    if istrained:
        suffix = "_after_training"
    else:
        suffix = "_normal"
    image_path = fr"{temp_path}\card_mini_image\{card['assetbundleName']}{suffix}.png"

    # 读取图片并调整尺寸
    pic = Image.open(image_path)
    pic = pic.resize((156, 156))
    # 添加卡框
    card_frame = Image.open(fr"{temp_path}\example_image\{card['cardRarityType']}_cardframe.png")
    _, _, _, mask = card_frame.split()
    pic.paste(card_frame, (0, 0), mask)
    # 添加星标
    if card["cardRarityType"] == "rarity_1":
        star = Image.open(fr"{temp_path}\example_image\rarity_star_normal.png")
        star = star.resize((28, 28))
        _, _, _, mask = star.split()
        pic.paste(star, (10, 118), mask)
    if card["cardRarityType"] == "rarity_2":
        star = Image.open(fr"{temp_path}\example_image\rarity_star_normal.png")
        star = star.resize((28, 28))
        _, _, _, mask = star.split()
        pic.paste(star, (10, 118), mask)
        pic.paste(star, (36, 118), mask)
    if card["cardRarityType"] == "rarity_3":
        if istrained:
            star = Image.open(fr"{temp_path}\example_image\rarity_star_afterTraining.png")
        else:
            star = Image.open(fr"{temp_path}\example_image\rarity_star_normal.png")
        star = star.resize((28, 28))
        r, g, b, mask = star.split()
        pic.paste(star, (10, 118), mask)
        pic.paste(star, (36, 118), mask)
        pic.paste(star, (62, 118), mask)
    if card["cardRarityType"] == "rarity_4":
        if istrained:
            star = Image.open(fr"{temp_path}\example_image\rarity_star_afterTraining.png")
        else:
            star = Image.open(fr"{temp_path}\example_image\rarity_star_normal.png")
        star = star.resize((28, 28))
        _, _, _, mask = star.split()
        pic.paste(star, (10, 118), mask)
        pic.paste(star, (36, 118), mask)
        pic.paste(star, (62, 118), mask)
        pic.paste(star, (88, 118), mask)
    if card["cardRarityType"] == "rarity_birthday":
        star = Image.open(fr"{temp_path}\example_image\rarity_birthday.png")
        star = star.resize((28, 28))
        _, _, _, mask = star.split()
        pic.paste(star, (10, 118), mask)
    return pic