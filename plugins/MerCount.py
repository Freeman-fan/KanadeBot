import sqlite3
import random

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
@on_command("年度报告", only_to_me=False, permission=lambda sender: sender.is_superuser)
async def YearReport(session: CommandSession):
    result_dict, list1, list2, list3 = YearReportCount()
    await session.send(
        "年度报告\n"
        + "\n".join([f"{key}：{value}" for key, value in result_dict.items()])
    )


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
    sql = """SELECT COUNT(*) FROM products WHERE participation_in_splicing != ''"""
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
    result_dict["个切"] = f"{max_name}，共{max_num}次"
    # 开盘最多(participation_in_splicing不为空且main_spelling出现的名字按次数排序)
    sql = """SELECT main_spelling, COUNT(*) FROM products WHERE participation_in_splicing != '，' GROUP BY main_spelling ORDER BY COUNT(*) DESC"""
    cur.execute(sql)
    list2 = cur.fetchall()
    max_name = list2[0][0]
    max_num = list2[0][1]
    result_dict["开盘最多"] = f"{max_name}，共{max_num}次"
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
    max_cn = list3[0][0]
    max_num = list3[0][1]
    result_dict["参与拼盘最多"] = f"{max_cn}，共{max_num}次"
    return result_dict, list1, list2, list3


# 个人报告
@on_command("个人报告", only_to_me=False)
async def PersonalReport(session: CommandSession):
    #只允许私聊
    if session.event.message_type == "group":
        return
    #获取cn
    cn = session.current_arg_text.strip()
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
    await session.send(
        f"{cn}个人报告\n"
        + "\n".join([f"{key}：{value}" for key, value in result_dict.items()])
    )
    await session.send(f'本报告系自动统计生成，仅供娱乐使用，不对其真实性负责')
    


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
    return result_dict
