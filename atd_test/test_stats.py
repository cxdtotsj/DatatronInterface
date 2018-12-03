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

class StatisticGetdatalatest(unittest.TestCase):
    """/statistic/getdatalatestinf 接口用例"""

    @classmethod
    def setUpClass(cls):
        """使用 demo 账号"""
        cls.demo_heaher = pub_param.user_login("123456","demo")

    def setUp(self):
        self.api = '/statistic/getdatalatestinf'
        self.data = {
            "name": "Lamp_6_feedback",
            "things_id": "117461379685823535"    
        }

    def test01_statistic_getdatalatestinf_noThingsId(self):
        """case01:获取最新统计数据[RCM]--无设备ID"""
        
        self.data.update(things_id=None)
        res = run_method.post(self.api,json=self.data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1000,run_method.errInfo(res))
        
    def test02_statistic_getdatalatestinf_noName(self):
        """case02:获取最新统计数据[RCM]--无属性名称"""

        self.data.update(name=None)
        res = run_method.post(self.api,json=self.data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(len(res.json()["data_list"]),0,run_method.errInfo(res))

    def test03_statistic_getdatalatestinf_errThingsId(self):
        """case03:获取最新统计数据[RCM]--错误的设备ID"""

        self.data.update(things_id="112233")
        res = run_method.post(self.api,json=self.data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]),0,run_method.errInfo(res))

    def test04_statistic_getdatalatestinf_errName(self):
        """case04:获取最新统计数据[RCM]--错误的属性名称"""

        self.data.update(name="abc")
        res = run_method.post(self.api,json=self.data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]),0,run_method.errInfo(res))

    def test05_statistic_getdatalatestinf_success(self):
        """case05:获取最新统计数据[RCM]--输入ID和name"""

        self.data.update(data_source=0)
        res = run_method.post(self.api,json=self.data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(len(res.json()["data_list"]),0,run_method.errInfo(res))

@unittest.skip("开发中")
class StatisticQueryinf(unittest.TestCase):

    def test01_statistic_quertinf_noMeasurements(self):
        """case01:查询设备数据[RCM]--无设备ID"""
        pass

    def test02_statistic_quertinf_oneMeasurements(self):
        """case02:查询设备数据[RCM]--一个设备ID"""
        pass

    def test03_statistic_quertinf_noFields(self):
        """case03:查询设备数据[RCM]--无设备属性"""
        pass

    def test04_statistic_quertinf_oneFields(self):
        """case04:查询设备数据[RCM]--一个设备属性"""
        pass

    def test05_statistic_quertinf_multFields(self):
        """case05:查询设备数据[RCM]--多个设备属性"""
        pass

    def test06_statistic_quertinf_fieldFuncs_mean(self):
        """case06:查询设备数据[RCM]--对属性值求平均值"""
        pass

    def test07_statistic_quertinf_fieldFuncs_sum(self):
        """case07:查询设备数据[RCM]--对属性值求和"""
        pass

    def test08_statistic_quertinf_formTo(self):
        """case08:查询设备数据[RCM]--查找的时间范围(默认:time>now()-8h)"""
        pass

    def test09_statistic_quertinf_groupBy(self):
        """case09:查询设备数据[RCM]--聚合十分钟(含时间段)"""
        pass