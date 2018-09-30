'''
1.获取超级管理员token
'''
import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_method import BaseMethod
from util.operation_json import OperetionJson
import random


class PublicParam:

    def __init__(self):
        self.run_method = BaseMethod()
        self.super_token = self.get_super_token()
        self.opera_json = OperetionJson()

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
                "password": 12345678}
        res = self.run_method.post(api, data)
        res_dict = res.json()
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

    # 获取错误码
    def get_code(self, res):
        res_dict = res.json()
        result_code = res_dict["code"]
        return result_code
    
    # 获取request_id
    def get_request_id(self,res):
        return "X-Request-Id : %s" %res.headers["X-Request-Id"]
    
    # 创建用户，可选择是否绑定到组，是否有管理员权限
    def common_user(self, corp_id, role=None):
        # 新增用户
        user_api = '/user/create'
        random_email = "rd{}@random.com".format(random.randint(100000,999999))
        user_data = {"email":random_email,
                            "name":"随机生成的用户",
                            "password":123456}
        user_resopnse = self.run_method.post(user_api,user_data,headers=self.get_super_header())
        if user_resopnse.status_code is not 200:
            print("用户新增失败")
            print(user_resopnse.json())
        user_id = user_resopnse.json()["id"]

        # 用户绑定到组织
        user_corp_api = '/corp/user/add'
        if role is not None:
            user_corp_data = {"user_id":user_id,
                                "corp_id":corp_id,
                                "role":role}
        else:
            user_corp_data = {"user_id":user_id,
                                "corp_id":corp_id}
        userCorp_response = self.run_method.post(user_corp_api,user_corp_data,headers=self.get_super_header())
        if userCorp_response.status_code is not 200:
            print("用户绑定到公司失败")
            print(userCorp_response.json())
        return user_id
    
    # 将用户从组织删除
    def user_corp_del(self,user_id,corp_id=None):
        del_api = "/corp/user/del"
        if corp_id is not None:
            data = {"corp_id":corp_id,
                    "user_id":user_id}
            del_response = self.run_method.post(del_api,data,headers=self.get_super_header())
        else:
            data = {"user_id":user_id}
            del_response = self.run_method.post(del_api,data,headers=self.get_corp_header())
        if del_response.status_code is not 200:
            print("用户新增失败")
            print(del_response.json())



if __name__ == "__main__":
    import time
    basedata = PublicParam()
    basedata.user_corp_del("110082450750714413")