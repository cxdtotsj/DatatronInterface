'''
园区类接口

test01 : /building/create
test02 : /building/get
test03 : /building/list
test04 : /building/update
test05 : /building/del
test06 : /building/model/upload
test07 : /building/model/get
test08 : /building/model/list
test09 : /building/model/entityget
test10 : model update

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

        api = '/building/create'
        zone_id = self.pub_param.create_zone(self.corp_header)
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

        api = '/building/create'
        zone_id = self.pub_param.create_zone(self.corp_header)
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
                                         "id"], "zone_id": zone_id, "name": data["name"], "data": data})

    # 依赖用例 test01_07_building_create_noZoneId
    def test01_10_building_create_nameRepeat(self):
        '''case01_10:创建建筑[ZCM]--名称重复(无ZoneID,不同的corp_id)'''

        api = '/building/create'
        repeat_name = self.opera_json.get_data(
            "test01_07_building")["name"]
        ohter_corp_header = self.pub_param.common_user(role=524288)
        data = Building.building_data()
        data.update(name=repeat_name)
        res = self.run_method.post(api, json=data, headers=ohter_corp_header)
        self.assertEqual(res.status_code, 200, res.json())

    # 依赖用例 test01_07_building_create_noZoneId
    def test01_11_building_create_nameRepeat(self):
        '''case01_11:创建建筑[ZCM]--名称重复(无ZoneID,相同的corp_id)'''

        api = '/building/create'
        repeat_name = self.opera_json.get_data(
            "test01_07_building")["name"]
        data = Building.building_data()
        data.update(name=repeat_name)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1409, res.json())

    # 依赖用例 test01_09_building_create_success
    def test01_12_building_create_nameRepeat(self):
        '''case01_12:创建建筑[ZCM]--名称重复(相同ZoneID)'''

        api = '/building/create'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        building_detail = self.pub_param.building_get(
            building_id, self.corp_header)
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

        api = '/building/create'
        repeat_name = self.opera_json.get_data("test01_09_building")["name"]
        zone_id = self.pub_param.create_zone(self.corp_header)
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

        api = '/building/create'
        common_user_header = self.pub_param.common_user(self.corp_id)
        data = Building.building_data()
        res = self.run_method.post(api, json=data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    @unittest.skip("存在BUG，暂时跳过")
    def test01_16_building_create_delCorpUser(self):
        '''case01_16:创建建筑--已删除管理员新增建筑'''

        api = '/building/create'
        data = Building.building_data()

        # 获取该用户 token
        user_email, __, user_id = self.pub_param.user_reset_corp(
            self.corp_id, role=1 << 19)
        user_header = self.pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id, self.corp_id)

        # 新增园区
        res = self.run_method.post(api, json=data, headers=user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")

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

        api = '/building/get'
        other_building_id = self.pub_param.create_building()
        data = {"id": other_building_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")

    # 依赖用例 test01_09_building_create_success
    def test02_03_building_get_success(self):
        '''case02_03:获取建筑详细信息[ZCM]--所在组织的建筑'''

        api = '/building/get'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        building_name = self.opera_json.get_data("test01_09_building")["data"]
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断 新增的园区信息 是否返回正确
        self.opera_assert.is_dict_in(building_name, res.json())

    def test02_04_building_get_zsm(self):
        '''case02_04:获取建筑详细信息[ZSM]'''

        api = '/building/get'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        building_name = self.opera_json.get_data("test01_09_building")["data"]
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断 新增的园区信息 是否返回正确
        self.opera_assert.is_dict_in(building_name, res.json())

    def test02_05_building_get_noRole(self):
        '''case02_05:获取建筑详细信息--普通组织用户'''

        api = '/building/get'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        building_name = self.opera_json.get_data("test01_09_building")["data"]
        common_user_header = self.pub_param.common_user(self.corp_id)
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断 新增的园区信息 是否返回正确
        self.opera_assert.is_dict_in(building_name, res.json())

    def test02_06_building_get_noRole(self):
        '''case02_06:获取建筑详细信息--错误的建筑ID'''

        api = '/building/get'
        data = {"id": "11223344"}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1404, "状态码返回错误")

    def test03_01_building_list_success(self):
        '''case03_01:建筑列表[ZCM]--查看成功,无zone_id(corp_id)'''

        api = '/building/list'
        data = {"page": 1,
                "size": 10}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断返回的建筑是否都为该 corp_id
        self.opera_assert.is_equal_value(
            self.corp_id, res.json()["data_list"], "corp_id")

    # 依赖用例 test01_09_building_create_success
    def test03_02_building_list_zoneId(self):
        '''case03_02:建筑列表[ZCM]--园区ID过滤(zone_id)'''

        api = '/building/list'
        zone_id = self.opera_json.get_data("test01_09_building")["zone_id"]
        data = {"page": 1,
                "size": 10,
                "zone_id": zone_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断返回的建筑是否都为该 corp_id
        self.opera_assert.is_equal_value(
            zone_id, res.json()["data_list"], "zone_id")

    def test03_03_building_list_zsm(self):
        '''case03_03:建筑列表[ZSM]--超级管理员(total数量)'''

        api = '/building/list'
        data = {"page": 1,
                "size": 10}
        res = self.run_method.post(api, data, headers=self.super_header)
        sql = '''select id as total from building where status != 3;'''
        building_num = self.opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], str(building_num), "返回的建筑数量不正确")

    def test03_04_building_list_noRole(self):
        '''case03_04:建筑列表--组织普通用户'''

        api = '/building/list'
        data = {"page": 1,
                "size": 10}
        common_user_header = self.pub_param.common_user(self.corp_id)
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断返回的园区是否都为该 corp_id
        self.opera_assert.is_equal_value(
            self.corp_id, res.json()["data_list"], "corp_id")

    def test03_05_building_list_noRole(self):
        '''case03_05:建筑列表--非法用户'''

        api = '/building/list'
        data = {"page": 1,
                "size": 10}
        res = self.run_method.post(api, data, headers={"Authorization": "abc"})
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, "状态码返回错误")

    # 依赖用例 test01_09_building_create_success
    def test04_01_building_update_noName(self):
        '''case04_01:编辑建筑[RCM]--无名称'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(name=None)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(new_data["name"], '', "建筑名称被更新为NULL")

    # 依赖用例 test01_07_building_create_noZoneId
    def test04_02_building_update_nameRepeat(self):
        '''case04_02:编辑建筑[RCM]--重复名称'''

        api = '/building/update'
        building_id = self.pub_param.create_building(
            header=self.corp_header, is_belong_zone=False)
        data = self.pub_param.building_get(building_id, self.corp_header)
        cmp_bud_name = self.opera_json.get_data("test01_07_building")["name"]

        data.update(name=cmp_bud_name)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(new_data["name"], cmp_bud_name, "建筑名称更新为重复")

    # 依赖用例 test01_09_building_create_success
    def test04_03_building_update_area(self):
        '''case04_03:编辑建筑[RCM]--更新面积'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(area=222)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["area"], 222, "面积未更新成功")

    def test04_04_building_update_layerNum(self):
        '''case04_04:编辑建筑[RCM]--更新层数'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(layer_num=55)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["layer_num"], 55, "楼层未更新成功")

    def test04_05_building_update_underlayerNum(self):
        '''case04_05:编辑建筑[RCM]--更新地下层数'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(underlayer_num=10)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["underlayer_num"], 10, "地下楼层未更新成功")

    def test04_06_building_update_coord(self):
        '''case04_06:编辑建筑[RCM]--更新经纬度'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        new_coord = {
            "longitude": 200,
            "latitude": 200,
            "altitude": 100,
            "angle": 90
        }
        data.update(coord=new_coord)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["coord"], new_coord, "经纬度未更新成功")

    def test04_07_building_update_extra(self):
        '''case04_07:编辑建筑[RCM]--更新附加信息'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        new_extra = {
            "build_corp": "更新建筑单位名称",
            "build_start_at": "2020-10-10",
            "construct_corp": "更新规划单位名称",
            "construct_end_at": "2020-10-10",
            "design_corp": "更新设计单位名称",
            "design_end_at": "2020-10-10",
            "plan_corp": "更新施工单位名称",
            "plan_end_at": "2020-10-10",
            "supervise_corp": "更新监理单位名称",
            "supervise_end_at": "2020-10-10"
        }
        data.update(extra=new_extra)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["extra"], new_extra, "附加信息未更新成功")

    def test04_08_building_update_rsmArea(self):
        '''case04_08:编辑建筑[RSM]--超管更新面积,不成功'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(area=88)
        res = self.run_method.post(api, json=data, headers=self.super_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")
        self.assertNotEqual(new_data["area"], 88, "超管面积更新成功")

    def test04_09_building_update_noRole(self):
        '''case04_09:编辑建筑[组织普通用户]--更新不成功'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        common_user_header = self.pub_param.common_user(self.corp_id)
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(area=77)
        res = self.run_method.post(api, json=data, headers=common_user_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")
        self.assertNotEqual(new_data["area"], 77, "普通用户面积更新成功")

    def test04_10_building_update_otherCorp(self):
        '''case04_10:编辑建筑[其他组织管理员]--更新不成功'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        other_corp_header = self.pub_param.common_user(role=524288)
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(area=66)
        res = self.run_method.post(api, json=data, headers=other_corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(new_data["area"], 66, "面积更新成功")

    @unittest.skip("存在BUG,暂时跳过")
    def test04_11_building_update_delCorpUser(self):
        '''case04_11:更新建筑--已删除管理员编辑建筑'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(area=199)

        # 获取该用户 token
        user_email, __, user_id = self.pub_param.user_reset_corp(
            self.corp_id, role=1 << 19)
        user_header = self.pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id, self.corp_id)

        # 编辑建筑
        res = self.run_method.post(api, json=data, headers=user_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")
        self.assertNotEqual(new_data["area"], 199, "普通用户面积更新成功")

    def test05_01_building_del_success(self):
        '''case05_01:删除建筑[ZCM]--删除成功'''

        api = '/building/del'
        building_id = self.pub_param.create_building(
            header=self.corp_header, is_belong_zone=False)
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["status"], 3, "建筑未成功删除")

    def test05_02_building_del_zoneId(self):
        '''case05_02:删除建筑[ZCM]--删除成功'''

        api = '/building/del'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["status"], 3, "建筑未成功删除")

    def test05_03_building_del_rsm(self):
        '''case05_03:删除建筑[ZSM]--删除成功'''

        api = '/building/del'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "普通用户删除园区成功")
        self.assertNotEqual(new_data["status"], 3, "超管删除建筑成功")

    def test05_04_building_del_noRole(self):
        '''case05_04:删除建筑[普通用户]--删除失败'''

        api = '/building/del'
        building_id = self.pub_param.create_building(header=self.corp_header)
        common_user_header = self.pub_param.common_user(self.corp_id)
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=common_user_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "普通用户删除园区成功")
        self.assertNotEqual(new_data["status"], 3, "普通用户删除建筑成功")

    def test05_05_building_del_otherCorp(self):
        '''case05_05:删除建筑[其他组织管理员]--删除失败'''

        api = '/building/del'
        building_id = self.pub_param.create_building(header=self.corp_header)
        other_corp_header = self.pub_param.common_user(role=524288)
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=other_corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(new_data["status"], 3, "其他组织管理员删除建筑成功")

    @unittest.skip("存在BUG,暂时跳过")
    def test05_06_building_del_delCorpUser(self):
        '''case05_06:删除建筑--已删除管理员删除建筑'''

        api = '/building/del'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {"id": building_id}

        # 获取该用户 token
        user_email, __, user_id = self.pub_param.user_reset_corp(
            self.corp_id, role=1 << 19)
        user_header = self.pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id, self.corp_id)

        # 编辑建筑
        res = self.run_method.post(api, data, headers=user_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "普通用户删除园区成功")
        self.assertNotEqual(new_data["status"], 3, "普通用户删除建筑成功")

    def test06_01_building_model_upload_noBuildingId(self):
        """case06_01:上传建筑模型[RCM]--无建筑ID"""

        api = '/building/model/upload'
        data = {
            "building_id": None,
            "mt": "T"
        }
        with open(Building.file_LangChaV2, 'rb') as fileop:
            files = {"file": fileop}
            res = self.run_method.post(
                api, data, files=files, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, "错误码返回错误")

    def test06_02_building_model_upload_errBuildingId(self):
        """case06_02:上传建筑模型[RCM]--错误的建筑ID"""

        api = '/building/model/upload'
        data = {
            "building_id": "112233",
            "model_type": "T"
        }
        with open(Building.file_LangChaV2, 'rb') as fileop:
            files = {"file": fileop}
            res = self.run_method.post(
                api, data, files=files, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1404, "错误码返回错误")

    def test06_03_building_model_upload_noModelType(self):
        """case06_03:上传建筑模型[RCM]--无建筑物类型"""

        api = '/building/model/upload'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {
            "building_id": building_id
        }
        with open(Building.file_LangChaV2, 'rb') as fileop:
            files = {"file": fileop}
            res = self.run_method.post(
                api, data, files=files, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotIn("err", res.json(), res.json())

    def test06_04_building_model_upload_errModelType(self):
        """case06_04:上传建筑模型[RCM]--错误的建筑物类型"""

        api = '/building/model/upload'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {
            "building_id": building_id,
            "model_type": "ZSS"
        }
        with open(Building.file_LangChaV2, 'rb') as fileop:
            files = {"file": fileop}
            res = self.run_method.post(
                api, data, files=files, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, "错误码返回错误")

    def test06_05_building_model_upload_noFile(self):
        """case06_05:上传建筑模型[RCM]--无模型文件"""

        api = '/building/model/upload'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1000, "错误码返回错误")

    def test06_06_building_model_upload_doubleType(self):
        """case06_06:上传建筑模型[RCM]--上传类型T、A,验证data.json未被覆盖"""

        # 上传全类型 T 的模型文件
        res_t,building_id = self.pub_param.building_model_upload(header=self.corp_header)
        metaUrl_t = res_t["meta_url"]
        guid_t_one = self.pub_param.get_guid(metaUrl_t)
        # 上传类型 A 的模型文件
        res_b,__ = self.pub_param.building_model_upload(building_id,self.corp_header,'B','LangChaV2.objr')
        guid_t_two = self.pub_param.get_guid(metaUrl_t) # 再次获取类型T的guid
        metaUrl_b = res_b["meta_url"]
        guid_b = self.pub_param.get_guid(metaUrl_b)     # 获取类型B的guid
        self.assertEqual(guid_t_one,guid_t_two,"上传其他类型模型后，T类型的data被覆盖")
        self.assertNotEqual(guid_t_two,guid_b,"上传其他类型模型后，T类型被B类型覆盖")
        
    def test06_07_building_model_upload_rsm(self):
        """case06_07:上传建筑模型[RSM]--RSM上传建筑模型"""

        api = '/building/model/upload'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = self.run_method.post(
                api, data, files=files, headers=self.super_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test06_08_building_model_upload_noRole(self):
        """case06_08:上传建筑模型[普通用户]--普通用户上传建筑模型"""

        api = '/building/model/upload'
        building_id = self.pub_param.create_building(header=self.corp_header)
        common_user_header = self.pub_param.common_user(corp_id=self.corp_id)
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = self.run_method.post(
                api, data, files=files, headers=common_user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test06_09_building_model_upload_OtherCorp(self):
        """case06_09:上传建筑模型[RCM]--RCM上传其他组织的建筑模型"""

        api = '/building/model/upload'
        building_id = self.pub_param.create_building()
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = self.run_method.post(
                api, data, files=files, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1403, res.json())

    def test07_01_building_model_get_noBuildingId(self):
        """case07_01:获取模型关联信息[RCM]--无建筑ID"""

        api = '/building/model/get'
        data = {
            "building_id": None,
            "model_type": "T"
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test07_02_building_model_get_errBuildingId(self):
        """case07_02:获取模型关联信息[RCM]--错误的建筑ID"""

        api = '/building/model/get'
        data = {
            "building_id": "112233",
            "model_type": "T"
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1000, res.json())

    def test07_03_building_model_get_noModelType(self):
        """case07_03:获取模型关联信息[RCM]--无模型类型"""

        api = '/building/model/get'
        r, building_id = self.pub_param.building_model_upload(
            header=self.corp_header)
        data = {
            "building_id": building_id,
            "model_type": None
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

        self.opera_json.check_json_value("test07_03_building",
                                         {"building_id": building_id,
                                             "model_id": r["model_id"]})

    # 依赖用例 test07_03_building
    def test07_04_building_model_get_errModelType(self):
        """case07_04:获取模型关联信息[RCM]--错误的模型类型"""

        api = '/building/model/get'
        building_id = self.opera_json.get_data(
            "test07_03_building")["building_id"]
        data = {
            "building_id": building_id,
            "model_type": "SCC"
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1000, res.json())

    def test07_05_building_model_get_success(self):
        """case07_05:获取模型关联信息[RCM]--查询成功"""

        api = '/building/model/get'
        building_id, model_id = self.opera_json.get_data(
            "test07_03_building").values()
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["id"], model_id, res.json())

    def test08_01_building_model_list_noBuildingId(self):
        """case08_01:特定建筑模型列表--无建筑ID"""

        api = '/building/model/list'
        data = {
            "building_id": None
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], "0", res.json())

    def test08_02_building_model_list_errBuildingId(self):
        """case08_02:特定建筑模型列表--错误的建筑ID"""

        api = '/building/model/list'
        data = {
            "building_id": "112233"
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], "0", res.json())

    def test08_03_building_model_list_success(self):
        """case08_03:特定建筑模型列表--查询成功"""

        api = '/building/model/list'
        r,building_id = self.pub_param.building_model_upload(header=self.corp_header)
        self.pub_param.get_guid(r["meta_url"])
        data = {
            "building_id": building_id
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 200, res.json())
        self.opera_assert.is_list_in(building_id,res.json()["data_list"],"building_id")
    
    def test08_04_building_model_list_sorted(self):
        """case08_04:特定建筑模型列表--按类型顺序排序"""

        api = '/building/model/list'
        building_id = self.pub_param.create_building(header=self.corp_header)
        for model_type in Building.modeltype_list:
            self.pub_param.building_model_upload(building_id,self.corp_header,model_type)
            time.sleep(1)
        data = {
            "building_id":building_id
        }
        res = self.run_method.post(api,data)
        mt_sorted = Building.modelType_sorted() # 已排好序的model_type
        self.assertEqual(res.status_code, 200, res.json())
        self.opera_assert.is_equal_sorted(mt_sorted,res.json()["data_list"],"model_type")


    def test09_01_building_model_entityget_noModelId(self):
        """case09_01:获取构件信息--无模型ID"""

        api = '/building/model/entityget'
        r, building_id = self.pub_param.building_model_upload(
            header=self.corp_header)
        meta_url, model_id = r["meta_url"], r["model_id"]
        guid = self.pub_param.get_guid(meta_url)
        data = {
            "model_id": None,
            "guid": guid
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

        self.opera_json.check_json_value("test09_01_building",
                                         {"building_id": building_id,
                                             "model_id": model_id,
                                             "guid": guid})

    # 依赖用例 test09_01_building
    def test09_02_building_model_entityget_errModelId(self):
        """case09_02:获取构件信息--错误的模型ID"""

        api = '/building/model/entityget'
        guid = self.opera_json.get_data("test09_01_building")["guid"]
        data = {
            "model_id": "112233",
            "guid": guid
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1000, res.json())

    def test09_03_building_model_entityget_noGuId(self):
        """case09_03:获取构件信息--无构件ID"""

        api = '/building/model/entityget'
        model_id = self.opera_json.get_data("test09_01_building")["model_id"]
        data = {
            "model_id": model_id,
            "guid": None
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test09_04_building_model_entityget_errGuId(self):
        """case09_04:获取构件信息--错误的构件ID"""

        api = '/building/model/entityget'
        model_id = self.opera_json.get_data("test09_01_building")["model_id"]
        data = {
            "model_id": model_id,
            "guid": "abc123"
        }
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1400, res.json())

    def test09_05_building_model_entityget_success(self):
        """case09_05:获取构件信息--查询成功"""

        api = '/building/model/entityget'
        __, model_id, guid = self.opera_json.get_data(
            "test09_01_building").values()
        data = {
            "model_id": model_id,
            "guid": guid}
        res = self.run_method.post(api, data)
        self.assertEqual(res.status_code, 200, res.json())

    def test10_01_building_model_upload_update(self):
        """case10_01:上传建筑模型[RCM]--更新建筑模型"""

        # 获取更新前的 model_name
        __, building_id = self.pub_param.building_model_upload(
            header=self.corp_header)
        sql = '''select model_name from building_model 
                    where building_id={} and model_type='T';'''.format(building_id)
        old_modelName = self.opera_db.get_fetchone(sql)["model_name"]
        self.pub_param.building_model_upload(
            building_id=building_id, header=self.corp_header, filename='LangChaV2.objr')
        new_modelName = self.opera_db.get_fetchone(sql)["model_name"]

        self.assertNotEqual(old_modelName, new_modelName, "更新文件未成功")

    def test10_02_building_model_get_update(self):
        """case10_02:获得模型关联信息[RCM]--获取更新后的model_id"""

        # 获取更新前的 model_id
        __, building_id = self.pub_param.building_model_upload(
            header=self.corp_header)
        sql = '''select id from building_model 
                    where building_id={} and model_type='T';'''.format(building_id)
        old_id = self.opera_db.get_fetchone(sql)["id"]
        self.pub_param.building_model_upload(
            building_id=building_id, header=self.corp_header, filename='LangChaV2.objr')
        new_id = self.opera_db.get_fetchone(sql)["id"]

        self.assertNotEqual(old_id, new_id, "model_id未更新")

    def test10_03_building_model_model_entityget_update(self):
        """case10_03:获取构件信息[RCM]--获取更新后的构件信息"""

        # 获取更新前的building_id model_id guid
        old_res,building_id = self.pub_param.building_model_upload(header=self.corp_header)
        old_metaUrl = old_res["meta_url"]
        old_guid = self.pub_param.get_guid(old_metaUrl)
        # 更新 model
        new_res,__ = self.pub_param.building_model_upload(
            building_id=building_id, header=self.corp_header, filename='LangChaV2.objr')
        new_metaUrl = new_res["meta_url"]
        entities = self.pub_param.get_update_entities(new_metaUrl,old_guid)
        self.assertNotIn(old_guid,[i["Guid"] for i in entities],"Guid未更新")

        
