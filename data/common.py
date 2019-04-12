"""公共方法"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import random
from base.base_method import BaseMethod


class Common:

    def __init__(self):
        self.run_method = BaseMethod()

    def login(self, passwd, email=None, mobile=None):
        """返回登录信息"""
        api = "/user/login"
        data = {
            "email": email,
            "mobile": mobile,
            "password": passwd
        }
        try:
            res = self.run_method.post(api, data)
            res.raise_for_status()
            return res.json()
        except:
            print(self.run_method.errInfo(res))

    def header_user(self, passwd, email=None, mobile=None):
        """返回 用户登录header"""
        res = self.login(passwd=passwd, email=email, mobile=mobile)
        token = res["token"]
        return {"Authorization": token, "id-prefix": "ci"}

    def header_super(self):
        """返回 超级管理员header"""
        return self.header_user(passwd="abc123", email="admin@admin")

    def header_corp(self):
        """返回 组织管理员header、corp_id"""
        res = self.login(passwd=12345678, email="xdchenadmin@admin")
        token = res["token"]
        cid = res["corp_id"]
        return {"Authorization": token, "id-prefix": "ci"}, cid

    def header_common(self):
        """返回 组织普通用户header"""
        return self.header_user(passwd="12345678", email="common.user@xdchen.com")

    def header_otherCorp(self):
        """返回 其他组织管理员header"""
        return self.header_user(passwd="12345678", email="othercorp@xdchen.com")

    def get_request_id(self,res):
        """获取请求返回的request_id"""
        return "X-Request-Id : %s" % res.headers["X-Request-Id"]
    
    def random_name(self,name,num=None):
        """
        num=None,return random_name;
        num=int,return []
        """
        stamp = int(time.time())
        rd8 = random.randint(0,10000000)
        if num is None:
            random_name = '{}{}_{}'.format(name,stamp,rd8)
        else:
            random_name = ['{}_{}{}_{}'.format(i,name,stamp,rd8) for i in range(num)]
        return random_name


if __name__ == '__main__':
    common = Common()
    # super_header = common.header_super()
    # print(super_header)
    # corp_header,corp_id = common.header_corp()
    # print(corp_header, corp_id)
    # common_header = common.header_common()
    # print(common_header)
    # otherCorp_header = common.header_otherCorp()
    # print(otherCorp_header)
    name = common.header_common()
    print(name)