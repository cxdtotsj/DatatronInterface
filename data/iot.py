""""Iot接口的封装"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from base.base_method import BaseMethod
from data.common import Common


class IotAPI:

    def __init__(self):
        self.run_method = BaseMethod()
        self.common = Common()

    # category
    def iot_category_create(self, header, parent_id=None):
        """返回 category_id"""

        if parent_id is not None:
            pid = parent_id
        else:
            pid = ""
        api = '/iot/category/create'
        data = {
            "parent_id": pid,
            "name": self.common.random_name("Auto新增Category勿删")
        }
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("新增Category产品类别失败")
            print(self.run_method.errInfo(res))

    # product
    def iot_product_create(self, node_type, by_gateway, header):
        """返回 产品ID"""
        # node_type: 0-设备, 1-网关
        # by_gateway: 0-不接入, 1-接入

        api = '/iot/product/create'
        data = {
            "name": self.common.random_name("依赖产品名称"),
            "category_id": "000000",
            "node_type": node_type,
            "by_gateway": by_gateway,
            "description": "依赖API测试数据"
        }
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("新增Iot产品失败")
            print(self.run_method.errInfo(res))

    def iot_product_get(self, product_id, header):
        """返回 产品查询信息"""

        api = '/iot/product/get'
        data = {
            "id": product_id,
        }
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()
        except:
            print("Iot产品查询失败")
            print(self.run_method.errInfo(res))
    
    def iot_product_topic_create(self, operation, header, product_id=None):
        """返回 TOPIC ID"""

        api = '/iot/product/topic/create'
        if product_id is not None:
            pid = product_id
        else:
            pid = self.iot_product_create(1, 0, header)
        data = {
            "product_id": pid,
            "name": self.common.random_name("auto"),
            "operation": operation,
            "description": "Auto描述"
        }
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("产品TOPIC新增失败")
            print(self.run_method.errInfo(res))


    # device
    def iot_device_create(self, product_id, header):
        """返回 设备ID"""

        api = '/iot/device/create'
        node_type = self.iot_product_get(product_id, header)["prod"]["node_type"]
        data = {
            "product_id": product_id,
            "name": self.common.random_name("Auto新增设备名称"),
            "node_type": node_type
        }
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("设备新增失败")
            print(self.run_method.errInfo(res))


if __name__ == '__main__':

    iot = IotAPI()
    corp_header, _ = iot.common.header_corp()
    # super_header = iot.common.header_super()
    # p_info = iot.iot_category_create(super_header)
    pid = iot.iot_product_create(1,1,corp_header)
    pid = iot.iot_product_topic_create("PUB",corp_header, pid)
    print(pid)

