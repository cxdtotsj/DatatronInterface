'''
Iot 产品类接口

/iot/product/create
/iot/product/get
/iot/product/list
/iot/product/secretreset
/iot/product/delete
/iot/product/topic/list

'''

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from base.base_method import BaseMethod
from util.operation_db import OperationDB
from data.common import Common
from data.iot import IotAPI



run_method = BaseMethod()
opera_db = OperationDB()
common = Common()
corp_header, corp_id = common.header_corp()
other_corp_header = common.header_otherCorp()

iot = IotAPI()


class TestIotProductCreate(unittest.TestCase):

    def setUp(self):
        # node_type: 节点类型(0:设备/1:网关),默认为0
        # by_gateway: 是否接入网关(0:不接/1:接入),默认为0
        self.api = '/iot/product/create'
        self.data = {
            "name": common.random_name("Auto_创建产品"),
            "category_id": "100",
            "node_type": None,
            "by_gateway": None,
            "description": None
        }

    def test01_iot_product_create_noName(self):
        """case01:创建产品--无产品名称"""

        self.data.update(name=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_iot_product_create_noCategoryId(self):
        """case02:创建产品--无所属分类"""

        self.data.update(category_id=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))
    
    def test03_iot_product_create_default_nodeType(self):
        """case03:创建产品--默认节点类型(设备)"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["node_type"], 0, run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))
        
    def test04_iot_product_create_device_nodeType(self):
        """case04:创建产品--设备节点类型"""

        self.data.update(node_type=0)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["node_type"], 0, run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))

    def test05_iot_product_create_gateway_nodeType(self):
        """case05:创建产品--网关节点类型"""

        self.data.update(node_type=1)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["node_type"], 1, run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))

    def test06_iot_product_create_gateway_default_byGateway(self):
        """case06:创建产品--网关默认是否接入网关(0--不接入)"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["by_gateway"], 0, run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))

    def test07_iot_product_create_device_default_byGateway(self):
        """case07:创建产品--设备默认是否接入网关(0--不接入)"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["by_gateway"], 0, run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))

    def test08_iot_product_create_device_0_byGateway(self):
        """case08:创建产品--设备不接入网关"""

        self.data.update(by_gateway=0)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["by_gateway"], 0, run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))

    def test09_iot_product_create_device_1_byGateway(self):
        """case09:创建产品---设备接入网关"""

        self.data.update(by_gateway=1)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["by_gateway"], 1, run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))

    def test10_iot_product_create_success(self):
        """case10:创建产品---新增成功(无描述)"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["description"], "", run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))

    def test11_iot_product_create_description(self):
        """case11:创建产品---新增成功(有描述)"""

        self.data.update(description="测试描述")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(res.json()["id"])
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["description"], "测试描述", run_method.errInfo(res))
        self.assertEqual(sql_data["status"], 1, run_method.errInfo(res))


class TestIotProductGet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 新增网关
        cls.gw_id = iot.iot_product_create(1, 0, corp_header)
        # 新增网关下设备（还缺少绑定动作，接口待补充）
        cls.gw_device_id = iot.iot_product_create(0, 1,corp_header)
        # 新增独立设备
        cls.sign_device_id = iot.iot_product_create(0, 0, corp_header)

    def setUp(self):
        self.api = '/iot/product/get'
        self.data = {
            "id": None
        }
    
    def test01_iot_product_get_gateway(self):
        """case01:查询产品---查询网关"""

        self.data.update(id=self.gw_id)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        j_data = res.json()
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(self.gw_id)
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["name"], j_data["prod"]["name"], run_method.errInfo(res))
        self.assertEqual(sql_data["node_type"], j_data["prod"]["node_type"], run_method.errInfo(res))
        self.assertEqual(sql_data["by_gateway"], j_data["prod"]["by_gateway"], run_method.errInfo(res))
        self.assertEqual(sql_data["category_id"], j_data["prod"]["category_id"], run_method.errInfo(res))
        self.assertEqual(sql_data["secret"], j_data["prod"]["secret"], run_method.errInfo(res))
        self.assertEqual(sql_data["description"], j_data["prod"]["description"], run_method.errInfo(res))
        self.assertEqual(sql_data["status"], j_data["prod"]["status"], run_method.errInfo(res))
        # device_num 的校验
        # self.assertEqual(j_data["device_num"], 1, run_method.errInfo(res))

    def test02_iot_product_get_gwDevice(self):
        """case02:查询产品---查询网关下设备"""

        self.data.update(id=self.gw_device_id)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        j_data = res.json()
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(self.gw_device_id)
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["name"], j_data["prod"]["name"], run_method.errInfo(res))
        self.assertEqual(sql_data["node_type"], j_data["prod"]["node_type"], run_method.errInfo(res))
        self.assertEqual(sql_data["by_gateway"], j_data["prod"]["by_gateway"], run_method.errInfo(res))
        self.assertEqual(sql_data["category_id"], j_data["prod"]["category_id"], run_method.errInfo(res))
        self.assertEqual(sql_data["secret"], j_data["prod"]["secret"], run_method.errInfo(res))
        self.assertEqual(sql_data["description"], j_data["prod"]["description"], run_method.errInfo(res))
        self.assertEqual(sql_data["status"], j_data["prod"]["status"], run_method.errInfo(res))

    def test03_iot_product_get_signDevice(self):
        """case03:查询产品---查询独立设备"""

        self.data.update(id=self.sign_device_id)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        j_data = res.json()
        sql = '''SELECT * FROM iot_product 
                    where id = '{}';'''.format(self.sign_device_id)
        sql_data = opera_db.get_fetchone(sql)
        self.assertEqual(sql_data["name"], j_data["prod"]["name"], run_method.errInfo(res))
        self.assertEqual(sql_data["node_type"], j_data["prod"]["node_type"], run_method.errInfo(res))
        self.assertEqual(sql_data["by_gateway"], j_data["prod"]["by_gateway"], run_method.errInfo(res))
        self.assertEqual(sql_data["category_id"], j_data["prod"]["category_id"], run_method.errInfo(res))
        self.assertEqual(sql_data["secret"], j_data["prod"]["secret"], run_method.errInfo(res))
        self.assertEqual(sql_data["description"], j_data["prod"]["description"], run_method.errInfo(res))
        self.assertEqual(sql_data["status"], j_data["prod"]["status"], run_method.errInfo(res))
    

class TestIotProductList(unittest.TestCase):

    def test01_iot_product_list_success(self):
        """case01:查询产品列表---查询成功"""

        api = '/iot/product/list'
        data = {
            "limit": 50,
            "page": 1
        }
        res = run_method.post(api, data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''select * from iot_product where status = 1 and corp_id = '{}';'''.format(corp_id)
        sql_num = opera_db.get_effect_row(sql)
        self.assertEqual(res.json()["total"], str(sql_num), run_method.errInfo(res))


class TestIotProductSecretreset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product_id = iot.iot_product_create(1, 0, corp_header)
        cls.sercret = iot.iot_product_get(cls.product_id, corp_header)
    
    def setUp(self):
        self.api = '/iot/product/secretreset'
        self.data = {
            "id": self.product_id
        }
    
    def test01_iot_product_secretreset(self):
        """case01:产品密钥重置---重置成功"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        s_reset = iot.iot_product_get(self.product_id, corp_header)
        self.assertNotEqual(s_reset, self.sercret, run_method.errInfo(res))


class TestIotProductUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product_id = iot.iot_product_create(1, 0, corp_header)

    def setUp(self):
        self.api = '/iot/product/update'
        self.data = {
            "id": self.product_id,
            "name": None,
            "description": None
        }

    def test01_iot_product_update_noId(self):
        """case01:产品更新---无产品ID"""
 
        self.data.update(id=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_iot_product_update_noName(self):
        """case02:产品更新---无产品名称"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_iot_product_update_repeatName(self):
        """case03:产品更新---重复的产品名称"""

        # 新增一个产品，并获取name
        pid = iot.iot_product_create(1, 0, corp_header)
        o_name = iot.iot_product_get(pid, corp_header)["prod"]["name"]
        self.data.update(name=o_name)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))

    def test04_iot_product_update_diffCorp_repeatName(self):
        """case04:产品更新---不同Corp的重复产品名称"""

        # 不同corp，新增产品，并获取产品名称
        pid = iot.iot_product_create(1, 0, other_corp_header)
        o_name = iot.iot_product_get(pid, corp_header)["prod"]["name"]
        self.data.update(name=o_name)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 获取更新后的 name
        r_name = iot.iot_product_get(self.product_id, corp_header)["prod"]["name"]
        self.assertEqual(r_name, o_name, run_method.errInfo(res))

    def test05_iot_product_update_description(self):
        """case05:产品更新---描述"""

        name = common.random_name("更新描述")
        self.data.update({
            "name": name,
            "description": "更新后的描述"
        })
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 获取更新后的描述
        r_desc = iot.iot_product_get(self.product_id, corp_header)["prod"]["description"]
        self.assertEqual(r_desc, "更新后的描述", run_method.errInfo(res))


class TestIotProductDelete(unittest.TestCase):

    def setUp(self):
        self.product_id = iot.iot_product_create(1, 0, corp_header)
        self.api = '/iot/product/delete'
        self.data = {
            "id": self.product_id
        }

    def test01_iot_product_delete_noDevice(self):
        """case01:产品删除---产品下无设备(删除成功)"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''select status from iot_product where id = '{}';'''.format(self.product_id)
        r_status = opera_db.get_fetchone(sql)["status"]
        self.assertEqual(r_status, 0, run_method.errInfo(res))

    def test02_iot_product_delete_haveDevice(self):
        """case02:产品删除---产品下存在设备(不允许删除)"""

        iot.iot_device_create(self.product_id, corp_header)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1000, run_method.errInfo(res))
        sql = '''select status from iot_product where id = '{}';'''.format(self.product_id)
        r_status = opera_db.get_fetchone(sql)["status"]
        self.assertEqual(r_status, 1, run_method.errInfo(res))


class TestIotProductTopicCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product_id = iot.iot_product_create(1, 0, corp_header)

    def setUp(self):
        self.api = '/iot/product/topic/create'
        self.data = {
            "product_id": self.product_id,
            "name": common.random_name("testcase"),
            "operation": None,
            "description": None
        }

    def test01_iot_product_topic_create_noProductId(self):
        """case01:创建产品Topic---无产品ID"""

        self.data.update(product_id=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_iot_product_topic_create_noName(self):
        """case02:创建产品Topic---无Topic名称"""

        self.data.update(name=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_iot_product_topic_create_noOperation(self):
        """case03:创建产品Topic---无操作权限"""

        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test04_iot_product_topic_create_pub_operation(self):
        """case04:创建产品Topic---发布操作权限(PUB--发布)"""

        self.data.update(operation="PUB")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(res.json()["id"])
        op = opera_db.get_fetchone(sql)["operation"]
        self.assertEqual(op, "PUB", run_method.errInfo(res))

    def test05_iot_product_topic_create_sub_operation(self):
        """case05:创建产品Topic---订阅操作权限(SUB--订阅)"""

        self.data.update(operation="SUB")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(res.json()["id"])
        op = opera_db.get_fetchone(sql)["operation"]
        self.assertEqual(op, "SUB", run_method.errInfo(res))

    def test06_iot_product_topic_create_all_operation(self):
        """case06:创建产品Topic---订阅和发布操作权限(ALL--订阅和发布)"""

        self.data.update(operation="ALL")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(res.json()["id"])
        op = opera_db.get_fetchone(sql)["operation"]
        self.assertEqual(op, "ALL", run_method.errInfo(res))

    def test07_iot_product_topic_create_description(self):
        """case07:创建产品Topic---存在描述"""

        self.data.update({
            "operation": "ALL",
            "description": "描述信息"
        })
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(res.json()["id"])
        desc = opera_db.get_fetchone(sql)["description"]
        self.assertEqual(desc, "描述信息", run_method.errInfo(res))


class TestIotProductTopicUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.topic_id = iot.iot_product_topic_create("ALL", corp_header)

    def setUp(self):
        self.api = '/iot/product/topic/update'
        self.data = {
            "id": self.topic_id,
            "name": common.random_name("update"),
            "operation": None,
            "description": None
        }

    def test01_iot_product_topic_update_noId(self):
        """case01:修改产品Topic---无Topic ID"""

        self.data.update(id=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test02_iot_product_topic_update_noName(self):
        """case02:修改产品Topic---无Topic名称"""

        self.data.update(name=None)
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 400, run_method.errInfo(res))
        self.assertEqual(res.json()["code"], 1400, run_method.errInfo(res))

    def test03_iot_product_topic_update_sub(self):
        """case03:修改产品Topic---订阅操作权限(SUB--订阅)"""

        self.data.update(operation="SUB")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(self.topic_id)
        op = opera_db.get_fetchone(sql)["operation"]
        self.assertEqual(op, "SUB", run_method.errInfo(res))

    def test04_iot_product_topic_update_pub(self):
        """case04:修改产品Topic---发布操作权限(PUB--发布)"""

        self.data.update(operation="PUB")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(self.topic_id)
        op = opera_db.get_fetchone(sql)["operation"]
        self.assertEqual(op, "PUB", run_method.errInfo(res))

    def test05_iot_product_topic_update_all(self):
        """case05:修改产品Topic---订阅和发布操作权限(ALL--订阅和发布)"""

        self.data.update(operation="ALL")
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(self.topic_id)
        op = opera_db.get_fetchone(sql)["operation"]
        self.assertEqual(op, "ALL", run_method.errInfo(res))

    def test06_iot_product_topic_update_description(self):
        """case06:修改产品Topic---描述"""

        self.data.update({
            "operation": "ALL",
            "description": "更新后描述"
        })
        res = run_method.post(self.api, self.data, headers=corp_header)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        sql = '''SELECT * FROM iot_product_topic where id = '{}';'''.format(self.topic_id)
        desc = opera_db.get_fetchone(sql)["description"]
        self.assertEqual(desc, "更新后描述", run_method.errInfo(res))


class TestIotProductTopicList(unittest.TestCase):

    def test01_iot_product_topic_list_noId(self):
        """case01:产品Topic列表---无产品ID"""
    

    def test02_iot_product_topic_list_noCustTopic(self):
        """case02:产品Topic列表---产品无自定义topic(显示系统默认的Topic)"""


    def test03_iot_product_topic_list_custTopic(self):
        """case03:产品Topic列表---产品存在自定义topic(包括系统默认的Topic)"""


    def test04_iot_product_topic_list_topicRule(self):
        """case04:产品Topic列表---查看自定义topic显示规则"""


class TestIotProductTopicDelete(unittest.TestCase):

    def test01_iot_product_topic_delete_noId(self):
        """case01:删除产品Topic---无Topic ID"""


    def test02_iot_product_topic_delete_success(self):
        """case02:删除产品Topic---删除成功"""
    

class TestIotDeviceCreate(unittest.TestCase):

    def test01_iot_device_create_noProductId(self):
        """case01:新增设备---无产品ID"""
    

    def test02_iot_device_create_noName(self):
        """case02:新增设备---无设备名称"""


    def test03_iot_device_create_gw(self):
        """case03:新增设备---新增网关"""


    def test04_iot_device_create_thing(self):
        """case04:新增设备---新增设备"""


    def test05_iot_device_create_repeatName(self):
        """case05:新增设备---同一产品下,设备名称重复"""


    def test06_iot_device_create_diffPrd_repeatName(self):
        """case06:新增设备---不同产品下,设备名称重复"""


class TestIotDeviceGet(unittest.TestCase):

    def test01_iot_device_get_gateway(self):
        """case01:查询设备---查询网关设备"""


    def test02_iot_device_get_gwDevice(self):
        """case02:查询设备---查询网关下子设备"""


    def test03_iot_device_get_signDevice(self):
        """case03:查询设备---查询独立设备"""


    def test04_iot_device_get_disable(self):
        """case04:查询设备---查询已禁用设备"""


class TestIotDeviceList(unittest.TestCase):

    def test01_iot_device_list_childDevice(self):
        """case01:查询设备列表---查询成功(存在子设备)"""


    def test02_iot_device_list_disable(self):
        """case02:查询设备列表---查询成功(存在禁用设备)"""


class TestIotDeviceDelete(unittest.TestCase):

    def test01_iot_device_delete_gateway(self):
        """case01:设备删除---网关(不存在子设备,允许删除)"""


    def test02_iot_device_delete_haveChildDevice(self):
        """case02:设备删除---网关下存在子设备(不允许删除)"""


    def test03_iot_device_delete_signDevice(self):
        """case03:设备删除---删除独立设备"""


    def test04_iot_device_delete_childDevice(self):
        """case04:设备删除---删除子设备"""


class TestIotDeviceChildCreate(unittest.TestCase):

    def test01_iot_device_child_create_noGwId(self):
        """case01:新增子设备---无网关ID"""


    def test02_iot_device_child_create_noProductId(self):
        """case02:新增子设备---无产品ID"""


    def test03_iot_device_child_create_noDeviceId(self):
        """case03:新增子设备---无设备ID"""


    def test04_iot_device_child_create_success(self):
        """case04:新增子设备---新增成功"""


    def test05_iot_device_child_create_otherGW(self):
        """case05:新增子设备---子设备再其他网关设备下再次绑定(不允许)"""


class TestIotDeviceChildList(unittest.TestCase):

    def test01_iot_device_child_list_noGwId(self):
        """case01:子设备列表---无网关ID"""


    def test02_iot_device_child_list_success(self):
        """case02:子设备列表---查询成功(存在删除过的子设备,应不在列表)"""


class TestIotDeviceChildDelete(unittest.TestCase):

    def test01_iot_device_child_delete_noId(self):
        """case01:子设备列表---无子设备ID"""


    def test02_iot_device_child_delete_signDevice(self):
        """case02:子设备列表---独立设备ID"""


    def test03_iot_device_child_delete_gateway(self):
        """case03:子设备列表---网关设备ID"""


    def test04_iot_device_child_delete_success(self):
        """case04:子设备列表---删除成功(移除parent_id, status应不变)"""


class TestIotDeviceTopicList(unittest.TestCase):

    def test01_iot_device_topic_list_noProductId(self):
        """case01:设备Topic列表---无产品ID"""


    def test02_iot_device_topic_list_noDeviceId(self):
        """case02:设备Topic列表---无设备ID"""


    def test03_iot_device_topic_list_topicRule(self):
        """case03:设备Topic列表---设备topic"""
    

class TestIotGroupCreate(unittest.TestCase):

    def test01_iot_group_create_noName(self):
        """case01:新增分组---无组名称"""
    

    def test02_iot_group_create_level1(self):
        """case02:新增分组---新增第一级(parent_id为0)"""


    def test03_iot_group_create_level2(self):
        """case03:新增分组---新增第二级"""


    def test04_iot_group_create_level3(self):
        """case03:新增分组---新增第三级"""


class TestIotGroupList(unittest.TestCase):

    def test01_iot_group_list_noId(self):
        """case01:分组列表---无父组ID"""


    def test02_iot_group_list_level1(self):
        """case02:分组列表---第一级父组ID"""


    def test03_iot_group_list_level2(self):
        """case03:分组列表---第二级父组ID"""


class TestIotGroupDelete(unittest.TestCase):

    def test01_iot_group_delete_noId(self):
        """case01:分组删除---无组ID"""


    def test02_iot_group_delete_level1(self):
        """case02:分组删除---删除第一级分组(无子分组)"""


    def test03_iot_group_delete_level2(self):
        """case03:分组删除---删除第二级分组(无子分组)"""


    def test04_iot_group_delete_parent(self):
        """case04:分组删除---删除父分组(存在子分组)"""


    def test05_iot_group_delete_device(self):
        """case05:分组删除---删除分组(存在设备)"""


class TestIotGroupDeviceAdd(unittest.TestCase):
    
    def test01_iot_group_device_add_noGroupId(self):
        """case01:添加设备到组---无组ID"""


    def test02_iot_group_device_add_noDeviceId(self):
        """case02:添加设备到组---无设备ID"""


    def test03_iot_group_device_add_group1(self):
        """case03:添加设备到组---设备添加到组1"""


    def test04_iot_group_device_add_group2(self):
        """case04:添加设备到组---同一设备添加到组2"""


    def test05_iot_group_device_add_again(self):
        """case05:添加设备到组---移除后再次添加该设备"""


class TestIotGroupDeviceList(unittest.TestCase):

    def test01_iot_group_device_list_noId(self):
        """case01:查询组设备列表---无组ID"""


    def test01_iot_group_device_list_success(self):
        """case01:查询组设备列表---查询成功"""


class TestIotGroupDeviceDel(unittest.TestCase):
    
    def test01_iot_group_device_del_noGroupId(self):
        """case01:移除组设备---无组ID"""


    def test02_iot_group_device_del_noDeviceId(self):
        """case02:移除组设备---无设备ID"""


    def test04_iot_group_device_del_success(self):
        """case04:移除组设备---移除成功"""