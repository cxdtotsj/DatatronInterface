import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import BuildingApiData as Building
from data.api_data import ThingsApiData as Things
from base.base_method import BaseMethod
from data.public_param import PublicParam
from util.operation_json import OperetionJson
from util.operation_assert import OperationAssert
from util.operation_db import OperationDB
import unittest
import time
import requests
from random import randint

run_method = BaseMethod()
pub_param = PublicParam()
opera_json = OperetionJson()
opera_assert = OperationAssert()
opera_db = OperationDB()
super_header = pub_param.get_super_header()
corp_header, corp_id = pub_param.get_corp_user()


class AddData():

    def add_device(self):
        api = '/things/add'
        data = {
            "device_name": Things.device_name()
        }
        try:
            res = run_method.post(api, data, headers=corp_header)
            res.raise_for_status()
            device_id = res.json()["id"]
            return device_id
        except:
            print(run_method.errInfo(res))

    # 设备id list
    def add_device_idList(self, num):
        device_idList = [self.add_device() for i in range(num)]
        return device_idList

    def get_entities(self, meta_url):
        """输入 meta_url,返回 entities"""
        for i in range(6):
            r = requests.get(meta_url)
            if r.status_code == 200:
                break
            else:
                time.sleep(5)
        try:
            entities = r.json()["Entities"]
        except ValueError:
            entities = None
        return entities

    # entities guid list
    def get_guidList(self, building_id):
        # 上传建筑模型
        r, __ = pub_param.building_model_upload(
            building_id=building_id, header=corp_header,filename="LangChaV2.objr")
        meta_url = r["meta_url"]
        # 获取entities
        entities = self.get_entities(meta_url)
        guidList = [entity["Guid"] for entity in entities]
        return guidList

    # building_model_things表 insert
    def bd_add_main(self):
        building_id = pub_param.create_building(header=corp_header)
        guidList = self.get_guidList(building_id)
        device_idList = self.add_device_idList(len(guidList))
        dg_list = list(zip(device_idList, guidList))
        print(dg_list)
        for device_id, guid in dg_list:
            sql = '''INSERT INTO building_model_things 
                    (id,things_id, building_id, type, guid, uRl, create_at, update_at) 
                    VALUES 
                    ('{}','{}', '{}', 'bim', '{}', 'http://www.baidu.com', '2018-11-07 15:31:16', '2018-11-07 15:31:16');'''.format(randint(1000000000, 9999999999), device_id, building_id, guid)
            opera_db.insert_data(sql)
            time.sleep(1)


if __name__ == '__main__':
    ad = AddData()
    
    building_id = pub_param.create_building(header=corp_header)
    glist = ad.get_guidList(building_id)
    print(glist)