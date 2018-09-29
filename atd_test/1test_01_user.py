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

    def test01_05_user_create_super_email(self):
        '''case01_05:创建用户--超管邮箱新增'''
        pass

    def test01_06_user_create_emailRepeat(self):
        '''case01_06:创建用户--邮箱重复新增'''
        pass

    def test01_07_user_create_super_mobile(self):
        '''case01_07:创建用户--超管手机新增'''
        pass

    def test01_08_user_create_mobileRepeat(self):
        '''case01_08:创建用户--手机重复新增'''
        pass

    def test01_09_user_create_noAuth(self):
        '''case01_09:创建用户--未授权创建用户'''
        pass
    
    def test01_10_user_create_email(self):
        '''case01_10:创建用户--组管理员邮箱创建'''
        pass
    
    def test01_11_user_create_mobile(self):
        '''case01_11:创建用户--组管理员手机创建'''
        pass


    def test02_01_user_list_noPage(self):
        '''case02_01:用户列表--未传page'''
        pass

    def test02_02_user_list_errPage(self):
        '''case02_02:用户列表--错误的page参数'''
        pass
    
    def test02_03_user_list_noSize(self):
        '''case02_03:用户列表--未传size'''
        pass
    
    def test02_04_user_list_errSzieType(self):
        '''case02_04:用户列表--错误的size参数'''
        pass
    
    def test02_05_user_list_super_success(self):
        '''case02_05:用户列表--超管查询所有用户（Size最大100）'''
    
    def test02_06_user_list_common_success(self):
        '''case02_06:用户列表--普通用户查询自己所在组'''
    

    def test03_01_user_login_errMobile(self):
        '''case03_01:登录接口--错误的手机号'''
        pass
    
    def test03_02_user_login_errEmail(self):
        '''case03_02:登录接口--错误的邮箱'''
        pass
    
    def test03_03_user_login_noPasswd(self):
        '''case03_03:登录接口--错误的密码'''
        pass
    
    def test03_04_user_login_firstLogin(self):
        '''case03_04:登录接口--邮箱第一次登录，密码须修改'''
        pass

    def test03_05_user_login_bothME(self):
        '''case03_05:登录接口--同时输入手机号和邮箱'''
    
    def test03_06_user_login_email(self):
        '''case03_06:登录接口--邮箱登录（密码已修改）'''
        pass
    
    def test03_07_user_login_mobile(self):
        '''case03_07:登录接口--手机第一次登录（邮箱已登录过）'''
        pass

    # 新用户修改密码
    def test04_01_user_passwd_reset_id(self):
        '''case04_01:重置用户密码--输入id修改密码并能登录'''
        pass
    
    def test04_02_user_passwd_reset_mobile(self):
        '''case04_02:重置用户密码--输入手机修改密码并能登录'''
        pass

    def test04_03_user_passwd_reset_email(self):
        '''case04_03:重置用户密码--输入邮箱修改密码并能登录'''
        pass
    
    # 老用户修改密码
    def test04_04_user_passwd_reset_errPassword(self):
        '''case04_04:重置用户密码--输入错误的旧密码'''
        pass
    
    def test04_05_user_passwd_reset_noPasswd(self):
        '''case04_05:重置用户密码--新密码为空'''
        pass
    
    def test04_06_user_passwd_reset_errPasswd(self):
        '''case04_06:重置用户密码--新密码小于6位'''
        pass
    
    def test04_07_user_passwd_reset_oldToken(self):
        '''case04_07:重置用户密码--修改密码后使用旧token操作'''
        pass
    
    def test04_08_user_passwd_reset_oldLonin(self):
        '''case04_08:重置用户密码--修改密码后用旧密码登录'''
        pass
    
    def test04_09_user_passwd_reset_newLogin(self):
        '''case04_09:重置用户密码--修改密码后用新密码登录'''
        pass      

    # 超管修改密码
    def test04_10_user_passwd_reset_noToken(self):
        '''case04_10:重置用户密码--原密码不填，无token'''
        pass 

    def test04_11_user_passwd_reset_mustTrue(self):
        '''case04_11:重置用户密码--超管修改密码后登录（未重置密码）'''
        pass 
    
    def test04_12_user_passwd_reset_mustFalse(self):
        '''case04_12:重置用户密码--超管修改密码后登录（未重置密码）'''
        pass 



if __name__ == '__main__':
    unittest.main()
