'''
初始化
'''

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from base.base_method import BaseMethod
from util.operation_db import OperationDB
from data.common import Common



class InitTest:
    def __init__(self):
        self.run_method = BaseMethod()
        self.common = Common()
        self.opera_db = OperationDB()
        self.super_header = self.common.header_super()
    
    # 创建用户
    def user_create(self,name,password,email=None,mobile=None):
        """创建用户"""
        api = '/user/create'
        data = {
            "email": email,
            "mobile": mobile,
            "name": name,
            "password": password
        }
        try:
            res = self.run_method.post(api,data, headers=self.super_header)
            res.raise_for_status()
            print("用户: {} 创建成功!".format(name))
            return res.json()["id"]
        except:
            print("重置密码失败")
            print(self.run_method.errInfo(res))
    
    # 修改密码
    def user_passed_reset(self,password,newpasswd,email=None,mobile=None):
        """修改密码"""
        api = '/user/passwd/reset'
        data = {
            "email": email,
            "mobile": mobile,
            "password": password,
            "newpasswd": newpasswd
        }
        try:
            res = self.run_method.post(api, data)
            res.raise_for_status()
        except:
            print("重置密码失败")
            print(self.run_method.errInfo(res))
    
    # 创建组织
    def corp_create(self,name):
        """新增组织"""
        api = '/corp/create'
        data = {
            "name": name
        }
        sql = '''select name from corp where name = '{}';'''.format(name)
        corp_name = self.opera_db.get_fetchone(sql)
        if corp_name is None:
            try:
                res = self.run_method.post(api, data, headers=self.super_header)
                res.raise_for_status()
                print("-------------------------------")
                print("组织: {} 创建成功!".format(name))
                return res.json()["id"]
            except:
                print("新增组织失败")
                print(self.run_method.errInfo(res))
    
    # 用户添加到组织
    def user_corp_add(self,user_id,corp_id,role):
        """用户添加至组织"""
        api = '/corp/user/add'
        data = {
            "user_id": user_id,
            "corp_id": corp_id,
            "role": role
        }
        try:
            res = self.run_method.post(api, data, headers=self.super_header)
            res.raise_for_status()
            print("用户添加至组织成功")
        except:
            print("用户添加至组织失败")
            print(self.run_method.errInfo(res))
    
    # init
    def data_init(self):

        corp = "测试公司初始化勿删2"
        corp_id = self.corp_create(corp)
        user_data = [
            ("xdchenadmin@admin2", "测试管理员初始化勿删2", "123456", "12345678", 524288),
            ("common.user@xdchen.com2", "普通用户账号--勿删2", "123456", "12345678", 0)
        ]
        for i in user_data:
            email = i[0]
            user_name = i[1]
            password = i[2]
            newpasswd = i[3]
            role = i[4]
            user_id = self.user_create(name=user_name, password=password, email= email)
            self.user_passed_reset(password=password,newpasswd=newpasswd,email=email)
            self.user_corp_add(user_id=user_id, corp_id=corp_id,role=role)
        
        other_corp = "其他组织--勿删2"
        other_corp_id = self.corp_create(other_corp)
        other_user_id = self.user_create(name="其他组织用户--勿删2", password="123456", email= "othercorp@xdchen.com2")
        self.user_passed_reset(password="123456",newpasswd="12345678",email="othercorp@xdchen.com2")
        self.user_corp_add(user_id=other_user_id, corp_id=other_corp_id,role=524288)


if __name__ == '__main__':
    init = InitTest()
    init.data_init()
    