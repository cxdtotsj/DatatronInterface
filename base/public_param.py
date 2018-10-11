'''
1.获取超级管理员token
'''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_method import BaseMethod
from util.operation_json import OperetionJson
import random
import time


class PublicParam:

    def __init__(self):
        self.run_method = BaseMethod()
        self.super_token = self.get_super_token()
        self.opera_json = OperetionJson()

    # 获取超级管理员(1 << 30) token
    def get_super_token(self):
        api = "/user/login"
        data = {"email": "admin@admin",
                "password": "abc123"}
        res = self.run_method.post(api, data)
        res_dict = res.json()
        if res.status_code == 200:
            token = res_dict["token"]
            return token
        elif res.status_code == 400:
            err_code = res_dict["code"]
            if err_code == 1401:
                print("Super密码不匹配")
            elif err_code == 1404:
                print("Super用户不存在")
            elif err_code == 1426:
                print("Super密码需修改")

    # 超级管理员 (1 << 30) header
    def get_super_header(self):
        return {"Authorization": self.super_token}

    # 公司管理员 token
    def get_corp_token(self, email=None, password=None):
        '''未传入参数时，返回管理员token;
            传入参数，则返回指定用户token'''
        api = "/user/login"
        if email is not None:
            data = {"email": email,
                    "password": password}
        else:
            data = {"email": "xdchenadmin@admin",
                    "password": 12345678}
        res = self.run_method.post(api, data)
        res_dict = res.json()
        if res.status_code == 200:
            token = res_dict["token"]
            corp_id = res_dict["corp_id"]
            return token, corp_id
        elif res.status_code == 400:
            err_code = res_dict["code"]
            if err_code == 1401:
                print("Corp密码不匹配")
            elif err_code == 1404:
                print("Corp用户不存在")
            elif err_code == 1426:
                print("Corp密码需修改")

    # 公司管理员 header
    def get_corp_user(self):
        '''同时返回 header 、corp_id'''
        corp_token, corp_id = self.get_corp_token()
        return {"Authorization": corp_token}, corp_id

    # 获取错误码
    def get_code(self, res):
        res_dict = res.json()
        result_code = res_dict["code"]
        return result_code

    # 获取request_id
    def get_request_id(self, res):
        return "X-Request-Id : %s" % res.headers["X-Request-Id"]

    # 创建用户
    def create_user(self, email, user_name, passwd):
        api = '/user/create'
        data = {"email": email,
                "name": user_name,
                "password": passwd}
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("用户创建失败")
            print(res.json())

    # 创建公司
    def create_corp(self, corp_name):
        api = "/corp/create"
        data = {"name": corp_name}
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("组织(公司)创建失败")
            print(res.json())

    # 用户添加到组织（公司）
    def user_add_corp(self, user_id, corp_id, role=None):
        api = "/corp/user/add"
        if role is not None:
            data = {"user_id": user_id,
                    "corp_id": corp_id,
                    "role": role}
        else:
            data = {"user_id": user_id,
                    "corp_id": corp_id}
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
            assert res.json()["id"] is not ''
        except:
            print("用户绑定到组织失败")
            print(res.json())

    # 用户第一次登录前重置密码
    def user_pwd_reset(self, user_id, password, newpasswd):
        api = "/user/passwd/reset"
        data = {"id": user_id,
                "password": password,
                "newpasswd": newpasswd}
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
        except:
            print("用户重置密码失败")
            print(res.json())

    # 用户登录并返回token
    def user_header(self, password, email=None, mobile=None):
        api = "/user/login"
        if email is not None:
            data = {"email": email,
                    "password": password}
        elif mobile is not None:
            data = {"mobile": mobile,
                    "password": password}
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
            return {"Authorization": res.json()["token"]}
        except:
            print("用户登录失败")
            print(res.json())

    # 将用户从组织删除
    def user_corp_del(self, user_id, corp_id=None, corp_header=None):
        del_api = "/corp/user/del"
        if corp_id is not None:
            data = {"corp_id": corp_id,
                    "user_id": user_id}
            del_response = self.run_method.post(
                del_api, data, headers=corp_header)
        else:
            data = {"user_id": user_id}
            del_response = self.run_method.post(
                del_api, data, headers=self.get_super_header())
        if del_response.status_code is not 200:
            print("用户新增失败")
            print(del_response.json())

    # 创建用户，包括 : 管理员用户，普通用户，返回header
    def common_user(self, corp_id=None, role=None):
        '''返回user_header, 组织管理员 role=524288'''
        stamp = int(time.time())
        corp_name = "随机组织名称{}".format(stamp)
        random_email = "rd{}@random.com".format(random.randint(100000, 999999))
        user_name = "随机生成用户"
        oldpasswd = "123456"
        newpasswd = "12345678"
        if corp_id is not None:
            corp_id = corp_id
        else:
            corp_id = self.create_corp(corp_name)
        # 新增用户
        user_id = self.create_user(random_email, user_name, oldpasswd)
        # 用户绑定到组织
        self.user_add_corp(user_id, corp_id=corp_id, role=role)
        # 用户重置密码
        self.user_pwd_reset(user_id, oldpasswd, newpasswd)
        # 用户登录并返回 header
        user_header = self.user_header(newpasswd, email=random_email)
        return user_header

    # 园区 id
    def create_zone(self, header=None):
        api = '/zone/create'
        random_num = int(time.time()) + random.randint(0,100000)
        zone_name = "随机园区名称{}".format(random_num)
        data = {
            "name": zone_name,
            "area": 100,
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
        if header is not None:
            user_header = header
        else:
            user_header = self.common_user(role=524288)
        try:
            res = self.run_method.post(api, json=data, headers=user_header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("新增园区失败")
            print(res.json())

    # 当传入 zone_id,未传入 header 时，传入的 zone_id 无效
    def create_building(self, zone_id=None,header=None,is_belong_zone=True):
        '''返回建筑ID'''
        api = '/building/create'
        random_num = int(time.time()) + random.randint(0,100000)
        zone_name = "随机建筑名称{}".format(random_num)
        data = {
            "name": zone_name,
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
        if zone_id is not None:
            is_belong_zone = True
            data.update(zone_id=zone_id)
        if header is not None:
            user_header = header
        else:
            user_header = self.common_user(role=524288)
            zone_id = self.create_zone(header=user_header)
            if is_belong_zone:
                data.update(zone_id=zone_id)
        try:
            res = self.run_method.post(api, json=data, headers=user_header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("新增建筑失败")
            print(res.json())

    # 获取园区详细信息
    def zone_get(self, zone_id, header):
        api = "/zone/get"
        data = {"id": zone_id}
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()
        except:
            print(res.json())
            print("获取园区详细信息失败")

    # 获取建筑详细信息
    def building_get(self, building_id, header):
        api = "/building/get"
        data = {"id": building_id}
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()
        except:
            print("获取建筑详细信息失败")


if __name__ == "__main__":
    import time
    import requests
    # 111656884594815531
    basedata = PublicParam()
    data1 = basedata.create_building(is_belong_zone=False)
    print(data1)


