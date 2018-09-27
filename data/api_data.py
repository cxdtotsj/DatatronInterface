"""
1.test_qa 测试文件的继承
"""
import datetime
import random


class QaApiData:

    # 专家提问接口 /api/v1/qa/qsubmit
    qa_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    qa_title = "这是问题题目 -- %s" % qa_time
    qa_desc = "这是问题描述 -- %s" % qa_time
    qa_img_one = ["/1536116758846885506?imageView2/2/w/212/h/136/q/100"]
    qa_img_four = ["/1536116758846885506?imageView2/2/w/212/h/136/q/100",
                  "/1536116758846885506?imageView2/2/w/212/h/136/q/100",
                  "/1536116758846885506?imageView2/2/w/212/h/136/q/100",
                  "/1536116758846885506?imageView2/2/w/212/h/136/q/100"]
    qa_headers = {"content-type": "application/json"}

    # 专家回答接口 /api/v1/qa/asubmit
    answer_content = "这是问题答案 -- %s" % qa_time


class UserApiData:

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