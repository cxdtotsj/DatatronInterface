import datetime
import time
import sys
import os

# env_dist = os.environ
# print(env_dist)
#
# for key in env_dist:
#     print(key + ':' + env_dist[key])


# def get_baseurl(key):
#     baseurl = os.environ.get(key)
#     return baseurl
#
# print(get_baseurl("JAVA_HOME"))
# path = os.environ.get("GOPATH")
# print(path)



# a = "这是一条评论 %s" %(datetime.datetime.now())
# print(a)
# print(type(a))

# b = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# print(b)
#
# # 获取当前时间戳
# a = int(time.time()+1000)
# print(a)
#
# # 时间戳转换成时间
# c = time.localtime(a)
# d = time.strftime("%Y-%m-%d %H:%M:%S",c)
# print(d)

# 转换时间戳函数1534474495
# def human_time(stamptime):
#     c = time.localtime(stamptime)
#     d = time.strftime("%Y-%m-%d %H:%M:%S", c)
#     print(d)
#
# human_time(1534474495)




# timeStamp = 1535791757
# timearrary = time.localtime(timeStamp)
# cuurrenttime = time.strftime("%Y-%m-%d %H:%M:%S",timearrary)
# print(cuurrenttime)
# print(type(cuurrenttime))

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# time_now = datetime.datetime.now().date()
# filepath = r"{}\report\report{}.html".format(rootPath, time_now)
# file_name = filepath.split("report2")[1]
# true_name = "report2{}".format(file_name)
# print(true_name)
#
# class get_time:
#
#     def gettime(self):
#         time_test = datetime.datetime.now()
#         return time_test

# '''模拟装饰器'''
#
#
# def contin(func):
#     def count_print():
#         for i in range(1, 10):
#             func()
#     return count_print
#
#
#
# @contin
# def print_num():
#     print(1)
#
#
# print_num()

    # 获取测试用户的 user_id，token
    def get_token(self):
        api = "/api/v1/user/login"
        data = {"mobile": 18321829313, "password": "Password01!"}
        res = self.run_method.post(api, data)
        if res.status_code == 200:
            res_dict = res.json()
            try:
                self.token = res_dict["data"]["token"]
                self.user_id = res_dict["data"]["user_id"]
                return self.token, self.user_id
            except BaseException:
                print("用户名或验证码错误")
        else:
            print("服务器登陆失败")


def comm_login(mobile,passwd):
    def actual_decorator(decorated):
        def inner(*args,**kws):
            api = "/api/v1/user/login"
            data = {"mobile": mobile, "password": passwd}
            res = run_method.post(api, data)
            token = res_dict["data"]["token"]
            user_id = res_dict["data"]["user_id"]






def test06_01_user_feedback_noContent(self):
    """case06-01 : 用户反馈 ;
        未填写反馈内容 """
    api = "/api/v1/user/feedback"
    data = {"user_id": self.user_id,
            "token": self.token}

    res = self.run_method.post(api, data)

    self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
    self.assertEqual(
        self.run_method.get_result(res),
        "fail", res.json())
    self.assertEqual(
        self.run_method.get_errno(res),
        "-50030",
        "返回的errno不正确")

    
