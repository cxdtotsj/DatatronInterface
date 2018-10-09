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
    stamp = int(time.time())
    zone_name = 'Auto园区名称{}'.format(stamp)


if __name__ == '__main__':
    zone = ZoneApiData()
    print(zone.zone_name)