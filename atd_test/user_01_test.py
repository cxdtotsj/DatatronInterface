'''用户类接口'''
import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import UserApiData as User
from base.base_method import BaseMethod
from base.public_param import PublicParam
import unittest


class TestUser(unittest.TestCase, User):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.super_header = cls.pub_param.get_super_header()

    def test01_01_user_create_noName(self):
        '''case01_01:创建用户--缺少用户名 '''

        api = "/user/create"
        data = {"name": None,
                "password": "123456"}
        res = self.run_method.post(api, data, headers=self.super_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_02_user_create_noPasswd(self):
        '''case01_02:创建用户--缺少密码'''

        api = "/user/create"
        data = {"name": "test04",
                "password": None}
        res = self.run_method.post(api, data, headers=self.super_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_03_user_create_noToken(self):
        '''case01_03:创建用户--无token'''

        api = "/user/create"
        data = {"name": User.user_name,
                "password": "123456"}
        res = self.run_method.post(api, data)
        res_dict = res.json()
        self.assertEqual(res.status_code, 401, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1401, res_dict)

    def test01_04_user_create_noEAM(self):
        '''case01_04:创建用户--无手机号或邮箱'''
        pass

    def test01_05_user_create_email(self):
        '''case01_05:创建用户--邮箱新增'''
        pass

    def test01_06_user_create_emailRepeat(self):
        '''case01_06:创建用户--邮箱重复新增'''
        pass

    def test01_07_user_create_mobile(self):
        '''case01_07:创建用户--手机新增'''
        pass

    def test01_08_user_create_mobileRepeat(self):
        '''case01_08:创建用户--手机重复新增'''
        pass

    def test01_09_user_create_noAuth(self):
        '''case01_09:创建用户--未授权创建用户'''
        pass

if __name__ == '__main__':
    unittest.main()
