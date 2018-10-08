'''建筑类接口'''
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
    
    def test01_01_building_create_noName(self):
        '''case01_01:创建建筑--无建筑名称'''
        pass

    def test01_02_building_create_noLoc(self):
        '''case01_02:创建建筑--无地址'''
        pass
    
    def test01_03_building_create_noArea(self):
        '''case01_03:创建建筑--无面积'''
        pass
    
    def test01_04_buliding_create_noLayer(self):
        '''case01_04:创建建筑--无层数'''
        pass
    
    def test01_05_buliding_create_noUnderlayer(self):
        '''case01_05:创建建筑--无地下层数'''
        pass
    
    def test01_06_building_create_noCoord(self):
        '''case01_06:创建建筑--无经纬度'''
        pass
    
    def test01_07_building_create_noZoneId(self):
        '''case01_07:创建建筑[ZCM]--不属于园区建筑'''
        pass

    def test01_08_building_create_ZoneId(self):
        '''case01_08:创建建筑[ZCM]--属于园区建筑'''
        pass

    def test01_09_building_create_success(self):
        '''case01_09:创建建筑[ZCM]--新增成功(全部信息)'''
        pass
    
    def test01_10_building_create_nameRepeat(self):
        '''case01_10:创建建筑[ZCM]--名称重复(无ZoneID,不同的corp_id)'''
        pass

    def test01_11_building_create_nameRepeat(self):
        '''case01_11:创建建筑[ZCM]--名称重复(相同ZoneID)'''
        pass

    def test01_12_building_create_nameRepeat(self):
        '''case01_12:创建建筑[ZCM]--名称重复(不同ZoneID)'''
        pass

    def test01_13_building_create_rsm(self):
        '''case01_13:创建建筑[ZSM]--超级管理员新增(角色受限)'''
        pass

    def test01_14_building_create_noRole(self):
        '''case01_13:创建建筑--普通公组织用户新增(角色受限)'''
        pass


    def test02_01_building_get_noId(self):
        '''case02_01:获取建筑详细信息--无建筑ID'''
        pass
    
    def test02_02_building_get_errId(self):
        '''case02_02:获取建筑详细信息[ZCM]--其他组织的建筑'''
        pass
    
    def test02_03_building_get_success(self):
        '''case02_03:获取建筑详细信息[ZCM]--所在组织的建筑'''
        pass
    
    def test02_04_building_get_zsm(self):
        '''case02_04:获取建筑详细信息[ZSM]'''
        pass

    def test02_06_building_get_noRole(self):
        '''case02_06:获取建筑详细信息--普通组织用户'''
        pass


    def test03_01_building_list_noPage(self):
        '''case03_01:建筑列表--未传page'''
        pass
    
    def test03_02_building_list_errPageType(self):
        '''case03_02:建筑列表--错误的page参数'''
        pass

    def test03_03_building_list_noSize(self):
        '''case03_03:建筑列表--未传size'''
        pass
    
    def test03_04_building_list_errSizeType(self):
        '''case03_04:建筑列表--错误的size参数'''
        pass
    
    def test03_05_building_list_success(self):
        '''case03_05:建筑列表[ZCM]--查看成功(total数量)'''
        pass

    def test03_06_building_list_zsm(self):
        '''case03_06:建筑列表[ZSM]--超级管理员(total数量)'''
        pass

    def test03_07_building_list_noRole(self):
        '''case03_07:建筑列表--组织普通用户'''
        pass
