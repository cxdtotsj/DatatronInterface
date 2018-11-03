'''
设备类接口

test01 : /things/add

'''


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import ThingsApiData as Things
from base.base_method import BaseMethod
from data.public_param import PublicParam
from util.operation_json import OperetionJson
from util.operation_assert import OperationAssert
from util.operation_db import OperationDB
import unittest
import time


run_method = BaseMethod()
pub_param = PublicParam()
opera_json = OperetionJson()
opera_assert = OperationAssert()
opera_db = OperationDB()
super_header = pub_param.get_super_header()
corp_header, corp_id = pub_param.get_corp_user()


class TestThingsAdd(unittest.TestCase):

    def test01_things_add_noName(self):
        """case01:设备添加[RCM]--无设备名称"""

        api = '/things/add'
        data = {
            "device_name": None
        }
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test02_things_add_noToken(self):
        """case02:设备添加[RCM]--无Auth"""

        api = '/things/add'
        data = {
            "device_name": Things.device_name()
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test03_things_add_rsm(self):
        """case03:设备添加[RCM]--RSM新增"""

        api = '/things/add'
        data = {
            "device_name": Things.device_name()
        }
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test04_things_add_noRole(self):
        """case04:设备添加[普通用户]--普通用户新增"""

        api = '/things/add'
        data = {
            "device_name": Things.device_name()
        }
        common_user_header = pub_param.common_user(corp_id=corp_id)
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test05_things_add_rcm(self):
        """case05:设备添加[RCM]--RCM新增"""

        api = '/things/add'
        data = {
            "device_name": Things.device_name()
        }
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertIsNotNone(res.json()["id"], res.json())

    def test06_things_add_default_deviceType(self):
        """case06:设备添加[RCM]--默认的设备类型"""

        api = '/things/add'
        data = {
            "device_name": Things.device_name()
        }
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select device_type from thingsv2 
                    where id = "{}";'''.format(res.json()["id"])
        device_type = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(device_type["device_type"],
                         0, "数据库结果:{}".format(device_type))

    def test07_things_add_design_deviceType(self):
        """case07:设备添加[RCM]--指定的设备类型"""

        api = '/things/add'
        data = {
            "device_name": Things.device_name(),
            "device_type": "TYPE_GATEWAY"
        }
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select device_type from thingsv2 
                    where id = "{}";'''.format(res.json()["id"])
        device_type = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(device_type["device_type"],
                         1, "数据库结果:{}".format(device_type))

    def test08_things_add_design_success(self):
        """case08:设备添加[RCM]--全字段"""

        api = '/things/add'
        data = {
            "device_name": Things.device_name(),
            "device_type": "TYPE_GATEWAY",
            "device_desc": "设备说明"
        }
        res = run_method.post(api, data, headers=corp_header)
        sql = '''select device_desc from thingsv2 
                    where id = "{}";'''.format(res.json()["id"])
        device_desc = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(
            device_desc["device_desc"], data["device_desc"], "数据库结果:{}".format(device_desc))
