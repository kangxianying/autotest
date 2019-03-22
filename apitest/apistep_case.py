import requests,time,re,sys #?
import urllib,zlib #?
import pymysql
import HTMLTestRunner #?
import unittest #?
from trace import CoverageResults #?
import json
from idlelib.rpc import response_queue  #?
from time import sleep

HOSTNAME = '127.0.0.1'

class ApistepTest(unittest.TestCase):
    def setup(self):
        time.sleep(1)

    def test_readApistepcase(self):
        sql = "SELECT id, apiname, apiurl, apimethod, apiparamvalue, apiresult, apistatus ,Apitest_id from apitest_apistep"
        coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
        cursor = coon.cursor()
        aa = cursor.execute(sql)
        info = cursor.fetchmany(aa)
        for ii in info:
            case_list = []
            case_list.append(ii)
            print (case_list)
            res = interfaceTest(case_list)
            print(res)
            # try:
            #     assert res == 'pass'
            # except AssertionError as e:
            #     print("出错")
            assert res == 'pass'


        coon.commit()
        cursor.close()
        coon.close()


    def teardown(self):
        time.sleep(1)
# def test_readApistepcase():
#         sql = "SELECT id, apiname, apiurl, apimethod, apiparamvalue, apiresult, apistatus ,Apitest_id from apitest_apistep"
#         coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
#         cursor = coon.cursor()
#         aa = cursor.execute(sql)
#         info = cursor.fetchmany(aa)
#         for ii in info:
#             case_list = []
#             case_list.append(ii)
#             print (case_list)
#             res = interfaceTest(case_list)
#             print(res)
#             try:
#                 assert res == 'pass'
#             except AssertionError as e:
#                 print("出错")
#
#
#
#         coon.commit()
#         cursor.close()
#         coon.close()

def interfaceTest(case_list):
    res_flags = []
    request_urls = []
    responses = []
    # strinfo = re.compile('{seturl}') #需要传递的参数
    # strinfo2 = re.compile('{TaskId}')#需要传递的参数
    # tasknoinfo = re.compile('{taskno}')#需要传递的参数

    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[1]
            method = case[3]
            url = case[2]
            param = case[4]
            print(param)
            res_check = case[5]
            print(res_check)
            Apitest_id = case[7]
        except Exception as e:
            return '测试用例格式不正确！%s'%e
        if param== '':
            new_url = url
            request_urls.append(new_url)
        elif param== 'null':
            url = strinfo.sub(str(seturl('seturl')),url)
            new_url = 'http://'+url

        elif '{' in param:
            new_url = url
            print(new_url)
            request_urls.append(new_url)

        else:
          # #  url = schemainfo.sub(mod_config.getConfig('project', "schema"),url)
          #   url = strinfo.sub(str(seturl('seturl')),url)
          # #  url = strinfo2.sub(TaskId,url)
          #   param = strinfo.sub(TaskId,param)
          #   param = tasknoinfo.sub(taskno,param)
          #   new_url = 'http://'+url
          #   request_urls.append(new_url)
          url = strinfo.sub(str(seturl('seturl')), url)
          print(url)
          new_url = url + '?' + urlParam(param)  # 请求报文
          print(new_url)
          request_urls.append(new_url)

        if method.upper() == 'GET':
            print(new_url)
            headers = {
                'Authorization': '',
                'Content-Type': 'application/json',
            }
            if "=" in urlParam(param): #为不带json body的
                data = None
                #                print(str(case_id)+' request is get' + str(new_url.encode('utf-8'))+ '?' +str(urlParam(param).encode('utf-8')))

                results = requests.get(new_url).text
                print('response is get' + results)
                responses.append(results)
                res = readRes(results, res_check)  #结果判断


            else: #带json body
                print('request is get ' + new_url + 'body is' + urlParam(param))
                data = urlParam(param)
                req = urllib.request.Request(url=new_url, data=data, headers=headers, method="GET")
                try:
                    results = urllib.request.urlopen(req).read()
                    print('response is get')
                    print(results)
                except Exception as e:
                    return caseWriteResult(case_id, '0')
                res = readRes(results, res_check) #结果判断


            if 'pass' == res:
                res_flags.append('pass')
                writeResult(case_id,results, '1')
                caseWriteResult(Apitest_id, '1')
            else:
                res_flags.append('fail')
                writeResult(case_id, results,'0')
                caseWriteResult(Apitest_id, '0')
            writeBug(case_id, interface_name, new_url, results, res_check)
            return res


        if method.upper() == "POST":
            headers = {
                #                'Authorization': 'Credential' + id,
                'Content-Type': 'application/json'
            }
            if "=" in urlParam(param):
                data = None
                results = requests.patch(new_url + '?' + urlParam(param), data, headers=headers).text
                print('response is post' + results.encode('utf-8'))
                responses.append(results)
                res = readRes(results, res_check)

            else:
                print(str(case_id) + ' request is ' + url + '  body is ' + str(urlParam(param)))
                # form = json.dumps(param)
                results = requests.post(new_url, data=param, headers=headers).text
                print('response is post' + str(results))
                responses.append(results)
                res = readRes(results, res_check)


            if 'pass' == res:
                writeResult(case_id,results, '1')
                res_flags.append('pass')
                caseWriteResult(Apitest_id, '1')
            else:
                writeResult(case_id,results, '0')
                res_flags.append('fail')
                caseWriteResult(Apitest_id, '0')
                writeBug(case_id, interface_name, new_url, results, res_check)
            return res
        # assert "pass" in res



def readRes(res, res_check):
    res = str(res.replace('":"',"=").replace('":',"="))
    res_check = res_check.split(';')
    for s in res_check:
        if s in res:
            pass
        else:
            return '错误，返回参数和预期结果不一致' + s
    return 'pass'


def urlParam(param):
    param1 = param.replace('&quot;', '"')
    return param1


def CredentialId():
    global id
    url = 'http://' + 'api.test.com.cn' + '/api/Security/Authentication/Signin/web'
    body_data = json.dumps({"Identity": 'test', "Password": 'test'})
    headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json'}
    response = requests.post(url=url, data=body_data, headers=headers)
    data = response.text
    regx = '.*"CredentialId":"(.*)","Scene"'
    pm = re.search(regx, data)
    id = pm.group(1)


def seturl(set):
    global setvalue
    sql = "SELECT `setname`,`setvalue` from set_set"
    coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
    cursor = coon.cursor()
    aa = cursor.execute(sql)
    info = cursor.fetchmany(aa)
    print  (info)
    coon.commit()
    cursor.close()
    coon.close()
    if info[0][0] == set:
        setvalue = info[0][1]
        print (setvalue)
    return setvalue


def preOrderSN(results):
    global preOrderSN
    regx = '.*"preOrderSN":"(.*)","toHome"'
    pm = re.search(regx, results)
    if pm:
        preOrderSN = pm.group(1).encode('utf-8')
        return preOrderSN
    return False


def TaskId(results):
    global TaskId
    regx = '.*"TaskId":(.*),"PlanId"'
    pm = re.search(regx, results)
    if pm:
        TaskId = pm.group(1).encode('utf-8')
        #  print TaskId
        return TaskId
    return False


def taskno(param):
    global taskno
    a = int(time.time())
    taskno = 'task_' + str(a)
    return taskno


def writeResult(case_id, response, result): #流程接口中单个结果
    result = result.encode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE apitest_apistep set apitest_apistep.apiresponse=%s,apitest_apistep.apistatus=%s,apitest_apistep.create_time=%s where apitest_apistep.id=%s;"
    param = (response, result, now, case_id)
    print ('api autotest result is ' + result.decode())
    coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
    cursor = coon.cursor()
    cursor.execute(sql, param)
    coon.commit()
    cursor.close()
    coon.close()


def caseWriteResult(case_id, result): #流程接口中总结果
    result = result.encode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE apitest_apitest set apitest_apitest.apitestresult=%s,apitest_apitest.create_time=%s where apitest_apitest.id=%s;"
    param = (result, now, case_id)
    print ('api autotest result is ' + result.decode())
    coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
    cursor = coon.cursor()
    cursor.execute(sql, param)
    coon.commit()
    cursor.close()
    coon.close()


def writeBug(bug_id, interface_name, request, response, res_check): #每个接口的bug
    #interface_name = interface_name.encode('utf-8')
    # res_check = res_check.encode('utf-8')
    # request = request.encode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    bugname = str(bug_id) + '_' + str(interface_name) + '_出错了'
    bugdetail = '[请求数据]<br />' + str(request) + '<br/>' + '[预期结果]<br/>' + str(res_check) + '<br/>' + '<br/>' + '[响应数据]<br />' + '<br/>' + str(response)
    print (bugdetail)
    sql = "INSERT INTO `bug_bug` (" \
          "`bugname`,`bugdetail`,`bugstatus`,`buglevel`, `bugcreater`, `bugassign`,`created_time`,`Product_id`)  " \
          "VALUES ('%s','%s','激活','3','kxy', 'kxy', '%s', '2');" % (bugname, pymysql.escape_string(bugdetail), now)
    coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
    cursor = coon.cursor()
    cursor.execute(sql)
    coon.commit()
    cursor.close()
    coon.close()


if __name__ == '__main__':
    #test_readApistepcase()
    #unittest.main()
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    testunit = unittest.TestSuite()
    #testunit.addTest(ApisTest("test_readApiscase"))
    testunit.addTest(ApistepTest("test_readApistepcase"))
    filename = "G:\\autotest\\apitest\\templates\\report.html"
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"全部接口测试报告", description=u"全部接口",verbosity=2)
    runner.run(testunit)
    fp.close()

    print('Done!')
    time.sleep(1)