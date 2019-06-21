import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from base.base_method import BaseMethod
from util.operation_db import OperationDB
from data.common import Common


class DataTest:
    def __init__(self):
        self.run_method = BaseMethod()
        # self.common = Common()
        # self.opera_db = OperationDB()
        # self.super_header = self.common.header_super()

    def login(self):
        api = '/user/login'
        data = {
            'email': "xdchenadmin@admin",
            "password": 12345678
        }
        res = self.run_method.post(api, data)
        print(res.json())


if __name__ == '__main__':
    t = DataTest()
    t.login()