'''
1.获取测试用户、专家的 user_id 、 token
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB


class PublicParam:

    def __init__(self):
        self.run_method = BaseMethod()
        self.opera_db = OperationDB()
        self.token = self.get_token()[0]
        self.user_id = self.get_token()[1]

    # 获取测试用户的 user_id，token
    def get_token(self):
        api = "/api/v1/user/login"
        data = {"mobile": 18321829313, "password": "Password01!"}
        res = self.run_method.post(api, data)
        if res.status_code == 200:
            res_dict = res.json()
            try:
                self.token = res_dict["data"]["token"]
                self.user_id = res_dict["data"]["user_id"]
                return self.token, self.user_id
            except BaseException:
                print("用户名或验证码错误")
        else:
            print("服务器登陆失败")

    # 获取专家的user_id，token
    def get_expert_info(self):
        api = "/api/v1/user/login"
        data = {"mobile": 18317026527, "password": "Password01!"}
        res = self.run_method.post(api, data)
        if res.status_code == 200:
            res_dict = res.json()
            try:
                self.e_token = res_dict["data"]["token"]
                self.e_id = res_dict["data"]["user_id"]
                return self.e_token, self.e_id
            except BaseException:
                print("用户名或验证码错误")
        else:
            print("服务器登陆失败")

    # 获取用户id
    def get_id(self):
        sql = '''select id from zyt_user where user_id = '{}';'''.format(self.user_id)
        id = self.opera_db.get_fetchone(sql)["id"]
        return id


if __name__ == "__main__":
    import time
    basedata = PublicParam()
    eid = basedata.get_id()
    print(eid)
