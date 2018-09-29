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
    
    