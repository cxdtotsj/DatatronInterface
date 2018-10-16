'''
组织类接口

test01 : /corp/create
test02 : /corp/user/add
test03 : /corp/user/list
test04 : /corp/list
test05 : /corp/user/del

'''

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import CorpApiData as Corp
from base.base_method import BaseMethod
from base.public_param import PublicParam
from util.operation_json import OperetionJson
from util.operation_assert import OperationAssert
from util.operation_db import OperationDB
import unittest


class TestCorp(unittest.TestCase, Corp):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.opera_json = OperetionJson()
        cls.opera_assert = OperationAssert()
        cls.opera_db = OperationDB()
        cls.super_header = cls.pub_param.get_super_header()
        cls.corp_header, cls.corp_id = cls.pub_param.get_corp_user()

    def test01_01_corp_create_noName(self):
        '''case01_01:创建组--name为空'''

        api = "/corp/create"
        data = {"name": None}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test01_02_corp_create_noToken(self):
        '''case01_02:创建组--无token'''

        api = "/corp/create"
        data = {"name": Corp.corp_name()}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test01_03_corp_create_noRole(self):
        '''case01_03[普通用户]:创建组--未授权'''

        api = "/corp/create"
        data = {"name": Corp.corp_name()}
        common_user_header = self.pub_param.common_user()
        res = self.run_method.post(api, data, common_user_header)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test01_04_corp_create_noRole(self):
        '''case01_04:创建组[RCM]--未授权'''

        api = "/corp/create"
        data = {"name": Corp.corp_name()}
        rcm_user_header = self.pub_param.common_user(role=1 << 19)
        res = self.run_method.post(api, data, rcm_user_header)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test01_05_corp_create_success(self):
        '''case01_05:创建组[RSM]--标准输入'''

        api = "/corp/create"
        data = {"name": Corp.corp_name()}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(res.json()["id"], '', "新增的组织未返回ID")

    def test02_01_corp_user_add_noUserId(self):
        '''case02_01:用户添加到组[RSM]--无用户ID'''

        api = "/corp/user/add"
        data = {
            "user_id": None,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["users"][0]["id"], '', res.json())

    @unittest.skip("暂时未对输入的user_id做校验")
    def test02_02_corp_user_add_errUserId(self):
        '''case02_02:用户添加到组[RSM]--错误的用户ID'''

        api = "/corp/user/add"
        data = {
            "user_id": None,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())

    def test02_03_corp_user_add_super_noCorpId(self):
        '''case02_03:用户添加到组[RSM]--无组ID'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {
            "user_id": user_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1000, res.json())

    @unittest.skip("暂时未对输入的corp_id做校验")
    def test02_04_corp_user_add_super_errCorpId(self):
        '''case02_04:用户添加到组[RSM]--错误的组ID'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {
            "user_id": user_id,
            "corp_id": "11220099"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())

    def test02_05_corp_user_add_noToken(self):
        '''case02_05:用户添加到组[RSM]--无token'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {
            "user_id": user_id,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test02_06_corp_user_add_super_success(self):
        '''case02_06:用户添加到组[RSM]--添加用户成功(单个用户)'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {
            "user_id": user_id,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(res.json()["users"][0]["id"], user_id, res.json())

    def test02_07_corp_user_add_super_multiple(self):
        '''case02_07:用户添加到组[RSM]--添加用户成功(多个用户)'''

        api = "/corp/user/add"
        *__, user_one = self.pub_param.user_reset()
        *__, user_two = self.pub_param.user_reset()
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.opera_assert.is_list_equal(
            [user_one, user_two], res.json()["users"], "id")

    def test02_08_corp_user_add_noCorpId(self):
        '''case02_08:用户添加到组[RCM]--未传组ID(暂不考虑管理员同时在两个组)'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {"user_id": user_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(res.json()["users"][0]["id"], user_id, res.json())

    def test02_09_corp_user_add_errCorpId(self):
        '''case02_09:用户添加到组[RCM]--传入错误组ID(管理员所在组)'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {"user_id": user_id,
                "corp_id": "001199"}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(res.json()["users"][0]["id"], user_id, res.json())

    def test02_10_corp_user_add_rcmRole(self):
        '''case02_10:用户添加到组[RCM]--添加组管理员权限'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {"user_id": user_id,
                "role": 1 << 19}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(res.json()["role"], str(1 << 19), res.json())
        self.assertEqual(res.json()["users"][0]["id"], user_id, res.json())

    def test02_11_corp_user_add_rsmRole(self):
        '''case02_11:用户添加到组[RCM]--添加超管权限'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        data = {"user_id": user_id,
                "role": 1 << 30}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertNotEqual(res.json()["role"], str(1 << 30), res.json())
        self.assertEqual(res.json()["users"][0]["id"], user_id, res.json())

    def test02_12_corp_user_add_noRole(self):
        '''case02_12:用户添加到组[普通用户]--用户在该组但无管理员权限'''

        api = "/corp/user/add"
        *__, user_id = self.pub_param.user_reset()
        common_user_header = self.pub_param.common_user(self.corp_id)
        data = {"user_id": user_id}
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test02_13_corp_user_add_rcm_multiple(self):
        '''case02_13:用户添加到组[RCM]--添加用户成功(多个用户)'''

        api = "/corp/user/add"
        *__, user_one = self.pub_param.user_reset()
        *__, user_two = self.pub_param.user_reset()
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.opera_assert.is_list_equal(
            [user_one, user_two], res.json()["users"], "id")

    def test03_01_corp_user_list_noCorpId(self):
        '''case03_01:组内用户列表[RSM]--超管无组ID'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "size": 10,
            "corp_id": None}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1000, res.json())

    def test03_02_corp_user_list_super_errCorpId(self):
        '''case03_02:组内用户列表[RSM]--错误的组ID'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "size": 10,
            "corp_id": "112233"}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], str(0), res.json())

    def test03_03_corp_user_list_noToken(self):
        '''case03_03:组内用户列表--无token'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "size": 10,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test03_04_corp_user_list_success(self):
        '''case03_04:组内用户列表[RSM]--查看成功'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "size": 10,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            self.corp_id)
        user_num = self.opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], str(user_num), res.json())

    def test03_05_corp_user_list_noCorpId(self):
        '''case03_05:组内用户列表[RCM]--未传组ID(管理员只在一个组)'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "size": 10}
        res = self.run_method.post(api, data, headers=self.corp_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            self.corp_id)
        user_num = self.opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], str(user_num), res.json())

    def test03_06_corp_user_list_otherCorpId(self):
        '''cas03_06:组内用户列表[RCM]--传入其他组ID'''

        api = "/corp/user/list"
        corp_id = self.pub_param.create_corp()
        data = {
            "page": 1,
            "size": 10,
            "corp_id": corp_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            self.corp_id)
        user_num = self.opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], str(user_num), res.json())

    def test03_07_corp_user_list_commonUser(self):
        '''cas03_07:组内用户列表[普通用户]--普通用户查看所在组内用户'''

        api = "/corp/user/list"
        common_user_header = self.pub_param.common_user(self.corp_id)
        data = {
            "page": 1,
            "size": 10}
        res = self.run_method.post(api, data, headers=common_user_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            self.corp_id)
        user_num = self.opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], str(user_num), res.json())

    def test04_01_corp_list_super_success(self):
        '''case04_01:组列表[RSM]--超管查询成功'''

        api = "/corp/list"
        data = {
            "page": 1,
            "size": 10}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())

    def test04_02_corp_list_rcm_success(self):
        '''case04_02:组列表[RCM]--组织管理员查询成功'''

        api = "/corp/list"
        data = {
            "page": 1,
            "size": 10}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["data_list"][0]
                         ["id"], self.corp_id, res.json())

    def test04_03_corp_list_common_success(self):
        '''case04_03:组列表[普通用户]--普通用户查询成功'''

        api = "/corp/list"
        data = {
            "page": 1,
            "size": 10}
        common_user_header = self.pub_param.common_user(self.corp_id)
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["data_list"][0]
                         ["id"], self.corp_id, res.json())

    def test05_01_corp_user_del_noUserId(self):
        '''case05_01:用户从组删除[RSM]--无用户ID'''

        api = '/corp/user/del'
        data = {
            "user_id": None,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(res.json()["users"][0]["id"], '', res.json())

    def test05_02_corp_user_del_errUserId(self):
        '''case05_02:用户从组删除[RSM]--错误的用户ID'''

        api = '/corp/user/del'
        data = {
            "user_id": "112334",
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(res.json()["users"][0]["id"],
                         data["user_id"], res.json())

    def test05_03_corp_user_del_super_noCorpId(self):
        '''case05_03:用户从组删除[RSM]--超管无组ID'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id)
        data = {"user_id": user_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = self.opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], '', res.json())
        self.assertEqual(corp_user_status["status"],
                         1, "无corp_id情况下user_id被删除")

    def test05_04_corp_user_del_super_errCorpId(self):
        '''case05_04:用户从组删除[RSM]--错误的组ID'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id)
        data = {
            "user_id": user_id,
            "corp_id": "12121313"}
        res = self.run_method.post(api, data, headers=self.super_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = self.opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(corp_user_status["status"],
                         1, "无corp_id情况下user_id被删除")

    def test05_05_corp_user_del_noToken(self):
        '''case05_05:用户从组删除[RSM]--无token'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id)
        data = {
            "user_id": user_id,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test05_06_corp_user_del_super_success(self):
        '''case05_06:用户从组删除[RSM]--删除用户成功'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id)
        data = {
            "user_id": user_id,
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        sql = '''select status from corp_user where user_id = '{}' and corp_id = '{}';'''.format(
            user_id, self.corp_id)
        corp_user_status = self.opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(corp_user_status["status"],
                         2, "删除失败")

    def test05_07_corp_user_del_multiple(self):
        '''case05_07:用户从组删除[RSM]--多个用户'''

        api = '/corp/user/del'
        *__, user_one = self.pub_param.user_reset_corp(self.corp_id)
        *__, user_two = self.pub_param.user_reset_corp(self.corp_id)
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        sql = '''select status from corp_user where user_id in ('{}','{}') and corp_id = '{}';'''.format(
            user_one, user_two, self.corp_id)
        corp_user_status = self.opera_db.get_fetchall(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.opera_assert.is_list_in(2, corp_user_status, "status")

    def test05_08_corp_user_del_noCorpId(self):
        '''case05_08:用户从组删除[RCM]--未传组ID(暂时不考虑同时在两个组)'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id)
        data = {"user_id": user_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        sql = '''select status from corp_user where user_id = '{}' and corp_id = '{}';'''.format(
            user_id, self.corp_id)
        corp_user_status = self.opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(corp_user_status["status"],
                         2, "删除失败")

    def test05_09_corp_user_del_rcm_multiple(self):
        '''case05_09:用户从组删除[RCM]--删除多个用户'''

        api = '/corp/user/del'
        *__, user_one = self.pub_param.user_reset_corp(self.corp_id)
        *__, user_two = self.pub_param.user_reset_corp(self.corp_id)
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": self.corp_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        sql = '''select status from corp_user where user_id in ('{}','{}') and corp_id = '{}';'''.format(
            user_one, user_two, self.corp_id)
        corp_user_status = self.opera_db.get_fetchall(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.opera_assert.is_list_in(2, corp_user_status, "status")

    def test05_10_corp_user_del_noAuth(self):
        '''case05_10:用户从组删除[RCM]--删除该组织其他管理员'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id, role=1 << 19)
        data = {"user_id": user_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        sql = '''select status from corp_user where user_id = '{}' and corp_id = '{}';'''.format(
            user_id, self.corp_id)
        corp_user_status = self.opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], self.corp_id, res.json())
        self.assertEqual(corp_user_status["status"],
                         2, "删除失败")

    def test05_11_corp_user_del_otherCorp(self):
        '''case05_11:用户从组删除[RCM]--删除其他组用户'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp()
        data = {"user_id": user_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = self.opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(corp_user_status["status"],
                         1, "管理员删除其他组织用户成功")

    def test05_12_corp_user_del_noRole(self):
        '''case05_12:用户从组删除[普通用户]--用户在该组但无管理员权限'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id, role=1 << 19)
        data = {"user_id": user_id}
        common_user_header = self.pub_param.common_user(self.corp_id)
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    @unittest.skip("存在BUG，暂时跳过")
    def test05_13_corp_user_del_delCorpUser(self):
        '''case05_13:用户从组删除--已删除管理员移除用户'''

        api = '/corp/user/del'
        *__, user_id = self.pub_param.user_reset_corp(self.corp_id, role=1 << 19)
        data = {"user_id": user_id}

        # 获取该用户 token
        user_email, __, del_user_id = self.pub_param.user_reset_corp(
            self.corp_id, role=1 << 19)
        user_header = self.pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(del_user_id, self.corp_id)

        # 移除用户
        res = self.run_method.post(api, data, headers=user_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = self.opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")
        self.assertEqual(corp_user_status["status"],
                         1, "已被移除的管理员仍可以删除用户")
