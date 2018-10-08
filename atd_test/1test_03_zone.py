'''园区类接口'''
import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.api_data import CorpApiData as Corp
from base.base_method import BaseMethod
from base.public_param import PublicParam
import unittest


class TestBuilding(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.pub_param = PublicParam()
        cls.super_header = cls.pub_param.get_super_header()
    
    def test01_01_zone_create_noName(self):
        '''case01_01:创建园区--无园区名称'''
        pass
    
    def test01_02_zone_create_noBuildNum(self):
        '''case01_02:创建园区--无楼宇数量'''
        pass
        
    def test01_03_zone_create_noArea(self):
        '''case01_03:创建园区--无面积'''
        pass
    
    def test01_04_zone_create_noLoc(self):
        '''case01_04:创建园区--无地址'''
        pass

    def test01_05_zone_create_noCoord(self):
        '''case01_05:创建园区--无经纬度'''
        pass

    def test01_06_zone_create_noExtra(self):
        '''case01_06:创建园区[ZCM]--无附加信息'''
        pass
    
    def test01_07_zone_create_success(self):
        '''case01_07:创建园区[ZCM]--新增成功(全部信息)'''
        pass
    
    def test01_08_zone_create_nameRepeat(self):
        '''case01_08:创建园区[ZCM]--园区名称重复'''
        pass
    
    def test01_09_zone_create_noCorpId(self):
        '''case01_09:创建园区[ZSM]--无CorpID'''
        pass
    
    def test01_10_zone_create_CorpId(self):
        '''case01_10:创建园区[ZSM]--新增成功(指定CorpID)'''
        pass
    
    def test01_11_zone_create_noRole(self):
        '''case01_11:创建园区--普通组织用户新增'''
        pass  
    

    def test02_01_zone_get_noId(self):
        '''case02_01:获取园区详细信息--无园区ID'''
        pass
    
    def test02_02_zone_get_errId(self):
        '''case02_02:获取园区详细信息[ZCM]--其他组织的园区'''
        pass
    
    def test02_03_zone_get_success(self):
        '''case02_03:获取园区详细信息[ZCM]--所在组织的园区'''
        pass
    
    def test02_04_zone_get_zsm(self):
        '''case02_04:获取园区详细信息[ZSM]'''
        pass

    def test02_05_zone_get_noRole(self):
        '''case02_05:获取园区详细信息--普通组织用户'''
        pass


    def test03_01_zone_list_noPage(self):
        '''case03_01:园区列表--未传page'''
        pass
    
    def test03_02_zone_list_errPageType(self):
        '''case03_02:园区列表--错误的page参数'''
        pass

    def test03_03_zone_list_noSize(self):
        '''case03_03:园区列表--未传size'''
        pass
    
    def test03_04_zone_list_errSizeType(self):
        '''case03_04:园区列表--错误的size参数'''
        pass
    
    def test03_05_zone_list_success(self):
        '''case03_05:园区列表[ZCM]--查看成功(total数量)'''
        pass

    def test03_06_zone_list_zsm(self):
        '''case03_06:园区列表[ZSM]--超级管理员(total数量)'''
        pass

    def test03_07_zone_list_noRole(self):
        '''case03_07:园区列表--组织普通用户'''
        pass
    

    # 编辑园区


    # 删除园区
    def test05_01_zone_del_noId(self):
        '''case05_01:删除园区--无ID'''
        pass
    
    def test05_02_zone_del_success(self):
        '''case05_02:删除园区[ZCM]--删除成功'''
        pass
    
    def test05_03_zone_del_success(self):
        '''case05_03:删除园区[ZSM]--删除成功'''
        pass


 
