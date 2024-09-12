import sqlite3
from sqlite3 import Error as DatabaseError

from plugins.MaeModule.GetMerItem import GetMerItem


class GetMerUpdate:
    def __init__(self, db_path=f".\DataBase\mer_updata.db"):
        try:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn = conn
        except DatabaseError as e:
            print(f"创建数据库错误：{str(e)}")
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS itmes(
                mNum TEXT PRIMARY KEY,
                status INTEGER,
                name TEXT,
                jpprice INTEGER,
                commentNum INTEGER,
                id INTEGER
            );
            """
            cur = conn.cursor()
            cur.execute(sql)
        except DatabaseError as e:
            print(f"创建表错误：{str(e)}")

    # 添加新的监控对象
    def AddItem(self, mNum, id):
        _, name, _, jpprice, _, status, _, comment_list = GetMerItem(mNum=mNum)
        commentNum = len(comment_list)

        sql = """
        INSERT INTO items (mNum, status, name, jpprice, commentNum, ID)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            cur = self.conn.cursor()
            # 执行 SQL 语句
            cur.execute(sql, (mNum, status, name, jpprice, commentNum, id))
            # 提交事务
            self.conn.commit()
            return True
        except DatabaseError as e:
            print(f"AddItem添加记录错误: {str(e)}")
            return False
        finally:
            if cur:
                cur.close()

    # 删除监控对象
    def DelItem(self, mNum, id):
        try:
            sql = """
            DELETE FROM items WHERE mNum = ? AND id = ?
            """
            cur = self.conn.cursor()
            cur.execute(sql, (mNum, id))
            self.conn.commit()
            if cur.rowcount == 0:
                return False
            else:
                return True
        except DatabaseError as e:
            print(f"DelItem删除记录错误：{str(e)}")
            return False
        finally:
            if cur:
                cur.close()

    # 查询有多少个对象
    def GetItemNum(self, id):
        try:
            sql = """
            SELECT COUNT(*) FROM items WHERE id = ?
            """
            cur = self.conn.cursor()
            cur.execute(sql, (id,))
            result = cur.fetchone()
            item_count = result[0]
            return item_count
        except DatabaseError as e:
            print(f"GetItemNum查询错误：{str(e)}")
            return None
        finally:
            if cur:
                cur.close()

    # 查询某个对象的属性
    def GetItemInfo(self, mNum):
        try:
            sql = """
            SELECT mNum, name, jpprice, status, commentNum FROM items WHERE mNum = ?
            """
            cur = self.conn.cursor()
            cur.execute(sql, (mNum,))
            result = cur.fetchone()
            if result:
                return {
                    "mNum": result[0],
                    "name": result[1],
                    "jpprice": result[2],
                    "status": result[3],
                    "commentNum": result[4],
                }
            else:
                return None
        except DatabaseError as e:
            print(f"GetItemInfo查询错误：{str(e)}")
            return None
        finally:
            if cur:
                cur.close()

    # 更新某个对象的某个值
    def UpdataItem(self, mNum, field, value):
        try:
            sql = f"""
            UPDATE items SET {field} = ? WHERE mNum = ?
            """
            cur = self.conn.cursor()
            cur.execute(sql, (value, mNum))
            self.conn.commit()
            if cur.rowcount == 0:
                return False
            else:
                return True
        except DatabaseError as e:
            print(f"UpdataItem更新错误：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 获取所有值的mNum
    def GetAllmNum(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT mNum FROM items")
            mNums = cur.fetchall()
            return [mNum[0] for mNum in mNums]
        except DatabaseError as e:
            print(f"GetAllmNum查询错误：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 获取m码下对应的id
    def GetID(self, mNum):
        try:
            sql = """SELECT id FROM items WHERE mNum = ?"""
            cur = self.conn.cursor()
            result = cur.fetchone()
            if result:
                return result
            else:
                return None
        except DatabaseError as e:
            print(f'GetID查询错误：{str(e)}')

