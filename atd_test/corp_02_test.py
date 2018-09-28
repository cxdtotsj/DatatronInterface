'''用户类接口'''
import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import CorpApiData as Corp
from base.base_method import BaseMethod
from base.public_param import PublicParam
import unittest


class TestCorp(unittest.TestCase, Corp):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.super_header = cls.pub_param.get_super_header()
    
    def test_01_01_corp_create_noName(self):
        '''case01_01:创建组--name为空'''

        api = '/corp/create'
        data = {"name":None}
    
    def test01_02_corp_create_noToken(self):
        '''case01_02:创建组--无token'''
        pass
    
    def test01_03_corp_create_noAuth(self):
        '''case01_03:创建组--未授权'''
        pass
    

    # 超管用例 01 ~ 07
    def test02_01_corp_user_add_noUserId(self):
        '''case02_01:用户添加到组--无用户ID'''
        pass
    
    def test02_02_corp_user_add_errorUserId(self):
        '''case02_02:用户添加到组--错误的用户ID'''
        pass
    
    def test02_03_corp_user_add_super_noCorpId(self):
        '''case02_03:用户添加到组--无组ID'''
        pass
    
    def test02_04_corp_user_add_super_errorCorpId(self):
        '''case02_04:用户添加到组--错误的组ID'''
        pass
    
    def test02_05_corp_user_add_noToken(self):
        '''case02_05:用户添加到组--无token'''
        pass
    
    def test02_06_corp_user_add_super_success(self):
        '''case02_06:用户添加到组--添加用户成功'''
        pass
    
    def test02_07_corp_user_add_repeat(self):
        '''case02_07:用户添加到组--再次将相同用户添加到组'''
        pass

    # 组管理员账号 08 ~ 13
    def test02_08_corp_user_add_noCorpId(self):
        '''case02_08:用户添加到组--未传组ID(管理员同时在两个组)'''
        pass
    
    def test02_09_corp_user_add_havaCorpId(self):
        '''case02_09:用户添加到组--传入组ID(有管理员权限)'''
        pass
    
    def test02_10_corp_user_add_ohterCorpId(self):
        '''cas2_10:用户添加到组--传入其他组ID(无管理员权限)'''
        pass
    
    def test02_11_corp_user_add_noRole(self):
        '''case02_11:用户添加到组--未添加role'''
        pass

    def test02_12_corp_user_add_noRole(self):
        '''case02_12:用户添加到组--添加组管理员权限'''
        pass
    
    def test02_13_corp_user_add_noRole(self):
        '''case02_13:用户添加到组--添加超管权限'''
        pass

    def test02_14_corp_user_add_noAuth(self):
        '''case02_14:用户添加到组--用户在该组但无管理员权限'''
        pass
    

    # 超管用例 01 ~ 07
    def test03_01_corp_user_del_noUserId(self):
        '''case03_01:用户从组删除--无用户ID'''
        pass
    
    def test03_02_corp_user_del_errUserId(self):
        '''case03_02:用户从组删除--错误的用户ID'''
        pass

    def test03_03_corp_user_del_super_noCorpId(self):
        '''case03_03:用户从组删除--超管无组ID'''
        pass
    
    def test03_04_corp_user_del_super_errorCorpId(self):
        '''case03_04:用户从组删除--错误的组ID'''
        pass

    def test03_05_corp_user_del_noToken(self):
        '''case03_05:用户从组删除--无token'''
        pass
    
    def test03_06_corp_user_del_super_success(self):
        '''case03_06:用户从组删除--删除用户成功'''
        pass
    
    def test03_07_corp_user_del_repeat(self):
        '''case03_07:用户从组删除--再次删除用户'''
        pass
    
    # 组管理员账号 08 ~ 10
    def test03_08_corp_user_del_noCorpId(self):
        '''case03_08:用户从组删除--未传组ID(管理员同时在两个组)'''
        pass
    
    def test03_09_corp_user_del_haveCorpId(self):
        '''case03_09:用户从组删除--传入组ID(有管理员权限)'''
        pass
    
    def test03_10_corp_user_del_otherCorpId(self):
        '''cas3_10:用户从组删除--传入其他组ID(无管理员权限)'''
        pass
    
    def test03_11_corp_user_del_noAuth(self):
        '''case03_11:用户从组删除--用户在该组但无管理员权限'''
        pass    


    def test04_01_corp_list_noPage(self):
        '''case04_01:组列表--未传page'''
        pass
    
    def test04_02_corp_list_errPageType(self):
        '''case04_02:组列表--错误的page参数'''
        pass
    
    def test04_03_corp_list_noSize(self):
        '''case04_03:组列表--未传size'''
        pass
    
    def test04_04_corp_list_errSzieType(self):
        '''case04_04:组列表--错误的size参数'''
        pass
    
    def test04_05_corp_list_super_success(self):
        '''case04_05:组列表--超管查询成功'''
        pass

    def test04_06_corp_list_common_success(self):
        '''case04_06:组列表--普通用户查询成功'''
        pass