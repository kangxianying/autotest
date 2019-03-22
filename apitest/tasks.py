# -*- coding:utf-8 -*-

import requests, time, sys, re
import urllib, zlib
import pymysql

import unittest
from trace import CoverageResults  #查看代码覆盖率

import json
from idlelib.rpc import response_queue  #队列,线程间最常用的交换数据的形式
from apitest.celery import app

from time import sleep

import os
from selenium import webdriver
#from appium import webdriver


PATH = lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__),p))
global driver

@app.task
def hello_world():
    print('已运行')

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task
def apisauto_testcase():
    sql = "SELECT id,apiname,apiurl,apimethod,apiparamvalue,apiresult,apistatus from apitest_apis "
    coon = pymysql.connect(user='root', passwd='test123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
    cursor = coon.cursor()
    aa = cursor.execute(sql)
    info = cursor.fetchmany(aa)
    print(info)
    for ii in info:
        case_list = []
        case_list.append(ii)
        interfaceTest1(case_list)
    coon.commit()
    cursor.close()
    coon.close()

def interfaceTest1(case_list):
    res_flags = []
    request_urls = []
    responses = []
    strinfo = re.compile('{seturl}')
    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[1]
            url = case[2]
            method = case[3]
            param = case[4]
            res_check = case[5]
        except Exception as e:
            return '测试用例格式不正确！%s'%e
        if param == '':
            new_url = 'http://' +url
        elif param == 'null':
            url = strinfo.sub(str(seturl('seturl')),url)
            new_url = 'http://' +url
        else:
            url = strinfo.sub(str(seturl('seturl')), url)
            new_url = 'http://' + url
            request_urls.append(new_url)
        if method.upper() =='GET':
            headers = {'Authorization':'', 'Content-Type':'application/json'}
            if "=" in urlParam(param):
                data = None
                print(str(case_id)+ 'request is get' + new_url.encode('utf-8') + '?' + urlParam(param).encode('utf-8'))




def seturl(set):
    global setvalue
    sql = "SELECT `setname`,`setvalue` from set_set"
    coon = pymysql.connect(user='root',passwd='test123456',db='autotest',port=3306,host='127.0.0.1',charset='utf8')
    cursor = coon.cursor()
    aa = cursor.execute(sql)
    info = cursor.fetchmany(aa)
    print(info)
    coon.commit()
    cursor.close()
    coon.close()
    if info[0][0] ==set:
        setvalue = info[0][1]
        print(setvalue)
    return setvalue

def urlParam(param):
    paraml = param.replace('&quot;','"')
    return paraml

