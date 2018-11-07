'''
园区类接口

test01 : /zone/create
test02 : /zone/get
test03 : /zone/list
test04 : /zone/update
test05 : /zone/del

'''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import ZoneApiData as Zone
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

class TestZoneCreate(unittest.TestCase):

    def test01_zone_create_noName(self):
        '''case01:创建园区--无园区名称'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("name")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_zone_create_noBuildNum(self):
        '''case02:创建园区--无楼宇数量'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("building_num")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_zone_create_noArea(self):
        '''case03:创建园区--无面积(默认为0)'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("area")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        zone_detail = pub_param.zone_get(
            res.json()["id"], corp_header)
        self.assertEqual(zone_detail["area"], 0, "面积默认值返回错误")

    def test04_zone_create_noLoc(self):
        '''case04:创建园区--无地址'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("loc")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_zone_create_noCoord(self):
        '''case05:创建园区--无经纬度'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("coord")
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test06_zone_create_noExtra(self):
        '''case06:创建园区[ZCM]--无附加信息'''

        api = '/zone/create'
        data = Zone.zone_data()
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))

    def test07_zone_create_success(self):
        '''case07:创建园区[ZCM]--新增成功(全部信息)'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.update({
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
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))

        opera_json.check_json_value("test07_zone_create", {
                                         "zone_id": res.json()["id"], "data": data})

    # 依赖用例 test07_zone_create_success
    def test08_zone_create_nameRepeat(self):
        '''case08:创建园区[ZCM]--园区名称重复'''

        api = '/zone/create'
        zone_id = opera_json.get_data("test07_zone_create")["zone_id"]
        repeat_name = pub_param.zone_get(
            zone_id, corp_header)["name"]
        data = Zone.zone_data()
        data.update(name=repeat_name)
        res = run_method.post(api, json=data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1409, run_method.errInfo(res))

    def test09_zone_create_noCorpId(self):
        '''case09:创建园区[ZSM]--无CorpID'''

        api = '/zone/create'
        data = Zone.zone_data()
        res = run_method.post(api, json=data, headers=super_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test10_zone_create_corpId(self):
        '''case10:创建园区[ZSM]--新增成功(指定CorpID)'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.update(corp_id=corp_id)
        res = run_method.post(api, json=data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["corp_id"], corp_id, run_method.errInfo(res))

    def test11_zone_create_noRole(self):
        '''case11:创建园区[普通用户]--普通组织用户新增'''

        api = '/zone/create'
        data = Zone.zone_data()
        common_user_header = pub_param.common_user(corp_id)
        res = run_method.post(api, json=data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    @unittest.skip("存在BUG，暂时跳过")
    def test12_zone_create_delCorpUser(self):
        '''case12:创建园区--已删除管理员新增园区'''

        api = '/zone/create'
        data = Zone.zone_data()

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


class TestZoneGet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.zone_data = Zone.zone_data()
        cls.zone_data.update({
            "extra": {
                "build_corp": "建筑单位名称",
                "build_start_at": "2018-10-10",
                "construct_corp": "规划单位名称",
                "construct_end_at": "2018-10-10",
                "design_corp": "设计单位名称",
                "design_end_at": "2018-10-10",
                "plan_corp": "施工单位名称",
                "plan_end_at": "2018-10-10",
                "supervise_corp": "监理单位名称",
                "supervise_end_at": "2018-10-10"
            }
        })
        cls.zone_id = pub_param.create_zone(corp_header,cls.zone_data)

    def test01_zone_get_noId(self):
        '''case01:获取园区详细信息--无园区ID'''

        api = '/zone/get'
        data = {"id": None}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))

    def test02_zone_get_otherId(self):
        '''case02:获取园区详细信息[ZCM]--其他组织的园区'''

        api = '/zone/get'
        zone_id = pub_param.create_zone()   # 创建其他组织园区
        data = {"id": zone_id}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test03_zone_get_success(self):
        '''case03:获取园区详细信息[ZCM]--所在组织的园区'''

        api = '/zone/get'
        data = {"id": self.zone_id}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断 新增的园区信息 是否返回正确
        opera_assert.is_dict_in(self.zone_data, res.json())

    def test04_zone_get_zsm(self):
        '''case04:获取园区详细信息[ZSM]'''

        api = '/zone/get'
        data = {"id": self.zone_id}
        res = run_method.post(api, data, headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断 新增的园区信息 是否返回正确
        opera_assert.is_dict_in(self.zone_data, res.json())

    def test05_zone_get_noRole(self):
        '''case05:获取园区详细信息--普通组织用户'''

        api = '/zone/get'
        # 新建普通用户，无管理员权限
        common_user_header = pub_param.common_user(corp_id)
        data = {"id": self.zone_id}
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

    def test06_zone_get_errZoneId(self):
        '''case06:获取园区详细信息--错误的园区ID'''

        api = '/zone/get'
        data = {"id": 11223344}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))


class TestZoneList(unittest.TestCase):

    def test01_zone_list_success(self):
        '''case01:园区列表[ZCM]--查看成功(corp_id)'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断返回的园区是否都为该 corp_id
        opera_assert.is_equal_value(
            corp_id, res.json()["data_list"], "corp_id")

    def test02_zone_list_zsm(self):
        '''case02:园区列表[ZSM]--超级管理员(total数量)'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        res = run_method.post(api, data, headers=super_header)
        sql = '''select id from zone where status not in (0,3);'''
        zone_num = opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(zone_num), run_method.errInfo(res))

    def test03_zone_list_noRole(self):
        '''case03:园区列表--组织普通用户'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        common_user_header = pub_param.common_user(corp_id)
        res = run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 判断返回的园区是否都为该 corp_id
        opera_assert.is_equal_value(
            corp_id, res.json()["data_list"], "corp_id")

    def test04_zone_list_errUser(self):
        '''case04:园区列表--非法用户'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        res = run_method.post(api, data, headers={"Authorization": "abc"})
        self.assertEqual(res.status_code, 401, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))


class TestZoneUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.zone_data = Zone.zone_data()
        cls.zone_data.update({
            "extra": {
                "build_corp": "建筑单位名称",
                "build_start_at": "2019-10-10",
                "construct_corp": "规划单位名称",
                "construct_end_at": "2019-10-10",
                "design_corp": "设计单位名称",
                "design_end_at": "2019-10-10",
                "plan_corp": "施工单位名称",
                "plan_end_at": "2019-10-10",
                "supervise_corp": "监理单位名称",
                "supervise_end_at": "2019-10-10"
            }
        })
        cls.zone_id = pub_param.create_zone(corp_header,cls.zone_data)

    def test01_zone_update_area(self):
        '''case01:编辑园区[RCM]--更新面积'''

        api = '/zone/update'
        data = pub_param.zone_get(self.zone_id, corp_header)
        data.update(area=50)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["area"], 50, "面积未更新成功")

    def test02_zone_update_buildingNum(self):
        '''case02:编辑园区[RCM]--更新楼宇数'''

        api = '/zone/update'
        data = pub_param.zone_get(self.zone_id, corp_header)
        data.update(building_num=28)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["building_num"], 28, "楼宇数未更新成功")

    def test03_zone_update_coord(self):
        '''case03:编辑园区[RCM]--更新经纬度'''

        api = '/zone/update'
        data = pub_param.zone_get(self.zone_id, corp_header)
        new_coord = {
            "longitude": 200,
            "latitude": 200,
            "altitude": 100,
            "angle":90
        }
        data.update(coord=new_coord)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["coord"], new_coord, "经纬度未更新成功")

    def test04_zone_update_extra(self):
        '''case04:编辑园区[RCM]--更新附加信息'''

        api = '/zone/update'
        data = pub_param.zone_get(self.zone_id, corp_header)
        new_extra = {
            "build_corp": "更新建筑单位名称",
            "build_start_at": "2018-10-10",
            "construct_corp": "更新规划单位名称",
            "construct_end_at": "2018-10-10",
            "design_corp": "更新设计单位名称",
            "design_end_at": "2018-10-10",
            "plan_corp": "更新施工单位名称",
            "plan_end_at": "2018-10-10",
            "supervise_corp": "更新监理单位名称",
            "supervise_end_at": "2018-10-10"
        }
        data.update(extra=new_extra)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["extra"], new_extra, "附加信息未更新成功")

    def test05_zone_update_rsmArea(self):
        '''case05:编辑园区[RSM]--超管更新面积'''

        api = '/zone/update'
        data = pub_param.zone_get(self.zone_id, super_header)
        data.update(area=9999)
        res = run_method.post(api, json=data, headers=corp_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["area"], 9999, "面积未更新成功")

    def test06_zone_update_noRole(self):
        '''case06:编辑园区[组织普通用户]--更新不成功'''

        api = '/zone/update'
        common_header = pub_param.common_user(corp_id)
        data = pub_param.zone_get(self.zone_id, corp_header)
        data.update(area=8888)
        res = run_method.post(api, json=data, headers=common_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["area"], 8888, "普通用户面积更新成功")

    def test07_zone_update_otherCorp(self):
        '''case07:编辑园区[其他组织管理员]--更新不成功'''

        api = '/zone/update'
        other_corp_header = pub_param.common_user(role=524288)
        data = pub_param.zone_get(self.zone_id, corp_header)
        data.update(area=6666)
        res = run_method.post(api, json=data, headers=other_corp_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(new_data["area"], 6666, "面积更新成功")

    @unittest.skip("存在BUG，暂时跳过")
    def test08_zone_update_delCorpUser(self):
        '''case08:编辑园区--已删除管理员编辑园区'''

        api = '/zone/update'
        data = pub_param.zone_get(self.zone_id, corp_header)
        data.update(area=6789)

        # 获取该用户 token
        user_email, __, user_id = pub_param.user_reset_corp(
            corp_id, role=1 << 19)
        user_header = pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        pub_param.user_corp_del(user_id, corp_id)

        # 编辑园区
        res = run_method.post(api, json=data, headers=user_header)
        new_data = pub_param.zone_get(self.zone_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(new_data["area"], 6789, "普通用户面积更新成功")


class TestZoneDel(unittest.TestCase):

    def test01_zone_del_success(self):
        '''case01:删除园区[ZCM]--删除成功'''

        api = '/zone/del'
        zone_id = pub_param.create_zone(header=corp_header)
        data = {"id": zone_id}
        res = run_method.post(api, data, headers=corp_header)
        new_data = pub_param.zone_get(zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 3, "园区未成功删除")

    def test02_zone_del_zsm(self):
        '''case02:删除园区[ZSM]--删除成功'''

        api = '/zone/del'
        zone_id = pub_param.create_zone(header=corp_header)
        data = {"id": zone_id}
        res = run_method.post(api, data, headers=super_header)
        time.sleep(2)
        new_data = pub_param.zone_get(zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 3, "园区未成功删除")

    def test03_zone_del_noRole(self):
        '''case03:删除园区[普通用户]--删除失败'''

        api = '/zone/del'
        common_header = pub_param.common_user(corp_id)
        zone_id = pub_param.create_zone(header=corp_header)
        data = {"id": zone_id}
        res = run_method.post(api, data, headers=common_header)
        zone_detail = pub_param.zone_get(zone_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(zone_detail["status"], 3, "园区被普通用户删除")

    def test04_zone_del_otherCorp(self):
        '''case04:删除园区[其他组织管理员]--删除失败'''

        api = '/zone/del'
        other_corp_header = pub_param.common_user(role=524288)
        zone_id = pub_param.create_zone(header=corp_header)
        data = {"id": zone_id}
        res = run_method.post(api, data, headers=other_corp_header)
        zone_detail = pub_param.zone_get(zone_id, corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotEqual(zone_detail["status"], 3, "园区被其他组织管理员删除")

    @unittest.skip("存在BUG，暂时跳过")
    def test05_zone_del_noRole(self):
        '''case05:删除园区--已删除管理员删除建筑'''

        api = '/zone/del'
        zone_id = pub_param.create_zone(header=corp_header)
        data = {"id": zone_id}

        # 获取该用户 token
        user_email, __, user_id = pub_param.user_reset_corp(
            corp_id, role=1 << 19)
        user_header = pub_param.user_header(12345678, email=user_email)

        # 把用户从 corp 中删除
        pub_param.user_corp_del(user_id, corp_id)

        # 删除园区
        res = run_method.post(api, data, headers=user_header)
        zone_detail = pub_param.zone_get(zone_id, corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertNotEqual(zone_detail["status"], 3, "园区被普通用户删除")
