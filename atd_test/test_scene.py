# '''
# 场景类接口

# /scene/create
# /scene/get
# /scene/list
# /scene/update
# /scene/del

# '''

# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from base.base_method import BaseMethod
# from data.public_param import PublicParam
# from util.operation_assert import OperationAssert
# from util.operation_db import OperationDB
# from data.api_data import SceneApiData as Scene
# import unittest

# run_method = BaseMethod()
# pub_param = PublicParam()
# opera_assert = OperationAssert()
# opera_db = OperationDB()
# super_header = pub_param.get_super_header()
# corp_header, corp_id = pub_param.get_corp_user()
# # 普通用户
# common_user_header = pub_param.common_user(corp_id)
# # 其他组织RCM
# other_corp_header = pub_param.common_user(role=524288)


# class TestSceneCreate(unittest.TestCase):

#     def setUp(self):
#         self.api = '/scene/create'
#         self.data = {
#             "name": Scene.scene_name()
#         }
    
#     def test01_scene_create_noName(self):
#         """case01:创建场景[RCM]--无场景名称"""
        
#         self.data.update(name=None)
#         res =run_method.post(self.api,json=self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))
    
#     def test02_scene_create_errCorpId(self):
#         """case02:创建场景[RCM]--错误的corp_id"""

#         self.data.update(corp_id="112200abc")
#         res =run_method.post(self.api,json=self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         scene_dict = pub_param.get_scene(res.json()["id"])
#         self.assertEqual(scene_dict["corp_id"],corp_id,"默认corp_id不正确")

#     def test03_scene_create_rsm(self):
#         """case03:创建场景[RSM]--超管新增无权限"""

#         res =run_method.post(self.api,json=self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test04_scene_create_noRole(self):
#         """case04:创建场景[普通用户]--普通用户新增无权限"""

#         res =run_method.post(self.api,json=self.data,headers=common_user_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
    
#     def test05_scene_create_noAuth(self):
#         """case04:创建场景--无Auth"""

#         res =run_method.post(self.api,json=self.data)
#         self.assertEqual(res.status_code,401,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

#     def test06_scene_create_success(self):
#         """case06:创建场景[RCM]--新增成功"""

#         self.data.update(
#             {
#                 "models":"models test",
#                 "metrics":"metrics test",
#                 "layout":"layout test"
#             }
#         )
#         res = run_method.post(self.api,json=self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         scene_dict = pub_param.get_scene(res.json()["id"])
#         opera_assert.is_dict_in(self.data,scene_dict)
        

# class TestSceneGet(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         sc_api = '/scene/create'
#         cls.sc_data = {
#             "name":Scene.scene_name(),
#             "models":"model get",
#             "metrics":"metrics get",
#             "layout":"layout get"
#         }
#         try:
#             res = run_method.post(sc_api,json=cls.sc_data,headers=corp_header)
#             res.raise_for_status()
#             cls.scene_id = res.json()["id"]
#         except:
#             print(run_method.errInfo(res))
#         cls.api = '/scene/get'
    
#     def test01_scene_get_noId(self):
#         """case01:获取场景--无场景ID"""

#         data = {
#             "id":None
#         }
#         res = run_method.post(self.api,data)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))
        
#     def test02_scene_get_errId(self):
#         """case02:获取场景--错误的建筑ID"""
    
#         data = {
#             "id":"1122abcc"
#         }
#         res = run_method.post(self.api,data)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1000,run_method.errInfo(res))

#     def test03_scene_get_success(self):
#         """case03:获取场景--查询成功"""

#         data = {
#             "id":self.scene_id
#         }
#         res = run_method.post(self.api,data)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         opera_assert.is_dict_in(self.sc_data,res.json())

# class TestSceneList(unittest.TestCase):

#     def setUp(self):
#         self.api = '/scene/list'
#         self.data = {
#             "page":1,
#             "limit":100
#         }

#     def test01_scene_list_rsm(self):
#         """case01:场景列表[RSM]--超管查询"""
        
#         res = run_method.post(self.api,self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test02_scene_list_noRole(self):
#         """case01:场景列表[普通用户]--普通用户查询"""

#         res = run_method.post(self.api,self.data,headers=common_user_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
    
#     def test03_scene_list_noAuth(self):
#         """case01:场景列表--无Auth"""
    
#         res = run_method.post(self.api,self.data)
#         self.assertEqual(res.status_code,401,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

#     def test04_scene_list_success(self):
#         """case04:场景列表[RCM]--查询成功"""
        
#         pub_param.create_scene()    # 构建其他组织的数据
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         opera_assert.is_list_in(corp_id,res.json()["data_list"],"corp_id")

# class TestSceneUpdate(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.scene_id = pub_param.create_scene(header=corp_header)
#         cls.api = '/scene/update'

#     def test01_scene_update_name(self):
#         """case01:场景更新[RCM]--更新场景名称"""
        
#         data = pub_param.get_scene(self.scene_id)
#         data.update(name = Scene.scene_name())
#         res = run_method.post(self.api,json=data,headers=corp_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(new_data["name"], data["name"], run_method.errInfo(res))
    
#     def test02_scene_update_models(self):
#         """case02:场景更新[RCM]--更新模型相关"""

#         data = pub_param.get_scene(self.scene_id)
#         data.update(models = "models update")
#         res = run_method.post(self.api,json=data,headers=corp_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(new_data["models"], "models update", run_method.errInfo(res))

#     def test03_scene_update_metrics(self):
#         """case03:场景更新[RCM]--更新统计相关"""

#         data = pub_param.get_scene(self.scene_id)
#         data.update(metrics = "metrics update")
#         res = run_method.post(self.api,json=data,headers=corp_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(new_data["metrics"], "metrics update", run_method.errInfo(res))

#     def test04_scene_update_layout(self):
#         """case04:场景更新[RCM]--更新布局相关"""

#         data = pub_param.get_scene(self.scene_id)
#         data.update(layout = "layout update")
#         res = run_method.post(self.api,json=data,headers=corp_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(new_data["layout"], "layout update", run_method.errInfo(res))

#     def test05_scene_update_rsm(self):
#         """case05:场景更新[RSM]--超管更新无权限"""

#         data = pub_param.get_scene(self.scene_id)
#         data.update(name = Scene.scene_name())
#         res = run_method.post(self.api,json=data,headers=super_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
#         self.assertNotEqual(new_data["name"], data["name"], run_method.errInfo(res))

#     def test06_scene_update_noRole(self):
#         """case02:场景更新[普通用户]--普通用户更新无权限"""

#         data = pub_param.get_scene(self.scene_id)
#         data.update(name = Scene.scene_name())
#         res = run_method.post(self.api,json=data,headers=common_user_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
#         self.assertNotEqual(new_data["name"], data["name"], run_method.errInfo(res))
    
#     def test07_scene_update_otherCorp(self):
#         """case07:场景更新[RCM]--其他组织管理员更新无权限"""

#         data = pub_param.get_scene(self.scene_id)
#         data.update(name = Scene.scene_name())
#         res = run_method.post(self.api,json=data,headers=other_corp_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 400, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))
#         self.assertNotEqual(new_data["name"], data["name"], run_method.errInfo(res))
    
#     @unittest.skip("暂时跳过")
#     def test08_scene_update_delCorpUser(self):
#         """case08:场景更新--已删除管理员更新"""
#         pass


# class TestSceneDel(unittest.TestCase):

#     def setUp(self):
#         self.api = '/scene/del'
#         self.scene_id = pub_param.create_scene(header=corp_header)

#     def test01_scene_del_rsm(self):
#         """case01:场景删除[RSM]--超管删除无权限"""

#         data = {
#             "id":self.scene_id
#         }
#         res = run_method.post(self.api,data,headers=super_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
#         self.assertEqual(new_data["status"], 1, run_method.errInfo(res)) # 1为启用状态

#     def test02_scene_del_noRole(self):
#         """case02:场景删除[普通用户]--普通用户删除无权限"""

#         data = {
#             "id":self.scene_id
#         }
#         res = run_method.post(self.api,data,headers=common_user_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))
#         self.assertEqual(new_data["status"], 1, run_method.errInfo(res))

#     def test03_scene_del_otherCorp(self):
#         """case03:场景删除[RCM]--其他组织RCM删除无权限"""

#         data = {
#             "id":self.scene_id
#         }
#         res = run_method.post(self.api,data,headers=other_corp_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 400, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"], 1404, run_method.errInfo(res))
#         self.assertEqual(new_data["status"], 1, run_method.errInfo(res))

#     def test04_scene_del_success(self):
#         """case04:场景删除[RCM]--RCM删除成功"""

#         data = {
#             "id":self.scene_id
#         }
#         res = run_method.post(self.api,data,headers=corp_header)
#         new_data = pub_param.get_scene(self.scene_id)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(new_data["status"], 2, run_method.errInfo(res)) # 2为已删除状态

#     @unittest.skip("跳过")
#     def test05_scene_del_delCorpUser(self):
#         """case05:场景删除--已删除RCM删除无权限"""
#         pass

# class TestSceneModelurllist(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         building_id = pub_param.create_sign_building(header=corp_header)
#         cls.models = []
#         for _ in range(3):
#             model_res,__ = pub_param.building_model_upload(building_id,corp_header)
#             cls.models.append(model_res["model_id"])

#     def setUp(self):
#         self.api = '/scene/modelurllist'
#         self.data = {
#             "models":None
#         }

#     def test01_scene_modelurllist_noId(self):
#         """case01:场景模型url列表--无模型ID"""

#         res = run_method.post(self.api,json=self.data,headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(res.json()["midURL"],{},run_method.errInfo(res))
    
#     def test02_scene_modelurllist_oneId(self):
#         """case02:场景模型url列表--一个模型ID"""
        
#         mid = self.models[:1]   # 取第一个model_id
#         self.data.update(models=mid)
#         res = run_method.post(self.api,json=self.data,headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(len(res.json()["midURL"]),1,run_method.errInfo(res))
#         self.assertIsNotNone(res.json()["midURL"][mid[0]],run_method.errInfo(res))

#     def test03_scene_modelurllist_multId(self):
#         """case03:场景模型url列表--多个模型ID"""

#         self.data.update(models=self.models)
#         res = run_method.post(self.api,json=self.data,headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(len(res.json()["midURL"]),3,run_method.errInfo(res))
#         self.assertEqual(len(res.json()["midURL"].values()),3,run_method.errInfo(res))

#     def test04_scene_modelurllist_disableId(self):
#         """case04:场景模型url列表--存在停用的建筑"""

#         building_id = pub_param.create_sign_building(header=corp_header)
#         models = []
#         model_res,__ = pub_param.building_model_upload(building_id,corp_header)
#         models.append(model_res["model_id"])        # 停用建筑的models
#         model_list = self.models + models           # 合并启用建筑和停用建筑
#         sql = '''update building set status = 2 where id = '{}';'''.format(building_id) 
#         opera_db.update_data(sql)   # 停用建筑
#         self.data.update(models=model_list)
#         res = run_method.post(self.api,json=self.data,headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(len(res.json()["midURL"]),3,run_method.errInfo(res))
#         self.assertEqual(len(res.json()["midURL"].values()),3,run_method.errInfo(res))

