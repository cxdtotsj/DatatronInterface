"""
1.test_qa 测试文件的继承
"""
import datetime
import time
import random

class UserApiData:

    #  /user/create
    user_num = random.randint(1,50)
    user_name = "auto_test{}".format(user_num)


class CorpApiData:

    pass


class ZoneApiData:

    # /zone/create
    @classmethod
    def random_num(self):
        stamp = int(time.time())
        random_num = stamp + random.randint(0,100000)
        zone_name = 'Auto园区名称{}'.format(random_num)
        return zone_name


class BuildingApiData:

    @classmethod
    def building_data(self):
        # /zone/create
        stamp = int(time.time())
        random_num = stamp + random.randint(0,100)
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