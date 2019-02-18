'''
建筑模型相关

/model/upload
/model/update
/model/nameupdate
/model/list
/model/listv2
/model/entityget
/model/buildingget

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
common_user_header = pub_param.get_common_user()
other_corp_header = pub_param.get_otherCorp_user()


class TestModelUpload(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.building_id = pub_param.create_building(header=corp_header)
        cls.layer_id = pub_param.create_building_layer(cls.building_id,corp_header)

    def setUp(self):
        self.api = '/model/upload'
        self.data = {
            "building_id": self.building_id,
            "layer_id":self.layer_id,
            "model_type": "T",
            "model_name": "模型上传测试"
        }

    def test01_model_upload_noBuildingId(self):
        """case01:上传建筑模型[RCM]--无建筑ID"""

        self.data.update(building_id=None)
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_model_upload_errBuildingId(self):
        """case02:上传建筑模型[RCM]--错误的建筑ID"""

        self.data.update(building_id="112233")
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))

    def test03_model_upload_noModelType(self):
        """case03:上传建筑模型[RCM]--无建筑物类型"""

        self.data.update(model_type=None)
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotIn("err", res.json(), run_method.errInfo(res))

    def test04_model_upload_errModelType(self):
        """case04:上传建筑模型[RCM]--错误的建筑物类型"""

        self.data.update(model_type="ZSS")
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_model_upload_noFile(self):
        """case05:上传建筑模型[RCM]--无模型文件"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test06_model_upload_doubleType(self):
        """case06:上传建筑模型[RCM]--上传类型T、B,验证data.json未被覆盖"""

        # 上传全类型 T 的模型文件
        layer_id = pub_param.create_building_layer(self.building_id,corp_header) # 新增一个楼层
        self.data.update(layer_id=layer_id)
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res_t = run_method.post(self.api,self.data,files=files,headers=corp_header)
        self.assertEqual(res_t.status_code, 200, run_method.errInfo(res_t))
        metaUrl_t = res_t.json()["meta_url"]
        guid_t_one = pub_param.get_guid(metaUrl_t)  # 第一次获取 t 的 guid
        # 上传类型 B 的模型文件
        self.data.update(model_type="B")
        with open(Building.file_LangChaV2, 'rb') as fileop:
            files = {"file": fileop}
            res_b = run_method.post(self.api,self.data,files=files,headers=corp_header)
        self.assertEqual(res_b.status_code, 200, run_method.errInfo(res_b))
        guid_t_two = pub_param.get_guid(metaUrl_t)  # 第二次获取 t 的guid
        metaUrl_b = res_b.json()["meta_url"]
        guid_b = pub_param.get_guid(metaUrl_b)     # 获取类型B的guid
        self.assertEqual(guid_t_one, guid_t_two, "上传其他类型模型后，T类型的data被覆盖")
        self.assertNotEqual(guid_t_two, guid_b, "上传其他类型模型后，T类型被B类型覆盖")

    def test07_model_upload_rsm(self):
        """case07:上传建筑模型[RSM]--RSM上传建筑模型"""

        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=super_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test08_model_upload_noRole(self):
        """case08:上传建筑模型[普通用户]--普通用户上传建筑模型"""

        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test09_model_upload_OtherCorp(self):
        """case09:上传建筑模型[RCM]--RCM上传其他组织的建筑模型"""

        building_id = pub_param.create_building()
        self.data.update(building_id=building_id)
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test10_model_upload_multLayer(self):
        """case10:上传建筑模型[RCM]--多楼层上传建筑模型"""
        
        layer_id = pub_param.create_building_layer(self.building_id,corp_header)
        self.data.update(layer_id=layer_id)
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertNotIn("err", res.json(), run_method.errInfo(res))

    def test11_model_upload_multModel(self):
        """case11:上传建筑模型[RCM]--同楼层上传同专业建筑模型(应无法上传)"""
        
        layer_id = pub_param.create_building_layer(self.building_id,corp_header)
        self.data.update(layer_id=layer_id)
        pub_param.building_model_upload(
            building_id=self.building_id,header=corp_header,model_type="T",layer_id=layer_id) # 第一次上传
        with open(Building.file_TPY_7, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))        


class TestModelUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        构造用例依赖数据，上传类型为A的模型
        """
        __, cls.building_id = pub_param.building_model_upload(
            header=corp_header, model_type="A")
        res_models = pub_param.get_model_listv2(header=corp_header,building_id=cls.building_id, )
        cls.model_id = res_models["data_list"][0]["id"]
        cls.file_name = res_models["data_list"][0]["file_name"].split("|")[1]
        cls.model_type = res_models["data_list"][0]["model_type"]
        cls.model_name = res_models["data_list"][0]["model_name"]

    def setUp(self):
        self.api = '/model/update'
        self.data = {
            "model_id": self.model_id,
            "model_type": "T",
            "model_name": "更新后模型"
        }

    def test01_model_update_rsm(self):
        """case01:更新建筑模型[RSM]--RSM更新建筑模型"""

        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(self.api, self.data, files=files,headers=super_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test02_model_update_noRole(self):
        """case02:更新建筑模型[普通用户]--普通用户更新建筑模型"""

        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test03_model_update_otherCorp(self):
        """case03:更新建筑模型[其他组织RCM]--其他组织RCM更新建筑模型"""

        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=other_corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test04_model_update_noModelId(self):
        """case04:更新建筑模型[RCM]--无模型ID"""

        self.data.update(model_id=None)
        with open(Building.file_Office, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test05_model_update_noModelType(self):
        """case05:更新建筑模型[RCM]--无模型类型(默认为T)"""

        self.data.update(model_type=None)
        with open(Building.file_LangChaV2, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

        # 获取更新后的model信息
        model_res = pub_param.get_model_listv2(header=corp_header,building_id=self.building_id, )
        if len(model_res["data_list"]) == 1:    # 判断是否新上传文件
            m_type = model_res["data_list"][0]["model_type"]
            self.assertNotEqual(self.model_type, m_type,
                                "模型类型未更新,model_id : {}".format(self.model_id))
        else:
            print("模型未更新,新增模型文件,model_id : {}".format(self.model_id))

    def test06_model_update_noModelFile(self):
        """case06:更新建筑模型[RCM]--无模型文件"""

        files = {"file": None}
        res = run_method.post(self.api, self.data,
                              files=files, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test07_model_update_success(self):
        """case07:更新建筑模型[RCM]--更新成功(模型文件)"""

        self.data.update(
            {
                "model_type": "B",
                "model_name": "第二次更新"
            }
        )
        with open(Building.file_TPY_7, 'rb') as fileop:
            files = {"file": fileop}
            res = run_method.post(
                self.api, self.data, files=files, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))

        # 获取更新后的model信息
        model_res = pub_param.get_model_listv2(header=corp_header,building_id=self.building_id)
        if len(model_res["data_list"]) == 1:    # 判断是否新上传文件
            m_type = model_res["data_list"][0]["model_type"]
            try:
                m_file = model_res["data_list"][0]["file_name"].split("|")[1]
            except IndexError:
                print("获取模型文件名失败，返回的model_list:{}".format(model_res))
            m_name = model_res["data_list"][0]["model_name"]
            self.assertNotEqual(self.model_type, m_type,
                                "模型类型未更新,model_id : {}".format(self.model_id))
            self.assertNotEqual(self.file_name, m_file,
                                "模型文件名未更新,model_id : {}".format(self.model_id))
            self.assertNotEqual(self.model_name, m_name,
                                "模型名称未更新,model_id : {}".format(self.model_id))
        else:
            print("模型未更新,新增模型文件,model_id : {}".format(self.model_id))

@unittest.skip("issue=#45")
class TestModelEntityget(unittest.TestCase):

    def setUp(self):
        self.api = '/model/entityget'

    def test01_model_entityget_noModelId(self):
        """case01:获取构件信息--无模型ID"""

        r, building_id = pub_param.building_model_upload(
            header=corp_header)
        meta_url, model_id = r["meta_url"], r["model_id"]
        entities = pub_param.get_entities(meta_url)
        guids = [entity["Guid"] for entity in entities]
        data = {
            "model_id": None,
            "guid": guids[0]
        }
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

        opera_json.check_json_value("test01_model_entityget",
                                    {"building_id": building_id,
                                     "model_id": model_id,
                                     "guid": guids[0],
                                     "guid_last": guids[-1]})

    # 依赖用例 test01_building_model_entityget
    def test02_model_entityget_errModelId(self):
        """case02:获取构件信息--错误的模型ID"""

        guid = opera_json.get_data("test01_model_entityget")["guid"]
        data = {
            "model_id": "112233",
            "guid": guid
        }
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 13, run_method.errInfo(res))

    def test03_model_entityget_noGuId(self):
        """case03:获取构件信息--无构件ID"""

        model_id = opera_json.get_data(
            "test01_model_entityget")["model_id"]
        data = {
            "model_id": model_id,
            "guid": None
        }
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test04_model_entityget_errGuId(self):
        """case04:获取构件信息--错误的构件ID"""

        model_id = opera_json.get_data(
            "test01_model_entityget")["model_id"]
        data = {
            "model_id": model_id,
            "guid": "abc123"
        }
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 13, run_method.errInfo(res))

    def test05_model_entityget_success(self):
        """case05:获取构件信息--查询成功"""

        __, model_id, guid, __ = opera_json.get_data(
            "test01_model_entityget").values()
        data = {
            "model_id": model_id,
            "guid": guid}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["Guid"], guid, run_method.errInfo(res))

    def test06_model_entityget_lastGuid(self):
        """case06:获取构件信息--查询成功"""

        __, model_id, __, guid_last = opera_json.get_data(
            "test01_model_entityget").values()
        data = {
            "model_id": model_id,
            "guid": guid_last}
        res = run_method.post(self.api, data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["Guid"],
                         guid_last, run_method.errInfo(res))


class TestModelNameupdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        res, cls.building_id = pub_param.building_model_upload(
            header=corp_header)
        cls.model_id = res["model_id"]

    def setUp(self):
        self.api = '/model/nameupdate'
        self.data = {
            "id": self.model_id,
            "model_name": "更新后模型名称"
        }

    def test01_model_nameupdate_noModelId(self):
        """case01:编辑模型名称[RCM]--无模型ID"""

        self.data.update(id=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_model_nameupdate_noModelName(self):
        """case02:编辑模型名称[RCM]--无模型名称"""

        self.data.update(model_name=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_model_nameupdate_rsm(self):
        """case03:编辑模型名称[RSM]--更新受限"""

        res = run_method.post(self.api, self.data, headers=super_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test04_model_nameupdate_noRole(self):
        """case04:编辑模型名称[普通用户]--更新受限"""

        res = run_method.post(self.api, self.data, headers=common_user_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test05_model_nameupdate_otherCorp(self):
        """case05:编辑模型名称[其他组织RCM]--更新受限"""

        res = run_method.post(self.api, self.data, headers=other_corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

    def test06_model_nameupdate_modelName(self):
        """case06:编辑模型名称[RCM]--模型名称更新成功"""

        self.data.update(model_name="test06模型名称")
        res = run_method.post(self.api, self.data, headers=corp_header)
        model_res = pub_param.get_model_listv2(header=corp_header,building_id=self.building_id)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(model_res["data_list"][0]["model_name"],
                         self.data["model_name"], run_method.assertInfo(model_res))

    def test07_model_nameupdate_layerName(self):
        """case07:编辑模型名称[RCM]--楼层名称更新成功"""

        self.data.update(layer_name="test07楼层名称")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 获取更新后的楼层名称
        layer_name = pub_param.get_building_layerList(self.building_id,corp_header)[0]["name"]
        self.assertEqual(layer_name,"test07楼层名称",run_method.errInfo(res))


class TestModelListv2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 新增园区
        cls.zone_id = pub_param.create_zone(header=corp_header) 
        # 新增园区所属建筑
        cls.building_one = pub_param.create_building(zone_id=cls.zone_id,header=corp_header)
        cls.building_two = pub_param.create_building(zone_id=cls.zone_id,header=corp_header)
        # 新增 building_one 所属楼层,上传模型
        cls.layer_one = pub_param.create_building_layer(cls.building_one,corp_header)
        pub_param.building_model_upload(building_id=cls.building_one,header=corp_header,layer_id=cls.layer_one)
        # 新增 building_two 所属楼层
        for _ in range(0,2):
            pub_param.building_model_upload(building_id=cls.building_two,header=corp_header) # 新增楼层，并上传模型
    
    def setUp(self):
        self.api = '/model/listv2'
        self.data = {
            "zone_id": None,
            "building_id": None,
            "layer_id": None
        }

    def test01_model_listv2_noId(self):
        """case01:模型列表[RCM]--无ID"""
        
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 0, run_method.errInfo(res))

    def test02_model_listv2_layerId(self):
        """case02:模型列表[RCM]--只传楼层ID"""

        self.data.update(layer_id=self.layer_one)
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 1, run_method.errInfo(res))
        self.assertEqual(res.json()["data_list"][0]["layer_id"], self.layer_one, run_method.errInfo(res))
        self.assertNotEqual(res.json()["data_list"][0]["id"], "", run_method.errInfo(res))

    def test03_model_listv2_buildingId(self):
        """case03:模型列表[RCM]--只传建筑ID"""

        self.data.update(building_id=self.building_two)
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 2, run_method.errInfo(res)) # building_two 有2个楼层,每层一个模型
        opera_assert.is_list_in(self.building_two,res.json()["data_list"],"building_id")

    def test04_model_listv2_zoneId(self):
        """case04:模型列表[RCM]--只传园区ID"""

        self.data.update(zone_id=self.zone_id)
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(len(res.json()["data_list"]), 3, run_method.errInfo(res)) # zone 有3个楼层,每层一个模型

    def test05_model_listv2_zoneBuildId(self):
        """case05:模型列表[RCM]--同时传园区建筑ID"""

        self.data.update({
            "zone_id":self.zone_id,
            "building_id":self.building_two
        })
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test06_model_listv2_zoneLayerId(self):
        """case06:模型列表[RCM]--同时传园区楼层ID"""

        self.data.update({
            "zone_id":self.zone_id,
            "layer_id":self.layer_one
        })
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))   

    def test07_model_listv2_buildLayerId(self):
        """case07:模型列表[RCM]--同时传建筑楼层ID"""

        self.data.update({
            "building_id":self.building_one,
            "layer_id":self.layer_one
        })
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test08_model_listv2_zoneBuildLayerId(self):
        """case08:模型列表[RCM]--同时传园区建筑楼层ID"""

        self.data.update({
            "zone_id":self.zone_id,
            "building_id":self.building_one,
            "layer_id":self.layer_one
        })
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))


class TestModelBuildingget(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        model_resp,cls.building_id = pub_param.building_model_upload(header=corp_header)
        cls.model_id = model_resp["model_id"]

    def setUp(self):
        self.api = '/model/buildingget'
        self.data = {
            "id": self.model_id
        }

    def test01_model_buildingget_noId(self):
        """case01:建筑详细信息[RCM]--无模型ID"""

        self.data.update(id=None)
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))
    
    def test02_model_buildingget_rsm(self):
        """case02:建筑详细信息[RSM]--查询成功"""

        res = run_method.post(self.api,self.data,headers=super_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], self.building_id, run_method.errInfo(res))

    def test03_model_buildingget_rcm(self):
        """case03:建筑详细信息[RCM]--查询成功"""

        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], self.building_id, run_method.errInfo(res))
    
    def test04_model_buildingget_commUser(self):
        """case04:建筑详细信息[普通用户]--查询受限"""

        res = run_method.post(self.api,self.data,headers=common_user_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["id"], self.building_id, run_method.errInfo(res))

    def test05_model_buildingget_otherCorp(self):
        """case05:建筑详细信息[普通用户]--查询受限"""

        res = run_method.post(self.api,self.data,headers=other_corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))