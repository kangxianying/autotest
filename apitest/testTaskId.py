import re
import requests
import urllib
def TaskId(results):
    global TaskId
    regx = '.*"TaskId":(.*), "PlanId"'
    pm = re.search(regx, results)
    print(pm)
    if pm:
        TaskId = pm.group(1).encode('utf-8')
        print(TaskId)
        return TaskId
    return False

def GetToken():#????
    global token
    url = 'http:// '+HOSTNAME+'/buyer/user/login.do'
    params = {
        'phone': '2312444',
        'pwd': '123456',
    }
    request = urllib.request(url = url, data = urllib.urlencode(params))
    response = urllib.urlopen(request)
    data = response.read()
    regx = '.*"token":"(.*)","niceName"'
    pm = re.search(regx, data)
    if pm:
        token = pm.group(1)
        return token
    return False

def preOrderSN(results):
    global preOrderSN
    regx = '.*"preOrderSN":"(.*)","toHome"'
    pm = re.search(regx, results)
    if pm:
        preOrderSN = pm.group(1).encode('utf-8')
        return preOrderSN
    return False






if __name__ == '__main__':
    results = '"TaskId":123456, "PlanId"'
    value = TaskId(results)
    print (value.decode('utf-8'))
    print ('Done!')


