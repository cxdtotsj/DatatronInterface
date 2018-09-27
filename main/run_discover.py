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


'''添加用例集'''
# 获取test目录路径
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
case_path = os.path.join(rootPath, "zyt_test")

suite = unittest.defaultTestLoader.discover(case_path, pattern="test*.py")

'''生成HTML的报告'''
time = datetime.datetime.now().date()
filepath = r"{}\report\report{}.html".format(rootPath, time)
fp = open(filepath, 'wb')
runner = HTMLTestRunner.HTMLTestRunner(
    stream=fp, verbosity=2, title="ZTY Interface Testing")
runner.run(suite)
fp.close()

'''发送邮件'''
report_name = "report2{}".format(filepath.split("report2")[1])
send_email = SendEmail()
send_email.send_main(filepath, report_name)
