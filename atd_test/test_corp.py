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
from data.public_param import PublicParam
from util.operation_json import OperetionJson
from util.operation_assert import OperationAssert
from util.operation_db import OperationDB
import unittest


run_method = BaseMethod()
pub_param = PublicParam()
opera_json = OperetionJson()
opera_assert = OperationAssert()
opera_db = OperationDB()
super_header = pub_param.get_super_header()
corp_header, corp_id = pub_param.get_corp_user()
# 普通用户
common_user_header = pub_param.common_user(corp_id)
# 其他组织RCM
other_corp_header = pub_param.common_user(role=524288)


class TestCorpCreate(unittest.TestCase, Corp):

    def setUp(self):
        self.api = "/corp/create"
        self.data = {"name": Corp.corp_name()}

    def test01_corp_create_noName(self):
        '''case01:创建组--name为空'''

        self.data.update(name=None)
        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_corp_create_noToken(self):
        '''case02:创建组--无token'''

        res = run_method.post(self.api, self.data)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test03_corp_create_noRole(self):
        '''case03[普通用户]:创建组--未授权'''

        res = run_method.post(self.api, self.data, common_user_header)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test04_corp_create_noRole(self):
        '''case04:创建组[RCM]--未授权'''

        res = run_method.post(self.api, self.data, corp_header)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test05_corp_create_success(self):
        '''case05:创建组[RSM]--标准输入'''

        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["id"], '', "新增的组织未返回ID")


class TestCorpUserAdd(unittest.TestCase):

    def test01_corp_user_add_noUserId(self):
        '''case01:用户添加到组[RSM]--无用户ID'''

        api = "/corp/user/add"
        data = {
            "user_id": None,
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"], '', run_method.errInfo(res))

    @unittest.skip("暂时未对输入的user_id做校验")
    def test02_corp_user_add_errUserId(self):
        '''case02:用户添加到组[RSM]--错误的用户ID'''

        api = "/corp/user/add"
        data = {
            "user_id": None,
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test03_corp_user_add_noCorpId(self):
        '''case03:用户添加到组[RSM]--无组ID'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {
            "user_id": user_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    @unittest.skip("暂时未对输入的corp_id做校验")
    def test04_corp_user_add_errCorpId(self):
        '''case04:用户添加到组[RSM]--错误的组ID'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {
            "user_id": user_id,
            "corp_id": "11220099"}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test05_corp_user_add_noToken(self):
        '''case05:用户添加到组[RSM]--无token'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {
            "user_id": user_id,
            "corp_id": corp_id}
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test06_corp_user_add_success(self):
        '''case06:用户添加到组[RSM]--添加用户成功(单个用户)'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {
            "user_id": user_id,
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"], user_id, run_method.errInfo(res))

    def test07_corp_user_add_multiple(self):
        '''case07:用户添加到组[RSM]--添加用户成功(多个用户)'''

        api = "/corp/user/add"
        *__, user_one = pub_param.user_reset()
        *__, user_two = pub_param.user_reset()
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        opera_assert.is_list_equal(
            [user_one, user_two], res.json()["users"], "id")

    def test08_corp_user_add_noCorpId(self):
        '''case08:用户添加到组[RCM]--未传组ID(暂不考虑管理员同时在两个组)'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {"user_id": user_id}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"], user_id, run_method.errInfo(res))

    def test09_corp_user_add_errCorpId(self):
        '''case09:用户添加到组[RCM]--传入错误组ID(管理员所在组)'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {"user_id": user_id,
                "corp_id": "001199"}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"], user_id, run_method.errInfo(res))

    def test10_corp_user_add_rcmRole(self):
        '''case10:用户添加到组[RCM]--添加组管理员权限'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {"user_id": user_id,
                "role": 1 << 19}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(res.json()["role"], str(1 << 19), run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"], user_id, run_method.errInfo(res))

    def test11_corp_user_add_rsmRole(self):
        '''case11:用户添加到组[RCM]--添加超管权限'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {"user_id": user_id,
                "role": 1 << 30}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertNotEqual(res.json()["role"], str(1 << 30), run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"], user_id, run_method.errInfo(res))

    def test12_corp_user_add_noRole(self):
        '''case12:用户添加到组[普通用户]--用户在该组但无管理员权限'''

        api = "/corp/user/add"
        *__, user_id = pub_param.user_reset()
        data = {"user_id": user_id}
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test13_corp_user_add_multiple(self):
        '''case13:用户添加到组[RCM]--添加用户成功(多个用户)'''

        api = "/corp/user/add"
        *__, user_one = pub_param.user_reset()
        *__, user_two = pub_param.user_reset()
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        opera_assert.is_list_equal(
            [user_one, user_two], res.json()["users"], "id")


class TestCorpUserList(unittest.TestCase):

    def test01_corp_user_list_noCorpId(self):
        '''case01:组内用户列表[RSM]--超管无组ID'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "limit": 10,
            "corp_id": None}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test02_corp_user_list_errCorpId(self):
        '''case02:组内用户列表[RSM]--错误的组ID'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "limit": 10,
            "corp_id": "112233"}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(0), run_method.errInfo(res))

    def test03_corp_user_list_noToken(self):
        '''case03:组内用户列表--无token'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "limit": 10,
            "corp_id": corp_id}
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test04_corp_user_list_success(self):
        '''case04:组内用户列表[RSM]--查看成功'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "limit": 10,
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            corp_id)
        user_num = opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(user_num), run_method.errInfo(res))

    def test05_corp_user_list_noCorpId(self):
        '''case05:组内用户列表[RCM]--未传组ID(管理员只在一个组)'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "limit": 10}
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            corp_id)
        user_num = opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(user_num), run_method.errInfo(res))

    def test06_corp_user_list_otherCorpId(self):
        '''case06:组内用户列表[RCM]--传入其他组ID'''

        api = "/corp/user/list"
        other_corp_id = pub_param.create_corp()
        data = {
            "page": 1,
            "limit": 10,
            "corp_id": other_corp_id}
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            corp_id)
        user_num = opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(user_num), run_method.errInfo(res))

    def test07_corp_user_list_commonUser(self):
        '''cas07:组内用户列表[普通用户]--普通用户查看所在组内用户'''

        api = "/corp/user/list"
        data = {
            "page": 1,
            "limit": 10}
        res = run_method.post(api, data, headers=common_user_header)
        sql = '''select id from corp_user where corp_id = '{}' and status = 1;'''.format(
            corp_id)
        user_num = opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(user_num), run_method.errInfo(res))


class TestCorpList(unittest.TestCase):

    def test01_corp_list_super_success(self):
        '''case01:组列表[RSM]--超管查询成功'''

        api = "/corp/list"
        data = {
            "page": 1,
            "limit": 10}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test02_corp_list_rcm_success(self):
        '''case02:组列表[RCM]--组织管理员查询成功'''

        api = "/corp/list"
        data = {
            "page": 1,
            "limit": 10}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["data_list"][0]
                         ["id"], corp_id, run_method.errInfo(res))

    def test03_corp_list_common_success(self):
        '''case03:组列表[普通用户]--普通用户查询成功'''

        api = "/corp/list"
        data = {
            "page": 1,
            "limit": 10}
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["data_list"][0]
                         ["id"], corp_id, run_method.errInfo(res))


class TestCorpUserDel(unittest.TestCase):

    def test01_corp_user_del_noUserId(self):
        '''case01:用户从组删除[RSM]--无用户ID'''

        api = '/corp/user/del'
        data = {
            "user_id": None,
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"], '', run_method.errInfo(res))

    def test02_corp_user_del_errUserId(self):
        '''case02:用户从组删除[RSM]--错误的用户ID'''

        api = '/corp/user/del'
        data = {
            "user_id": "112334",
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(res.json()["users"][0]["id"],
                         data["user_id"], run_method.errInfo(res))

    def test03_corp_user_del_noCorpId(self):
        '''case03:用户从组删除[RSM]--超管无组ID'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id)
        data = {"user_id": user_id}
        res = run_method.post(api, data, headers=super_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], '', run_method.errInfo(res))
        self.assertEqual(corp_user_status["status"],
                         1, "无corp_id情况下user_id被删除")

    def test04_corp_user_del_errCorpId(self):
        '''case04:用户从组删除[RSM]--错误的组ID'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id)
        data = {
            "user_id": user_id,
            "corp_id": "12121313"}
        res = run_method.post(api, data, headers=super_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(corp_user_status["status"],
                         1, "无corp_id情况下user_id被删除")

    def test05_corp_user_del_noToken(self):
        '''case05:用户从组删除[RSM]--无token'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id)
        data = {
            "user_id": user_id,
            "corp_id": corp_id}
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test06_corp_user_del_success(self):
        '''case06:用户从组删除[RSM]--删除用户成功'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id)
        data = {
            "user_id": user_id,
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        sql = '''select status from corp_user where user_id = '{}' and corp_id = '{}';'''.format(
            user_id, corp_id)
        corp_user_status = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(corp_user_status["status"],
                         2, "删除失败")

    def test07_corp_user_del_multiple(self):
        '''case07:用户从组删除[RSM]--多个用户'''

        api = '/corp/user/del'
        *__, user_one = pub_param.user_reset_corp(corp_id)
        *__, user_two = pub_param.user_reset_corp(corp_id)
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=super_header)
        sql = '''select status from corp_user where user_id in ('{}','{}') and corp_id = '{}';'''.format(
            user_one, user_two, corp_id)
        corp_user_status = opera_db.get_fetchall(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        opera_assert.is_list_in(2, corp_user_status, "status")

    def test08_corp_user_del_noCorpId(self):
        '''case08:用户从组删除[RCM]--未传组ID(暂时不考虑同时在两个组)'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id)
        data = {"user_id": user_id}
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select status from corp_user where user_id = '{}' and corp_id = '{}';'''.format(
            user_id, corp_id)
        corp_user_status = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(corp_user_status["status"],
                         2, "删除失败")

    def test09_corp_user_del_multiple(self):
        '''case09:用户从组删除[RCM]--删除多个用户'''

        api = '/corp/user/del'
        *__, user_one = pub_param.user_reset_corp(corp_id)
        *__, user_two = pub_param.user_reset_corp(corp_id)
        data = {
            "user_id": "{},{}".format(user_one, user_two),
            "corp_id": corp_id}
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select status from corp_user where user_id in ('{}','{}') and corp_id = '{}';'''.format(
            user_one, user_two, corp_id)
        corp_user_status = opera_db.get_fetchall(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        opera_assert.is_list_in(2, corp_user_status, "status")

    def test10_corp_user_del_noAuth(self):
        '''case10:用户从组删除[RCM]--删除该组织其他管理员'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id, role=1 << 19)
        data = {"user_id": user_id}
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select status from corp_user where user_id = '{}' and corp_id = '{}';'''.format(
            user_id, corp_id)
        corp_user_status = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], corp_id, run_method.errInfo(res))
        self.assertEqual(corp_user_status["status"],
                         2, "删除失败")

    def test11_corp_user_del_otherCorp(self):
        '''case11:用户从组删除[RCM]--删除其他组用户'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp()
        data = {"user_id": user_id}
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(corp_user_status["status"],
                         1, "管理员删除其他组织用户成功")

    def test12_corp_user_del_noRole(self):
        '''case12:用户从组删除[普通用户]--用户在该组但无管理员权限'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id, role=1 << 19)
        data = {"user_id": user_id}
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    @unittest.skip("存在BUG，暂时跳过")
    def test13_corp_user_del_delCorpUser(self):
        '''case13:用户从组删除--已删除管理员移除用户'''

        api = '/corp/user/del'
        *__, user_id = pub_param.user_reset_corp(corp_id, role=1 << 19)
        data = {"user_id": user_id}

        # 获取该用户 token
        user_email, __, del_user_id = pub_param.user_reset_corp(
            corp_id, role=1 << 19)
        user_header = pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        pub_param.user_corp_del(del_user_id, corp_id)

        # 移除用户
        res = run_method.post(api, data, headers=user_header)
        sql = '''select status from corp_user where user_id = '{}';'''.format(
            user_id)
        corp_user_status = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertEqual(corp_user_status["status"],
                         1, "数据库查询结果:{}".format(corp_user_status))
