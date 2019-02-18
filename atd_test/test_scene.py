'''
场景类接口

/scene/create
/scene/get
/scene/list
/scene/update
/scene/modelurllist
/scene/del

'''

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_method import BaseMethod
from data.public_param import PublicParam
from util.operation_assert import OperationAssert
from util.operation_db import OperationDB
from util.operation_json import OperetionJson
from data.api_data import SceneApiData as Scene
import unittest

run_method = BaseMethod()
pub_param = PublicParam()
opera_assert = OperationAssert()
opera_db = OperationDB()
opera_json = OperetionJson()
super_header = pub_param.get_super_header()
corp_header, corp_id = pub_param.get_corp_user()
common_user_header = pub_param.get_common_user()
other_corp_header = pub_param.get_otherCorp_user()


class TestSceneCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.zone_pid = pub_param.create_scene(header=corp_header) # 园区父场景
        cls.build_pid = pub_param.create_scene(header=corp_header,parent_id=cls.zone_pid) # 建筑父场景
        # depend by class TestLayerDeviceList
        cls.zone_id,cls.building_id,cls.layer_id = opera_json.get_data("LayerDeviceList").values()

    def setUp(self):
        self.api = '/scene/create'
        self.data = {
            "name": Scene.scene_name(),
            "scope_type": 0
        }

    def test01_scene_create_rsm(self):
        """case01:创建场景[RSM]--超管新增无权限"""

        res =run_method.post(self.api,json=self.data,headers=super_header)
        self.assertEqual(res.status_code,403,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

    def test02_scene_create_noRole(self):
        """case02:创建场景[普通用户]--普通用户新增无权限"""

        res =run_method.post(self.api,json=self.data,headers=common_user_header)
        self.assertEqual(res.status_code,403,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
    
    def test03_scene_create_noAuth(self):
        """case03:创建场景--无Auth"""

        res =run_method.post(self.api,json=self.data)
        self.assertEqual(res.status_code,401,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

    def test04_scene_create_noName(self):
        """case04:创建场景[RCM]--无场景名称"""
        
        self.data.update(name=None)
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test05_scene_create_zoneType_noParentId(self):
        """case05:创建场景[RCM]--园区模型范围,不存在父场景"""

        self.data.update({
            "scope_type": 1,
            "scope_id": self.zone_id,
            "parent_id": None
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["id"],"",run_method.errInfo(res))

    def test06_scene_create_zoneType_noScopeId(self):
        """case06:创建场景[RCM]--园区模型范围,不存在Scope_id"""

        self.data.update({
            "scope_type": 1,
            "scope_id": None
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test07_scene_create_zoneType_haveParentId(self):
        """case07:创建场景[RCM]--园区模型范围,选择父场景"""

        self.data.update({
            "scope_type": 1,
            "scope_id": self.zone_id,
            "parent_id": self.zone_pid
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["id"],"",run_method.errInfo(res))

    def test06_scene_create_buildType_noParentId(self):
        """case06:创建场景[RCM]--楼宇模型范围,不存在父场景"""

        self.data.update({
            "scope_type": 2,
            "scope_id": self.building_id,
            "parent_id": None
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["id"],"",run_method.errInfo(res))

    def test06_scene_create_buildType_noScopeId(self):
        """case06:创建场景[RCM]--楼宇模型范围,不存在Scope_id"""

        self.data.update({
            "scope_type": 2,
            "scope_id": None
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test07_scene_create_buildType_haveParentId(self):
        """case07:创建场景[RCM]--楼宇模型范围,选择父场景"""

        self.data.update({
            "scope_type": 2,
            "scope_id": self.building_id,
            "parent_id": self.zone_pid
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["id"],"",run_method.errInfo(res))

    def test08_scene_create_layerType_noParentId(self):
        """case08:创建场景[RCM]--楼层模型范围,不存在父场景"""

        self.data.update({
            "scope_type": 4,
            "scope_id": self.layer_id,
            "parent_id": None
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["id"],"",run_method.errInfo(res))

    def test06_scene_create_layerType_noScopeId(self):
        """case06:创建场景[RCM]--楼层模型范围,不存在Scope_id"""

        self.data.update({
            "scope_type": 4,
            "scope_id": None
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test09_scene_create_layerType_haveBuildParentId(self):
        """case09:创建场景[RCM]--楼层模型范围,选择楼宇父场景"""

        self.data.update({
            "scope_type": 4,
            "scope_id": self.layer_id,
            "parent_id": self.build_pid
        })
        res =run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["id"],"",run_method.errInfo(res))

    def test10_scene_create_thingsIds(self):
        """case10:创建场景[RCM]--新增成功，thingsAdd"""

        self.data.update({
            "scope_type": 4,
            "scope_id": self.layer_id,
            "parent_id": self.build_pid,
            "things_ids": ["1234","5678"],
            "metrics":"metrics test",
            "layout":"layout test"
        })
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        scene_dict = pub_param.get_scene(res.json()["id"],corp_header)
        self.assertNotEqual(scene_dict["things_ids"],[],run_method.errInfo(res))

class TestSceneGet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # depend by class TestLayerDeviceList
        _,building_id,layer_id = opera_json.get_data("LayerDeviceList").values()
        sql = '''select * from building_model where layer_id = '{}';'''.format(layer_id)
        result = opera_db.get_effect_row(sql)
        if result != 1: # 判断该楼层是否已上传模型，如已上传，则不需要再上传模型
            pub_param.building_model_upload(building_id=building_id,header=corp_header,layer_id=layer_id)
        sc_api = '/scene/create'
        cls.sc_data = {
            "name":Scene.scene_name(),
            "scope_type": 2,
            "scope_id": building_id,
            "metrics":"metrics get",
            "layout":"layout get"
        }
        try:
            res = run_method.post(sc_api,json=cls.sc_data,headers=corp_header)
            res.raise_for_status()
            cls.scene_id = res.json()["id"]
        except:
            print(run_method.errInfo(res))
        cls.api = '/scene/get'
    
    def test01_scene_get_noId(self):
        """case01:获取场景--无场景ID"""

        data = {
            "id":None
        }
        res = run_method.post(self.api,data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test02_scene_get_fillFalse(self):
        """case02:获取场景--查询成功,不加载模型"""

        data = {
            "id":self.scene_id,
            "fill": 0
        }
        res = run_method.post(self.api,data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertEqual(res.json()["models"],[],run_method.errInfo(res))

    def test03_scene_get_fillTrue(self):
        """case03:获取场景--查询成功,加载模型"""

        data = {
            "id":self.scene_id,
            "fill": 1
        }
        res = run_method.post(self.api,data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["models"],[],run_method.errInfo(res))

    def test04_scene_get_things_ids(self):
        """case04:获取场景--未指定设备,加载全部已标记设备"""

        data = {
            "id":self.scene_id,
            "fill": 1
        }
        res = run_method.post(self.api,data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["things_ids"],[],run_method.errInfo(res))


class TestSceneList(unittest.TestCase):

    def setUp(self):
        self.api = '/scene/list'
        self.data = {
            "page":1,
            "limit":100
        }

    def test01_scene_list_rsm(self):
        """case01:场景列表[RSM]--超管查询"""
        
        res = run_method.post(self.api,self.data,headers=super_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        self.assertNotEqual(res.json()["data_list"],[],run_method.errInfo(res))

    def test02_scene_list_noRole(self):
        """case01:场景列表[普通用户]--普通用户查询"""

        res = run_method.post(self.api,self.data,headers=common_user_header)
        self.assertEqual(res.status_code,403,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
    
    def test03_scene_list_noAuth(self):
        """case01:场景列表--无Auth"""
    
        res = run_method.post(self.api,self.data)
        self.assertEqual(res.status_code,401,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

    def test04_scene_list_success(self):
        """case04:场景列表[RCM]--查询成功"""
        
        pub_param.create_scene()    # 构建其他组织的数据
        res = run_method.post(self.api,self.data,headers=corp_header)
        self.assertEqual(res.status_code,200,run_method.errInfo(res))
        opera_assert.is_list_in(corp_id,res.json()["data_list"],"corp_id")

class TestSceneUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.scene_id = pub_param.create_scene(header=corp_header)

    
    def setUp(self):
        self.api = '/scene/update'
        self.data = {
            "id": self.scene_id,
            "name": "修改后名称",
            "parent_id": None,
            "scope_type": None,
            "scope_id": None,
            "things_ids": None,
            "metrics": None,
            "layout": None
        }
        

    def test01_scene_update_name(self):
        """case01:场景更新[RCM]--更新场景名称"""
        
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_resp["name"], self.data["name"], run_method.errInfo(res))

    def test02_scene_update_metrics(self):
        """case02:场景更新[RCM]--更新统计相关"""

        self.data.update(metrics = "metrics update")
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_resp["metrics"], self.data["metrics"], run_method.errInfo(res))

    def test03_scene_update_layout(self):
        """case03:场景更新[RCM]--更新布局相关"""

        self.data.update(layout = "layout update")
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_resp["layout"], self.data["layout"], run_method.errInfo(res))

    def test04_scene_update_parentId(self):
        """case04:场景更新[RCM]--更新父场景"""

        pid = pub_param.create_scene(header=corp_header) # 园区父场景
        self.data.update(parent_id=pid)
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_resp["parent_id"], pid, run_method.errInfo(res))

    def test05_scene_update_scopeType_noScopeId(self):
        """case05:场景更新[RCM]--更新场景范围，无ScopeId"""

        self.data.update(scope_type=1)
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        self.assertEqual(res.status_code,400,run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

    def test06_scene_update_ScopeId(self):
        """case06:场景更新[RCM]--更新场景范围，有ScopeId"""

        zone_id = pub_param.create_zone(corp_header)
        self.data.update({
            "scope_type": 1,
            "scope_id": zone_id
        })
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_resp["scope_type"], 'ZONE', run_method.errInfo(res))
        self.assertEqual(new_resp["scope_id"], zone_id, run_method.errInfo(res))

    def test07_scene_update_thingsIds(self):
        """case07:场景更新[RCM]--更新选中的设备"""

        self.data.update(things_ids=["111","222"])
        res = run_method.post(self.api,json=self.data,headers=corp_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_resp["things_ids"], self.data["things_ids"], run_method.errInfo(res))

    def test08_scene_update_rsm(self):
        """case08:场景更新[RSM]--超管更新无权限"""

        self.data.update(name = Scene.scene_name())
        res = run_method.post(self.api,json=self.data,headers=super_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
        self.assertNotEqual(new_resp["name"], self.data["name"], run_method.errInfo(res))

    def test09_scene_update_noRole(self):
        """case09:场景更新[普通用户]--普通用户更新无权限"""

        self.data.update(name = Scene.scene_name())
        res = run_method.post(self.api,json=self.data,headers=common_user_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
        self.assertNotEqual(new_resp["name"], self.data["name"], run_method.errInfo(res))
    
    def test10_scene_update_otherCorp(self):
        """case10:场景更新[RCM]--其他组织管理员更新无权限"""

        self.data.update(name = Scene.scene_name())
        res = run_method.post(self.api,json=self.data,headers=other_corp_header)
        new_resp = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))
        self.assertNotEqual(new_resp["name"], self.data["name"], run_method.errInfo(res))
    
    @unittest.skip("暂时跳过")
    def test11_scene_update_delCorpUser(self):
        """case11:场景更新--已删除管理员更新"""
        pass


class TestSceneDel(unittest.TestCase):

    def setUp(self):
        self.api = '/scene/del'
        self.scene_id = pub_param.create_scene(header=corp_header)

    def test01_scene_del_rsm(self):
        """case01:场景删除[RSM]--超管删除无权限"""

        data = {
            "id":self.scene_id
        }
        res = run_method.post(self.api,data,headers=super_header)
        new_data = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 1, run_method.errInfo(res)) # 1为启用状态

    def test02_scene_del_noRole(self):
        """case02:场景删除[普通用户]--普通用户删除无权限"""

        data = {
            "id":self.scene_id
        }
        res = run_method.post(self.api,data,headers=common_user_header)
        new_data = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 403, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 1, run_method.errInfo(res))

    def test03_scene_del_otherCorp(self):
        """case03:场景删除[RCM]--其他组织RCM删除无权限"""

        data = {
            "id":self.scene_id
        }
        res = run_method.post(self.api,data,headers=other_corp_header)
        new_data = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 1, run_method.errInfo(res))

    def test04_scene_del_success(self):
        """case04:场景删除[RCM]--RCM删除成功"""

        data = {
            "id":self.scene_id
        }
        res = run_method.post(self.api,data,headers=corp_header)
        new_data = pub_param.get_scene(self.scene_id,corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(new_data["status"], 2, run_method.errInfo(res)) # 2为已删除状态

    @unittest.skip("跳过")
    def test05_scene_del_delCorpUser(self):
        """case05:场景删除--已删除RCM删除无权限"""
        pass
