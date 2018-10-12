"""
1.test_qa 测试文件的继承
"""
import datetime
import time
import random


class UserApiData:

    #  /user/create
    user_num = random.randint(1, 50)
    user_name = "auto_test{}".format(user_num)
    user_email = "auto{}@auto.com".format(random.randint(100000, 999999))
    user_mobile = random.randint(10000000000,19999999999)
    oldpasswd = "123456"
    newpasswd = "12345678"


class CorpApiData:

    pass


class ZoneApiData:

    @classmethod
    def zone_data(self):
        # /zone/create
        stamp = int(time.time())
        random_num = stamp + random.randint(0, 100000)
        zone_name = 'Auto园区名称{}'.format(random_num)
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
                "altitude": 0
            }
        }
        return data


class BuildingApiData:

    @classmethod
    def building_data(self):
        # /zone/create
        stamp = int(time.time())
        random_num = stamp + random.randint(0, 100)
        building_name = 'Auto建筑名称{}'.format(random_num)
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
                "longitude": 0
            }
        }
        return data


if __name__ == '__main__':
    # a = BuildingApiData()
    print(BuildingApiData.building_data()["name"])
    print(type(BuildingApiData.building_data()))
    print(BuildingApiData.building_data()["name"])
