'''用户类接口'''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import UserApiData as User
from base.base_method import BaseMethod
from base.public_param import PublicParam
from util.operation_json import OperetionJson
import unittest


class TestUser(unittest.TestCase, User):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.opera_json = OperetionJson()
        cls.super_header = cls.pub_param.get_super_header()
        cls.corp_header, cls.corp_id = cls.pub_param.get_corp_user()

    def test01_01_user_create_noName(self):
        '''case01_01:创建用户[RSM]--缺少用户名 '''

        api = "/user/create"
        data = {
            "eamil": User.user_email,
            "name": None,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test01_02_user_create_noPasswd(self):
        '''case01_02:创建用户[RSM]--缺少密码'''

        api = "/user/create"
        data = {
            "eamil": User.user_email,
            "name": "test04",
            "password": None}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test01_03_user_create_noToken(self):
        '''case01_03:创建用户[RSM]--无token'''

        api = "/user/create"
        data = {
            "eamil": User.user_email,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test01_04_user_create_noEAM(self):
        '''case01_04:创建用户[RSM]--无手机号和邮箱'''

        api = "/user/create"
        data = {
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test01_05_user_create_super_email(self):
        '''case01_05:创建用户[RSM]--超管邮箱新增'''

        api = "/user/create"
        data = {
            "email": User.user_email,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())

        self.opera_json.check_json_value("test01_05_user", data["email"])

    # 依赖用例 test01_05_user_create_super_email
    def test01_06_user_create_emailRepeat(self):
        '''case01_06:创建用户[RSM]--邮箱重复新增'''

        api = "/user/create"
        repeat_email = self.opera_json.get_data("test01_05_user")
        data = {
            "email": repeat_email,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1409, res.json())

    def test01_07_user_create_super_mobile(self):
        '''case01_07:创建用户[RSM]--超管手机新增'''

        api = "/user/create"
        data = {
            "mobile": User.user_mobile,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())

        self.opera_json.check_json_value("test01_07_user", data["mobile"])

    # 依赖用例 test01_07_user_create_super_mobile
    def test01_08_user_create_mobileRepeat(self):
        '''case01_08:创建用户[RSM]--手机重复新增'''

        api = "/user/create"
        repeat_mobile = self.opera_json.get_data("test01_07_user")
        data = {
            "mobile": repeat_mobile,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1409, res.json())

    def test01_09_user_create_noRole(self):
        '''case01_09:创建用户[普通用户]--未授权创建用户'''

        common_user_header = self.pub_param.common_user(self.corp_id)
        api = "/user/create"
        data = {
            "email": User.user_email,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test01_10_user_create_email(self):
        '''case01_10:创建用户[RCM]--组管理员邮箱创建'''

        api = "/user/create"
        data = {
            "email": User.user_email,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())

    def test01_11_user_create_mobile(self):
        '''case01_11:创建用户[RCM]--组管理员手机创建'''

        api = "/user/create"
        data = {
            "mobile": User.user_mobile,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())

    def test01_12_user_create_BothEM(self):
        '''case01_12:创建用户[RCM]--组管理员手机、邮箱同时创建'''

        api = "/user/create"
        data = {
            "mobile": User.user_mobile,
            "email": User.user_email,
            "name": User.user_name,
            "password": "123456"}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())

        self.opera_json.check_json_value(
            "test01_12_user", {"mobile": data["mobile"], "email": data["email"]})

    def test02_01_user_list_super(self):
        '''case02_01:用户列表--超管查询所有用户（Size最大100）'''

        api = '/user/list'
        data = {
            "page": 1,
            "size": 20}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())

    def test02_02_user_list_rcm(self):
        '''case02_02:用户列表--组织管理员查看自己所在组(暂不支持)'''
        pass

    def test02_03_user_list_commonUser(self):
        '''case02_03:用户列表--普通用户查询自己所在组(暂不支持)'''
        pass

    def test02_04_user_list_nameSearch(self):
        '''case02_04:用户列表--name查询(暂不支持)'''
        pass

    def test03_01_user_login_noPassword(self):
        '''case03_01:登录接口--无password'''

        api = '/user/login'
        data = {"mobile": "122121"}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test03_02_user_login_errMobile(self):
        '''case03_02:登录接口--错误的手机号'''

        api = '/user/login'
        data = {
            "mobile": "122121",
            "password": 123456}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1404, res.json())

    def test03_03_user_login_errEmail(self):
        '''case03_03:登录接口--错误的邮箱'''

        api = '/user/login'
        data = {
            "mobile": "122121",
            "password": 123456}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1404, res.json())

    # 依赖用例 test01_05_user_create_super_email
    def test03_04_user_login_noPasswd(self):
        '''case03_04:登录接口--错误的密码'''

        api = '/user/login'
        user_email = self.opera_json.get_data("test01_05_user")
        data = {
            "email": user_email,
            "password": 000000}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test03_05_user_login_firstLogin(self):
        '''case03_05:登录接口--邮箱第一次登录,未重置密码'''

        api = '/user/login'
        user_email = self.opera_json.get_data("test01_05_user")
        data = {
            "email": user_email,
            "password": 123456}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1426, res.json())

    def test03_06_user_login_firstLogin(self):
        '''case03_06:登录接口--邮箱登录，未绑定到组织(已重置密码)'''

        api = '/user/login'
        user_email = self.opera_json.get_data("test01_05_user")
        self.pub_param.user_pwd_reset(123456, 12345678, email=user_email)
        data = {
            "email": user_email,
            "password": 12345678}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1000, res.json())

    # 依赖用例 test01_12_user_create_BothEM
    def test03_07_user_login_email(self):
        '''case03_07:登录接口--邮箱登录（绑定到组织）'''

        api = '/user/login'
        user_email, *__ = self.pub_param.user_reset_corp(self.corp_id)
        data = {
            "email": user_email,
            "password": 12345678}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["corp_id"], self.corp_id, res.json())

    def test03_08_user_login_mobile(self):
        '''case03_08:登录接口--手机第一次登录'''

        api = '/user/login'
        __, user_mobile, __ = self.pub_param.user_reset_corp(self.corp_id)
        data = {
            "mobile": user_mobile,
            "password": 12345678}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["corp_id"], self.corp_id, res.json())

    def test03_09_user_login_bothME(self):
        '''case03_09:登录接口--同时输入手机号和邮箱'''

        api = '/user/login'
        user_email, user_mobile, __ = self.pub_param.user_reset_corp(
            self.corp_id)
        data = {
            "mobile": user_mobile,
            "email": user_email,
            "password": 12345678}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())


    # 新用户修改密码
    def test04_01_user_passwd_reset_id(self):
        '''case04_01:重置用户密码--输入id修改密码并能登录'''
        api = '/user/passwd/reset'
        *__,user_id = self.pub_param.user_reset_corp(self.corp_id)

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

    def test04_13_user_passwd_reset_noRole(self):
        '''case04_13:重置用户密码[普通用户]--修改其他用户密码'''
        pass

    def test04_14_user_passwd_reset_Corp(self):
        '''case04_14:重置用户密码[RCM]--修改本组织普通用户密码'''
        pass

    def test04_15_user_passwd_reset_otherCorp(self):
        '''case04_15:重置用户密码[RCM]--修改其他组织用户密码'''
        pass

if __name__ == '__main__':
    unittest.main()
