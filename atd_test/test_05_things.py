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


class TestThings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.opera_json = OperetionJson()
        cls.opera_assert = OperationAssert()
        cls.opera_db = OperationDB()
        cls.super_header = cls.pub_param.get_super_header()
        cls.corp_header, cls.corp_id = cls.pub_param.get_corp_user()
    
    def test01_01_things_add_noName(self):
        """case01_01:设备添加[RCM]--无设备名称"""
        
        api = '/things/add'
        data = {
            "device_name":None
        }
        res = self.run_method.post(api,data,headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())
    
    def test01_02_things_add_noToken(self):
        """case01_02:设备添加[RCM]--无Auth"""

        api = '/things/add'
        data = {
            "device_name":Things.device_name()
        }
        res = self.run_method.post(api,data)
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, res.json())

    def test01_03_things_add_rsm(self):
        """case01_03:设备添加[RCM]--RSM新增"""

        api = '/things/add'
        data = {
            "device_name":Things.device_name()
        }
        res = self.run_method.post(api,data,headers=self.super_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test01_04_things_add_noRole(self):
        """case01_04:设备添加[普通用户]--普通用户新增"""
        pass

    def test01_05_things_add_rcm(self):
        """case01_05:设备添加[RCM]--RCM新增"""
        pass

    def test01_06_things_add_default_deviceType(self):
        """case01_06:设备添加[RCM]--默认的设备类型"""
        pass

    def test01_07_things_add_design_deviceType(self):
        """case01_07:设备添加[RCM]--指定的设备类型"""
        pass

    def test01_08_things_add_design_success(self):
        """case01_08:设备添加[RCM]--全字段"""
        pass