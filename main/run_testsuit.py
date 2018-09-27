'''
用例集
'''

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import datetime
import HTMLTestRunner
import unittest
from util.send_email import SendEmail
from zyt_test.test_04_course import TestCourse
from zyt_test.test_02_activity import TestActivityAView,TestActivityBSignUp


'''添加用例集'''
testCourse = unittest.TestLoader().loadTestsFromTestCase(TestCourse)
testActivityView = unittest.TestLoader().loadTestsFromTestCase(TestActivityAView)
testActivitySignUp = unittest.TestLoader().loadTestsFromTestCase(TestActivityBSignUp)

suite = unittest.TestSuite([testCourse ,testActivityView,testActivitySignUp])

# 生成HTML的报告
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
time = datetime.datetime.now().date()
filepath = r"{}\report\report{}.html".format(rootPath, time)
fp = open(filepath, 'wb')
runner = HTMLTestRunner.HTMLTestRunner(
    stream=fp, verbosity=2, title="ZTY Interface Testing")
runner.run(suite)
fp.close()

report_name = "report2{}".format(filepath.split("report2")[1])
send_email = SendEmail()
send_email.send_main(filepath, report_name)
