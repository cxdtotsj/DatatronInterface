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

    # 获取 登录 账号 token
    def user_login(self,passwd,email=None,mobile=None):
        """返回 header Authorization"""
        
        api = "/user/login"
        data = {
            "email":email,
            "mobile":mobile,
            "password":passwd
        }
        try:
            res = self.run_method.post(api, data)
            res.raise_for_status()
            token = res.json()["token"]
            return {"Authorization":token}
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
        """时间戳和随机数生成 corp_name、random_email、random_mobile"""
        time.sleep(2)
        stamp = int(time.time())
        rd5 = random.randint(0,10000)

        corp_name = "随机组织名称{}".format(stamp)
        random_email = "erd{}_{}@random.com".format(stamp,rd5)
        random_mobile = random.randint(10000000000, 99999999999)

        # 判断随机生成的 mobile 是否已存在
        sql_p = '''select mobile from user where mobile = '{}';'''.format(random_mobile)
        sql_mobile = self.opera_db.get_fetchone(sql_p)
        while sql_mobile is not None:
            random_mobile = random.randint(10000000000, 99999999999)
            sql_p2 = '''select mobile from user where mobile = '{}';'''.format(random_mobile)
            sql_mobile = self.opera_db.get_fetchone(sql_p2)

        # 判断 email 是否重复
        sql_e = '''select mobile from user where mobile = '{}';'''.format(random_mobile)
        sql_email = self.opera_db.get_fetchone(sql_e)
        while sql_email is not None:
            time.sleep(1)
            stamp1 = int(time.time())
            rd6 = random.randint(0,100000)
            random_mobile = "rm{}_{}@timestamp.com".format(stamp1,rd6)
            sql_e2 = '''select mobile from user where email = '{}';'''.format(random_mobile)
            sql_email = self.opera_db.get_fetchone(sql_e2)
            
        return corp_name,random_email,random_mobile

    def random_name(self,name,num=None):
        """num=None,return random_name;
           num=int,return []
        """

        time.sleep(1)
        stamp = int(time.time())
        rd5 = random.randint(0,10000)

        if num is None:
            random_name = '{}{}_{}'.format(name,stamp,rd5)
        else:
            random_name = ['{}_{}{}_{}'.format(i,name,stamp,rd5) for i in range(num)]
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
            corp_name = self.random_name("rd组织")
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

        corp_name,random_email,*__ = self.stamp_random_CEM()
        user_name = "随机生成用户"
        oldpasswd = "123456"
        newpasswd = "12345678"
        if corp_id is not None:
            corp_id = corp_id
        else:
            corp_id = self.create_corp(corp_name)
        # 新增用户
        user_id = self.create_user(
            user_name, oldpasswd, email=random_email)
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
            zone_name = self.random_name("rd园区")
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
        building_name = self.random_name("rd建筑")

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
            building_name = self.random_name("rd独栋建筑")
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
    def building_model_upload(self,building_id=None,header=None,model_type=None,filename=None,model_name=None):
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
        if model_name is not None:
            model_name = model_name
        else:
            model_name = "其他模型"
        api = "/building/model/upload"
        path_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),'dataconfig',filename)
        data = {
                "building_id" :building_id,
                "model_type":model_type,
                "model_name":model_name
            }
        try:
            with open(path_file,'rb') as fileop:
                files = {"file":fileop}
                r = self.run_method.post(api,data=data,files=files,headers=header)
                r.raise_for_status()
                if "err" in r.text:
                    print("创建building并上传模型返回error")
                    print(self.run_method.errInfo(r))
                return r.json(),building_id
        except:
            print("创建building并上传模型失败")
            print(self.run_method.errInfo(r))


    # 获取meta_url页面构件的GUID
    def get_guid(self,meta_url):
        """输入 meta_url,返回 guid"""
        for _ in range(6):
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


    # 获取meta_url的 entities
    def get_entities(self, meta_url):
        """输入 meta_url,返回 entities"""
        for _ in range(6):
            r = requests.get(meta_url)
            if r.status_code == 200:
                break
            else:
                time.sleep(5)
        try:
            entities = r.json()["Entities"]
        except ValueError:
            entities = None
        return entities

    # 获取 entities 的 guidList
    def get_guidList(self, building_id,header=None,filename=None):
        """返回 guidList,model_id"""
        # 上传建筑模型
        r, __ = self.building_model_upload(
            building_id=building_id, header=header,filename=filename)
        meta_url = r["meta_url"]
        model_id = r["model_id"]
        # 获取entities
        entities = self.get_entities(meta_url)
        guidList = [entity["Guid"] for entity in entities]
        return guidList,model_id

    # 获取更新后的meta_url 页面返回的更新后的 Entities
    def get_update_entities(self,meta_url,old_guid):
        """输入 meta_url，未更新前的 old_guid,返回 entities"""
        for _ in range(6):
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
        api = '/building/model/entityget'
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

    # 获取建筑模型信息
    def get_building_model(self,building_id,header):
        """return res.json()"""

        api = '/building/model/list'
        data = {
            "building_id":building_id
        }
        try:
            res = self.run_method.post(api,data,headers=header)
            res.raise_for_status()
            return res.json()
        except:
            print("获取建筑模型信息失败")
            print(self.run_method.errInfo(res))


    # 创建设备
    def create_device(self,data=None,header=None,device_type=None):
        """return device_id"""
        api = '/things/add'

        if device_type is not None:
            device_type = device_type
        else:
            device_type = "TYPE_DEVICE"
        if data is not None:
            data = data
        else:
            data = {
                "device_id":self.random_name("随机设备名称"),
                "device_type":device_type
                }
        if header is not None:
            user_header = header
        else:
            user_header = self.common_user(role=524288)
        try:
            res = self.run_method.post(api, data, headers=user_header)
            res.raise_for_status()
            return res.json()["id"]
        except:
            print("新增设备失败")
            print(self.run_method.errInfo(res))
    
    # 数据库创建 parent 关联设备
    def create_parent_device(self,header=None,device_num=None):
        """
        device_num:需要绑定到网关的设备数量
        """

        if header is not None:
            user_header = header
        else:
            user_header = self.common_user(role=524288)
        if device_num is not None:
            device_num = device_num
        else:
            device_num = device_num
        parent_id = self.create_device(header=user_header,device_type="TYPE_GATEWAY")
        for _ in range(device_num):
            device_id = self.create_device(header=user_header)
            sql = '''UPDATE things SET parent_id = '{}',device_type=0 
                    where id = '{}';'''.format(parent_id,device_id)
            self.opera_db.update_data(sql)
        return parent_id

    # 查询设备
    def get_things(self,things_id,header):
        """return scene_json"""

        api = '/things/get'
        data = {
            "id":things_id
        }
        try:
            res = self.run_method.post(api,data,headers=header)
            res.raise_for_status()
            return res.json()
        except:
            print("获取设备失败")
            print(self.run_method.errInfo(res))

    # 设备列表
    def get_things_list(self,header,parent_id=None):
        """return deviceId_list"""

        api = '/things/list'
        if parent_id is not None:
            data = {
                "parent_id":parent_id,
                "page":1,
                "limit":100
            }
        else:
            data = {
                "page":1,
                "limit":100
            }
        try:
            res = self.run_method.post(api,data,headers=header)
            res.raise_for_status()
            data_list = res.json()["data_list"]
            return [device["id"] for device in data_list]
        except:
            print("获取设备列表失败")
            print(self.run_method.errInfo(res))

    # 获取设备token
    def get_device_token(self,device_id,header):
        """return token"""

        api = '/things/token/get'
        data = {
            "id":device_id
        }
        try:
            res = self.run_method.post(api,data,headers=header)
            res.raise_for_status()
            return res.json()["token"]
        except:
            print("获取设备token失败")
            print(self.run_method.errInfo(res))

    # 解析device_token
    def analyze_device_token(self,token):
        """return res.json()"""
        
        api = '/token'
        data = {
            "token":token
        }
        try:
            res = self.run_method.post(api,data)
            res.raise_for_status()
            return res.json()
        except:
            print("解析设备token失败")
            print(self.run_method.errInfo(res))
    
    # 插入设备属性 things_data
    def insert_thingsData(self,corp_id,things_id,attrs_name):
        """attrs_name必须为可迭代类型"""

        for name in attrs_name:
            random_id = int(time.time())
            create_at = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(random_id))
            sql = '''INSERT INTO things_data
                        (id,corp_id,things_id, name, dtype, value, bvalue, svalue, dvalue, create_at) 
                    VALUES 
                        ('{}','{}','{}', '{}', '', 0, 0, 0, NULL, '{}');'''.format(
                            random_id,corp_id,things_id,name,create_at)
            self.opera_db.insert_data(sql)
            time.sleep(1)
        
    
    # 创建场景
    def create_scene(self,data=None,header=None):
        """return scene_id"""

        api = '/scene/create'
        if data is not None:
            data = data
        else:
            scene_name = self.random_name("随机场景名称")
            data = {
                "name":scene_name
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
            print("新增场景失败")
            print(self.run_method.errInfo(res))
    
    # 获取场景
    def get_scene(self,scene_id):
        """return scene_json"""

        api = '/scene/get'
        data = {
            "id":scene_id
        }
        try:
            res = self.run_method.post(api,data)
            res.raise_for_status()
            return res.json()
        except:
            print("获取场景失败")
            print(self.run_method.errInfo(res))



if __name__ == "__main__":
    import time
    bd = PublicParam()
    cid = bd.create_corp()
    print(cid)


