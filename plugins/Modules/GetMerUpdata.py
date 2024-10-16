from typing import Union
import sqlite3
from sqlite3 import Error as DatabaseError

from plugins.CustomClass.response import FuncResponse
from plugins.Modules.GetMerItem import GetMerItem


class UpdateResponse:
    def __init__(self, updateId: int, mNum: int, oldData: str, newData: str, id: str):
        self.mNum = mNum
        self.updateId = updateId
        self.oldData = oldData
        self.newData = newData
        self.id = id


class GetMerUpdate:
    def __init__(self, db_path=f".\DataBase\merUpdata.db"):
        try:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn = conn
        except DatabaseError as e:
            print(f"创建数据库错误：{str(e)}")
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS items(
                mNum TEXT PRIMARY KEY,
                status INTEGER,
                name TEXT,
                jpprice INTEGER,
                commentNum INTEGER,
                id TEXT
            );
            """
            cur = conn.cursor()
            cur.execute(sql)
        except DatabaseError as e:
            print(f"创建表错误：{str(e)}")

    # 添加新的监控对象
    async def AddItem(self, mNum: str, id: str):
        cur = self.conn.cursor()
        # 检查对象是否已存在
        cur.execute("SELECT * FROM items WHERE mNum = ?", (mNum,))
        existing_record = cur.fetchone()
        if existing_record:
            # 存在，更新id
            cur.execute("SELECT id FROM items WHERE mNum = ?", (mNum,))
            existing_record = cur.fetchone()
            if id in existing_record[0]:
                return FuncResponse(1, "添加失败。请勿重复添加")
            else:
                id = f"{existing_record[0]}{id} "
                cur.execute("UPDATE items SET id = ? WHERE mNum=?", (id, mNum))
                self.conn.commit()
        elif existing_record == None:
            # 不存在，添加记录
            meritem = await GetMerItem(mNum=mNum)
            if meritem.response_code == 1:
                return FuncResponse(1, f"添加失败。\n{meritem.response_data}")
            elif meritem.response_code == 0:
                commentNum = len(meritem.comment_list)
                sql = """
                    INSERT INTO items(mNum, status, name, jpprice, commentNum, ID)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """
                try:
                    id += " "
                    cur.execute(
                        sql,
                        (
                            meritem.product_id,
                            meritem.product_status,
                            meritem.product_name,
                            meritem.product_price,
                            commentNum,
                            id,
                        ),
                    )
                    self.conn.commit()
                except DatabaseError as e:
                    print(f"AddItem添加记录错误: {str(e)}")
                    return FuncResponse(1, f"添加失败。\n{str(e)}")
                finally:
                    if cur:
                        cur.close()
        return FuncResponse(0, "添加成功")

    # 删除监控对象
    def DelItem(self, mNum: str, id: str) -> FuncResponse:
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id FROM items WHERE mNum = ?", (mNum,))
            existing_record = cur.fetchone()
            if existing_record == None:
                # 返回id为空
                return FuncResponse(1, "删除失败：未找到记录")
            elif existing_record:
                ids = existing_record[0].split()
                if id not in ids:
                    # 返回id中不存在指定id
                    return FuncResponse(1, "删除失败：未找到记录")
                ids.remove(id)
                if len(ids) == 0:
                    # 删除后剩余id数量为0
                    cur.execute("DELETE FROM items WHERE mNum = ?", (mNum,))
                    self.conn.commit()
                else:
                    new_ids = ""
                    for id in ids:
                        new_ids += f"{id} "
                    cur.execute(
                        "UPDATE items SET id = ? WHERE mNum = ?", (new_ids, mNum)
                    )
                    self.conn.commit()
                return FuncResponse(0, "删除成功")
        except Exception as e:
            print(f"DelItem删除记录错误：{str(e)}")
            return FuncResponse(1, f"删除失败：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 查询id下所有监控对象
    def GetIdItem(self, id: str) -> FuncResponse:
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT mNum FROM items WHERE id LIKE ?", ("%" + id + "%",))
            existing_record = cur.fetchall()
            if existing_record == []:
                return FuncResponse(1, "查询失败：您没有监控对象")
            elif existing_record:
                mNums = []
                for record in existing_record:
                    mNums.append(record[0])
                return FuncResponse(0, mNums)
        except Exception as e:
            return FuncResponse(1, f"查询失败：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 查询id下监控对象数量
    def GetIdItemNum(self, id: str) -> FuncResponse:
        try:
            getIdItem = self.GetIdItem(id)
            if getIdItem.response_code == 1:
                return FuncResponse(1, getIdItem.response_data)
            elif getIdItem.response_code == 0:
                itemNum = len(getIdItem.response_data)
                return FuncResponse(0, itemNum)
        except Exception as e:
            return FuncResponse(1, f"查询失败：{str(e)}")

    # 查询对象的属性
    async def GetItemInfo(self, mNum: str) -> FuncResponse:
        try:
            sql = """
            SELECT mNum, name, jpprice, status, commentNum FROM items WHERE mNum = ?
            """
            cur = self.conn.cursor()
            cur.execute(sql, (mNum,))
            result = cur.fetchone()
            if result:
                data = {
                    "mNum": result[0],
                    "name": result[1],
                    "jpprice": result[2],
                    "status": result[3],
                    "commentNum": result[4],
                }
                return FuncResponse(0, data)
            else:
                merItem = await GetMerItem(mNum=mNum)
                if merItem.response_code == 0:
                    data = {
                        "mNum": merItem.product_id,
                        "name": merItem.product_name,
                        "jpprice": merItem.product_price,
                        "status": merItem.product_status,
                        "commentNum": len(merItem.comment_list),
                    }
                    return FuncResponse(0, data)
                elif merItem.response_code == 1:
                    return FuncResponse(1, f"查询失败：{merItem.response_data}")
        except Exception as e:
            return FuncResponse(1, f"查询失败：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 更新某个对象的某个值
    def UpdataItem(self, mNum: str, field: str, value: str) -> bool:
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

    # 查找所有更新并更新数据库
    async def GetAllUpdate(self) -> FuncResponse:
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT mNum, name, jpprice, status, commentNum, id FROM items")
            result = cur.fetchall()
            if result:
                updateGroup = []
                for item in result:
                    mNum = item[0]
                    merItem = await GetMerItem(mNum=mNum)
                    if item[1] != merItem.product_name:
                        updateResponse = UpdateResponse(
                            1, mNum, item[1], merItem.product_name, item[5]
                        )
                        updateGroup.append(updateResponse)
                        self.UpdataItem(mNum, "name", merItem.product_name)
                    elif item[2] != merItem.product_price:
                        updateResponse = UpdateResponse(
                            2, mNum, item[2], int(merItem.product_price), item[5]
                        )
                        updateGroup.append(updateResponse)
                        self.UpdataItem(mNum, "jpprice", merItem.product_price)
                    elif item[3] != merItem.product_status:
                        updateResponse = UpdateResponse(3, mNum, None, None, item[5])
                        updateGroup.append(updateResponse)
                        # 状态变动唯一可能就是售出，因此直接删除
                        cur.execute("DELETE FROM items WHERE mNum = ?", (mNum,))
                        self.conn.commit()
                    elif item[4] != len(merItem.comment_list):
                        updateResponse = UpdateResponse(
                            4, mNum, None, merItem.comment_list[0], item[5]
                        )
                        updateGroup.append(updateResponse)
                        self.UpdataItem(mNum, "commentNum", len(merItem.comment_list))
                if updateGroup != []:
                    return FuncResponse(0, updateGroup)
                else:
                    return FuncResponse(-1, "没有更新")
            else:
                return FuncResponse(-1, "没有更新")
        except Exception as e:
            print(e)
            return FuncResponse(1, f"查找更新失败：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 获取所有值的mNum
    def GetAllmNum(self) -> FuncResponse:
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT mNum FROM items")
            result = cur.fetchall()
            mNums = []
            for item in result:
                mNums.append(item[0])
            return FuncResponse(0, mNums)
        except Exception as e:
            return FuncResponse(1, f"查询失败：{str(e)}")
        finally:
            if cur:
                cur.close()

    # 获取m码下对应的id
    def GetmNumID(self, mNum: str) -> FuncResponse:
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id FROM items WHERE mNum = ?", (mNum,))
            result = cur.fetchone()
            if result:
                return FuncResponse(0, result[0])
            else:
                return FuncResponse(1, "未查询到记录")
        except DatabaseError as e:
            print(f"GetID查询错误：{str(e)}")
            return FuncResponse(1, f"查询失败：{str(e)}")
