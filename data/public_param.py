'''
1.获取超级管理员token
'''
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base.base_method import BaseMethod
from util.operation_db import OperationDB
import random
import time
import requests


class PublicParam:

    def __init__(self):
        self.run_method = BaseMethod()
        self.super_token = self.get_super_token()
        self.opera_db = OperationDB()

    # 获取超级管理员(1 << 30) token
    def get_super_token(self):
        api = "/user/login"
        data = {"email": "admin@admin",
                "password": "abc123"}
        try:
            res = self.run_method.post(api, data)
            res.raise_for_status()
            token = res.json()["token"]
            return token
        except:
            print(self.run_method.errInfo(res))

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
        try:
            res = self.run_method.post(api, data)
            res.raise_for_status()
            token = res.json()["token"]
            corp_id = res.json()["corp_id"]
            return token, corp_id
        except:
            print(self.run_method.errInfo(res))


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
 
    def stamp_random_CEM(self):
        """时间戳和随机数生成 corp_name、random_email、random_mobile、zone_name、building_name"""
        time.sleep(2)
        stamp = int(time.time())

        corp_name = "随机组织名称{}".format(stamp)
        random_email = "rd{}@random.com".format(stamp)
        random_mobile = random.randint(10000000000, 19999999999)
        zone_name = "随机园区名称{}".format(stamp)
        building_name = "随机建筑名称{}".format(stamp)
        sql = '''select mobile from user where mobile = '{}';'''.format(random_mobile)
        sql_mobile = self.opera_db.get_fetchone(sql)
        # 判断随机生成的 mobile 是否已存在
        while sql_mobile is not None:
            random_mobile = random.randint(10000000000, 19999999999)
            sql = '''select mobile from user where mobile = '{}';'''.format(random_mobile)
            sql_mobile = self.opera_db.get_fetchone(sql)
        return corp_name,random_email,random_mobile,zone_name,building_name

    def random_name(self,name,num=None):
        """num=None,return random_name;
           num=int,return []
        """
        time.sleep(2)
        stamp = int(time.time())

        if num is None:
            random_name = '{}{}'.format(name,stamp)
        else:
            random_name = ['{}-{}{}'.format(i,name,stamp) for i in range(num)]
        return random_name


    # 创建用户
    def create_user(self, user_name, passwd, email=None, mobile=None):
        api = '/user/create'
        data = {
            "mobile": mobile,
            "email": email,
            "name": user_name,
            "password": passwd}
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("用户创建失败")
            print(self.run_method.errInfo(res))

    # 创建公司
    def create_corp(self, corp_name=None):
        '''返回 corp_id'''
        api = "/corp/create"
        if corp_name is not None:
            corp_name = corp_name
        else:
            corp_name,*__ = self.stamp_random_CEM()
        data = {"name": corp_name}
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("组织(公司)创建失败")
            print(self.run_method.errInfo(res))

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
            assert res.json()["id"] is not '',self.run_method.errInfo(res)
        except:
            print("用户绑定到组织失败")
            print(self.run_method.errInfo(res))

    # 用户第一次登录前重置密码
    def user_pwd_reset(self, password, newpasswd, user_id=None, email=None, mobile=None):
        '''user_id email mobile 三选一'''

        api = "/user/passwd/reset"
        data = {
            "password": password,
            "newpasswd": newpasswd}
        if user_id is not None:
            email = None
            mobile = None
            data.update(id=user_id)
        elif email is not None:
            mobile = None
            data.update(email=email)
        elif mobile is not None:
            data.update(mobile=mobile)
        try:
            res = self.run_method.post(
                api, data, headers=self.get_super_header())
            res.raise_for_status()
        except:
            print("用户重置密码失败")
            print(self.run_method.errInfo(res))

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
            print(self.run_method.errInfo(res))

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
        try:
            del_response = self.run_method.post(
                del_api, data, headers=self.get_super_header())
            del_response.raise_for_status()
        except:
            print("用户删除失败")
            print(self.run_method.errInfo(del_response))

    # 创建用户，包括 : 管理员用户，普通用户，返回header
    def common_user(self, corp_id=None, role=None):
        '''自动生成email、mobile,返回user_header, 组织管理员 role=1<<19'''

        corp_name,random_email,random_mobile,*__ = self.stamp_random_CEM()
        user_name = "随机生成用户"
        oldpasswd = "123456"
        newpasswd = "12345678"
        if corp_id is not None:
            corp_id = corp_id
        else:
            corp_id = self.create_corp(corp_name)
        # 新增用户
        user_id = self.create_user(
            user_name, oldpasswd, email=random_email, mobile=random_mobile)
        # 用户绑定到组织
        self.user_add_corp(user_id, corp_id=corp_id, role=role)
        # 用户重置密码
        self.user_pwd_reset(oldpasswd, newpasswd, user_id=user_id)
        # 用户登录并返回 header
        user_header = self.user_header(newpasswd, email=random_email)
        return user_header

    # 新增用户，修改密码，绑定到组织,返回 email、mobile、user_id
    def user_reset_corp(self, corp_id=None, role=None):
        '''返回email、mobile、user_id, 组织管理员 role=524288'''

        corp_name,random_email,random_mobile,*__ = self.stamp_random_CEM()
        user_name = "随机生成用户"
        oldpasswd = "123456"
        newpasswd = "12345678"
        if corp_id is not None:
            corp_id = corp_id
        else:
            corp_id = self.create_corp(corp_name)
        # 新增用户
        user_id = self.create_user(user_name, oldpasswd,email=random_email, mobile=random_mobile)
        # 用户重置密码
        self.user_pwd_reset(oldpasswd, newpasswd, user_id=user_id)
        # 用户绑定到组织
        self.user_add_corp(user_id, corp_id=corp_id, role=role)
        return random_email,random_mobile,user_id

    # 新增用户，修改密码，绑定到组织,返回 email、mobile、user_id
    def user_reset(self):
        '''返回email、mobile、user_id'''

        __,random_email,random_mobile,*__ = self.stamp_random_CEM()
        user_name = "随机生成用户"
        oldpasswd = "123456"
        newpasswd = "12345678"
        # 新增用户
        user_id = self.create_user(user_name, oldpasswd,email=random_email, mobile=random_mobile)
        # 用户重置密码
        self.user_pwd_reset(oldpasswd, newpasswd, user_id=user_id)
        return random_email,random_mobile,user_id


    # 新增用户，并绑定到组织, 未修改密码
    def user_corp(self,corp_id=None,role=None):
        """返回email、mobile、user_id, 组织管理员 role=524288"""

        corp_name,random_email,random_mobile,*__ = self.stamp_random_CEM()
        user_name = "随机生成用户"
        oldpasswd = "123456"
        if corp_id is not None:
            corp_id = corp_id
        else:
            corp_id = self.create_corp(corp_name)
        # 新增用户
        user_id = self.create_user(user_name,oldpasswd,email=random_email,mobile=random_mobile)
        # 用户绑定到组织
        self.user_add_corp(user_id, corp_id=corp_id, role=role)
        return random_email,random_mobile,user_id


    # 园区 id
    def create_zone(self, header=None,data=None):
        api = '/zone/create'
        if data is not None:
            data = data
        else:
            *__,zone_name,__ = self.stamp_random_CEM()
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
            print(self.run_method.errInfo(res))

    # 当传入 zone_id,未传入 header 时，传入的 zone_id 无效
    def create_building(self, zone_id=None, header=None, is_belong_zone=True):
        '''返回建筑ID'''
        api = '/building/create'
        *__,building_name,__ = self.stamp_random_CEM()

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
            print(self.run_method.errInfo(res))
    
    # 创建独栋建筑
    def create_sign_building(self,data=None,header=None):
        """data默认时，为独栋建筑；return 建筑 ID"""
        api = '/building/create'
        if data is not None:
            data = data
        else:
            *__,building_name,__ = self.stamp_random_CEM()
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
        if header is not None:
            user_header = header
        else:
            user_header = self.common_user(role=524288)
        try:
            res = self.run_method.post(api, json=data, headers=user_header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("新增建筑失败")
            print(self.run_method.errInfo(res))


    # 获取园区详细信息
    def zone_get(self, zone_id, header):
        api = "/zone/get"
        data = {"id": zone_id}
        try:
            res = self.run_method.post(api, data, headers=header)
            res.raise_for_status()
            return res.json()
        except:
            print("获取园区详细信息失败")
            print(self.run_method.errInfo(res))

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
            print(self.run_method.errInfo(res))
    
    # 创建building，并上传模型
    def building_model_upload(self,building_id=None,header=None,model_type=None,filename=None):
        "return r.json(),building_id"

        if building_id is not None:
            building_id = building_id
        else:
            building_id = self.create_building(header=header)
        if model_type is not None:
            model_type=model_type
        else:
            model_type = "T"
        if filename is not None:
            filename=filename
        else:
            filename = 'Office.objr'
        api = "/building/model/upload"
        path_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig',filename)
        data = {
                "building_id" :building_id,
                "model_type":model_type
            }
        try:
            with open(path_file,'rb') as fileop:
                files = {"file":fileop}
                r = self.run_method.post(api,data=data,files=files,headers=header)
        except:
            print("创建building并上传模型失败")
            print(self.run_method.errInfo(r))
        if "err" in r.json():
            print("创建building并上传模型返回error")
            print(self.run_method.errInfo(r))
        return r.json(),building_id



    # 获取meta_url页面构件的GUID
    def get_guid(self,meta_url):
        """输入 meta_url,返回 guid"""
        for i in range(6):
            r = requests.get(meta_url)
            if r.status_code == 200:
                break
            else:
                time.sleep(5)
        try:
            guid = r.json()["Entities"][0]["Guid"]
        except ValueError:
            guid = None
        return guid

    # 获取更新后的meta_url 页面返回的更新后的 Entities
    def get_update_entities(self,meta_url,old_guid):
        """输入 meta_url，未更新前的 old_guid,返回 entities"""
        for i in range(6):
            guid = self.get_guid(meta_url)  # 获取新的guid
            if guid == old_guid:            # 更新完成前，guid仍是原来的
                time.sleep(5)
            else:
                break
        try:
            entities = requests.get(meta_url).json()["Entities"]
        except ValueError:
            entities = None
        return entities
    
    # 获取构件信息
    def get_entity(self,model_id,guid):
        """return entity.json()"""
        api = 'building/model/entityget'
        data = {
            "model_id":model_id,
            "guid":guid
        }
        try:
            entity = self.run_method.post(api,data)
            entity.raise_for_status()
            return entity.json()
        except:
            print("获取构建信息超时")
            print(self.run_method.errInfo(entity))
        
if __name__ == "__main__":
    import time
    bd = PublicParam()
    name_1 = bd.random_name("自动化")
    print(name_1)
    can1,can2,can3 = bd.random_name("参数化",3)
    print(can1,can2,can3)