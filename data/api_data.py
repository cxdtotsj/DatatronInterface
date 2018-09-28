"""
1.test_qa 测试文件的继承
"""
import datetime
import random
from base.public_param import PublicParam

class UserApiData:

    #  /user/create
    user_num = random.randint(1,50)
    user_name = "auto_test{}".format(user_num)


class CorpApiData:

    pass