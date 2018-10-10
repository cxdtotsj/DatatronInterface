import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
import base.setting


class OperationDB:

    def __init__(self):
        self.host = base.setting.db_host
        self.port = base.setting.db_port
        self.user = base.setting.db_user
        self.pwd = base.setting.db_password
        self.db_name = base.setting.db_db
        self.db = self.get_db()
        self.mycursor = self.get_cursor()

    def get_db(self):
        db = pymysql.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             password=self.pwd,
                             db=self.db_name,
                             charset="utf8",
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        return db

    # def get_db(self):
    #     db = pymysql.connect(host='10.241.11.7',
    #                          port=4000,
    #                          user='root',
    #                          password='pAssw0rd',
    #                          db='datatron',
    #                          charset="utf8",
    #                          autocommit=True,
    #                          cursorclass=pymysql.cursors.DictCursor)
    #     return db

    def get_cursor(self):
        mycursor = self.db.cursor()
        return mycursor

    # 获取行数
    def get_effect_row(self, sql, paramers=None):
        if paramers is None:
            effect_row = self.mycursor.execute(sql)
        else:
            effect_row = self.mycursor.execute(sql % paramers)
        return effect_row

    # 获取第一个返回结果
    def get_fetchone(self, sql, paramers=None):
        if paramers is None:
            self.mycursor.execute(sql)
        else:
            self.mycursor.execute(sql % paramers)
        row_one = self.mycursor.fetchone()
        return row_one

    # 获取指定返回结果
    def get_fetchmany(self, sql, n, paramers=None):
        if paramers is None:
            self.mycursor.execute(sql)
        else:
            self.mycursor.execute(sql % paramers)
        row_num = self.mycursor.fetchmany(n)
        return row_num

    # 获取全部返回结果
    def get_fetchall(self, sql, paramers=None):
        if paramers is None:
            self.mycursor.execute(sql)
        else:
            self.mycursor.execute(sql % paramers)
        row_all = self.mycursor.fetchall()
        return row_all

    # 更新数据
    def update_data(self, sql):
        try:
            self.mycursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("更新数据失败", e)

    # 插入数据，并返回自增id
    def insert_data(self, sql):
        try:
            self.mycursor.execute(sql)
            self.db.commit()
            last_id = self.mycursor.lastrowid
            return last_id
        except Exception as e:
            self.db.rollback()
            print("插入数据失败", e)

    # 删除数据
    def delete_data(self, sql):
        try:
            self.mycursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print("删除数据失败", e)

    # 关闭数据库连接
    def close_db(self):
        self.mycursor.close()


if __name__ == '__main__':
    dbdata = OperationDB()
    sql = '''select id from zone where status != 3;'''
    a = dbdata.get_effect_row(sql)
    print(a)