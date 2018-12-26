'''
建筑类接口

/building/create
/building/get
/building/list
/building/update
/building/del

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
        self.assertEqual(res.json()["corp_id"],
                         corp_id, run_method.errInfo(res))
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
        self.assertEqual(res.json()["corp_id"],
                         corp_id, run_method.errInfo(res))
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
        self.assertEqual(res.json()["corp_id"],
                         corp_id, run_method.errInfo(res))
        self.assertEqual(building_detail["zone_id"], zone_id, "园区建筑不存在园区ID")

        opera_json.check_json_value("test09_building_create", {"id": res.json()[
            "id"], "zone_id": zone_id, "name": data["name"], "data": data})

    # 依赖用例 test07_building_create_noZoneId
    def test10_building_create_nameRepeat(self):
        '''case10:创建建筑[ZCM]--名称重复(无ZoneID,不同的corp_id)'''

        api = '/building/create'
        repeat_name = opera_json.get_data(
            "test07_building_create")["name"]
        data = Building.building_data()
        data.update(name=repeat_name)
        res = run_method.post(api, json=data, headers=other_corp_header)
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
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

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
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

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
        self.assertEqual(res.json()["corp_id"],
                         corp_id, run_method.errInfo(res))

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
        cls.building_id = pub_param.create_sign_building(
            cls.building_data, corp_header)

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
        # 上传模型
        pub_param.building_model_upload(self.building_id, corp_header)
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断 新增的园区信息 是否返回正确
        opera_assert.is_dict_in(self.building_data, res.json())
        self.assertNotEqual(
            len(res.json()["models"]), 0, run_method.errInfo(res))

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

    def setUp(self):
        self.api = '/building/list'
        self.data = {
            "page": 1,
            "limit": 100
        }

    def test01_building_list_success(self):
        '''case01:建筑列表[RCM]--查看成功,无zone_id(corp_id)'''

        pub_param.create_building(header=corp_header)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["total"], '0', run_method.errInfo(res))
        # 判断返回的建筑是否都为该 corp_id
        opera_assert.is_list_in(
            corp_id, res.json()["data_list"], "corp_id")

    def test02_building_list_zoneId(self):
        '''case02:建筑列表[RCM]--园区ID过滤(zone_id)'''

        zone_id = pub_param.create_zone(corp_header)  # 新增园区
        pub_param.create_building(
            zone_id=zone_id, header=corp_header)  # 新增属于园区的建筑
        self.data.update(zone_id=zone_id)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["total"], '0', run_method.errInfo(res))
        # 判断返回的建筑是否都为该 zone_id
        opera_assert.is_list_in(
            zone_id, res.json()["data_list"], "zone_id")

    def test03_building_list_rsm(self):
        '''case03:建筑列表[RSM]--超级管理员(total数量)'''

        api = '/building/list'
        data = {"page": 1,
                "limit": 100}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test04_building_list_noRole(self):
        '''case04:建筑列表--组织普通用户'''

        api = '/building/list'
        data = {"page": 1,
                "limit": 100}
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(res.json()["total"], '0', run_method.errInfo(res))
        # 判断返回的建筑是否都为该 corp_id
        opera_assert.is_list_in(
            corp_id, res.json()["data_list"], "corp_id")

    def test05_building_list_noRole(self):
        '''case05:建筑列表--非法用户'''

        api = '/building/list'
        data = {"page": 1,
                "limit": 100}
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
        cls.building_id = pub_param.create_sign_building(
            building_data, corp_header)

    def test02_building_update_nameRepeat(self):
        '''case02:编辑建筑[RCM]--重复名称'''

        api = '/building/update'
        bud_one_id = pub_param.create_sign_building(
            header=corp_header)           # 新增独栋建筑一
        bud_two_id = pub_param.create_sign_building(
            header=corp_header)           # 新增独栋建筑二
        bud_one_name = pub_param.building_get(bud_one_id, corp_header)[
            "name"]    # 获取独栋建筑一 name
        bud_two_data = pub_param.building_get(
            bud_two_id, corp_header)            # 获取独栋建筑二 data
        # 更新独栋建筑二的 name,和第一栋建筑一致
        bud_two_data.update(name=bud_one_name)
        res = run_method.post(api, json=bud_two_data, headers=corp_header)
        bud_two_new_data = pub_param.building_get(bud_two_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 第二栋更新后的name和建筑一一致
        self.assertEqual(
            bud_two_new_data["name"], bud_one_name, "建筑名称更新未成功")

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