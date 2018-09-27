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


class ApiData:

    # headers
    headers = {"content-type": "application/json"}

    # 用户手机号
    user_phone = 18321829313

    # 反馈内容 /api/v1/user/feedback
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feed_content = "自动反馈内容 %s" % time_now

    # 个人资料 /api/v1/user/edit
    random_num = random.randint(1,50)
    nick_name = "bear%s" % random_num

    # 作品 /api/v1/user/saveproject
    p_name = "作品名称 %s" % time_now
    p_desc = "作品简介 %s" % time_now
    p_img = "/1535965522439599110?imageView2/2/w/212/h/136/q/100"

    # 申诉内容
    appeal_content = "这是问题申诉内容 -- %s" % time_now