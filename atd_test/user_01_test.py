'''用户类接口'''
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from data.api_data import UserApiData as User
from base.base_method import BaseMethod
from base.public_param import PublicParam
import unittest


class TestUser(unittest.TestCase,User):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.base_header = cls.pub_param.get_base_header()

    def test01_01_user_create_noName(self):
        '''case01_01:创建用户--缺少用户名 '''

        api = "/user/create"
        data = {"name": None,
                "password": "123456"}
        res = self.run_method.post(api, data, headers=self.base_header)
        res_dict = res.json()

        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_02_user_create_noPasswd(self):
       '''case01_02:创建用户--缺少密码'''

       api = "/user/create"
       data = {"name": "test04",
               "password": None}
       res = self.run_method.post(api, data, headers=self.base_header)
       res_dict = res.json()

       self.assertEqual(res.status_code, 400, "状态码返回出错误")
       self.assertEqual(res_dict["code"], 1400, res.json())
    
    def test01_03_user_create_noAuth(self):
        '''case01_03:创建用户--未授权'''

        api = "/user/create"
        data = {"name": User.user_name,
                "password": "123456"}
        
        res = self.run_method.post(api, data)
        res_dict = res.json()
 
        self.assertEqual(res.status_code, 401, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1401, res.json())
    
    def test01_04_user_create_success(self):
        '''case01_04:创建用户--新增成功，必填项'''
        pass
    
    def test01_05_user_create_success(self):
        '''case01_05:创建用户--新增成功，全部参数'''
        pass




if __name__ == '__main__':
    unittest.main()