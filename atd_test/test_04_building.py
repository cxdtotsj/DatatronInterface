'''
园区类接口

test01 : /building/create
test02 : /building/get
test03 : /building/list
test04 : /building/update
test05 : /building/del

'''

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
        user_email,__,user_id = self.pub_param.user_reset_corp(self.corp_id,role=1<<19)
        user_header = self.pub_param.user_header(12345678,email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id,self.corp_id)

        # 新增园区
        res = self.run_method.post(api,json=data,headers=user_header)
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
            "altitude": 100
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
    def test01_12_building_update_delCorpUser(self):
        '''case01_12:更新建筑--已删除管理员编辑建筑'''

        api = '/building/update'
        building_id = self.opera_json.get_data("test01_09_building")["id"]
        data = self.pub_param.building_get(building_id, self.corp_header)
        data.update(area=199)

        # 获取该用户 token
        user_email,__,user_id = self.pub_param.user_reset_corp(self.corp_id,role=1<<19)
        user_header = self.pub_param.user_header(12345678,email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id,self.corp_id)

        # 编辑建筑
        res = self.run_method.post(api,json=data,headers=user_header)
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
        self.assertNotEqual(new_data["status"],3,"超管删除建筑成功")

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
        self.assertNotEqual(new_data["status"],3,"普通用户删除建筑成功")

    def test05_05_building_del_otherCorp(self):
        '''case05_05:删除建筑[其他组织管理员]--删除失败'''
        
        api = '/building/del'
        building_id = self.pub_param.create_building(header=self.corp_header)
        other_corp_header = self.pub_param.common_user(role=524288)
        data = {"id": building_id}
        res = self.run_method.post(api, data, headers=other_corp_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(new_data["status"],3,"其他组织管理员删除建筑成功")

    @unittest.skip("存在BUG,暂时跳过")
    def test06_06_building_del_delCorpUser(self):
        '''case06_06:删除建筑--已删除管理员删除建筑'''

        api = '/building/del'
        building_id = self.pub_param.create_building(header=self.corp_header)
        data = {"id": building_id}

        # 获取该用户 token
        user_email,__,user_id = self.pub_param.user_reset_corp(self.corp_id,role=1<<19)
        user_header = self.pub_param.user_header(12345678,email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id,self.corp_id)

        # 编辑建筑
        res = self.run_method.post(api, data, headers=user_header)
        new_data = self.pub_param.building_get(building_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "普通用户删除园区成功")
        self.assertNotEqual(new_data["status"],3,"普通用户删除建筑成功")
