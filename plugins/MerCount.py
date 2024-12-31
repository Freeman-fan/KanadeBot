import sqlite3
import random
import time

import nonebot
from nonebot import on_command, CommandSession

plugin_name = "年终统计"


class merDB:
    def __init__(self, db_name: str = ".\DataBase\data.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()


# 抽奖
@on_command("抽奖", only_to_me=False, permission=lambda sender: sender.is_superuser)
async def ChouJiang(session: CommandSession):
    message = session.current_arg_text.split()
    try:
        num = int(message[0])
    except:
        num = 10
    lucky_name_list = GetLuckyName(num)
    await session.send("中奖名单\n" + "，".join(lucky_name_list))


# 抽奖实现
def GetLuckyName(num: int = 10) -> list:
    all_cn_list = GetCNList()
    lucky_num_list = random.sample(range(len(all_cn_list)), num)
    lucky_name_list = [all_cn_list[lucky_num] for lucky_num in lucky_num_list]
    return lucky_name_list


# 获取不重复cn列表
def GetCNList() -> list:
    db = merDB()
    cur = db.cur
    all_cn_list = []
    sql = """SELECT main_spelling, participation_in_splicing FROM products"""
    cur.execute(sql)
    existing_record = cur.fetchall()
    main_sqelling_list = [item[0] for item in existing_record]
    participation_in_splicing_list = [item[1] for item in existing_record]
    for participation_in_splicing in participation_in_splicing_list:
        cn_list = participation_in_splicing.split("，")
        for cn in cn_list:
            cn = cn.strip()
            if cn not in all_cn_list:
                all_cn_list.append(cn)
    for cn in main_sqelling_list:
        cn = cn.strip()
        if cn not in all_cn_list:
            all_cn_list.append(cn)
    return all_cn_list


# 年度报告
@on_command("年度报告", only_to_me=True, permission=lambda sender: sender.is_superuser)
async def YearReport(session: CommandSession):
    result_dict, _, _, _ = YearReportCount()
    await session.send('新年新气象，新年的夜宵更是令人回味无穷！在这个既是举国欢庆，又是夜宵诞生一周年的日子里，我们欢聚一堂，共同回顾我们在夜宵吃谷的点点滴滴。接下来我们将看到在这过去的一年里，夜宵众人创造了多少的奇迹，然后祝愿我们在新的一年里也能再接再厉，继续发挥明知山有穷偏向谷山行的精神！')
    time.sleep(5)
    await session.send('首先我们能看到的是——夜宵的年度总结！')
    time.sleep(1)
    text = f"在过去的一年内夜宵总共切煤数达到了{result_dict['总切煤数']}次，其金额更是高达{result_dict['总金额']}元，再创历史新高！哦对我们没有历史，那我们现在就是在创造历史！"
    await session.send(text)
    time.sleep(5)
    text = f"承蒙yhm的溺爱，夜宵切煤总重量达到{result_dict['总重量']}克！\n在这份重量级的成就之中又暗藏了多少人心酸的泪水和干瘪的钱包呢，这我们不得而知，我们在此对那些幸运儿表示由衷的祝福。"
    await session.send(text)
    time.sleep(5)
    text = f"回望夜宵初建，从一开始的十几人到现在的将近500，有些人是开朝老将，有些人是新生血液，有些人半途离开，有些人坚守到了现在。在这一年里夜宵切煤的总人数达到{result_dict['总人数']}人，总人次达到{result_dict['总人次']}次，{result_dict['拼盘数']}次的拼盘数。"
    await session.send(text)
    time.sleep(5)
    text = f"虽然在其中由于种种不幸夜宵的异常数字有{result_dict['异常数']}之多，但是塞翁失马焉知祸福，祝飞来钱财使我们吃到更好价的谷子！"
    await session.send(text)
    time.sleep(5)
    await session.send("祝夜宵在新的一年里再接再厉，再创辉煌，争取总有一天总人数和吃谷人数呈1：1，造就佳话。")
    time.sleep(1)
    await session.send('噫！你中了！现在向我们走来的是这一年茫茫吃谷路中脱颖而出的健儿。')
    time.sleep(5)
    text = f"个切之王——{result_dict['个切cn']}！\n个切总数共{result_dict['个切最多']}次，你指尖的m码是我们的信仰，你不断送切的身影照亮了夜宵的黑暗，你从未说过停谷也从未停下入侵yhm谷圈的步伐，你，就是我们的榜样！祝{result_dict['个切cn']}新的一年里再接再厉，勇切新高！"
    await session.send(text)
    time.sleep(5)
    text = f"开盘界の盘古——{result_dict['开盘cn']}！\n2024年你一共开了{result_dict['开盘最多']}个拼盘。盘古开天地你开谷盘，感谢你在包尾推不出去、先切后拼没人吃、疯狂推车没人理、打表收肾地狱、好不容易拼成结果慢人一步独守sold房的世道还有一颗坚定不移的开盘精神。加油，到现在还在开盘的人，做什么都会成功的.jpg"
    await session.send(text)
    time.sleep(5)
    text = f"参盘冲锋兵——{result_dict['参与拼盘cn']}！既然你诚心诚意的发问了，我就大发慈悲的告诉你，为了防止大盘被抢sold，为了盘主的钱包，贯彻停谷与我凹的有机统一，可爱又迷人的吃谷角色，{result_dict['参与拼盘cn']}！2024年一共参与了{result_dict['参与拼盘最多']}个拼盘。ta是穿梭在夜宵救人于水火的天使，停谷的明天在等著ta！"
    await session.send(text)
    time.sleep(5)
    await session.send('我们要以这些群友为榜样，努力赚钱，努力吃谷，做自推的ATM机，我们都有美好的未来！')
    time.sleep(1)
    await session.send(f'本报告系自动统计生成。文案撰写：Yan')


# 年度报告实现
def YearReportCount() -> dict:
    result_dict = dict()
    # 连接数据库
    db = merDB()
    cur = db.cur
    # 查询数据
    # 总切煤数
    sql = """SELECT COUNT(*) FROM products"""
    cur.execute(sql)
    total_num = cur.fetchone()[0]
    result_dict["总切煤数"] = total_num
    # 总金额
    sql = """SELECT SUM(price) FROM products"""
    cur.execute(sql)
    total_price = cur.fetchone()[0]
    result_dict["总金额"] = total_price
    # 总重量
    sql = """SELECT SUM(weight) FROM products"""
    cur.execute(sql)
    total_weight = cur.fetchone()[0]
    result_dict["总重量"] = total_weight
    # 总人数
    result_dict["总人数"] = len(GetCNList())
    # 总人次
    sql = """SELECT main_spelling, participation_in_splicing FROM products"""
    cur.execute(sql)
    existing_record = cur.fetchall()
    main_sqelling_list = [item[0] for item in existing_record]
    participation_in_splicing_list = [item[1] for item in existing_record]
    total_people_count = len(main_sqelling_list)
    for list in participation_in_splicing_list:
        if list == "":
            continue
        total_people_count += len(list.split("，"))
    result_dict["总人次"] = total_people_count
    # 拼盘数
    sql = """SELECT COUNT(*) FROM products WHERE participation_in_splicing != '，'"""
    cur.execute(sql)
    splicing_count = cur.fetchone()[0]
    result_dict["拼盘数"] = splicing_count
    # 异常数(状态栏是异常)
    sql = """SELECT COUNT(status) FROM products WHERE status = '异常'"""
    cur.execute(sql)
    abnormal_count = cur.fetchone()[0]
    result_dict["异常数"] = abnormal_count
    # 个切(participation_in_splicing为空的且main_spelling出现的名字按次数排序)
    sql = """SELECT main_spelling, COUNT(*) FROM products WHERE participation_in_splicing = '，' GROUP BY main_spelling ORDER BY COUNT(*) DESC"""
    cur.execute(sql)
    list1 = cur.fetchall()
    max_name = list1[0][0]
    max_num = list1[0][1]
    result_dict["个切cn"] = max_name
    result_dict["个切最多"] = max_num
    # 开盘最多(participation_in_splicing不为空且main_spelling出现的名字按次数排序)
    sql = """SELECT main_spelling, COUNT(*) FROM products WHERE participation_in_splicing != '，' GROUP BY main_spelling ORDER BY COUNT(*) DESC"""
    cur.execute(sql)
    list2 = cur.fetchall()
    max_name = list2[0][0]
    max_num = list2[0][1]
    result_dict["开盘cn"] = max_name
    result_dict["开盘最多"] = max_num
    # 参与拼盘最多(participation_in_splicing中出现最多的名字)
    sql = """SELECT participation_in_splicing FROM products"""
    cur.execute(sql)
    splicing_list = cur.fetchall()
    all_cn_list = []
    for item in splicing_list:
        cn_list = item[0].split("，")
        for cn in cn_list:
            if cn == "":
                continue
            all_cn_list.append(cn)
    # 统计all_cn_list中出现cn出现的次数
    list3 = dict()
    for cn in all_cn_list:
        if cn not in list3:
            list3[cn] = 1
        else:
            list3[cn] += 1
    list3 = sorted(list3.items(), key=lambda item: item[1], reverse=True)
    max_name = list3[0][0]
    max_num = list3[0][1]
    result_dict["参与拼盘cn"] = max_name
    result_dict["参与拼盘最多"] = max_num
    return result_dict, list1, list2, list3


# 个人报告
@on_command("个人报告", only_to_me=False)
async def PersonalReport(session: CommandSession):
    #只允许私聊
    if session.event.message_type == "group":
        return
    #获取cn
    cn = session.current_arg_text.strip()
    cn = cn.lower()
    #鉴权
    bot = nonebot.get_bot()
    group_id = 937806799
    user_id = session.event.user_id
    result = await bot.get_group_member_info(group_id=group_id, user_id=user_id)
    nickname = result['card']
    if cn not in nickname and user_id != 501079827:
        await session.send("你没有权限查看该用户的个人报告\n请重新发送或联系管理员")
        return
    #获取报告
    result_dict = PersonalReportCount(cn)
    await session.send('你好，这是你的报告')
    time.sleep(1)
    text = f'今年你一共切了{result_dict["总切煤数"]}次煤，超越夜宵100%的人，你就是自己的切煤之星！'
    await session.send(text)
    time.sleep(3)
    text = f'在这之中，你总共有{result_dict["个切数"]}次自切，{result_dict["开盘数"]}次开盘，一共参与了{result_dict["参与拼盘数"]}个盘。'
    await session.send(text)
    time.sleep(3)
    text = f'拜阴花妹和瓜仁所赐，你今年有{result_dict["异常数"]}个异常，希望2025年能对你好一些。'
    await session.send(text)
    time.sleep(3)
    text = f'今年你给自推花了{result_dict["个切总金额"]}+元。自推的财布非你莫属！'
    await session.send(text)
    time.sleep(3)
    await session.send('祝你在新的一年里切得更好，吃得更香，2025年，夜宵继续与我们同在！')
    time.sleep(1)
    await session.send(f'本报告系自动统计生成，仅供娱乐使用，不对其真实性负责。文案：Yan')
    


# 个人报告实现
def PersonalReportCount(cn: str) -> dict:
    # 总切煤数、个切数、开盘数、参与拼盘数、异常数
    result_dict = dict()
    # 连接数据库
    db = merDB()
    cur = db.cur
    # 查询数据
    # 总切煤数(main_spelling等于cn或participation_in_splicing中包含cn的)
    sql = """SELECT COUNT(*) FROM products WHERE main_spelling = ? OR participation_in_splicing LIKE ?"""
    cur.execute(sql, (cn, f"%{cn}，%"))
    total_num = cur.fetchone()[0]
    result_dict["总切煤数"] = total_num
    # 个切数(participation_in_splicing为空的且main_spelling等于cn)
    sql = """SELECT COUNT(*) FROM products WHERE participation_in_splicing = '，' AND main_spelling = ?"""
    cur.execute(sql, (cn,))
    single_num = cur.fetchone()[0]
    result_dict["个切数"] = single_num
    # 开盘数(participation_in_splicing不为空且main_spelling等于cn)
    sql = """SELECT COUNT(*) FROM products WHERE participation_in_splicing != '，' AND main_spelling = ?"""
    cur.execute(sql, (cn,))
    open_num = cur.fetchone()[0]
    result_dict["开盘数"] = open_num
    # 参与拼盘数(participation_in_splicing中包含cn)
    sql = """SELECT COUNT(*) FROM products WHERE participation_in_splicing LIKE ?"""
    cur.execute(sql, (f"%{cn}，%",))
    splicing_num = cur.fetchone()[0]
    result_dict["参与拼盘数"] = splicing_num
    # 异常数(main_spelling等于cn或participation_in_splicing中包含cn的且status等于异常)
    sql = """SELECT COUNT(*) FROM products WHERE (main_spelling = ? OR participation_in_splicing LIKE ?) AND status = '异常'"""
    cur.execute(sql, (cn, f"%{cn}，%"))
    abnormal_num = cur.fetchone()[0]
    result_dict["异常数"] = abnormal_num
    # 个切总金额(participation_in_splicing为空的且main_spelling等于cn)
    sql = """SELECT SUM(price) FROM products WHERE participation_in_splicing = '，' AND main_spelling = ?"""
    cur.execute(sql, (cn,))
    single_price = cur.fetchone()[0]
    result_dict["个切总金额"] = single_price
    return result_dict
