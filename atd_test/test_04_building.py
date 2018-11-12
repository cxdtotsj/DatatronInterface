'''
园区类接口

TestBuildingCreate :         /building/create
TestBuildingGet :            /building/get
TestBuildingList :           /building/list
TestBuildingUpdate :         /building/update
TestBuildingDel :            /building/del
TestBuildingModelUpload :    /building/model/upload
TestBuildingModelGet :       /building/model/get
TestBuildingModelList :      /building/model/list
TestBuildingModelEntityget : /building/model/entityget
TestBuildingModelUpdate :     model update
TestBuildingModelDevicelist: /building/model/devicelist
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


class TestBuildingCreate(unittest.TestCase):

    def test01_building_create_noName(self):
        '''case01:创建建筑--无建筑名称'''

        api = '/building/create'
        data = Building.building_data()
        data.pop("name")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_building_create_noLoc(self):
        '''case02:创建建筑--无地址'''

        api = '/building/create'
        data = Building.building_data()
        data.pop("loc")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_building_create_noArea(self):
        '''case03:创建建筑--无面积'''

        api = '/building/create'
        data = Building.building_data()
        data.pop("area")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        building_detail = pub_param.building_get(
            res.json()["id"], corp_header)
        self.assertEqual(building_detail["area"], 0, "面积默认值返回错误")

    def test04_buliding_create_noLayer(self):
        '''case04:创建建筑--无层数'''

        api = '/building/create'
        data = Building.building_data()
        data.pop("layer_num")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        building_detail = pub_param.building_get(
            res.json()["id"], corp_header)
        self.assertEqual(building_detail["layer_num"], 0, "楼层数默认值返回错误")

    def test05_buliding_create_noUnderlayer(self):
        '''case05:创建建筑--无地下层数'''

        api = '/building/create'
        data = Building.building_data()
        data.pop("underlayer_num")
        res = run_method.post(api, json=data, headers=corp_header)
        try:
            building_detail = pub_param.building_get(
                res.json()["id"], corp_header)
        except KeyError:
            print(run_method.errInfo(res))
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(building_detail["underlayer_num"], 0, "地下层数默认值返回错误")

    def test06_building_create_noCoord(self):
        '''case06:创建建筑--无经纬度'''

        api = '/building/create'
        data = Building.building_data()
        data.pop("coord")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test07_building_create_noZoneId(self):
        '''case07:创建建筑[ZCM]--不属于园区建筑(无附加信息)'''

        api = '/building/create'
        data = Building.building_data()
        res = run_method.post(api, json=data, headers=corp_header)
        try:
            building_detail = pub_param.building_get(
                res.json()["id"], corp_header)
        except KeyError:
            print(run_method.errInfo(res))
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))
        self.assertEqual(building_detail["zone_id"], "", "独栋建筑存在园区ID")

        opera_json.check_json_value(
            "test07_building_create", {"id": res.json()["id"], "name": data["name"], "data": data})

    def test08_building_create_ZoneId(self):
        '''case08:创建建筑[ZCM]--属于园区建筑(无附加信息)'''

        api = '/building/create'
        zone_id = pub_param.create_zone(corp_header)
        data = Building.building_data()
        data.update(zone_id=zone_id)
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        building_detail = pub_param.building_get(
            res.json()["id"], corp_header)
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))
        self.assertEqual(building_detail["zone_id"], zone_id, "园区建筑不存在园区ID")

    def test09_building_create_success(self):
        '''case09:创建建筑[ZCM]--新增成功(全部信息)'''

        api = '/building/create'
        zone_id = pub_param.create_zone(corp_header)
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
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        building_detail = pub_param.building_get(
            res.json()["id"], corp_header)
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))
        self.assertEqual(building_detail["zone_id"], zone_id, "园区建筑不存在园区ID")

        opera_json.check_json_value("test09_building_create", {"id": res.json()[
            "id"], "zone_id": zone_id, "name": data["name"], "data": data})

    # 依赖用例 test07_building_create_noZoneId
    def test10_building_create_nameRepeat(self):
        '''case10:创建建筑[ZCM]--名称重复(无ZoneID,不同的corp_id)'''

        api = '/building/create'
        repeat_name = opera_json.get_data(
            "test07_building_create")["name"]
        ohter_corp_header = pub_param.common_user(role=524288)
        data = Building.building_data()
        data.update(name=repeat_name)
        res = run_method.post(api, json=data, headers=ohter_corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    # 依赖用例 test07_building_create_noZoneId
    def test11_building_create_nameRepeat(self):
        '''case11:创建建筑[ZCM]--名称重复(无ZoneID,相同的corp_id)'''

        api = '/building/create'
        repeat_name = opera_json.get_data(
            "test07_building_create")["name"]
        data = Building.building_data()
        data.update(name=repeat_name)
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1409, run_method.errInfo(res))

    # 依赖用例 test09_building_create_success
    def test12_building_create_nameRepeat(self):
        '''case12:创建建筑[ZCM]--名称重复(相同ZoneID)'''

        api = '/building/create'
        building_id = opera_json.get_data("test09_building_create")["id"]
        building_detail = pub_param.building_get(
            building_id, corp_header)
        data = Building.building_data()
        data.update({
            "name": building_detail["name"],
            "zone_id": building_detail["zone_id"]
        })
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1409, run_method.errInfo(res))

    # 依赖用例 test09_building_create_success
    def test13_building_create_nameRepeat(self):
        '''case13:创建建筑[ZCM]--名称重复(不同ZoneID)'''

        api = '/building/create'
        repeat_name = opera_json.get_data("test09_building_create")["name"]
        zone_id = pub_param.create_zone(corp_header)
        data = Building.building_data()
        data.update({
            "name": repeat_name,
            "zone_id": zone_id,
        })
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))

    def test14_building_create_rsm(self):
        '''case14:创建建筑[ZSM]--超级管理员新增(角色受限)'''

        api = '/building/create'
        data = Building.building_data()
        res = run_method.post(api, json=data, headers=super_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test15_building_create_noRole(self):
        '''case15:创建建筑--普通组织用户新增(角色受限)'''

        api = '/building/create'
        common_user_header = pub_param.common_user(corp_id)
        data = Building.building_data()
        res = run_method.post(api, json=data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    @unittest.skip("存在BUG，暂时跳过")
    def test16_building_create_delCorpUser(self):
        '''case16:创建建筑--已删除管理员新增建筑'''

        api = '/building/create'
        data = Building.building_data()

        # 获取该用户 token
        user_email, __, user_id = pub_param.user_reset_corp(
            corp_id, role=1 << 19)
        user_header = pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        pub_param.user_corp_del(user_id, corp_id)

        # 新增园区
        res = run_method.post(api, json=data, headers=user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))


class TestBuildingGet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        zone_id = pub_param.create_zone(corp_header)
        cls.building_data = Building.building_data()
        cls.building_data.update({
            "zone_id": zone_id,
            "extra": {
                "build_corp": "建筑单位名称",
                "build_start_at": "2019-10-09",
                "construct_corp": "规划单位名称",
                "construct_end_at": "2019-10-09",
                "design_corp": "设计单位名称",
                "design_end_at": "2019-10-09",
                "plan_corp": "施工单位名称",
                "plan_end_at": "2019-10-09",
                "supervise_corp": "监理单位名称",
                "supervise_end_at": "2019-10-09"
            }
        })
        cls.building_id = pub_param.create_sign_building(cls.building_data,corp_header)


    def test01_building_get_noId(self):
        '''case01:获取建筑详细信息--无建筑ID'''

        api = '/building/get'
        data = {"id": None}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))

    def test02_building_get_errId(self):
        '''case02:获取建筑详细信息[ZCM]--其他组织的建筑'''

        api = '/building/get'
        other_building_id = pub_param.create_building()
        data = {"id": other_building_id}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test03_building_get_success(self):
        '''case03:获取建筑详细信息[ZCM]--所在组织的建筑'''

        api = '/building/get'
        data = {"id": self.building_id}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断 新增的园区信息 是否返回正确
        opera_assert.is_dict_in(self.building_data, res.json())

    def test04_building_get_zsm(self):
        '''case04:获取建筑详细信息[ZSM]'''

        api = '/building/get'
        data = {"id": self.building_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断 新增的园区信息 是否返回正确
        opera_assert.is_dict_in(self.building_data, res.json())

    def test05_building_get_noRole(self):
        '''case05:获取建筑详细信息--普通组织用户'''

        api = '/building/get'
        common_user_header = pub_param.common_user(corp_id)
        data = {"id": self.building_id}
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断 新增的园区信息 是否返回正确
        opera_assert.is_dict_in(self.building_data, res.json())

    def test06_building_get_errBuildingId(self):
        '''case06:获取建筑详细信息--错误的建筑ID'''

        api = '/building/get'
        data = {"id": "11223344"}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))


class TestBuildingList(unittest.TestCase):

    def test01_building_list_success(self):
        '''case01:建筑列表[RCM]--查看成功,无zone_id(corp_id)'''

        api = '/building/list'
        data = {"page": 1,
                "size": 100}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断返回的建筑是否都为该 corp_id
        opera_assert.is_list_in(
            corp_id, res.json()["data_list"], "corp_id")

    def test02_building_list_zoneId(self):
        '''case02:建筑列表[RCM]--园区ID过滤(zone_id)'''

        api = '/building/list'
        zone_id = pub_param.create_zone(corp_header)                  # 新增园区
        pub_param.create_building(zone_id=zone_id,header=corp_header) # 新增属于园区的建筑
        data = {"page": 1,
                "size": 100,
                "zone_id": zone_id}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断返回的建筑是否都为该 zone_id
        opera_assert.is_list_in(
            zone_id, res.json()["data_list"], "zone_id")

    def test03_building_list_rsm(self):
        '''case03:建筑列表[RSM]--超级管理员(total数量)'''

        api = '/building/list'
        data = {"page": 1,
                "size": 100}
        res = run_method.post(api, data, headers=super_header)
        sql = '''select id as total from building where status != 3;'''
        building_num = opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(building_num), run_method.errInfo(res))

    def test04_building_list_noRole(self):
        '''case04:建筑列表--组织普通用户'''

        api = '/building/list'
        data = {"page": 1,
                "size": 100}
        common_user_header = pub_param.common_user(corp_id)
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断返回的建筑是否都为该 corp_id
        opera_assert.is_list_in(
            corp_id, res.json()["data_list"], "corp_id")

    def test05_building_list_noRole(self):
        '''case05:建筑列表--非法用户'''

        api = '/building/list'
        data = {"page": 1,
                "size": 100}
        res = run_method.post(api, data, headers={"Authorization": "abc"})
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))


class TestBuildingUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        zone_id = pub_param.create_zone(header=corp_header)
        building_data = Building.building_data()
        building_data.update({
            "zone_id": zone_id,
            "extra": {
                "build_corp": "建筑单位名称",
                "build_start_at": "2016-10-09",
                "construct_corp": "规划单位名称",
                "construct_end_at": "2016-10-09",
                "design_corp": "设计单位名称",
                "design_end_at": "2016-10-09",
                "plan_corp": "施工单位名称",
                "plan_end_at": "2016-10-09",
                "supervise_corp": "监理单位名称",
                "supervise_end_at": "2016-10-09"
            }
        })
        cls.building_id = pub_param.create_sign_building(building_data,corp_header)

    def test01_building_update_noName(self):
        '''case01:编辑建筑[RCM]--无名称'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(name=None)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(new_data["name"], '', "建筑名称被更新为NULL")

    def test02_building_update_nameRepeat(self):
        '''case02:编辑建筑[RCM]--重复名称'''

        api = '/building/update'
        bud_one_id = pub_param.create_sign_building(header=corp_header)           # 新增独栋建筑一
        bud_two_id = pub_param.create_sign_building(header=corp_header)           # 新增独栋建筑二
        bud_one_name = pub_param.building_get(bud_one_id, corp_header)["name"]    # 获取独栋建筑一 name
        bud_two_data = pub_param.building_get(bud_one_id, corp_header)            # 获取独栋建筑二 data
        bud_two_data.update(name=bud_one_name)                                    # 更新独栋建筑二的 name,和第一栋建筑一致
        res = run_method.post(api, json=bud_two_data, headers=corp_header)
        bud_two_new_data = pub_param.building_get(bud_two_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(bud_two_new_data["name"], bud_one_name, "建筑名称更新为重复")   # 第二栋更新后的name和建筑一不一致

    def test03_building_update_area(self):
        '''case03:编辑建筑[RCM]--更新面积'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(area=222)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["area"], 222, "面积未更新成功")

    def test04_building_update_layerNum(self):
        '''case04:编辑建筑[RCM]--更新层数'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(layer_num=55)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["layer_num"], 55, "楼层未更新成功")

    def test05_building_update_underlayerNum(self):
        '''case05:编辑建筑[RCM]--更新地下层数'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(underlayer_num=10)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["underlayer_num"], 10, "地下楼层未更新成功")

    def test06_building_update_coord(self):
        '''case06:编辑建筑[RCM]--更新经纬度'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
        new_coord = {
            "longitude": 200,
            "latitude": 200,
            "altitude": 100,
            "angle": 90
        }
        data.update(coord=new_coord)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["coord"], new_coord, "经纬度未更新成功")

    def test07_building_update_extra(self):
        '''case07:编辑建筑[RCM]--更新附加信息'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
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
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["extra"], new_extra, "附加信息未更新成功")

    def test08_building_update_rsmArea(self):
        '''case08:编辑建筑[RSM]--超管更新面积,不成功'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(area=88)
        res = run_method.post(api, json=data, headers=super_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["area"], 88, "超管面积更新成功")

    def test09_building_update_noRole(self):
        '''case09:编辑建筑[组织普通用户]--更新不成功'''

        api = '/building/update'
        common_user_header = pub_param.common_user(corp_id)
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(area=77)
        res = run_method.post(api, json=data, headers=common_user_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["area"], 77, "普通用户面积更新成功")

    def test10_building_update_otherCorp(self):
        '''case10:编辑建筑[其他组织管理员]--更新不成功'''

        api = '/building/update'
        other_corp_header = pub_param.common_user(role=524288)
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(area=66)
        res = run_method.post(api, json=data, headers=other_corp_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(new_data["area"], 66, "面积更新成功")

    @unittest.skip("存在BUG,暂时跳过")
    def test11_building_update_delCorpUser(self):
        '''case11:更新建筑--已删除管理员编辑建筑'''

        api = '/building/update'
        data = pub_param.building_get(self.building_id, corp_header)
        data.update(area=199)

        # 获取该用户 token
        user_email, __, user_id = pub_param.user_reset_corp(
            corp_id, role=1 << 19)
        user_header = pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        pub_param.user_corp_del(user_id, corp_id)

        # 编辑建筑
        res = run_method.post(api, json=data, headers=user_header)
        new_data = pub_param.building_get(self.building_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["area"], 199, "普通用户面积更新成功")


class TestBuildingDel(unittest.TestCase):

    def test01_building_del_success(self):
        '''case01:删除建筑[ZCM]--删除成功'''

        api = '/building/del'
        building_id = pub_param.create_building(
            header=corp_header, is_belong_zone=False)
        data = {"id": building_id}
        res = run_method.post(api, data, headers=corp_header)
        new_data = pub_param.building_get(building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 3, "建筑未成功删除")

    def test02_building_del_zoneId(self):
        '''case02:删除建筑[ZCM]--删除成功'''

        api = '/building/del'
        building_id = pub_param.create_building(header=corp_header)
        data = {"id": building_id}
        res = run_method.post(api, data, headers=corp_header)
        new_data = pub_param.building_get(building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 3, "建筑未成功删除")

    def test03_building_del_rsm(self):
        '''case03:删除建筑[ZSM]--删除成功'''

        api = '/building/del'
        building_id = pub_param.create_building(header=corp_header)
        data = {"id": building_id}
        res = run_method.post(api, data, headers=super_header)
        new_data = pub_param.building_get(building_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["status"], 3, "超管删除建筑成功")

    def test04_building_del_noRole(self):
        '''case04:删除建筑[普通用户]--删除失败'''

        api = '/building/del'
        building_id = pub_param.create_building(header=corp_header)
        common_user_header = pub_param.common_user(corp_id)
        data = {"id": building_id}
        res = run_method.post(api, data, headers=common_user_header)
        new_data = pub_param.building_get(building_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["status"], 3, "普通用户删除建筑成功")

    def test05_building_del_otherCorp(self):
        '''case05:删除建筑[其他组织管理员]--删除失败'''

        api = '/building/del'
        building_id = pub_param.create_building(header=corp_header)
        other_corp_header = pub_param.common_user(role=524288)
        data = {"id": building_id}
        res = run_method.post(api, data, headers=other_corp_header)
        new_data = pub_param.building_get(building_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(new_data["status"], 3, "其他组织管理员删除建筑成功")

    @unittest.skip("存在BUG,暂时跳过")
    def test06_building_del_delCorpUser(self):
        '''case06:删除建筑--已删除管理员删除建筑'''

        api = '/building/del'
        building_id = pub_param.create_building(header=corp_header)
        data = {"id": building_id}

        # 获取该用户 token
        user_email, __, user_id = pub_param.user_reset_corp(
            corp_id, role=1 << 19)
        user_header = pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        pub_param.user_corp_del(user_id, corp_id)

        # 编辑建筑
        res = run_method.post(api, data, headers=user_header)
        new_data = pub_param.building_get(building_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["status"], 3, "普通用户删除建筑成功")


class TestBuildingModelUpload(unittest.TestCase):


    def test01_building_model_upload_noBuildingId(self):
        """case01:上传建筑模型[RCM]--无建筑ID"""

        api = '/building/model/upload'
        data = {
            "building_id": None,
            "mt": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                api, data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_building_model_upload_errBuildingId(self):
        """case02:上传建筑模型[RCM]--错误的建筑ID"""

        api = '/building/model/upload'
        data = {
            "building_id": "112233",
            "model_type": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                api, data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))

    def test03_building_model_upload_noModelType(self):
        """case03:上传建筑模型[RCM]--无建筑物类型"""

        api = '/building/model/upload'
        building_id = pub_param.create_building(header=corp_header)
        data = {
            "building_id": building_id
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                api, data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotIn("err", res.json(), run_method.errInfo(res))

    def test04_building_model_upload_errModelType(self):
        """case04:上传建筑模型[RCM]--错误的建筑物类型"""

        api = '/building/model/upload'
        building_id = pub_param.create_building(header=corp_header)
        data = {
            "building_id": building_id,
            "model_type": "ZSS"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                api, data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_building_model_upload_noFile(self):
        """case05:上传建筑模型[RCM]--无模型文件"""

        api = '/building/model/upload'
        building_id = pub_param.create_building(header=corp_header)
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test06_building_model_upload_doubleType(self):
        """case06:上传建筑模型[RCM]--上传类型T、A,验证data.json未被覆盖"""

        # 上传全类型 T 的模型文件
        res_t, building_id = pub_param.building_model_upload(
            header=corp_header)
        metaUrl_t = res_t["meta_url"]
        guid_t_one = pub_param.get_guid(metaUrl_t)  # 第一次获取 t 的 guid
        # 上传类型 B 的模型文件
        res_b, __ = pub_param.building_model_upload(
            building_id, corp_header, 'B', 'LangChaV2.objr')
        guid_t_two = pub_param.get_guid(metaUrl_t)  # 第二次获取 t 的guid
        metaUrl_b = res_b["meta_url"]
        guid_b = pub_param.get_guid(metaUrl_b)     # 获取类型B的guid
        self.assertEqual(guid_t_one, guid_t_two, "上传其他类型模型后，T类型的data被覆盖")
        self.assertNotEqual(guid_t_two, guid_b, "上传其他类型模型后，T类型被B类型覆盖")

    def test07_building_model_upload_rsm(self):
        """case07:上传建筑模型[RSM]--RSM上传建筑模型"""

        api = '/building/model/upload'
        building_id = pub_param.create_building(header=corp_header)
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                api, data, files=files, headers=super_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test08_building_model_upload_noRole(self):
        """case08:上传建筑模型[普通用户]--普通用户上传建筑模型"""

        api = '/building/model/upload'
        building_id = pub_param.create_building(header=corp_header)
        common_user_header = pub_param.common_user(corp_id=corp_id)
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                api, data, files=files, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test09_building_model_upload_OtherCorp(self):
        """case09:上传建筑模型[RCM]--RCM上传其他组织的建筑模型"""

        api = '/building/model/upload'
        building_id = pub_param.create_building()
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                api, data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))


class TestBuildingModelGet(unittest.TestCase):

    def test01_building_model_get_noBuildingId(self):
        """case01:获取模型关联信息[RCM]--无建筑ID"""

        api = '/building/model/get'
        data = {
            "building_id": None,
            "model_type": "T"
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_building_model_get_errBuildingId(self):
        """case02:获取模型关联信息[RCM]--错误的建筑ID"""

        api = '/building/model/get'
        data = {
            "building_id": "112233",
            "model_type": "T"
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test03_building_model_get_noModelType(self):
        """case03:获取模型关联信息[RCM]--无模型类型"""

        api = '/building/model/get'
        r, building_id = pub_param.building_model_upload(
            header=corp_header)
        data = {
            "building_id": building_id,
            "model_type": None
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

        opera_json.check_json_value("test03_building_model_get",
                                    {"building_id": building_id,
                                     "model_id": r["model_id"]})

    # 依赖用例 test03_building_model_get
    def test04_building_model_get_errModelType(self):
        """case04:获取模型关联信息[RCM]--错误的模型类型"""

        api = '/building/model/get'
        building_id = opera_json.get_data(
            "test03_building_model_get")["building_id"]
        data = {
            "building_id": building_id,
            "model_type": "SCC"
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test05_building_model_get_success(self):
        """case05:获取模型关联信息[RCM]--查询成功"""

        api = '/building/model/get'
        building_id, model_id = opera_json.get_data(
            "test03_building_model_get").values()
        data = {
            "building_id": building_id,
            "model_type": "T"
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], model_id, run_method.errInfo(res))


class TestBuildingModelList(unittest.TestCase):

    def test01_building_model_list_noBuildingId(self):
        """case01:特定建筑模型列表--无建筑ID"""

        api = '/building/model/list'
        data = {
            "building_id": None
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], "0", run_method.errInfo(res))

    def test02_building_model_list_errBuildingId(self):
        """case02:特定建筑模型列表--错误的建筑ID"""

        api = '/building/model/list'
        data = {
            "building_id": "112233"
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], "0", run_method.errInfo(res))

    def test03_building_model_list_success(self):
        """case03:特定建筑模型列表--查询成功"""

        api = '/building/model/list'
        r, building_id = pub_param.building_model_upload(header=corp_header)
        pub_param.get_guid(r["meta_url"])
        data = {
            "building_id": building_id
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        opera_assert.is_list_in(building_id, res.json()[
                                "data_list"], "building_id")

    def test04_building_model_list_sorted(self):
        """case04:特定建筑模型列表--按类型顺序排序"""

        api = '/building/model/list'
        building_id = pub_param.create_building(header=corp_header)
        for model_type in Building.modeltype_list:
            pub_param.building_model_upload(
                building_id, corp_header, model_type)
            time.sleep(1)
        data = {
            "building_id": building_id
        }
        res = run_method.post(api, data)
        mt_sorted = Building.modelType_sorted()  # 已排好序的model_type
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        opera_assert.is_equal_sorted(
            mt_sorted, res.json()["data_list"], "model_type")


class TestBuildingModelEntityget(unittest.TestCase):

    def test01_building_model_entityget_noModelId(self):
        """case01:获取构件信息--无模型ID"""

        api = '/building/model/entityget'
        r, building_id = pub_param.building_model_upload(
            header=corp_header)
        meta_url, model_id = r["meta_url"], r["model_id"]
        guid = pub_param.get_guid(meta_url)
        data = {
            "model_id": None,
            "guid": guid
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

        opera_json.check_json_value("test01_building_model_entityget",
                                    {"building_id": building_id,
                                     "model_id": model_id,
                                     "guid": guid})

    # 依赖用例 test01_building_model_entityget
    def test02_building_model_entityget_errModelId(self):
        """case02:获取构件信息--错误的模型ID"""

        api = '/building/model/entityget'
        guid = opera_json.get_data("test01_building_model_entityget")["guid"]
        data = {
            "model_id": "112233",
            "guid": guid
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test03_building_model_entityget_noGuId(self):
        """case03:获取构件信息--无构件ID"""

        api = '/building/model/entityget'
        model_id = opera_json.get_data("test01_building_model_entityget")["model_id"]
        data = {
            "model_id": model_id,
            "guid": None
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test04_building_model_entityget_errGuId(self):
        """case04:获取构件信息--错误的构件ID"""

        api = '/building/model/entityget'
        model_id = opera_json.get_data("test01_building_model_entityget")["model_id"]
        data = {
            "model_id": model_id,
            "guid": "abc123"
        }
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_building_model_entityget_success(self):
        """case05:获取构件信息--查询成功"""

        api = '/building/model/entityget'
        __, model_id, guid = opera_json.get_data(
            "test01_building_model_entityget").values()
        data = {
            "model_id": model_id,
            "guid": guid}
        res = run_method.post(api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))


class TestBuildingModelUpdate(unittest.TestCase):


    def test01_building_model_upload_update(self):
        """case01:上传建筑模型[RCM]--更新建筑模型"""

        # 获取更新前的 model_name
        __, building_id = pub_param.building_model_upload(
            header=corp_header)
        sql = '''select model_name from building_model 
                    where building_id={} and model_type='T';'''.format(building_id)
        old_modelName = opera_db.get_fetchone(sql)["model_name"]
        pub_param.building_model_upload(
            building_id=building_id, header=corp_header, filename='LangChaV2.objr')
        new_modelName = opera_db.get_fetchone(sql)["model_name"]
        self.assertNotEqual(old_modelName, new_modelName, "更新文件未成功")

    def test02_building_model_get_update(self):
        """case02:获得模型关联信息[RCM]--获取更新后的model_id"""

        # 获取更新前的 model_id
        __, building_id = pub_param.building_model_upload(
            header=corp_header)
        sql = '''select id from building_model 
                    where building_id={} and model_type='T';'''.format(building_id)
        old_id = opera_db.get_fetchone(sql)["id"]
        pub_param.building_model_upload(
            building_id=building_id, header=corp_header, filename='LangChaV2.objr')
        new_id = opera_db.get_fetchone(sql)["id"]
        self.assertNotEqual(old_id, new_id, "model_id未更新")

    def test03_building_model_model_entityget_update(self):
        """case03:获取构件信息[RCM]--获取更新后的构件信息"""

        # 获取更新前的building_id model_id guid
        old_res, building_id = pub_param.building_model_upload(
            header=corp_header)
        old_metaUrl = old_res["meta_url"]
        old_guid = pub_param.get_guid(old_metaUrl)
        # 更新 model
        new_res, __ = pub_param.building_model_upload(
            building_id=building_id, header=corp_header, filename='LangChaV2.objr')
        new_metaUrl = new_res["meta_url"]
        entities = pub_param.get_update_entities(new_metaUrl, old_guid)
        self.assertNotIn(old_guid, [i["Guid"] for i in entities], "Guid未更新")


class TestBuildingModelDeviceadd(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = '/building/model/deviceadd'
        cls.building_id = pub_param.create_building(header=corp_header)
        cls.guidList = pub_param.get_guidList(cls.building_id,corp_header,"LangChaV2.objr")[:20]

        opera_json.check_json_value("deviceadd",{"building_id":cls.building_id})    # use to class devicelist

    def test01_building_model_deviceadd_noBuildingId(self):
        """case01:添加关联设备[RCM]--无建筑ID"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": None,
            "guid": self.guidList[0],
            "things_id": device_id,
            "type": "bim"
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test02_building_model_deviceadd_noThingsId(self):
        """case02:添加关联设备[RCM]--无设备ID"""

        data = {
            "building_id": self.building_id,
            "guid": self.guidList[1],   
            "things_id": None,
            "type": "bim"
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test03_building_model_deviceadd_noType(self):
        """case03:添加关联设备[RCM]--无设备关联类型"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[2],   
            "things_id": device_id,
            "type": None
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test04_building_model_deviceadd_bim_noGU(self):
        """case04:添加关联设备[RCM]--类型为BIM,无guid,无url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": None,   
            "things_id": device_id,
            "type": "bim",
            "url":None
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test05_building_model_deviceadd_bim_guid(self):
        """case05:添加关联设备[RCM]--类型为BIM,有guid,无url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[3],   
            "things_id": device_id,
            "type": "bim",
            "url":None
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        sql = '''select * from building_model_things where id = '{}';'''.format(res.json()["id"])
        device_data = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertIsNotNone(res.json()["id"],run_method.errInfo(res))
        self.assertIsNotNone(device_data,run_method.errInfo(res))

    def test06_building_model_deviceadd_bim_url(self):
        """case06:添加关联设备[RCM]--类型为BIM,无guid,有url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": None,   
            "things_id": device_id,
            "type": "bim",
            "url":"https://www.baidu.com"
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test07_building_model_deviceadd_bim_GU(self):
        """case07:添加关联设备[RCM]--类型为BIM,有guid,有url"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[4],   
            "things_id": device_id,
            "type": "bim",
            "url":"https://www.baidu.com"
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        sql = '''select * from building_model_things where id = '{}';'''.format(res.json()["id"])
        device_data = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertIsNotNone(res.json()["id"],run_method.errInfo(res))
        self.assertIsNotNone(device_data,run_method.errInfo(res))
    
    def test08_building_model_deviceadd_extra_noUCG(self):
        """case08:添加关联设备[RCM]--类型为extra，无url,无coord,无guid"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": None,   
            "things_id": device_id,
            "type": "extra",
            "url": None,
            "coord": None
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test09_building_model_deviceadd_extra_url(self):
        """case09:添加关联设备[RCM]--类型为extra，无url,无coord,有guid"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[5],   
            "things_id": device_id,
            "type": "extra",
            "url": None,
            "coord": None
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test10_building_model_deviceadd_extra_url(self):
        """case10:添加关联设备[RCM]--类型为extra，有url，无coord"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,   
            "things_id": device_id,
            "type": "extra",
            "url": "https://www.baidu.com",
            "coord": None
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test11_building_model_deviceadd_extra_coord(self):
        """case11:添加关联设备[RCM]--类型为extra，无url,有coord"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,   
            "things_id": device_id,
            "type": "extra",
            "url": None,
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle":0
                }
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test12_building_model_deviceadd_UC(self):
        """case12:添加关联设备[RCM]--类型为extra，有url,有coord"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,   
            "things_id": device_id,
            "type": "extra",
            "url": "https://www.baidu.com",
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle":0
                }
            }
        res = run_method.post(self.api,json=data,headers=corp_header)
        sql = '''select * from building_model_things where id = '{}';'''.format(res.json()["id"])
        device_data = opera_db.get_fetchone(sql)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertIsNotNone(res.json()["id"],run_method.errInfo(res))
        self.assertIsNotNone(device_data,run_method.errInfo(res))

    def test13_building_model_deviceadd_rsm(self):
        """case13:添加关联设备[RSM]--新增无权限"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[6],   
            "things_id": device_id,
            "type": "bim"
            }
        res = run_method.post(self.api,json=data,headers=super_header)
        self.assertEqual(res.status_code,403,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

    def test14_building_model_deviceadd_noRole(self):
        """case14:添加关联设备[普通用户]--新增无权限"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[7],   
            "things_id": device_id,
            "type": "bim"
            }
        common_user_header = pub_param.common_user(corp_id)
        res = run_method.post(self.api,json=data,headers=common_user_header)
        self.assertEqual(res.status_code,403,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

    def test15_building_model_deviceadd_otherCorp(self):
        """case15:添加关联设备[其他组织RCM]--新增无权限"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[8],   
            "things_id": device_id,
            "type": "bim"
            }
        other_corp_header = pub_param.common_user(role=1<<19)
        res = run_method.post(self.api,json=data,headers=other_corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

    def test16_building_model_deviceadd_noAuth(self):
        """case16:添加关联设备--无Auth"""

        device_id = pub_param.create_device(header=corp_header)
        data = {
            "building_id": self.building_id,
            "guid": self.guidList[9],   
            "things_id": device_id,
            "type": "bim"
            }
        res = run_method.post(self.api,json=data)
        self.assertEqual(res.status_code,401,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

    @unittest.skip("暂时跳过")
    def test17_building_model_deviceadd_DelCorpUser(self):
        """case17:添加关联设备[RCM]--已删除管理员"""
        pass

class TestBuildingModelDevicelist(unittest.TestCase):

    def setUp(self):
        self.api = '/building/model/devicelist'
        self.data = {
            "page":1,
            "size":100
        }

    def test01_building_model_devicelist_noId(self):
        """case01:获取建筑内所有设备列表--无建筑ID"""

        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertEqual(res.json()["total"],"0",run_method.errInfo(res))
        

    def test02_building_model_devicelist_errId(self):
        """case02:获取建筑内所有设备列表--错误的建筑ID"""

        self.data.update(building_id="abc")
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertEqual(res.json()["total"],"0",run_method.errInfo(res))

    # 依赖 class TestBuildingModelDeviceadd 
    def test03_building_model_devicelist_success(self):
        """case03:获取建筑内所有设备列表--查询成功"""

        building_id = opera_json.get_data("deviceadd")["building_id"]
        self.data.update(building_id=building_id)
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        opera_assert.is_list_in(building_id,res.json()["data_list"],"building_id")