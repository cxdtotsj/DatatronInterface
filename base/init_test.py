'''
初始化
'''

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from base.base_method import BaseMethod
from util.operation_json import OperetionJson
from base.public_param import PublicParam


class InitTest:
    def __init__(self):
        self.run_method = BaseMethod()
        self.opera_json = OperetionJson()
        self.pub_param = PublicParam()
        self.super_header = self.pub_param.get_super_header()

    # 创建公司、用户、并绑定用户到公司
    def user_corp_add(self):
        # 新增用户
        createUser_api = '/user/create'
        createUser_data = {"email":"test10@admin",
                            "name":"测试管理员初始化勿删",
                            "password":123456}
        user_resopnse = self.run_method.post(createUser_api,createUser_data,headers=self.super_header)
        if user_resopnse.status_code is not 200:
            print("用户新增失败")
            print(user_resopnse.json())
        user_id = user_resopnse.json()["id"]
        self.opera_json.check_json_value("user_corp_add",{"user_id":user_id})

        # 修改密码
        userReset_api = '/user/passwd/reset'
        userReset_data = {"email":"test10@admin",
                            "password":123456,
                            "newpasswd":12345678}
        reset_response = self.run_method.post(userReset_api,userReset_data)
        if reset_response.status_code is not 200:
            print("新用户修改密码失败")
            print(reset_response.json())

        # 新增公司
        createCorp_api = '/corp/create'
        createCorp_data = {"name":"测试公司初始化勿删13"}
        corp_response = self.run_method.post(createCorp_api,createCorp_data,headers=self.super_header)
        if corp_response.status_code is not 200:
            print("公司新增失败")
            print(corp_response.json())
        corp_id = corp_response.json()["id"]
        self.opera_json.check_json_value("user_corp_add",{"user_id":user_id,"corp_id":corp_id})

        # 将用户绑定到组
        user_corp_api = '/corp/user/add'
        user_corp_data = {"user_id":user_id,
                            "corp_id":corp_id,
                            "role":524288}
        userCorp_response = self.run_method.post(user_corp_api,user_corp_data,headers=self.super_header)
        if userCorp_response.status_code is not 200:
            print("用户绑定到公司失败")
            print(userCorp_response.json())
        


if __name__ == '__main__':
    init = InitTest()
    init.user_corp_add()