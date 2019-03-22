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

class ApiTest(unittest.TestCase):
    #读取数据库中的单一流程接口测试用例，这个可以从页面添加
    def test_readApiscase(self):
        sql = "SELECT id,apiname,apiurl,apimethod,apiparamvalue,apiresult,apistatus from apitest_apis "
        coon = pymysql.connect(user='root',passwd='123456',db='autotest',port=3306,host='127.0.0.1',charset='utf8')
        cursor = coon.cursor()
        aa = cursor.execute(sql)
        info = cursor.fetchmany(aa)
        print(info)#这里返回元组()  ((2, '百度搜索', 'https://www.baidu.com/', 'get', 's?wd=谷歌', '谷歌', 0),)
        for ii in info:
            case_list = []
            case_list.append(ii)
            print(case_list)#这里返回列表[]  [(2, '百度搜索', 'https://www.baidu.com/', 'get', 's?wd=谷歌', '谷歌', 0)]
            interfaceTest(case_list)
        coon.commit()
        cursor.close()
        coon.close()

    #读取测试用例，并执行，判断结果，记录结果，有bug记录进bug管理系统
    def interfaceTest(case_list):
        res_flags = []
        request_urls = []
        responses = []
        strinfo = re.compile('{seturl}') #正则表达式
        for case in case_list:
            try:
                case_id = case[0]
                interface_name = case[1]
                print(interface_name)   #百度搜索
                url = case[2]
                method = case[3]
                param = case[4]
                print(param)  #s?wd=谷歌
                res_check = case[5]
                print(res_check)
            except Exception as e:
                return '测试用例格式不对 %s' %e
            if param=='':
    #            如果请求参数是空的话，请求报文就是url，然后把请求报文存到请求报文list中

                #new_url = 'http://'+'api.test.com.cn'+url
                new_url = url
                request_urls.append(new_url)

            elif param=='null':
                url = strinfo.sub(str(seturl('seturl')),url)
                new_url = 'http://' +url

            elif '{' in param:
                new_url = url
                request_urls.append(new_url)
            else:

                url = strinfo.sub(str(seturl('seturl')), url)
                print(url)
                new_url = url + '?' + urlParam(param)  # 请求报文
                print(new_url)
                request_urls.append(new_url)

            if method.upper() == 'GET':
                print(new_url)
                headers = {
                    'Authorization':'',
                    'Content-Type':'application/json',
                }
                if "=" in urlParam(param):
                    data = None
    #                print(str(case_id)+' request is get' + str(new_url.encode('utf-8'))+ '?' +str(urlParam(param).encode('utf-8')))

                    results = requests.get(new_url).text
                    print('response is get' + results)
                    responses.append(results)
                    res = readRes(results, res_check)

                else:
                    print('request is get '+ new_url+'body is'+ urlParam(param))
                    data = urlParam(param)
                    req = urllib.request.Request(url=new_url,data=data,headers=headers,method="GET")
                    try:
                        results = urllib.request.urlopen(req).read()
                        print('response is get')
                        print(results)
                    except Exception as e:
                        return caseWriteResult(case_id,'0')
                    res = readRes(results,res_check)
                if 'pass' == res:
                    res_flags.append('pass')
                    writeResult(case_id,'1')
                    caseWriteResult(case_id,'1')
                else:
                    res_flags.append('fail')
                    writeResult(case_id,'0')
                    caseWriteResult(case_id,'0')
                    writeBug(case_id,interface_name,new_url,results,res_check)


            if method.upper()=="POST":
                headers={
    #                'Authorization': 'Credential' + id,
                    'Content-Type': 'application/json'
                }
                if "=" in urlParam(param):
                    data = None
                    results = requests.patch(new_url + '?' +urlParam(param),data,headers=headers).text
                    print('response is post' + results.encode('utf-8'))
                    responses.append(results)
                    res = readRes(results, '')
                else:
                    print(str(case_id)+' request is '+ url + '  body is ' + str(urlParam(param)))
                    #form = json.dumps(param)
                    results = requests.post(new_url,data=param,headers=headers).text
                    print('response is post'+ str(results))
                    responses.append(results)
                    res = readRes(results,res_check)
                if 'pass' == res:
                    writeResult(case_id, '1')
                    res_flags.append('pass')
                    caseWriteResult(case_id, '1')
                else:
                    writeResult(case_id, '0')
                    res_flags.append('fail')
                    caseWriteResult(case_id, '0')
                    writeBug(case_id, interface_name, new_url, results, res_check)


    def readRes(res, res_check):
        res = str(res.replace('":"',"=").replace('":',"="))
        print(res)
        res_check = res_check.split(':')
        print(res_check)
        for s in res_check:
            if s in res:
                pass
            else:
                return '错误，返回参数和预期结果不一致'+s
        return 'pass'

    def urlParam(param):
        param1 = param.replace('&quot;','"')
        return param1

    def CredentialId():
        global id
        url = 'http://' + 'api.test.com.cn'+'/api/Security/Authentication/Signin/web'
        body_data = json.dumps({"Identity":'test',"Password":'test'})
        headers = {
            'Connection':'keep-alive',
            'Content-Type':'application/json'
        }
        response = requests.post(url=url,data=body_data,headers=headers)
        data = response.text
        regx = '.*"CredentialId":"(.*)","Scene"'
        pm = re.search(regx,data)
        id = pm.group(1)

    def seturl(set):
        global setvalue
        sql = "SELECT setname,setvalue from set_set"
        coon = pymysql.connect(user='root',passwd='123456',db='autotest',port=3306,host=HOSTNAME,charset='utf8')
        cursor = coon.cursor()
        aa = cursor.execute(sql)
        info = cursor.fetchmany(aa)
        print('info is ')
        print(info) #(('testurl', '127.0.0.1'),)
        coon.commit()
        cursor.close()
        coon.close()
        if info[0][0] == set:
            setvalue = info[0][1]
            print('setvalue is '+ setvalue)
            return setvalue

    #流程接口的结果写入
    def writeResult(case_id,result):
        result = result.encode('utf-8')
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now)
        param = (result, now, case_id)
        sql = "UPDATE apitest_apis set `apistatus`=%s, `create_time`=%s  WHERE `id`=%s;"#, (str(result), str(now), str(case_id))
        print('api autotest result is '+ result.decode())
        coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host=HOSTNAME, charset='utf8')
        cursor = coon.cursor()
        cursor.execute(sql,param)
        coon.commit()
        cursor.close()
        coon.close()

    def caseWriteResult(case_id,result):
        result = result.encode('utf-8')
        print(str(result))
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE apitest_apitest set apitest_apitest.apitestresult=%s, apitest_apitest.create_time=%s where apitest_apitest.id=%s;"
        param = (result, now, case_id)
        print('api autotest result is ' + result.decode())
        coon = pymysql.connect(user='root', passwd='123456', db='autotest', port=3306, host='127.0.0.1', charset='utf8')
        cursor = coon.cursor()
        cursor.execute(sql, param)
        coon.commit()
        cursor.close()
        coon.close()

    #bug记录进bug管理表
    def writeBug(bug_id,interface_name,request,response,res_check):
        interface_name = interface_name.encode('utf-8')
        #res_check = res_check.encode('utf-8')
        request = request.encode('utf-8')
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        bugname = str(bug_id) + '_' + interface_name.decode() + '_出错了'
        bugdetail = '[请求数据]<br />' + str(request) + '<br/>' + '[预期结果]<br/>' + str(res_check) + '<br/>' + '<br/>' + '[响应数据]<br />' + '<br/>' + str(response)
        print(bugdetail)
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

    test_readSQLcase()
    print('Done')
    time.sleep(1)




