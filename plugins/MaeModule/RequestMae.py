import requests
import sqlite3
from sqlite3 import Error as DatabaseError
import time


# 类：抓取
class RequestMae:
    def __init__(
        self,
        name: str,
        target_type: str,
        target_id: list,
        keyword: list,
        priceMin: int,
        priceMax: int,
        inuse: bool,
    ):
        self.name = name
        self.target_type = target_type
        self.target_id = target_id
        self.keyword = keyword
        self.priceMin = priceMin
        self.priceMax = priceMax
        self.inuse = inuse
        self.data = {
            "keyword": keyword,
            "itemConditionId": None,
            "page": "1",
            "categoryId": [],
            "sort": 1,
            "status": ["1"],
            "priceMin": priceMin,
            "priceMax": priceMax,
            "shippingPayerId": [],
            "shippingMethod": [],
            "order": "",
        }
        self.Create_Database()
        self.Getdata()
        self.Initialize_Database()

    # 创建数据库
    def Create_Database(self):
        # 新建数据库
        try:
            db_path = f"{self.name}.db"
            conn = sqlite3.connect(db_path)
            self.db_path = db_path
            self.conn = conn
        except DatabaseError as e:
            print(f"创建数据库错误：{str(e)}")
        # 创建表
        try:
            sql_create_table = """
            CREATE TABLE IF NOT EXISTS items(
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
        except DatabaseError as e:
            print(f"创建表错误：{str(e)}")

    # 获取数据
    def Getdata(self):
        response = self.RequesePost()
        if response.status_code == 200:
            sql_add_item = """
            INSERT OR IGNORE INTO items (mNum, status, name, jpprice, firstPhoto, isSand) VALUES (?, ?, ?, ?, ?, ?);
            """
            data = response.json()
            for item in data["data"]["list"]:
                mNum = item["id"]
                status = item["status"]
                name = item["name"]
                jpprice = item["price"]
                firstphoto = item["thumbnails"][0]
                try:
                    cur = self.conn.cursor()
                    cur.execute(
                        sql_add_item, (mNum, status, name, jpprice, firstphoto, 0)
                    )
                    self.conn.commit()
                except DatabaseError as e:
                    print(f"写入数据库错误：{str(e)}")
                finally:
                    if cur:
                        cur.close()

    # 初始化数据库
    def Initialize_Database(self):
        try:
            conn = self.conn
            cur = conn.cursor()
            sql = f"UPDATE items SET isSand = 1"
            cur.execute(sql)
            conn.commit()
        except DatabaseError as e:
            print(f"初始化数据库错误：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 网络请求
    def RequesePost(self):
        url = "https://www.maetown.cn/Mobile/Mercari/SearchV3"
        data = self.data
        response = requests.post(url, data=data)
        return response


