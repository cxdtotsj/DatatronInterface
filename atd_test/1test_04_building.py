'''建筑类接口'''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import BuildingApiData as Building
from base.base_method import BaseMethod
from base.public_param import PublicParam
from util.operation_json import OperetionJson
from util.operation_assert import OperationAssert
from util.operation_db import OperationDB
import unittest


class TestBuilding(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.opera_json = OperetionJson()
        cls.opera_assert = OperationAssert()
        cls.opera_db = OperationDB()
        cls.super_header = cls.pub_param.get_super_header()
        cls.corp_header, cls.corp_id = cls.pub_param.get_corp_user()

    def test01_01_building_create_noName(self):
        '''case01_01:创建建筑--无建筑名称'''
        api = '/building/create'
        data = Building.building_data()
        data.pop("name")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1400, "状态码返回错误")

    def test01_02_building_create_noLoc(self):
        '''case01_02:创建建筑--无地址'''
        api = '/building/create'
        data = Building.building_data()
        data.pop("loc")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, "状态码返回错误")

    def test01_03_building_create_noArea(self):
        '''case01_03:创建建筑--无面积'''
        api = '/building/create'
        data = Building.building_data()
        data.pop("area")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        building_detail = self.pub_param.building_get(
            res.json()["id"], self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(building_detail["area"], 0, "面积默认值返回错误")

    def test01_04_buliding_create_noLayer(self):
        '''case01_04:创建建筑--无层数'''
        api = '/building/create'
        data = Building.building_data()
        data.pop("layer_num")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        building_detail = self.pub_param.building_get(
            res.json()["id"], self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(building_detail["layer_num"], 0, "楼层数默认值返回错误")

    def test01_05_buliding_create_noUnderlayer(self):
        '''case01_05:创建建筑--无地下层数'''
        api = '/building/create'
        data = Building.building_data()
        data.pop("underlayer_num")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        try:
            building_detail = self.pub_param.building_get(
                res.json()["id"], self.corp_header)
        except KeyError:
            print(res.json())
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(building_detail["underlayer_num"], 0, "地下层数默认值返回错误")

    def test01_06_building_create_noCoord(self):
        '''case01_06:创建建筑--无经纬度'''
        api = '/building/create'
        data = Building.building_data()
        data.pop("coord")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, "状态码返回错误")

    def test01_07_building_create_noZoneId(self):
        '''case01_07:创建建筑[ZCM]--不属于园区建筑(无附加信息)'''
        api = '/building/create'
        data = Building.building_data()
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        try:
            building_detail = self.pub_param.building_get(
                res.json()["id"], self.corp_header)
        except KeyError:
            print(res.json())
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["corp_id"], self.corp_id, "组织ID返回错误")
        self.assertEqual(building_detail["zone_id"], "", "独栋建筑存在园区ID")

        self.opera_json.check_json_value(
            "test01_07_building", {"id": res.json()["id"], "name": data["name"], "data": data})

    def test01_08_building_create_ZoneId(self):
        '''case01_08:创建建筑[ZCM]--属于园区建筑(无附加信息)'''
        zone_id = self.pub_param.create_zone(self.corp_header)
        api = '/building/create'
        data = Building.building_data()
        data.update(zone_id=zone_id)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        building_detail = self.pub_param.building_get(
            res.json()["id"], self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["corp_id"], self.corp_id, "组织ID返回错误")
        self.assertEqual(building_detail["zone_id"], zone_id, "园区建筑不存在园区ID")

    def test01_09_building_create_success(self):
        '''case01_09:创建建筑[ZCM]--新增成功(全部信息)'''
        zone_id = self.pub_param.create_zone(self.corp_header)
        api = '/building/create'
        data = Building.building_data()
        data.update({
            "zone_id": zone_id,
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
        })
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        building_detail = self.pub_param.building_get(
            res.json()["id"], self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["corp_id"], self.corp_id, "组织ID返回错误")
        self.assertEqual(building_detail["zone_id"], zone_id, "园区建筑不存在园区ID")

        self.opera_json.check_json_value("test01_09_building", {"id": res.json()[
                                         "id"], "name": data["name"], "data": data})

    # 依赖用例 test01_07_building_create_noZoneId
    def test01_10_building_create_nameRepeat(self):
        '''case01_10:创建建筑[ZCM]--名称重复(无ZoneID,不同的corp_id)'''
        repeat_name = self.opera_json.get_data(
            "test01_07_building")["name"]
        ohter_corp_header = self.pub_param.common_user(role=524288)
        api = '/building/create'
        data = Building.building_data()
        data.update(name=repeat_name)
        res = self.run_method.post(api, json=data, headers=ohter_corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["corp_id"], ohter_corp_header, "组织ID返回错误")

    # 依赖用例 test01_07_building_create_noZoneId
    def test01_11_building_create_nameRepeat(self):
        '''case01_11:创建建筑[ZCM]--名称重复(无ZoneID,相同的corp_id)'''
        repeat_name = self.opera_json.get_data(
            "test01_07_building")["name"]
        api = '/building/create'
        data = Building.building_data()
        data.update(name=repeat_name)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1409, res.json())

    # 依赖用例 test01_09_building_create_success
    def test01_12_building_create_nameRepeat(self):
        '''case01_12:创建建筑[ZCM]--名称重复(相同ZoneID)'''
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        building_detail = self.pub_param.building_get(
            building_id, self.corp_header)
        api = '/building/create'
        data = Building.building_data()
        data.update({
            "name": building_detail["name"],
            "zone_id": building_detail["zone_id"]
        })
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1409, res.json())

    # 依赖用例 test01_09_building_create_success
    def test01_13_building_create_nameRepeat(self):
        '''case01_13:创建建筑[ZCM]--名称重复(不同ZoneID)'''
        repeat_name = self.opera_json.get_data("test01_09_building")["name"]
        zone_id = self.pub_param.create_zone(self.corp_header)
        api = '/building/create'
        data = Building.building_data()
        data.update({
            "name": repeat_name,
            "zone_id": zone_id,
        })
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["corp_id"], self.corp_id, "组织ID返回错误")

    def test01_14_building_create_rsm(self):
        '''case01_14:创建建筑[ZSM]--超级管理员新增(角色受限)'''
        api = '/building/create'
        data = Building.building_data()
        res = self.run_method.post(api, json=data, headers=self.super_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test01_15_building_create_noRole(self):
        '''case01_15:创建建筑--普通组织用户新增(角色受限)'''
        common_user_header = self.pub_param.common_user(self.corp_id)
        api = '/building/create'
        data = Building.building_data()
        res = self.run_method.post(api, json=data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())
        
    def test02_01_building_get_noId(self):
        '''case02_01:获取建筑详细信息--无建筑ID'''
        api = '/building/get'
        data = {"id": None}
        res = self.run_method.post(api, data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1404, "状态码返回错误")

    def test02_02_building_get_errId(self):
        '''case02_02:获取建筑详细信息[ZCM]--其他组织的建筑'''
        other_building_id = self.pub_param.create_building()
        api = '/building/get'
        data = {"id": other_building_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1403, "状态码返回错误")

    def test02_03_building_get_success(self):
        '''case02_03:获取建筑详细信息[ZCM]--所在组织的建筑'''
        pass

    def test02_04_building_get_zsm(self):
        '''case02_04:获取建筑详细信息[ZSM]'''
        pass

    def test02_06_building_get_noRole(self):
        '''case02_06:获取建筑详细信息--普通组织用户'''
        pass

    def test03_01_building_list_noPage(self):
        '''case03_01:建筑列表--未传page'''
        pass

    def test03_02_building_list_errPageType(self):
        '''case03_02:建筑列表--错误的page参数'''
        pass

    def test03_03_building_list_noSize(self):
        '''case03_03:建筑列表--未传size'''
        pass

    def test03_04_building_list_errSizeType(self):
        '''case03_04:建筑列表--错误的size参数'''
        pass

    def test03_05_building_list_success(self):
        '''case03_05:建筑列表[ZCM]--查看成功(total数量)'''
        pass

    def test03_06_building_list_zsm(self):
        '''case03_06:建筑列表[ZSM]--超级管理员(total数量)'''
        pass

    def test03_07_building_list_noRole(self):
        '''case03_07:建筑列表--组织普通用户'''
        pass
