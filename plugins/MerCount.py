import sqlite3
import random

from nonebot import on_command, CommandSession


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
                print(cn, 1)
                all_cn_list.append(cn)
    for cn in main_sqelling_list:
        cn = cn.strip()
        if cn not in all_cn_list:
            print(cn, 1)
            all_cn_list.append(cn)
    return all_cn_list


# 年度报告
@on_command("年度报告", only_to_me=False, permission=lambda sender: sender.is_superuser)
async def YearReport(session: CommandSession):
    result_dict = YearReportCount()
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
    # 个切最多(participation_in_splicing为空的且main_spelling出现最多的名字)
    sql = """SELECT main_spelling, COUNT(*) FROM products WHERE participation_in_splicing = '' GROUP BY main_spelling ORDER BY COUNT(*) DESC LIMIT 1"""
    cur.execute(sql)
    list = cur.fetchone()
    max_name = list[0]
    max_num = list[1]
    result_dict["个切最多"] = f"{max_name}，共{max_num}次"
    # 开盘最多(participation_in_splicing不为空且main_spelling出现最多的名字)
    sql = """SELECT main_spelling, COUNT(*) FROM products WHERE participation_in_splicing != '' GROUP BY main_spelling ORDER BY COUNT(*) DESC LIMIT 1"""
    cur.execute(sql)
    list = cur.fetchone()
    max_name = list[0]
    max_num = list[1]
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
    # 统计all_cn_list中出现次数最多的cn
    max_num = all_cn_list.count(max(set(all_cn_list), key=all_cn_list.count))
    max_cn = max(set(all_cn_list), key=all_cn_list.count)
    result_dict["参与拼盘最多"] = f"{max_cn}，共{max_num}次"
    return result_dict


# 个人报告
@on_command("个人报告", only_to_me=False)
async def PersonalReport(session: CommandSession):
    pass


# 个人报告实现
def PersonalReportCount(cn: str) -> dict:
    pass
