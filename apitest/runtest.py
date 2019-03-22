import unittest
import json
import requests
import HTMLTestRunner
import time

from apistest_case import ApisTest
from apistep_case import ApistepTest

if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(ApisTest("test_readApiscase"))
    testunit.addTest(ApistepTest("test_readApistepcase"))
    filename = "G:\\autotest\\apitest\\templates\\report.html"
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"全部接口测试报告", description=u"全部接口")
    runner.run(testunit)

    print('Done!')
    time.sleep(1)