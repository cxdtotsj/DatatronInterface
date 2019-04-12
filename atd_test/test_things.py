# '''
# 设备类接口

# /things/add
# /things/get
# /things/list
# /things/update
# /things/token/get
# /things/token/regen
# /things/attrs

# '''


# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from data.api_data import ThingsApiData as Things
# from base.base_method import BaseMethod
# from data.public_param import PublicParam
# from util.operation_json import OperetionJson
# from util.operation_assert import OperationAssert
# from util.operation_db import OperationDB
# import unittest
# import time


# run_method = BaseMethod()
# pub_param = PublicParam()
# opera_json = OperetionJson()
# opera_assert = OperationAssert()
# opera_db = OperationDB()
# super_header = pub_param.get_super_header()
# corp_header, corp_id = pub_param.get_corp_user()
# common_user_header = pub_param.get_common_user()
# other_corp_header = pub_param.get_otherCorp_user()


# class TestThingsAdd(unittest.TestCase):

#     def setUp(self):
#         self.api = '/things/add'
#         self.data = {
#             "device_id": Things.device_id(),
#             "device_type":"TYPE_DEVICE"
#         }

#     def test01_things_add_noName(self):
#         """case01:设备添加[RCM]--无设备名称"""

#         self.data.update(device_id=None)
#         res = run_method.post(self.api, self.data, headers=corp_header)
#         self.assertEqual(res.status_code, 400, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

#     def test02_things_add_noToken(self):
#         """case02:设备添加[RCM]--无Auth"""

#         res = run_method.post(self.api, self.data)
#         self.assertEqual(res.status_code, 401, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"], 1401, run_method.errInfo(res))

#     def test03_things_add_rsm(self):
#         """case03:设备添加[RCM]--RSM新增"""

#         res = run_method.post(self.api, self.data, headers=super_header)
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

#     def test04_things_add_noRole(self):
#         """case04:设备添加[普通用户]--普通用户新增"""

#         res = run_method.post(self.api, self.data, headers=common_user_header)
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"], 1403, run_method.errInfo(res))

#     def test05_things_add_rcm(self):
#         """case05:设备添加[RCM]--RCM新增"""

#         res = run_method.post(self.api, self.data, headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertIsNotNone(res.json()["id"], run_method.errInfo(res))

#     def test06_things_add_default_deviceType(self):
#         """case06:设备添加[RCM]--默认的设备类型"""

#         res = run_method.post(self.api, self.data, headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         sql = '''select device_type from things 
#                     where id = "{}";'''.format(res.json()["id"])
#         device_type = opera_db.get_fetchone(sql)
#         self.assertEqual(device_type["device_type"],
#                          1, "数据库结果:{}".format(device_type))    # 1 为 TYPE_DEVICE-单体设备

#     def test07_things_add_design_deviceType(self):
#         """case07:设备添加[RCM]--指定的设备类型"""

#         self.data.update(device_type="TYPE_GATEWAY")
#         res = run_method.post(self.api, self.data, headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         sql = '''select device_type from things 
#                     where id = "{}";'''.format(res.json()["id"])
#         device_type = opera_db.get_fetchone(sql)
#         self.assertEqual(device_type["device_type"],
#                          2, "数据库结果:{}".format(device_type))    # 2 为 TYPE_GATEWAY-网关

#     def test08_things_add_design_success(self):
#         """case08:设备添加[RCM]--全字段"""

#         self.data.update({
#             "device_type": "TYPE_GATEWAY",
#             "device_alias":"设备别名",
#             "device_desc": "设备说明"
#         })
#         res = run_method.post(self.api, self.data, headers=corp_header)
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         sql = '''select device_desc from things
#                     where id = "{}";'''.format(res.json()["id"])
#         device_desc = opera_db.get_fetchone(sql)
#         self.assertEqual(
#             device_desc["device_desc"], self.data["device_desc"], "数据库结果:{}".format(device_desc))


# class TestThingsGet(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.data = {
#             "device_id":Things.device_id(),
#             "device_type":"TYPE_DEVICE",
#             "device_alias":"设备别名",
#             "device_desc":"设备描述"
#         }
#         cls.device_id = pub_param.create_device(cls.data,header=corp_header)
    
#     def setUp(self):
#         self.api = '/things/get'
#         self.data = {
#             "id":self.device_id
#         }
    
#     def test01_things_get_noId(self):
#         """case01:设备获取[RCM]--无设备ID"""
        
#         self.data.update(id=None)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

#     def test02_things_get_errId(self):
#         """case02:设备获取[RCM]--错误的设备ID"""

#         self.data.update(id="1122abcc")
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))


#     def test03_things_get_rsm(self):
#         """case03:设备获取[RSM]--超管查询受限"""

#         res = run_method.post(self.api,self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test04_things_get_noRole(self):
#         """case04:设备获取[普通用户]--普通用户查询受限"""

#         res = run_method.post(self.api,self.data,headers=common_user_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test05_things_get_otherCorp(self):
#         """case05:设备获取[其他组织管理员]--其他组织管理员查询受限"""

#         res = run_method.post(self.api,self.data,headers=other_corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))

#     def test06_things_get_noAuth(self):
#         """case06:设备获取--无Auth"""

#         res = run_method.post(self.api,self.data)
#         self.assertEqual(res.status_code,401,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

#     def test07_things_get_success(self):
#         """case07:设备获取[RCM]--RCM查询成功"""

#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         opera_assert.is_dict_in(self.data,res.json())

# class TestThingsList(unittest.TestCase):

#     def setUp(self):
#         self.api = '/things/list'
#         self.data = {
#             "page":1,
#             "limit":100,
#             "type_filter": "ALL"
#         }

#     def test01_things_list_rsm(self):
#         """case01:设备列表[RCM]--RSM查询受限"""
        
#         res = run_method.post(self.api,self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test02_things_list_noRole(self):
#         """case02:设备列表[普通用户]--普通用户查询受限"""

#         res = run_method.post(self.api,self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test03_things_list_noAuth(self):
#         """case03:设备列表--无Auth"""

#         res = run_method.post(self.api,self.data)
#         self.assertEqual(res.status_code,401,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

#     def test04_things_list_success(self):
#         """case04:设备列表[RCM]--RCM查询成功"""

#         pub_param.create_device()    # 构建其他组织的数据
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         self.assertNotEqual(res.json()["total"],'0',run_method.errInfo(res))
#         opera_assert.is_list_in(corp_id,res.json()["data_list"],"corp_id")

#     def test05_things_list_noPId(self):
#         """case05:设备列表[RCM]--无parent_id(根节点下所有设备类型的设备)"""
        
#         sql = '''select id from things where 
#             corp_id = '{}' and parent_id = '';'''.format(corp_id)
#         device_num = opera_db.get_effect_row(sql)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.json()["total"],str(device_num),run_method.errInfo(res))

#     def test06_things_list_PId(self):
#         """case06:设备列表[RCM]--有parent_id(父节点下所有设备)"""
        
#         self.data.pop("type_filter")
#         parent_id = pub_param.create_parent_device(corp_header,3)   # 3表示新增的网关下设备
#         self.data.update(parent_id=parent_id)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.json()["total"],'3',run_method.errInfo(res))


# class TestThingsUpdate(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.device_data = {
#             "device_id":Things.device_id(),
#             "device_type":"TYPE_DEVICE",
#             "device_alias":"存在设备别名",
#             "device_desc":"存在设备描述"
#         }
#         cls.device_id = pub_param.create_device(cls.device_data,corp_header)
#         cls.api = '/things/update'


#     def test01_things_update_alias(self):
#         """case01:修改设备信息[RCM]--更新设备别名(别名不为空)"""

#         data = {
#             "id":self.device_id,
#             "device_alias":"修改设备别名"
#         }
#         res = run_method.post(self.api,data,headers=corp_header)        
#         new_alias_name = pub_param.get_things(self.device_id,corp_header)["device_alias"]
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(new_alias_name, data["device_alias"], run_method.errInfo(res))

#     def test02_things_update_noAlias(self):
#         """case02:修改设备信息[RCM]--更新设备别名(别名为空)"""

#         data = {
#             "id":self.device_id,
#             "device_alias":""
#         }
#         res = run_method.post(self.api,data,headers=corp_header)        
#         new_alias_name = pub_param.get_things(self.device_id,corp_header)["device_alias"]
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertNotEqual(new_alias_name, "", run_method.errInfo(res))

#     def test03_things_update_desc(self):
#         """case03:修改设备信息[RCM]--更新设备描述(描述不为空)"""

#         data = {
#             "id":self.device_id,
#             "device_desc":"修改设备描述"
#         }
#         res = run_method.post(self.api,data,headers=corp_header)        
#         new_desc_name = pub_param.get_things(self.device_id,corp_header)["device_desc"]
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertEqual(new_desc_name, data["device_desc"], run_method.errInfo(res))

#     def test04_things_update_noDesc(self):
#         """case04:修改设备信息[RCM]--更新设备描述(描述为空)"""

#         data = {
#             "id":self.device_id,
#             "device_desc":""
#         }
#         res = run_method.post(self.api,data,headers=corp_header)        
#         new_desc_name = pub_param.get_things(self.device_id,corp_header)["device_desc"]
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertNotEqual(new_desc_name, "", run_method.errInfo(res))

#     def test05_things_update_name(self):
#         """case05:修改设备信息[RCM]--更新设备名称(受限)"""

#         data = {
#             "id":self.device_id,
#             "device_id":"更新后设备名称"
#         }
#         res = run_method.post(self.api,data,headers=corp_header)        
#         new_device_id = pub_param.get_things(self.device_id,corp_header)["device_id"]
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertNotEqual(new_device_id, data["device_id"], run_method.errInfo(res))

#     def test06_things_update_type(self):
#         """case06:修改设备信息[RCM]--更新设备类型(受限)"""

#         data = {
#             "id":self.device_id,
#             "device_type":"TYPE_GATEWAY"
#         }
#         res = run_method.post(self.api,data,headers=corp_header)        
#         new_device_type = pub_param.get_things(self.device_id,corp_header)["device_type"]
#         self.assertEqual(res.status_code, 200, run_method.errInfo(res))
#         self.assertNotEqual(new_device_type, data["device_type"], run_method.errInfo(res))

#     def test07_things_update_rsm(self):
#         """case07:修改设备信息[RSM]--超管更新(受限)"""

#         data = {
#             "id":self.device_id,
#             "device_alias":"超管修改设备别名"
#         }
#         res = run_method.post(self.api,data,headers=super_header)        
#         new_alias_name = pub_param.get_things(self.device_id,corp_header)["device_alias"]
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
#         self.assertNotEqual(new_alias_name, data["device_alias"], run_method.errInfo(res))

#     def test08_things_update_noRole(self):
#         """case08:修改设备信息[普通用户]--普通用户更新(受限)"""

#         data = {
#             "id":self.device_id,
#             "device_alias":"普通用户修改设备别名"
#         }
#         res = run_method.post(self.api,data,headers=common_user_header)        
#         new_alias_name = pub_param.get_things(self.device_id,corp_header)["device_alias"]
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
#         self.assertNotEqual(new_alias_name, data["device_alias"], run_method.errInfo(res))

#     @unittest.skip("issue=#34")
#     def test08_things_update_otherCorp(self):
#         """case08:修改设备信息[其他组织管理员]--其他组织管理员更新(受限)"""

#         data = {
#             "id":self.device_id,
#             "device_alias":"其他组织管理员修改设备别名"
#         }
#         res = run_method.post(self.api,data,headers=other_corp_header)        
#         new_alias_name = pub_param.get_things(self.device_id,corp_header)["device_alias"]
#         self.assertEqual(res.status_code, 403, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))
#         self.assertNotEqual(new_alias_name, data["device_alias"], run_method.errInfo(res))

#     def test09_things_update_noAuth(self):
#         """case09:修改设备信息--无Auth"""

#         data = {
#             "id":self.device_id,
#             "device_alias":"无Auth修改设备别名"
#         }
#         res = run_method.post(self.api,data)        
#         new_alias_name = pub_param.get_things(self.device_id,corp_header)["device_alias"]
#         self.assertEqual(res.status_code, 401, run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))
#         self.assertNotEqual(new_alias_name, data["device_alias"], run_method.errInfo(res))


# class TestThingsTokenGet(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.device_id = pub_param.create_device(header=corp_header)

#     def setUp(self):
#         self.api = '/things/token/get'
#         self.data = {
#             "id":self.device_id
#         }

#     def test01_things_token_get_noId(self):
#         """case01:设备授权token[RCM]--无设备ID"""
        
#         self.data.update(id=None)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

#     def test02_things_token_get_errId(self):
#         """case02:设备授权token[RCM]--错误的设备ID"""
        
#         self.data.update(id="err1122")
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))

#     def test03_things_token_get_rsm(self):
#         """case03:设备授权token[RCM]--rsm受限"""

#         res = run_method.post(self.api,self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test04_things_token_get_noRole(self):
#         """case04:设备授权token[普通用户]--普通用户受限"""

#         res = run_method.post(self.api,self.data,headers=common_user_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     # 根节点设备可以生成token
#     def test05_things_token_get_success(self):
#         """case05:设备授权token[RCM]--RCM第一次获取成功"""

#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         res_token = pub_param.analyze_device_token(res.json()["token"])
#         try:
#             token_id = res_token["id"]
#             token_cid = res_token["cid"]
#             token_ses = res_token["ses"]
#             token_svc = res_token["svc"]
#         except KeyError:
#             print("解析token后,返回的key不存在")
#             print(run_method.errInfo(res))
#         self.assertNotEqual(token_id,"",run_method.errInfo(res))
#         self.assertEqual(token_cid,corp_id,run_method.errInfo(res))
#         self.assertNotEqual(token_ses,"",run_method.errInfo(res))
#         self.assertEqual(token_svc,"things",run_method.errInfo(res))
#         opera_json.check_json_value("test05_things_token_get",token_ses)

#     def test06_things_token_get_second(self):
#         """case06:设备授权token[RCM]--RCM第二次获取token一致"""
        
#         time.sleep(1)
#         token_ses = opera_json.get_data("test05_things_token_get")   # 依赖用例：test05_things_token_get_success
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         res_token = pub_param.analyze_device_token(res.json()["token"])
#         ses_two = res_token["ses"]
#         self.assertEqual(ses_two,token_ses,run_method.errInfo(res))

#     def test07_things_token_get_otherCorp(self):
#         """case07:设备授权token[其他组织管理员]--其他组织管理员查询受限"""

#         res = run_method.post(self.api,self.data,headers=other_corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))

#     def test08_things_token_get_noAuth(self):
#         """case08:设备授权token--无Auth"""

#         res = run_method.post(self.api,self.data)
#         self.assertEqual(res.status_code,401,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

#     def test09_things_token_get_noRootDevice(self):
#         """case09:非根节点设备生成token[RCM]--禁止生成token"""

#         parent_id = pub_param.create_parent_device(corp_header,1)
#         device_id = pub_param.get_things_list(corp_header,parent_id)[0]
#         data = {
#             "id":device_id
#         }
#         res = run_method.post(self.api,data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))


# class TestThingsTokenRegen(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.device_id = pub_param.create_device(header=corp_header)
#         token = pub_param.get_device_token(cls.device_id,corp_header)
#         cls.ses = pub_param.analyze_device_token(token)["ses"]

#     def setUp(self):
#         self.api = '/things/token/regen'
#         self.data = {
#             "id":self.device_id
#         }

#     def test01_things_token_regen_noId(self):
#         """case01:重置设备授权token[RCM]--无设备ID"""

#         self.data.update(id=None)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))

#     def test02_things_token_regen_errId(self):
#         """case02:重置设备授权token[RCM]--错误的设备ID"""

#         self.data.update(id="err1122")
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))

#     def test03_things_token_regen_rsm(self):
#         """case03:重置设备授权token[RCM]--rsm受限"""

#         res = run_method.post(self.api,self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test04_things_token_regen_noRole(self):
#         """case04:重置设备授权token[普通用户]--普通用户受限"""

#         res = run_method.post(self.api,self.data,headers=common_user_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test05_things_token_regen_success(self):
#         """case05:重置设备授权token[RCM]--RCM重置成功(GET获取到重置后的token)"""

#         time.sleep(1)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))

#         # 再次通过token_get接口获取token，ses是否和重置后的token一致
#         time.sleep(1)
#         new_token = pub_param.get_device_token(self.device_id,corp_header)
#         res_token = pub_param.analyze_device_token(new_token)
#         try:
#             token_id = res_token["id"]
#             token_cid = res_token["cid"]
#             token_ses = res_token["ses"]
#             token_svc = res_token["svc"]
#         except KeyError:
#             print("重新生成的token,返回的key不存在")
#             print(run_method.errInfo(res))
#         self.assertNotEqual(token_id,"",run_method.errInfo(res))
#         self.assertEqual(token_cid,corp_id,run_method.errInfo(res))
#         self.assertNotEqual(token_ses,"",run_method.errInfo(res))
#         self.assertEqual(token_svc,"things",run_method.errInfo(res))
#         self.assertNotEqual(token_ses,self.ses,run_method.errInfo(res))

#     def test06_things_token_regen_noAuth(self):
#         """case06:重置设备授权token--无Auth"""

#         res = run_method.post(self.api,self.data)
#         self.assertEqual(res.status_code,401,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))

#     def test07_things_token_regen_otherCorp(self):
#         """case07:重置设备授权token[其他组织管理员]--其他组织管理员查询受限"""

#         res = run_method.post(self.api,self.data,headers=other_corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))


# class TestThingsAttrs(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         cls.device_id = pub_param.create_device(header=corp_header)
#         # 新增设备属性
#         attars_names = ["attrs_test01","attrs_test02","attrs_test03","attrs_test01"]
#         pub_param.insert_thingsData(corp_id,cls.device_id,attars_names)

#     def setUp(self):
#         self.api = '/things/attrs'
#         self.data = {
#             "id":self.device_id
#         }

#     def test00_things_attrs_success(self):
#         """case00:获取设备属性[RCM]--查询已注册设备"""

#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         self.assertEqual(len(res.json()["attrs"]),3,run_method.errInfo(res))

#     def test01_things_attrs_noId(self):
#         """case01:获取设备属性[RCM]--无设备ID"""
        
#         self.data.update(id=None)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1400,run_method.errInfo(res))
    
#     def test02_things_attrs_errId(self):
#         """case02:获取设备属性[RCM]--错误的设备ID"""

#         self.data.update(id="abc123")
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,400,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1404,run_method.errInfo(res))

#     def test03_things_attrs_rsm(self):
#         """case03:获取设备属性[RCM]--rsm受限"""

#         res = run_method.post(self.api,self.data,headers=super_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test04_things_attrs_noRole(self):
#         """case04:获取设备属性[普通用户]--普通用户受限"""

#         res = run_method.post(self.api,self.data,headers=common_user_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test05_things_attrs_noRegister(self):
#         """case05:获取设备属性[RCM]--未注册设备"""

#         device_id = pub_param.create_device(header=corp_header)
#         self.data.update(id=device_id)
#         res = run_method.post(self.api,self.data,headers=corp_header)
#         self.assertEqual(res.status_code,200,run_method.errInfo(res))
#         self.assertEqual(res.json()["attrs"],[],run_method.errInfo(res))

#     @unittest.skip("issue=#36")
#     def test06_things_attrs_otherCorp(self):
#         """case06:获取设备属性[其他组织管理员]--其他组织管理员查询受限"""

#         res = run_method.post(self.api,self.data,headers=other_corp_header)
#         self.assertEqual(res.status_code,403,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1403,run_method.errInfo(res))

#     def test07_things_token_get_noAuth(self):
#         """case07:获取设备属性--无Auth"""

#         res = run_method.post(self.api,self.data)
#         self.assertEqual(res.status_code,401,run_method.errInfo(res))
#         self.assertEqual(res.json()["code"],1401,run_method.errInfo(res))