'''组织类接口'''
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
        pass
    
    def test01_02_corp_create_noToken(self):
        '''case01_02:创建组--无token'''
        pass
    
    def test01_03_corp_create_noAuth(self):
        '''case01_03:创建组--未授权'''
        pass
    
    def test01_04_corp_create_success(self):
        '''case01_03:创建组--标准输入'''
        pass


    # 超管用例 01 ~ 07
    def test02_01_corp_user_add_noUserId(self):
        '''case02_01:用户添加到组--无用户ID'''
        pass
    
    def test02_02_corp_user_add_errUserId(self):
        '''case02_02:用户添加到组--错误的用户ID'''
        pass
    
    def test02_03_corp_user_add_super_noCorpId(self):
        '''case02_03:用户添加到组--无组ID'''
        pass
    
    def test02_04_corp_user_add_super_errCorpId(self):
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
        '''case02_08:用户添加到组--未传组ID(暂不考虑管理员同时在两个组)'''
        pass
    
    def test02_09_corp_user_add_havaCorpId(self):
        '''case02_09:用户添加到组--传入组ID(管理员所在组)'''
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
    

    def test03_01_corp_user_list_noPage(self):
        '''case03_01:组内用户列表--未传page'''
        pass
    
    def test03_02_corp_user_list_errPageType(self):
        '''case03_02:组内用户列表--错误的page参数'''
        pass

    def test03_03_corp_user_list_noSize(self):
        '''case03_03:组内用户列表--未传size'''
        pass
    
    def test03_04_corp_user_list_errSizeType(self):
        '''case03_04:组内用户列表--错误的size参数'''
        pass
    
    def test03_05_corp_user_list_super_noCorpId(self):
        '''case03_05:组内用户列表--超管无组ID'''
        pass
    
    def test03_06_corp_user_list_super_errCorpId(self):
        '''case03_06:组内用户列表--错误的组ID'''
        pass
    
    def test03_07_corp_user_list_noToken(self):
        '''case03_07:组内用户列表--无token'''
        pass
    
    def test03_08_corp_user_list_super_success(self):
        '''case03_08:组内用户列表--查看成功'''
        pass
    
    def test03_09_corp_user_list_noCorpId(self):
        '''case03_09:组内用户列表--未传组ID(管理员只在一个组)'''
        pass

    def test03_10_corp_user_list_noCorpId(self):
        '''case03_10:组内用户列表--未传组ID(暂不考虑管理员同时在两个组)'''
        pass    
    
    def test03_11_corp_user_list_haveCorpId(self):
        '''case03_11:组内用户列表--传入组ID(管理员所在组)'''
        pass  

    def test03_12_corp_user_list_otherCorpId(self):
        '''cas3_12:组内用户列表--传入其他组ID(无管理员权限)'''
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
    

    # 超管用例 01 ~ 07
    def test05_01_corp_user_del_noUserId(self):
        '''case05_01:用户从组删除--无用户ID'''
        pass
    
    def test05_02_corp_user_del_errUserId(self):
        '''case05_02:用户从组删除--错误的用户ID'''
        pass

    def test05_03_corp_user_del_super_noCorpId(self):
        '''case05_03:用户从组删除--超管无组ID'''
        pass
    
    def test05_04_corp_user_del_super_errCorpId(self):
        '''case05_04:用户从组删除--错误的组ID'''
        pass

    def test05_05_corp_user_del_noToken(self):
        '''case05_05:用户从组删除--无token'''
        pass
    
    def test05_06_corp_user_del_super_success(self):
        '''case05_06:用户从组删除--删除用户成功'''
        pass
    
    def test05_07_corp_user_del_repeat(self):
        '''case05_07:用户从组删除--再次删除用户'''
        pass
    
    # 组管理员账号 08 ~ 10
    def test05_08_corp_user_del_otherCorpId(self):
        '''case05_08:用户从组删除--传入其他组ID(无管理员权限)'''
        pass

    def test05_09_corp_user_del_noCorpId(self):
        '''case05_09:用户从组删除--未传组ID'''
        pass
    
    def test05_10_corp_user_del_haveCorpId(self):
        '''case05_10:用户从组删除--传入组ID(管理员在其他组的ID，暂不考虑)'''
        pass
    
    def test05_11_corp_user_del_noAuth(self):
        '''case05_11:用户从组删除--用户在该组但无管理员权限'''
        pass    


