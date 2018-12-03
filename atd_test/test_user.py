'''
用户类接口

test01 : /user/create
test02 : /user/list
test03 : /user/login
test04 : /user/passwd/reset

'''

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import UserApiData as User
from base.base_method import BaseMethod
from data.public_param import PublicParam
from util.operation_json import OperetionJson
import unittest
import time


run_method = BaseMethod()
pub_param = PublicParam()
opera_json = OperetionJson()
super_header = pub_param.get_super_header()
corp_header, corp_id = pub_param.get_corp_user()
# 普通用户
common_user_header = pub_param.common_user(corp_id)
# 其他组织RCM
other_corp_header = pub_param.common_user(role=524288)


class TestUserCreate(unittest.TestCase, User):

    def setUp(self):
        self.api = "/user/create"
        self.data = {
            "email": User.user_email(),
            "name": User.user_name(),
            "password": "123456"}

    def test01_user_create_noName(self):
        '''case01:创建用户[RSM]--缺少用户名 '''

        self.data.update(name=None)
        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_user_create_noPasswd(self):
        '''case02:创建用户[RSM]--缺少密码'''

        self.data.update(password=None)
        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_user_create_noToken(self):
        '''case03:创建用户[RSM]--无token'''

        res = run_method.post(self.api, self.data)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test04_user_create_noEAM(self):
        '''case04:创建用户[RSM]--无手机号和邮箱'''

        self.data.pop("email")
        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_user_create_super_email(self):
        '''case05:创建用户[RSM]--超管邮箱新增'''

        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        opera_json.check_json_value("test05_user_create", self.data["email"])   # 保存email至json，后续用例调用

    # 依赖用例 test05_user_create
    def test06_user_create_emailRepeat(self):
        '''case06:创建用户[RSM]--邮箱重复新增'''

        repeat_email = opera_json.get_data("test05_user_create")  # 获取用例test05_user_create的email
        self.data.update(email=repeat_email)
        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1409, run_method.errInfo(res))

    def test07_user_create_super_mobile(self):
        '''case07:创建用户[RSM]--超管手机新增'''

        self.data.pop("email")
        self.data.update(mobile=User.user_mobile())
        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

        opera_json.check_json_value("test07_user_create", self.data["mobile"])    # 保存mobile至json

    # 依赖用例 test07_user_create
    def test08_user_create_mobileRepeat(self):
        '''case08:创建用户[RSM]--手机重复新增'''

        self.data.pop("email")
        repeat_mobile = opera_json.get_data("test07_user_create")   # 获取test07_user_create的mobile
        self.data.update(mobile=repeat_mobile)
        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1409, run_method.errInfo(res))

    def test09_user_create_noRole(self):
        '''case09:创建用户[普通用户]--未授权创建用户'''

        res = run_method.post(self.api, self.data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test10_user_create_email(self):
        '''case10:创建用户[RCM]--组管理员邮箱创建'''

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test11_user_create_mobile(self):
        '''case11:创建用户[RCM]--组管理员手机创建'''

        self.data.pop("email")
        self.data.update(mobile=User.user_mobile())
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test12_user_create_BothEM(self):
        '''case12:创建用户[RCM]--组管理员手机、邮箱同时创建'''

        self.data.update(mobile=User.user_mobile())
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))


class TestUserList(unittest.TestCase):

    def setUp(self):
        self.api = '/user/list'
        self.data = {
            "page": 1,
            "limit": 100}

    def test01_user_list_super(self):
        '''case01:用户列表--超管查询所有用户（limit最大100）'''

        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test02_user_list_rcm(self):
        '''case02:用户列表--组织管理员查看自己所在组(暂不支持)'''
        pass

    def test03_user_list_commonUser(self):
        '''case03:用户列表--普通用户查询自己所在组(暂不支持)'''
        pass

    def test04_user_list_nameSearch(self):
        '''case04:用户列表--name查询(暂不支持)'''
        pass


class TestUserLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = '/user/login'

    def test01_user_login_noPassword(self):
        '''case01:登录接口--无password'''

        data = {"mobile": "122121"}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_user_login_errMobile(self):
        '''case02:登录接口--错误的手机号'''

        data = {
            "mobile": "122121",
            "password": 123456}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))

    def test03_user_login_errEmail(self):
        '''case03:登录接口--错误的邮箱'''
 
        data = {
            "mobile": "122121",
            "password": 123456}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))

    def test04_user_login_noPasswd(self):
        '''case04:登录接口--错误的密码'''
        
        user_email,*__ = pub_param.user_reset_corp(corp_id=corp_id)
        data = {
            "email": user_email,
            "password": 000000}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test05_user_login_firstLogin(self):
        '''case05:登录接口--邮箱第一次登录,未重置密码'''
        
        user_email,*__ = pub_param.user_corp(corp_id)
        data = {
            "email": user_email,
            "password": 123456}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1426, run_method.errInfo(res))

    def test06_user_login_firstLogin(self):
        '''case06:登录接口--邮箱登录，未绑定到组织(已重置密码)'''
        
        user_email,*__ = pub_param.user_reset()
        pub_param.user_pwd_reset(123456, 12345678, email=user_email)
        data = {
            "email": user_email,
            "password": 12345678}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test07_user_login_email(self):
        '''case07:登录接口--邮箱登录（绑定到组织）'''
        
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "password": 12345678}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))

    def test08_user_login_mobile(self):
        '''case08:登录接口--手机第一次登录'''
        
        __, user_mobile, __ = pub_param.user_reset_corp(corp_id)
        data = {
            "mobile": user_mobile,
            "password": 12345678}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))

    def test09_user_login_bothME(self):
        '''case09:登录接口--同时输入手机号和邮箱'''
        
        user_email, user_mobile, __ = pub_param.user_reset_corp(
            corp_id)
        data = {
            "mobile": user_mobile,
            "email": user_email,
            "password": 12345678}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))


class TestUserPwdReset(unittest.TestCase):

    def test01_user_passwd_reset_id(self):
        '''case01:重置用户密码[普通用户]--输入id修改密码并能登录'''

        api = '/user/passwd/reset'
        user_email, __, user_id = pub_param.user_corp(corp_id)
        data = {
            "id": user_id,
            "password": 123456,
            "newpasswd": 12345678}
        res = run_method.post(api, data)
        login_res = pub_param.user_header(12345678, email=user_email)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertTrue(login_res["Authorization"], run_method.errInfo(res))

    def test02_user_passwd_reset_mobile(self):
        '''case02:重置用户密码[普通用户]--输入手机修改密码并能登录'''

        api = '/user/passwd/reset'
        __, user_mobile, __ = pub_param.user_corp(corp_id)
        data = {
            "mobile": user_mobile,
            "password": 123456,
            "newpasswd": 12345678}
        res = run_method.post(api, data)
        login_res = pub_param.user_header(12345678, mobile=user_mobile)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertTrue(login_res["Authorization"], run_method.errInfo(res))

    def test03_user_passwd_reset_email(self):
        '''case03:重置用户密码[普通用户]--输入邮箱修改密码并能登录'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_corp(corp_id)
        data = {
            "email": user_email,
            "password": 123456,
            "newpasswd": 12345678}
        res = run_method.post(api, data)
        login_res = pub_param.user_header(12345678, email=user_email)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertTrue(login_res["Authorization"], run_method.errInfo(res))

    def test04_user_passwd_reset_noPasswd(self):
        '''case04:重置用户密码[RSM]--新密码为空'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "newpasswd": None}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_user_passwd_reset_errPasswd(self):
        '''case05:重置用户密码[RSM]--新密码小于6位'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "newpasswd": 12345}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test06_user_passwd_reset_noToken(self):
        '''case06:重置用户密码[RSM]--原密码不填，无token'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "newpasswd": 123456}
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test07_user_passwd_reset_mustFalse(self):
        '''case07:重置用户密码--超管修改密码后登录（需要重置密码）'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "newpasswd": 1234567,
            "mustReset": "true"}
        res = run_method.post(api, data, headers=super_header)
        login_data = {
            "email": user_email,
            "password": 1234567}
        login_res = run_method.post("/user/login", login_data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(login_res.json()["code"], 1426, run_method.errInfo(login_res))

    def test08_user_passwd_reset_noRole(self):
        '''case08:重置用户密码[普通用户]--修改其他用户密码'''

        api = '/user/passwd/reset'

        # 创建其他组织的用户，返回email
        user_email, *__ = pub_param.user_reset_corp()
        data = {
            "email": user_email,
            "newpasswd": 12345678}
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test09_user_passwd_reset_oldLonin(self):
        '''case09:重置用户密码[RSM]--修改密码后用旧密码登录'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "newpasswd": 12345678}
        res = run_method.post(api, data, headers=super_header)
        login_data = {
            "email": user_email,
            "password": 123456}
        login_res = run_method.post("/user/login", login_data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(login_res.json()["code"], 1401, run_method.errInfo(res))

    def test10_user_passwd_reset_newLogin(self):
        '''case10:重置用户密码[RSM]--修改密码后用新密码登录'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "newpasswd": 12345678}
        res = run_method.post(api, data, headers=super_header)
        login_data = {
            "email": user_email,
            "password": 12345678}
        login_res = run_method.post("/user/login", login_data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(login_res.status_code, 200, run_method.errInfo(login_res))

    @unittest.skip("确认 组织管理员是否可以修改密码？")
    def test11_user_passwd_reset_Corp(self):
        '''case11:重置用户密码[RCM]--修改本组织普通用户密码(原密码为空)'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp(corp_id)
        data = {
            "email": user_email,
            "newpasswd": 12345678}
        res = run_method.post(api, data, headers=corp_header)
        login_data = {
            "email": user_email,
            "password": 12345678}
        login_res = run_method.post("/user/login", login_data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(login_res.status_code, 200, run_method.errInfo(login_res))

    def test12_user_passwd_reset_otherCorp(self):
        '''case12:重置用户密码[RCM]--修改其他组织用户密码'''

        api = '/user/passwd/reset'
        user_email, *__ = pub_param.user_reset_corp()
        data = {
            "email": user_email,
            "newpasswd": 12345678}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))
        time.sleep(2)


if __name__ == '__main__':
    unittest.main()
