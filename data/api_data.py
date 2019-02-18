"""
1.test_qa 测试文件的继承
"""
import datetime
import time
import random
import os


class UserApiData:

    #  /user/create
    @classmethod
    def user_name(self):
        user_name = "auto_test{}".format(random.randint(1, 50))
        return user_name

    @classmethod
    def user_email(self):
        rd5 = random.randint(10000,99999)
        rd6 = random.randint(100000, 999999)
        user_email = "auto{}_{}@auto.com".format(rd5,rd6)
        return user_email

    @classmethod
    def user_mobile(self):
        user_mobile = random.randint(10000000000,99999999999)
        return user_mobile

    oldpasswd = "123456"
    newpasswd = "12345678"


class CorpApiData:

    @classmethod
    def corp_name(self):
        time.sleep(1)
        stamp = int(time.time())
        rd5 = random.randint(10000,99999)
        corp_name = 'Auto组织名称{}_{}'.format(stamp,rd5)
        return corp_name


class ZoneApiData:

    @classmethod
    def zone_data(self):
        # /zone/create
        time.sleep(1)
        stamp = int(time.time())
        rd5 = random.randint(10000,99999)
        zone_name = 'Auto园区名称{}_{}'.format(stamp,rd5)
        # 园区新增基础 json，缺少 corp_id, extra 字段
        data = {
            "name": zone_name,
            "area": 1000,
            "building_num": 19,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "coord": {
                "longitude": 121,
                "latitude": 31,
                "altitude": 0,
                "angle":0
            }
        }
        return data


class BuildingApiData:

    @classmethod
    def building_data(self):
        # /zone/create
        time.sleep(1)
        stamp = int(time.time())
        rd5 = random.randint(10000,99999)
        building_name = 'Auto建筑名称{}_{}'.format(stamp,rd5)
        # 建筑新增基础 json，缺少 zone_id, extra 字段
        data = {
            "name": building_name,
            "loc": {
                "province": "上海市",
                "city": "上海市",
                "county": "静安区",
                "addr": "恒丰路329号"
            },
            "area": 100,
            "layer_num": 31,
            "underlayer_num": 3,
            "coord": {
                "altitude": 122,
                "latitude": 32,
                "longitude": 0,
                "angle":0
            }
        }
        return data

    file_LangChaV2 = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig','LangChaV2.objr')
    file_Office = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig','Office.objr')
    file_TPY_7 = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig','TPY-ZL-A-7F.objr')

    # modeltype_list = ['T','S','A','M','E','P','F','C','B']
    modeltype_list = ['T','S','A']

    @classmethod
    def modelType_sorted(self):
        """返回已排序的 model_type"""
        modelType_list = ['S','A']
        # modelType_list = ['T','S','A','M','E','P','F','C','B']
        modelType_list.sort()
        modelType_list.insert(0,'T')
        return modelType_list


class ThingsApiData:
    
    @classmethod
    def device_id(self):
        time.sleep(1)
        stamp = int(time.time())
        rd5 = random.randint(10000,99999)
        device_id = 'Auto设备名称{}_{}'.format(stamp,rd5)
        return device_id

class SceneApiData:

    @classmethod
    def scene_name(self):
        time.sleep(1)
        stamp = int(time.time())
        rd5 = random.randint(10000,99999)
        scene_name = 'Auto场景名称{}_{}'.format(stamp,rd5)
        return scene_name




if __name__ == '__main__':
    a = BuildingApiData()
    print(a.file_Office)
    