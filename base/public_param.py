'''
1.获取超级管理员token
'''
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from base.base_method import BaseMethod


class PublicParam:

    def __init__(self):
        self.run_method = BaseMethod()
        self.super_token = self.get_super_token()

    # 获取超级管理员(1 << 30) token
    def get_super_token(self):
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
                print("Super密码不匹配")
            elif err_code == 1404:
                print("Super用户不存在")
            elif err_code == 1426:
                print("Super密码需修改")
    
    # 超级管理员 (1 << 30) header
    def get_super_header(self):
        return {"Authorization":self.super_token}
    
    # 公司管理员 token
    def get_corp_token(self):
        api = "/user/login"
        data = {"email": "xdchenadmin@admin", 
                "password": 123456}
        res = self.run_method.post(api, data)
        res_dict = res.json()
        print(res_dict)
        if res.status_code == 200:
            token = res_dict["token"]
            return token
        elif res.status_code == 400:
            err_code = res_dict["code"]
            if err_code == 1401:
                print("Corp密码不匹配")
            elif err_code == 1404:
                print("Corp用户不存在")
            elif err_code == 1426:
                print("Corp密码需修改")
    
    # 公司管理员 header
    def get_corp_header(self):
        return {"Authorization":self.get_corp_token()}

    def get_code(self, res):
        '''获取错误code'''
        res_dict = res.json()
        result_code = res_dict["code"]
        return result_code 


if __name__ == "__main__":
    import time
    basedata = PublicParam()
    print(basedata.super_token)