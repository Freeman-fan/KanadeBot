import requests
import time
import sqlite3
from sqlite3 import Error


# 类：请求mae数据
class RequestMae:
    def __init__(self, keyword="", minprice="", maxprice=""):
        self.data = {
            "keyword": keyword,
            "itemConditionId": None,
            "page": "1",
            "categoryId": [],
            "sort": 1,
            "status": ["1"],
            "priceMin": minprice,
            "priceMax": maxprice,
            "shippingPayerId": [],
            "shippingMethod": [],
            "order": "",
        }

    def GetGoods(self):
        url = "https://www.maetown.cn/Mobile/Mercari/SearchV3"
        data = self.data
        response = requests.post(url, data=data)
        return response


# 新建数据库
def create_db_and_table(conn):
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS items (
            mNum TEXT PRIMARY KEY,
            status INTEGER,  
            name TEXT,
            jpprice INTEGER,
            firstPhoto TEXT,
            isSand INTEGER
        );
        """
        cur = conn.cursor()
        cur.execute(sql_create_table)
    except Error as e:
        print(e)


# 连接到数据库
def create_connection(db_file):
    """创建数据库连接"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


# 写入数据库
def add_item(conn, m_num, status, name, jpprice, firstPhoto, issand="0"):
    sql_add_item = """
    INSERT OR IGNORE INTO items (mNum, status, name, jpprice, firstPhoto, isSand) VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        # 使用cursor()方法获取操作游标
        cur = conn.cursor()
        # 执行SQL插入语句
        cur.execute(sql_add_item, (m_num, status, name, jpprice, firstPhoto, issand))
        # 提交事务
        conn.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        # 关闭游标
        if cur:
            cur.close()


# 清空数据库
def clear_table_data(conn):
    try:
        sql_clear_table = "DELETE FROM items;"
        conn.cursor().execute(sql_clear_table)
    except Error as e:
        print(e)


# 解析json并写入数据库
def ProcessJson(conn, data):
    # 对数据进行分析或处理
    for item in data["data"]["list"]:
            m_num = item["id"]
            status = item["status"]
            name = item["name"]
            jpprice = item["price"]
            firstphoto = item["thumbnails"][0]
            # insert_sql = """
            #     INSERT INTO items (mNum, status, name, jpprice, firstPhoto) VALUES (?, ?, ?, ?, ?);
            #     """
            # 执行插入操作
            add_item(
                conn,
                m_num=m_num,
                status=status,
                name=name,
                jpprice=jpprice,
                firstPhoto=firstphoto,
                issand=0,
            )
            # conn.commit()

# 发送记录(这个代码应该集成到bot里面，但先放在这里)
def update_and_print_records(conn):
    try:
        # 查询所有isSand值为0的记录
        cur = conn.cursor()
        cur.execute("SELECT * FROM items WHERE isSand = 0")
        # 遍历查询结果
        for row in cur.fetchall():
            m_num, status, name, jpprice, firstPhoto, isSand = row
            if isSand == 0:
                # 打印记录
                print(f" {m_num}, {name}, {jpprice}")
                # 更新isSand值为1
                update_sql = "UPDATE items SET isSand = 1 WHERE mNum = ?"
                cur.execute(update_sql, (m_num,))
        # 提交事务
        conn.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if cur:
            cur.close()


# 主程序入口
if __name__ == "__main__":
    # 初始化数据库
    database_file = "MerGoods.db"
    conn = create_connection(database_file)
    create_db_and_table(conn)
    clear_table_data(conn)
    # 测试：进行一次请求并写入数据库
    for i in range(99999):
        request_pjsk = RequestMae("プロセカ")
        response_pjsk = request_pjsk.GetGoods()
        if response_pjsk.status_code == 200:
            # 解析返回的JSON数据
            data = response_pjsk.json()
            ProcessJson(conn, data)
        else:
            print("Failed to retrieve data:", response_pjsk.status_code)
        update_and_print_records(conn)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}：成功执行")
        time.sleep(1)
