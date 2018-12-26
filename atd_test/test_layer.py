'''
Layer相关

/layer/create
/layer/list
/layer/device/add
/layer/device/list
/layer/class/create
/layer/class/list
/layer/class/update

'''


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import BuildingApiData as Building
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
# 普通用户
common_user_header = pub_param.common_user(corp_id)
# 其他组织RCM
other_corp_header = pub_param.common_user(role=524288)


class TestLayerCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.zone_id = pub_param.create_zone(header=corp_header)
        cls.z_building = pub_param.create_building(zone_id=cls.zone_id,header=corp_header) # 园区建筑
        cls.s_building = pub_param.create_sign_building(header=corp_header) # 独栋建筑

    def setUp(self):
        self.api = '/layer/create'
        self.data = {
            "building_id":self.s_building,
            "name":"layer create testcase"
        }

    def test01_layer_create_noBuildingId(self):
        """case01:创建建筑层[RCM]--无建筑ID"""
        
        self.data.update(building_id=None)
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_layer_create_noName(self):
        """case02:创建建筑层[RCM]--无楼层名称"""
    
        self.data.update(name=None)
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_layer_create_signBuilding(self):
        """case03:创建建筑层[RCM]--独栋建筑新增楼层(数据库zone_id字段为空)"""

        res = run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 查找数据库，zone_id 是否为空
        sql = '''select zone_id from building_layer where id = '{}';'''.format(res.json()["id"])
        result = opera_db.get_fetchone(sql)
        self.assertEqual(result["zone_id"],'',"{}{}".format(result,run_method.errInfo(res)))

    def test04_layer_create_zoneBuilding(self):
        """case04:创建建筑层[RCM]--园区建筑新增楼层(数据库zone_id字段不为空)"""

        self.data.update(building_id=self.z_building)
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 查找数据库，zone_id 是否为空
        sql = '''select zone_id from building_layer where id = '{}';'''.format(res.json()["id"])
        result = opera_db.get_fetchone(sql)
        self.assertEqual(result["zone_id"],self.zone_id,"{}{}".format(result,run_method.errInfo(res)))

    def test05_layer_create_multLayer(self):
        """case05:创建建筑层[RCM]--新增多个楼层"""

        self.data.update(building_id=self.s_building)
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''select id from building_layer where building_id='{}';'''.format(self.s_building)
        num = opera_db.get_effect_row(sql)
        self.assertEqual(num,2,run_method.errInfo(res))

    def test06_layer_create_rsm(self):
        """case06:创建建筑层[RSM]--权限受限"""
        
        res = run_method.post(self.api,json=self.data,headers=super_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test07_layer_create_noRole(self):
        """case07:创建建筑层[普通用户]--权限受限"""
        
        res = run_method.post(self.api,json=self.data,headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test08_layer_create_otherCorp(self):
        """case08:创建建筑层[其他组织管理员]--权限受限"""

        res = run_method.post(self.api,json=self.data,headers=other_corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))


class TestLayerList(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # 新增园区
        cls.zone_id = pub_param.create_zone(header=corp_header) 
        # 新增园区所属建筑
        cls.building_one = pub_param.create_building(zone_id=cls.zone_id,header=corp_header)
        cls.building_two = pub_param.create_building(zone_id=cls.zone_id,header=corp_header)
        # 新增 building_one 所属楼层
        cls.layer_one = pub_param.create_building_layer(cls.building_one,corp_header)
        # 新增 building_two 所属楼层
        for _ in range(0,2):
            pub_param.create_building_layer(cls.building_two,corp_header)

    def setUp(self):
        self.api = '/layer/list'
        self.data = {
            "page":1,
            "limit":50
        }

    def test01_layer_list_noId(self):
        """case01:获取层列表[RCM]--无ID"""
        
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_layer_list_layerId(self):
        """case02:获取层列表[RCM]--只传楼层ID"""

        self.data.update(layer_id=self.layer_one)
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], '1', run_method.errInfo(res))
        self.assertEqual(res.json()["data_list"][0]["id"], self.layer_one, run_method.errInfo(res))

    def test03_layer_list_buildingId(self):
        """case03:获取层列表[RCM]--只传建筑ID"""

        self.data.update(building_id=self.building_two)
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], '2', run_method.errInfo(res)) # building_two 有2个楼层
        opera_assert.is_list_in(self.building_two,res.json()["data_list"],"building_id")

    def test04_layer_list_zoneId(self):
        """case04:获取层列表[RCM]--只传园区ID"""

        self.data.update(zone_id=self.zone_id)
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], '3', run_method.errInfo(res)) # zone 有3个楼层
        opera_assert.is_list_in(self.zone_id,res.json()["data_list"],"zone_id")

    # def test05_layer_list_zoneBuildId(self):
    #     """case05:获取层列表[RCM]--同时传园区建筑ID"""

    #     self.data.update({
    #         "zone_id":self.zone_id,
    #         "building_id":self.building_two
    #     })
    #     res = run_method.post(self.api,self.data,headers=corp_header)
    #     self.assertEqual(res.status_code, 200, run_method.errInfo(res))
    #     self.assertEqual(res.json()["total"], '2', run_method.errInfo(res)) # building_two 有2个楼层
    #     opera_assert.is_list_in(self.building_two,res.json()["data_list"],"building_id")

    # def test06_layer_list_zoneLayerId(self):
    #     """case06:获取层列表[RCM]--同时传园区楼层ID"""

    #     self.data.update({
    #         "zone_id":self.zone_id,
    #         "layer_id":self.layer_one
    #     })
    #     res = run_method.post(self.api,self.data,headers=corp_header)
    #     self.assertEqual(res.status_code, 200, run_method.errInfo(res))
    #     self.assertEqual(res.json()["total"], '1', run_method.errInfo(res)) 
    #     self.assertEqual(res.json()["data_list"][0]["id"], self.layer_one, run_method.errInfo(res))        

    # def test07_layer_list_buildLayerId(self):
    #     """case07:获取层列表[RCM]--同时传建筑楼层ID"""

    #     self.data.update({
    #         "building_id":self.building_one,
    #         "layer_id":self.layer_one
    #     })
    #     res = run_method.post(self.api,self.data,headers=corp_header)
    #     self.assertEqual(res.status_code, 200, run_method.errInfo(res))
    #     self.assertEqual(res.json()["total"], '1', run_method.errInfo(res)) 
    #     self.assertEqual(res.json()["data_list"][0]["id"], self.layer_one, run_method.errInfo(res))  

    # def test08_layer_list_zoneBuildLayerId(self):
    #     """case08:获取层列表[RCM]--同时传园区建筑楼层ID"""

    #     self.data.update({
    #         "zone_id":self.zone_id,
    #         "building_id":self.building_one,
    #         "layer_id":self.layer_one
    #     })
    #     res = run_method.post(self.api,self.data,headers=corp_header)
    #     self.assertEqual(res.status_code, 200, run_method.errInfo(res))
    #     self.assertEqual(res.json()["total"], '1', run_method.errInfo(res)) 
    #     self.assertEqual(res.json()["data_list"][0]["id"], self.layer_one, run_method.errInfo(res))


class TestLayerDeviceAdd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = '/layer/device/add'
        building_id = pub_param.create_building(header=corp_header)
        cls.guidList,__ = pub_param.get_guidList(
            building_id, corp_header, "LangChaV2.objr")[:20]
        cls.layer_id = pub_param.create_building_layer(building_id,corp_header)
        cls.class_id = pub_param.create_layer_class(header=corp_header)
        # use to class devicelist
        opera_json.check_json_value(
            "deviceadd", {"layer_id": cls.layer_id})
        
    def test00_layer_device_add_noLevel(self):
        """case00:添加关联设备[RCM]--无可视等级"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "things_id": device_id,
            "level": None,
            "class_id": self.class_id,
            "type": "extra",
            "url": "https://www.baidu.com",
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle": 0
            }
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["level"], "UNKNOWN", run_method.errInfo(res))

    def test01_layer_device_add_noLayerId(self):
        """case01:添加关联设备[RCM]--无楼层ID"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": None,
            "guid": self.guidList[0],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim"
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_layer_device_add_noThingsId(self):
        """case02:添加关联设备[RCM]--无设备ID"""

        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[1],
            "things_id": None,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim"
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_layer_device_add_noType(self):
        """case03:添加关联设备[RCM]--无设备关联类型"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[2],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": None
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test04_layer_device_add_bim_noGU(self):
        """case04:添加关联设备[RCM]--类型为BIM,无guid,无url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": None,
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim",
            "url": None
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_layer_device_add_bim_guid(self):
        """case05:添加关联设备[RCM]--类型为BIM,有guid,无url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[3],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim",
            "url": None
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''select * from building_layer_things where id = '{}';'''.format(res.json()[
                                                                                "id"])
        device_data = opera_db.get_fetchone(sql)
        self.assertIsNotNone(res.json()["id"], run_method.errInfo(res))
        self.assertIsNotNone(device_data, run_method.errInfo(res))

    def test06_layer_device_add_bim_url(self):
        """case06:添加关联设备[RCM]--类型为BIM,无guid,有url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": None,
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim",
            "url": "https://www.baidu.com"
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test07_layer_device_add_bim_GU(self):
        """case07:添加关联设备[RCM]--类型为BIM,有guid,有url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[4],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim",
            "url": "https://www.baidu.com"
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''select * from building_layer_things where id = '{}';'''.format(res.json()[
                                                                                "id"])
        device_data = opera_db.get_fetchone(sql)
        self.assertIsNotNone(res.json()["id"], run_method.errInfo(res))
        self.assertIsNotNone(device_data, run_method.errInfo(res))

    def test08_layer_device_add_extra_noUCG(self):
        """case08:添加关联设备[RCM]--类型为extra，无url,无coord,无guid"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": None,
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "extra",
            "url": None,
            "coord": None
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test09_layer_device_add_extra_url(self):
        """case09:添加关联设备[RCM]--类型为extra，无url,无coord,有guid"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[5],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "extra",
            "url": None,
            "coord": None
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test10_layer_device_add_extra_url(self):
        """case10:添加关联设备[RCM]--类型为extra，有url，无coord"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "extra",
            "url": "https://www.baidu.com",
            "coord": None
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test11_layer_device_add_extra_coord(self):
        """case11:添加关联设备[RCM]--类型为extra，无url,有coord"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "extra",
            "url": None,
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle": 0
            }
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test12_layer_device_add_UC(self):
        """case12:添加关联设备[RCM]--类型为extra，有url,有coord"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "extra",
            "url": "https://www.baidu.com",
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle": 0
            }
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''select * from building_layer_things where id = '{}';'''.format(res.json()[
                                                                                "id"])
        device_data = opera_db.get_fetchone(sql)
        self.assertIsNotNone(res.json()["id"], run_method.errInfo(res))
        self.assertIsNotNone(device_data, run_method.errInfo(res))
        opera_json.check_json_value("test12_layer_device_add",device_id)

    # 依赖用例 test12_layer_device_add
    def test13_layer_device_add_diffClassId(self):
        """case13:添加关联设备[RCM]--类型为extra，有url,有coord"""

        class_id = pub_param.create_layer_class(header=corp_header)
        device_id = opera_json.get_data("test12_layer_device_add")
        data = {
            "layer_id": self.layer_id,
            "things_id": device_id,
            "level": 7,
            "class_id": class_id,
            "type": "extra",
            "url": "https://www.baidu.com",
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle": 0
            }
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''select * from building_layer_things where id = '{}';'''.format(res.json()[
                                                                                "id"])
        device_data = opera_db.get_fetchone(sql)
        self.assertIsNotNone(res.json()["id"], run_method.errInfo(res))
        self.assertIsNotNone(device_data, run_method.errInfo(res))

    def test13_layer_device_add_rsm(self):
        """case13:添加关联设备[RSM]--新增无权限"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[6],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim"
        }
        res = run_method.post(self.api, json=data, headers=super_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test14_layer_device_add_noRole(self):
        """case14:添加关联设备[普通用户]--新增无权限"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[7],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim"
        }
        res = run_method.post(self.api, json=data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test15_layer_device_add_otherCorp(self):
        """case15:添加关联设备[其他组织RCM]--新增无权限"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[8],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim"
        }
        res = run_method.post(self.api, json=data, headers=other_corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test16_layer_device_add_noAuth(self):
        """case16:添加关联设备--无Auth"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "guid": self.guidList[9],
            "things_id": device_id,
            "level": 7,
            "class_id": self.class_id,
            "type": "bim"
        }
        res = run_method.post(self.api, json=data)
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

    def test17_layer_device_add_noClassId(self):
        """case17:添加关联设备--无数据模式"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "layer_id": self.layer_id,
            "things_id": device_id,
            "level": 7,
            "class_id": None,
            "type": "extra",
            "url": "https://www.baidu.com",
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle": 0
            }
        }
        res = run_method.post(self.api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))


class TestLayerDeviceList(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        front_dlist = pub_param.front_deviceList(corp_header)
        cls.cid_one = front_dlist[1]        # class 1
        cls.cid_two = front_dlist[2]        # class 2
        cls.zone_id = front_dlist[0][0]     # zone
        cls.bid_one = front_dlist[0][1]     # building_one
        cls.layer_oo = front_dlist[0][3]    # building_one--layer_one
        # cls.cid_one = 'ci-121914597971080209'
        # cls.cid_two = 'ci-121914599833351185'
        # cls.zone_id = 'ci-121914591847396369'
        # cls.bid_one = 'ci-121914593709667345'
        # cls.layer_oo = 'ci-121914595756487697'


    def setUp(self):
        self.api = '/layer/device/list'
        self.data = {
            "level": 1,
            "class_id": self.cid_one,
            "zone_id": None,
            "building_id": None,
            "layer_id": None
        }

    def test01_layer_device_list_noLevel(self):
        """case01:获取所有设备列表--无可视等级"""

        self.data.update(level=None)
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 0, run_method.errInfo(res))

    def test02_layer_device_list_noClassId(self):
        """case02:获取所有设备列表--无数据模式"""

        self.data.update(class_id=None)
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 0, run_method.errInfo(res))

    def test03_layer_device_list_zoneL1C1(self):
        """case03:获取所有设备列表--zone、level1、class1"""

        self.data.update({
            "zone_id": self.zone_id
        })
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 7, run_method.errInfo(res))

    def test04_layer_device_list_zoneL1C2(self):
        """case04:获取所有设备列表--zone、level1、class2"""

        self.data.update({
            "class_id": self.cid_two,
            "zone_id": self.zone_id
        })
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 7, run_method.errInfo(res))

    def test05_layer_device_list_buildingL2C1(self):
        """case05:获取所有设备列表--building、level2、class1"""

        self.data.update({
            "level": 2,
            "building_id": self.bid_one
        })
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 5, run_method.errInfo(res))

    def test06_layer_device_list_buildingL2C2(self):
        """case06:获取所有设备列表--building、level2、class2"""

        self.data.update({
            "level": 2,
            "class_id": self.cid_two,
            "building_id": self.bid_one
        })
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 3, run_method.errInfo(res))

    def test07_layer_device_list_layerL3C1(self):
        """case07:获取所有设备列表--layer、level4、class1"""

        self.data.update({
            "level": 4,
            "layer_id": self.layer_oo
        })
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 3, run_method.errInfo(res))

    def test08_layer_device_list_layerL3C2(self):
        """case08:获取所有设备列表--layer、level4、class2"""

        self.data.update({
            "level": 4,
            "class_id": self.cid_two,
            "layer_id": self.layer_oo
        })
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 2, run_method.errInfo(res))