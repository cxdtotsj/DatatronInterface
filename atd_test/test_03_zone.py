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
from base.public_param import PublicParam
from util.operation_json import OperetionJson
from util.operation_assert import OperationAssert
from util.operation_db import OperationDB
import unittest
import time


class TestZone(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.opera_json = OperetionJson()
        cls.opera_assert = OperationAssert()
        cls.opera_db = OperationDB()
        cls.super_header = cls.pub_param.get_super_header()
        cls.corp_header, cls.corp_id = cls.pub_param.get_corp_user()

    def test01_01_zone_create_noName(self):
        '''case01_01:创建园区--无园区名称'''
        
        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("name")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1400, "状态码返回错误")

    def test01_02_zone_create_noBuildNum(self):
        '''case01_02:创建园区--无楼宇数量'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("building_num")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1400, "状态码返回错误")

    def test01_03_zone_create_noArea(self):
        '''case01_03:创建园区--无面积(默认为0)'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("area")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        zone_detail = self.pub_param.zone_get(
            res.json()["id"], self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(zone_detail["area"], 0, "面积默认值返回错误")

    def test01_04_zone_create_noLoc(self):
        '''case01_04:创建园区--无地址'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("loc")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1400, res_dict)

    def test01_05_zone_create_noCoord(self):
        '''case01_05:创建园区--无经纬度'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.pop("coord")
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1400, "状态码返回错误")

    def test01_06_zone_create_noExtra(self):
        '''case01_06:创建园区[ZCM]--无附加信息'''
        
        api = '/zone/create'
        data = Zone.zone_data()
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res_dict["corp_id"], self.corp_id, "组织ID返回错误")

        self.opera_json.check_json_value(
            "test01_06_zone_create_noExtra", res_dict["name"])

    def test01_07_zone_create_success(self):
        '''case01_07:创建园区[ZCM]--新增成功(全部信息)'''

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
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res_dict["corp_id"], self.corp_id, "组织ID返回错误")

        self.opera_json.check_json_value("test01_07_zone", {
                                         "zone_id": res_dict["id"], "data": data})

    # 依赖用例 test01_06_zone_create_noExtra
    def test01_08_zone_create_nameRepeat(self):
        '''case01_08:创建园区[ZCM]--园区名称重复'''

        api = '/zone/create'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        repeat_name = self.pub_param.zone_get(
            zone_id, self.corp_header)["name"]
        data = Zone.zone_data()
        data.update(name=repeat_name)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1409, res.json())

    def test01_09_zone_create_noCorpId(self):
        '''case01_09:创建园区[ZSM]--无CorpID'''

        api = '/zone/create'
        data = Zone.zone_data()
        res = self.run_method.post(api, json=data, headers=self.super_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1400, "状态码返回错误")

    def test01_10_zone_create_corpId(self):
        '''case01_10:创建园区[ZSM]--新增成功(指定CorpID)'''

        api = '/zone/create'
        data = Zone.zone_data()
        data.update(corp_id=self.corp_id)
        res = self.run_method.post(api, json=data, headers=self.super_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res_dict["corp_id"], self.corp_id, "组织ID返回错误")

    def test01_11_zone_create_noRole(self):
        '''case01_11:创建园区[普通用户]--普通组织用户新增'''

        api = '/zone/create'
        data = Zone.zone_data()
        common_user_header = self.pub_param.common_user(self.corp_id)
        res = self.run_method.post(api, json=data, headers=common_user_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res_dict["code"], 1403, "状态码返回错误")

    @unittest.skip("存在BUG，暂时跳过")
    def test01_12_zone_create_delCorpUser(self):
        '''case01_12:创建园区--已删除管理员新增园区'''

        api = '/zone/create'
        data = Zone.zone_data()

        # 获取该用户 token
        user_email,__,user_id = self.pub_param.user_reset_corp(self.corp_id,role=1<<19)
        user_header = self.pub_param.user_header(12345678,email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id,self.corp_id)

        # 新增园区
        res = self.run_method.post(api,json=data,headers=user_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")


    def test02_01_zone_get_noId(self):
        '''case02_01:获取园区详细信息--无园区ID'''

        api = '/zone/get'
        data = {"id": None}
        res = self.run_method.post(api, data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1404, "状态码返回错误")

    def test02_02_zone_get_otherId(self):
        '''case02_02:获取园区详细信息[ZCM]--其他组织的园区'''

        api = '/zone/get'
        # 创建其他组织园区
        zone_id = self.pub_param.create_zone()
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        res_dict = res.json()
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res_dict["code"], 1403, "状态码返回错误")

    # 依赖用例 test01_07_zone
    def test02_03_zone_get_success(self):
        '''case02_03:获取园区详细信息[ZCM]--所在组织的园区'''

        api = '/zone/get'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        zone_data = self.opera_json.get_data("test01_07_zone")["data"]
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断 新增的园区信息 是否返回正确
        self.opera_assert.is_dict_in(zone_data, res.json())

    # 依赖用例 test01_07_zone
    def test02_04_zone_get_zsm(self):
        '''case02_04:获取园区详细信息[ZSM]'''

        api = '/zone/get'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        zone_data = self.opera_json.get_data("test01_07_zone")["data"]
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断 新增的园区信息 是否返回正确
        self.opera_assert.is_dict_in(zone_data, res.json())

    # 依赖用例 test01_07_zone
    def test02_05_zone_get_noRole(self):
        '''case02_05:获取园区详细信息--普通组织用户'''

        api = '/zone/get'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        # 新建普通用户，无管理员权限
        common_user_header = self.pub_param.common_user(self.corp_id)
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, res.json())

    def test02_06_zone_get_errZoneId(self):
        '''case02_06:获取园区详细信息--错误的园区ID'''

        api = '/zone/get'
        data = {"id": 11223344}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 400, res.json())
        self.assertEqual(res.json()["code"], 1404, "状态码返回错误")

    def test03_01_zone_list_success(self):
        '''case03_01:园区列表[ZCM]--查看成功(corp_id)'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        res = self.run_method.post(api, data, headers=self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断返回的园区是否都为该 corp_id
        self.opera_assert.is_equal_value(
            self.corp_id, res.json()["data_list"], "corp_id")

    def test03_02_zone_list_zsm(self):
        '''case03_02:园区列表[ZSM]--超级管理员(total数量)'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        res = self.run_method.post(api, data, headers=self.super_header)
        sql = '''select id from zone where status != 3;'''
        zone_num = self.opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(res.json()["total"], str(zone_num), "返回的zone数量不正确")

    def test03_03_zone_list_noRole(self):
        '''case03_03:园区列表--组织普通用户'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        common_user_header = self.pub_param.common_user(self.corp_id)
        res = self.run_method.post(api, data, headers=common_user_header)
        self.assertEqual(res.status_code, 200, res.json())
        # 判断返回的园区是否都为该 corp_id
        self.opera_assert.is_equal_value(
            self.corp_id, res.json()["data_list"], "corp_id")

    def test03_04_zone_list_errUser(self):
        '''case03_04:园区列表--非法用户'''

        api = '/zone/list'
        data = {"page": 1,
                "size": 10}
        res = self.run_method.post(api, data, headers={"Authorization": "abc"})
        self.assertEqual(res.status_code, 401, res.json())
        self.assertEqual(res.json()["code"], 1401, "状态码返回错误")

    # 依赖用例 test01_07_zone
    def test04_01_zone_update_area(self):
        '''case04_01:编辑园区[RCM]--更新面积'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        data = self.pub_param.zone_get(zone_id, self.corp_header)
        data.update(area=50)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["area"], 50, "面积未更新成功")

    def test04_02_zone_update_buildingNum(self):
        '''case04_02:编辑园区[RCM]--更新楼宇数'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        data = self.pub_param.zone_get(zone_id, self.corp_header)
        data.update(building_num=28)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["building_num"], 28, "楼宇数未更新成功")

    def test04_03_zone_update_coord(self):
        '''case04_03:编辑园区[RCM]--更新经纬度'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        data = self.pub_param.zone_get(zone_id, self.corp_header)
        new_coord = {
            "longitude": 200,
            "latitude": 200,
            "altitude": 100
        }
        data.update(coord=new_coord)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["coord"], new_coord, "经纬度未更新成功")

    def test04_04_zone_update_extra(self):
        '''case04_04:编辑园区[RCM]--更新附加信息'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        data = self.pub_param.zone_get(zone_id, self.corp_header)
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
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["extra"], new_extra, "附加信息未更新成功")

    def test04_05_zone_update_rsmArea(self):
        '''case04_05:编辑园区[RSM]--超管更新面积'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        data = self.pub_param.zone_get(zone_id, self.super_header)
        data.update(area=9999)
        res = self.run_method.post(api, json=data, headers=self.corp_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["area"], 9999, "面积未更新成功")

    def test04_06_zone_update_noRole(self):
        '''case04_06:编辑园区[组织普通用户]--更新不成功'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        common_header = self.pub_param.common_user(self.corp_id)
        data = self.pub_param.zone_get(zone_id, self.corp_header)
        data.update(area=8888)
        res = self.run_method.post(api, json=data, headers=common_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")
        self.assertNotEqual(new_data["area"], 8888, "普通用户面积更新成功")

    def test04_07_zone_update_otherCorp(self):
        '''case04_07:编辑园区[其他组织管理员]--更新不成功'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        other_corp_header = self.pub_param.common_user(role=524288)
        data = self.pub_param.zone_get(zone_id, self.corp_header)
        data.update(area=6666)
        res = self.run_method.post(api, json=data, headers=other_corp_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(new_data["area"], 6666, "面积更新成功")

    @unittest.skip("存在BUG，暂时跳过")
    def test04_08_zone_update_delCorpUser(self):
        '''case04_08:编辑园区--已删除管理员编辑园区'''

        api = '/zone/update'
        zone_id = self.opera_json.get_data("test01_07_zone")["zone_id"]
        data = self.pub_param.zone_get(zone_id, self.corp_header)
        data.update(area=6789)

        # 获取该用户 token
        user_email,__,user_id = self.pub_param.user_reset_corp(self.corp_id,role=1<<19)
        user_header = self.pub_param.user_header(12345678,email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id,self.corp_id)

        # 编辑园区
        res = self.run_method.post(api,json=data,headers=user_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")
        self.assertNotEqual(new_data["area"], 6789, "普通用户面积更新成功")


    def test05_01_zone_del_success(self):
        '''case05_01:删除园区[ZCM]--删除成功'''

        api = '/zone/del'
        zone_id = self.pub_param.create_zone(header=self.corp_header)
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=self.corp_header)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["status"], 3, "园区未成功删除")

    def test05_02_zone_del_zsm(self):
        '''case05_02:删除园区[ZSM]--删除成功'''

        api = '/zone/del'
        zone_id = self.pub_param.create_zone(header=self.corp_header)
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=self.super_header)
        time.sleep(2)
        new_data = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertEqual(new_data["status"], 3, "园区未成功删除")

    def test05_03_zone_del_noRole(self):
        '''case05_03:删除园区[普通用户]--删除失败'''

        api = '/zone/del'
        zone_id = self.pub_param.create_zone(header=self.corp_header)
        common_header = self.pub_param.common_user(self.corp_id)
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=common_header)
        zone_detail = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "普通用户删除园区成功")
        self.assertNotEqual(zone_detail["status"], 3, "园区被普通用户删除")

    def test05_04_zone_del_otherCorp(self):
        '''case05_04:删除园区[其他组织管理员]--删除失败'''
        
        api = '/zone/del'
        zone_id = self.pub_param.create_zone(header=self.corp_header)
        other_corp_header = self.pub_param.common_user(role=524288)
        data = {"id": zone_id}
        res = self.run_method.post(api, data, headers=other_corp_header)
        zone_detail = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 200, res.json())
        self.assertNotEqual(zone_detail["status"], 3, "园区被其他组织管理员删除")

    @unittest.skip("存在BUG，暂时跳过")
    def test05_05_zone_del_noRole(self):
        '''case05_05:删除园区--已删除管理员删除建筑'''

        api = '/zone/del'
        zone_id = self.pub_param.create_zone(header=self.corp_header)
        data = {"id": zone_id}

        # 获取该用户 token
        user_email,__,user_id = self.pub_param.user_reset_corp(self.corp_id,role=1<<19)
        user_header = self.pub_param.user_header(12345678,email=user_email)

        # 把用户从 corp 中删除
        self.pub_param.user_corp_del(user_id,self.corp_id)

        # 删除园区
        res = self.run_method.post(api,data,headers=user_header)
        zone_detail = self.pub_param.zone_get(zone_id, self.corp_header)
        self.assertEqual(res.status_code, 403, res.json())
        self.assertEqual(res.json()["code"], 1403, "状态码返回错误")
        self.assertNotEqual(zone_detail["status"], 3, "园区被普通用户删除")