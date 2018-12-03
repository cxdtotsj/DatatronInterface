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
# c = time.localtime(1542875030)
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


# import requests    
# url = "https://dt-dev.arctron.cn/api/user/login"
# data = {"email": "admin@admin", 
#         "password": "abc123"}
# r = requests.post(url,data)
# print(r.text)
# print("X-Request-Id : %s" %r.headers["X-Request-Id"]) 

#
# def get_value(a):
#     b = []
#     b.append(a["corp_id"])
#     print(b)
#
# list_map = a["data_list"]
# rs = list(map(lambda i:i["corp_id"],list_map))
# print(rs)


# dict1 = {"a":1,"b":3}

# dict2 = {"c":5,"a":8}

# a = {'id': '111383146515149355', 'corp_id': '', 'name': 'Auto园区名称1539077601', 'loc': {'province': '上海市', 'city': '上海市', 'county': '静安区', 'addr': '恒丰路329号'}, 'coord': {'longitude': 121, 'latitude': 31, 'altitude': 0}, 'building_num': 19, 'building_count': 0, 'area': 50, 'extra': {'build_corp': '建筑单位名称', 'build_start_at': '2018-10-09', 'plan_corp': '施工单位名称', 'plan_end_at': '2018-10-09', 'design_corp': '设计单位名称', 'design_end_at': '2018-10-09', 'construct_corp': '规划单位名称', 'construct_end_at': '2018-10-09', 'supervise_corp': '监理单位名称', 'supervise_end_at': '2018-10-09'}, 'status': 1, 'modify_by': '109777231298966563', 'create_at': '1539077528', 'update_at': '1539159376'}
# print(a["corp_id"])
# print(type(a["corp_id"]))

# site= {'name': '我的博客地址', 'alexa': 10000, 'url':'http://blog.csdn.net/uuihoo/'}
# site.pop('alexa',"url") # 删除要删除的键值对，如{'name':'我的博客地址'}这个键值对
# print(site)

# list1 = [1,2,3]
# print(sum(list1))

# modelType_list = ['B','A','S','M','E','P','F','C']
# a = sorted(modelType_list)
# a.insert(0,"T")
# print(a)
# print(modelType_list)
# print(len(modelType_list))


# @staticmethod
# def listcontent(driver, path,except_value):
#     table = driver.find_element_by_xpath(path)
#     rows = table.find_elements_by_tag_name("tr")
#     rowcontents = []
#     for row in rows[1:]:
#         rowcontent = row.find_element_by_xpath("td[5]")
#         rowcontents.append(rowcontent)
#     texts = []
#     for coll in rowcontents:
#         text = coll.text
#         texts.append(text)
#     assert except_value in texts,"this is  except_value : ...{}...,\n this is texts : ...{}...".format(except_value,texts)


# test_id = 123

# class testAr:

#     def testar(self):

#         test_id = 456
#         print(test_id)

# if __name__ == '__main__':
#     ar = testAr()
#     ar.testar()

import uuid

a = uuid.uuid4
print(a)