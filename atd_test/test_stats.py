'''
Stats:

/statistic/getdatalatestinf
/statistic/querybatchinf
/stats/statsinfo

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


class StatisticQuerybatchinf(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """使用 demo 账号"""
        cls.demo_heaher = pub_param.user_login("123456","demo")
        cls.ut24 = pub_param.beforeUTC(24)
        cls.api = '/statistic/querybatchinf'

    def test01_statistic_quertinf_oneMeasurements(self):
        """case01:查询设备数据[RCM]--一个设备ID"""

        data = {
            "query_list":[
                {
                    "measurement": "117461383276147759",
                    "fields":[
                        "CO2_1"
                    ],
                    "from":self.ut24
                }
            ]
        }
        res = run_method.post(self.api,json=data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        # self.assertIsNotNone(res.json()["data_list"][0]["values"],run_method.errInfo(res)) # 设备有问题

    def test02_statistic_quertinf_fieldFuncs_sum(self):
        """case02:查询设备数据[RCM]--对属性值求和"""

        data = {
            "query_list":[
                {
                    "measurement": "117461383276147759",
                    "fields":[
                        "CO2_1"
                    ],
                    "field_funcs":{"CO2_1":"SUM"},
                    "from":self.ut24
                }
            ]
        }
        res = run_method.post(self.api,json=data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        # self.assertIsNotNone(res.json()["data_list"][0]["values"],run_method.errInfo(res)) # 设备有问题

    def test03_statistic_quertinf_groupBy(self):
        """case03:查询设备数据[RCM]--聚合1小时(含时间段)"""

        data = {
            "query_list":[
                {
                    "measurement": "117461383276147759",
                    "fields":[
                        "CO2_1"
                    ],
                    "field_funcs":{"CO2_1":"SUM"},
                    "aggregation_raw":"time(1h)",
                    "from":self.ut24
                }
            ]
        }
        res = run_method.post(self.api,json=data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        # self.assertTrue(len(res.json()["data_list"][0]["values"])>=24,run_method.errInfo(res)) # 设备有问题

    def test04_statistic_quertinf_multFields(self):
        """case04:查询设备数据[RCM]--多个设备属性"""

        data = {
            "query_list":[
                {
                    "measurement": "117461404985865263",
                    "fields":[
                        "EP",
                        "EQ"
                    ],
                    "from":self.ut24
                }
            ]
        }
        res = run_method.post(self.api,json=data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))

    def test05_statistic_quertinf_multMeasurements(self):
        """case05:查询设备数据[RCM]--多个设备ID"""

        data = {
            "query_list":[
                {
                    "measurement": "117461383276147759",
                    "fields":[
                        "CO2_1"
                    ],
                    "aggregation_raw":"time(6h)",
                    "from":self.ut24
                },
                {
                    "measurement": "117461379601937455",
                    "fields":[
                        "CO2_2"
                    ],
                    "aggregation_raw":"time(6h)",
                    "from":self.ut24
                }
            ]
        }
        res = run_method.post(self.api,json=data,headers=self.demo_heaher)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        # self.assertIsNotNone(res.json()["data_list"][0]["values"],run_method.errInfo(res))
        # self.assertIsNotNone(res.json()["data_list"][1]["values"],run_method.errInfo(res))
        # self.assertEqual(len(res.json()["data_list"]),2,run_method.errInfo(res))
    
class TestStatsinfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.opera_db = OperationDB()
        cls.super_header = pub_param.get_super_header()
        cls.corp_header, cls.corp_id = pub_param.get_corp_user()
        # 普通用户
        cls.common_user_header = pub_param.common_user(cls.corp_id)

    def setUp(self):
        self.api = '/stats/statsinfo'

    def test01_statsinfo_zone_area_rcm(self):
        """case01:获得园区总面积[RCM]--获取组织内所有园区面积"""

        sql = '''select sum(area) area from zone where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        area = self.opera_db.get_fetchone(sql)["area"]
        res = run_method.post(self.api,headers=self.corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["zone_area"],area,run_method.errInfo(res))

    def test02_statsinfo_zone_area_rsm(self):
        """case02:获得园区总面积[RSM]--获取所有园区面积"""

        sql = '''select sum(area) area from zone where status in (1,2);'''
        area = self.opera_db.get_fetchone(sql)["area"]
        res = run_method.post(self.api,headers=self.super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["zone_area"],area,run_method.errInfo(res))

    def test03_statsinfo_zone_area_noRole(self):
        """case03:获得园区总面积[普通用户]--获取组织内所有园区面积"""

        sql = '''select sum(area) area from zone where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        area = self.opera_db.get_fetchone(sql)["area"]
        res = run_method.post(self.api,headers=self.common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["zone_area"],area,run_method.errInfo(res))

    def test04_statsinfo_zone_num_rcm(self):
        """case04:获得园区数量[RCM]--获取组织内园区数量"""

        sql = '''select id from zone where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        total = self.opera_db.get_effect_row(sql)
        res = run_method.post(self.api,headers=self.corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["zone_num"],str(total),run_method.errInfo(res))

    def test05_statsinfo_zone_num_rsm(self):
        """case05:获得园区数量[RSM]--获取所有园区数量"""

        sql = '''select id from zone where status in (1,2);'''
        total = self.opera_db.get_effect_row(sql)
        res = run_method.post(self.api,headers=self.super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["zone_num"],str(total),run_method.errInfo(res))

    def test06_statsinfo_zone_num_noRole(self):
        """case06:获得园区数量[普通用户]--获取组织内园区数量"""

        sql = '''select id from zone where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        total = self.opera_db.get_effect_row(sql)
        res = run_method.post(self.api,headers=self.common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["zone_num"],str(total),run_method.errInfo(res))

    def test07_statsinfo_building_area_rcm(self):
        """case07:获得建筑总面积[RCM]--获取组织内所有建筑面积"""

        sql = '''select sum(area) area from building where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        area = self.opera_db.get_fetchone(sql)["area"]
        res = run_method.post(self.api,headers=self.corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["building_area"],float(area),run_method.errInfo(res))

    def test08_statsinfo_zone_area_rsm(self):
        """case08:获得建筑总面积[RSM]--获取所有建筑面积"""

        sql = '''select sum(area) area from building where status in (1,2);'''
        area = self.opera_db.get_fetchone(sql)["area"]
        res = run_method.post(self.api,headers=self.super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["building_area"],float(area),run_method.errInfo(res))

    def test09_statsinfo_zone_area_noRole(self):
        """case09:获得建筑总面积[普通用户]--获取组织内所有建筑面积"""

        sql = '''select sum(area) area from building where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        area = self.opera_db.get_fetchone(sql)["area"]
        res = run_method.post(self.api,headers=self.common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["building_area"],float(area),run_method.errInfo(res))

    def test10_statsinfo_zone_num_rcm(self):
        """case10:获得建筑数量[RCM]--获取组织内建筑数量"""

        sql = '''select id from building where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        total = self.opera_db.get_effect_row(sql)
        res = run_method.post(self.api,headers=self.corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["building_num"],str(total),run_method.errInfo(res))

    def test11_statsinfo_zone_num_rsm(self):
        """case11:获得建筑数量[RSM]--获取所有建筑数量"""

        sql = '''select id from building where status in (1,2);'''
        total = self.opera_db.get_effect_row(sql)
        res = run_method.post(self.api,headers=self.super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["building_num"],str(total),run_method.errInfo(res))

    def test12_statsinfo_zone_num_noRole(self):
        """case12:获得建筑数量[普通用户]--获取组织内建筑数量"""

        sql = '''select id from building where status in (1,2) and corp_id = '{}';'''.format(self.corp_id)
        total = self.opera_db.get_effect_row(sql)
        res = run_method.post(self.api,headers=self.common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["building_num"],str(total),run_method.errInfo(res))
    
    def test13_statsinfo_prov_num_rsm(self):
        """case13:获得省份数量[RSM]--获取所有项目省份数量"""

        res = run_method.post(self.api,headers=self.super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["prov_num"],'0',run_method.errInfo(res))

    def test14_statsinfo_prov_num_rcm(self):
        """case14:获得省份数量[RCM]--获取组织内项目省份数量"""

        res = run_method.post(self.api,headers=self.corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["prov_num"],'0',run_method.errInfo(res))

    def test15_statsinfo_prov_num_noRole(self):
        """case15:获得省份数量[普通用户]--获取组织内项目省份数量"""

        res = run_method.post(self.api,headers=self.common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["prov_num"],'0',run_method.errInfo(res))

    def test16_statsinfo_city_num_rsm(self):
        """case16:获得城市数量[RSM]--获取所有项目城市数量"""

        res = run_method.post(self.api,headers=self.super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["city_num"],'0',run_method.errInfo(res))

    def test17_statsinfo_city_num_rcm(self):
        """case17:获得城市数量[RCM]--获取所有项目城市数量"""

        res = run_method.post(self.api,headers=self.corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["city_num"],'0',run_method.errInfo(res))

    def test18_statsinfo_city_num_noRole(self):
        """case18:获得城市数量[普通用户]--获取所有项目城市数量"""

        res = run_method.post(self.api,headers=self.common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["city_num"],'0',run_method.errInfo(res))