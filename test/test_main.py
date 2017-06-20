# coding: utf-8

"""
测试
"""

import unittest
from utils import utils

class MyTest(unittest.TestCase):
    # 初始化工作
    def setUp(self):
        pass

        # 退出清理工作

    def tearDown(self):
        pass

        # 具体的测试用例，一定要以test开头

    def test1(self):
        self.assertEqual(utils.generateUniquePostcardName(), 'test1 fail')

    def test2(self):
        self.assertEqual(utils.hash_email_to_username_fool('zgh@12.com'), 1, 'test2 fail')

if __name__ =='__main__':
    unittest.main()