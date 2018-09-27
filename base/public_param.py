'''
1.获取超级管理员token
'''
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from base.base_method import BaseMethod
from util.operation_db import OperationDB


class PublicParam:

    def __init__(self):
        self.run_method = BaseMethod()
        self.opera_db = OperationDB()
        self.token = self.get_token()

    # 获取超级管理员(1 << 30) token
    def get_token(self):
        api = "/user/login"
        data = {"email": "admin@admin", 
                "password": "abc123"}
        res = self.run_method.post(api, data)
        res_dict = res.json()
        if res.status_code == 200:
            token = res_dict["token"]
            return token
        elif res.status_code == 400:
            err_code = res_dict["code"]
            if err_code == 1401:
                print("密码不匹配")
            elif err_code == 1404:
                print("用户不存在")
            elif err_code == 1426:
                print("密码需修改")
    
    def get_base_header(self):
        return {"Authorization":self.token}
         
    def get_code(self, res):
        '''获取错误code'''
        res_dict = res.json()
        result_code = res_dict["code"]
        return result_code 


if __name__ == "__main__":
    import time
    basedata = PublicParam()
    token = basedata.get_token()
    print(token)
    time.sleep(3)
    header = basedata.get_base_header()
    print(header)
