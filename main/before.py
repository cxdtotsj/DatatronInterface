'''
注册
'''

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
import json


class BeforeTest:
    def __init__(self):
        self.run_method = BaseMethod()
        self.opera_db = OperationDB()

    def send_code(self,mobile):
        api = "/api/v1/user/sendcode"
        data = {"mobile": mobile,
                "smsType": 2}
        self.run_method.post(api, data)

    def user_register(self):
        api = "/api/v1/user/register"
        mobile_list = [18321829313, 18317026527]
        for mobile in mobile_list:
            self.send_code(mobile)
            sql = '''SELECT template_param FROM base_message 
                        where phone_number = '{}'  ORDER BY create_at DESC;'''.format(mobile)
            code_str = self.opera_db.get_fetchone(sql)["template_param"]
            code = json.loads(code_str)["code"]
            print(code)
            data = {"mobile": mobile,
                    "code": int(code),
                    "password": "Password01!"}
            res = self.run_method.post(api, data).json()
            assert res["code"] == 1, "注册失败"


if __name__ == '__main__':
    before_test = BeforeTest()
    before_test.user_register()