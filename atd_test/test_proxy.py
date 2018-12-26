'''
Proxy:

/proxy/create
/proxy/list
/proxy/query
/proxy/querybatch

'''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.operation_json import OperetionJson
from util.operation_db import OperationDB
from base.base_method import BaseMethod
import unittest
import requests


run_method = BaseMethod()
opera_json = OperetionJson()
opera_db = OperationDB()

class TestProxyCreate(unittest.TestCase):

    def test01_proxy_create_success(self):
        """case01:创建方法--创建GET方法"""
        
        api = '/proxy/create'
        data = {
            "URL":"https://www.baidu.com",
            "content_type": 0,
            "method": 0,
            "name": "auto_test"
        }
        res = run_method.post(api,json=data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        # 存入ID，后面做数据清除
        opera_json.check_json_value("test01_proxy_create",res.json()["id"])


class TestProxyList(unittest.TestCase):

    def test01_proxy_list_success(self):
        """case01:方法列表--获取方法列表"""

        api = '/proxy/list'
        res = run_method.post(api)
        sql = '''select id from proxy;'''
        num = opera_db.get_effect_row(sql)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()["total"], str(num), run_method.errInfo(res))


class TestProxyQuery(unittest.TestCase):

    def test01_proxy_query_noId(self):
        """case01:方法列表--获取方法列表"""
        
        api = '/proxy/query'
        mid = opera_json.get_data("test01_proxy_create")
        data = {
            "id":mid
        }
        res = run_method.post(api,json=data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
    
    def test02_proxy_query_mock(self):
        """case01:方法列表--获取方法列表"""

        api = 'https://dt-dev.arctron.cn/api/proxy/query?debug=1&mock=true'
        data = {
            "id":"120620004952519178"
        }
        res = requests.post(api,json=data)
        self.assertEqual(res.status_code, 200, run_method.errInfo(res))
        self.assertEqual(res.json()[0]["aims"],595,run_method.errInfo(res))
        
    @classmethod
    def tearDownClass(cls):
        mid = opera_json.get_data("test01_proxy_create")
        sql = '''delete from proxy where id = {};'''.format(mid)
        opera_db.delete_data(sql)