'''园区类接口'''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import ZoneApiData as Zone
from base.base_method import BaseMethod
from base.public_param import PublicParam
from util.operation_json import OperetionJson
import unittest
import json


class TestZone(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.super_header = cls.pub_param.get_super_header()
        cls.corp_header, cls.corp_id = cls.pub_param.get_corp_header()
        cls.opera_json = OperetionJson()

    def test01_01_zone_create_noName(self):
        '''case01_01:创建园区--无园区名称'''
        api = '/zone/create'
        data = {
            "area": 100,
            "building_num": 19,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_02_zone_create_noBuildNum(self):
        '''case01_02:创建园区--无楼宇数量'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_03_zone_create_noArea(self):
        '''case01_03:创建园区--无面积(默认为0)'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "building_num": 31,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 200, "状态码返回出错误")
        self.assertEqual(res_dict["area"], 0, res_dict)

    def test01_04_zone_create_noLoc(self):
        '''case01_04:创建园区--无地址'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "building_num": 31,
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_05_zone_create_noCoord(self):
        '''case01_05:创建园区--无经纬度'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "building_num": 31,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_06_zone_create_noExtra(self):
        '''case01_06:创建园区[ZCM]--无附加信息'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "building_num": 19,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 200, "状态码返回出错误")
        self.assertEqual(res_dict["corpId"], self.corp_id, res_dict)
    
        self.opera_json.check_json_value(
            "test01_06_zone_create_noExtra", res_dict["name"])

    def test01_07_zone_create_success(self):
        '''case01_07:创建园区[ZCM]--新增成功(全部信息)'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "building_num": 19,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            },
            "extra": {
                "build_corp": "建筑单位名称",
                "build_start_at": "2018-10-09",
                "construct_corp": "规划单位名称",
                "construct_end_at": "2018-10-09",
                "design_corp": "设计单位名称",
                "design_end_at": "2018-10-09",
                "plan_corp": "施工单位名称",
                "plan_end_at": "2018-10-09",
                "supervise_corp": "监理单位名称",
                "supervise_end_at": "2018-10-09"
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 200, "状态码返回出错误")
        self.assertEqual(res_dict["corpId"], self.corp_id, res_dict)

        self.opera_json.check_json_value("test01_07_zone_create_success", {
                                         "zone_id": res_dict["id"], "data": data})

    def test01_08_zone_create_nameRepeat(self):
        '''case01_08:创建园区[ZCM]--园区名称重复'''
        api = '/zone/create'
        # 依赖用例 test01_06_zone_create_noExtra
        repeat_name = self.opera_json.get_data("test01_07_zone_create_success")
        data = {
            "name": repeat_name,
            "area": 100,
            "building_num": 19,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1409, res_dict)

    def test01_09_zone_create_noCorpId(self):
        '''case01_09:创建园区[ZSM]--无CorpID'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "building_num": 19,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.super_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_10_zone_create_corpId(self):
        '''case01_10:创建园区[ZSM]--新增成功(指定CorpID)'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "building_num": 19,
            "corp_id": self.corp_id,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(api, json=data, headers=self.super_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 200, "状态码返回出错误")
        self.assertEqual(res_dict["corpId"], self.corp_id, res_dict)

    def test01_11_zone_create_noRole(self):
        '''case01_11:创建园区--普通组织用户新增'''
        api = '/zone/create'
        data = {
            "name": Zone.zone_name,
            "area": 100,
            "building_num": 19,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0
            }
        }
        res = self.run_method.post(
            api, json=data, headers=self.pub_param.common_user(self.corp_id))
        res_dict = res.json()
        self.assertEqual(res.status_code, 403, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1403, res_dict)

    def test02_01_zone_get_noId(self):
        '''case02_01:获取园区详细信息--无园区ID'''
        api = "/zone/get"
        data = {"id": None}
        res = self.run_method.post(api, data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1404, res_dict)

    def test02_02_zone_get_otherId(self):
        '''case02_02:获取园区详细信息[ZCM]--其他组织的园区'''
        api = "/zone/get"
        # 创建其他组织园区
        zone_id = self.pub_param.create_zone()
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, "状态码返回出错误")
        self.assertEqual(res_dict["code"], 1403, res_dict)

    def test02_03_zone_get_success(self):
        '''case02_03:获取园区详细信息[ZCM]--所在组织的园区'''
        api = "/zone/get"
        # 依赖用例 test01_07_zone_create_success
        zone_id = self.opera_json.get_data("test01_07_zone_create_success")["zone_id"]
        zone_data = self.opera_json.get_data("test01_07_zone_create_success")["data"]
        zone_list = [(k,v) for k,v in zone_data.items()]
        print(zone_list)
        print(type(zone_list))
        #print(zone_data)
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        print("---------------------------------------------------------------")
        res_list = [(k,v) for k,v in res.json().items()]
        print(res_list)
        self.assertEqual(res.status_code, 200, "状态码返回出错误")
        # self.assertIn(zone_value,res_value)
        print(zone_list in res_list)


    def test02_04_zone_get_zsm(self):
        '''case02_04:获取园区详细信息[ZSM]'''
        pass

    def test02_05_zone_get_noRole(self):
        '''case02_05:获取园区详细信息--普通组织用户'''
        pass

    def test02_06_zone_get_noRole(self):
        '''case02_06:获取园区详细信息--错误的园区ID'''
        pass

    def test03_01_zone_list_noPage(self):
        '''case03_01:园区列表--未传page'''
        pass

    def test03_02_zone_list_errPageType(self):
        '''case03_02:园区列表--错误的page参数'''
        pass

    def test03_03_zone_list_noSize(self):
        '''case03_03:园区列表--未传size'''
        pass

    def test03_04_zone_list_errSizeType(self):
        '''case03_04:园区列表--错误的size参数'''
        pass

    def test03_05_zone_list_success(self):
        '''case03_05:园区列表[ZCM]--查看成功(total数量)'''
        pass

    def test03_06_zone_list_zsm(self):
        '''case03_06:园区列表[ZSM]--超级管理员(total数量)'''
        pass

    def test03_07_zone_list_noRole(self):
        '''case03_07:园区列表--组织普通用户'''
        pass

    # 编辑园区

    # 删除园区

    def test05_01_zone_del_noId(self):
        '''case05_01:删除园区--无ID'''
        pass

    def test05_02_zone_del_success(self):
        '''case05_02:删除园区[ZCM]--删除成功'''
        pass

    def test05_03_zone_del_success(self):
        '''case05_03:删除园区[ZSM]--删除成功'''
        pass
