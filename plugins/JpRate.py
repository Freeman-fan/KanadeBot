import requests
from bs4 import BeautifulSoup

import nonebot

Jprate = 0.05


@nonebot.scheduler.scheduled_job("interval", minutes = 1)
async def _():
    bot = nonebot.get_bot()
    global Jprate
    rate_update, update_date = GetJpRate()
    if rate_update != Jprate:
        await bot.send_private_msg(user_id=501079827, message=f'日元汇率变动：{rate_update}\n更新时间{update_date}')
        Jprate = rate_update




def GetJpRate():
    try:
        url = 'https://www.boc.cn/sourcedb/whpj/'
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            tr_tags = soup.find_all('tr')
            for tr in tr_tags:
                td_tags = tr.find_all('td')
                if td_tags and '日元' in td_tags[0].text:
                    rate = td_tags[3].text.strip()
                    update_date_tag = tr.find('td', class_='pjrq')
                    update_date = update_date_tag.text.strip()
                    return(rate, update_date)
        else:
            print('请求失败：', response.status_code)
            return None
    except Exception as e:
        print(f'GetJpRate请求错误：{str(e)}')
        return None