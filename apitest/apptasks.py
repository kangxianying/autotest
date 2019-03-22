# -*- coding:utf-8 -*-

import requests,time,sys,re
import urllib,zlib
import pymysql

import unittest
from trace import CoverageResults  #跟踪或跟踪Python语句执行
import json
from idlelib.rpc import response_queue   #
from apitest.celery import app

from time import sleep

import os
from appium import webdriver

PATH = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__), p))

global driver

# 在appium server 与手机端建立会话关系时，手机端需要告诉服务端设备相关的一些参数，
# 根据这些参数服务端可以做出相应的处理。
@app.task
def appauto_testcase(self): #app例
    desired_caps = {}
    # 设备系统
    desired_caps['platformName'] = 'Android'
    # 设备系统版本号
    desired_caps['platformVersion'] = '19'
    # 设备名称，必须有！
    desired_caps['deviceName'] = 'Android Emulator'
    # desired_caps['app'] = r'D:\test\test.apk' #被测试的APP在电脑的路径
    # 应用的包名,在参数中如果添加了应用的安装路径，就可以不用写包名和启动的activity参数
    desired_caps['appPackage'] = 'com.android.calculator2'
    desired_caps['appActivity'] = '.Calculator'
    time.sleep(1)
    self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    time.sleep(1)
    sql = "SELECT id,appfindmethod, appevelement, appoptmethod,appassertdata,`apptestresult` from apptest_appcasestep where apptest_appcasestep.Appcase_id=1 ORDER BY id ASC "
    coon = pymysql.connect(user='root',passwd='test123456',db='autotest',port=3306,host='127.0.0.1',charset='utf8')
    cursor = coon.cursor()
    aa = cursor.execute(sql)
    info = cursor.fetchmany(aa)
    for ii in info:
        case_list = []
        case_list.append(ii)
        apptestcase(self,case_list)
    coon.commit()
    cursor.close()
    coon.close()
    self.driver.quit()



def apptestcase(self,case_list):
    for case in case_list:
        try:
            case_id = case[0]
            findmethod = case[1]
            evelement = case[2]
            optmethod = case[3]
        except Exception as e:
            return '测试用例格式不正确！%s'%e
        print(evelement)
        time.sleep(10)
        if optmethod== 'click' and findmethod=='find_element_by_id':
            self.driver.find_element_by_id(evelement).send_keys('test')
        elif optmethod== 'click' and findmethod=='find_element_by_name':
            self.driver.find_element_by_name(evelement).click()
        elif optmethod=='sendkey':
            self.driver.find_element_by_name(evelement).send_keys()














